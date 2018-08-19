from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    # TODO: Add Required Fields here
