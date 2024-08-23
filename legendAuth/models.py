from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    kyc_status = models.CharField(max_length=10, default='Pending')
    attached_cards = models.JSONField(default=list)
    btc_private_key = models.CharField(max_length=64, blank=True, null=True)
