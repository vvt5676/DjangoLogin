from django.urls import path, include
from django.contrib.auth import views as auth_views
from authentication import views as my_auth_views

app_name = 'authentication'

urlpatterns = [
    path('signup/', my_auth_views.signup, name='signup'),
    path('account_activation_sent/', my_auth_views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', my_auth_views.activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),
]
