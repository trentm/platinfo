Here-in examples of running

```
platinfo -y
```

on various machines. This can help you get an idea of what information `platinfo` provides, and hence whether it might be useful to you. If you've run `platinfo` on an architecture or OS that doesn't seem to be here, please add your own example output. Thanks! Here is how to do so quickly:

```
cd /tmp
rm -f platinfo.py
wget http://platinfo.googlecode.com/svn/branches/0.x/lib/platinfo.py
python platinfo.py -y
```

Then cut 'n paste that output into a comment. Be sure to put your example output in the triple-braces, `{{{ ... }}}`, this Wiki's syntax for a code block.


# Examples #

```
--- platinfo version="0.14.0"
os_name: Mac OS X
darwin_ver: 9.6.0
name: macosx-x86
os: macosx
arch: x86
os_ver: 10.5.6
os_build: 9G55
```