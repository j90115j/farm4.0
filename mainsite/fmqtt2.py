import paho.mqtt.client as mqtt
from .models import tlight, thumi, ttemp, tsoil 
import time
import decimal
# import pandas as pd
# import numpy as np

read_photocell=False
read_temp=False
read_humi=False
read_tempf=False
read_soil=False
light=[]
temp=[]
humi=[]
soil=[]
# a=np.array([1,2,3,4,5])
# df = pd.DataFrame(a)
# df.columns=["photocell","temp","humi","tempf","soil"]

# 當地端程式連線伺服器得到回應時，要做的動作
def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))

  # 將訂閱主題寫在on_connet中
  # 如果我們失去連線或重新連線時 
  # 地端程式將會重新訂閱
  client.subscribe("command")

# 當接收到從伺服器發送的訊息時要進行的動作
def on_message(client, userdata, msg):
  # 轉換編碼utf-8才看得懂中文
  #print(msg.topic+" "+ msg.payload.decode('utf-8'))
  global read_photocell,read_temp,read_humi,read_tempf,read_soil
  if msg.payload.decode('utf-8')=='photocellVal':
    read_photocell=True
  elif msg.payload.decode('utf-8')=='temp':
    read_temp=True
  elif msg.payload.decode('utf-8')=='humi':
    read_humi=True
  elif msg.payload.decode('utf-8')=='tempf':
    read_tempf=True
  elif msg.payload.decode('utf-8')=='soil_sensorValue':
    read_soil=True
  elif msg.payload.decode('utf-8')=='photo':
    print("")
  else:
    if read_photocell:
      read_photocell=False
      # print("photocell="+msg.payload.decode('utf-8'))
      tmp = str(msg.payload.decode('utf-8'))
      tmp = decimal.Decimal(tmp).quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_DOWN)
      light.append(tmp)
      tlight(light=tmp).save()
      
    elif read_temp:
      read_temp=False
      tmp = str(msg.payload.decode('utf-8'))
      tmp = decimal.Decimal(tmp).quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_DOWN)
      temp.append(tmp)
      ttemp(temp=tmp).save()
    elif read_humi:
      read_humi=False
      tmp = str(msg.payload.decode('utf-8'))
      tmp = decimal.Decimal(tmp).quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_DOWN)
      humi.append(tmp)
      thumi(humi=tmp).save()
    elif read_tempf:
      read_tempf=False
      tempf = msg.payload.decode('utf-8')
    elif read_soil:
      read_soil=False
      tmp = str(msg.payload.decode('utf-8'))
      tmp = decimal.Decimal(tmp).quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_DOWN)
      soil.append(tmp)
      tsoil(soil=tmp).save()



# 連線設定
# 初始化地端程式
client = mqtt.Client()

# 設定連線的動作
client.on_connect = on_connect

# 設定接收訊息的動作
client.on_message = on_message

# 設定登入帳號密碼
# client.username_pw_set("1234","123")

# 設定連線資訊(IP, Port, 連線時間)
client.connect("127.0.0.1", 1883, 60)
# client.connect("34.70.113.250", 1883, 60)
# client.connect("192.168.50.246", 1883, 60)


# 開始連線，執行設定的動作和處理重新連線問題
# 也可以手動使用其他loop函式來進行連接
# client.loop_forever()