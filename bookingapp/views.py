from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import TravelOption, Booking
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction

def home(request):
    return render(request, 'bookingapp/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'bookingapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'bookingapp/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST['email']
        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')
    return render(request, 'bookingapp/profile.html')

def travel_options(request):
    travel_type = request.GET.get('type')
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    date = request.GET.get('date')

    options = TravelOption.objects.all()

    if travel_type:
        options = options.filter(type=travel_type)
    if source:
        options = options.filter(source__icontains=source)
    if destination:
        options = options.filter(destination__icontains=destination)
    if date:
        options = options.filter(datetime__date=date)
        
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    if price_min:
        options = options.filter(price__gte=price_min)
    if price_max:
        options = options.filter(price__lte=price_max)


    return render(request, 'bookingapp/travel_options.html', {'options': options})

@login_required
def book_travel(request, travel_id):
    travel = get_object_or_404(TravelOption, id=travel_id)

    if request.method == 'POST':
        seats = int(request.POST['seats'])
        if seats <= 0:
            messages.error(request, 'Number of seats must be greater than 0.')
            return redirect('travel_options')

        if travel.available_seats >= seats:
            total_price = travel.price * seats

            with transaction.atomic():
                booking = Booking.objects.create(
                    user=request.user,
                    travel_option=travel,
                    number_of_seats=seats,
                    total_price=total_price,
                    booking_date=timezone.now(),
                    status='Confirmed'
                )
                travel.available_seats -= seats
                travel.save()

            messages.success(request, 'Booking confirmed successfully!')
            return redirect('my_bookings')
        else:
            messages.error(request, 'Not enough seats available.')
            
        MAX_SEATS = 10
        if seats > MAX_SEATS:
            messages.error(request, f'Cannot book more than {MAX_SEATS} seats at a time.')
            return redirect('travel_options')


    return render(request, 'bookingapp/book_travel.html', {'travel': travel})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'bookingapp/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status == 'Confirmed':
        booking.status = 'Cancelled'
        booking.save()

        travel = booking.travel_option
        travel.available_seats += booking.number_of_seats
        travel.save()

        messages.success(request, 'Booking cancelled successfully.')

    return redirect('my_bookings')




