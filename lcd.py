#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lcddriver
from time import sleep
from datetime import datetime
import systemd.daemon
import psutil as ps
from requests import get

I2C_BUS = 1

lcd = lcddriver.lcd(I2C_BUS)

display = [
    "####################",
    "####################",
    "####################",
    "####################",
    ]

def get_hwmon():
    with open('/sys/class/hwmon/hwmon0/temp1_input', 'r') as f:
        data = f.read()
        return int(data)

def get_ext_ip()
    ip = get("https://api.ipify.org").text
    return ip

def loadind():
    lcd.display_string("####################",1)
    lcd.display_string("#SYSTEM  MONITORING#",2)
    lcd.display_string("# LCD SERVICE LOAD #",3)
    lcd.display_string("####################",4)
    sleep(10)
    lcd.clear()
    lcd.backlight_off()

def refresh():
    lcd.display_string("CPU:"+str(ps.cpu_percent()).rjust(4)+"%"+"  "+str(round(get_hwmon()/1000))+"C "+datetime.now().strftime('%d.%m'),1)
    lcd.display_string("MEM:"+str(ps.virtual_memory()[2]).rjust(4)+"%"+"   "+datetime.now().strftime('%H:%M:%S'), 2)

if __name__ == '__main__':
    systemd.daemon.notify('READY=1')
    loadind()
    while True:
        refresh()
        sleep(1)
