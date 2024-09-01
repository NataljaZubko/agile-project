from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from apps.users.models import User
from apps.users.serializers.user_serializers import UserListSerializer, RegisterUserSerializer, UserDetailSerializer

class UserListGenericView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

class RegisterUserGenericView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

class UserDetailGenericView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer