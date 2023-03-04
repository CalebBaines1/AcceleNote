from flask import Flask
from flask_restful import Resource, Api, reqparse
from PIL import Image
import pytesseract
import werkzeug

# Initialize App
app = Flask(__name__)
api = Api(app)

# Set path for pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\cbain\AppData\Local\Programs\Tesseract-OCR\tesseract'

# /text_recognition
class Text_Recognition(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        return self.img_process(args['file'])
    
    def img_process(self, img):
        return pytesseract.image_to_string(img, lang='eng')
    

# api.com/text_recognition
api.add_resource(Text_Recognition, '/text_recognition')

if __name__ =="__main__":
    app.run()