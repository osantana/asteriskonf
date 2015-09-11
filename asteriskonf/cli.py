#!/usr/bin/env python

import sys
import csv
import argparse

from .parser import Parser


SQL_TEMPLATE = ("INSERT INTO {table} (filename, cat_metric, category, var_metric, var_name, var_val, commented) "
                "VALUES ('{filename}', {item.sectionno}, '{item.section}', {item.itemno}, "
                "'{item.key}', '{item.value}', 0);")


def export_csv(parser, output):
    writer = csv.writer(output)
    writer.writerow(("filename", "section_number", "section", "item_number", "key", "value", "commented"))
    for item in parser.parse():
        writer.writerow((parser.filename, item.sectionno, item.section, item.itemno, item.key, item.value, 0))


def export_sql(parser, output, table):
    filename = parser.filename
    for item in parser.parse():
        print(SQL_TEMPLATE.format(table=table, filename=filename, item=item), file=output)


def main():
    parser = argparse.ArgumentParser(description='Export Asterisk .conf files')
    parser.add_argument('configurations', metavar='configs', nargs='+',
                        help='list of configuration files')
    parser.add_argument('--format', "-f", metavar="FMT", default="sql",
                        help="export format (available: csv, sql)")
    parser.add_argument('--sql-table', "-t", metavar="TABLE", default="ast_config",
                        help="table name for SQL export")
    parser.add_argument("--output", "-O", metavar="FILE", default="-",
                        help="output file")
    args = parser.parse_args()

    if args.output == "-":
        output = sys.stdout
    else:
        output = open(args.output, "w")

    try:
        for configfile in args.configurations:
            configuration_parser = Parser(configfile)
            if args.format == "csv":
                export_csv(configuration_parser, output)
            elif args.format == "sql":
                export_sql(configuration_parser, output, table=args.sql_table)
            else:
                parser.error("Invalid export format")
                return 1
    finally:
        if args.output != "-":
            output.close()


if __name__ == "__main__":
    sys.exit(int(main() or 0))
