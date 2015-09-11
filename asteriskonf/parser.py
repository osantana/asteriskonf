# coding: utf-8

import re
import os
from collections import namedtuple


MULTIPLIER = 10
COMMENT_OUT = re.compile(r";.*$")

is_section = re.compile(r"[][](?P<name>.*?)[][]\s*(\((?P<inherit>[^!]*)\))?")
is_template = re.compile(r"[][](?P<name>.*?)[][]\s*(\(!,?(?P<inherit>.*?)?\))")

Item = namedtuple("Item", ["sectionno", "section", "itemno", "key", "value"])


class Configuration(object):
    def __init__(self):
        self.templates = {}
        self.sections = []

    def parse(self, filename):
        with open(filename) as config:
            self.parse_file(config)

    def parse_file(self, config):
        current = None
        for raw_line in config:
            line = COMMENT_OUT.sub("", raw_line).strip()
            if raw_line.lstrip().startswith(";"):
                continue  # TODO: commented line

            if not line:
                continue

            template_data = is_template.match(line)
            if template_data:
                template_data = template_data.groupdict()
                current = Template(self, template_data["name"], template_data["inherit"])
                continue

            section_data = is_section.match(line)
            if section_data:
                section_data = section_data.groupdict()
                current = Section(self, section_data["name"], section_data["inherit"])
                continue

            current.add_item(line)

    def __iter__(self):
        for sectionno, section in enumerate(self.sections):
            for itemno, item in enumerate(section):
                yield Item((sectionno + 1) * MULTIPLIER, section.name, (itemno + 1) * MULTIPLIER, item[0], item[1])


class AbstractSection(object):
    def __init__(self, configuration, name, inherit=None):
        self.name = name
        self.items = []

        if inherit is None:
            inherit = ""
        inherit = [s.strip() for s in inherit.split(",")]
        self.inherit = [configuration.templates[template] for template in inherit if template]
        self._add_section(configuration)

    def _add_section(self, configuration):
        raise NotImplementedError("Abstract method")

    def add_item(self, line):
        split = "=>" if "=>" in line else "="
        self.items.append(tuple(i.strip() for i in line.split(split)))


class Template(AbstractSection):
    def _add_section(self, configuration):
        configuration.templates[self.name] = self


class Section(AbstractSection):
    def _add_section(self, configuration):
        configuration.sections.append(self)

    def __iter__(self):
        for template in self.inherit:
            for item in template.items:
                yield item

        for item in self.items:
            yield item


class Parser(object):
    def __init__(self, path):
        self.path = path
        self.filename = os.path.basename(path)

    def parse(self):
        configuration = Configuration()
        configuration.parse(self.path)
        return configuration
