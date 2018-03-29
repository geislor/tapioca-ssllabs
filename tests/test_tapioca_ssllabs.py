# coding: utf-8

import unittest
import json
from argparse import Namespace

from tapioca_ssllabs import SslLabs
from tapioca_ssllabs.exceptions import InvocationErrorException


class TestTapiocaSslLabs(unittest.TestCase):

    def setUp(self):
        self.wrapper = SslLabs()

    def test_info(self):
        response = self.wrapper.info().get()
        info = response().data
        self.assertEqual(info.get('engineVersion'), '1.31.0')

    def test_analyze(self):
        params = {'host': 'www.ssllabs.com'}

        response = self.wrapper.analyze().get(params=params)
        analyze = json.loads(json.dumps(response().data), object_hook=lambda d: Namespace(**d))
        self.assertEqual(analyze.host, 'www.ssllabs.com')

    def test_analyze_bad_input(self):
        params = {'host': '.invalid.host', 'startNew': 'on'}
        try:
            self.wrapper.analyze().get(params=params)

            # should not get to this point, as InvocationErrorException must have been raised
            self.assertTrue(False)

        except InvocationErrorException as e:
            self.assertEqual('Invalid host', str(e))

    def test_get_endpoint_data(self):
        params = {'host': 'www.ssllabs.com',
                  's': '64.41.200.100'}

        response = self.wrapper.get_endpoint_data().get(params=params)
        endpoint = json.loads(json.dumps(response().data), object_hook=lambda d: Namespace(**d))
        self.assertEqual(endpoint.serverName, 'www.ssllabs.com')

    def test_get_status_codes(self):
        response = self.wrapper.get_status_codes().get()
        info = response().data
        self.assertIsNotNone(info.get('statusDetails'))


if __name__ == '__main__':
    unittest.main()
