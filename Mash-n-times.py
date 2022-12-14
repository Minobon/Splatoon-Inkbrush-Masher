#!/usr/bin/env python3

import os
import threading
import time
import keyboard

# Re-connect USB Gadget device
os.system('echo > /sys/kernel/config/usb_gadget/procon/UDC')
os.system('ls /sys/class/udc > /sys/kernel/config/usb_gadget/procon/UDC')

time.sleep(0.5)

# HID Device ID
gadget = os.open('/dev/hidg0', os.O_RDWR | os.O_NONBLOCK)
procon = os.open('/dev/hidraw0', os.O_RDWR | os.O_NONBLOCK)

# Global variables
last_ZR = False
ZR_on = 0
count = 0
mash_flag = False
toggle = True
last_mash = 0

# ============= CONFIG =============

# Single push threshold (ms).
# Initial value : 300
config_ms = 300

# Number of shots (integer).
# Initial value : 6
config_count = 6

# Mash function switch key (one character).
# Initial value : 'p'
config_key = 'p'

# Mash rate [times per second] (numerical value)
# Initial value : 30
config_rate = 30

# ==============================

def procon_input():
    while True:
        try:
            input_data = os.read(gadget, 128)
            #print('>>>', input_data.hex())
            os.write(procon, input_data)
        except BlockingIOError:
            pass
        except:
            os._exit(1)

def toggle():
    global toggle
    while True:
        time.sleep(1/10)
        if keyboard.is_pressed(config_key):
            if toggle:
                toggle = False
                print("Mash function switched off.")
            else:
                toggle = True
                print("Mash function switched on.")

def mash(data):
    global last_ZR, ZR_on, count, mash_flag, config_ms, config_count, last_mash
    if not last_ZR:
        if ((data[3] & 0b10000000) == 0b10000000):
            #ZR off -> on
            ZR_on = time.time()
            last_ZR = True
        else:
            pass
    else: 
        if ((data[3] & 0b10000000) == 0b10000000):
            last_ZR = True
        else:
            #ZR on -> off
            pressed_time = (time.time() - ZR_on) * 1000
            if pressed_time <= config_ms:
                mash_flag = True
                count = 0
                last_mash = time.time()
                print("ZR button shortly pressed")
            else:
                pass
            last_ZR = False
    if mash_flag:
        mash_interval = (time.time() - last_mash)
        if count >= config_count:
            mash_flag = False
        if mash_interval >= (1 / config_rate):
            data2 = bytearray(data)
            data2[3] |= 0x80
            data = bytes(data2)
            last_mash = time.time()
            count = count + 1
            print("Pressed ZR button")
        else:
            pass
    return data

def procon_output():
    while True:
        try:
            output_data = os.read(procon, 128)
            #print('<<<', output_data.hex())
            if toggle:
                output_data_2 = mash(output_data)
            else:
                output_data_2 = output_data
            os.write(gadget, output_data_2)
        except BlockingIOError:
            pass
        except Exception as e:
            print(e)
            os._exit(1)

threading.Thread(target=toggle).start()
threading.Thread(target=procon_input).start()
threading.Thread(target=procon_output).start()