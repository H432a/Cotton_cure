import os
import zipfile
import shutil
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras.optimizers import Adam

# Step 1: Unzip the dataset
input_zip_file = 'Cotton plant disease.zip'
extracted_folder = 'extracted_data'

# Extract ZIP file
with zipfile.ZipFile(input_zip_file, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder)
print(f"Files extracted to: {extracted_folder}")

# Step 2: Organize the dataset
dataset_folder = os.path.join(extracted_folder, 'Cotton plant disease')
new_dataset_folder = extracted_folder

# Move folders to the new dataset folder
for class_name in os.listdir(dataset_folder):
    old_path = os.path.join(dataset_folder, class_name)
    new_path = os.path.join(new_dataset_folder, class_name)
    
    # Only move if it's a directory
    if os.path.isdir(old_path):
        shutil.move(old_path, new_path)
        print(f'Moved {old_path} to {new_path}')

# Remove the empty original folder
if os.path.exists(dataset_folder):
    shutil.rmtree(dataset_folder)
    print(f'Removed empty folder: {dataset_folder}')

# Step 3: Set up data generators
train_datagen = ImageDataGenerator(rescale=1.0/255.0, validation_split=0.2)

# Load images for training and validation
train_generator = train_datagen.flow_from_directory(
    new_dataset_folder,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',  # Use 'categorical' for multi-class classification
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    new_dataset_folder,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',  # Use 'categorical' for multi-class classification
    subset='validation'
)

# Step 4: Define the model
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model = Sequential([
    base_model,
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(6, activation='softmax')  # 6 output classes for multi-class classification
])

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

# Step 5: Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size,
    epochs=25
)

# Optional: Save the model
model.save('cotton_disease_model.h5')
print("Model saved as cotton_disease_model.h5")



