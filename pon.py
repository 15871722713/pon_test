# -*- coding: utf-8 -*-
# @Author: JinHua
# @Date:   2019-08-29 10:59:25
# @Last Modified by:   JinHua
# @Last Modified time: 2019-09-05 13:37:09


import time
import logger
import telnetlib
from read_config import get_config_by_name


ont_ip = get_config_by_name('ONT', 'ip')
ont_port = get_config_by_name('ONT', 'port')

olt_ip = get_config_by_name('OLT', 'ip')
olt_username = get_config_by_name('OLT', 'username')
olt_password = get_config_by_name('OLT', 'password')


class Ont(object):
    """docstring for Ont"""

    def __init__(self):
        self.ip = ont_ip
        self.port = ont_port
        self.ssh = telnetlib.Telnet()
        # self.ssh.set_debuglevel(1)
        self.ont_linux_prompt_regex = b'(\r\n\r?)?(~|/[\w/-_]+) #'
        self.ont_brcm_prompt_regex = b'(\r\n\r?)? >'
        self.ont_prompts = [self.ont_brcm_prompt_regex, self.ont_linux_prompt_regex]
        self.ont_prompt_names = ['ont_brcm', 'ont_linux']
        self.p_ont_brcm = 0
        self.p_ont_linux = 1

    def login(self):
        logger.log('Start to login ont')
        try:
            self.ssh.open(self.ip, self.port)
        except Exception as e:
            logger.log('Network is unreachable')
        self.ssh.write(b'\n')
        i, m, text = self.ssh.expect(self.ont_prompts, timeout=10)
        if i:
            logger.log('Login sucessful')

    def prompt_ont_brcm_to_linux(self):
        self.ssh.write(b'\n')
        self.ssh.read_until(self.ont_brcm_prompt_regex, timeout=5)
        self.ssh.write(b'sh\n')
        self.ssh.read_until(self.ont_linux_prompt_regex, timeout=5)

    def prompt_ont_linux_to_brcm(self):
        self.ssh.write(b'\n')
        self.ssh.read_until(self.ont_linux_prompt_regex, timeout=5)
        self.ssh.write(b'exit\n')
        self.ssh.read_until(self.ont_brcm_prompt_regex, timeout=5)

    def get_ont_prompt(self, p):
        self.ssh.write(b' \n')
        i, m, text = self.ssh.expect(self.ont_prompts, timeout=10)
        if i == self.p_ont_brcm:
            if p == self.p_ont_linux:
                self.prompt_ont_brcm_to_linux()
        elif i == self.p_ont_linux:
            if p == self.p_ont_brcm:
                self.prompt_ont_linux_to_brcm()

    def send_cmd(self, p, c):
        self.get_ont_prompt(p)
        self.ssh.write(c.encode('ascii') + b'\n')
        time.sleep(0.5)
        result = self.ssh.read_very_eager().decode('ascii')
        logger.log('Send ont cmd:{}'.format(c))
        logger.log(result)


class Olt(object):
    """docstring for Olt"""

    def __init__(self):
        self.ip = olt_ip
        self.username = olt_username
        self.password = olt_password
        self.ssh = telnetlib.Telnet()
        # self.ssh.set_debuglevel(1)
        self.login_prompt_regex = b'wuhan>'

    def login(self):
        logger.log('Start to login olt')
        try:
            self.ssh.open(self.ip)
        except Exception as e:
            logger.log('Network is unreachable')
        if self.ssh.read_until(b'Username:', timeout=30):
            self.ssh.write(self.username.encode('ascii') + b'\n')
            if self.ssh.read_until(b'Password:', timeout=30):
                self.ssh.write(self.password.encode('ascii') + b'\n')
                time.sleep(1)
                if self.ssh.read_until(self.login_prompt_regex, timeout=30):
                    logger.log('Login sucessful')
        else:
            logger.log('Login Failed')

    def send_cmd(self, c):
        self.ssh.write(b'\n')
        self.ssh.read_until(self.login_prompt_regex, timeout=5)
        self.ssh.write(c.encode('ascii') + b'\n')
        time.sleep(1)
        result = self.ssh.read_very_eager().decode('ascii')
        logger.log('Send olt cmd:{}'.format(c))
        logger.log(result)


if __name__ == '__main__':
    olt = Olt()
    olt.login()
    olt.send_cmd('show interface vlan')

    ont = Ont()
    ont.login()
    ont.send_cmd(ont.p_ont_brcm, 'wan show')
