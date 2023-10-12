from django.contrib import admin
from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='index'),
    path('detail/<int:id>/',views.detail,name='detail'),
    path('success/',views.payment_success_view,name='success'),
    path('failed/',views.payment_failed_view,name='failed'),
    path('api/checkout-session/<int:id>/',views.create_checkout_session,name='api_checkout_session'),
    path('createproduct/',views.create_product,name='create_product'),
    path('editproduct/<int:id>/',views.product_edit,name='editproduct'),
    path('delete/<int:id>/',views.product_delete,name='deleteproduct'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('register/',views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='myapp/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='myapp/logout.html'),name='logout'),
    path('invalid/',views.invalid,name='invalid'),
    path('purchases/',views.my_purchases,name='purchases')
]

urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
