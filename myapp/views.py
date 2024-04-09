from django.shortcuts import render,redirect
from . models import *
import random
import requests
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import stripe
from django.conf import settings

stripe.api_key=settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN='http://localhost:8000'

@csrf_exempt
def create_checkout_session(request):
    amount=int(json.load(request)['post_data'])
    final_amount=amount*100

    session=stripe.checkout.Session.create(
        paymant_method_types=['card'],
        line_items=[{
            'price_data':{
                'currency':'inr',
                'product_data':{
                    'name':'Checkout Session Data',
                },
                'unit_amount':final_amount,
            },
            'quantity':1,
        }],
        mode='payment',
        success_url=YOUR_DOMAIN + '/success.html',
        cancel_url=YOUR_DOMAIN + '/cancel.html',)
    
def success(request):
    user=User.objects.get(email=request.session['email'])
    bookevent=BookEvent.objects.filter(user=user)
    for i in bookevent:
        i.payment_status=True
        i.save()
    return render(request,'success.html')

def cancel(request):
    return render(request,'cancel.html')


def home(request):
    return render(request,'home.html')

def index(request):
    user=User.objects.get(email=request.session['email'])
    if user.usertype=="user":
        return render(request,'index.html')
    else:
        return render(request,'mindex.html')

def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg="Email Already Registered"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                    usertype=request.POST['usertype'],
                    firstname=request.POST['firstname'],
                    lastname=request.POST['lastname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    password=request.POST['password'],
                    profile=request.FILES['profile'],
                    
                    )
                msg="Sign up succesfully.."
                return render(request,'login.html',{'msg':msg})
            else:
                msg="Password and confirm Password does not same"
                return render(request,'signup.html',{'msg':msg})
            
    else:
        return render(request,'signup.html')

