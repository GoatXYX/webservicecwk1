from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/stories/', views.api_get_stories, name='api_get_stories'),
    path('api/stories/<int:key>/', views.api_delete_story, name='api_delete_story')
]
