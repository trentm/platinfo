# Run this script as "python trunk/scripts/ci.py" from your Continuous
# Integration tool (eg: Hudson).
"""A script to run buildout and tests for PyPM trunk

This is specifically meant to be used with Hudson
"""

import sys
assert (2,5) <= sys.version_info[:2] < (3,0), \
  'unsupported Python version: %s' % sys.version_info

import os
from os import path
import subprocess

root = path.abspath(path.dirname(path.dirname(__file__)))
os.chdir(root)

assert len(sys.argv) == 2, 'incorrect args'
pyver = sys.argv[1]
assert len(pyver) == 3, 'not a python version'
pyver1, pyver2 = pyver.split('.')

if sys.platform.startswith('win'):
    python_exe = 'python%s%s' % (pyver1, pyver2)
elif sys.platform.startswith('darwin'):
    python_exe = '/usr/local/bin/python' + pyver
else:
    python_exe = '/opt/ActivePython-%s/bin/python%s' \
            % (pyver, pyver)


def run(*args):
    print 'RUN:', args
    subprocess.check_call(args)

print 'Environment variables'
print '====================='
print '\n'.join([k + ' = ' + v for k,v in os.environ.items()])
print

print "sys.version=%s" % sys.version
try:
    import activestate
except ImportError:
    print >>sys.stderr, 'ERROR: activestate module is unavailable. Not ActivePython?'
else:
    print "activestate.version_info=%s" % activestate.version_info


# Remove Hudson added Java paths to prevent errors like:
#   /Java/jre6/bin"" was unexpected at this time.
if sys.platform.startswith('win'):
    pth = [p for p in os.getenv('PATH').split(';') if '/Java/' not in p]
    os.environ['PATH'] = ';'.join(pth)
    print 'Modified PATH=%s' % os.getenv("PATH")

# run platinfo test
os.chdir('test')
run(python_exe, 'test.py')

print 'bin/ci: finished'




