#!/usr/bin/env python

import argparse
import sys

from astropy.io.votable import parse

__title__ = 'votable2sql'
__version__ = '1.0.0'
__author__ = 'Jochen Klar'
__email__ = 'jklar@aip.de'
__license__ = 'Apache-2.0'
__copyright__ = 'Copyright 2016-2017 Leibniz Institute for Astrophysics Potsdam (AIP)'
__description__ = 'Tool to convert VOTables into SQL dumps'

DATATYPES = {
    'mysql': {
        'char': 'CHAR',
        'unsignedByte': 'TINYINT',
        'short': 'SMALLINT',
        'int': 'INT',
        'long': 'BIGINT',
        'float': 'FLOAT',
        'double': 'DOUBLE',
        'timestamp': 'TIMESTAMP'
    },
    'sql': {
        'char': 'character',
        'unsignedByte': 'tinyint',
        'short': 'smallint',
        'int': 'int',
        'long': 'bigint',
        'float': 'real',
        'double': 'double precision',
        'timestamp': 'timestamp'
    }
}


def main():
    # setup argparse
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('votable', help='VOTable file to be processed')
    parser.add_argument('-o', '--output', help='Output file [default: STDOUT]')
    parser.add_argument('-d', '--dialect', default='sql', help='SQL dialect, e.g. sql, mysql [default: sql]')
    parser.add_argument('-s', '--skip', action='append', default=[], help='Skip column')
    parser.add_argument('--schema', help='Schema to use')
    parser.add_argument('--table', help='Table to use')

    # parse the arguments
    args = parser.parse_args()

    # read the VOTable file
    votable = parse(args.votable)
    table = votable.get_first_table()
    fields = [(i, field) for i, field in enumerate(table.fields) if field.name not in args.skip]

    # construct table_name
    if args.schema:
        table_name = '%(schema_name)s.%(table_name)s' % {
            'schema_name': quote_identifier(args.dialect, args.schema),
            'table_name': quote_identifier(args.dialect, args.table or table.name),
        }
    else:
        table_name = quote_identifier(args.dialect, args.table or table.name)

    # create the drop table if exists statement
    drop_stmt = '''
DROP TABLE IF EXISTS %(table_name)s;
''' % {
        'table_name': table_name
    }

    # create the create table statement
    create_stmt = '''
CREATE TABLE %(table_name)s (
%(field_strings)s
);
''' % {
        'table_name': table_name,
        'field_strings': ',\n'.join([field_string(args.dialect, field) for _, field in fields])
    }

    # create the insert statement
    insert_stmt = '''
INSERT INTO %(table_name)s VALUES
%(values_strings)s
;
''' % {
        'table_name': table_name,
        'values_strings': ',\n'.join([values_string('postgresql', fields, row) for row in table.array])
    }

    if args.output:
        f = open(args.output, 'w')
    else:
        f = sys.stdout

    f.write(drop_stmt)
    f.write(create_stmt)
    f.write(insert_stmt)
    f.close()


def quote_identifier(engine, string):
    if engine == 'mysql':
        return '`%s`' % string
    else:
        return '"%s"' % string


def field_string(engine, field):
    return '  %(name)s %(datatype)s' % {
        'name': quote_identifier(engine, field.name),
        'datatype': DATATYPES[engine][field.datatype]
    }


def values_string(engine, fields, row):
    return '(%s)' % ', '.join(str(row[i]) for i, _ in fields)


if __name__ == "__main__":
    main()
