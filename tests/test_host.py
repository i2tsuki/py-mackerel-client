# -*- coding: utf-8 -*-
"""
    mackerel.tests.test_host
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Mackerel host tests.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :copyright: (c) 2016 Iskandar Setiadi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
from unittest import TestCase
from mock import patch
from mackerel.clienthde import Client
from tests.test_util import dummy_response


class TestHost(TestCase):
    @classmethod
    def setUpClass(cls):
        api_key = os.environ.get('MACKEREL_APIKEY')
        cls.client = Client(mackerel_api_key=api_key)
        cls.id = 'xxxxxxxxxxx'

    @patch('mackerel.clienthde.requests.get')
    def test_should_get_ipaddress(self, m):
        """ Host().ip_addr() should get ipaddress. """
        dummy_response(m, 'fixtures/get_host.json')
        host = self.client.get_host(self.id)
        self.assertEqual(host.ip_addr(), '10.0.2.15')

    @patch('mackerel.clienthde.requests.get')
    def test_should_get_macaddress(self, m):
        """ Host().mac_addr() should get ipaddress. """
        dummy_response(m, 'fixtures/get_host.json')
        host = self.client.get_host(self.id)
        self.assertEqual(host.mac_addr(), '08:00:27:96:ed:36')
