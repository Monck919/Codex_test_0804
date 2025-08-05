import cv2
import os

# 1) Load face detection model (OpenCV built-in Haar cascade)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# 2) Read video file (change to 0 to use webcam)
video_path = "sample_video.mp4"
cap = cv2.VideoCapture(video_path)

# Create directory to save detected faces
output_dir = "faces"
os.makedirs(output_dir, exist_ok=True)
saved_count = 0

# 3) Process video frame by frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale for better detection performance
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 4) Detect faces (parameters can be adjusted)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # 5) Draw rectangles on faces and save them as images
    for (x, y, w, h) in faces:
        # Draw rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Crop and save face region
        face_img = frame[y:y + h, x:x + w]
        output_path = os.path.join(output_dir, f"face_{saved_count}.jpg")
        cv2.imwrite(output_path, face_img)
        saved_count += 1

    # Display result
    cv2.imshow("Video - Face Detection", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 6) Cleanup
cap.release()
cv2.destroyAllWindows()

print(f"Saved {saved_count} face images.")
