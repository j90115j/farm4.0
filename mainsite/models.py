from django.db import models
from django.utils import timezone

# Create your models here.

# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     slug = models.CharField(max_length=200)
#     body = models.TextField()
#     pub_date = models.DateTimeField(default=timezone.now)

#     class Meta:
#         ordering = ('-pub_date',)

#     def __str__(self):
#         return self.title
class IMG(models.Model):
    # upload_to為圖片上傳的路徑，不存在就創建一個新的。
    img_url = models.ImageField(upload_to='img')

class tlight(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    light = models.FloatField()

    def __str__(self):
        return self.title
    
class ttemp(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    temp = models.FloatField()
    def __str__(self):
        return self.title

class thumi(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    humi = models.FloatField()
    def __str__(self):
        return self.title

class tsoil(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    soil = models.FloatField() 
    def __str__(self):
        return self.title