from django.shortcuts import render ,redirect ,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login
from .models import Amenities , Hotel ,HotelBooking

from django.contrib.auth.decorators import login_required
# Create your views here.





@login_required(login_url='/login_page/')
def check_booking(start_date  , end_date ,uid , room_count):
    qs = HotelBooking.objects.filter(
        start_date__lte=start_date,
        end_date__gte=end_date,
        hotel__uid = uid
        )
    
    if len(qs) >= room_count:
        return False
    
    return True


@login_required(login_url='/login_page/')
def home(request):

    amenities_objs= Amenities.objects.all()
    hotels_objs =  Hotel.objects.all()
    sort_by = request.GET.get('sort_by')
    amenities = request.GET.getlist('amenities')
    if sort_by:
        
        if sort_by == 'ASC':
            hotels_objs = hotels_objs.order_by('hotel_price')
        elif sort_by == 'DSC':
            hotels_objs = hotels_objs.order_by('-hotel_price')

    search = request.GET.get('search')

    if search:
        hotels_objs = hotels_objs.filter(hotel_name__icontains = search)

    if len(amenities):
        hotels_objs = hotels_objs.filter(amenities__amenity_name__in = amenities).distinct
    

    context = {'amenities_objs' : amenities_objs , 'hotels_objs' : hotels_objs , 'sort_by':sort_by  , 'amenities' : amenities}

    return render(request , 'home.html' , context)


def login_page(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        user_obj = User.objects.filter(username = username)

        if not user_obj.exists():
            messages.warning(request,'Account not found')
            return redirect('/login_page/')


        user_obj = authenticate(username = username , password = password)
        if  user_obj is None:
            messages.warning(request , "Wrong password")
            return redirect('/login_page/')
        else:
            login(request , user_obj)
            return redirect('/')

        
        
        


    return render(request , 'login_page.html')

@login_required(login_url='/login_page/')
def hotel_detail(request,uid):
    hotel_obj = Hotel.objects.get(uid = uid)

    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout= request.POST.get('checkout')
        hotel = Hotel.objects.get(uid = uid)
        if not check_booking(checkin ,checkout  , uid , hotel.room_count):
            messages.warning(request, 'Hotel is already booked in these dates ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        HotelBooking.objects.create(hotel=hotel , user = request.user , start_date=checkin
        , end_date = checkout , booking_type  = 'Pre Paid')
        
        messages.success(request, 'Your booking has been saved')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

        
    
    return render(request , 'hotel_detail.html' ,{
        'hotels_obj' :hotel_obj
    })


def register(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        user_obj = User.objects.filter(username = username)

        if user_obj.exists():
            messages.warning(request,'Username Already Exists.')
            return redirect('/register/')


        user_obj = User.objects.create(username = username)
        user_obj.set_password(password)
        user_obj.save()
        return redirect('/register/')

    return render(request , 'register.html')