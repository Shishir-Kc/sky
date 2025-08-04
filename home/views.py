from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView, api_view
from rest_framework import status
from decouple import config
from groq import Groq
from . import models
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny



client = Groq(api_key=config('GROQ_API'))


def landingpage(request):
    return render(request,'home/landingpage.html')

def chat(request):
    return render(request,'home/chat.html')





def generate(text):
    full_response = ""
    completion = client.chat.completions.create(
     model="gemma2-9b-it",
     messages=[
        {
         "role": "system",
         "content": "you are an advance ai named SKY !"
       },
       {
         "role": "user",
         "content": text
       }
     ],
     temperature=1,
     max_completion_tokens=1024,
     top_p=1,
     stream=True,
     stop=None,
 )

    for chunk in completion:
     data = chunk.choices[0].delta.content 
     if data:
        full_response +=data

    return full_response


class AI(APIView):
    permission_classes = [AllowAny]

    def post(self,request,p=None):
          user_input = p if p is not None else request.data.get('user_input')
        # user_info = request.user 
          data = user_input
          ai_response = generate(data)
          data = models.UserChat(user=request.user,user_chat=data,ai_reply=ai_response)
          data.save()
          return Response({
              'user':user_input,
              'ai':ai_response
              
              },status=status.HTTP_200_OK)
    
    def get(self,request):
        return Response({'message':'geettt'},status=status.HTTP_202_ACCEPTED)
    
