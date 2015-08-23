There are currently two active (aka maintained) streams of platinfo.

# platinfo 0.x #

  * stable
  * Will preserve backwards compatibility -- which basically amounts to not making changes to platform names (modulo bugs).
  * maintained in the "branches/0.x" branch.

# platinfo 2.x #

  * new "platinfo2" module name to avoid compat nightmares
  * current unstable: this stream is still in early stages of changing platform names
  * developed in the trunk

## how 2.x differs from 0.x ##

  * (planned) Will use "windows" for `PlatInfo.os` instead of "win32" or "win64". The old names were imperfect and misleading references to either what used to be called the "win32 API" (but is now the [Windows API](http://en.wikipedia.org/wiki/Windows_api)).
  * see also the thoughts in FutureWork