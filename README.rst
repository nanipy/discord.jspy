discord.jspy
==========

.. image:: https://img.shields.io/badge/python-3.6%20%7C%203.7-blue.svg
.. image:: https://img.shields.io/badge/code%20style-JavaScript-lightgrey.svg

discord.jspy is an API wrapper for Discord written in Python using JavaScript code style.

This was written to allow easier writing of bots or chat logs. Make sure to familiarise yourself with the discord.py API using the `documentation <http://discordpy.rtfd.org/en/latest>`__.

Additions to discord.py rewrite
-------------------------------

discord.jspy adds the following features on top of the latest discord.py rewrite version:

- Addon support using `bot.enable`
- Mutiple bot owners

We recommend joining either the `official discord.py server <https://discord.gg/r3sSKJJ>`_ or the `Discord API server <https://discord.gg/discord-api>`_ for help and discussion about the discord.py library.

Installing
----------

To install the library without full voice support, you can just run the following command:

**discord.jspy is not on pypi yet, use the development version!**

.. code:: sh

    python3 -m pip install -U discord.jspy

Otherwise to get voice support you should run the following command:

.. code:: sh

    python3 -m pip install -U discord.jspy[voice]


To install the development version, do the following:

.. code:: sh

    python3 -m pip install -U git+https://github.com/nanipy/discord.jspy

or the more long winded from cloned source:

.. code:: sh

    $ git clone https://github.com/nanipy/discord.jspy
    $ cd discord.jspy
    $ python3 -m pip install -U .[voice]

Please note that on Linux installing voice you must install the following packages via your favourite package manager (e.g. ``apt``, ``yum``, etc) before running the above command:

* libffi-dev (or ``libffi-devel`` on some systems)
* python-dev (e.g. ``python3.6-dev`` for Python 3.6)

Quick Example
------------

.. code:: py

    import discordjspy
    import asyncio

    class MyClient(discordjspy.Client):
        async def on_ready(self):
            print('Logged in as')
            print(self.user.name)
            print(self.user.id)
            print('------')

        async def on_message(self, message):
            # don't respond to ourselves
            if message.author == self.user:
                return
            if message.content.startswith('!test'):
                counter = 0
                tmp = await message.channel.send('Calculating messages...')
                async for msg in message.channel.history(limit=100):
                    if msg.author == message.author:
                        counter += 1

                await tmp.edit(content='You have {} messages.'.format(counter))
            elif message.content.startswith('!sleep'):
                with message.channel.typing():
                    await asyncio.sleep(5.0)
                    await message.channel.send('Done sleeping.')

    client = MyClient()
    client.run('token')

You can find examples in the examples directory.

Requirements
------------

* Python 3.6+
* ``aiohttp`` library
* ``websockets`` library
* ``js.py`` library
* ``PyNaCl`` library (optional, for voice only)

  - On Linux systems this requires the ``libffi`` library. You can install in
    debian based systems by doing ``sudo apt-get install libffi-dev``.

Usually ``pip`` will handle these for you.

