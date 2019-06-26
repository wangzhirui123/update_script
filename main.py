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
from config.config import PID

reload(sys)
sys.setdefaultencoding('utf8')


if __name__ == '__main__':

    alluser = AllUser(json.loads(requests.get('http://111.62.41.223/user/queryNoInUserByPId?project_id=%s'%base64.b64decode(PID)).content))
    for i in alluser:
        i.push_info()
    time.sleep(30)
