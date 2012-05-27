#!/usr/bin/env python
import unittest
from pytm import Api
import urllib2
import datetime
import json

class TestApi(unittest.TestCase):
    def setUp(self):
        self.api = Api()

    def tearDown(self):
        self.api = None

    def test_get(self):
        r = self.api.get("Search/General.json")
        self.assertIsInstance(r, urllib2.addinfourl)

        self.assertRaises(urllib2.HTTPError,
                          self.api.get,"Search/GeneralJason")

    def test_search(self):
        response = self.api.search()
        self.assertEqual(response,
        '{"TotalCount":0,"Page":1,"PageSize":0,"List":[],"FoundCategories":[]}')

    def test_search_motors_used(self):
        response = self.api.search_motors_used()
        self.assertIsNotNone(response)

    def test_categories(self):
        response = self.api.categories("0001-1484")
        self.assertIsNotNone(response)

    def test_categories_updated(self):
        last_updated = self.api.categories_updated()
        self.assertIsInstance(last_updated, datetime.datetime)

    def test_latest(self):
        r1 = self.api.latest()
        self.assertIsNotNone(r1)
        r2 = self.api.latest(page=2)
        self.assertIsNotNone(r2)
        r3 = self.api.latest(rows=1)
        self.assertIsNotNone(r3)
        r4 = self.api.latest(region=1)
        self.assertIsNotNone(r4)
        r5 = self.api.latest(page=2,rows=1,region=1,file_format="json")
        self.assertIsNotNone(r5)
        latest = json.loads(r5)
        self.assertTrue("List" in latest)

if __name__ == '__main__':
    unittest.main()

