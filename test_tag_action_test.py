# -*- coding: utf-8 -*-
# @Author: JinHua
# @Date:   2019-08-29 14:59:51
# @Last Modified by:   JinHua
# @Last Modified time: 2019-09-05 13:30:24

import sys
import time
import tcl_cmd
import logger
import unittest
from pon import *
import HTMLTestRunner
from stc import send_packets


timestr = str(time.strftime("%Y%m%d%H%M%S"))
filename = 'tag_action_test_{}.html'.format(timestr)
logname = 'tag_action_test_{}.log'.format(timestr)


class TestTagAction(unittest.TestCase):
    """docstring for TestTagAction"""
    @classmethod
    def setUpClass(self):
        logger.set_log_level(logger.DEBUG)
        logger.logfile(logname)
        logger.log('Set up test')
        global ont, olt, stc
        ont = Ont()
        olt = Olt()
        olt.login()
        ont.login()
        stc = send_packets()
        # time.sleep(5)

    def test001VlanTransparent(self):
        logger.log('Start to test001')
        olt.send_cmd('add eth-svc Data1 to-ont-port 1000/g1 bw-profile CC+-BW svc-tag-action TA01 outer-vlan 100')
        time.sleep(5)
        stc.main(tcl_cmd.cmds)
        rxStreamResult, txStreamResult = stc.get_status()
        self.assertEqual(int(rxStreamResult), 0, msg='Upstream drop  packets')
        self.assertEqual(int(txStreamResult), 0, msg='Dwstream drop  packets')
        ont.send_cmd(ont.p_ont_linux, 'brctl showmacs bronu1')
        olt.send_cmd('show mac on-vlan 100')

    @classmethod
    def tearDownClass(self):
        logger.log('Tearing down test')
        olt.send_cmd('remove eth-svc Data1 from-ont-port 1000/g1')
        # logger.close_log_file()


fp = open('result/{}'.format(filename), 'wb')
suite = unittest.TestLoader().loadTestsFromTestCase(TestTagAction)
runner = HTMLTestRunner.HTMLTestRunner(fp)
runner.run(suite)
fp.close()
