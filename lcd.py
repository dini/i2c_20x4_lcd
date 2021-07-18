#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103, C0114

from time import sleep
from datetime import datetime
import systemd.daemon
import psutil as ps
from socket import socket
from requests import get
import lcddriver

I2C_BUS = 1

lcd = lcddriver.lcd(I2C_BUS)

display = [
    "####################",
    "####################",
    "####################",
    "####################",
    ]


def get_hwmon():
    """Get temp from hwmon"""
    with open('/sys/class/hwmon/hwmon0/temp1_input', 'r') as f:
        data = f.read()
        return int(data)


def get_ext_ip():
    """Get external IP"""
    try:
        ip = get("https://api.ipify.org").text
    except:
        ip = "No connection"
    return ip


def get_hddtemp():
    """Get temp from hddtemp"""
    conn = socket()
    conn.connect(('127.0.0.1', 7634))
    data = ''
    while True:
        buff = conn.recv(4096)
        if not buff:
            break
        data += buff.decode()
    return data


def hddtemp():
    """Parse hddtemp"""
    data = []
    drive_array = get_hddtemp().split("||")
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
    sleep(10)
    lcd.clear()
    lcd.backlight_off()


def refresh():
    """Refresh function"""
    cpu_percent = str(ps.cpu_percent()).rjust(4)
    cpu_temp = str(round(get_hwmon()/1000))
    date = datetime.now().strftime('%d.%m')
    mem_percent = str(ps.virtual_memory()[2]).rjust(4)
    time = datetime.now().strftime('%H:%M')
    hdd = hddtemp()
    lcd.display_string(
        "CPU:" + cpu_percent + "%  " + cpu_temp + "C " + date, 1
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
    loadind()
    while True:
        refresh()
        sleep(1)
