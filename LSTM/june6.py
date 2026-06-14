import numpy as np
import matplotlib.pyplot as plt

print("Import Tensorflow")
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dropout, Dense
print("Tensorflow version", tf.__version__)

vocab_size = 10000
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=vocab_size)
print("Loaded dataset with {} training samples, {} test samples".format(len(X_train), len(X_test)))

max_length = 200
X_train = pad_sequences(X_train, maxlen=max_length, padding='post')
X_test = pad_sequences(X_test, maxlen=max_length, padding='post') 

print(X_train[0])  

word_index = imdb.get_word_index()
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
reverse_word_index[0] = "[PADDING]"
reverse_word_index[1] = "[START]"
reverse_word_index[2] = "[OOV]"
reverse_word_index[3] = "[UNUSED]"

def decode_review(text):
    return " ".join([reverse_word_index.get(i, "?") for i in text])

print(decode_review(X_train[100]))
print("Positif" if y_train[100] else "Negatif")

model = Sequential()
model.add(Embedding(vocab_size, 128, input_length=max_length))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

result = model.fit(X_train, y_train, batch_size=64, epochs=5, validation_split=0.2)

test_loss, test_accuracy = model.evaluate(X_test, y_test)
print("Test accuracy: {}".format(test_accuracy))

model.summary()

plt.plot(result.history['accuracy'], label='Training Accuracy')
plt.plot(result.history['loss'], label='Training Loss')
plt.title('Training Performance')
plt.ylabel('Accuracy/Loss')
plt.xlabel('Epoch')
plt.legend()
plt.show()