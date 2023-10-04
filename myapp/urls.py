from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.index,name='index'),
    path('detail/<int:id>/',views.detail,name='detail'),
    path('success/',views.payment_view_success,name='payment_success'),
    path('failed/',views.payment_failed_view,name='payment_failed'),
    
]

urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
