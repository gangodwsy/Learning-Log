from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):#创建一个最简单的模型表单
	class Meta:
		model = Topic#根据哪个模型创建表单
		fields = ['text']#该表单只包含字段text
		labels = {'text': ''}#这里表示不要为字段text生成标签

class EntryForm(forms.ModelForm):
	class Meta:
		model = Entry
		fields = ['text']
		labels = {'text': ' '}
		widgets = {'text': forms.Textarea(attrs={'cols': 80})}