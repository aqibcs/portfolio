import os
from dotenv import load_dotenv

from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Skill, Experience, Education
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError

# Load environment variables from .env
load_dotenv()

def home(request):
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    educations = Education.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home')
    else:
        form = ContactForm()
    
    context = {
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
        'form': form,
    }
    return render(request, 'core/home.html', context)


def about(request):
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    educations = Education.objects.all()
    
    context = {
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
    }
    return render(request, 'core/about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_entry = form.save()

            # Email configuration from environment variables
            from_email = os.getenv("EMAIL_HOST_USER")
            recipient_email = os.getenv("EMAIL_HOST_USER")

            try:
                send_mail(
                    subject=f"New Contact Form Submission: {contact_entry.subject}",
                    message=f"Name: {contact_entry.name}\nEmail: {contact_entry.email}\n\nMessage:\n{contact_entry.message}",
                    from_email=from_email,
                    recipient_list=[recipient_email],
                    fail_silently=False,
                )

                send_mail(
                    subject="We Received Your Message!",
                    message=f"Hello {contact_entry.name},\n\n"
                            "Thank you for reaching out! We have received your message and will get back to you soon.\n\n"
                            "Best regards,\nAqib Shah",
                    from_email=from_email,
                    recipient_list=[contact_entry.email],
                    fail_silently=False,
                )

            except BadHeaderError:
                messages.error(request, "Invalid email header detected.")
                return redirect('contact')

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')

    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})
