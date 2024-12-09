"""Classes that encapsulate a single Stretchsense peripheral."""

from bluepy import btle
from abc import ABC
import numpy as np
from peripheral import stretchsense_delegate
from typing import Optional

class StretchSensePeripheral(btle.Peripheral, ABC):
    """An abstract class providing a blueprint for concrete peripherals.
    
    Args:
        address:
            A string representing the Bluetooth address of this Peripheral.

    Attributes:
        ACTIVE_SENSORS:
            A numpy array representing the sensors that represent each joint.
        NUM_SENSORS:
            An integer representing the number of sensors on the glove.
        SIDE:
            A string representing which hand the glove is for.
    """

    def __init__(self, address: str):
        super().__init__(address, "random")

        # Attributes
        self.ACTIVE_SENSORS: np.ndarray
        self.NUM_SENSORS: int
        self.SIDE: str

        # The peripheral's service uuid
        self._SERVICE_UUID: str

        # The delegate user to handle notifications from this peripheral
        self._delegate = stretchsense_delegate.StretchSenseDelegate()

        # Bluetooth address of this peripheral
        self._address: str = address

    def setup(self) -> None:
        """Sets up the glove for data collection."""

        print(f"connected to {self._address}")

        # Set up delegate
        self.withDelegate(self._delegate)

        # Getting the handle
        svc = self.getServiceByUUID(self._SERVICE_UUID)
        char = svc.getCharacteristics()[0]
        handle = char.valHandle

        # Turn on notifications
        self.writeCharacteristic(handle + 1, b'\x01\x00')

        # change sampling rate to 90Hz
        self.writeCharacteristic(29, b'\x5a')
        
    def read_sensors(self) -> Optional[np.ndarray]:
        """Gets a sample of capacitance data.

        Waits for the glove to send a sample of capacitance data with a timeout
        of 1 second. Then retrieves the capacitatance data from
        the delegate and returns it if it is a valid data set.

        Returns:
            A numpy array with n capacitance readings where n = the number of
            sensors on the glove or None.
        """

        if self.waitForNotifications(1.0):
            # Read capacitance values from delegate
            cap = self._delegate.capacitance

            # Return values if it has the correct dimensions
            if len(cap) == self.NUM_SENSORS:
                return cap
            else:
                print(f'Receiving {self.NUM_SENSORS} sensors but expects {len(cap)}.')
            
class RightStretchSenseGlove(StretchSensePeripheral):
    """Represents a particular right handed Stretchsense glove."""

    def __init__(self, address: str):
        super().__init__(address)

        # Set up constants
        self._SERVICE_UUID: str = '00001701-7374-7265-7563-6873656e7365'

        # Sensor reaction for 7 sensor glove; used by the author originally
        # self.ACTIVE_SENSORS: np.ndarray = np.array([
        #     [1, 1, 0, 1, 0, 0, 0, 0], # thumb yaw /splay
        #     [0, 1, 1, 1, 0, 0, 0, 0], # thumb pitch
        #     [0, 0, 0, 0, 1, 0, 0, 0], # index
        #     [0, 0, 0, 0, 0, 1, 0, 0], # middle
        #     [0, 0, 0, 0, 0, 0, 1, 0], # ring
        #     [0, 0, 0, 0, 0, 0, 0, 1]  # pinky
        # ])

        # Sensor reaction for 10 sensor glove; used by hiro
        # put your hand flat with palm facing up and middle finger pointing forward
        # x axis: along middle finger, from palm to the tip of the middle finger; roll defined about this axis
        # y axis: from palm to your right; pitch defined about this axis
        # z axis: from palm to the back of your hand, pointing vertically down; yaw defined about this axis
        self.ACTIVE_SENSORS: np.ndarray = np.array([
            [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], # thumb yaw
            [0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0], # thumb pitch
            [0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0], # index
            [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1], # middle
            [0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1], # ring
            [0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0]  # pinky
        ])
        
        self.NUM_SENSORS: int = 10
        self.SIDE: str = "right"


class LeftStretchSenseGlove(StretchSensePeripheral):
    """Represents a particular left handed Stretchsense glove."""

    def __init__(self, address: str, pkg_directory: str):
        super().__init__(address)

        # Set up constants
        self._SERVICE_UUID: str = '00001701-7374-7265-7563-6873656e7365'
        self.ACTIVE_SENSORS: np.ndarray = np.array([
            [1, 1, 0, 1, 0, 0, 0, 0], # thumb
            [0, 1, 1, 1, 0, 0, 0, 0], # thumb
            [0, 0, 0, 0, 1, 0, 0, 0], # index
            [0, 0, 0, 0, 0, 1, 0, 0], # middle
            [0, 0, 0, 0, 0, 0, 1, 0], # ring
            [0, 0, 0, 0, 0, 0, 0, 1]  # pinky
        ])
        self.NUM_SENSORS: int = 10
        self.SIDE: str = "left"