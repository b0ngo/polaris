#!/bin/python3.7

import clinfo
import Debug
import nordvpnapi

import json
import os
import random
import re
import subprocess

class ServerManagement:
    url = "https://nordvpn.com/api/server"
    
    def __init__(self):
        self.__regions = {}

    def load_servers(self):
        api = nordvpnapi.Api(self.url)
        jdata = api.get_data()
        api.serialize_data(jdata)

        for srv in api.get_servers():
            self.add_server_to_region(srv)

    def add_server_to_region(self, srv):
        key = srv.get_flag()

        if key not in self.__regions:
            self.add_region(key, srv.get_country())

        region = self.__regions[key].add_server(srv)

    def add_region(self, flag, name):
        r = Region(flag, name)
        self.__regions[flag] = r

    def seek_fastest_server(self, flag):
        curr_srv = None
        curr_ping = -1
        
        region = self.__regions.get(flag)

        srvs = region.get_servers()
        l = len(srvs)

        if l > 10:
            srvs = [region.get_servers()[random.randrange(l)]
                for srv in range(10)
            ]

        for srv in srvs:
            ping = self.ping_server(srv)

            if ping == -1:
                continue

            if (curr_ping > ping) or (curr_ping == -1):
                curr_ping = ping
                curr_srv = srv
    
        return curr_srv

    def ping_server(self, srv):
        input = "ping -c 4 " + srv.get_ip() + " | tail -1| awk '{print $4}' | cut -d '/' -f 2"

        try:
            ping = subprocess.Popen(input,
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE,
                                    shell=True)
            output = ping.communicate()
            latency = int(re.findall(r"\d+", output[0].__str__())[0])
        except:
            return -1

        return latency

class ServerManagementOffline(ServerManagement):
    def __init__(self):
        super().__init__();
        Debug.set_offline()

    def load_servers(self):
        api = nordvpnapi.Api(self.url)
        jdata = api.get_data()
        api.serialize_data(jdata)

        for srv in api.get_servers():
            self.add_server_to_region(srv)


class Region:
    def __init__(self, flag, name):
        self.__flag = flag
        self.__name = name
        self.__servers = []

    def add_server(self, srv):
        self.__servers.append(srv)

    def get_server(self, i):
        if i < 0 or i >= len(self.__servers):
            return -1

        return self.__servers[i]

    def get_servers(self):
        return self.__servers

def main(offline_mode):
    if offline_mode:
        Debug.set_offline()

    if Debug.is_offline():
        srv_mgmt = ServerManagementOffline()
    else:
        srv_mgmt = ServerManagement()
    srv_mgmt.load_servers()

    client_info = clinfo.ClientInfo()
    curr_srv = srv_mgmt.seek_fastest_server(client_info.country_flag)

    print(client_info.country_flag)
    print(curr_srv.get_id())
    print(curr_srv.get_ip())
    print(curr_srv.get_flag())
    print(curr_srv.get_name())

main(True)
