from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    full_name = models.CharField(max_length=50, null=False)
    phone = models.PositiveIntegerField(null=False)
    email_address = models.EmailField(max_length=50, null=True, blank=True)
    is_spam = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

class UserContactMap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}, {self.contact.full_name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.PositiveIntegerField(null=False, unique=True)
    email_address = models.EmailField(max_length=50, null=True, blank=True)
    is_spam = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    