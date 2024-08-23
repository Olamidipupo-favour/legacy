from django.urls import path
from .views import CustomUserRegistrationView, CustomTokenObtainPairView

urlpatterns = [
    path('api/register/', CustomUserRegistrationView.as_view(), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

]
