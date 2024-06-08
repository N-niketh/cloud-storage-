from flask import Flask, request, jsonify, render_template, send_from_directory
import uuid
import os
from threading import Thread
from db import db
import dns.resolver
from werkzeug.utils import secure_filename

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['1.1.1.1']

UPLOAD_DIR = 'uploads'

app = Flask(__name__, template_folder='templates')

@app.route('/<unique_id>', methods=['GET', 'POST'])
def upload(unique_id):
    if request.method == 'POST':
        files = request.files.getlist('files')  
        check = db.storage.find_one({"unique_id": unique_id})
        if check:
            user = check["user_id"]
            user_dir = os.path.join(UPLOAD_DIR, str(user))
            os.makedirs(user_dir, exist_ok=True)
            for file in files:
                filename = secure_filename(file.filename)
                filepath = os.path.join(user_dir, filename)
                if os.path.exists(filepath):
                    base, extension = os.path.splitext(filename)
                    count = 1
                    while os.path.exists(filepath):
                        filename = f"{base}_{count}{extension}"
                        filepath = os.path.join(user_dir, filename)
                        count += 1
                file.save(filepath)
    return render_template('upload.html', unique_id=unique_id)

@app.route('/view/<unique_id>', methods=['GET'])
def view_file(unique_id):
    view = request.args.get('view')
    if view == 'true':
        check = db.storage.find_one({"unique_id": unique_id})
        if check:
            user = check["user_id"]
            user_dir = os.path.join(UPLOAD_DIR, str(user))
            files = os.listdir(user_dir)
            if files:
                return render_template('view_files.html', unique_id=unique_id, files=files, user=user)
            else:
                return jsonify({"error": "No files found for this user"}), 404
        else:
            return jsonify({"error": "Invalid unique_id"}), 404
    return jsonify({"error": "Invalid request"}), 400

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    unique_id = request.args.get('unique_id')
    if unique_id:
        check = db.storage.find_one({"unique_id": unique_id})
        if check:
            check_user_dumbo = check["user_id"]
            user_dir = os.path.join(UPLOAD_DIR, str(check_user_dumbo))
            return send_from_directory(user_dir, filename, as_attachment=True)
    return jsonify({"error": "Unauthorized access"}), 403

@app.route('/', methods=['GET', 'POST'])
def generate_link():
    unique_id = str(uuid.uuid4())
    link = f'{unique_id}'
    return jsonify({'unique_id': link})
@app.route('/delete/<filename>', methods=['GET'])
def delete_file(filename):
    unique_id = request.args.get('unique_id')
    if unique_id:
        check = db.storage.find_one({"unique_id": unique_id})
        if check:
            check_user_id = check["user_id"]
            user_dir = os.path.join(UPLOAD_DIR, str(check_user_id))
            filepath = os.path.join(user_dir, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                return jsonify({"message": "File deleted successfully"}), 200
            else:
                return jsonify({"error": "File not found"}), 404
        else:
            return jsonify({"error": "Invalid unique_id"}), 404
    return jsonify({"error": "Unauthorized access"}), 403

def run():
    app.run()

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
