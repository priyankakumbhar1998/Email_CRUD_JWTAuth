from django.urls import path
from .views import LibraryAPI, LibraryDetailsAPI

urlpatterns = [
    path('library/', LibraryAPI.as_view()),
    path('library/<int:pk>/', LibraryDetailsAPI.as_view()),
]