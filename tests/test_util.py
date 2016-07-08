# -*- coding: utf-8 -*-
"""
    mackerel.tests.test_util
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Utilities for Mackerel tests.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :copyright: (c) 2016 Iskandar Setiadi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import requests

def dummy_response(m, filename, status_code=200):
    response = requests.Response()
    response.status_code = status_code
    root_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(root_path, filename)
    with open(file_path, 'r') as f:
        data = f.read()
        response._content = data
        m.return_value = response
