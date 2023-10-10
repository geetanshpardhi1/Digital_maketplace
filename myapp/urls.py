from django.contrib import admin
from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.index,name='index'),
    path('detail/<int:id>/',views.detail,name='detail'),
    path('success/',views.payment_success_view,name='success'),
    path('failed/',views.payment_failed_view,name='failed'),
    path('api/checkout-session/<int:id>/',views.create_checkout_session,name='api_checkout_session'),
    path('createproduct/',views.create_product,name='create_product'),
    path('editproduct/<int:id>/',views.product_edit,name='editproduct'),
    path('delete/<int:id>/',views.product_delete,name='deleteproduct'),
    path('dashboard',views.dashboard,name='dashboard')
    
]

urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
