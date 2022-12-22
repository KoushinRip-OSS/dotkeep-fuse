#!/usr/bin/env python

#    Copyright (C) 2001  Jeff Epler  <jepler@unpythonic.dhs.org>
#    Copyright (C) 2006  Csaba Henk  <csaba.henk@creo.hu>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#

from __future__ import print_function

import os, os.path
import sys
from xmp import Xmp

import fuse
from fuse import Fuse


if not hasattr(fuse, '__version__'):
    raise RuntimeError("your fuse-py doesn't know of fuse.__version__, probably it's too old.")

fuse.fuse_python_api = (0, 2)

fuse.feature_assert('stateful_files', 'has_init')

class Dotkeep(Xmp):
    def readdir(self, path, offset):
        have_dir, have_dotkeep = False, False
        for e in os.scandir("." + path):
            yield fuse.Direntry(e.name)
            if e.is_dir():
                have_dir = True
            if e.name == '.keep':
                have_dotkeep = True
        if not have_dir and not have_dotkeep:
            yield fuse.Direntry(".keep")

    def access(self, path, mode):
        if os.path.basename(path) == ".keep":
            return
        return super().access(path, mode)

    def getattr(self, path):
        if os.path.basename(path) == ".keep":
            return os.lstat("/dev/null")
        return super().getattr(path)

    class DKFile(Xmp.XmpFile):
        def __init__(self, path, flags, *mode):
            if os.path.basename(path) == ".keep":
                return self._subinit("/dev/null", flags, *mode)
            super().__init__(path, flags, *mode)

    def main(self, *a, **kw):
        self.file_class = self.DKFile
        return Fuse.main(self, *a, **kw)

def main():

    usage = """
Add .keep files as necessary to make directories efficiently on some cloud-based applications

""" + Fuse.fusage

    server = Dotkeep(version="%prog " + fuse.__version__,
                 usage=usage,
                 dash_s_do='setsingle')

    server.parser.add_option(mountopt="root", metavar="PATH", default='/',
                             help="mirror filesystem from under PATH [default: %default]")
    server.parse(values=server, errex=1)

    try:
        if server.fuse_args.mount_expected():
            os.chdir(server.root)
    except OSError:
        print("can't enter root of underlying filesystem", file=sys.stderr)
        sys.exit(1)

    server.main()


if __name__ == '__main__':
    main()
