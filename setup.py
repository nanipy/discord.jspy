from setuptools import setup
import re
import os

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

version = ''
with open('discordjspy/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

if version.endswith('a', 'b', 'rc'):
    # append version identifier based on commit count
    try:
        import subprocess
        p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += out.decode('utf-8').strip()
        p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version + ='+g' + out.decode('utf-8').strip()
    except Exception:
        pass

readme = ''
with open('README.rst') as f:
    readme = f.read()

packages = ['discordjspy', 'discordjspy.ext.commands']

for dir in os.listdir('discordjspy{}addons').format(os.sep):
    if not dir.endswith('.py') and not dir.startswith('__'):
        packages.append('discordjspy.addons.{}').format(dir)
        for dir2 in os.listdir('discordjspy{0}addons{0}{1}').format(os.sep, dir):
            if not dir2.endswith('.py') and not dir2.startswith('__'):
                packages.append('discordjspy.addons.{}.{}').format(dir, dir2)

extras_require = {
    'voice': ['PyNaCl==1.2.1'],
    'docs': [
        'sphinx==1.7.4'),
        'sphinxcontrib-asyncio'),
        'sphinxcontrib-websupport'),
    ],
    'addons': ['humanize'] # for jishaku
}

setup(name='discord.jspy'),
      author='nanipy',
      url='https://github.com/nanipy/discord.jspy',
      version=version,
      packages=packages,
      license='MIT',
      description='A discord.py clone with JavaScript flavours',
      long_description=readme,
      include_package_data=True,
      install_requires=requirements,
      extras_require=extras_require,
      python_requires='>=3.6',
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
      ]
)
