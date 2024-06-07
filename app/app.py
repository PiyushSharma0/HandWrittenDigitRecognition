import tkinter as tk
from tkinter import Button, Canvas, Label
import tensorflow as tf
import numpy as np
from PIL import Image, ImageGrab
import io

# Load the pre-trained model
model = tf.keras.models.load_model('model/mnist_cnn_model.h5')

class DigitRecognizerApp:
    def __init__(self, master):
        self.master = master
        master.title("Digit Recognizer")

        self.canvas = Canvas(master, width=280, height=280, bg='white', bd=2, relief='groove')
        self.canvas.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.label_result = Label(master, text="Prediction: None")
        self.label_result.grid(row=1, column=0, columnspan=2)

        self.button_clear = Button(master, text="Clear", command=self.clear_canvas)
        self.button_clear.grid(row=2, column=0)

        self.button_predict = Button(master, text="Predict", command=self.predict_digit)
        self.button_predict.grid(row=2, column=1)

        self.drawing = False
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)

    def start_draw(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event):
        if self.drawing:
            x = event.x
            y = event.y
            self.canvas.create_line((self.last_x, self.last_y, x, y), width=10, fill='black', capstyle=tk.ROUND, smooth=tk.TRUE)
            self.last_x = x
            self.last_y = y

    def clear_canvas(self):
        self.canvas.delete("all")
        self.label_result.config(text="Prediction: None")

    def predict_digit(self):
        image = self.canvas_to_image()
        image = np.expand_dims(image, axis=0)
        image = tf.cast(image, tf.float32) / 255.0
        prediction = model.predict(image)
        predicted_digit = np.argmax(prediction)
        self.label_result.config(text=f"Prediction: {predicted_digit}")

    def canvas_to_image(self):
        x = self.master.winfo_rootx() + self.canvas.winfo_x()
        y = self.master.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        raw_data = ImageGrab.grab().crop((x, y, x1, y1))
        img = raw_data.resize((28, 28))
        img = img.convert('L')
        img = np.array(img)
        return img


root = tk.Tk()
app = DigitRecognizerApp(root)
root.mainloop()
