from re import U
from turtle import update
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
import datetime 

# Create your views here.
@login_required
def tasks(request):
    search = request.GET.get('search', '')
    tasksDone = Task.objects.filter(completed = True, user=request.user).count()
    tasksDoing = Task.objects.filter(completed = False, user=request.user).count()
    try: 
        proportion = round(float(tasksDone / (tasksDone + tasksDoing)),2)
    except ZeroDivisionError:
        proportion = 0

    if search:
        tasks = Task.objects.filter(title__icontains=search, user=request.user)
    else:
        taskList = Task.objects.all().order_by('-created_at').filter(user=request.user)

        paginator = Paginator(taskList, 5)
        page = request.GET.get('page')
        tasks = paginator.get_page(page)
    
    return render(request, 'tasks/tasks.html', {'tasks': tasks, 'tasksDone': tasksDone, 'tasksDoing': tasksDoing, 'proportion': proportion})

@login_required
def taskView(request, id):
    task = get_object_or_404(Task, id=id)
    return render(request, 'tasks/task.html', {'task': task})

@login_required
def newTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.done = False
            task.user = request.user
            task.save()
            messages.info(request, 'Tarefa criada com sucesso!')
            return redirect('/')
    else:
        form = TaskForm()
        return render(request, 'tasks/addtask.html', {'form': form})

@login_required
def editTask(request, id):
    task = get_object_or_404(Task, id=id)
    form = TaskForm(instance=task)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task.save()
            messages.info(request, 'Tarefa editada com sucesso!')
            return redirect('/')
        else:
            return render(request, 'tasks/edittask.html', {'form': form, 'task': task})
    else:
        return render(request, 'tasks/edittask.html', {'form': form, 'task': task})

@login_required
def deleteTask(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()

    messages.info(request, 'Tarefa deletada com sucesso!')

    return redirect('/')

@login_required
def changeStatus(request, id):
    task = get_object_or_404(Task, id=id)
    if task.completed:
        task.completed = False
    else:
        task.completed = True
    
    task.save()

    return redirect('/')