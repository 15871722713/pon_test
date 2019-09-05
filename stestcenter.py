# -*- coding: utf-8 -*-
# @Author: JinHua
# @Date:   2019-08-29 15:45:50
# @Last Modified by:   JinHua
# @Last Modified time: 2019-09-05 13:37:08

from read_config import get_config_by_name
from StcPython import StcPython
stc = StcPython()


ip = get_config_by_name('STC', 'ip')
slotA = get_config_by_name('STC', 'slotA')
slotB = get_config_by_name('STC', 'slotB')
portA = get_config_by_name('STC', 'portA')
portB = get_config_by_name('STC', 'portB')
macA = get_config_by_name('STC', 'macA')
macB = get_config_by_name('STC', 'macB')


class testCenter(object):
    """docstring for testCenter"""

    def __init__(self):
        stc.log('INFO', 'Starting Test')
        stc.config('automationoptions', logto='stdout', loglevel='INFO')

    def send_packet(self):
        Project = stc.create('project')
        PortTx = stc.create('port', under=Project, location="//{0}/{1}/{2}".format(ip, slotA, portA), useDefaultHost='False')
        PortRx = stc.create('port', under=Project, location="//{0}/{1}/{2}".format(ip, slotB, portB), useDefaultHost='False')
        print('Start to send packets from port {}/{} to port {}/{}'.format(slotA, portA, slotB, portB))
        stc.connect(ip)
        print('Reserve port {0}/{1}/{2} {3}/{4}/{5}'.format(ip, slotA, portA, ip, slotB, portB))
        stc.reserve("{0}/{1}/{2} {3}/{4}/{5}".format(ip, slotA, portA, ip, slotB, portB))
        stc.perform('SetupPortMappings')
        stc.apply()
        print('Create up stream')
        StreamBlock = stc.create('streamBlock', under=PortTx, insertSig='true', frameConfig="", frameLengthMode='FIXED', maxFrameLength=1200, FixedFrameLength=128, loadUnit='BITS_PER_SECOND', load=100, name='StreamBlockPortA')
        Ethernet = stc.create('ethernet:EthernetII', under=StreamBlock, name='sb1_eth', srcMac=macA, dstMac=macB)
        VlanContainer = stc.create('vlans', under=Ethernet)
        stc.create('Vlan', under=VlanContainer, pri=000, cfi=0, id=100, name='vlan100')

        Generator = stc.get(PortTx, 'children-Generator')
        GeneratorConfig = stc.get(Generator, 'children-GeneratorConfig')
        stc.config(GeneratorConfig, DurationMode='BURSTS', BurstSize=10, Duration=100, LoadMode='FIXED', FixedLoad=100, LoadUnit='PERCENT_LINE_RATE', SchedulingMode='PORT_BASED')
        AnaResults = stc.subscribe(Parent=Project, ConfigType='Analyzer', resulttype='AnalyzerPortResults', filenameprefix='Analyzer_Port_Results')
        GenResults = stc.subscribe(Parent=Project, ConfigType='Generator', resulttype='GeneratorPortResults', filenameprefix='Generator_Port_Counter', Interval=2)
        stc.subscribe(Parent=Project, ConfigType='StreamBlock', resulttype='RxStreamSummaryResults', filenameprefix='RxStreamResults')
        stc.apply()
        print('Create dw stream')
        StreamBlock = stc.create('streamBlock', under=PortRx, insertSig='true', frameConfig="", frameLengthMode='FIXED', maxFrameLength=1200, FixedFrameLength=128, loadUnit='BITS_PER_SECOND', load=100, name='StreamBlockPortB')
        Ethernet = stc.create('ethernet:EthernetII', under=StreamBlock, name='sb1_eth', srcMac=macB, dstMac=macA)
        VlanContainer = stc.create('vlans', under=Ethernet)
        stc.create('Vlan', under=VlanContainer, pri=000, cfi=0, id=100, name='vlan100')

        Generator = stc.get(PortRx, 'children-Generator')
        GeneratorConfig = stc.get(Generator, 'children-GeneratorConfig')
        stc.config(GeneratorConfig, DurationMode='BURSTS', BurstSize=10, Duration=100, LoadMode='FIXED', FixedLoad=100, LoadUnit='PERCENT_LINE_RATE', SchedulingMode='PORT_BASED')
        AnaResults = stc.subscribe(Parent=Project, ConfigType='Analyzer', resulttype='AnalyzerPortResults', filenameprefix='Analyzer_Port_Results')
        GenResults = stc.subscribe(Parent=Project, ConfigType='Generator', resulttype='GeneratorPortResults', filenameprefix='Generator_Port_Counter', Interval=2)
        stc.subscribe(Parent=Project, ConfigType='StreamBlock', resulttype='RxStreamSummaryResults', filenameprefix='RxStreamResults')
        stc.apply()

        Analyzer = stc.get(PortRx, 'children-Analyzer')
        stc.perform('AnalyzerStart', AnalyzerList=Project)
        stc.perform('GeneratorStart', GeneratorList=Project)
        stc.sleep(2)
        stc.waitUntilComplete(timeout=100)
        # print("Current analyzer state ", stc.get(Analyzer, 'state'))
        # print("Current generator state ", stc.get(Generator, 'state'))

        stc.perform('GeneratorStop', GeneratorList=Generator)

        AnalyzerResults = stc.get(Analyzer, 'children-AnalyzerPortResults')
        # print('Frames Counts: ', Analyzer)
        # print('\tSignature frames: ', stc.get(AnalyzerResults, 'sigFrameCount'))
        # print('\tTotal frames: ', stc.get(AnalyzerResults, 'totalFrameCount'))
        print('Send packets finished,release stc port {0}/{1}/{2} {3}/{4}/{5}'.format(ip, slotA, portA, ip, slotB, portB))
        stc.release("{0}/{1}/{2} {3}/{4}/{5}".format(ip, slotA, portA, ip, slotB, portB))
        stc.disconnect(ip)

        print('Deleting project')
        stc.delete(Project)


