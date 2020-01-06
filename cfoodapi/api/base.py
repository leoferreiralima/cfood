from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from rest_framework import serializers, mixins, generics, pagination
from django_filters import BaseInFilter, NumberFilter
from django_filters import rest_framework as field_filters


class CurrentUserDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user.id

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class AuditedEntitySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        default=serializers.CreateOnlyDefault(timezone.now))
    updated_at = serializers.DateTimeField(default=timezone.now)
    created_by = serializers.IntegerField(
        default=serializers.CreateOnlyDefault(CurrentUserDefault()))
    updated_by = serializers.IntegerField(default=CurrentUserDefault())


class AuditedEntity(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    created_by = models.IntegerField(editable=False)
    updated_by = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class RetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   generics.GenericAPIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        request.data["active"] = False
        return self.partial_update(request, *args, **kwargs)


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


TYPES = {
    'number': "NUMBER"
}


class BaseFilter:

    def __init__(self, base_class, filter_class):
        self.base_class = base_class
        self.filter_class = filter_class

    def to_class(self):
        base = self.base_class()

        filters = {}

        variables = [i for i in dir(base) if not i.startswith('__')]
        for v in variables:
            value = getattr(base, v)

            if (value == TYPES["number"]):
                filters[v] = field_filters.NumberFilter(
                    field_name=v, lookup_expr='exact')
                filters["%s_max" % v] = field_filters.NumberFilter(
                    field_name=v, lookup_expr='lte')
                filters["%s_min" % v] = field_filters.NumberFilter(
                    field_name=v, lookup_expr='gte')
                filters["%s_in" % v] = NumberInFilter(
                    field_name=v, lookup_expr='in')

        return type("Custom_%s" % base.__class__.__name__, (self.filter_class,), filters)
