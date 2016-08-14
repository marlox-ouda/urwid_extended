from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst")) as fd:
    long_description = fd.read()

exec(open(path.join("urwid_extended", "version.py")).read())

setup(
    name='urwid_extended',
    version=__version__,
    description="Urwid new advanced widgets",
    long_description=long_description,
    keywords="curses ui widget scroll listbox user iterface text layout console ncures ihm",

    packages=['urwid_extended'],
    install_requires=['urwid'],
    extras_requires={
        'dev': ['twine'],
        'test': [],
    },

    url="https://github.com/marlox-ouda/urwid_extended",

    author="Marlox",
    author_email="urwid@mx.ouda.fr",

    license="MIT",
    platforms="unix-like",

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classsifiers=[
        "Development Status :: 1 - Planning",

        "Environment :: Console",
        "Environment :: Console :: Urwid",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: MIT License",
        # Alignment with Urwid
        "License :: OSI Approved :: LGPL",

        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",

        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Widget Sets",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
