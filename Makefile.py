
"""Makefile for the platinfo project.

${common_task_list}

See `mk -h' for options.
"""

import sys
import os
from os.path import join, dirname, normpath, abspath, exists, basename
import re
import webbrowser
from glob import glob

from mklib.common import MkError
from mklib import Task
from mklib import sh



class bugs(Task):
    """Open bug database page."""
    def make(self):
        webbrowser.open("http://code.google.com/p/platinfo/issues/list")

class site(Task):
    """Open the Google Code project page."""
    def make(self):
        webbrowser.open("http://code.google.com/p/platinfo/")

class clean(Task):
    """Clean generated files and dirs."""
    def make(self):
        patterns = [
            "dist",
            "MANIFEST",
            "*.pyc",
            "lib/*.pyc",
            "*.orig",
            "lib/*.orig",
        ]
        for pattern in patterns:
            p = join(self.dir, pattern)
            for path in glob(p):
                sh.rm(path, log=self.log)

class sdist(Task):
    """python setup.py sdist"""
    def make(self):
        sh.run_in_dir(
            "%spython setup.py sdist -f --formats zip" % _setup_command_prefix(),
            self.dir, self.log.debug)

class pypi_upload(Task):
    """Update release to pypi."""
    def make(self):
        #tasks = (sys.platform == "win32"
        #    and "sdist --formats zip bdist_wininst upload"
        #    or "sdist --formats zip upload")
        tasks = "sdist --formats zip upload"
        sh.run_in_dir("%spython setup.py %s" % (_setup_command_prefix(), tasks),
            self.dir, self.log.debug)

        sys.path.insert(0, join(self.dir, "lib"))
        url = "http://pypi.python.org/pypi/platinfo/"
        import webbrowser
        webbrowser.open_new(url)

class googlecode_upload(Task):
    """Update sdist to Google Code project site."""
    deps = ["sdist"]
    def make(self):
        helper_in_cwd = exists(join(self.dir, "googlecode_upload.py"))
        if helper_in_cwd:
            sys.path.insert(0, self.dir)
        try:
            import googlecode_upload
        except ImportError:
            raise MkError("couldn't import `googlecode_upload` (get it from http://support.googlecode.com/svn/trunk/scripts/googlecode_upload.py)")
        if helper_in_cwd:
            del sys.path[0]
        sys.path.insert(0, join(self.dir, "lib"))
        import platinfo

        sdist_path = join(self.dir, "dist",
            "platinfo-%s.zip" % platinfo.__version__)
        status, reason, url = googlecode_upload.upload_find_auth(
            sdist_path,
            "platinfo", # project_name
            "platinfo %s source package" % platinfo.__version__, # summary
            ["Featured", "Type-Archive"]) # labels
        if not url:
            raise MkError("couldn't upload sdist to Google Code: %s (%s)"
                          % (reason, status))
        self.log.info("uploaded sdist to `%s'", url)

        project_url = "http://code.google.com/p/platinfo/"
        import webbrowser
        webbrowser.open_new(project_url)

class test(Task):
    """Run all tests (except known failures)."""
    def make(self):
        for ver, python in self._gen_pythons():
            if ver < (2,4):
                # Don't support Python <= 2.3.
                continue
            elif ver >= (3,0):
                # Don't (yet) support Python 3.
                continue
            ver_str = "%s.%s" % ver
            print "-- test with Python %s (%s)" % (ver_str, python)
            assert ' ' not in python
            sh.run_in_dir("%s test.py" % python,
                          join(self.dir, "test"))

    def _python_ver_from_python(self, python):
        assert ' ' not in python
        o = os.popen('''%s -c "import sys; print(sys.version)"''' % python)
        ver_str = o.read().strip()
        ver_bits = re.split("\.|[^\d]", ver_str, 2)[:2]
        ver = tuple(map(int, ver_bits))
        return ver

    def _gen_python_names(self):
        yield "python"
        for ver in [(2,3), (2,4), (2,5), (2,6), (2,7), (3,0), (3,1)]:
            yield "python%d.%d" % ver

    def _gen_pythons(self):
        import which  # get it from http://trentm.com/projects/which
        python_from_ver = {}
        for name in self._gen_python_names():
            for python in which.whichall(name):
                ver = self._python_ver_from_python(python)
                if ver not in python_from_ver:
                    python_from_ver[ver] = python
        for ver, python in sorted(python_from_ver.items()):
            yield ver, python

class todo(Task):
    """Print out todo's and xxx's in the docs area."""
    def make(self):
        for path in _paths_from_path_patterns(['.'],
                excludes=[".svn", "*.pyc", "TO""DO.txt", "Makefile.py",
                          "*.png", "*.gif", "*.pprint", "*.prof",
                          "tmp-*"]):
            self._dump_pattern_in_path("TO\DO\\|XX\X", path)

        path = join(self.dir, "TO""DO.txt")
        todos = re.compile("^- ", re.M).findall(open(path, 'r').read())
        print "(plus %d TODOs from TO""DO.txt)" % len(todos)

    def _dump_pattern_in_path(self, pattern, path):
        os.system("grep -nH '%s' '%s'" % (pattern, path))



#---- internal support stuff

# Recipe: paths_from_path_patterns (0.3.7)
def _should_include_path(path, includes, excludes):
    """Return True iff the given path should be included."""
    from os.path import basename
    from fnmatch import fnmatch

    base = basename(path)
    if includes:
        for include in includes:
            if fnmatch(base, include):
                try:
                    log.debug("include `%s' (matches `%s')", path, include)
                except (NameError, AttributeError):
                    pass
                break
        else:
            try:
                log.debug("exclude `%s' (matches no includes)", path)
            except (NameError, AttributeError):
                pass
            return False
    for exclude in excludes:
        if fnmatch(base, exclude):
            try:
                log.debug("exclude `%s' (matches `%s')", path, exclude)
            except (NameError, AttributeError):
                pass
            return False
    return True

