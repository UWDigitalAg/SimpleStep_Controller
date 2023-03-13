import json
import logging
from typing import List

from .periphery.periphery import Periphery
from .periphery.picam import Camera

# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 20:56:24 2020

@author: Michael Beck
University of Winnipeg
"""

"""
Module controlling the periphery

Provide an API for User Interfaces
Load and access periphery (Linear Actuator, PiCam, pan-tilt system)
Manage config files for peripheries

:raises InitializeException: When connection to one periphery fails 
"""


class InitializeException(Exception):
    pass


class Wormbot:

    def __init__(self, config: str = None):
        self.logger = logging.getLogger('MainLogger.EAGL-I')
        self.logger.info("Booting systems...")

        """Initialize periphery"""
        self.camera = Periphery("DummyCamera", {})

        try:
            try:
                self.camera = Camera()
                self.logger.info("Camera connected")
            except Exception as e:
                self.logger.error("Failed to connect to camera")
                raise InitializeException from e
        except InitializeException:
            self.logger.info("Shut down and disconnect peripheries")
            self.camera.shutdown()
            del self.camera

        self.peripheries = {
                           'camera': self.camera
                           }

        for name, per in self.peripheries.items():
            per.initialize()

        if config is not None:
            self.read_config(config)
        else:
            self.read_config('default.config')

    def __enter__(self):
        self.logger.info("Booting complete")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info("Shutting down systems...")
        self.shutdown()

    def shutdown(self):
        """Bring peripheries to state from which they can be started again"""
        self.logger.debug("Shut down all peripheries")
        for name, per in self.peripheries.items():
            per.shutdown()

    # Read/Write configuration files
    def read_config(self, path: str) -> bool:
        """Read and set parameters from a config file, return success"""
        try:
            with open(path, 'r') as f:
                parameters = json.load(f)
        except OSError as err:
            self.logger.error("Cannot read parameter file")
            self.logger.error(str(err))
            return False
        # Create backup from current settings
        if path != 'backup.config':
            self.write_config('backup.config')

        success = True
        for per_name, per in self.peripheries.items():
            for par in [p for p in parameters if p[0] == per_name]:
                success = success and per.set_par(par[1], par[2])
        if not success and path != 'backup.config':
            self.logger.warning("One or more parameters were not set. "
                                "Returning to original parameter settings.")
            self.read_config('backup.config')
        elif not success:
            self.logger.error("Not able to return to backup parameters. "
                              "System is in unknown state!")
        return success

    def write_config(self, path: str) -> bool:
        """Write parameters from periphery to path, return success"""
        parameter_lines = []
        success = True
        for per_name, per in self.peripheries.items():
            for par_name, par in per.get_par().items():
                parameter_lines.append([per_name, par_name, par])
        # Format a human-readable dump
        dump = '[\n'
        for line in parameter_lines[:-1]:
            dump = dump + json.dumps(line) + ',\n'
        dump = dump + json.dumps(parameter_lines[-1]) + '\n]'

        try:
            with open(path, 'w') as f:
                f.write(dump)
        except OSError:
            self.logger.error("Cannot write parameters", exc_info=True)
            success = False
        return success

    # TODO: Convenience methods to access functionality of 2 or more systems

    def trigger_at(self, target_pose: List[float]):
        # TODO implement function
        pass
