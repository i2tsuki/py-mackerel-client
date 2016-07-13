mackerel.clienthde
==================
.. image:: https://travis-ci.org/HDE/py-mackerel-client.svg?branch=hde-dev
    :target: https://travis-ci.org/HDE/py-mackerel-client

.. image:: https://coveralls.io/repos/github/HDE/py-mackerel-client/badge.svg?branch=hde-dev
    :target: https://coveralls.io/github/HDE/py-mackerel-client?branch=hde-dev

mackerel.clienthde is a python library to access Mackerel (https://mackerel.io/).

This project is forked from `heavenshell/py-mackerel-client <https://github.com/heavenshell/py-mackerel-client>`_, which is initially ported from `mackerel-client-ruby <https://github.com/mackerelio/mackerel-client-ruby>`_.

Install
-------

.. code:: shell

  $ pip install mackerel.clienthde


Dependency
----------

mackerel.clienthde use `requests <http://docs.python-requests.org/en/latest/>`_, `simplejson <https://github.com/simplejson/simplejson>`_ and `click <http://click.pocoo.org/3/>`_.

Usage
-----
Get hosts
~~~~~~~~~

.. code:: python

  from mackerel.clienthde import Client

  # Alternatively, you can set MACKEREL_APIKEY as environment variable
  # And simply call "client = Client()"
  client = Client(mackerel_api_key='<Put your API key')
  hosts = client.get_hosts()


Get host
~~~~~~~~

.. code:: python

  from mackerel.clienthde import Client

  # Alternatively, you can set MACKEREL_APIKEY as environment variable
  # And simply call "client = Client()"
  client = Client(mackerel_api_key='<Put your API key')
  host = client.get_host('<hostId>')


Update host status
~~~~~~~~~~~~~~~~~~

.. code:: python

  from mackerel.clienthde import Client

  # Alternatively, you can set MACKEREL_APIKEY as environment variable
  # And simply call "client = Client()"
  client = Client(mackerel_api_key='<Put your API key')
  # Poweroff.
  self.client.update_host_status('<hostId>', 'poweroff')
  # Standby.
  self.client.update_host_status('<hostId>', 'standby')
  # Working.
  self.client.update_host_status('<hostId>', 'working')
  # Maintenance.
  self.client.update_host_status('<hostId>', 'maintenance')

Retire host
~~~~~~~~~~~

.. code:: python

  from mackerel.clienthde import Client

  # Alternatively, you can set MACKEREL_APIKEY as environment variable
  # And simply call "client = Client()"
  client = Client(mackerel_api_key='<Put your API key')
  self.client.retire_host('<hostId>')


Get latest metrics
~~~~~~~~~~~~~~~~~~

.. code:: python

  from mackerel.clienthde import Client

  # Alternatively, you can set MACKEREL_APIKEY as environment variable
  # And simply call "client = Client()"
  client = Client(mackerel_api_key='<Put your API key')
  # Get hostId A's and hostId B's loadavg5, memory.free value.
  metrics = self.client.get_latest_metrics(['<hostId A>', '<hostId B>'],
                                           ['loadavg5', 'memory.free'])



Post metrics
~~~~~~~~~~~~
.. code:: python

  from mackerel.clienthde import Client

  # Alternatively, you can set MACKEREL_APIKEY as environment variable
  # And simply call "client = Client()"
  client = Client(mackerel_api_key='<Put your API key>')
  metrics = [
      {
          'hostId': '<hostId>', 'name': 'custom.metrics.loadavg',
          'time': 1401537844, 'value': 1.4
      },
      {
          'hostId': '<hostId>', 'name': 'custom.metrics.uptime',
          'time': 1401537844, 'value': 500
      }

  ]
  # Post `custom.metrics.loadavg` and `custom.metrics.uptime` to `hostId`.
  client.post_metrics(metrics)


Post service metrics
~~~~~~~~~~~~~~~~~~~~
.. code:: python

  from mackerel.clienthde import Client

  # Alternatively, you can set MACKEREL_APIKEY as environment variable
  # And simply call "client = Client()"
  client = Client(mackerel_api_key='<Put your API key>')
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
  # Post 'custom.metrics.latency' and 'custom.metrics.uptime' to `service_name`.
  self.client.post_service_metrics('service_name', metrics)


Get monitors [NEW in this forked version]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code:: python

  from mackerel.clienthde import Client

  # Alternatively, you can set MACKEREL_APIKEY as environment variable
  # And simply call "client = Client()"
  client = Client(mackerel_api_key='<Put your API key')
  monitors = client.get_monitors()  # list all Monitors
  # Specify list of ids to search, return a dict with id as key
  monitor_targets = client.get_monitors(ids=['1ABCDabcde1'])


Create monitor [NEW in this forked version]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code:: python

  from mackerel.clienthde import Client

  # Alternatively, you can set MACKEREL_APIKEY as environment variable
  # And simply call "client = Client()"
  client = Client(mackerel_api_key='<Put your API key')
  # Create monitor as specified in https://mackerel.io/api-docs/entry/monitors#create
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
  # Post params to Mackerel
  # result['id'] will give Monitor id if create operation succeeded
  result = client.create_monitor(params)


Update monitor [NEW in this forked version]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code:: python

  from mackerel.clienthde import Client

  # Alternatively, you can set MACKEREL_APIKEY as environment variable
  # And simply call "client = Client()"
  client = Client(mackerel_api_key='<Put your API key')
  # Since update Monitor requires all fields to be specified,
  # it is suggested to retrieve the latest value first
  monitor_id = '1ABCDabcde1'
  monitors = client.get_monitors(ids=[monitor_id])
  monitor = monitors[monitor_id]
  # In this example, we assume Monitor is class of MonitorService
  monitor.warning = 800
  monitor.critical = 1000
  # Update params to Mackerel
  result = client.update_monitor(
      monitor_id=monitor_id,
      monitor_params=monitor._to_post_params_dict()
  )


Delete monitor [NEW in this forked version]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code:: python

  from mackerel.clienthde import Client

  # Alternatively, you can set MACKEREL_APIKEY as environment variable
  # And simply call "client = Client()"
  client = Client(mackerel_api_key='<Put your API key')
  # Delete Monitor
  result = client.delete_monitor(monitor_id='1ABCDabcde1')


CLI
---

Get host(s) information from hostname or service, role.

.. code:: shell

  $ mkr.py info [--name foo] [--service service] [--role role]

Set status of a host.

.. code:: shell

  $ mkr.py status --host-id foo --status working

Retire a host.

.. code:: shell

  $ mkr.py retire --host-id foo

Get status of a host.

.. code:: shell

  $ mkr.py status --host-id foo

Authentication
--------------

.. code:: shell

  $ export MACKEREL_APIKEY=foobar
