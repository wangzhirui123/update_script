# -*- coding: utf-8 -*-
__author__ = 'Px'

import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')

PID = 'MjQ011111'
APPLICATIONLOG_PATH = None

IP_LIST = ['192.168.1.1051','192.168.1.1151']




LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'Log/').replace('\\','/')
a = "3"
if __name__ == '__main__':
    print LOG_PATH
