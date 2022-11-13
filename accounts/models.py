from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
GENDER_SELECTION = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Order','Order')
)
# Create your models here.

class MyUser(AbstractUser):
    mobile_number = models.CharField(max_length=10, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=20,null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_SELECTION)

    