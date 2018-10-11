import re
import json
from urllib.request import urlopen

import Debug

""" container for function gathering information about the client """

class ClientInfo:
    jdata = {}
    
    def __init__(self):
        input_data = self.get_jdata_for_ip_info()
        jdata = json.loads(input_data)

        self.ip = jdata['ip']
        self.hostname = jdata['hostname']
        self.city = jdata['city']
        self.region = jdata['region']
        self.country_flag = jdata['country']
        self.location = jdata['loc']
        self.organisation = jdata['org']

    def get_jdata_for_ip_info(self):
        if Debug.is_offline():
            jdata = """{
                "ip" : "192.168.0.2",
                "hostname" : "hostname.de",
                "city" : "Test City",
                "region" : "Test Region",
                "country" : "DE",
                "loc" : "50.1172,8.7281",
                "postal" : "00001",
                "org" : "Test Ltd"
                }
            """
        else:
            url = 'http://ipinfo.io/json'
            jdata = json.load(urlopen(url))

        return jdata


