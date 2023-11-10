import cv2
import argparse
import tkinter as tk
from tkinter import font
import os
from PIL import Image, ImageTk
import time
import matplotlib.pyplot as plt
import numpy as np

# Function to parse the arguments from the command line.
def parse_args():
    parser = argparse.ArgumentParser(description="Add a watermark on an image.")
    parser.add_argument('--image_path', type=str, required=True, help='Path of the image that you want to apply the watermark on.')
    parser.add_argument('--watermark_path', type=str, required=True, help='Path of the watermark')
    return parser.parse_args()

# Create a Tkinter class to implement drawing ROI functionality.
class Application(tk.Frame):
    def __init__(self, img_path, watermark_path, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.img_path = img_path
        self.watermark_path = watermark_path
        self.create_widgets()

    def create_widgets(self):
        # Load and display the image
        self.img = Image.open(self.img_path)
        self.tkimage = ImageTk.PhotoImage(self.img)
        self.canvas = tk.Canvas(self, width=self.img.width, height=self.img.height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tkimage)
        self.canvas.pack()

        
        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Add a button to apply watermark
        self.watermark_button = tk.Button(self, text="Apply Watermark", command=self.apply_watermark_on_image, font=font.Font(size=12), height=2, width=20)
        self.watermark_button.pack()

        # Add a save button
        self.save_button = tk.Button(self, text="Save Image", command=self.save_image, font=font.Font(size=12), height=2, width=20)
        self.save_button.pack()

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        # Create a rectangle (initially a single point)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=3)
        # Bind the motion event
        self.canvas.bind("<B1-Motion>", self.on_motion)

    def on_motion(self, event):
        # Update the rectangle's end point to the current mouse position
        self.end_x, self.end_y = event.x, event.y
        # Update the rectangle's coordinates
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_release(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.rectangle_coords = (self.start_x, self.start_y, self.end_x, self.end_y)
        # Unbind the motion event
        self.canvas.unbind("<B1-Motion>")

    
    def apply_watermark_on_image(self):

        # Read the image and the watermark
        img = cv2.imread(self.img_path)
        watermark = cv2.imread(self.watermark_path, -1) # .png, including the alpha channel.

        # Get all the channels including Alpha
        b,g,r,a = cv2.split(watermark)
        
        # Get the inverse alpha (basically an inv mask with a .png image.)
        inverse_a = cv2.bitwise_not(a)
        # Merge the alpha and inv alpha since original image has 3 channels.
        a_merged = cv2.merge([a, a, a])
        inverse_a_merged = cv2.merge([inverse_a, inverse_a, inverse_a])

        # Get the coordinates of the plotted ROI.
        tlx, tly, brx, bry = self.rectangle_coords
        roi = img.copy()[tly:bry, tlx:brx] # ROI from the image.

        # Resize the masks to the size of the ROI
        a_merged = cv2.resize(a_merged,(roi.shape[1], roi.shape[0]), cv2.INTER_AREA) 
        inverse_a_merged = cv2.resize(inverse_a_merged,(roi.shape[1], roi.shape[0]), cv2.INTER_AREA)

        # Perform bitwise operations to obtain the final combined ROI
        resized_watermark = cv2.resize(watermark[:,:,:3],(roi.shape[1], roi.shape[0]), cv2.INTER_AREA)
        watermark_foreground = cv2.bitwise_and(resized_watermark, a_merged)
        roi_background = cv2.bitwise_and(roi, inverse_a_merged)
        final_combined_roi = cv2.bitwise_or(watermark_foreground, roi_background)
        
        # Append the ROI back to the original image
        img[tly:bry, tlx:brx] = final_combined_roi

        # Update the canvas with the new image
        self.img_with_watermark = img
        self.tkimage = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(self.img_with_watermark, cv2.COLOR_BGR2RGB)))
        self.canvas.create_image(0, 0, anchor="nw", image=self.tkimage)

    def save_image(self):

        # Save the image
        cv2.imwrite('outputs/image_with_watermark.jpeg', self.img_with_watermark)
        self.quit()

if __name__ == '__main__':

    # Get commandline arguments
    args = parse_args()
    img_path = args.image_path
    watermark_path = args.watermark_path

    # 1. Create a Tkinter GUI which allows user to draw a ROI on the image
    root = tk.Tk()
    app = Application(img_path=img_path, watermark_path=watermark_path, master=root)
    app.mainloop()


