#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 05:24:59 2024

Control of CAEN N1470 -- setHV_Off

@author: Lada Chytka (based on CAEN_HV.py from Vlastik Jilek)
"""

from CAENHV import CAENHV
import numpy as np
from time import sleep

dev = "/dev/ttyUSB1"
c = CAENHV(dev)

tolerance = 1 # V

vset = []
for ch in range(4):
    vset.append(c.readParam("VSET", ch))
    c.setOff(ch)
    
vset = np.zeros(4)
vmon = np.ones(4)*9999

print("Ramping DOWN PMTs")
print("PMT1\tPMT2\tPMT3\tPMT4")

while(np.amax(np.abs(vset-vmon)) > tolerance):
    p = ""
    for ch in range(4):
        vmon[ch] = c.readParam("VMON", ch)
        p += "{:.1f}\t".format(vmon[ch])
    print(p)
    sleep(1)