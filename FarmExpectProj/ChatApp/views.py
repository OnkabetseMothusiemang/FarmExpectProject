from django.shortcuts import render
from django.http import  JsonResponse
import openai
import requests ,os
from django.core.files.base import ContentFile
from .models import Image  
from django.conf import settings
import json


def home(request):
    return render(request, 'index.html')


def chatBot(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body)
            user_input = data.get('user_input', '')

            if not user_input:
                return JsonResponse({'response': 'No input provided'}, status=400)

            # Set API key for OpenAI
            openai.api_key = settings.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input},
                ],
                max_tokens=256,
                temperature=0.5,
            )

            # Extract the chatbot response
            chatbot_response = response['choices'][0]['message']['content'].strip()

            if not chatbot_response:
                return JsonResponse({'response': 'No response from AI'}, status=500)

            return JsonResponse({'response': chatbot_response})

        except Exception as e:
            # Log the error
            print(f"Error: {e}")
            return JsonResponse({'response': 'An error occurred while processing your request.'}, status=500)

    return JsonResponse({'response': 'Invalid request method.'}, status=400)






def generate_image(request):
    openai.api_key = settings.OPENAI_API_KEY
    obj = None
    print('NO API')

    if openai.api_key is not None and request.method == 'POST':
        try:
            print('got API')
            user_input = request.POST.get('user_input')
            
            # Call OpenAI API to create the image
            response = openai.Image.create(
                prompt=user_input,
                size='256x256'
            )

            # Extract the image URL
            image_url = response["data"][0]["url"]
            print(image_url)

            # Download the image
            img_response = requests.get(image_url)
            
            if img_response.status_code == 200:
                img_file = ContentFile(img_response.content)

                # Create a unique filename
                count = Image.objects.count() + 1
                fname = f"image-{count}.jpg"

                # Save the image to your model
                obj = Image(phrase=user_input)
                obj.ai_image.save(fname, img_file)
                obj.save()

                print(obj)
                return render(request, 'image.html', {"object": obj})
            else:
                print('Image download failed.')
                return JsonResponse({"error": "Failed to download the image from OpenAI"}, status=500)

        except Exception as e:
            print(f"Error generating image: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    # If not a POST request, render the template without an image
    return render(request, 'image.html')


# Create your views here.
