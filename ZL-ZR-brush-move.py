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
toggle = True
last_mash = 0

# ============= CONFIG =============

# Single push threshold (ms).
# Initial value : 300
config_ms = 300

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
    global last_mash
    if ((data[3] & 0b10000000) == 0b10000000):
        mash_interval = (time.time() - last_mash)
        data2 = bytearray(data)
        if ((data[5] & 0b10000000) == 0b10000000):
            data2[3] |= 0x80
        else:
            if mash_interval >= (1 / config_rate):
                data2[3] |= 0x80
                last_mash = time.time()
                print("Pressed ZR button")
            else:
                data2[3] = data2[3] & 0b01111111
        data = bytes(data2)
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