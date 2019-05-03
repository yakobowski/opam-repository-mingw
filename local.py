#!/usr/bin/env python3

import os.path
import re
import shutil
from distutils.dir_util import copy_tree
from urllib.request import urlretrieve

sources = "all.txt"

regex = re.compile("src:\s*\"([^\"]*)\"")

class Opam_Pkg:

    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.opamfile = os.path.join('packages', self.name, self.name + '.' + self.version, 'opam')
        self.local_opamfile = os.path.join('local', 'packages', self.name, self.name + '.' + self.version, 'opam')
        with open(self.opamfile, 'r') as fn:
            text = fn.read()
            m = regex.search(text)
            if m is not None:
                url = m.group(1)
                self.url = url
            else:
                self.url = None

    def localname(self):
        """returns pair (dir, name), the local location of the package tarball"""
        if self.url is not None:
            filename = self.url[self.url.rfind('/')+1:]
            localdir = 'src' + '/' + self.name + '.' + self.version
            return localdir, filename

    def download(self):
        if self.url is None:
            return
        print (self.url)
        if not self.url.startswith('http'):
            return
        d, fn = self.localname()
        print (d);
        if os.path.isfile(os.path.join(d, fn)):
            return
        try:
            os.mkdir(d)
        except FileExistsError:
            pass
        urlretrieve(self.url, os.path.join(d, fn))

    def localize(self):
        with open(self.opamfile, 'r') as f:
            text = f.read()
        def urlrepl(m):
            url = m.group(1)
            filename = url[url.rfind('/')+1:]
            d, fn = self.localname()
            return "src: \"local/" + d + '/' + fn + "\""
        text = regex.sub(urlrepl, text)
        with open(self.local_opamfile, 'w') as f:
            f.write(text)

    def copy_tree(self):
        copy_tree(
            os.path.join("packages", self.name, self.name + '.' + self.version),
            os.path.join("local", "packages", self.name, self.name + '.' + self.version)
        )

def create_packages():
    pkgs = []
    with open(sources, 'r') as fn:
        for line in fn.readlines():
            split = line.split()
            pkg = split[0]
            version = split[1]
            pkgs.append(Opam_Pkg(pkg, version))
    return pkgs

def main():
    pkgs = create_packages()
    #os.mkdir(os."packages2")
    for pkg in pkgs:
        print(pkg.opamfile)
        pkg.download()
        pkg.copy_tree()
        pkg.localize()
        # download()

main()
