# -*- coding: utf-8 -*-
__author__ = 'Px'

import sys
import json
import base64
import time
import gevent
import requests
import gevent.monkey
from tools import AllUser
gevent.monkey.patch_socket()
from requests.exceptions import ConnectionError
from config.config import PID
from config.config import IP_LIST
reload(sys)
sys.setdefaultencoding('utf8')
STATUS = 1

if __name__ == '__main__':
    for ip in IP_LIST:
        try:
            code = requests.get('http://{}:8090'.format(ip))
        except ConnectionError:
            print '{}网络错误'.format(ip)
            STATUS = 0

    if STATUS:

        try:
            alluser = AllUser(json.loads(requests.get('http://111.62.41.223/user/queryNoInUserByPId?project_id=%s'%base64.b64decode(PID)).content))
            [item.push_info() for item in alluser]
            time.sleep(30)
        except ValueError:
            print "检查项目ID配置"
    else:
        print "请检查网路"

