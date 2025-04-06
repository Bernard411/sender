import requests
import json
from django.http import JsonResponse
import random

REMOTE_API_URL = "https://innocent2025.pythonanywhere.com/api/update_data/"

def send_data(request):
    sensor_value = random.uniform(10, 100)
    data = {"sensor_value": sensor_value}

    try:
        response = requests.post(REMOTE_API_URL, json=data)

        # Debugging output
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)

        if response.ok:
            return JsonResponse({"message": "Data sent successfully!"})
        return JsonResponse({"error": f"Failed to send data: {response.text}"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        print("Request Error:", str(e))
        return JsonResponse({"error": f"Request failed: {str(e)}"}, status=500)


import subprocess
import os
from django.http import JsonResponse
from django.shortcuts import render

# Get the directory of the current file (views.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = os.path.join(BASE_DIR, "water_api.py")

# Store process ID globally
process = None

def control_script(request, action):
    global process

    if action == "start":
        if process is None:
            process = subprocess.Popen(["python3", SCRIPT_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return JsonResponse({"status": "Script started"})
        else:
            return JsonResponse({"status": "Already running"})

    elif action == "stop":
        if process:
            process.terminate()  # Stop the script
            process = None
            return JsonResponse({"status": "Script stopped"})
        else:
            return JsonResponse({"status": "Not running"})

    return JsonResponse({"status": "Invalid action"})

# import subprocess
# import os
# from django.http import JsonResponse
# from django.shortcuts import render
# import platform

# # Get the directory of the current file (views.py)
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# SCRIPT_PATH = os.path.join(BASE_DIR, "water_api.py")

# # Store process ID globally
# process = None

# def control_script(request, action):
#     global process

#     # Choose the right python command based on OS
#     python_command = "python3" if platform.system() != "Windows" else "python"

#     if action == "start":
#         if process is None:
#             process = subprocess.Popen([python_command, SCRIPT_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             return JsonResponse({"status": "Script started"})
#         else:
#             return JsonResponse({"status": "Already running"})

#     elif action == "stop":
#         if process:
#             process.terminate()  # Stop the script
#             process = None
#             return JsonResponse({"status": "Script stopped"})
#         else:
#             return JsonResponse({"status": "Not running"})

#     return JsonResponse({"status": "Invalid action"})


def control_page(request):
    return render(request, "control.html")
