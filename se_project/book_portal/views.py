from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)

# Create your views here.
def about(request):
    return render(request,'book_portal/about.html',{'title':'About'})

def home(request):
	return render(request, 'book_portal/home.html', {'title':'Home'})