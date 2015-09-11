# coding: utf-8

import re

from setuptools import setup


def find_version(fname):
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


__version__ = find_version("asteriskonf/__init__.py")


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='asteriskonf',
    version=__version__,
    description='Export Asterisk configuration file',
    long_description=read("README.md"),
    author='Osvaldo Santana Neto',
    author_email='asteriskonf@osantana.me',
    url='https://github.com/osantana/asteriskonf',
    license=read("LICENSE"),
    zip_safe=True,
    keywords='asterisk configuration script',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=["asteriskonf"],
    entry_points={
        'console_scripts': [
            "asteriskonf = asteriskonf.cli:main"
        ]
    },
)
