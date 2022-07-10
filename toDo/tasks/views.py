from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import Task
from .forms import TaskForm

# Create your views here.
def tasks(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/tasks.html', {'tasks': tasks})

def taskView(request, id):
    task = get_object_or_404(Task, id=id)
    return render(request, 'tasks/task.html', {'task': task})

def newTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.done = False
            task.save()
            messages.info(request, 'Tarefa criada com sucesso!')
            return redirect('/')
    else:
        form = TaskForm()
        return render(request, 'tasks/addtask.html', {'form': form})

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

def deleteTask(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()

    messages.info(request, 'Tarefa deletada com sucesso!')

    return redirect('/')