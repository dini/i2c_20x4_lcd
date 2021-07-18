#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103, C0114

import time
from collections import defaultdict
from datetime import datetime
import systemd.daemon
import psutil as ps
from socket import socket
from requests import get
import lcddriver

I2C_BUS = 1


class CachedValue(object):
    def __init__(self):
        self.timestamp = -1
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self.timestamp = time.time()

    def isOld(self, seconds):
        return (time.time() - self.timestamp) >= seconds


def get_hwmon():
    """Get temp from hwmon"""
    if _cached['hwmon'].isOld(10):
        with open('/sys/class/hwmon/hwmon0/temp1_input', 'r') as f:
            _cached['hwmon'].value = f.read()
    return int(_cached['hwmon'].value)


def get_ext_ip():
    """Get external IP"""
    if _cached['extip'].isOld(60):
        try:
            _cached['extip'].value = get("https://api.ipify.org").text
        except:
            _cached['extip'].value = "No connection"
    return _cached['extip'].value


def get_hddtemp(host):
    """Get temp from hddtemp"""
    if _cached['hddtemp' + host].isOld(15):
        conn = socket()
        conn.connect((host, 7634))
        data = ''
        while True:
            buff = conn.recv(4096)
            if not buff:
                break
            data += buff.decode()
        _cached['hddtemp' + host].value = data
    return _cached['hddtemp' + host].value


def hddtemp(self.host = '127.0.0.1'):
    """Parse hddtemp"""
    data = []
    drive_array = get_hddtemp(self.host).split("||")
    for drive in drive_array:
        if drive[0] != "|":
            drive = "|" + drive
        drive_data = drive.split("|")
        if drive_data[3] == "ERR":
            data.append("ERR")
        elif drive_data[3] == "SLP":
            data.append("SLP")
        elif drive_data[4] != "C":
            data.append("!!!")
        else:
            data.append(drive_data[3] + drive_data[4])
    return data


def loadind():
    """Welcome display"""
    lcd.display_string("####################", 1)
    lcd.display_string("#SYSTEM  MONITORING#", 2)
    lcd.display_string("# LCD SERVICE LOAD #", 3)
    lcd.display_string("####################", 4)
    time.sleep(10)
    lcd.clear()
    lcd.backlight_off()


def refresh():
    """Refresh function"""
    if _cached['cpu'].isOld(3):
        _cached['cpu'].value = str(ps.cpu_percent()).rjust(4)
    cpu_temp = str(round(get_hwmon()/1000))
    date = datetime.now().strftime('%d.%m')
    mem_percent = str(ps.virtual_memory()[2]).rjust(4)
    time = datetime.now().strftime('%H:%M')
    hdd = hddtemp()
    lcd.display_string(
        "CPU:" + _cached['cpu'].value + "%  " + cpu_temp + "C " + date, 1
        )
    lcd.display_string(
        "MEM:" + mem_percent + "%      " + time, 2
        )
    lcd.display_string(
        "SDA:" + hdd[0] + "      SDB:" + hdd[1], 3
        )
    lcd.display_string(
        "IP:" + get_ext_ip(), 4
        )


if __name__ == '__main__':
    systemd.daemon.notify('READY=1')
    lcd = lcddriver.lcd(I2C_BUS)
    loadind()
    _cached = defaultdict(CachedValue)
    while True:
        refresh()
        time.sleep(1)
