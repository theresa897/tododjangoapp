from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import *
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import * 
from .serializers import *
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterSerializer

    def get_object(self):
        return self.request.user

class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.deleted = True
        user.save()
        return Response(status=204)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
        
class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class=RegisterSerializer

    def get_queryset(self):                                            # added string
        return super().get_queryset().filter(id=self.request.user.id)

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes= (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)