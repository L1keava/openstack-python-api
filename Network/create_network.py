#!/usr/bin/python3.6
import requests, json, time

"""
    默认创建名称为： pvm_int 的网络，子网名称为： pvm_intsubnet
    范围为： 192.168.199.0/24

"""

# 全局变量controller ip地址
ip = "10.10.109.188"


class create_network():
    # 获取token值
    def __init__(self):
        self.network_id = None
        self.headers = {'Content-Type': 'application/json'}
        data = {
            "auth": {"identity": {"methods": ["password"], "password": {
                "user": {"domain": {"name": "demo"}, "name": "admin", "password": "11111112"}}},
                     "scope": {"project": {"domain": {"name": "demo"}, "name": "admin"}}}

        }

        rsp = requests.post("http://{}:5000/v3/auth/tokens".format(ip), headers=self.headers, data=json.dumps(data))
        self.headers['X-Auth-Token'] = rsp.headers['X-Subject-Token']

    # 删除之前的网络
    def delete_network(self):
        vm_list = requests.get("http://{}:9696/v2.0/networks".format(ip), headers=self.headers)
        for i in vm_list.json()["networks"]:
            if i["name"] == "pvm_int":
                requests.delete("http://{}:9696/v2.0/networks/{}".format(ip, i["id"]), headers=self.headers)

    # 创建一个网络
    def create_network(self):
        data = {
            "network": {
                'name': "pvm_int",
            }
        }
        rsp = requests.post("http://{}:9696/v2.0/networks".format(ip), data=json.dumps(data), headers=self.headers)
        self.network_id = rsp.json()["network"]["id"]

    # 对该网络创建子网，并做到格式化输出
    def create_subnet(self):
        self.delete_network()
        self.create_network()
        data = {
            "subnet": {
                "network_id": self.network_id,
                "name": "pvm_intsubnet",
                "cidr": "192.168.199.0/24",
                "ip_version": 4
            }}
        rsp = requests.post("http://{}:9696/v2.0/subnets".format(ip), data=json.dumps(data), headers=self.headers)
        print(rsp.json()["subnet"]["name"])
        print(rsp.json()["subnet"]["id"])
        print(rsp.json())


# 定义一个创建实例
create_network().create_subnet()