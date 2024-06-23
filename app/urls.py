# tasks/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('register/', Register.as_view(), name="register"),
    path('users/', UserList.as_view()),
    path('user/<int:pk>/', UserUpdateView.as_view(), name='user-detail'),
    # path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    # path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]