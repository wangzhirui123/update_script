# -*- coding: utf-8 -*-
__author__ = 'Px'
import requests
import sys
import base64
import numbers
import json
import time
import gevent
import gevent.monkey
from config.config import PID,IP_LIST
from concurrent.futures import ThreadPoolExecutor
gevent.monkey.patch_socket()
reload(sys)
sys.setdefaultencoding('utf8')

def color_print(msg,color='red', exits=False):

    color_msg = {'blue': '\033[1;36m%s\033[0m',
                 'green': '\033[1;32m%s\033[0m',
                 'yellow': '\033[1;33m%s\033[0m',
                 'red': '\033[1;31m%s\033[0m',
                 'title': '\033[30;42m%s\033[0m',
                 'info': '\033[32m%s\033[0m'}
    msg = color_msg.get(color, 'red') % msg
    print msg

def transcoding(info):
    return base64.b64decode(info)

def deleteinfo(userid,ip):
    '''删除人员'''
    photo_data = {
        'pass':'123456',
        'id':'%s'%userid
            }
    print userid,ip
    result = requests.post('http://{}:8090/person/delete'.format(ip),data=photo_data).content

class AllUser(object):
    def __init__(self,user_list):
        self.pwd = '123456'
        self.user = user_list

    def __get__(self, instance, owner):

        return self.user

    def __getitem__(self, item):

        cls = type(self)
        if isinstance(item,numbers.Integral):
            return cls(user_list = self.user[item])
        return self.user[item]

    def deleteinfo(self,ip):

        photo_data = {
        'pass':'123456',
        'id':'%s'%self.user['id']
            }
        result = requests.post('http://{}:8090/person/delete'.format(ip),data=photo_data).content

    def delete_allinfo(self):
        for i in IP_LIST:
            self.deleteinfo(i)

    def push_photo(self,ip):

        photo_data = {
            'pass':'123456',
            'personId':'%s'%self.user['id'],
            'faceId':'',
            'imgBase64':base64.b64encode(requests.get(self.user['img_oss']).content)
        }
        try:
            photo_result = requests.post(url='http://{}:8090/face/create'.format(ip),data=photo_data).content
            photo_reg_info = json.loads(photo_result)
            if 'false' in photo_result:
                self.deleteinfo(ip)
                print u' {}  {}:照片添加失败-{} 人脸识别设备已删除该人员信息,请重新录入'.format(ip,photo_reg_info['msg'],self.user['realname'])
                
            else:
                print u' {}  {}:照片添加成功-{}'.format(ip,photo_reg_info['data'],self.user['realname'])
                update_user = requests.get('http://111.62.41.156:8010/user/updateUserenterByUserId?user_id=%s'%self.user['id'])
        except Exception as e:
            print e

    def push_personnel(self,ip):

        person_data = {
            'pass':self.pwd,
            'person':'{"id":"%s","idcardNum":"","name":"%s","IDNumber":"","jobNumber":"","facePermission":"1","idCardPermission":"2","faceAndCardPermission":"2","ID Permission":"2"}'%(self.user['id'],self.user['realname'])
        }

        try:*+
            person_result = requests.post('http://{}:8090/person/create'.format(ip),data=person_data).content

            if 'true' in person_result:
                print u' {}  人员信息添加成功-{}'.format(ip,self.user['realname'])
                self.push_photo(ip)
            else:
                print u' {}  人员信息添加失败-{},{} 人脸识别设备已删除该人员信息,请重新录入'.format(ip,self.user['realname'],json.loads(person_result)['msg'])
                self.deleteinfo(ip)
                return None
        except Exception as e:
            print e

    def push_info(self):

        with ThreadPoolExecutor(2)as T:
            T.map(self.push_personnel,IP_LIST)





if __name__ == '__main__':
    # tasks = [gevent.spawn(push_info(i)) for i in all_user(PID)]
    # gevent.joinall(tasks)
    # with ThreadPoolExecutor(20) as T:
    #     T.map(push_info,all_user(PID))
    deleteinfo(1196,'192.168.1.105')
    deleteinfo(1196,'192.168.1.115')
