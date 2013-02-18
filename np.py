#!/usr/bin/python

import re

class Config:
    config = None
    children = []

    def __init__(self):
        pass

    def __str__(self):
        res = "I'm a config object\n"
        for child in self.children:
            res += str(child)

        return res



    def parse(self, config):
        self.config = config

        self._guess_platform()
        # get interfaces
        self.children.extend(Interface._parse_xr_interfaces(self.config))



    def _guess_platform(self):
        """ Guess platform from config

            Possible NILS integration?
        """
        # XXX: just return XR for now
        return 'xr'




class Interface:
    """ Representing a physical or logical interface
    """
    name = None
    description = None

    def __init__(self):
        pass

    def __str__(self):
        return "IF %-25s - %s\n" % (self.name, self.description)

    @classmethod
    def _parse_xr_interfaces(cls, config):
        """ Parse interfaces from an XR config!
        """
        res = []

        for line in config.splitlines():
            # get interface name
            m = re.match('interface (?!preconfigure)(.*)$', line)
            if m is not None:
                res.append(Interface._parse_xr_interface(config, m.group(1)))

        return res

    @classmethod
    def _parse_xr_interface(cls, config, name):
        data = { 'name': name,
                'description': None }

        in_if = False
        for line in config.splitlines():
            if re.match('interface ' + name, line):
                in_if = True

            m = re.match(' description (.*)$', line)
            if in_if and m is not None:
                data['description'] = m.group(1)

            if re.match('!', line):
                in_if = False

        return Interface.from_dict(data)


    @classmethod
    def from_dict(cls, data):
        i = Interface()
        i.name = data['name']
        i.description = data['description']
        return i




if __name__ == '__main__':
    f = open('kst5-core-1')
    raw_config = f.read()
    f.close()
    c = Config()
    c.parse(raw_config)

    print c

