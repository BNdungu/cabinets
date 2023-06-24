import network
from machine import Pin

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

led = Pin("LED",Pin.OUT)
led.off()
ssid = 'wifi ssid'
password = 'wifi_password'

if wlan.isconnected():
    wlan.disconnect()

wlan.connect(ssid,password)

while not wlan.isconnected():
    pass
if wlan.isconnected():
    print("Connected to WiFi")
    print(wlan.ifconfig())
    led.on()


