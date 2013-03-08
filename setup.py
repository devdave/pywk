import os
import sys
import pywk

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

required=["PySide"]

setup(
    name="pywk", #PyWick?
    version=pywk.__version__,
    description='A platform/container for a WebKit powered desktop app',
    author="David Ward",
    author_email="dotgraph_related@ominian.net",
    url="https://github.com/devdave/pywk",
    packages=['pywk'],
    install_requires=required,
)