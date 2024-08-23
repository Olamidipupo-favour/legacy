from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserProfile

class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    # Custom fields can be added as needed
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    kyc_status = serializers.CharField(max_length=10, default='Pending')
    attached_cards = serializers.JSONField(default=list)
    btc_private_key = serializers.CharField(max_length=64, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'balance', 'kyc_status', 'attached_cards', 'btc_private_key']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extract profile related data
        balance = validated_data.pop('balance')
        kyc_status = validated_data.pop('kyc_status')
        attached_cards = validated_data.pop('attached_cards')
        btc_private_key = validated_data.pop('btc_private_key', '')

        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Create associated user profile
        UserProfile.objects.create(
            user=user,
            balance=balance,
            kyc_status=kyc_status,
            attached_cards=attached_cards,
            btc_private_key=btc_private_key
        )

        return user

    def to_representation(self, instance):
        """
        Customize the response to include JWT tokens and user information
        """
        refresh = RefreshToken.for_user(instance)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': instance.id,
            'balance': instance.profile.balance,
            'last_login': instance.last_login,
            'created_at': instance.date_joined,
            'kyc_status': instance.profile.kyc_status,
            'attached_cards': instance.profile.attached_cards,
            'btc_private_key': instance.profile.btc_private_key,
        }
        return data

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom fields to the response
        data.update({
            'user_id': self.user.id,
            'balance': self.user.profile.balance,  # Assuming balance is stored in a related Profile model
            'last_login': self.user.last_login,
            'created_at': self.user.date_joined,
            'kyc_status': self.user.profile.kyc_status,  # Assuming KYC status is in Profile model
            'attached_cards': self.user.profile.attached_cards,  # Assuming attached cards is in Profile model
            'btc_private_key': self.user.profile.btc_private_key,  # Assuming BTC key is in Profile model
        })

        return data
