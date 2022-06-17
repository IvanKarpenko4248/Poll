from django.urls import path
from . import views

urlpatterns = [
    path('', views.PollsMainView.as_view(), name='home'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('poll/<int:pk>/', views.PollDetailView.as_view(), name='poll_detail'),
    path('question/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
]
