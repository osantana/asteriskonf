# coding: utf-8

import re
import os
from collections import namedtuple


MULTIPLIER = 10
COMMENT_OUT = re.compile(r";.*$")

is_section = re.compile(r"[][](?P<name>.*?)[][]\s*(\((?P<inherit>[^!]*)\))?")
is_template = re.compile(r"[][](?P<name>.*?)[][]\s*(\(!,?(?P<inherit>.*?)?\))")

Item = namedtuple("Item", ["filename", "sectionno", "section", "itemno", "key", "value"])


class Parser(object):
    def __init__(self, path):
        self.path = path
        self.filename = os.path.basename(path)
        self.templates = {}
        self.sections = []

    def parse(self):
        with open(self.path) as config:
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

    @property
    def items(self):
        ret = []
        for sectionno, section in enumerate(self.sections):
            for itemno, item in enumerate(section.items):
                ret.append(Item(self.filename,
                                sectionno * MULTIPLIER,
                                section.name,
                                itemno * MULTIPLIER,
                                item[0], item[1]))
        return ret


class AbstractSection(object):
    def __init__(self, configuration, name, inherit):
        self.name = name
        self._items = []

        if inherit is None:
            inherit = ""
        inherit = [s.strip() for s in inherit.split(",")]
        self.inherit = [configuration.templates[template] for template in inherit if template]
        self._add_section(configuration)

    def _add_section(self, configuration):
        raise NotImplementedError("Abstract method")

    def add_item(self, line):
        split = "=>" if "=>" in line else "="
        self._items.append(tuple(i.strip() for i in line.split(split)))

    @property
    def items(self):
        ret = []
        for template in self.inherit:
            ret.extend(template.items)
        ret.extend(self._items)
        return ret


class Template(AbstractSection):
    def _add_section(self, configuration):
        configuration.templates[self.name] = self


class Section(AbstractSection):
    def _add_section(self, configuration):
        configuration.sections.append(self)
