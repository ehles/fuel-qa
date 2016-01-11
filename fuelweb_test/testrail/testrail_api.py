import requests
import urllib2
import json

class APIClient:
    def __init__(self, base_url, username='', password=''):
        self.user = username
        self.password = password
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url + 'index.php?/api/v2/'

    def send_get(self, uri):
        return self.__send_request('GET', uri, None)

    def send_post(self, uri, data):
        return self.__send_request('POST', uri, data)

    def __send_request(self, method, uri, data):
        url = self.__url + uri
        request = urllib2.Request(url)

        headers = {'Content-type': 'application/json'}


        e = None
        try:
            if (method == 'POST'):
                response = requests.post(url,
                                         headers=headers,
                                         auth=(self.user, self.password),
                                         data=json.dumps(data)).json()
            else:
                response = requests.get(url,
                                        headers=headers,
                                        auth=(self.user, self.password)).json()
        except urllib2.HTTPError as e:
            response = e.read()

        if response:
            result = response
        else:
            result = {}

        if e != None:
            if result and 'error' in result:
                error = '"' + result['error'] + '"'
            else:
                error = 'No additional error message received'
            raise APIError('TestRail API returned HTTP %s (%s)' %
                           (e.code, error))

        return result


class APIError(Exception):
    pass
