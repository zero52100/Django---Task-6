from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import BankAccount

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Increment successful login counter in cookies
            success_logins = request.session.get('success_logins', 0)
            request.session['success_logins'] = success_logins + 1
            return redirect('bank_details')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def bank_details(request):
    try:
        bank_account = BankAccount.objects.get(user=request.user)
    except BankAccount.DoesNotExist:
        # If BankAccount doesn't exist for the user, create a new one
        bank_account = BankAccount.objects.create(user=request.user, account_number='', ifsc_code='', balance=0.0)
    return render(request, 'bank_details.html', {'bank_account': bank_account})
