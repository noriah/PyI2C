#!/usr/bin/python

import math
import time
from I2C_Interface import I2C_Interface

# HMC5883L Library for Python/RasPi
# @author noriah

class HMC5883L:

    HMC_I2C_ADDR        =   0x1e # Device I2C Address

    HMC_SCALE           =   0.92 # Axes scale value

    # Configuration Register A
    HMC_MMODE_BIT       =   1 # Measurement Mode bits start
    HMC_MMODE_LEN       =   2 # Measurement Mode bits length
    HMC_MMODE_NORM      =   0x00 # Normal Measurement Config (Default)
    HMC_MMODE_POSB      =   0x01 # Positive bias configuration
    HMC_MMODE_NEGB      =   0x02 # Negative bias configuration
    HMC_MMODE_RES       =   0x03 # Reserved

    HMC_RATE_BIT        =   4 # Rate bits start
    HMC_RATE_LEN        =   3 # Rate bits length
    HMC_RATE_075        =   0x00 # 0.75Hz
    HMC_RATE_1P5        =   0x01 # 1.50Hz
    HMC_RATE_3P0        =   0x02 # 3.00Hz
    HMC_RATE_7P5        =   0x03 # 7.50Hz
    HMC_RATE_15P        =   0x04 # 15.0Hz (Default)
    HMC_RATE_30P        =   0x05 # 30.0Hz
    HMC_RATE_75P        =   0x06 # 75.0Hz
    HMC_RATE_RES        =   0x07 # Reserved

    HMC_AVRG_BIT        =   6 # Averaging bits start
    HMC_AVRG_LEN        =   2 # Averaging bits length
    HMC_AVRG_1          =   0x00 # 1 Sample (Default)
    HMC_AVRG_2          =   0x01 # 2 Samples
    HMC_AVRG_4          =   0x02 # 4 Samples
    HMC_AVRG_8          =   0x03 # 8 Samples

    # Configuration Register B
    HMC_GAIN_BIT        =   7 # Gain bits start
    HMC_GAIN_LEN        =   3 # Gain bits length
    HMC_GAIN_1370       =   0x00 # +/- 0.88 Ga / 1370 Gain LSb/Gauss
    HMC_GAIN_1090       =   0x01 # +/- 1.30 Ga / 1090 Gain LSb/Gauss (Default)
    HMC_GAIN_820        =   0x02 # +/- 1.90 Ga / 820 Gain LSb/Gauss
    HMC_GAIN_660        =   0x03 # +/- 2.50 Ga / 660 Gain LSb/Gauss
    HMC_GAIN_440        =   0x04 # +/- 4.00 Ga / 440 Gain LSb/Gauss
    HMC_GAIN_390        =   0x05 # +/- 4.70 Ga / 390 Gain LSb/Gauss
    HMC_GAIN_330        =   0x06 # +/- 5.60 Ga / 330 Gain LSb/Gauss
    HMC_GAIN_230        =   0x07 # +/- 8.10 Ga / 230 Gain LSb/Gauss

    # Mode Register
    HMC_MODE_BIT        =   1 # Mode bits start
    HMC_MODE_LEN        =   2 # Mode bits length
    HMC_MODE_CONTINUOUS =   0x00 # Continuous-Measurement Mode
    HMC_MODE_SINGLE     =   0x01 # Single-Measurement Mode (Default)
    HMC_MODE_IDLE       =   0x02 # Idle Mode (Power Saving)

    # Status Register
    HMC_LOCK_BIT        =   1 # Data output register lock
    HMC_RDY_BIT         =   0 # Ready Bit

    # Read Registers
    HMC_REG_CFG_A       =   0x00 # Configuration Register A
    HMC_REG_CFG_B       =   0x01 # Configuration Register B
    HMC_REG_CFG_MODE    =   0x02 # Mode Register
    HMC_REG_X_MSB       =   0x03 # Data Output X MSB Register
    HMC_REG_X_LSB       =   0x04 # Data Output X LSB Register
    HMC_REG_Z_MSB       =   0x05 # Data Output Z MSB Register
    HMC_REG_Z_LSB       =   0x06 # Data Output Z LSB Register
    HMC_REG_Y_MSB       =   0x07 # Data Output Y MSB Register
    HMC_REG_Y_LSB       =   0x08 # Data Output Y LSB Register
    HMC_REG_STATUS      =   0x09 # Status Register
    HMC_REG_IDA         =   0x0A # Identification Register A
    HMC_REG_IDC         =   0x0B # Identification Register B
    HMC_REG_IDC         =   0x0C # Identification Register C

    HMC_PRINT_STRING    =   "Raw\tX:\t{0[0]}\tY:\t{0[1]}\tZ:\t{0[2]}\tHead:\t{0[3]}\nScaled\tX:\t{0[4]}\tY:\t{0[5]}\tZ:\t{0[6]}\tHead:\t{0[7]}"


    xFix = 0
    yFix = 0
    zFix = 0

    def __init__(self, bus):
        self.bus = I2C_Interface(self.HMC_I2C_ADDR, bus)

        self.bus.writeByteBits(self.HMC_REG_CFG_A, 0x00, self.HMC_AVRG_8, self.HMC_RATE_15P, self.HMC_MMODE_NORM)
        #self.setMeasurementMode(self.HMC_MMODE_NORM)
        #self.setRate(self.HMC_RATE_15P)
        #self.setAveraging(self.HMC_AVRG_8)

        self.setGain(self.HMC_GAIN_1090)
        self.setOpMode(self.HMC_MODE_CONTINUOUS)
        time.sleep(0.7)

    def __str__(self):
        return self.HMC_PRINT_STRING.format(self.getValues())

    def getRawHeading(self):
        (x, y, z) = self.getRawAxes()
        return self.__calc_head(x, y)

    def getScaledHeading(self):
        (x, y, z) = self.getScaledAxes()
        return self.__calc_head(x, y)

    def getRawAxes(self):
        axes = self.__get_mag_axes()
        return (axes[0], axes[1], axes[2])

    def getScaledAxes(self):
        axes = self.__get_mag_axes()
        return (axes[3], axes[4], axes[5])

    def getAxes(self):
        return self.__get_mag_axes()

    def getRawX(self):
        return self.__get_mag_axes()[0]
    
    def getScaledX(self):
        return self.__get_mag_axes()[3]

    def getRawY(self):
        return self.__get_mag_axes()[1]
    
    def getScaledY(self):
        return self.__get_mag_axes()[4]

    def getRawZ(self):
        return self.__get_mag_axes()[2]

    def getScaledZ(self):
        return self.__get_mag_axes()[5]

    def setXFix(self, value):
        self.xFix = value

    def setYFix(self, value):
        self.yFix = value

    def setZFix(self, value):
        self.zFix = value

    def getValues(self):
        axes = self.getAxes()
        rawHead = round(math.degrees(self.__calc_head(axes[0], axes[1])), 2)
        scaleHead = round(math.degrees(self.__calc_head(axes[3], axes[4])), 2)
        return (axes[0], axes[1], axes[2], rawHead, axes[3], axes[4], axes[5], scaleHead)

    def setMeasurementMode(self, value):
        return self.bus.writeBits(self.HMC_REG_CFG_A,
                                  self.HMC_MMODE_BIT, self.HMC_MMODE_LEN,
                                  value)

    def getMeasurementMode(self):
        return self.bus.writeBits(self.HMC_REG_CFG_A, self.HMC_MMODE_BIT, self.HMC_MMODE_LEN)

    def setRate(self, value):
        return self.bus.writeBits(self.HMC_REG_CFG_A,
                                  self.HMC_RATE_BIT, self.HMC_RATE_LEN,
                                  value)

    def getRate(self):
        return self.bus.writeBits(self.HMC_REG_CFG_A, self.HMC_RATE_BIT, self.HMC_RATE_LEN)

    def setAveraging(self, value):
        return self.bus.writeBits(self.HMC_REG_CFG_A,
                                  self.HMC_AVRG_BIT, self.HMC_AVRG_LEN,
                                  value)

    def getAveraging(self):
        return self.bus.writeBits(self.HMC_REG_CFG_A, self.HMC_AVRG_BIT, self.HMC_AVRG_LEN)

    def setGain(self, value):
        return self.bus.writeBits(self.HMC_REG_CFG_B,
                                  self.HMC_GAIN_BIT, self.HMC_GAIN_LEN,
                                  value)

    def getGain(self):
        return self.bus.readBits(self.HMC_REG_CFG_B, self.HMC_GAIN_BIT, self.HMC_GAIN_LEN)

    def setOpMode(self, value):
        return self.bus.writeBits(self.HMC_REG_CFG_MODE,
                                  self.HMC_MODE_BIT, self.HMC_MODE_LEN,
                                  value)

    def getOpMode(self):
        return self.bus.readBits(self.HMC_REG_CFG_MODE, self.HMC_MODE_BIT, self.HMC_MODE_LEN)

    def getLock(self):
        return self.bus.readBit(self.HMC_REG_STATUS, self.HMC_LOCK_BIT)

    def getRDY(self):
        return self.bus.readBit(self.HMC_REG_STATUS, self.HMC_RDY_BIT)

    def getIDA(self):
        return self.bus.readByte(self.HMC_REG_IDA)

    def getIDB(self):
        return self.bus.readByte(self.HMC_REG_IDB)

    def getIDC(self):
        return self.bus.readByte(self.HMC_REG_IDC)

    def __get_mag_axes(self):
        data = self.bus.readBytesL(self.HMC_REG_X_MSB, 6)
        x = self.bus.val2c((data[0] << 8) | data[1]) + self.xFix
        y = self.bus.val2c((data[4] << 8) | data[5]) + self.yFix
        z = self.bus.val2c((data[2] << 8) | data[3]) + self.zFix

        return [x, y, z, x * self.HMC_SCALE, y * self.HMC_SCALE, z * self.HMC_SCALE]

    def __calc_head(self, x, y, fix_neg = True):
        bearing = math.atan2(y, x)

        if (bearing < 0 and fix_neg):
            bearing += 2 * math.pi

        return bearing



