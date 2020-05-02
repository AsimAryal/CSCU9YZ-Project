"""
author/initial implementation: Dr Kevin Swingler
contributor: Asim Aryal
version: 020420

This is a part of Dissertation+Project submitted in partial fulfilment for the degree of
Bachelor of Science with Honours in Computing Science @ University of Stirling


Project Supervisor: Dr Kevin Swingler
"""
# Setup Instructions -Windows 10
# # Controlling the Bluetooth glove over COM
# 
# - `Windows key + i` to open Settings, select `Devices`
# - Check if ESP32Buzz is paired. If not, add it. Check it is turned on!!
# - Then click `More Bluetooth Options`, go to the COM tab and check device is listed as Outgoing. Find name (COM3)
#  - If not, click `Add` and add the device as outgoing
#  
# Permission denied usually means some other service is connected. It might be this program! Run `ser.close()` to
# free it up.

# Install pyserial before running this

# # Commands to Glove
# 
# - Format is locbuzzduration. Where:
# - loc is four binary digits for trbl
# - buzz is the word buzz
# - duration is in ms
# - Ends with a full stop (.)

import serial
import time

ser = serial.Serial("COM3")
print("COM PORT: ", ser.name)

'''
 location codes:
 t = top, b = bottom, l = left, r = right, a = all
 '''
vibe_location = {'t': '1000', 'r': '0100', 'b': '0010', 'l': '0001', 'a': '1111'}


def open_glove():
    """

    :return: Serial Port in Use for outgoing Bluetooth connection
    """
    return serial.Serial('COM3')


def close_glove():
    """
    Closes serial port
    :return: None
    """
    ser.close()


def buzz(loc, lenms, obj):
    """
    Makes the vibrations happen. A set number of patterns have been programmed
    :param loc: Location of the vibration motor (t, b, l, r, a)
    :param lenms: Length of time in milliseconds
    :param obj: name of object
    :return: None
    """
    if obj == "bottle":
        bottle(loc, lenms)
    elif obj == "fork":
        fork(loc, lenms)
    elif obj == "wine glass":
        wine_glass(loc, lenms)
    elif obj == "cell phone":
        cell_phone(loc, lenms)
    elif obj == "knife":
        knife(loc, lenms)
    else:
        loc_code = vibe_location[loc]
        com = loc_code + 'buzz' + str(lenms) + '.'
        ser.write(str.encode(com))


def buzz_top_right(lenms, obj):
    """
    Vibrates top and right vibration motors
    :param lenms: Length of time in milliseconds
    :param obj: object name
    :return: None
    """
    buzz("t", lenms, obj)
    buzz("r", lenms, obj)


def buzz_top_left(lenms, obj):
    """
    Vibrates top and left vibration motors
    :param lenms: Length of time in milliseconds
    :param obj: object name
    :return: None
    """
    buzz("t", lenms, obj)
    buzz("l", lenms, obj,)


def buzz_bottom_left(lenms, obj):
    """
     Vibrates bottom and left vibration motors
    :param lenms: Length of time in milliseconds
    :param obj: object name
    :return: None
    """
    buzz("b", lenms, obj)
    buzz("l", lenms, obj)


def buzz_bottom_right(lenms, obj):
    """
    Vibrates bottom and right vibration motors
    :param lenms: Length of time in milliseconds
    :param obj: object name
    :return: None
    """
    buzz("b", lenms, obj)
    buzz("r", lenms, obj)


def bottle(loc, lenms):
    """
    Vibrtion pattern for bottle - 3 in a row with 0.1s between each
    :param loc: Location of the vibration motor (t, b, l, r, a)
    :param lenms: Length of time in milliseconds
    :return: None
    """
    for i in range(3):
        loc_code = vibe_location[loc]
        com = loc_code + 'buzz' + str(lenms) + '.'
        ser.write(str.encode(com))
        time.sleep(0.1)


def cell_phone(loc, lenms):
    """
    Vibration pattern for cell-phone - short - long - short
    :param loc: Location of the vibration motor (t, b, l, r, a)
    :param lenms: Length of time in milliseconds
    :return: None
    """
    loc_code = vibe_location[loc]
    com = loc_code + 'buzz' + str(lenms) + '.'
    ser.write(str.encode(com))
    time.sleep(0.1)

    loc_code = vibe_location[loc]
    com = loc_code + 'buzz' + str(lenms+(lenms/3)) + '.'
    ser.write(str.encode(com))
    time.sleep(0.1)

    loc_code = vibe_location[loc]
    com = loc_code + 'buzz' + str(lenms) + '.'
    ser.write(str.encode(com))


def wine_glass(loc, lenms):
    """
        Vibration pattern for wine glass - three in a row with 0.2s between each
        :param loc: Location of the vibration motor (t, b, l, r, a)
        :param lenms: Length of time in milliseconds
        :return: None
        """
    for i in range(3):
        loc_code = vibe_location[loc]
        com = loc_code + 'buzz' + str(lenms) + '.'
        ser.write(str.encode(com))
        lenms = lenms + (lenms / 3)
        time.sleep(0.1)


def fork(loc, lenms):
    """
        Vibration pattern for fork - two consecutive vibrations of different lengths, first short, second long
        :param loc: Location of the vibration motor (t, b, l, r, a)
        :param lenms: Length of time in milliseconds
        :return: None
        """
    loc_code = vibe_location[loc]
    com = loc_code + 'buzz' + str(lenms) + '.'
    ser.write(str.encode(com))
    time.sleep(0.1)
    loc_code = vibe_location[loc]
    com = loc_code + 'buzz' + str(lenms + (lenms / 2)) + '.'
    ser.write(str.encode(com))


def knife(loc, lenms):
    """
        Vibration pattern for knife - two consecutive vibrations of different lengths, first long, second short
        :param loc: Location of the vibration motor (t, b, l, r, a)
        :param lenms: Length of time in milliseconds
        :return: None
        """
    loc_code = vibe_location[loc]
    com = loc_code + 'buzz' + str(lenms) + '.'
    ser.write(str.encode(com))
    time.sleep(0.1)
    loc_code = vibe_location[loc]
    com = loc_code + 'buzz' + str(lenms - (lenms / 3)) + '.'
    ser.write(str.encode(com))


# Test Buzz when starting up
buzz('a', 50, "cell phone")
