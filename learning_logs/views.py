from django.shortcuts import render,redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


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
            return redirect('learning_logs:topics')#redirect function 
        #display a blank or invalid form 
    context = {'form':form}
    return render(request, 'learning_logs/new_topic.html',context)

def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form =  EntryForm()
    else:
        #Post data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)#still havent saved it in the database yet cause we need to attach it to the topic 
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
        
    #display a blank or invalid form
    context = {'topic':topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html',context)

def edit_entry(request, entry_id):
    """edit an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic# we are setting this topic for later so that we can redirect back to topic 

    if request.method !=  'POST':
        #initial request; pre-fill form with the current entry
        form = EntryForm(instance=entry)#means a build a form using this specific antry as the source so all current values appear in the inputs 
    else:
        #POST data submitted; process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)#redirecting to topics page 
        
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)
