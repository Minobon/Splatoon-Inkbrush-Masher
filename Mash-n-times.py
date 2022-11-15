#!/usr/bin/env python3

import os
import threading
import time
import keyboard

# Re-connect USB Gadget device
os.system('echo > /sys/kernel/config/usb_gadget/procon/UDC')
os.system('ls /sys/class/udc > /sys/kernel/config/usb_gadget/procon/UDC')

time.sleep(0.5)

gadget = os.open('/dev/hidg0', os.O_RDWR | os.O_NONBLOCK)
procon = os.open('/dev/hidraw0', os.O_RDWR | os.O_NONBLOCK)

last_ZR = False
ZR_on = 0
count = 0
rapid_fire_flag = False
toggle = True

#Judgment threshold (in ms).
config_ms = 300

#Number of shots (in integer).
config_count = 3

#Toggle key
config_key = 'p'

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
                print("Rapid-fire function switched off.")
            else:
                toggle = True
                print("Rapid-fire function switched on.")


def rensya(data):
    global last_ZR, ZR_on, count, rapid_fire_flag, config_ms, config_count
    if not last_ZR:
        if data[3] >= 0x80:
            #ZR off -> on
            ZR_on = time.time()
            last_ZR = True
        else:
            pass
    else: 
        if data[3] >= 0x80:
            pass
        else:
            #ZR on -> off
            pressed_time = (time.time() - ZR_on) * 1000
            if pressed_time <= config_ms:
                rapid_fire_flag = True
                count = 0
                print("ZR button shortly pressed")
            else:
                pass
            last_ZR = False
    if rapid_fire_flag:
        count = count + 1
        d_counfig_count = config_count * 6
        if count == d_counfig_count :
            rapid_fire_flag = False
        if count % 6 >= 2:
            data2 = bytearray(data)
            data2[3] |= 0x80
            data = bytes(data2)
        if count % 6 == 0:
            print("Pressed ZR button")
    return data

def procon_output():
    while True:
        try:
            output_data = os.read(procon, 128)
            #print('<<<', output_data.hex())
            if toggle:
                output_data_2 = rensya(output_data)
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