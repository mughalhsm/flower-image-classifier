import os
import tensorflow as tf
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import json
from PIL import Image
import argparse

# Turning logging off in terminal output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

# Creat a parser
parser = argparse.ArgumentParser(description="CLI Application the predicts flower species from image")

# Positional arguments 
parser.add_argument("image", help="path to the input image", type=str)
parser.add_argument("model", help="path to the saved Keras model", type=str)

# Optional arguments 
parser.add_argument("-k", "--top_k", default=5, help ="top k class probabilities", type=int)
parser.add_argument("-n", "--category_names", default="./label_map.json", help="path to mapping labels to the flower species names", type=str)

args = parser.parse_args()   


image_path = args.image
saved_model = args.model
top_k = args.top_k
category_names = args.category_names


# Load a JSON file that maps the class values to other category names
with open(category_names, 'r') as f:
    class_names = json.load(f)


# Load the saved model 
loaded_model = tf.keras.models.load_model(saved_model, custom_objects={'KerasLayer': hub.KerasLayer}, compile=False)

def process_image(image):
    image = tf.convert_to_tensor(image, dtype=tf.float32)
    image = tf.image.resize(image, (image_size, image_size))
    image /= 255
    return image.numpy()


# Image resize and normalization
image_size = 224
def process_image(image):
    image = tf.convert_to_tensor(image, dtype=tf.float32)
    image = tf.image.resize(image, (image_size, image_size))
    image /= 255
    return image.numpy()


# Predict the top K flower classes along with probabilities
def predict(image_path, model, top_k):
    image = Image.open(image_path)
    image = np.asarray(image)
    processed_image = process_image(image)
    
    expanded_image = np.expand_dims(processed_image, axis=0)
    
    prediction = model.predict(expanded_image)
    
    print(prediction.shape)
    top_k_values, top_k_indices = tf.nn.top_k(prediction, k= top_k)
    return top_k_values.numpy()[0], top_k_indices.numpy()[0]


# Getting probabilites then print class name and probability. 
top_k_probs, top_k_classes = predict(image_path, loaded_model, top_k) 
print('List of flower labels along with corresponding probabilities:', top_k_classes, top_k_probs)
print(class_names)
print('----------Predictions-----------')
for i in range(len(top_k_classes)):
    print('Number - ', i + 1)
    print('Flower Species: ', class_names[str(top_k_classes[i]+1)])
    print('Probability: ', top_k_probs[i])
    print('- - - - - - - - - - - - - - - - -')
