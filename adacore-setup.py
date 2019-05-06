#!/usr/bin/env python
import argparse
import re
import os
import shutil
import subprocess

args = None
descr = """Setup an opam install"""

local_regex = re.compile("src:\s*\"local")

def parse_arguments():
    global args
    parser = argparse.ArgumentParser(
            description=descr,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
            '--srcdir', dest="srcdir", metavar='S',
            action="store", 
            help='directory of the opam repository')
    parser.add_argument(
            '--installdir', dest="installdir", metavar='S',
            action="store", 
            help='directory where opam and ocaml will be installed')
    args = parser.parse_args()

def replace_urls():
    """replace local links to point to current repos"""
    matches = []
    for root, dirnames, filenames in os.walk('packages'):
        for filename in filenames:
            if filename.endswith("opam"):
                matches.append(os.path.join(root, filename))
    for fn in matches:
        with open(fn, 'r') as f:
            text = f.read()
        text = local_regex.sub("src: \"" + args.srcdir , text)
        with open(fn, 'w') as f:
            f.write(text)

def clean():
    if os.path.exists(args.installdir):
        shutil.rmtree(args.installdir)

def opam_init():
    subprocess.call(['opam', 'init', '--bare', '--disable-sandboxing', '--bypass-checks', '-n', '-y', args.srcdir])

def opam_switch(arg):
    subprocess.call(['opam', 'switch', 'create', '-y', arg])

def opam_install(arg):
    subprocess.call(['opam', 'install', '-y', arg])

def opam_install_deps(arg):
    subprocess.call(['opam', 'install', '-y', '--deps-only', arg])

def main():
    parse_arguments()
    clean()
    os.environ['OPAMROOT'] = args.installdir
    print (os.environ['OPAMROOT'])
    replace_urls()
    opam_init()
    opam_switch('ocaml-system.4.07.1')

    # opam_install_deps('infer')
    # opam_install_deps('alt-ergo')
    # opam_install_deps('why3')


main()
