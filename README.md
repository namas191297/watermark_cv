# Image Watermarking Tool

This Python application allows users to apply a watermark to a selected region of an image. It is built using Tkinter for the GUI and uses OpenCV for image processing. Built as a fun project during my participation in the 'Mastering OpenCV with Python course' offered by OpenCV.

[![Video Demo](https://d33v4339jhl8k0.cloudfront.net/docs/assets/591c8a010428634b4a33375c/images/5ab4866b2c7d3a56d8873f4c/file-MrylO8jADD.png)](https://www.youtube.com/watch?v=0wKTHITp3Qw)


## Features

- Interactive GUI to select the region of interest (ROI) on the image for watermarking.
- Supports PNG watermark files.

## Installation

Before running the application, ensure you have Python installed on your system. This tool also requires additional Python libraries, which can be installed via pip.

1. Clone the repository.

```bash
cd watermark_cv
```

2. Install the required libraries: numpy, opencv-python, pillow, and matplotlib.

```bash
pip install numpy opencv-python pillow matplotlib
```

## Usage

To use this tool, follow these steps:

1. Launch the application.

```bash
python create_watermark.py --image_path "path/to/image.jpg" --watermark_path "path/to/watermark.png"
```
2. The application window will open displaying the chosen image.
3. Use the mouse to draw a rectangle on the image where you want the watermark to be applied.
4. Click the "Apply Watermark" button to add the watermark to the selected region.
5. Once satisfied with the result, click the "Save Image" button to save the watermarked image and exit the application.

## Notes

- The watermark file needs to be in PNG format.

## Contributing

Feel free to fork this repository and submit pull requests for any improvements or bug fixes.

## License

MIT
