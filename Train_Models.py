#!/usr/bin/env python
# coding: utf-8
import os
import io
import itertools
import tensorflow as tf
from tensorflow import keras as K
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import datetime
import shutil


# Flagga för att ta bort all tidigare sparad logdata
clean_logs = False

# Skapa logmapp om den inte finns.
os.makedirs("logs/", exist_ok=True)

# Rensa loggdata
if clean_logs:
    shutil.rmtree("logs/")


# Funktion för att generara en "Confusion matrix" som kan skrivas som en tensorflow bild.
def image_cmatrix(model, xtest, ytest):

    # Förutsäg utvärden och välj det med högst sannolikhet som prediktion.
    ypred = model.predict(xtest).argmax(-1)
    ytest = ytest.argmax(-1)
    acc = (ytest == ypred).mean()
    class_names = [str(x) for x in range(10)]

    # Bygg upp en förväxlingsmatris
    cm = confusion_matrix(ytest, ypred, normalize='true')
    figure = plt.figure(figsize=(8, 8))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(f"Average accuracy{round(100 * acc, 2)}", fontsize=22)
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=45)
    plt.yticks(tick_marks, class_names)

    # Normalisera matrisen
    cm = np.around(cm.astype('float') / cm.sum(axis=1)
                   [:, np.newaxis], decimals=2)

    # Bästäm gräns på när texten ska vara vit och när den ska vara svart.
    threshold = cm.max() / 2.

    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        color = "white" if cm[i, j] > threshold else "black"
        plt.text(j, i, cm[i, j], horizontalalignment="center", color=color)

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

    # Använd en byte buffer för att spara bilden i minnet
    buf = io.BytesIO()

    plt.savefig(buf, format='png')
    plt.close(figure)
    buf.seek(0)

    # Konvertera bilden till en tensor
    image = tf.image.decode_png(buf.getvalue(), channels=4)
    image = tf.expand_dims(image, 0)

    return image


####        TensorFlow delen börjar här          ####
#### Du behöver inte modifiera någonting ovanför ####
# Läs in datan
x_train = np.concatenate([np.load(f"X Train{i+1}.npy") for i in range(2)])
x_test = np.load("X Test.npy")
x_move = np.load("X Moved Numbers.npy")
x_rot = np.load("X Rotated Numbers.npy")

y_train = np.load("Y Train.npy")
y_test = np.load("Y Test.npy")
y_move = np.load("Y Moved Numbers.npy")
y_rot = np.load("Y Rotated Numbers.npy")


# Model för ett vanlig artificiellt-neuronnät.
def non_convolutional_model():
    model = K.Sequential()
    model.add(K.layers.Flatten())
    model.add(K.layers.Input(28*28))
    model.add(K.layers.Dense(32, activation="relu"))
    model.add(K.layers.Dense(10, activation="softmax"))

    model.compile(loss="categorical_crossentropy",
                  optimizer=K.optimizers.SGD(lr=0.7),
                  metrics=["accuracy"],)
    return model


# Model för ett "convolutional" neuronnät.
def convolutional_model():
    model = K.Sequential()
    model.add(K.layers.Input((28, 28, 1)))
    model.add(K.layers.Conv2D(16, kernel_size=(
        16, 16),
        strides=(1, 1),
        activation="relu"))
    model.add(K.layers.MaxPooling2D())
    model.add(K.layers.Flatten())
    model.add(K.layers.Dense(10, activation="softmax"))

    model.compile(loss="categorical_crossentropy",
                  optimizer=K.optimizers.SGD(lr=0.7),
                  metrics=["accuracy"])
    return model


# Mapp för att logga resultat som ska visas i tensorboard
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tb_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, profile_batch=0)

# Välj en modell
model = non_convolutional_model()

# Träna modellen
model.fit(x_train, y_train,
          epochs=100,
          validation_split=0.2,
          batch_size=256,
          verbose=1,
          callbacks=[tb_callback],
          )


# Skriv resultat till filer.
file_writer = tf.summary.create_file_writer(log_dir)
image_train = image_cmatrix(model, x_train, y_train)
image_test = image_cmatrix(model, x_test, y_test)
image_move = image_cmatrix(model, x_move, y_move)
image_rot = image_cmatrix(model, x_rot, y_rot)

with file_writer.as_default():
    tf.summary.image("Train Data", image_train, max_outputs=1, step=0)
    tf.summary.image("Test Data", image_test, max_outputs=1, step=0)
    tf.summary.image("Moved Data", image_move, max_outputs=1, step=0)
    tf.summary.image("Rotated Data", image_rot, max_outputs=1, step=0)
