# -*- coding: utf-8 -*-
"""
    mackerel.host
    ~~~~~~~~~~~~~

    Mackerel client implemented by Python.

    Ported from `mackerel-client-ruby`.
    <https://github.com/mackerelio/mackerel-client-ruby>

    :copyright: (c) 2014 Hatena, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""


class Service(object):
    def __init__(self, **kwargs):
        """Construct a Service.

        :param name: Service name
        :param memo: Service memo
        :param roles: Service roles
        """

        self.args = kwargs
        self.name = kwargs.get('name', None)
        self.memo = kwargs.get('memo', None)
        self.roles = kwargs.get('roles', None)

    def __repr__(self):
        repr = '<Service('
        repr += 'name={0}, memo={1}, roles={2})>'
        return repr.format(self.name, self.memo, self.roles)
