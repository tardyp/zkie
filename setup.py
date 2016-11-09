#!/usr/bin/env python
#
"""
Standard setup script.
"""
import os

from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

setup(
    name="zkie",
    version="0.1.2",
    description="zookeeper commandline, like httpie but for zookeeper",
    long_description=README,
    author="Pierre Tardy",
    author_email="tardyp@gmail.com",
    license="MIT",
    packages=["zkie"],
    entry_points={
        'console_scripts': [
            'zk=zkie:cmd',
        ],
    },
    install_requires=[
        'argh',
        'kazoo'
    ],
    extras_require = {
       'ui': [
       'pygments',
       'hexdump'
       ]
    }

)
