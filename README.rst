votable2sql
===========

Setup
-----

```
pip install git+https://github.com/aipescience/votable2sql
```

Usage
-----

```bash
usage: votable2sql [-h] [-o OUTPUT] [-d DIALECT] [-s SKIP] [--schema SCHEMA]
                   [--table TABLE]
                   votable

Tool to convert VOTables into SQL dumps

positional arguments:
  votable               VOTable file to be processed

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file [default: STDOUT]
  -d DIALECT, --dialect DIALECT
                        SQL dialect, e.g. sql, mysql [default: sql]
  -s SKIP, --skip SKIP  Skip column
  --schema SCHEMA       Schema to use
  --table TABLE         Table to use
```

Examples
--------

```bash
# writes the sql dump to STDOUT
votable2sql test.votable.xml

# writes the sql dump to test.sql
votable2sql test.votable.xml -o test.sql

# writes a MySQL dump
votable2sql test.votable.xml -d mysql

# writes a MySQL dump skipping `vx`, `vy` and `vz`
votable2sql test.votable.xml -d mysql -s vx -s vy -s vz
```
