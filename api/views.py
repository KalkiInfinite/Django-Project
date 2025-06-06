import os
import requests
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Item
from .serializers import ItemSerializer

# Google OAuth 2.0 Authentication View
class GoogleAuthView(APIView):
    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'error': 'Authorization code not provided'}, status=400)

        token_url = 'https://oauth2.googleapis.com/token'
        data = {
            'code': code,
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'redirect_uri': os.getenv('GOOGLE_REDIRECT_URI'),
            'grant_type': 'authorization_code'
        }
        token_response = requests.post(token_url, data=data)
        if not token_response.ok:
            return Response({'error': 'Failed to fetch access token'}, status=400)

        access_token = token_response.json().get('access_token')
        if not access_token:
            return Response({'error': 'Invalid token response'}, status=400)

        user_info = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers={
            'Authorization': f'Bearer {access_token}'
        }).json()

        email = user_info.get('email')
        name = user_info.get('name')

        if not email:
            return Response({'error': 'Unable to fetch user email'}, status=400)

        user, _ = User.objects.get_or_create(username=email, defaults={'first_name': name})
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

# Add an Item
class AddItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve Items (with optional filter)
class GetItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        title_filter = request.query_params.get('title')
        items = Item.objects.filter(user=request.user)
        if title_filter:
            items = items.filter(title__icontains=title_filter)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
