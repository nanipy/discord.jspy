from js import Array, require, String;

setuptools = require("setuptools");
re = require("re");
os = require("os");

requirements = Array();
with open('requirements.txt') as f:
  requirements = Array([String(f.read())._split("\n")]);

version = String();
with open('discordjspy/__init__.py') as f:
    version = String(f.read()).match(String('__version__\s*=\s*[\'"]([^\'"]*)[\'"]'))[0];

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

packages = Array([String('discordjspy'), String('discordjspy.ext.commands')]);

for dir in os.listdir(String('discordjspy{}addons').format(os.sep)):
    dir = String(dir);
    if not dir.endsWith(String('.py')) and not dir.startsWith(String('__')):
        packages.push(String('discordjspy.addons.{}').format(dir));
        for dir2 in os.listdir(String('discordjspy{0}addons{0}{1}').format(os.sep, dir)):
            dir2 = String(dir2);
            if not dir2.endswith(String('.py')) and not dir2.startsWith(String('__')):
                packages.push(String("discordjspy.addons.{}.{}").format(dir, dir2));

extras_require = {
    String('voice'): Array([String('PyNaCl==1.2.1')]),
    String('docs'): Array([
        String('sphinx==1.7.4'),
        String('sphinxcontrib-asyncio'),
        String('sphinxcontrib-websupport'),
    ]),
    String('addons'): Array([
        String('humanize'), # for jishaku
    ])
};

setuptools.setup(name=String('discord.jspy'),
      author=String('nanipy'),
      url=String('https://github.com/nanipy/discord.jspy'),
      version=version,
      packages=packages,
      license=String('MIT'),
      description=String('A discord.py clone with JavaScript flavours'),
      long_description=readme,
      include_package_data=True, # 'include_package_data' must be a boolean value, sadly we can't inherit from bool
      install_requires=requirements,
      extras_require=extras_require,
      python_requires=String('>=3.6'),
      classifiers=Array([
        String('Development Status :: 4 - Beta'),
        String('License :: OSI Approved :: MIT License'),
        String('Intended Audience :: Developers'),
        String('Natural Language :: English'),
        String('Operating System :: OS Independent'),
        String('Programming Language :: Python :: 3.6'),
        String('Programming Language :: Python :: 3.7'),
        String('Topic :: Internet'),
        String('Topic :: Software Development :: Libraries'),
        String('Topic :: Software Development :: Libraries :: Python Modules'),
        String('Topic :: Utilities'),
      ])
);
