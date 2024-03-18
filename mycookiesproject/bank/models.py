from django.db import models
from django.contrib.auth.models import User

class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s Bank Account"
