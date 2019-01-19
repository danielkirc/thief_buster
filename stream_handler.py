#!/usr/bin/env python3
import cv2
from threading import Thread
from face_detect import mark_faces

# Show time taken
from time import time

class StreamHandler:
    def __init__(self, path):
        self.stopped = False
        self.stream = cv2.VideoCapture(path)

        # Make sure no read errors occur before 1st shot is taken
        # After thread is started should contain latest image
        self.last_frame = self.get_latest_frame()

    def start(self):
        t = Thread(target=self.update)
        t.daemon = True
        t.start()
        return self

    def stop(self):
        self.stopped = True

    def read(self):
        return self.last_frame

    # Called internally
    def update(self):
        while not self.stopped:
            start_time = time()

            img = self.get_latest_frame()
            img = mark_faces(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.last_frame = img

            print("StreamHandler update took: ", time() - start_time)

    # Used in update and to get sample
    def get_latest_frame(self):
        # Next frame to get is the latest
        #self.stream.set(1, 1)

        # Empty old frames
        for i in range(5):
            ret, img = self.stream.read()
        if ret:
            return img
        else:
            self.stop()

# Debug
if __name__ == "__main__":
    from credentials import remote_server as v_source
    from time import sleep
    stream = StreamHandler(v_source)
    stream.start()
    while True:
        sleep(1)
