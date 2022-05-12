# python3

import argparse
import time
import numpy as np

import cv2
from threading import Thread

from tflite_runtime.interpreter import Interpreter

from gpiozero import Robot

class VideoStream:
    """Camera object that controls video streaming from Picamera"""
    def __init__(self,resolution=(640,480),framerate=30):
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])

        (self.grabbed, self.frame) = self.stream.read()

        self.stopped = False

    def start(self):
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                self.stram.release()
                return

            (self.grabbed,self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True

def load_labels(path):
    with open(path,'r') as f:
        return {i: line.strip() for i,line in enumerate(f.readlines())}

def set_input_tensor(interpreter,image):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:,:] = image

def classify_image(interpreter,image,top_k=1):
    set_input_tensor(interpreter,image)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))

    if output_details['dtype'] == np.uint8:
        scale, zero_point = output_details['quantization']
        output = scale * (output - zero_point)

    ordered = np.argpartition(-output,top_k)
    return [(i,output[i]) for i in ordered[:top_k]]

def main():
    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--model',help='File path of .tflite file.',required=True)
    parser.add_argument('--labels',help='File path of labels file.',required=True)
    args = parser.parse_args()

    labels = load_labels(args.labels)

    interpreter = Interpreter(args.model)
    interpreter.allocate_tensors()
    _,height,width,_ = interpreter.get_input_details()[0]['shape']

    botino = Robot(left=(5,6), right=(26,16))

    videostream = VideoStream(resolution=(640,480),framerate=30).start()
    time.sleep(1)

    while True:
        frame1 = videostream.read()

        frame = frame1.copy()
        frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width,height))
        input_data = np.expand_dims(frame_resized,axis=0)

        start_time = time.time()
        results = classify_image(interpreter,input_data)
        elapsed_ms = (time.time() - start_time) * 1000
        label_id,prob = results[0]

        label = '%s %.2f %.1fms' % (labels[label_id],prob, elapsed_ms)
        cv2.putText(frame,label,(5,30), cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)

        cv2.imshow('Object detector',frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

        if key == ord('w'):
            botino.forward(0.8)

        if key == ord('s'):
            botino.backward(0.8)

        if key == ord('a'):
            botino.left(0.8)

        if key == ord('d'):
            botino.right(0.8)

        if key == -1:
            # KEY RELEASED
            botino.stop()

    # Clean up
    cv2.destroyAllWindows()
    videostream.stop()

if __name__ == '__main__':
    main()

