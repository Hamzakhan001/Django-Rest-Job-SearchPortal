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
    