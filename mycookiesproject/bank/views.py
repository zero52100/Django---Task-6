from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import BankAccount

def home(request):
    if request.user.is_authenticated:
        return redirect('bank_details')  
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            success_logins = request.session.get('success_logins', 0)
            request.session['success_logins'] = success_logins + 1
            return redirect('bank_details')
        else:
            # Increment failed login attempts counter in session
            failed_logins = request.session.get('failed_logins', 0)
            request.session['failed_logins'] = failed_logins + 1
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
        print("Bank Account found:", bank_account)  
    except BankAccount.DoesNotExist:
        print("Bank Account does not exist for user:", request.user) 
        bank_account = BankAccount.objects.create(
            user=request.user,
            account_number='4556565656',
            ifsc_code='SBI4545454',
            balance=4500.00
        )
    return render(request, 'bank_details.html', {'bank_account': bank_account})
