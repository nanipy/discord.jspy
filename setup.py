from js import Array, require, String;

setuptools = require("setuptools");
re = require("re");

requirements = Array();
with open('requirements.txt') as f:
  requirements = Array([String(f.read())._split("\n")]);

version = String();
with open('discord/__init__.py') as f:
    version = String(f.read()).match('__version__\s*=\s*[\'"]([^\'"]*)[\'"]')[0];

if not version:
    raise RuntimeError('version is not set');

if version.endsWith((String('a'), String('b'), String('rc'))):
    # append version identifier based on commit count
    try:
        subprocess = require("subprocess");
        p = subprocess.Popen(Array([String('git'), String('rev-list'), String('--count'), String('HEAD')]),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE);
        out, err = p.communicate();
        if out:
            version = version.concat(out.decode(String('utf-8')).strip());
        p = subprocess.Popen(Array([String('git'), String('rev-parse'), String('--short'), String('HEAD')]),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE);
        out, err = p.communicate();
        if out:
            version = version.concat(String('+g').concat(String(out.decode('utf-8')).strip()));
    except Exception:
        pass;

readme = String();
with open('README.rst') as f:
    readme = String(f.read());

extras_require = {
    String('voice'): Array([String('PyNaCl==1.2.1')]),
    String('docs'): Array([
        String('sphinx==1.7.4'),
        String('sphinxcontrib-asyncio'),
        String('sphinxcontrib-websupport'),
    ])
};

setuptools.setup(name=String('discord.py'),
      author=String('Rapptz'),
      url=String('https://github.com/Rapptz/discord.py'),
      version=version,
      packages=Array([String('discord'), String('discord.ext.commands')]),
      license=String('MIT'),
      description=String('A python wrapper for the Discord API'),
      long_description=readme,
      include_package_data=True,
      install_requires=requirements,
      extras_require=extras_require,
      python_requires=String('>=3.5.3'),
      classifiers=Array([
        String('Development Status :: 4 - Beta'),
        String('License :: OSI Approved :: MIT License'),
        String('Intended Audience :: Developers'),
        String('Natural Language :: English'),
        String('Operating System :: OS Independent'),
        String('Programming Language :: Python :: 3.5'),
        String('Programming Language :: Python :: 3.6'),
        String('Programming Language :: Python :: 3.7'),
        String('Topic :: Internet'),
        String('Topic :: Software Development :: Libraries'),
        String('Topic :: Software Development :: Libraries :: Python Modules'),
        String('Topic :: Utilities'),
      ])
);
