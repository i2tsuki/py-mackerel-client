# -*- coding: utf-8 -*-
"""
    mackerel.tests.test_client
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Mackerel client tests.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :copyright: (c) 2016 Iskandar Setiadi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
from unittest import TestCase
from mock import patch
from mackerel.clienthde import Client, MackerelClientError,\
    MackerelMonitorError
from mackerel.host import Host
from mackerel.monitor import MonitorHost, MonitorExternal,\
    MonitorService, MonitorConnectivity
from tests.test_util import dummy_response

class TestClient(TestCase):
    @classmethod
    def setUpClass(cls):
        api_key = os.environ.get('MACKEREL_APIKEY')
        cls.client = Client(mackerel_api_key=api_key)
        cls.id = 'xxxxxxxxxxx'

    @patch('mackerel.clienthde.requests.get')
    def test_should_get_hosts(self, m):
        """ Client().get_hosts() should get host list. """
        dummy_response(m, 'fixtures/get_hosts.json')
        hosts = self.client.get_hosts()
        for host in hosts:
            self.assertTrue(isinstance(host, Host))

    @patch('mackerel.clienthde.requests.get')
    def test_should_get_host(self, m):
        """ Client().get_hosts() should get host. """
        dummy_response(m, 'fixtures/get_host.json')
        host = self.client.get_host(self.id)
        self.assertTrue(isinstance(host, Host))

    @patch('mackerel.clienthde.requests.post')
    def test_should_update_host_poweroff(self, m):
        """ Client().update_host_status('poweroff') should return success. """
        dummy_response(m, 'fixtures/success.json')
        ret = self.client.update_host_status(self.id, 'poweroff')
        self.assertEqual(ret['success'], True)
        with patch('mackerel.clienthde.requests.get') as m:
            dummy_response(m, 'fixtures/poweroff.json')
            host = self.client.get_host(self.id)
            self.assertEqual(host.status, 'poweroff')

    @patch('mackerel.clienthde.requests.post')
    def test_should_update_host_standby(self, m):
        """ Client().update_host_status('standby') should return success. """
        dummy_response(m, 'fixtures/success.json')
        ret = self.client.update_host_status(self.id, 'standby')
        self.assertEqual(ret['success'], True)

        with patch('mackerel.clienthde.requests.get') as m:
            dummy_response(m, 'fixtures/standby.json')
            host = self.client.get_host(self.id)
            self.assertEqual(host.status, 'standby')

    @patch('mackerel.clienthde.requests.post')
    def test_should_update_host_working(self, m):
        """ Client().update_host_status('working') should return success. """
        dummy_response(m, 'fixtures/success.json')
        ret = self.client.update_host_status('2k48zsCx8ij', 'working')
        self.assertEqual(ret['success'], True)
        with patch('mackerel.clienthde.requests.get') as m:
            dummy_response(m, 'fixtures/working.json')
            host = self.client.get_host(self.id)
            self.assertEqual(host.status, 'working')

    @patch('mackerel.clienthde.requests.post')
    def test_should_update_host_maintenance(self, m):
        """ Client().update_host_status('maintenance') should return success. """
        dummy_response(m, 'fixtures/success.json')
        ret = self.client.update_host_status(self.id, 'maintenance')
        self.assertEqual(ret['success'], True)
        with patch('mackerel.clienthde.requests.get') as m:
            dummy_response(m, 'fixtures/maintenance.json')
            host = self.client.get_host(self.id)
            self.assertEqual(host.status, 'maintenance')

    def test_should_update_host_invalid(self):
        """ Client().update_host_status('foo') should raise error. """
        with self.assertRaises(MackerelClientError):
            self.client.update_host_status(self.id, 'foo')

    @patch('mackerel.clienthde.requests.post')
    def test_should_retire(self, m):
        """ Client().retire_host() should return success. """
        dummy_response(m, 'fixtures/success.json')
        ret = self.client.retire_host(self.id)
        self.assertEqual(ret['success'], True)

    @patch('mackerel.clienthde.requests.get')
    def test_should_get_latest_metrics(self, m):
        """ Client().get_latest_metrics() should get metrics. """
        dummy_response(m, 'fixtures/get_latest_metrics.json')
        ret = self.client.get_latest_metrics([self.id],
                                             ['loadavg5', 'memory.free'])
        for k in ['loadavg5', 'memory.free']:
            self.assertTrue(k in ret['tsdbLatest'][self.id].keys())

    @patch('mackerel.clienthde.requests.post')
    def test_should_post_metrics(self, m):
        """ Client().post_metrics() should return success. """
        dummy_response(m, 'fixtures/success.json')
        id = self.id
        metrics = [
            {
                'hostId': id, 'name': 'custom.metrics.loadavg',
                'time': 1401537844, 'value': 1.4
            },
            {
                'hostId': id, 'name': 'custom.metrics.uptime',
                'time': 1401537844, 'value': 500
            }

        ]
        ret = self.client.post_metrics(metrics)
        self.assertEqual(ret['success'], True)

    @patch('mackerel.clienthde.requests.post')
    def test_should_post_service_metrics(self, m):
        """ Client().post_service_metrics() should return success. """
        dummy_response(m, 'fixtures/success.json')
        metrics = [
            {
                'name': 'custom.metrics.latency',
                'time': 1401537844, 'value': 0.5
            },
            {
                'name': 'custom.metrics.uptime',
                'time': 1401537844, 'value': 500
            }
        ]
        ret = self.client.post_service_metrics('service_name', metrics)
        self.assertEqual(ret['success'], True)

    @patch('mackerel.clienthde.requests.post')
    def test_should_raise_error_when_service_not_found(self, m):
        """ Client().post_service_metrics() should raise error when service name not found. """
        dummy_response(m, 'fixtures/error.json', 404)
        metrics = [
            {
                'name': 'custom.metrics.latency',
                'time': 1401537844, 'value': 0.5
            },
            {
                'name': 'custom.metrics.uptime',
                'time': 1401537844, 'value': 500
            }
        ]
        with self.assertRaises(MackerelClientError):
            self.client.post_service_metrics('foobarbaz', metrics)

    @patch('mackerel.clienthde.requests.get')
    def test_should_get_monitors(self, m):
        """ Client().get_monitors() should get monitor list. """
        dummy_response(m, 'fixtures/get_monitors.json')
        monitors = self.client.get_monitors()
        # Value is based on fixtures/get_monitors.json
        for monitor in monitors:
            if monitor.type == 'host':
                self.assertTrue(isinstance(monitor, MonitorHost))
                self.assertEqual(monitor.id, '1ABCDabcde2')
                self.assertEqual(monitor.name, 'loadavg5')
                self.assertEqual(monitor.duration, 3)
                self.assertEqual(monitor.metric, 'loadavg5')
                self.assertEqual(monitor.operator, '>')
                self.assertAlmostEqual(monitor.warning, 3.0)
                self.assertAlmostEqual(monitor.critical, 5.0)
                self.assertIsNone(monitor.notification_interval)
                self.assertEqual(monitor.scopes, [])
                self.assertEqual(monitor.exclude_scopes, ['projectname: v1'])
                self.assertTrue(not monitor.is_mute)
            elif monitor.type == 'service':
                self.assertTrue(isinstance(monitor, MonitorService))
                self.assertEqual(monitor.id, '1ABCDabcde3')
                self.assertEqual(monitor.name, 'DynamoDB.ConsumedReadCapacityUnits.table-name')
                self.assertEqual(monitor.service, 'projectname')
                self.assertEqual(monitor.duration, 1)
                self.assertEqual(monitor.metric, 'DynamoDB.ConsumedReadCapacityUnits.table-name')
                self.assertEqual(monitor.operator, '>')
                self.assertAlmostEqual(monitor.warning, 700.0)
                self.assertAlmostEqual(monitor.critical, 900.0)
                self.assertIsNone(monitor.notification_interval)
                self.assertTrue(not monitor.is_mute)
            elif monitor.type == 'external':
                self.assertTrue(isinstance(monitor, MonitorExternal))
                self.assertEqual(monitor.id, '1ABCDabcde4')
                self.assertEqual(monitor.name, 'example.com')
                self.assertEqual(monitor.url, 'https://example.com/_health/check')
                self.assertIsNone(monitor.service)
                self.assertIsNone(monitor.notification_interval)
                self.assertIsNone(monitor.response_time_warning)
                self.assertIsNone(monitor.response_time_critical)
                self.assertIsNone(monitor.response_time_duration)
                self.assertIsNone(monitor.contains_string)
                self.assertEqual(monitor.max_check_attempts, 3)
                self.assertIsNone(monitor.certificate_expiration_warning)
                self.assertIsNone(monitor.certificate_expiration_critical)
                self.assertTrue(not monitor.is_mute)
            else:
                self.assertTrue(isinstance(monitor, MonitorConnectivity))
                self.assertEqual(monitor.id, '1ABCDabcde1')
                self.assertEqual(monitor.scopes, [])
                self.assertEqual(monitor.exclude_scopes, [])
                self.assertTrue(not monitor.is_mute)

    @patch('mackerel.clienthde.requests.post')
    def test_should_create_monitor(self, m):
        """ Client().create_monitor() should return Monitor id. """
        dummy_response(m, 'fixtures/create_monitor.json')
        params = {
            'type': 'service',
            'name': 'ConsumedReadCapacityUnits.table-name',
            'service': 'HDE',
            'duration': 1,
            'metric': 'ConsumedReadCapacityUnits.table-name',
            'operator': '>',
            'warning': 700,
            'critical': 900
        }
        ret = self.client.create_monitor(params)
        self.assertEqual(ret['id'], '1ABCDabcde1')

    @patch('mackerel.clienthde.requests.get')
    def test_should_update_monitor(self, m):
        """ Client().update_monitor() should update Monitor properly. """
        dummy_response(m, 'fixtures/get_monitors.json')
        monitors = self.client.get_monitors(ids=['1ABCDabcde4'])
        monitor = monitors['1ABCDabcde4']
        with patch('mackerel.clienthde.requests.put') as m:
            dummy_response(m, 'fixtures/update_monitor.json')
            monitor.certificate_expiration_critical = 15
            ret = self.client.update_monitor(
                monitor_id='1ABCDabcde4',
                monitor_params=monitor._to_post_params_dict()
            )
            self.assertEqual(
                ret['id'],
                '1ABCDabcde4'
            )

    @patch('mackerel.clienthde.requests.delete')
    def test_should_delete_monitor(self, m):
        """ Client().delete_monitor() should delete Monitor properly. """
        dummy_response(m, 'fixtures/delete_monitor.json')
        ret = self.client.delete_monitor('1ABCDabcde1')
        self.assertEqual(ret['id'], '1ABCDabcde1')

    @patch('mackerel.clienthde.requests.get')
    def test_should_raise_error_when_get_monitors_newtype(self, m):
        """ Client().get_monitors() should raise error when type is not defined. """
        dummy_response(m, 'fixtures/get_monitors_newtype.json')
        with self.assertRaises(MackerelMonitorError):
            self.client.get_monitors()
