from django.db import models
from django.contrib.auth.models import User



class UserAccount(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='user/image/',blank=True)


class UserChat(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE)
     user_chat = models.TextField()
     ai_reply = models.TextField()

     class Meta:
          verbose_name = 'conversation history'

     def __str__(self):
      return self.user.username
     