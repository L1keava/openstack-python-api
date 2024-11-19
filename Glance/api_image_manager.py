#encoding:utf-8
# Copyright 2021~2022 The Cloud Computing support Teams of ChinaSkills.

import requests, json
import logging

# -----------logger-----------
# get logger
logger = logging.getLogger(__name__)
# level
logger.setLevel(logging.DEBUG)
# format
format = logging.Formatter('%(asctime)s %(message)s')
# to console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(format)
logger.addHandler(stream_handler)


# -----------logger-----------

def get_auth_token(controller_ip, domain, user, password):
    '''
    :param controller_ip: openstack master ip address
    :param domain: current user's domain
    :param user: user name
    :param password: user password
    :return: keystone auth Token for current user.
    '''

    try:
        url = "http://{}:5000/v3/auth/tokens".format(controller_ip)
        body = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "domain": {
                                "name": domain
                            },
                            "name": user,
                            "password": password
                        }
                    }
                },
                "scope": {
                    "project": {
                        "domain": {
                            "name": domain
                        },
                        "name": user
                    }
                }
            }
        }

        headers = {
            "Content-Type": "application/json",
        }
        print(body)
        Token = requests.post(url, data=json.dumps(body), headers=headers).headers['X-Subject-Token']

        headers = {
            "X-Auth-Token": Token
        }
        logger.debug(f"获取Token值：{str(Token)}")
        return headers
    except Exception as e:
        logger.error(f"获取Token值失败，请检查访问云主机控制节点IP是否正确？输出错误信息如下：{str(e)}")
        exit(0)


# 镜像管理
class image_manager:
    def __init__(self, handers: dict, resUrl: str):
        self.headers = handers
        self.resUrl = resUrl

    #POST  v2/images
    def create_image(self, image_name: str, container_format="bare", disk_format="qcow2"):
        """

        :param image_name:
        :param container_format:
        :param disk_format:
        :return:
        """
        body = {
            "container_format": container_format,
            "disk_format": disk_format,
            "name": image_name
        }
        response = requests.post(self.resUrl, data=json.dumps(body), headers=self.headers)
        logger.debug(response.status_code)
        if response.status_code == 201:
            return {"ImageItemCreatedSuccess": response.status_code}

        return response.text

    # 获取glance镜像id
    def get_image_id(self, image_name: str):
        result = json.loads(requests.get(self.resUrl, headers=self.headers).text)
        logger.debug(result)
        for item in result['images']:
            if (item['name'] == image_name):
                return item['id']

    # 上传glance镜像
    # Image data¶ Uploads and downloads raw image data.
    # These operations may be restricted to administrators. Consult your cloud operator’s documentation for details.
    # /v2/images/{image_id}/file
    # 镜像可以重名
    def upload_iamge_data(self, image_id: str, file_path=""):
        """

        :param image_id:
        :param file_path:
        :return:
        """
        self.resUrl = self.resUrl + "/" + image_id + "/file"
        self.headers['Content-Type'] = "application/octet-stream"
        response = requests.put(self.resUrl, data=open(file_path, 'rb').read(), headers=self.headers)

        logger.debug(response.status_code)
        if response.status_code == 204:
            return {"ImageItemCreatedSuccess": response.status_code}

        return response.text

    # ----------------------------
    # /v2/images
    # List images
    def get_images(self):
        """

        :return:
        """
        status_code = requests.get(self.resUrl, headers=self.headers).text
        logger.debug(f"返回状态:{str(status_code)}")
        return status_code

    # /v2/images/{image_id} Show image
    def get_image(self, id: str):
        """
        get a flavor by id.
        :return:
        """
        api_url = self.resUrl + "/" + id
        response = requests.get(api_url, headers=self.headers)
        return response.text
        result = json.loads(response.text)
        # logger.debug(f"get return:{str(result)}")
        # return result

    # /v2/images/{image_id} Delete image
    def delete_image(self, id: str):
        """
         delete a image by id.
         :return:
         """
        api_url = self.resUrl + "/" + id
        response = requests.delete(api_url, headers=self.headers)

        # 204 - No Content	The server has fulfilled the request.
        if response.status_code == 204:
            return {"Image itemDeletedSuccess": response.status_code}

        result = json.loads(response.text)
        logger.debug(f"delete return:{str(result)}")
        return result

        # http://192.168.200.226:8774/v2.1/ get apis version infomation.


if __name__ == '__main__':
    # 1. openstack allinone （controller ) credentials
    # host ip address
    # controller_ip = "10.24.2.22"
    controller_ip = "controller"
    # controller_ip = "10.24.2.22"
    # domain name
    domain = "demo"
    # user name
    user = "admin"
    # user password
    password = "000000"
    headers = get_auth_token(controller_ip, domain, user, password)
    print("headers:", headers)

    #  http://controller:9292
    image_m = image_manager(headers, "http://controller:9292/v2/images")


    #1. 查询有没有
    id = image_m.get_image_id(image_name="cirros001")
    print("cirros001，id为: ", id)

    if id:
        # 4. delete a user
        result = image_m.delete_image(id)
        print(f"delete{id} images:", result)

    #2. 创建
    result = image_m.create_image(image_name="cirros001")  # 调用glance-api中创建镜像方法
    print(f"create cirros001 image:", result)
    #3 上传
    id = image_m.get_image_id(image_name="cirros001")
    print("upload cirros001，id: ", id)
    #
    result = image_m.upload_iamge_data(id, file_path="cirros-0.3.4-x86_64-disk.img")
    print(f"upload {id} image:", result)
    #3
    import time
    time.sleep(60)
    id = image_m.get_image_id(image_name="cirros001")
    print("find id:", id)
    result = image_m.get_image(id)
    print(f"find {id} image:", result)
    print("-----------finished----------")

    # 判分方式
    # 1json结果
    # 2 openstack image 查询结果