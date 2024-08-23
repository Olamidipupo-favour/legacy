from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomUserRegistrationSerializer
from .serializers import CustomTokenObtainPairSerializer
class CustomUserRegistrationView(generics.CreateAPIView):
    serializer_class = CustomUserRegistrationSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
