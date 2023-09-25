from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import LoginSerializer, RegistrationSerializer
from .renderers import UserJSONRenderer


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        email = user.get('email', '')   
        password = user.get('password', '')
        user = authenticate(request, email=email, password=password)
        token, created = Token.objects.get_or_create(user=user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        if user:
            return Response({'jwt-token': access_token}, status=status.HTTP_200_OK)
        

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class UserDetailsView(APIView):
    

    def get(self, request):
        user = request.user
        user.data = {
            'username' : user.username,
            'email': user.email,
            'password': user.password,
        }
        return Response(user.data)