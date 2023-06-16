from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
	"""学习笔记的主页"""
	return render(request, 'learning_logs/index.html')#这里为什么不用在前面加templates

@login_required
def topics(request):
	"""显示所有的主题"""
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')#查询数据库请求提供Topic对象,并排序
	context = {'topics':topics}
	return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
	"""显示单个主题及其所有的条目"""
	#topic = Topic.objects.get(id=topic_id)
	topic = get_object_or_404(Topic, id=topic_id)#优化一下错误页面

	check_topic_owner(topic, request)

	entries = topic.entry_set.order_by('-date_added')
	context = {'topic':topic, 'entries':entries}
	return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
	"""添加主题"""

	#添加主题的话不用设置保护性404

	if request.method != 'POST':
		#未提交数据创建一个新表单
		form = TopicForm()
	else:
		#POST提交的数据：对数据进行处理
		form = TopicForm(data=request.POST)
		if form.is_valid():
			#form.save()#将表单数据保存到数据库
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return redirect('learning_logs:topics')

	# 显示空表单或指出表单数据无效
	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
	"""在特定主题中添加新条目"""
	#topic = Topic.objects.get(id=topic_id)
	topic = get_object_or_404(Topic, id=topic_id)

	check_topic_owner(topic, request)

	if request.method != 'POST':
		# 未提交数据：创建一个空表单
		form = EntryForm()
	else:
		# POST提交的数据：对数据进行处理
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)#创建一个新的条目对象
			new_entry.topic = topic#并设置新条目对象的topic属性
			new_entry.save()#把条目保存到数据库，并将其与正确的主题相关联(注意和上面做区分)
			return redirect('learning_logs:topic', topic_id=topic_id)

	#显示空表单或指出表单数据无效
	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	"""编辑既有的条目"""
	#entry = Entry.objects.get(id=entry_id)
	entry = get_object_or_404(Entry, id=entry_id)
	topic = entry.topic

	check_topic_owner(topic, request)

	if request.method != 'POST':
		#初次请求，使用当前条目填充表单
		form = EntryForm(instance=entry)
	else:
		#POST提交的数据：对数据进行处理
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('learning_logs:topic', topic_id=topic.id)

	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)

# 自己重构的函数。对topic, new_entry, edit_entry页面提供保护
def check_topic_owner(topic, request):
	if(topic.owner != request.user):
		raise Http404
