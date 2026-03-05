from django.contrib.auth.views import LoginView
from django.urls import path

from common.views import HomeView, NoteDetailsView

urlpatterns =[
    path('',HomeView.as_view(),name='home'),
    path('notes/<int:pk>/', NoteDetailsView.as_view(), name='note_detail'),

]