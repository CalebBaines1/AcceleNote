from PIL import Image

import pytesseract

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\cbain\AppData\Local\Programs\Tesseract-OCR\tesseract'

# Simple image to string
print(pytesseract.image_to_string(Image.open('images/hi.jpg'))+ "hi")