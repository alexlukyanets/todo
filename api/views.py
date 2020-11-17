from django.contrib.auth.models import User
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from .serizalizers import TodoSeralizer, TodoCompleteSeralizer
from todo.models import Todo
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(request.POST['username'], password=request.POST['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except IntegrityError:
            return JsonResponse(({'error': 'That username has already been taken. Please choose a new username'}),
                                status=201)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        user = authenticate(request, username= request.POST['username'], password = request.POST['password'])
        if user is None:
            return JsonResponse(({'error': 'Check username or password'}),
                                status=201)
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=200)



class TodoCompletedList(generics.ListAPIView):
    serializer_class = TodoSeralizer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=False).order_by('-datecompleted')


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSeralizer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)


class TodoComplete(generics.UpdateAPIView):
    serializer_class = TodoCompleteSeralizer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.datecompleted = timezone.now()
        serializer.save()


class TodoCreateList(generics.ListCreateAPIView):
    serializer_class = TodoSeralizer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
