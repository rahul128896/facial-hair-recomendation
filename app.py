from flask import Flask, render_template, request, redirect, url_for, Response
import os
import cv2
import base64
import numpy as np
from werkzeug.utils import secure_filename
from models.detect_face import detect_face_shape
from models.recommendator import get_recommendation

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_frames():
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Could not open video source")
        return
    while True:
        success, frame = camera.read()
        if not success:
            print("Error: Could not read frame")
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file uploaded!", 400

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return "Invalid file type!", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    return redirect(url_for("result", filename=filename))

@app.route("/capture", methods=["POST"])
def capture_image():
    image_data = request.form["image"]
    image_data = image_data.split(",")[1]  

    image_array = np.frombuffer(base64.b64decode(image_data), np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    filename = "captured_image.jpg"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    cv2.imwrite(filepath, image)

    return redirect(url_for("result", filename=filename))

@app.route("/result")
def result():
    filename = request.args.get("filename")
    if not filename:
        return "No file provided!", 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    face_shape = detect_face_shape(filepath)
    recommended_hairstyle = get_recommendation(face_shape)

    return render_template("result.html", filename=filename, face_shape=face_shape, recommendation=recommended_hairstyle)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
