# -*- coding: utf-8 -*-
# @Author: JinHua
# @Date:   2019-08-29 11:02:58
# @Last Modified by:   JinHua
# @Last Modified time: 2019-09-06 13:14:26


import os
import configparser


def get_config_by_name(section, name):
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pon_test.cfg')
    cf = configparser.ConfigParser()
    cf.read(file)
    return cf.get(section, name)
