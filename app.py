import os
from flask import Flask, request, render_template
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename
import util

# Here we need to find the current directory
dir_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = dir_path + '/data/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # request.file <class 'werkzeug.datastructures.FileStorage'>
        # request.url is http://127.0.0.1:5000/
        # check if the post request has the file part
        if 'file' not in request.files:
            log = 'no file field in request.'
            return render_template('fail.html', log=log)
        # print(request.files['file'])
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            log = 'Empty filename.'
            return render_template('fail.html', log=log)
        if file and util.allowed_file(file.filename):
            # get filename in a safe way
            filename = secure_filename(file.filename)
            # check if the data folder exists, if not create one
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            column_names, data_part = util.preview_csv(app.config['UPLOAD_FOLDER'] + filename)
            return render_template('verify.html', column_names=column_names, data_part=data_part, filename=filename)
    elif request.method == 'GET':
        return render_template('upload.html')


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    return render_template('verify.html')


@app.route('/configure', methods=['GET', 'POST'])
def configure():
    return render_template('configure.html')


@app.route('/run_tests', methods=['GET', 'POST'])
def run_tests():
    return render_template('run_tests.html')


@app.route('/review', methods=['GET', 'POST'])
def review():
    return render_template('review.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
