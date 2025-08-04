from .models import UserChat
from rest_framework import serializers

class USerChatserializer(serializers.ModelSerializer):
    class Meta:
        model = UserChat
        fields = ['user_chat','ai_reply']