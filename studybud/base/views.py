from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


# rooms = [
#         {'id':1,'name':'Python Room'},
#         {'id':2,'name':'Django Room'},
#         {'id':3,'name':'C# Room'},
#     ]
# Create your views here.
def home(request):
    # return HttpResponse("Home")
    rooms = Room.objects.all()
    context  = {'rooms':rooms}
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