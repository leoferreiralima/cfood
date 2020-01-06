from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.serializers import ProductItemSerializer
from api.models import ProductItem
from api.base import RetrieveUpdateDestroyAPIView, NumberInFilter, BaseFilter, TYPES

from rest_framework import filters
from django_filters import rest_framework as field_filters


class BaseProductItemFilter:
    id = TYPES["number"]


class ProductItemFilter(field_filters.FilterSet):
    id_max = field_filters.NumberFilter(field_name="id", lookup_expr='lte')
    id_min = field_filters.NumberFilter(field_name="id", lookup_expr='gte')
    #ids = NumberInFilter(field_name='id', lookup_expr='in')

    class Meta:
        model = ProductItem
        fields = ['id']


class ProductItemListCreate(generics.ListCreateAPIView):
    queryset = ProductItem.objects.filter(active=True)
    serializer_class = ProductItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter,
                       filters.SearchFilter, field_filters.DjangoFilterBackend]
    ordering_fields = "__all__"
    ordering = ['id']
    search_fields = ["id", "name"]
    filterset_class = BaseFilter(
        BaseProductItemFilter, ProductItemFilter).to_class()


class ProductItemListRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = ProductItem.objects.all()
    serializer_class = ProductItemSerializer
    permission_classes = [IsAuthenticated]
