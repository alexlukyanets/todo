from django.urls import path
from . import views

urlpatterns = [
    #Todos
    path('todos/completed/', views.TodoCompletedList.as_view()),
    path('todos/', views.TodoCreateList.as_view()),
    path('todos/<int:pk>', views.TodoRetrieveUpdateDestroy.as_view()),
    path('todos/<int:pk>/compleate', views.TodoComplete.as_view()),

    # Auth
    path('signup', views.signup),
    path('login', views.login),
]