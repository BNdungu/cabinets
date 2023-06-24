import wifi
import time
from machine import Pin
from umqtt.simple import MQTTClient

led = Pin("LED",Pin.OUT)
one = Pin(5,Pin.OUT)
two = Pin(13,Pin.OUT)
three = Pin(14,Pin.OUT)
four = Pin(15,Pin.OUT)
buzzer = Pin(0,Pin.OUT)
buzzer.on()


# Certificate path
cert_file = 'aws/device_cert.crt.der'
key_file = 'aws/privateKey.key.der'

device_id = 'pico'
hostname = 'iot_core_endpoint'

pub_topic = f'pub/topic'
sub_topic = f'sub/topic'



# Init MQTT client
def init_mqtt_client():
    global client
    try:
        with open(key_file, "rb") as f:
            key = f.read()
        with open(cert_file, "rb") as f:
            cert = f.read()
       

        client = MQTTClient(
            client_id=device_id,
            server=hostname,
            port=8883,
            ssl_params={"key": key, "cert": cert},
            keepalive=3600,
            ssl=True
        )
        print("Connecting to AWS server")
        client.connect()
        print(f"MQTT client Connected to AWS server at port 8883")
        print(f"Publish Topic: {pub_topic}")
    except Exception as e:
        print(f'init_mqtt_client error: {e}')


def Open(pin):
        pin.on()
        buzzer.off()
        time.sleep(.5)
        buzzer.on()
        time.sleep(.8)
        buzzer.off()
        time.sleep(.2)
        buzzer.on()
        time.sleep(1)
        pin.off()


def main():
    init_mqtt_client()

    def callback_handler(topic, msg):
        print("Received message")
        msg = msg.decode('utf-8')
        if msg == "1/open":
            pin = one
            Open(pin)
        elif msg == "2/open":
            pin = two
            Open(pin)
        elif msg == "3/open":
            pin = three
            Open(pin)
        elif msg == "4/open":
            pin = four
            Open(pin)
        
            
    
    try:
        global client

        # Subscribe
        client.set_callback(callback_handler)
        client.subscribe(sub_topic)
        while True:
            client.check_msg()

    except Exception as e:
        print(e)
        print("error")


if __name__ == "__main__":
    main()



