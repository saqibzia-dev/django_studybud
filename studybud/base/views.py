from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# rooms = [
#         {'id':1,'name':'Python Room'},
#         {'id':2,'name':'Django Room'},
#         {'id':3,'name':'C# Room'},
#     ]
# Create your views here.
def home(request):
    # return HttpResponse("Home")
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains = q)

        )
    # rooms = Room.objects.all()
    room_count = rooms.count()
    topics = Topic.objects.all()
    context  = {'rooms':rooms,'topics':topics,'room_count':room_count}
    return render(request,'base/home.html',context)

def room(request,pk):
    # return HttpResponse("Room")
    room = Room.objects.get(id = pk)
    # room = None
    # for item in rooms:
        
    #     if item['id'] == int(pk):
    #         room = item 
    context = {'room':room}        
    return render(request,'base/room.html',context)

@login_required(login_url = 'login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('home')
    context = {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url = 'login')
def update_room(request,pk):
    room_data = Room.objects.get(id = pk)
    form  = RoomForm(instance = room_data)
    if request.user != room_data.host:
        return HttpResponse('You are Not Allowed here!')
    if request.method == 'POST':
        form = RoomForm(request.POST,instance = room_data)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url = 'login' )
def delete_room(request,pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse('You are Not Allowed Here!')
    
    if request.method == "POST":
        room.delete()
        return redirect("home")
    
    context = {'obj':room}
    return render(request,'base/delete_data.html',context)


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request,"Username Doesnot Exists!")
        user = authenticate(request,username = username,password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Username or Password is Incorrect!")
    context = {'page':page}
    print(context)
    
    return render(request,'base/login_register.html',context)

def logout_page(request):
    logout(request)
    return redirect('home')

def register_page(request):
    page = 'register'
    context = {'page':page}
    
    return render(request,'base/login_register.html',context)
