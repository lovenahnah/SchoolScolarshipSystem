from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("student/apply/", views.apply_scholarship, name="apply"),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/review/<int:app_id>/", views.review_application, name="review"),
    path("register/", views.register, name="register"),
    path("", views.home, name="home"),

]
