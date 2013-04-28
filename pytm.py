#!/usr/bin/python

import urllib2
from urllib import urlencode
import json
import datetime
import re


class Api(object):
    '''A trademe api'''
    prod_url = 'http://api.trademe.co.nz/v1/'
    sandbox_url = 'http://api.tmsandbox.co.nz/v1/'

    def  __init__(self, test=True):
        if test is True:
            self.base_url = self.sandbox_url
        else:
            self.base_url = self.prod_url

    def get(self, path, query=None):
        self.query = ""
        if query is not None:
            self.query = "?" + urlencode(query)
        url = self.base_url + path + self.query
        r = urllib2.Request(url)
        try:
            response = urllib2.urlopen(r)

            # DEBUG: uncomment to print the full url requested
            #print response.geturl()

        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                # URLError exceptions such as network or connection errors
                #print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                # HTTPError exceptions such as 404 page not found
                #print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
            raise
        else:
            return response

    def search(self, query=None, file_format="json"):
        response = self.get("Search/General." + file_format, query)
        return response.read()

    def search_motors_used(self, query=None,
                           file_format="json"):
        path = "Search/Motors/Used." + file_format
        response = self.get(path, query)
        return response.read()

    def categories(self, category=None, region=None,
                   with_counts=False, file_format="json"):
        if category is None:
            response = self.get("Categories." + file_format)
        else:
            path = "Categories/" + category + "." + file_format
            if with_counts is False:
                response = self.get(path)
            else:
                if region is None:
                    response = self.get(path, {"with_counts": with_counts})
                else:
                    response = self.get(path, {"region": region, "with_counts": with_counts})

        return response.read()

    def categories_updated(self):
        ''' Takes a response like {"LastUpdated":"\/Date(1337834025323)\/"} and returns a datetime object'''
        def as_datetime(dct):
            if 'LastUpdated' in dct:
                m = re.search('\d{10}', dct["LastUpdated"])
                timestamp = int(m.group(0))
                return datetime.datetime.fromtimestamp(timestamp)
            return dct

        path = "Categories/lastupdated.json"
        try:
            response = self.get(path)
            last_updated = json.load(response, object_hook=as_datetime)
        except:
            print "Exception getting last updated - using epoch"
            last_updated = datetime.datetime(1970, 1, 1)
        return last_updated

    def latest(self, page=None, region=None, rows=None, file_format="json"):
        path = "Listings/Latest." + file_format
        query = {}
        if page is not None:
            query["page"] = page

        if region is not None:
            query["region"] = region

        if rows is not None:
            query["rows"] = rows

        if not query:
            query = None

        response = self.get(path, query)
        return response.read()
