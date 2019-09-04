# -*- coding: utf-8 -*-
# @Author: JinHua
# @Date:   2019-08-29 11:02:58
# @Last Modified by:   JinHua
# @Last Modified time: 2019-09-04 16:50:26


import os
import ConfigParser


def get_config_by_name(section, name):
    file = os.path.join('test.cfg')
    cf = ConfigParser.ConfigParser()
    cf.read(file)
    return cf.get(section, name)
