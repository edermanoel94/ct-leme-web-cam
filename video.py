import time

import cv2
import numpy.random

numpy.random.seed(int(time.time()))


class Video:
    def __init__(self):
        self.video = cv2.VideoCapture('http://187.111.99.18:9004/?CODE=1178')
        self.net = cv2.dnn.readNet("resources/models/yolov4-tiny/yolov4-tiny.weights",
                                   "resources/models/yolov4-tiny/yolov4-tiny.cfg")

        self.model = cv2.dnn_DetectionModel(self.net)
        self.model.setInputParams(size=(854, 480), scale=1 / 255)

        self.classes = []
        self.blacklist_classes = ['scissors', 'knife']

        # Setting classes to list
        with open("resources/models/yolov4-tiny/classes.txt") as f:
            for names in f.readlines():
                self.classes.append(names.strip())

        self.colors = numpy.random.uniform(0, 255, size=(len(self.classes), 3))

    def __del__(self):
        self.video.release()

    def found_suspect_objs(self, class_name):
        try:
            if self.blacklist_classes.index(class_name) > 0:
                return True
        except ValueError:
            return False

    def get_frame(self):
        ret, frame = self.video.read()

        (class_ids, scores, bboxes) = self.model.detect(frame)

        for class_id, score, bbox in zip(class_ids, scores, bboxes):
            (x, y, w, h) = bbox
            class_name = self.classes[class_id]

            cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, self.colors[class_id], 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), self.colors[class_id], 3)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
