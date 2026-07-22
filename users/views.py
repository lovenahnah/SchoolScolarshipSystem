from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ScholarshipApplication, ScholarshipType

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role == "student":
                return redirect("student_dashboard")
            elif user.role == "admin":
                return redirect("admin_dashboard")
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return redirect("login")

    applications = ScholarshipApplication.objects.filter(student=request.user)
    return render(request, "student_dashboard.html", {"applications": applications})

@login_required
def apply_scholarship(request):
    if request.user.role != "student":
        return redirect("login")

    if request.method == "POST":
        scholarship_type = request.POST["scholarship_type"]
        remarks = request.POST.get("remarks", "")
        file_upload = request.FILES.get("file_upload")

        ScholarshipApplication.objects.create(
            student=request.user,
            scholarship_type=scholarship_type,
            remarks=remarks,
            file_upload=file_upload
        )
        return redirect("student_dashboard")

    return render(request, "apply.html")

@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        return redirect("login")

    pending_apps = ScholarshipApplication.objects.filter(status="Pending")
    approved_apps = ScholarshipApplication.objects.filter(status="Approved")
    rejected_apps = ScholarshipApplication.objects.filter(status="Rejected")

    return render(request, "admin_dashboard.html", {
        "pending_apps": pending_apps,
        "approved_apps": approved_apps,
        "rejected_apps": rejected_apps,
    })


@login_required
def review_application(request, app_id):
    if request.user.role != "admin":
        return redirect("login")

    application = ScholarshipApplication.objects.get(id=app_id)
    if request.method == "POST":
        application.status = request.POST["status"]
        application.remarks = request.POST["remarks"]
        application.save()
        return redirect("admin_dashboard")

    return render(request, "review.html", {"application": application})

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from .models import User

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        role = request.POST["role"]
        course = request.POST.get("course", "")
        gpa = request.POST.get("gpa", None)

        # Create user
        user = User.objects.create(
            username=username,
            password=make_password(password),  # hash password
            role=role,
            course=course if role == "student" else None,
            gpa=gpa if role == "student" else None,
        )
        login(request, user)  # auto-login after registration
        if role == "student":
            return redirect("student_dashboard")
        else:
            return redirect("admin_dashboard")

    return render(request, "register.html")

def home(request):
    return render(request, "home.html")
