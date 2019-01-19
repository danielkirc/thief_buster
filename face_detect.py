#!/usr/bin/env python
import cv2
import face_recognition

known_faces = []
known_names = []

# WARNING: Very slow
def get_names(image, face_locations):
    face_encodings = face_recognition.face_encodings(image, face_locations)

    face_names = []
    for face_enc in face_encodings:
        matches = face_recognition.compare_faces(known_faces, face_enc)
        name = str(time())

        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
        else:
            known_faces.append(face_enc)
            known_names.append(name)

    return face_names

def mark_faces(image, show_names=False):
    small_image = cv2.resize(image, (0,0), fx=0.25, fy=0.25)
    face_locations = face_recognition.face_locations(image)

    # Draw a box around the face
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(image, (left, top), (right, bottom), (33, 33, 255), 2)

    if show_names:
        face_names = get_names(image, face_locations)
        # Draw a label with a name below the face
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    return image

