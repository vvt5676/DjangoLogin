from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from authentication.forms import SignUpForm
from authentication.tokens import account_activation_token
from .models import User


def account_activation_sent(request):
    return render(request, template_name='authentication/account_activation_sent.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Setting as False to prevent login without confirming email
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Verify your DjangoLogin Account'
            message = render_to_string('authentication/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            print("Mail Done!")
            return redirect(to='authentication:account_activation_sent')
        else:
            return render(request, template_name='authentication/signup.html', context={
                'form': form
            })
    else:
        form = SignUpForm()
        return render(request, template_name='authentication/signup.html', context={'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('main:home')
    else:
        return render(request, 'authentication/account_activation_invalid.html')
