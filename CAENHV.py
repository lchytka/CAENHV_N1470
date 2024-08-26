#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 04:24:48 2024

Control of CAEN N1470

@author: Lada Chytka (based on CAEN_HV.py from Vlastik Jilek)
"""

import serial

class CAENHV:
    def __init__(self, dev="/dev/ttyUSB0"):
        self.s = serial.Serial(dev,9600,timeout=1)
    
    def __del__(self):
        self.s.close()
        
    def setParam(self,param,ch,val):
        if param in {"VSET", "ISET", "RUP", "RDW", "MAXV", "IMAX"}:
            match param:
                case "VSET":
                    cmd = '$BD:00,CMD:SET,CH:{},PAR:{},VAL:{:.1f}\r\n'.format(ch,param,val)
                case "ISET":
                    cmd = '$BD:00,CMD:SET,CH:{},PAR:{},VAL:{:.2f}\r\n'.format(ch,param,val)
                case _:
                    cmd = '$BD:00,CMD:SET,CH:{},PAR:{},VAL:{}\r\n'.format(ch,param,val)
            self.s.write(cmd.encode('ascii'))
            self.s.readline()
        else:
            print("ERROR: Set {} not implemented".format(param))
            
    def readParam(self,param,ch):
        if param in {"VSET", "ISET", "RUP", "RDW", "MAXV", "IMAX", "IMON", "VMON"}:
            cmd = '$BD:00,CMD:MON,CH:{},PAR:{}\r\n'.format(ch,param)
            self.s.write(cmd.encode('ascii'))
            answ = self.s.readline()
            return float(answ.decode().split(":")[3].split("\r")[0])
        else:
            print("ERROR: Read {} not implemented".format(param))
        
    def setVolt(self, ch, val):
        print("Seting HV of Ch {} to {:.1f}".format(ch,val))
        self.setParam("VSET",ch,val)
        self.readParam("VSET", ch)
        
    def readVolt(self,ch):
        print("PMT {} Vmon: {:.1f}".format(ch+1,self.readParam("VMON", ch)))
        
    def setOn(self,ch):
        cmd = '$BD:00,CMD:SET,CH:{},PAR:ON\r\n'.format(ch)
        self.s.write(cmd.encode("ascii"))
        self.s.readline()
        
    def setOff(self,ch):
        cmd = '$BD:00,CMD:SET,CH:{},PAR:OFF\r\n'.format(ch)
        self.s.write(cmd.encode("ascii"))
        self.s.readline()
        