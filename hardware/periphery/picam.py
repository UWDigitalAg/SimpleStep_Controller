from picamera import PiCamera
from .periphery import Periphery
import io
import numpy as np
import cv2

# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 20:56:24 2020

@author: Michael Beck
University of Winnipeg
"""

"""
Controls the Pi-camera module
"""


class Camera(PiCamera, Periphery):

    def __init__(self, name: str = 'PiCam'):
        PiCamera.__init__(self)
        Periphery.__init__(self, name)

        self.logger.debug('Camera booting')

    def __enter__(self):
        self.logger.debug("Camera connected")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.debug("Disconnecting camera...")
        self.shutdown()

    def initialize(self):
        # TODO: Set camera settings, cooldown to adjust to light levels
        pass

    def shutdown(self):
        # PiCamera close command
        self.close()

    def trigger(self):
        """Convenience method to take a picture as an OpenCV object"""
        # Capture into byte-stream
        stream = io.BytesIO()
        self.capture(stream, format='jpeg')
        # Construct numpy array from stream
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)

        # 'decode' the image from the array, preserving color
        image = cv2.imdecode(data, 1)
        # OpenCV returns an array with data in BGR order. Switch it to RGB
        image = image[:, :, ::-1]
        return image

    @staticmethod
    def trigger_to_file(filepath: str = 'testimage.jpg'):
        camera.capture(filepath)