_NOT_SPECIFIED = ("NOT", "SPECIFIED")
def _paths_from_path_patterns(path_patterns, files=True, dirs="never",
                              recursive=True, includes=[], excludes=[],
                              on_error=_NOT_SPECIFIED):
    """_paths_from_path_patterns([<path-patterns>, ...]) -> file paths

    Generate a list of paths (files and/or dirs) represented by the given path
    patterns.

        "path_patterns" is a list of paths optionally using the '*', '?' and
            '[seq]' glob patterns.
        "files" is boolean (default True) indicating if file paths
            should be yielded
        "dirs" is string indicating under what conditions dirs are
            yielded. It must be one of:
              never             (default) never yield dirs
              always            yield all dirs matching given patterns
              if-not-recursive  only yield dirs for invocations when
                                recursive=False
            See use cases below for more details.
        "recursive" is boolean (default True) indicating if paths should
            be recursively yielded under given dirs.
        "includes" is a list of file patterns to include in recursive
            searches.
        "excludes" is a list of file and dir patterns to exclude.
            (Note: This is slightly different than GNU grep's --exclude
            option which only excludes *files*.  I.e. you cannot exclude
            a ".svn" dir.)
        "on_error" is an error callback called when a given path pattern
            matches nothing:
                on_error(PATH_PATTERN)
            If not specified, the default is look for a "log" global and
            call:
                log.error("`%s': No such file or directory")
            Specify None to do nothing.

    Typically this is useful for a command-line tool that takes a list
    of paths as arguments. (For Unix-heads: the shell on Windows does
    NOT expand glob chars, that is left to the app.)

    Use case #1: like `grep -r`
      {files=True, dirs='never', recursive=(if '-r' in opts)}
        script FILE     # yield FILE, else call on_error(FILE)
        script DIR      # yield nothing
        script PATH*    # yield all files matching PATH*; if none,
                        # call on_error(PATH*) callback
        script -r DIR   # yield files (not dirs) recursively under DIR
        script -r PATH* # yield files matching PATH* and files recursively
                        # under dirs matching PATH*; if none, call
                        # on_error(PATH*) callback

    Use case #2: like `file -r` (if it had a recursive option)
      {files=True, dirs='if-not-recursive', recursive=(if '-r' in opts)}
        script FILE     # yield FILE, else call on_error(FILE)
        script DIR      # yield DIR, else call on_error(DIR)
        script PATH*    # yield all files and dirs matching PATH*; if none,
                        # call on_error(PATH*) callback
        script -r DIR   # yield files (not dirs) recursively under DIR
        script -r PATH* # yield files matching PATH* and files recursively
                        # under dirs matching PATH*; if none, call
                        # on_error(PATH*) callback

    Use case #3: kind of like `find .`
      {files=True, dirs='always', recursive=(if '-r' in opts)}
        script FILE     # yield FILE, else call on_error(FILE)
        script DIR      # yield DIR, else call on_error(DIR)
        script PATH*    # yield all files and dirs matching PATH*; if none,
                        # call on_error(PATH*) callback
        script -r DIR   # yield files and dirs recursively under DIR
                        # (including DIR)
        script -r PATH* # yield files and dirs matching PATH* and recursively
                        # under dirs; if none, call on_error(PATH*)
                        # callback
    """
    from os.path import basename, exists, isdir, join
    from glob import glob

    assert not isinstance(path_patterns, basestring), \
        "'path_patterns' must be a sequence, not a string: %r" % path_patterns
    GLOB_CHARS = '*?['

    for path_pattern in path_patterns:
        # Determine the set of paths matching this path_pattern.
        for glob_char in GLOB_CHARS:
            if glob_char in path_pattern:
                paths = glob(path_pattern)
                break
        else:
            paths = exists(path_pattern) and [path_pattern] or []
        if not paths:
            if on_error is None:
                pass
            elif on_error is _NOT_SPECIFIED:
                try:
                    log.error("`%s': No such file or directory", path_pattern)
                except (NameError, AttributeError):
                    pass
            else:
                on_error(path_pattern)

        for path in paths:
            if isdir(path):
                # 'includes' SHOULD affect whether a dir is yielded.
                if (dirs == "always"
                    or (dirs == "if-not-recursive" and not recursive)
                   ) and _should_include_path(path, includes, excludes):
                    yield path

                # However, if recursive, 'includes' should NOT affect
                # whether a dir is recursed into. Otherwise you could
                # not:
                #   script -r --include="*.py" DIR
                if recursive and _should_include_path(path, [], excludes):
                    for dirpath, dirnames, filenames in os.walk(path):
                        dir_indeces_to_remove = []
                        for i, dirname in enumerate(dirnames):
                            d = join(dirpath, dirname)
                            if dirs == "always" \
                               and _should_include_path(d, includes, excludes):
                                yield d
                            if not _should_include_path(d, [], excludes):
                                dir_indeces_to_remove.append(i)
                        for i in reversed(dir_indeces_to_remove):
                            del dirnames[i]
                        if files:
                            for filename in sorted(filenames):
                                f = join(dirpath, filename)
                                if _should_include_path(f, includes, excludes):
                                    yield f

            elif files and _should_include_path(path, includes, excludes):
                yield path

def _setup_command_prefix():
    prefix = ""
    if sys.platform == "darwin":
        # http://forums.macosxhints.com/archive/index.php/t-43243.html
        # This is an Apple customization to `tar` to avoid creating
        # '._foo' files for extended-attributes for archived files.
        prefix = "COPY_EXTENDED_ATTRIBUTES_DISABLE=1 "
    return prefix


