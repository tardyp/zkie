#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import json
import os

import argh
from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

try:
    from pygments.lexers import guess_lexer_for_filename, guess_lexer, JsonLexer, HexdumpLexer
    from pygments.formatters import Terminal256Formatter
    from pygments import highlight
    from hexdump import hexdump
    hasPygments = True
except ImportError:
    hasPygments = False

DEFAULT_HOSTS = os.environ.get("ZK_HOST", "localhost:2181")


def pretty_print(fn, data):
    if not hasPygments:
        print(data)
        return

    lx = None
    # guess lexer will not guess json in priority, so we first try to decode json with json module
    try:
        data = json.dumps(json.loads(data), indent=2)
        lx = JsonLexer()
    except ValueError:
        pass
    if lx is None:
        try:
            lx = guess_lexer_for_filename(fn, data)
        except:
            pass
    if lx is None:
        try:
            lx = guess_lexer(data)
        except:
            pass
    if lx is None:
        lx = HexdumpLexer()
        data = hexdump(data, result='return')

    if isinstance(lx, JsonLexer):
        data = json.dumps(json.loads(data), indent=2)
    try:
        print(highlight(data, lx, Terminal256Formatter()))
    except UnicodeEncodeError:
        print(highlight(hexdump(data, result='return'), HexdumpLexer(), Terminal256Formatter()))


def ZK(hosts, path):
    if path.startswith("zk://"):
        path = urlparse.urlparse(path)
        hosts = path.netloc
        path = path.path
    zk = KazooClient(hosts=hosts)
    zk.start()
    return zk, path


def upload(dir, path, hosts=DEFAULT_HOSTS):
    zk, path = ZK(hosts, path)
    for root, dirs, files in os.walk(dir):
        outroot = root.replace(dir, "").strip("/")
        outroot = os.path.join(path, outroot)
        for name in files:
            inpath = os.path.join(root, name)
            outpath = os.path.join(outroot, name)
            zk.ensure_path(outpath)
            with open(inpath) as f:
                data = f.read()
                zk.set(outpath, data)
            print("created", outpath, ":")
            pretty_print(outpath, data)


def ls(path, hosts=DEFAULT_HOSTS):
    zk, path = ZK(hosts, path)
    children = zk.get_children(path)
    print("\n".join(children))


def find(path, hosts=DEFAULT_HOSTS):
    zk, _path = ZK(hosts, path)
    try:
        children = zk.get_children(_path)
    except NoNodeError:
        return
    for child in children:
        newpath = os.path.join(path, child)
        print(newpath)
        find(newpath, hosts)


@argh.arg('--out', '-O', help='output to the specicied file')
def get(path, out=None, hosts=DEFAULT_HOSTS):
    zk, path = ZK(hosts, path)
    children = zk.retry(zk.get, path)
    if out is None:
        data, metadata = children
        print(metadata)
        pretty_print(path, data)
    else:
        with open(out, "w") as f:
            f.write(children[0])

parser = argh.ArghParser()
parser.add_commands([upload, ls, get, find])


def cmd():
    parser.dispatch()
