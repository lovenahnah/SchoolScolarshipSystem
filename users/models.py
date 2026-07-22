from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    # Student-specific fields
    course = models.CharField(max_length=100, blank=True, null=True)
    gpa = models.FloatField(blank=True, null=True)

    # Admin-specific fields
    permissions = models.CharField(max_length=100, blank=True, null=True)


class ScholarshipType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class ScholarshipApplication(models.Model):
    SCHOLARSHIP_CHOICES = [
        ("academic", "Academic/Merit"),
        ("need", "Need-Based"),
        ("government", "Government-Funded"),
        ("private", "Private/Corporate"),
        ("athletic", "Athletic/Skill-Based"),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    scholarship_type = models.CharField(max_length=20, choices=SCHOLARSHIP_CHOICES)
    file_upload = models.FileField(upload_to="applications/", blank=True, null=True)
    status = models.CharField(max_length=50, default="Pending")
    date_submitted = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.get_scholarship_type_display()}"


class Document(models.Model):
    application = models.ForeignKey(ScholarshipApplication, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    message = models.TextField()
    status = models.CharField(max_length=20, default="Unread")
    created_at = models.DateTimeField(auto_now_add=True)


class AuditLog(models.Model):
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'admin'}
    )
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
