#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 05:01:06 2024

Control of CAEN N1470 -- getVoltages

@author: Lada Chytka (based on CAEN_HV.py from Vlastik Jilek)
"""

from CAENHV import CAENHV

dev = "/dev/ttyUSB1"
c = CAENHV(dev)

for ch in range(4):
    c.readVolt(ch)
    