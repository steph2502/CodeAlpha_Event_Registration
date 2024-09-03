from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Registration
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm,SignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})

@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if not Registration.objects.filter(user=request.user, event=event).exists():
        Registration.objects.create(user=request.user, event=event)
        messages.success(request, 'You have successfully registered for the event!')
    else:
        messages.info(request, 'You are already registered for this event.')
    return redirect('event_list')

@login_required
def manage_registration(request):
    registrations = Registration.objects.filter(user=request.user)
    return render(request, 'manage_registration.html', {'registrations': registrations})



def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in successfully.")
            return redirect('event_list')  # Redirect to event list or other relevant page
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('event_list') 

def signup_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Congratulations! You have successfully created your account.")
                return redirect('event_list')  
            else:
                messages.error(request, "Authentication failed. Please try again.")
        else:
            messages.error(request, "There was a problem registering. Please try again.")
            return redirect('signup')
    else:
        return render(request, 'signup.html', {'form': form})