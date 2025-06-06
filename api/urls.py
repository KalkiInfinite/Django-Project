from django.urls import path 
from .views import GoogleAuthView, AddItemView, GetItemView

urlpatterns = [
    path('google-auth/', GoogleAuthView.as_view(), name='google-auth'),
    path('add-item/', AddItemView.as_view(), name='add-item'),
    path('get-items/', GetItemView.as_view(), name='get-items'),
]
