from enum import Enum


class Urgency(Enum):
    CRITICAL = "Critical"
    MAJOR    = "Major"
    MEDIUM   = "Medium"
    MINOR    = "Minor"
    IGNORE   = ""



class Detections(Enum):
    VOID = 1

    DYNAMIC_UNKNOWN = 2
    VEHICLE = 3
    PERSON = 4

    OBSTRUCTION = 5

    BLUE = 3



labels_map: dict = {
    (0,  0,  0):            Detections.VOID,
    (111, 74,  0):          Detections.DYNAMIC_UNKNOWN,
    (81,  0, 81):           'ground',
    (129, 64, 129):         'road',                 # Changed
    (244, 35, 232):         'sidewalk',
    (250, 170, 160):        'parking',
    (230, 150, 140):        'rail track',
    (70, 70, 70):           Detections.OBSTRUCTION,
    (102, 102, 156):        Detections.OBSTRUCTION,
    (190, 153, 153):        Detections.OBSTRUCTION,
    (180, 165, 180):        Detections.OBSTRUCTION,
    (150, 100, 100):        'bridge',
    (150, 120, 90):         'tunnel',
    (153, 153, 153):        'pole',
    (153, 153, 153):        'polegroup',
    (250, 170, 30):         'traffic light',
    (220, 220,  0):         'traffic sign',
    (107, 142, 35):         'vegetation',
    (152, 251, 152):        'terrain',
    (70, 130, 180):         'sky',
    (220, 20, 60):          Detections.PERSON,
    (255,  0,  0):          'rider',
    (0,  0, 142):           Detections.VEHICLE,
    (0,  0, 70):            Detections.VEHICLE,
    (0, 60, 100):           Detections.VEHICLE,
    (0,  0, 90):            Detections.VEHICLE,
    (0,  0, 110):           Detections.VEHICLE,
    (0, 80, 100):           Detections.VEHICLE,
    (0,  0, 230):           Detections.VEHICLE,
    (119, 11, 32):          Detections.VEHICLE,
    (0,  0, 142):           'license plate'
}