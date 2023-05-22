from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from autoslug import AutoSlugField
from django_countries.fields import CountryField
from recruiters.models import Job
from django.utils import timezone



CHOICES=(
	('Full Time','Full Time'),
	('Part Time','Part Time'),
	('Internship','Internship'),
	('Remote','Remote'),
)


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True, related_name='profile')
    full_name=models.CharField(max_length=200, null=True, blank=True)
    country=CountryField(null=True,blank=True)
    location=models.CharField(max_length=255, null=True, blank=True)
    resume=models.FileField(upload_to="resumes",null=True,blank=True)
    grad_year = models.IntegerField(blank=True)
    looking_for=models.CharField(max_length=30, choices=CHOICES, default='Full Time',null=True)
    slug=AutoSlugField(populate_from='user',unique=True)
    