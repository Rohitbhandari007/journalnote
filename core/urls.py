from django.urls import path
from django.contrib.auth import views as auth_views

from .views import CreatePost, PostDetails, PostListView, register, searchbar, adsearch

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('create/', CreatePost.as_view(), name='create_post'),
    path('register/', register, name='register'),
    path('<int:pk>/', PostDetails.as_view(), name='detail'),
    path('search/', searchbar, name='search'),
    path('adsearch/', adsearch, name='adsearch'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="core/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="core/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="core/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="core/password_reset_done.html"),
         name="password_reset_complete"),




]
