from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView, api_view
from rest_framework import status
from decouple import config
from groq import Groq
from . import models
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

import base64
import os
from google import genai
from google.genai import types















# def generate(text):
#     client = genai.Client(
#         api_key=os.environ.get("GEMINI_API_KEY"),
#     )

#     model = "gemini-2.5-pro"
#     contents = [
#         types.Content(
#             role="user",
#             parts=[
#                 types.Part.from_text(text="""a py code to print helo world 
# """),
#             ],
#         ),
#         types.Content(
#             role="model",
#             parts=[
#                 types.Part.from_text(text="""**Generating Python Snippet**

# I'm focusing on crafting a concise Python code snippet. My primary goal is to fulfill the request for a \"hello world\" print statement. The simplicity of this task is at the forefront of my efforts.


# **Creating Direct Output**

# Now, I'm confident in delivering the Python code. I've distilled the request to its core: a \"hello world\" print statement. The simplicity of this task demands a direct, efficient approach. I've assessed the basic Python syntax and the core requirements of the prompt and am ready. The solution is print(\"hello world\").


# """),
#                 types.Part.from_text(text="""Of course, here is the Python code to print \"Hello, World!\":

# ```python
# print(\"Hello, World!\")
# ```

# ### How it works:

# *   `print()` is a built-in Python function that displays output to the screen.
# *   The text you want to print, in this case, \"Hello, World!\", is a string. In Python, strings are enclosed in either single or double quotation marks.

# When you run this code, the message \"Hello, World!\" will be displayed on the screen."""),
#             ],
#         ),
#         types.Content(
#             role="user",
#             parts=[
#                 types.Part.from_text(text=text),
#             ],
#         ),
#     ]
#     tools = [
#         types.Tool(googleSearch=types.GoogleSearch(
#         )),
#     ]
#     generate_content_config = types.GenerateContentConfig(
#         thinking_config = types.ThinkingConfig(
#             thinking_budget=-1,
#         ),
#         tools=tools,
#     )

#     for chunk in client.models.generate_content_stream(
#         model=model,
#         contents=contents,
#         config=generate_content_config,
#     ):
#         print(chunk.text, end="")

# if __name__ == "__main__":
    # generate()






client = Groq(api_key=config('GROQ_API'))


def landingpage(request):
    return render(request,'home/landingpage.html')

def chat(request):
    return render(request,'home/chat.html')





def generate(text):
    full_response = ""
    completion = client.chat.completions.create(
     model="openai/gpt-oss-120b", 
     messages=[
        {
         "role": "system",
         "content": "you are an advance ai named SKY ! made by Shishir Khatri also known as MRKC do not say repetly that u are SKy made by shishi Khatri aka MRKC"
       },
       {
         "role": "user",
         "content": text
       }
     ],
    
    temperature=1,
    max_completion_tokens=8192,
    top_p=1,
    reasoning_effort="medium",
    stream=True,
    stop=None
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
    
