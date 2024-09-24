import tensorflow as tf

print("TensorFlow version:", tf.__version__)

# Try creating a simple model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(10,)),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

print("Model created successfully!")