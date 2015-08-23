Any feature work will now be in "platinfo 2.x" (currently on the trunk, will use a new "platinfo2" module name to avoid compat nightmares). See PlatinfoVersions for details.

# Naming changes #

  * I'm considering using "mac" instead of "macosx" for `PlatInfo.os` on Mac. Certainly not decided though. I guess my main motivation is that a sufficiently unambiguous platform name for a universal Mac package is "mac" ("macosx" seems a bit pointless).
  * The libstdc++ version is one of the `PlatInfo` fields gathered on Linux. In platinfo 0.x this field is call `libcpp`. The original reason for that was to avoid `+` if the field were used in filenames. I think that was a mistake. The name should be `libstdc++` or possibly `libstdcpp`.


# Python 3 support #

How to other people typically develop Python packages for 2 and 3? I know about the 2to3 tool, but I curious how people structure their source tree, do releases, etc.


# Porting to other languages #

I would like to port the platinfo library to other languages. The main use I have for this module is for package naming in build systems. I just happen to use Python in the build systems I work with. Presuming the standardized platform naming provided here is reasonable, having Ruby, Perl, Java, etc. versions of this library would allow build tools written in other languages to share the same platform naming.

I don't see it being **likely** that a number of the major build tools provide common platform naming best practices based on this, but I can dream. :)