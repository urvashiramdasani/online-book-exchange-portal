from . import views
from django.urls import path

urlpatterns = [path('', views.home, name="book_portal-home"),
				path('about/', views.about, name="book_portal-about"),
]