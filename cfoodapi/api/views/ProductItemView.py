from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.serializers import ProductItemSerializer
from api.models import ProductItem
from api.base import RetrieveUpdateDestroyAPIView


class ProductItemListCreate(generics.ListCreateAPIView):
    queryset = ProductItem.objects.filter(active=True)
    serializer_class = ProductItemSerializer
    permission_classes = [IsAuthenticated]


class ProductItemListRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = ProductItem.objects.all()
    serializer_class = ProductItemSerializer
    permission_classes = [IsAuthenticated]
