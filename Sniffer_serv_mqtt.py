import paho.mqtt.client as mqtt
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util import strxor
import codecs


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("doco/doco")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    payload_dict = json.loads(payload)
    temperature = payload_dict.get("payload")
    cry_bi = base64.b64decode(temperature)
    print("AESKey (crypt):", AesKey[0])
    print("Temperature (crypt):", int(cry_bi.hex(),16) )
    bi = strxor.strxor_c(cry_bi,AesKey[0])
    print("Temperature (decrypt):", int(bi.hex(),16))


key = codecs.decode('000102030405060708090A0B0C0D0E0F','hex_codec')
plaintext = codecs.decode('00112233445566778899AABBCCDDEEFF','hex_codec')

cipher = AES.new(key, AES.MODE_ECB)
AesKey = cipher.encrypt(plaintext)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("198.27.70.149", 443, 60)

client.loop_forever()
