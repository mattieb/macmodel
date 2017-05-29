#!/usr/bin/env python
#
#   Looks up a Mac's friendly model name.
#
#   Based on http://apple.stackexchange.com/a/98089/21050
#

from subprocess import check_output
from urllib import urlopen
import xml.etree.ElementTree as ET

p_xml = check_output(['system_profiler', '-xml', 'SPHardwareDataType'])
p_root = ET.fromstring(p_xml)

p_dict = p_root.find('array/dict')

def locate_key(elem, search_key):
    """locate a specific key in a dict"""
    for child in elem:
        if child.tag == 'key':
            key = child.text
        elif key == search_key:
            return child
    raise LookupError(search_key)

p_items = locate_key(p_dict, '_items').find('dict')
p_serial = locate_key(p_items, 'serial_number')

serial = p_serial.text

m_xml = urlopen(
    'http://support-sp.apple.com/sp/product?cc=' + serial[-4:]
).read()
m_root = ET.fromstring(m_xml)
m_configcode = m_root.find('configCode')

print m_configcode.text

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
