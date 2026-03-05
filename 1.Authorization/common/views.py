from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView


# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'
    permission_required = ['auth.view_user']


# Assuming a Note model exists with at least 'title' and 'content' fields
# from .models import Note
class NoteDetailsView(DetailView):
    # model = Note # Uncomment and set your Note model here
    template_name = 'common/note_details.html'
    context_object_name = 'note' # The name of the context variable to use in the template