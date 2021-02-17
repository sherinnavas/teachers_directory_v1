from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse
import os.path
from os import path

# Create your models here.

class Subjects(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def search_for_sub(self, name):
        """Checking if the subject is present.
        """
        try:
            subject = Subjects.objects.get(name__iexact=name)
            return subject.id
        except Subjects.DoesNotExist:
            subject = Subjects.objects.create(name=name)
            return subject.id


class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_pic = models.ImageField(upload_to='uploads/',null=True)
    email = models.EmailField()
    phone_number = models.CharField( max_length=10, blank=True)
    room_number = models.CharField(max_length=5)
    subjects = models.ManyToManyField(Subjects, blank=True, null=True, default='')

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('teacher_details', args=[str(self.id)])

    @property
    def img_url(self):
        """Checking if the image is present in the directory.
        If not setting the default Image path
        """
        if self.profile_pic and os.path.isfile(self.profile_pic.name):
            return self.profile_pic.url
        else:
            return "/static/img/no-image.png"

    def check_email_exists(self, email):
        """Checking if the email already Exists.
        If yes,return None
        """
        try:
            teacher = Teacher.objects.get(email=email)
            return teacher
        except Teacher.DoesNotExist:
            return None
