from rest_framework import serializers
from todo.models import Todo


class TodoSeralizer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    datecompleted = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = ['id', 'title', 'memo', 'created', 'datecompleted', 'important', 'important']


class TodoCompleteSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id']
        read_only_fields = ['id', 'title', 'memo', 'created', 'datecompleted', 'important', 'important']
