import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# Get the base directory of your Django project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Construct the path to the model file
model_path = os.path.join(BASE_DIR, 'ml_model', 'cotton_disease_model.h5')

# Load the model
model = tf.keras.models.load_model(model_path)

def predict_disease(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # Load the image
    img_array = image.img_to_array(img)  # Convert to array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Normalize

    predictions = model.predict(img_array)  # Make predictions
    predicted_class = np.argmax(predictions, axis=1)  # Get the class index
    return predicted_class[0]  # Return the predicted class index


