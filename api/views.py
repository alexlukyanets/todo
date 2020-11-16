from rest_framework import generics, permissions
from .serizalizers import TodoSeralizer
from todo.models import Todo


class TodoCompletedList(generics.ListAPIView):
    serializer_class = TodoSeralizer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print('Try')
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=False).order_by('-datecompleted')

class TodoCreateList(generics.ListCreateAPIView):
    serializer_class = TodoSeralizer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print('Try')
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
