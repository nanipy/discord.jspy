import asyncio
import contextlib
import importlib
import inspect
import io
import pydoc
import typing

import discord
from discord.ext import commands
import import_expression
import jishaku.cog
from jishaku.cog import SEMICOLON_LOOKAROUND
from jishaku import utils

# normally i avoid redirect_stdout in async code
# but since this function is blocking anyway, it's fine
# also we use pydoc.help instead of pydoc.render_doc
# because the latter does not support topics, such as help('OPERATORS')
# also, even though pydoc.Helper supports a custom output var,
# it is not written to for help topics either
def help(x):
	"""Show documentation on a function, class, module, or help topic."""
	out = io.StringIO()
	with contextlib.redirect_stdout(out):
		pydoc.help(x)
	cleaned = out.getvalue().replace('`', '\N{zero width space}`')
	return '```\n' + cleaned + '\n```'

class ImportExpressionJishaku(jishaku.cog.Jishaku):
	def __init__(self, bot):
		super().__init__(bot)
		self.repl_global_scope = {
			'_bot': self.bot,
			'asyncio': asyncio,
			'discord': discord,
			'commands': discord.ext.commands,
			'help': help,

			import_expression.constants.IMPORTER: importlib.import_module,
		}

	async def repl_backend(self, ctx: commands.Context, code: str, callback):
		"""
		Attempt to compile and execute code, yielding results to a callback.
		:param ctx: Context for the repl environment and callback.
		:param code: Code to try and execute
		:param callback: Callback to send all results to.
		:return: The final result, if there was one.
		"""

		if "\n" not in code and not any(SEMICOLON_LOOKAROUND.findall(code)):
			# if there are no line breaks and no semicolons try eval mode first
			with_return = ' '.join(['return', code])

			try:
				# try to compile with 'return' in front first
				# this lets you do eval-like expressions
				coro_format = utils.repl_coro(with_return)
				code_object = import_expression.compile(coro_format, '<repl-v session>', 'exec')
			except SyntaxError:
				code_object = None
		else:
			code_object = None

		# we set as None and check here because nesting looks worse and complicates the traceback
		# if this code fails.

		if code_object is None:
			coro_format = utils.repl_coro(code)
			code_object = import_expression.compile(coro_format, '<repl-x session>', 'exec')

		# ensure that changes to the global scope are not persistent across invocations
		global_scope = self.repl_global_scope.copy()

		exec(code_object, global_scope)

		# Grab the coro we just defined
		extracted_coro = global_scope["__repl_coroutine"]

		result = None

		# Allow async generator definitions for multiple-result yielding
		if inspect.isasyncgenfunction(extracted_coro):
			# For every result we get back,
			async for result in extracted_coro(ctx):
				# send it to the callback.
				await callback(ctx, result)
		else:
			# Not an async generator, so await with local scope args
			result = await extracted_coro(ctx)
			await callback(ctx, result)

		return result

	@staticmethod
	async def py_callback(ctx: commands.Context, result) -> typing.Optional[discord.Message]:
		"""
		Callback that converts the result into a chat-compatible format and sends it to the chat.
		:param ctx: Context, passed by caller
		:param result: The object to be converted
		:return: The message sent
		"""
		if result is None:
			return

		if isinstance(result, discord.Embed):
			return await ctx.send(embed=result)

		if isinstance(result, discord.File):
			return await ctx.send(file=result)

		if not isinstance(result, str):
			result = repr(result)

		if len(result) > 2000:
			file = discord.File(fp=io.StringIO(result), filename='output.txt')
			return await ctx.send('Output too long.', file=file)

		if not result.strip():
			result = '\N{zero width space}'

		return await ctx.send(result)

def setup(bot):
	bot.add_cog(ImportExpressionJishaku(bot))
