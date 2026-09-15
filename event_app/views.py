from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Student, Event, Registration


def show_message(request, title, message, status="success",
                  primary_url=None, primary_label="Continue",
                  secondary_url=None, secondary_label=None):
    """Renders a styled notice-card message instead of a plain text response."""
    return render(
        request,
        'message.html',
        {
            'title': title,
            'message': message,
            'status': status,
            'primary_url': primary_url,
            'primary_label': primary_label,
            'secondary_url': secondary_url,
            'secondary_label': secondary_label,
        }
    )


def home(request):
    return render(request, 'index.html')


def register(request):

    if request.method == "POST":

        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if Student.objects.filter(email=email).exists():
            return show_message(
                request,
                title="Email already registered",
                message="An account with this email already exists. Please login instead.",
                status="error",
                primary_url=reverse('login'),
                primary_label="Go to login",
                secondary_url=reverse('register'),
                secondary_label="Try another email",
            )

        Student.objects.create(
            name=name,
            email=email,
            password=password
        )

        return show_message(
            request,
            title="Registration successful",
            message="Your account has been created. You can log in now.",
            status="success",
            primary_url=reverse('login'),
            primary_label="Go to login",
        )

    return render(request, 'register.html')


def login(request):

    if request.method == "POST":

        email = request.POST['email']
        password = request.POST['password']

        student = Student.objects.filter(
            email=email,
            password=password
        ).first()

        if student:

            request.session['student_id'] = student.id

            return redirect('dashboard')

        else:
            return show_message(
                request,
                title="Login failed",
                message="That email or password doesn't match our records.",
                status="error",
                primary_url=reverse('login'),
                primary_label="Try again",
                secondary_url=reverse('register'),
                secondary_label="Create an account",
            )

    return render(
        request,
        'login.html'
    )


def dashboard(request):

    total_events = Event.objects.count()

    total_registrations = Registration.objects.count()

    return render(
        request,
        'dashboard.html',
        {
            'total_events': total_events,
            'total_registrations': total_registrations
        }
    )


def events(request):

    search = request.GET.get('search')

    if search:
        events = Event.objects.filter(
            event_name__icontains=search
        )
    else:
        events = Event.objects.all()

    return render(
        request,
        'events.html',
        {'events': events}
    )


def join_event(request, event_id):

    student_id = request.session.get('student_id')

    if not student_id:
        return show_message(
            request,
            title="Please login first",
            message="You need to be logged in to register for an event.",
            status="error",
            primary_url=reverse('login'),
            primary_label="Go to login",
        )

    student = Student.objects.get(id=student_id)
    event = Event.objects.get(id=event_id)

    already_registered = Registration.objects.filter(
        student=student,
        event=event
    ).exists()

    if already_registered:
        return show_message(
            request,
            title="Already registered",
            message="You've already registered for \"%s\"." % event.event_name,
            status="error",
            primary_url=reverse('my_events'),
            primary_label="View my events",
            secondary_url=reverse('events'),
            secondary_label="Back to events",
        )

    Registration.objects.create(
        student=student,
        event=event
    )

    return show_message(
        request,
        title="You're registered!",
        message="You've successfully registered for \"%s\"." % event.event_name,
        status="success",
        primary_url=reverse('my_events'),
        primary_label="View my events",
        secondary_url=reverse('events'),
        secondary_label="Back to events",
    )


def logout(request):

    request.session.flush()

    return show_message(
        request,
        title="Logged out",
        message="You've been logged out successfully.",
        status="success",
        primary_url=reverse('home'),
        primary_label="Back to home",
    )


def my_events(request):

    student_id = request.session.get('student_id')

    if not student_id:
        return show_message(
            request,
            title="Please login first",
            message="You need to be logged in to see your registered events.",
            status="error",
            primary_url=reverse('login'),
            primary_label="Go to login",
        )

    registrations = Registration.objects.filter(
        student_id=student_id
    )

    return render(
        request,
        'my_events.html',
        {
            'registrations': registrations
        }
    )
