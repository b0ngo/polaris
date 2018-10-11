import urllib.request
import json

import Debug

class Server:
    """ represents one single server node """

    def __init__(self, ident):
        self.__ident = ident
        self.__categories = []

    def __str__(self):
        return f"id: {self.ident}; {self.name}; {self.domain} -> {self.ip}"
    
    def set_name(self, name):
        self.name = name

    def set_ip(self, ip):
        self.ip = ip

    def set_domain(self, domain):
        self.domain = domain

    def set_flag(self, flag):
        self.flag = flag

    def set_country(self, country):
        self.country = country
    
    def set_location(self, latitude, longitude):
        self.location = Serverlocation(latitude, longitude)

    def set_load(self, load):
        self.load = load

    def get_id(self):
        return self.__ident

    def get_name(self):
        return self.name

    def get_ip(self):
        return self.ip

    def get_domain(self):
        return self.domain

    def get_flag(self):
        return self.flag

    def get_country(self):
        return self.country

    def get_location(self):
        return self.location

    def get_load(self):
        return self.load


class Serverlocation:
    """ location of a server """

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

class Api:
    servers = []
    
    def __init__(self, url):
        self.url = url

    def get_server(self, i):
        if i < len(self.servers):
            return self.servers[i]
        return -1

    def get_servers(self):
        return self.servers

    def get_data(self):
        # only in python2
        # response = urllib.urlopen(self.url)
        # data = json.loads(response.read())
        # return data

        if Debug.is_offline():
            txt_file = open("./data/server.json")
            data = txt_file.read()
            txt_file.close()
        else:
            with urllib.request.urlopen(self.url) as url:
                data = url.read()

        return data

    def serialize_data(self, input_data):
        self.servers = []
        jdata = json.loads(input_data)
        
        # maps servers
        for i in range(0, len(jdata) - 1):
            srv = self.map_server(jdata[i]['id'],
                    jdata[i]['name'],
                    jdata[i]['ip_address'],
                    jdata[i]['domain'],
                    jdata[i]['flag'],
                    jdata[i]['country'],
                    jdata[i]['location']['lat'],
                    jdata[i]['location']['long'],
                    jdata[i]['load'])

            self.servers.append(srv)


    def map_server(self, ident, name, ip, domain, flag, country, latitude, longitude, load):
        srv = Server(ident)
        srv.set_name(name)
        srv.set_ip(ip)
        srv.set_domain(domain)
        srv.set_flag(flag)
        srv.set_country(country)
        srv.set_location(latitude, longitude)
        srv.set_load(load)

        return srv


