"""Face detection script using OpenCV.

This module provides a command line utility to detect faces in a video or
webcam stream and save each detected face as an individual image.
"""

from __future__ import annotations

import argparse
import os

import cv2


def capture_faces(video_path: str, output_dir: str = "faces") -> None:
    """Detect faces from a video source and save them as images.

    Args:
        video_path: Path to the input video file. Use an integer (as string)
            like "0" to access a webcam.
        output_dir: Directory where detected face images will be stored.
    """

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    # Allow numeric webcam index strings (e.g., "0")
    source = int(video_path) if video_path.isdigit() else video_path
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise FileNotFoundError(f"Unable to open video source: {video_path}")

    os.makedirs(output_dir, exist_ok=True)
    saved_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            face_img = frame[y : y + h, x : x + w]
            output_path = os.path.join(output_dir, f"face_{saved_count}.jpg")
            cv2.imwrite(output_path, face_img)
            saved_count += 1

        cv2.imshow("Video - Face Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Saved {saved_count} face images to '{output_dir}'.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Detect faces in a video or webcam and save them as images."
    )
    parser.add_argument(
        "--video",
        default="sample_video.mp4",
        help="Path to the input video file or webcam index (e.g., 0)",
    )
    parser.add_argument(
        "--output",
        default="faces",
        help="Directory to save detected face images",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    capture_faces(args.video, args.output)

