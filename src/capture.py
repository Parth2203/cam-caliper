import queue
import threading
import time
import cv2
import numpy as np


class CameraThread:
    camera_source = 0
    camera_width = 1920
    camera_height = 1080
    camera_frame_rate = 30
    camera_fourcc = cv2.VideoWriter_fourcc(*"MJPG")

    buffer_length = 5
    buffer_all = False

    camera = None
    camera_init = 0.5

    buffer = None

    frame_grab_run = False
    frame_grab_on = False

    frame_count = 0
    frames_returned = 0
    current_frame_rate = 0
    loop_start_time = 0

    def start(self):

        if self.buffer_all:
            self.buffer = queue.Queue(self.buffer_length)
        else:

            self.buffer = queue.Queue(1)

        self.camera = cv2.VideoCapture(self.camera_source)
        self.camera.set(3, self.camera_width)
        self.camera.set(4, self.camera_height)
        self.camera.set(5, self.camera_frame_rate)
        self.camera.set(6, self.camera_fourcc)
        time.sleep(self.camera_init)

        self.camera_width = int(self.camera.get(3))
        self.camera_height = int(self.camera.get(4))
        self.camera_frame_rate = int(self.camera.get(5))
        self.camera_mode = int(self.camera.get(6))
        self.camera_area = self.camera_width * self.camera_height

        self.black_frame = np.zeros((self.camera_height, self.camera_width, 3), np.uint8)

        self.frame_grab_run = True

        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def stop(self):

        self.frame_grab_run = False

        while self.frame_grab_on:
            time.sleep(0.1)

        if self.camera:
            try:
                self.camera.release()
            except:
                pass
        self.camera = None

        self.buffer = None

    def loop(self):

        frame = self.black_frame
        if not self.buffer.full():
            self.buffer.put(frame, False)

        self.frame_grab_on = True
        self.loop_start_time = time.time()

        fc = 0
        t1 = time.time()

        while 1:

            if not self.frame_grab_run:
                break

            if self.buffer_all:

                if self.buffer.full():
                    time.sleep(1 / self.camera_frame_rate)

                else:

                    grabbed, frame = self.camera.read()

                    if not grabbed:
                        break

                    self.buffer.put(frame, False)
                    self.frame_count += 1
                    fc += 1

            else:

                grabbed, frame = self.camera.read()
                if not grabbed:
                    break

                if self.buffer.full():
                    self.buffer.get()

                self.buffer.put(frame, False)
                self.frame_count += 1
                fc += 1

            if fc >= 10:
                self.current_frame_rate = round(fc / (time.time() - t1), 2)
                fc = 0
                t1 = time.time()

        self.loop_start_time = 0
        self.frame_grab_on = False
        self.stop()

    def next(self, black=True, wait=0):

        if black:
            frame = self.black_frame

        else:
            frame = None

        try:
            frame = self.buffer.get(timeout=wait)
            self.frames_returned += 1
        except queue.Empty:
            pass

        return frame
