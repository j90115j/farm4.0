from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import IMG, tlight, thumi, ttemp, tsoil 
from datetime import datetime
from DrPlant.settings import BASE_DIR

from tensorflow.keras.models import load_model
from PIL import Image 
from skimage import transform
import os
import numpy as np 
import tensorflow as tf
from . import fmqtt2

fmqtt2.client.loop_start()

fpath = os.path.join(BASE_DIR, 'static')+'/'
config = tf.compat.v1.ConfigProto(
    device_count={'CPU': 2},
    intra_op_parallelism_threads=1,
    allow_soft_placement=True
)

session = tf.compat.v1.Session(config=config)

tf.compat.v1.keras.backend.set_session(session)
model = load_model(filepath=fpath+'98%.hdfS')
# import pymysql

# Create your views here.
def showindex(request):
	now = datetime.now()

	# # 打开数据库连接
	# db = pymysql.connect("localhost","test123","test123","aiotdb" )
	
	# # 使用 cursor() 方法创建一个游标对象 cursor
	# cursor = db.cursor()
	 
	# # 使用 execute()  方法执行 SQL 查询 
	# cursor.execute("select * from sensors")
	 
	# # 使用 fetchone() 方法获取单条数据.
	# data = cursor.fetchall()

	# time = [str(rows[1]) for rows in data]
	
	# light = [rows[2] for rows in data]
	# now_light = data[-1][2]

	# temp = [rows[3] for rows in data]
	# now_temp = data[-1][3]

	# humid = [rows[4] for rows in data]
	# now_humid = data[-1][4]

	# soil_moisture = [rows[5] for rows in data]
	# now_soil_moisture = data[-1][5]

	# # 关闭数据库连接
	# cursor.close()
	# db.close()

	light = []
	temp = []
	humid = []
	soil_moisture = []
	time_light = []
	time_temp = []
	time_humid = []
	time_soil_moisture = []

	for i in (tlight.objects.values_list('time', flat=True)[::-1])[:10]:
		time_light.append(i)
	now_light_time = time_light[0]
	time_light = time_light[::-1]
	for i in (tlight.objects.values_list('light', flat=True)[::-1])[:10]:
		light.append(i)

	now_light = light[0]
	light = light[::-1]
	for i in (ttemp.objects.values_list('time', flat=True)[::-1])[:10]:
		time_temp.append(i)
	now_temp_time = time_temp[0]
	time_temp = time_temp[::-1]
	for i in (ttemp.objects.values_list('temp', flat=True)[::-1])[:10]:
		temp.append(i)
	now_temp = temp[0]
	temp = temp[::-1]
	for i in (thumi.objects.values_list('time', flat=True)[::-1])[:10]:
		time_humid.append(i)
	now_humid_time = time_humid[0]
	time_humid = time_humid[::-1]
	for i in (thumi.objects.values_list('humi', flat=True)[::-1])[:10]:
		humid.append(i)
	now_humid = humid[0]
	humid = humid[::-1]
	for i in (tsoil.objects.values_list('time', flat=True)[::-1])[:10]:
		time_soil_moisture.append(i)
	now_soil_moisture_time = time_soil_moisture[0]
	time_soil_moisture = time_soil_moisture[::-1]
	for i in (tsoil.objects.values_list('soil', flat=True)[::-1])[:10]:
		soil_moisture.append(i)
	now_soil_moisture = soil_moisture[0]
	soil_moisture = soil_moisture[::-1]


	if request.method == 'POST':
		img = IMG(img_url=request.FILES.get('img'))
		img.save()
		imgs = IMG.objects.all()
		last = imgs[len(imgs)-1]
		tt = last
		return render(request, 'index.html', locals())

	return render(request, 'index.html', locals())



# 清除圖片
def imgShow(request):
	imgs = IMG.objects.all()
	for i in imgs:
		os.remove(BASE_DIR+i.img_url.url)
		i.delete()
	# os.remove(BASE_DIR+imgs[len(imgs)-1].img_url.url)
	# imgs.delete()
	context = {
			'imgs' : imgs
	}
	return render(request, 'imgShow.html', locals())

def detect(request):
	if request.method == 'POST':
		img = IMG(img_url=request.FILES.get('img'))
		img.save()
		imgs = IMG.objects.all()[::-1][0].img_url.url

		# file= fpath+'Septoria_leaf_spot.JPG'
		file = BASE_DIR+imgs
		# msgfmqtt = fmqtt.get_msg()
		np_image = Image.open(file)
		np_image = np.array(np_image).astype('float32')/255
		np_image = transform.resize(np_image, (299,299,3))
		image = np.expand_dims(np_image, axis=0)
		with session.as_default():
				with session.graph.as_default():
						pred = model.predict(image)

		labels={0: 'Bacterial_spot', 
						1: 'Early_blight', 
						2: 'Late_blight', 
						3: 'Leaf_Mold', 
						4: 'Septoria_leaf_spot', 
						5: 'Spider_mites Two-spotted_spider_mite', 
						6: 'Target_Spot', 
						7: 'Yellow_Leaf_Curl_Virus', 
						8: 'Mosaic_virus', 
						9: 'Healthy'}
		predt=np.sort(-pred.reshape(-1))
		tmp=[]
		for i in predt[:3]:
				for j, k in zip(range(10), pred.reshape(-1)):
						if -i==k:
								tmp.append(labels[j])
								tmp.append(k)
								break
		t0 = tmp[0]
		t1 = tmp[1]
		t2 = tmp[2]
		t3 = tmp[3]
		t4 = tmp[4]
		t5 = tmp[5]
	return render(request, 'detect.html', locals())

def dbtest(request):
	light = []
	for i in tlight.objects.values_list('light', flat=True):
		light.append(i)
	now_light = light[-1]

	# light = list(tlight.objects.all())
	# light = tlight.objects.all().values
	# light = tlight.objects.values_list('light', flat=True)
	# n_light= light[-1]
	# tlight(light=342).save()

	# tlight(light=12).save()
	return render(request, 'dbtest.html', locals())

