from django.urls import path

from notes import views

app_name = 'notes'
urlpatterns = [
    path('', views.NotesList.as_view(), name='list'),
    path('<int:pk>/detail/', views.NoteDetailsView.as_view(), name='detail'),
]