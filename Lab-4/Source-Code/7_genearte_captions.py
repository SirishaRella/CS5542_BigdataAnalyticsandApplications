from pickle import load
from numpy import argmax
import glob
from keras.preprocessing.sequence import pad_sequences
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
from keras.models import load_model


# extract features from each photo in the directory
def extract_features(filename):
    # load the model
    model = VGG16()
    # re-structure the model
    model.layers.pop()
    model = Model(inputs=model.inputs, outputs=model.layers[-1].output)
    # load the photo
    image = load_img(filename, target_size=(224, 224))
    # convert the image pixels to a numpy array
    image = img_to_array(image)
    # reshape data for the model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # prepare the image for the VGG model
    image = preprocess_input(image)
    # get features
    feature = model.predict(image, verbose=0)
    return feature


# map an integer to a word
def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


# generate a description for an image
def generate_desc(model, tokenizer, photo, max_length):
    # seed the generation process
    in_text = 'startseq'
    # iterate over the whole length of the sequence
    for i in range(max_length):
        # integer encode input sequence
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        # pad input
        sequence = pad_sequences([sequence], maxlen=max_length)
        # predict next word
        yhat = model.predict([photo, sequence], verbose=0)
        # convert probability to integer
        yhat = argmax(yhat)
        # map integer to word
        word = word_for_id(yhat, tokenizer)
        # stop if we cannot map the word
        if word is None:
            break
        # append as input for generating the next word
        in_text += ' ' + word
        # stop if we predict the end of the sequence
        if word == 'endseq':
            break
    return in_text


# load the tokenizer
tokenizer = load(open('models/tokenizer.pkl', 'rb'))
# pre-define the max sequence length (from training)
max_length = 12
# load the model
model = load_model('models/showandtell.h5')

# load and prepare the photograph
photo = extract_features('3.jpg')

list = []
for item in glob.glob("C:\\Users\\Siri\\Desktop\\Lab-4\\Show_and_Tell\\test_data\\1\\*.jpg"):
    print(item)
    photo = extract_features(item)
    # generate description
    description = generate_desc(model, tokenizer, photo, max_length)
    description = description.split(' ')
    s = " "
    list.append(s.join(description[1:len(description)-1]))
    print(list)

final_output = ""

with open('prediction.txt', 'w') as file:
    for item in range(0, len(list)):
        final_output = final_output + list[item] + " "
        file.write(final_output)

print(final_output)


