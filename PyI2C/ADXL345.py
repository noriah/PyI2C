#!/usr/bin/python

import math
import time
from I2C_Interface import I2C_Interface

# ADXL345 Library for Python/RasPi
# @author noriah

class ADXL345:


    #


    # Registers
    ADXL_REG_DEVID          =   0x00
    # We dont touch 0x01 through 0x1c, internal use only.
    ADXL_REG_TAP_THRESH     =   0x1d
    ADXL_REG_OFSX           =   0x1e
    ADXL_REG_OFSY           =   0x1f
    ADXL_REG_OFSZ           =   0x20
    ADXL_REG_DUR            =   0x21
    ADXL_REG_LATENT         =   0x22
    ADXL_REG_WINDOW         =   0x23
    ADXL_REG_THRESH_ACT     =   0x24
    ADXL_REG_THRESH_INACT   =   0x25
    ADXL_REG_TIME_INACT     =   0x26
    ADXL_REG_ACT_INACT_CTL  =   0x27
    ADXL_REG_THRESH_FF      =   0x28
    ADXL_REG_TIME_FF        =   0x29
    ADXL_REG_TAP_AXES       =   0x2a
    ADXL_REG_ACT_TAP_STATUS =   0x2b
    ADXL_BW_RATE            =   0x2c
    ADXL_POWER_CTL          =   0x2d
    ADXL_INT_ENABLE         =   0x2e
    ADXL_INT_MAP            =   0x2f
    ADXL_INT_SOURCE         =   0x30
    ADXL_DATA_FORMAT        =   0x31
    ADXL_REG_DATA_X0        =   0x32
    ADXL_REG_DATA_X1        =   0x33
    ADXL_REG_DATA_Y0        =   0x34
    ADXL_REG_DATA_Y1        =   0x35
    ADXL_REG_DATA_Z0        =   0x36
    ADXL_REG_DATA_Z1        =   0x37
    ADXL_REG_FIFO_CTL       =   0x38
    ADXL_REG_FIFO_STATUS    =   0x39
