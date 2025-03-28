import cv2
import dlib
import numpy as np

PREDICTOR_PATH = "H:\\PROJECTS OF PYTHON\\Facial-Hair-and-Hairstyle-Recommendator\\models\\shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

def euclidean_distance(p1, p2):
    return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def detect_face_shape(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = detector(gray)
    if len(faces) == 0:
        return "No face detected"

    # Process the first detected face
    face = faces[0]
    landmarks = predictor(gray, face)

    # Facial measurements using Euclidean distances
    jaw_width = euclidean_distance(landmarks.part(0), landmarks.part(16))  # Jawline width
    cheekbone_width = euclidean_distance(landmarks.part(3), landmarks.part(13))  # Cheekbone width
    forehead_width = euclidean_distance(landmarks.part(17), landmarks.part(26))  # Forehead width
    face_length = euclidean_distance(landmarks.part(8), landmarks.part(27))  # Face height

    # Angle-based feature extraction (handles angled faces)
    jaw_angle = np.degrees(np.arctan2(
        landmarks.part(8).y - landmarks.part(0).y,  # Vertical vs horizontal jawline
        landmarks.part(8).x - landmarks.part(0).x
    ))

    # Face shape classification based on advanced metrics
    if face_length / jaw_width > 1.5:
        return "Oval"
    elif jaw_width / cheekbone_width > 1.1 and jaw_angle < 80:
        return "Square"
    elif forehead_width / jaw_width > 1.1:
        return "Heart"
    elif face_length / forehead_width > 1.4:
        return "Rectangle"
    elif jaw_width > cheekbone_width and jaw_angle > 85:
        return "Diamond"
    else:
        return "Round"

    return "Unknown"
