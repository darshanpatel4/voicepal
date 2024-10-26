import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import urllib3
import wikipedia 
import datetime
import requests
from urllib.parse import quote

def home(request):
    return render(request, 'index.html')

@csrf_exempt
def process_voice_input(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            voice_input = data.get('voiceInput', '')

            query = voice_input.lower()

            # Process the voice input as needed
            if "what is your name" in query or "what's your name" in query or "tell me your name" in query:
                message = "My name is Firday."
                # print("My name is Max.")
                response_data = {'message': message}
                return JsonResponse(response_data)

            
            elif 'wikipedia' in query:
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query)
                print(results)
                message = results
                response_data = {'message': message}
                return JsonResponse(response_data)

            elif 'time' in query:
                strTime = datetime.datetime.now().strftime("%I %M:%p")    
                message = f"Sir, it's {strTime}"
                response_data = {'message': message}
                return JsonResponse(response_data)

            elif 'location' in query:
                base_url = 'https://www.google.com/maps/place/'
                formatted_query = query.replace("location", "")  # Ensure query is URL-safe
                url = base_url + formatted_query
                message = f"Here is the location of {query}"
                response_data = {'message': message, 'url': url}
                return JsonResponse(response_data)

            elif 'youtube' in query:
                query = query.replace("youtube", "")
                url = 'https://www.youtube.com/results?search_query=' + query
                message = "Here is what I found for " + query
                response_data = {'message': message, 'url': url}
                return JsonResponse(response_data)

            else:
                message = ""
                response_data = {'message': message}
                return JsonResponse(response_data)
                
        except Exception as e:
            return JsonResponse({'error': 'Invalid data format'}, status=400)
    else:
        # Handle other HTTP methods, like GET, if needed
        return JsonResponse({'error': 'Method not allowed'}, status=405)