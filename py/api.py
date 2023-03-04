from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from PIL import Image
import pytesseract
import werkzeug
import os
import openai

# Initialize App
app = Flask(__name__)
api = Api(app)

# Set path for pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\cbain\AppData\Local\Programs\Tesseract-OCR\tesseract'

# Initialize openai object
openai.api_key = os.getenv("OPENAI_API_KEY")

# /text_recognition
class Text_Recognition(Resource):
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        gen_text = self.img_process(args['file'])
        response_text = self.text_process(gen_text)
        return self.build_response(response_text)
    
    def img_process(self, img):
        return pytesseract.image_to_string(img, lang='eng')
    
    def text_process(self, text):
        text_file =  open('prompts/summary_prompt.txt','r')
        sample_prompt = text_file.read()
        output_text = '`\n`Output: '
        process_prompt =  sample_prompt + text + output_text
        completion =  openai.Completion.create(model='text-davinci-003', prompt=process_prompt, max_tokens=100, temperature=0)
        return completion.choices[0].text
        

    def build_response(self, resp_text):
        clean_resp_text =  resp_text.strip().rstrip('\n').lstrip('\n')
        section_list = clean_resp_text.split(':')
        
        if len(section_list) == 3:
            section_list[1] = section_list[1].strip().replace('Summary', '').rstrip('\n')
            section_list[2] = section_list[2].strip()
            return jsonify(title=section_list[1], summary=section_list[2])
        return jsonify(error='Parse Error')

        

# api.com/text_recognition
api.add_resource(Text_Recognition, '/text_recognition')

if __name__ =="__main__":
    app.run(debug=True)