This is a small Python module that determines and returns standardized names for platforms, where the "standard" is Trent Mick's reasoning :) from experience building ActivePython on a fairly large number of platforms.

The driving goal is to provide platform names that are:
  * relatively short
  * readable (as much as possible making matching the given name to an actually machine self-explanatory)
  * be capable enough to produce all names needed to distinguish all platform-specific application builds
  * generally safe for usage in filenames
  * not ugly (e.g. "MSWin32" is ugly)

A simple usage example:

```
>>> from platinfo import PlatInfo
>>> pi = PlatInfo()
>>> pi.os
'macosx'
>>> pi.arch
'x86'
>>> pi.name()
'macosx-x86'
```

Currently this has fairly wide OS coverage (Windows, Linux, Mac, Solaris,
HP-UX, AIX). See ExampleOutput.

# Installation #

Use **one** of the following methods:

1. Basic install:

  * download the latest `platinfo-$version.zip`
  * unzip it
  * run `python setup.py install`

2. Install with any of `pip`, `pypm` (if you have ActivePython) or `easy_install`

```
pip install platinfo
pypm install platinfo
easy_install platinfo
```

After installing you should be able to run `platinfo --help` or `import platinfo` and start using it.


# More advanced usage #

A more advanced usage of `platinfo.py`. This is example is run on a SuSE Linux box.

```
>>> from platinfo import PlatInfo
>>> pi = PlatInfo()
>>> pi.os
'linux'
>>> pi.arch
'x86'

# A number of pieces of info gathered (some of them plat-dependent).
>>> pi.as_dict()
{'arch': 'x86',
 'distro': 'SuSE',
 'distro_desc': 'SuSE Linux 9.0 (i586)',
 'distro_ver': '9.0',
 'libcpp': 'libcpp5',
 'lsb_version': '1.3',
 'name': 'linux-x86',
 'os': 'linux',
 'os_ver': '2.4.21'}

# The default name is "<os>-<arch>"...
>>> pi.name()   # default
'linux-x86'
>>> print pi
linux-x86

# ...but that can be customized with some rules.
>>> pi.name('os', 'distro', 'arch')
'linux-suse-x86'
>>> pi.name('os', 'distro+distro_ver', 'arch')
'linux-suse9-x86'
>>> pi.name('os+os_ver[:2]', 'arch')
'linux2.4-x86'
>>> pi.name('os', 'arch', sep='/')
'linux/x86'

# The full name provide a little bit more info.
>>> pi.fullname()
'linux2.4-suse9-x86'

# platname() is a shortcut for PlatInfo.name(...).
>>> from platinfo import platname
>>> platname('os', 'distro', 'arch')
'linux-suse-x86'
```