if __name__ == '__main__':
    s = testCenter()
    s.send_packet()
# stc.log('INFO', 'Starting Test')


# stc.config('automationoptions', logto='stdout', loglevel='INFO')

# print('SpirentTestCenter system version: \t', stc.get('system1', 'version'))

# ip = '192.168.0.100'
# iTxSlot = 1
# iRxSlot = 1
# iTxPort = 3
# iRxPort = 4
# szMacAddrPortA = '00: 01: 02: 03: 04: 05'
# szMacAddrPortB = '22: 22: 22: 22: 22: 22'
# hProject = stc.create('project')
# print('Creating ports …')
# hPortTx = stc.create('port', under=hProject, location="//{0}/{1}/{2}".format(ip, iTxSlot, iTxPort), useDefaultHost='False')
# hPortRx = stc.create('port', under=hProject, location="//{0}/{1}/{2}".format(ip, iRxSlot, iRxPort), useDefaultHost='False')


# print("Connecting ", ip)
# stc.connect(ip)
# print('Reserving {0} / {1} / {2} and {3} / {4} / {5}'.format(ip, iTxSlot, iTxPort, ip, iRxSlot, iRxPort))
# stc.reserve("{0}/{1}/{2} {3}/{4}/{5}".format(ip, iTxSlot, iTxPort, ip, iRxSlot, iRxPort))

# print('Set up port mappings')
# stc.perform('SetupPortMappings')

# print('Apply configuration')
# stc.apply()

# hStreamBlock = stc.create('streamBlock', under=hPortTx, insertSig='true', frameConfig="", frameLengthMode='FIXED', maxFrameLength=1200, FixedFrameLength=128, loadUnit='BITS_PER_SECOND', load=100, name='StreamBlockPortA')
# hEthernet = stc.create('ethernet:EthernetII', under=hStreamBlock, name='sb1_eth', srcMac=szMacAddrPortA, dstMac=szMacAddrPortB)

# hVlanContainer = stc.create('vlans', under=hEthernet)
# hVlan = stc.create('Vlan', under=hVlanContainer, pri=000, cfi=0, id=100, name='vlan1')

# print('Configuring Generator')
# hGenerator = stc.get(hPortTx, 'children-Generator')
# hGeneratorConfig = stc.get(hGenerator, 'children-GeneratorConfig')
# stc.config(hGeneratorConfig,
#            DurationMode='BURSTS',
#            BurstSize=1,
#            Duration=100,
#            LoadMode='FIXED',
#            FixedLoad=100,
#            LoadUnit='PERCENT_LINE_RATE',
#            SchedulingMode='PORT_BASED')

# print('Subscribe to results')
# hAnaResults = stc.subscribe(Parent=hProject,
#                             ConfigType='Analyzer',
#                             resulttype='AnalyzerPortResults',
#                             filenameprefix='Analyzer_Port_Results')
# hGenResults = stc.subscribe(Parent=hProject,
#                             ConfigType='Generator',
#                             resulttype='GeneratorPortResults',
#                             filenameprefix='Generator_Port_Counter',
#                             Interval=2)
# stc.subscribe(Parent=hProject,
#               ConfigType='StreamBlock',
#               resulttype='RxStreamSummaryResults',
#               filenameprefix='RxStreamResults',
#               )

# print("\nApply configuration")
# stc.apply()

# print('Start Analyzer')
# hAnalyzer = stc.get(hPortRx, 'children-Analyzer')
# stc.perform('AnalyzerStart', AnalyzerList=hProject)
# print("Current analyzer state ", stc.get(hAnalyzer, 'state'))
# print('Start Generator')
# stc.perform('GeneratorStart', GeneratorList=hProject)
# print('Current generator state', stc.get(hGenerator, 'state'))
# print('Wait 2 seconds …')
# stc.sleep(2)
# print('Wait until generator stops …')
# stc.waitUntilComplete(timeout=100)
# print("Current analyzer state ", stc.get(hAnalyzer, 'state'))
# print("Current generator state ", stc.get(hGenerator, 'state'))
# print('Stop Analyzer')


# stc.perform('GeneratorStop', GeneratorList=hGenerator)

# hAnalyzerResults = stc.get(hAnalyzer, 'children-AnalyzerPortResults')
# print('Frames Counts: ', hAnalyzer)
# print('\tSignature frames: ', stc.get(hAnalyzerResults, 'sigFrameCount'))
# print('\tTotal frames: ', stc.get(hAnalyzerResults, 'totalFrameCount'))


# print('Releasing ports …')
# stc.release("{0}/{1}/{2} {3}/{4}/{5}".format(ip, iTxSlot, iTxPort, ip, iRxSlot, iRxPort))

# print('Disconnect from the chassis …')
# stc.disconnect(ip)

# print('Deleting project')
# stc.delete(hProject)
