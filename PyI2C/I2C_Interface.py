#!/usr/bin/python

import smbus
import math
import time

# SMBus I2C Interface
# @author noriah


class I2C_Interface:

    def __init__(self, addr, bus = smbus.SMBus(1)):
        self.bus = bus
        self.addr = addr

    def readByte(self, reg):
        return self.bus.read_byte_data(self.addr, reg)

    def readBytes(self, regs):
        return [self.readByte(reg) for reg in regs]

    def readBytesL(self, reg, number):
        return [self.readByte(reg + i) for i in xrange(0, number)]

    # PyComms - https://github.com/cTn-dev/PyComms
    def readBits(self, reg, start, length):
        byte = self.readByte(reg)

        bMask = ((1 << length) - 1) << (start - length + 1)
        byte &= mask
        byte >>= (start - length + 1)
        return byte

    # PyComms - https://github.com/cTn-dev/PyComms
    def readBit(self, reg, bit):
        byte = self.readByte(reg)
        value = byte & (1 << bit)
        return value

    def writeByte(self, reg, value):
        return self.bus.write_byte_data(self.addr, reg, value)

    def writeByteBits(self, reg, b1, b2, b3, b4):
        data = (b1 << 6)
        data |= (b2 << 4)
        data |= (b3 << 2)
        data |= b4
        self.writeByte(reg, data)

    # PyComms - https://github.com/cTn-dev/PyComms
    def writeBits(self, reg, start, length, value):
        byte = self.readByte(reg)
        bMask = ((1 << length) - 1) << (start - length + 1)
        value <<= (start - length + 1)
        value &= bMask
        byte  &= ~(bMask)
        byte |= value

        return self.writeByte(reg, byte)

    def val2c(self, val):
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val
