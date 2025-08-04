from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path('',views.landingpage,name='chat'),
    path('chat/',views.chat,name='chat'),
    # path('chat/',views.Chat.as_view()),
    path('sky/chat/',views.AI.as_view()),
    # path('chat/<str:p>/',views.Chat.as_view())
    
]
