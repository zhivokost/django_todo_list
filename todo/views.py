from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todos
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# домашняя страница
def home(request):
    return render(request, 'todo/home.html')

# регистрация пользователя
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username.'})
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})


# вход пользователя
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')



# выход пользователя
@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


# создание задачи/дела
@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit = False)
            newtodo.user_id = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Bad data passed in. Try again.'})


# список актуальных задач
@login_required
def currenttodos(request):
    todoss = Todos.objects.filter(user_id = request.user, date_complete__isnull = True)
    return render(request, 'todo/currenttodos.html', {'todoss': todoss})


# список завершенных задач
@login_required
def completetodos(request):
    todoss = Todos.objects.filter(user_id = request.user, date_complete__isnull = False).order_by('-date_complete')
    return render(request, 'todo/completetodos.html', {'todoss': todoss})


# просмотр деталей задачи
@login_required
def viewtodo(request, todo_pk):
    todo_id = get_object_or_404(Todos, pk = todo_pk, user_id = request.user)
    if request.method == 'GET':
        form = TodoForm(instance = todo_id)
        return render(request, 'todo/viewtodo.html', {'todo_id': todo_id, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance = todo_id)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo_id': todo_id, 'form': form, 'error': 'Bad info'})

# отметить задачу как выполненную
@login_required
def completetodo(request, todo_pk):
    todo_id = get_object_or_404(Todos, pk = todo_pk, user_id = request.user)
    if request.method == 'POST':
        todo_id.date_complete = timezone.now()
        todo_id.save()
        return redirect('currenttodos')

# удалить задачу
@login_required
def deletetodo(request, todo_pk):
    todo_id = get_object_or_404(Todos, pk = todo_pk, user_id = request.user)
    if request.method == 'POST':
        todo_id.delete()
        return redirect('currenttodos')
