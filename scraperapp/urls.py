from django.urls import include, path
from .views import FollowerList

urlpatterns = [
    path('followers/', FollowerList.as_view(), name='follower-list'),
]