def login(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                if user.usertype=="user":
                    request.session['email']=user.email
                    request.session['firstname']=user.firstname
                    request.session['profile']=user.profile.url
                    return render(request,'index.html')
                else:
                    request.session['email']=user.email
                    request.session['firstname']=user.firstname
                    request.session['profile']=user.profile.url
                    return render(request,'mindex.html')
            else:
                msg="Invalid Password"
                return render(request,'login.html',{'msg':msg})
        except Exception as e:
            print("Exception : ",e)
            msg="Email not registered"
            return render(request,'login.html',{'msg':msg})
    
    else:
        return render(request,'login.html')
    
def logout(request):
    del request.session['email']
    del request.session['firstname']
    del request.session['profile']
    return render(request,'login.html')

def changepass(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        if user.password==request.POST['opassword']:
            if request.POST['npassword']==request.POST['cpassword']:
                user.password=request.POST['npassword']
                user.save()
                return redirect('logout')
            else:
                msg="new password and confirm password not same"
                if user.usertype=="user":
                    return render(request,'changepass.html',{'msg':msg})
                else:
                    return render(request,'mchangepass.html',{'msg':msg})
        else:
            msg="old password wrong"
            if user.usertype=="user":
               return render(request,'changepass.html',{'msg':msg})
            else:
                return render(request,'mchangepass.html',{'msg':msg})
    else:
        if user.usertype=="user":
           return render(request,'changepass.html')
        else:
            return render(request,'mchangepass.html')
    
def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.firstname=request.POST['firstname']
        user.lastname=request.POST['lastname']
        user.mobile=request.POST['mobile']
        try:
            user.profile=request.FILES['profile']
        except:
            pass
        user.save()
        msg="update successfully"
        if user.usertype=="user":
            return render(request,'profile.html',{'user':user,'msg':msg})
        else:
            return render(request,'mprofile.html',{'user':user,'msg':msg})

    else:
        if user.usertype=="user":
            return render(request,'profile.html',{'user':user})
        else:
            return render(request,'mprofile.html',{'user':user})
    
def forgotpass(request):
    if request.method=="POST":
        try:
            user=User.objects.get(mobile=request.POST['mobile'])
            url = "https://www.fast2sms.com/dev/bulkV2"
            mobile=str(user.mobile)
            otp=random.randint(1000,9999)
            querystring = {"authorization":"s26ti9zkLybH75TEJw8UWRMaog3hnBcNuflDjASVXC1dKQGOqYMqcZeDuLhz5NkCV3xEs0yoYrQAfj1F","variables_values":str(otp),"route":"otp","numbers":mobile}

            headers = {
                'cache-control': "no-cache"
                }

            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
            return render(request,'otp.html',{'otp':otp,'mobile':mobile})

        except:
            msg="Your mobile not registered"
            return render(request,'forgotpass.html',{'msg':msg})

    return render(request,'forgotpass.html')

def otp(request):
    mobile=request.POST['mobile']
    otp=int(request.POST['otp'])
    uotp=int(request.POST['uotp'])
    
    if otp==uotp:
        return render(request,'newpass.html',{'mobile':mobile})
    else:
        msg="Invalid OTP"
        return render(request,'otp.html',{'otp':otp,'mobile':mobile,'msg':msg})
    
def newpass(request):
    mobile=request.POST['mobile']
    np=request.POST['np']
    cp=request.POST['cp']
    
    if np==cp:
        user=User.objects.get(mobile=mobile)
        user.password=np
        user.save()
        msg="Password update successfully"
        return render(request,'login.html',{'msg':msg})
    else:
        msg="New password and confirm password not match"
        return render(request,'newpass.html',{'mobile':mobile,'msg':msg})
    
def addevent(request):
    
    if request.method=="POST":
        user=User.objects.get(email=request.session['email'])    
        Event.objects.create(
            manager=user,
            event_name=request.POST['eventname'],
            event_date=request.POST['eventdate'],
            event_time=request.POST['eventtime'],
            event_venue=request.POST['eventvenue'],
            event_price=request.POST['eventprice'],
            event_desc=request.POST['eventdesc'],
            event_image=request.FILES['eventimage'],
        )
        msg="Event add successfully.."
        return render(request,'addevent.html',{'msg':msg})
    else:
        return render(request,'addevent.html')
    
def viewevent(request):
    manager=User.objects.get(email=request.session['email'])
    events=Event.objects.filter(manager=manager)
    return render(request,'viewevent.html',{'events':events})

def editevent(request,pk):
    event=Event.objects.get(pk=pk)
    if request.method=='POST':
        event.event_name=request.POST['eventname']
        event.event_date=request.POST['eventdate']
        event.event_time=request.POST['eventtime']
        event.event_venue=request.POST['eventvenue']
        event.event_price=request.POST['eventprice']
        event.event_desc=request.POST['eventdesc']
        try:
            event.event_image=request.FILES['eventimage']
        except:
            pass
        event.save()
        msg="Edit update successfully"
        return render(request,'editevent.html',{'event':event,'msg':msg})
    else:
        return render(request,'editevent.html',{'event':event})
    
def deleteevent(request,pk):
    event=Event.objects.get(pk=pk)
    event.delete()
    return redirect('viewevent')

def shows_events(request):
    events=Event.objects.all()
    return render(request,'shows-events.html',{'events':events})

def event_details(request,pk):
    event=Event.objects.get(pk=pk)
    return render(request,'event-details.html',{'event':event})

def bookevent(request,pk):
    user=User.objects.get(email=request.session['email'])
    event=Event.objects.get(pk=pk)
    BookEvent.objects.create(user=user,event=event)
    events=BookEvent.objects.filter(user=user)
    msg="your Event booked"
    return render(request,'myevent.html',{'events':events,'msg':msg})
    
def myevent(request):
    user=User.objects.get(email=request.session['email'])
    events=BookEvent.objects.filter(user=user)
    return render(request,'myevent.html',{'events':events})

def checkout(request,pk):
    bookevent=BookEvent.objects.get(pk=pk)
    net_price=bookevent.event.event_price
    print(net_price)
    print(bookevent)
    return render(request,'checkout.html',{'bookevent':bookevent,'net_price':net_price})
    