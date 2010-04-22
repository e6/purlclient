try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from purlclient import __version__, __description__, __long_description__, __license__

import os

setup(
    name='purlclient',
    version=__version__,
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    license=__license__,
    url='http://github.com/pudo/purlclient',
    description=__description__,
    keywords='purl url redirect persistence sustainability tool client',
    long_description =__long_description__,
    install_requires=[
        # only required if python <= 2.5 (as json library in python >= 2.6)
        # 'simplejson',
    ],
    packages=find_packages(exclude=['ez_setup']),
    scripts=[],
    include_package_data=True,
    always_unzip=True,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
