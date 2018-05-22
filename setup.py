import re

from setuptools import setup

with open('votable_to_sql/__init__.py') as f:
    metadata = dict(re.findall(r'__(.*)__ = [\']([^\']*)[\']', f.read()))

setup(
    name=metadata['title'],
    version=metadata['version'],
    author=metadata['author'],
    author_email=metadata['email'],
    maintainer=metadata['author'],
    maintainer_email=metadata['email'],
    license=metadata['license'],
    url='https://github.com/aipescience/votable2sql',
    description=metadata['description'],
    long_description=open('README.rst').read(),
    install_requires=[
        'astropy',
    ],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Astronomy'
    ],
    entry_points={
        'console_scripts': 'votable2sql=votable_to_sql:main'
    },
    packages=['votable_to_sql']
)
