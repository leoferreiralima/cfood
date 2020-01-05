from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from rest_framework import serializers, mixins, generics


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
