from django.shortcuts import render, redirect
from .models import Record
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm

# Create your views here.

def home(request):
    records = Record.objects.all().order_by('id')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'You have been logged in')
            return redirect('home')
        else:
            messages.success(request, 'There was an error logging in, please try again...')
            return redirect('home')
    else:
        return render(request,'home.html',{'records':records})


def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home') 

def register_user(request):
    form = SignUpForm(request.POST)
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})

    return render(request ,'register.html', {'form':form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_id = Record.objects.get(id=pk)
        return render(request, 'record.html',{'customer_record':customer_id})
    else:
        messages.success(request,'You mush have logged in to view this page')
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Record saved successfully...')
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, 'You must have login')
        return redirect('home')
    

def update_record(request,pk):
    if request.user.is_authenticated:
        customer_id = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=customer_id)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record has been updated')
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, 'You must have login')
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        customer_id = Record.objects.get(id=pk)
        customer_id.delete()
        messages.success(request, "Record deleted successfully...")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to do that...")
        return redirect('home')