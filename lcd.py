#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103, C0114

from time import sleep
from datetime import datetime
import systemd.daemon
import psutil as ps
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
    ip = get("https://api.ipify.org").text
    return ip


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
    time = datetime.now().strftime('%H:%M:%S')
    lcd.display_string(
        "CPU:" + cpu_percent + "%" + "  " + cpu_temp + "C " + date, 1
        )
    lcd.display_string(
        "MEM:" + mem_percent + "%" + "   " + time, 2
        )


if __name__ == '__main__':
    systemd.daemon.notify('READY=1')
    loadind()
    while True:
        refresh()
        sleep(1)
