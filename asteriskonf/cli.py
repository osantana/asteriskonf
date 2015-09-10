#!/usr/bin/env python

import sys
import argparse

from parser import Parser

def export_csv(configuration, output):
    filename = configuration.filename
    print(configuration)

def export_sql(configuration, output):
    filename = configuration.filename
    print(configuration, "sql")


def main():
    parser = argparse.ArgumentParser(description='Export Asterisk .conf files')
    parser.add_argument('configurations', metavar='configs', nargs='+',
                        help='list of configuration files')
    parser.add_argument('--format', metavar="FMT", default="sql",
                        help="export format (available: csv, sql)")
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
                export_sql(configuration_parser, output)
            else:
                parser.error("Invalid export format")
                return 1
    finally:
        if args.output != "-":
            output.close()


if __name__ == "__main__":
    sys.exit(int(main() or 0))
