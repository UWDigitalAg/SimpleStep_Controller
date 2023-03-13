from .periphery import Periphery, PeripheryException
# noinspection PyUnresolvedReferences
import pigpio
import os
import time

# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 20:56:24 2020

@author: Michael Beck
University of Winnipeg
"""


class PanTilt(Periphery):

    def __init__(self, name: str = 'PanTilt', max_pan: int = 2450,
                 min_pan: int = 600, max_tilt: int = 2300,
                 min_tilt: int = 1700):
        constants = {
            "pan_pin": 14,
            "tilt_pin": 15
        }
        # Speed: low numbers is quick, high are slow
        Periphery.__init__(self, name, {"max_pan": max_pan,
                                        "min_pan": min_pan,
                                        "max_tilt": max_tilt,
                                        "min_tilt": min_tilt,
                                        "speed": 0.003}, constants)
        self.logger.debug("Pan Tilt system booting")

        try:
            cmd_return = os.system("sudo pigpiod")
            self.logger.info("pigpiod ran with exit code {0}".
                             format(cmd_return))
            time.sleep(1)
            self.pi = pigpio.pi()
            if self.pi.connected:
                self.logger.info("GPIO initialized")
                self.initialize()
            else:
                raise PeripheryException
        except PeripheryException:
            self.logger.error("Failed to initialize GPIO")
            raise

    def initialize(self):
        """Setup PWM pins"""
        self.pi.set_servo_pulsewidth(self.constants["pan_pin"], 1525)
        self.pi.set_servo_pulsewidth(self.constants["tilt_pin"], 2050)

    def shutdown(self):
        # back to initial position
        self.pan_tilt(0, 0)
        self.pi.stop()
        os.system("sudo killall pigpiod")
        self.logger.info("stopping pigpiod ran with exit code {0}")

    def pan_tilt(self, pan: int, tilt: int):
        # convert angles to pulsewidths
        if -90.0 <= pan <= 90.0 and -25.0 <= tilt <= 35.0:
            pan_pulse = int(round(1525 + 925/90 * pan))
            tilt_pulse = int(round(2050 - 10 * tilt))
            self._pan(pan_pulse)
            self._tilt(tilt_pulse)
        else:
            self.logger.warning("Pan-tilt values out of bounds: " + str(pan) + ", " + str(tilt))

    def _pan(self, pan: int):
        """Pans to an angle given in pulse widths"""
        # TODO: Conversion into angles
        if pan < self.parameters['min_pan'] or pan > self.parameters['max_pan']:
            self.logger.warn("Pan angle given is out of bounds")
        else:
            old_pulse = self.pi.get_servo_pulsewidth(self.constants["pan_pin"])
            if old_pulse < pan:
                for i in range(pan - old_pulse):
                    self.pi.set_servo_pulsewidth(self.constants["pan_pin"], old_pulse+i)
                    time.sleep(self.parameters['speed'])
            else:
                for i in range(old_pulse - pan):
                    self.pi.set_servo_pulsewidth(self.constants["pan_pin"], old_pulse-i)
                    time.sleep(self.parameters['speed'])

    def _tilt(self, tilt: int):
        """Pans to an angle given in pulse widths"""
        # TODO: Conversion into angles
        if tilt < self.parameters['min_tilt'] or \
                tilt > self.parameters['max_tilt']:
            self.logger.warn("Tilt angle given is out of bounds")
        else:
            old_pulse = self.pi.get_servo_pulsewidth(self.constants['tilt_pin'])
            if old_pulse < tilt:
                for i in range(tilt - old_pulse):
                    self.pi.set_servo_pulsewidth(self.constants["tilt_pin"], old_pulse+i)
                    time.sleep(self.parameters['speed'])
            else:
                for i in range(old_pulse - tilt):
                    self.pi.set_servo_pulsewidth(self.constants["tilt_pin"], old_pulse-i)
                    time.sleep(self.parameters['speed'])
