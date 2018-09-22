#
# Maintainer:   Cambus
# Version:      0.0.1
#
#

import paho.mqtt.client as paho
import socket
import ssl
from time import sleep
from random import uniform


class CamMQttClient:
    def __del__(self):
        print ('MQtt client[] died')

    def __init__(self, pLogger, pOS):
        self.frame = None
        self.logger = pLogger
        self.OS = pOS
        self.connflag = False
        
        self.mqttc = paho.Client()
        self.mqttc.on_connect = self.onConnect
        self.mqttc.on_message = self.onMessage
        #mqttc.on_log = on_log

        
    def doSimpleConnec(self, pHost, pPort):
    
    def doSimpleConnec(self, pHost, pPort):
        awshost = "a3k400xgjmh5lk.iot.us-east-2.amazonaws.com"
        awsport = 8883
        clientId = "Teste"
        thingName = "Teste"
        caPath = "aws-iot-rootCA.pem"
        certPath = "e866e9eb47-certificate.pem.crt.txt"
        keyPath = "e866e9eb47-private.pem.key"

        #mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

        mqttc.connect(awshost, awsport, keepalive=60)

        mqttc.loop_start()

        mqttc.publish("aws/teste", "TEssssssteee", qos=0)

        mqttc.loop_forever()

    
    def onConnect(client, userdata, flags, rc):
        global connflag
        connflag = True
        print("Connection returned result: " + str(rc) )

    def onMessage(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    #def on_log(client, userdata, level, buf):
    #    print(msg.topic+" "+str(msg.payload))

