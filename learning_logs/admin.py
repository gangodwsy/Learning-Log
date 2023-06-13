from django.contrib import admin

# Register your models here.
from .models import Topic, Entry # 把模型注册到管理网站

admin.site.register(Topic)
admin.site.register(Entry)
