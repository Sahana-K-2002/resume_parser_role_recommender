import os
from flask import Flask, render_template, request
from pyresparser import ResumeParser

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_skills_from_pdf(filepath):
    data = ResumeParser(filepath).get_extracted_data()
    skills = data.get('skills', [])
    return skills

def create_uploads_folder():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    create_uploads_folder()
    
    file = request.files['file']
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        skills = extract_skills_from_pdf(filepath)
        print(skills)
    
    print('no files')

if __name__ == '__main__':
    app.run()

