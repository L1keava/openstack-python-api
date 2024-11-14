#!/usr/bin/python3.6
import requests, json, time

"""
    默认创建名称为： pvm1 的虚拟机
    调用镜像为： pvm_image
    调用云主机类型为： pvm_flavor
    的调用网络为： pvm_int
    请按照实际情况修改本文件！！！
"""

# 全局变量controller ip地址
ip = "10.10.109.188"

class create_vm():
    # 获取token值
    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        data = {
            "auth": {"identity": {"methods": ["password"], "password": {
            "user": {"domain": {"name": "demo"}, "name": "admin", "password": "000000"}}},
            "scope": {"project": {"domain": {"name": "demo"}, "name": "admin"}}}

            }

        rsp = requests.post("http://{}:5000/v3/auth/tokens".format(ip), headers=self.headers, data=json.dumps(data))
        self.headers['X-Auth-Token'] = rsp.headers['X-Subject-Token']


    # 删除之前的pvm1虚拟机
    def delete_vm(self):
        vm_list = requests.get("http://{}:8774/v2.1/servers".format(ip), headers=self.headers)
        for i in vm_list.json()["servers"]:
            if i["name"] == "pvm1":
                requests.delete("http://{}:8774/v2.1/servers/{}".format(ip,i["id"]), headers=self.headers)

    # 获取用于创建虚拟机的镜像id
    def get_image(self):
        image_list = requests.get("http://{}:9292/v2/images".format(ip), headers=self.headers)
        for i in image_list.json()["images"]:
            if i["name"] == "pvm_image":
                self.image_id = i["id"]

    # 获取用于创建虚拟机的云主机类型id
    def get_flavor(self):
        flavor_list = requests.get("http://{}:8774/v2.1/flavors".format(ip), headers=self.headers)
        for i in flavor_list.json()["flavors"]:
            if i["name"] == "pvm_flavor":
                self.flavor_id = i["id"]

    # 获取用于创建虚拟机的网络id
    def get_network(self):
        network_list = requests.get("http://{}:9696/v2.0/networks".format(ip), headers=self.headers)
        for i in network_list.json()["networks"]:
            if i["name"] == "pvm_int":
                self.network_id = i["id"]

    # 创建云主机并做到格式化输出
    def create_vm(self):
        self.delete_vm()
        self.get_image()
        self.get_flavor()
        self.get_network()
        data = {
            'server': {
                'name': 'pvm1', 'imageRef': self.image_id, 'flavorRef': self.flavor_id,
                           'networks': [{'uuid':self.network_id}]
            }
        }
        rsp = requests.post("http://{}:8774/v2.1/servers".format(ip), headers=self.headers, data=json.dumps(data))
        print(vm_data['server']['name'])
        print(rsp.json()['server']['id'])
        print(rsp.json())

# 定义一个创建实例
create_vm().create_vm()