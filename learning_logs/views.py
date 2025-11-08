from django.shortcuts import render,redirect
from .models import Topic
from .forms import TopicForm


def index(request):
    """the home page for learning logs app"""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """show all topics"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html',context)

def topic(request,topic_id):
    """show details about a single topic"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic,'entries':entries}

    return render(request, 'learning_logs/topic.html',context)

def new_topic(request):
    """add a new topic"""
    if request.method != 'POST':
        #no data submitted; create a blank form.
        form = TopicForm()
    else:
        #post data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')