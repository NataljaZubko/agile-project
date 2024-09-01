from rest_framework import serializers
from apps.users.models import User

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'position', 'project']

class RegisterUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 're_password', 'position', 'project']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        # Сначала проверка паролей
        if 'password' in data and data['password'] != data.get('re_password'):
            raise serializers.ValidationError({"password": "Passwords do not match."})

        # Проверка других полей
        if not data.get('username'):
            raise serializers.ValidationError({"username": "This field may not be blank."})

        if not data.get('first_name'):
            raise serializers.ValidationError({"first_name": "This field may not be blank."})

        if not data.get('last_name'):
            raise serializers.ValidationError({"last_name": "This field may not be blank."})

        if not data.get('email') or '@' not in data['email']:
            raise serializers.ValidationError({"email": "Enter a valid email address."})

        return data


    def create(self, validated_data):
        validated_data.pop('re_password')
        user = User.objects.create_user(**validated_data)
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'position', 'project']