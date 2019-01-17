#!/usr/bin/env python
import face_recognition
import cv2

# Video source
# remote_server, android, webcam
from credentials import webcam as video_source

def main():
    # TODO: Save / restore from file
    known_face_encodings = []
    known_names = []

    # Temporary holders updated per frame
    face_locations = []
    face_encodings = []
    face_names = []
    face_save_count = 0

    # Process every other frame
    process_this_frame = True

    video_capture = cv2.VideoCapture(video_source)
    while True:
        ret, img = video_capture.read()
        cv2.resize(img, (0,0), fx=0.25, fy=0.25)

        process_this_frame = not process_this_frame
        if process_this_frame:
            face_locations = face_recognition.face_locations(img)
            face_encodings = face_recognition.face_encodings(img, face_locations)
                                                                                              
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                                                                                              
                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_names[first_match_index]
                else:
                    face_save_count+=1
                    name = "Face#{0}".format(face_save_count)
                    known_face_encodings.append(face_encoding)
                    known_names.append(name)
                
                face_names.append(name)

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            #top *= 4
            #right *= 4
            #bottom *= 4
            #left *= 4

            # Draw a box around the face
            cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow("Video", img)

        # Hit 'q' on the keyboard to quit!
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('p'):
            print(known_names)

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

