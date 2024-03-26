from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import orderForm
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.template.loader import render_to_string
 
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func 

def allowed_user(roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists(): 
                group = request.user.groups.all()[0].name  
                if group in roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse('You are not allowed to access this page')
            else:
                return HttpResponse('You are not allowed to access this page') 
        return wrapper_func
    return decorator

def admin_only(view_funct):
    def wrapper_func(request,*args,**kwargs):
         group = None
         if request.user.groups.exists(): 
             group = request.user.groups.all()[0].name  
         if group == 'customer':
          return redirect('userz')  
         
         if group == 'admin':
             return view_funct(request,*args,**kwargs)
    return wrapper_func    
               
@login_required(login_url='l')
@admin_only
# @allowed_user(roles=['admin'])
def home(request):
    a=order.objects.all()
    b=customer.objects.all() 
    total=a.count()
    pending=a.filter(status="Pending").count()
    delivered=a.filter(status="Delivered").count()
    return render(request,"accounts/dashboard.html",context={"l1" :a, "l2":b,"o":total, "p":pending, "d":delivered })

@login_required(login_url='l')
@allowed_user(roles=['admin'])
def products(request):
    k=product.objects.all()
    return render(request,"accounts/product.html", context= { "list" :k })

@login_required(login_url='l')
@allowed_user(roles=['admin'])
def customers(request,pk):
    c =customer.objects.get(id=pk)
   # co= customer.order_set.all()
    co=order.objects.filter(customer__id= pk)
   # p=customer.objects.get
    return render(request,"accounts/customer.html",context={"email" : c, "o": co })  

@login_required(login_url='l')
@allowed_user(roles=['admin'])
def createorder(request):
    form = orderForm()  # Initialize an empty form
    # context = {"f": form}  # Optional, you can include this if needed

    if request.method == "POST":
        form = orderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {"f": form}
    return render(request, "accounts/order_form.html", context)

@login_required(login_url='l')
@allowed_user(roles=['admin'])
def updateorder(request,pk ):
    a = order.objects.get(id=pk)
    customer_instance = a.customer 
    user_name = customer_instance.user.username
    user_email = customer_instance.user.email
    # print(user_name)
    # print(user_email)
    form=orderForm(instance=a)
    if request.method == "POST": 
        form = orderForm(request.POST,instance=a)
        if form.is_valid():
            form.save()
            subject = 'Welcome to our  website!'
            message = render_to_string('accounts/update.html', {'username': user_name })
            from_email = 'noreply.reachus@gmail.com'
            to_email = [customer_instance.user.email]
            print(to_email)
            send_mail(subject, '', from_email, to_email, html_message=message)
            return redirect("/")
    context = {"f": form}
    return render(request,"accounts/order_form.html", context)

@login_required(login_url='l')
@allowed_user(roles=['admin']) 
def deleteorder(request,pk):
    a=order.objects.get(id=pk)
    # context={}
    if request.method == "POST": 
        a.delete()
        return redirect("/") 
    return render(request,"accounts/delete.html")

@unauthenticated_user
def register(request, flag=None):
    if request.method == "GET":
        return render(request, "accounts/index.html", context={"flag":flag})
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if name is "" or email is ""  or password is "" or cpassword is "":
             return redirect('r', flag=0)

        if password != cpassword:
            messages.error(request, "Password did not match")
            return redirect('r', flag=0)
        else:  
            if User.objects.filter(username=name).exists():
                messages.error(request, "User with the given username or email already exists")
            else:
                user = User.objects.create_user(
                    username=name,
                    email=email,
                    password=password
                )
                subject = 'Welcome to our  website!'
                message = render_to_string('accounts/welcome.html', {'username': name})
                from_email = 'noreply.reachus@gmail.com'
                to_email = [user.email]
                send_mail(subject, '', from_email, to_email, html_message=message)
        
                customer_group= Group.objects.get(name='customer')
                user.groups.add(customer_group)  
                customer.objects.create(user=user,name=user.username,email=email)    
                messages.success(request, "Account created successfully for" +  name)
                return redirect('r', flag=1)
    return render(request, "accounts/index.html", context={"flag":flag})

@unauthenticated_user
def logins(request):    
     if request.method == "POST":
         username=request.POST.get('username')
         password=request.POST.get('password')
         user = authenticate(username=username, password=password)
         if user is not None:
                login(request,user)
                return redirect('home')
         else:    
            messages.error(request,"User did not exist please check your credentials")
            return redirect('r')
         
     return render(request, "accounts/index.html")


def logoutuser(request):
    logout(request)
    return redirect('l')

@login_required(login_url='l')
@allowed_user(roles=['customer'])
def users(request):
    orders=request.user.customer.order_set.all()    
    total=orders.count()
    pending=orders.filter(status="Pending").count()
    delivered=orders.filter(status="Delivered").count()
    context={'orders':orders,"o":total, "p":pending, "d":delivered }
    return render(request,'accounts/user.html',context)