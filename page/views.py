import os
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image

# Define the path to the dataset folder containing the disease folders
dataset_path = 'C:\\Harinee\\SIH\\cottoncure\\ml_model\\extracted_data'  # Path to the folder containing class subfolders
class_names = os.listdir(dataset_path)  # Extract class names from the dataset

# Load the model (ensure this import points to your actual model loading logic)
from .load_model import model  # Import the loaded model

def index(request):
    return render(request, 'page/index.html')

# Predefined users allowed to sign up (with phone numbers)
ALLOWED_USER = {"name": "Harinee", "phone": "7550110045"}  # The one allowed user

def login_view(request):
    if request.method == 'POST':
        # Skip all validation and directly redirect after form submission
        return redirect("{% url 'choose_page' %}")  # Replace 'choose_page' with the actual name of your URL or path for 'choose.html'

    return render(request, 'page/login.html')

def blog_view(request):
    return render(request, 'page/blog.html')

def blogsub_view(request):
    return render(request, 'page/blogsub.html')

def choose_view(request):
    return render(request, 'page/choose.html')

def page3_view(request):
    return render(request, 'page/page3.html')

def payment_view(request):
    return render(request, 'page/payment.html')

def preprocess_image(image_file):
    # Open the uploaded image file using PIL
    img = Image.open(image_file)
    
    # Resize the image to 224x224 (assuming your model expects this size)
    img = img.resize((224, 224), Image.LANCZOS)

    # Convert the image to array
    img_array = image.img_to_array(img)

    # Normalize the image array
    img_array = img_array / 255.0  # Scale pixel values to [0, 1]

    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

def page1_view(request):
    if request.method == 'POST' and request.FILES['image']:
        img_file = request.FILES['image']

        # Preprocess the image
        img_array = preprocess_image(img_file)

        # Make prediction
        prediction = model.predict(img_array)
        predicted_class_index = np.argmax(prediction)  # Get index of the highest probability

        # Map index to class names
        predicted_label = class_names[predicted_class_index]

        # Map predicted diseases to specific HTML templates
        disease_templates = {
            'aphids': 'page/aphids.html',
            'army worm': 'page/army_worm.html',
            'bacterial blight': 'page/bacterial_blight.html',
            'powdery mildew': 'page/powdery_mildew.html',
            'target spot': 'page/target_spot.html'
        }

        # Use the predicted disease name to determine the template to render
        selected_template = disease_templates.get(predicted_label.lower(), 'page/result.html')

        # Get the disease name from the uploaded file name
        file_name, _ = os.path.splitext(img_file.name)  # Extract the name without the extension

        # Render the selected template and pass the predicted disease
        return render(request, selected_template, {'predicted_label': predicted_label, 'file_name': file_name})

    return render(request, 'page/page1.html')  # A template for uploading the image





