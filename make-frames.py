import cv2
import numpy as np
from PIL import Image, ImageDraw
import os
import glob

from utils.myEnums import labels_map, Detections, Urgency


def getFirstFrame(video_file: str):
    vidcap = cv2.VideoCapture(video_file)
    success, image = vidcap.read()
    if not success:
        raise Exception("MP4 file or its first frame not found")
    return image

# frame        -> whole array of current image
# arr_to_check -> the only part of frame[] to check for obstructions
def hasNoObstruction(arr_to_check: np.ndarray, frame: np.ndarray, urgency_level: Urgency) -> bool:
    for row in arr_to_check:
        for pixel in row:
            pixel = tuple(pixel)

            if pixel in labels_map and labels_map[pixel] != "road":
                # print(f"EMERGENCY - Non-road at: {pixel}")
                if urgency_level != Urgency.IGNORE:
                    cv2.putText(frame, f"{urgency_level.value} - Non-road", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, 1)
                return False

    return True



def main(args):
    # Clear the 'temp_vid' folder
    files = glob.glob('temp_vid/*')
    for f in files:
        os.remove(f)

    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    video_file = args["src"]
    first_frame = getFirstFrame(video_file)

    height, width, _ = first_frame.shape
    print(height, width)

    # CONSTANTS
    NUM_SECTORS = 15  # Number of width sectors
    MIDDLE_SECTOR = NUM_SECTORS // 2  # Index of middle sector
    WIDTH_SECTOR = width // NUM_SECTORS  # Width (pixels) of a single sector

    TEMP_VID_DIR = "temp_vid"                   # Path of 'temp_vid' directory (used to store frames of video)
    OUTPUT_FRAME_NAME = "output_img.png"

    counter = 0  # Counter for each frame

    cap = cv2.VideoCapture('input_vid.mp4')

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    # Read until video is completed
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        # TODO: Check the whole column for vehicles but not other pedestrians
        if hasNoObstruction(frame[height - 1: height, WIDTH_SECTOR * MIDDLE_SECTOR: WIDTH_SECTOR * 8], frame,
                            Urgency.CRITICAL) \
                and hasNoObstruction(frame[height - 100: height - 1, WIDTH_SECTOR * MIDDLE_SECTOR: WIDTH_SECTOR * 8],
                                     frame, Urgency.MAJOR):
            cv2.putText(frame, "No obstruction", (10, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, 1)

        else:
            index = 0
            while index < NUM_SECTORS + 1:
                if hasNoObstruction(frame[height - 100: height,
                                    WIDTH_SECTOR * (MIDDLE_SECTOR + index): WIDTH_SECTOR * (MIDDLE_SECTOR + index + 1)],
                                    frame, Urgency.IGNORE):
                    cv2.putText(frame, f"Move right by {index} steps", (10, 500), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (255, 255, 255), 1, 1)
                    break
                elif hasNoObstruction(frame[height - 100: height,
                                      WIDTH_SECTOR * (MIDDLE_SECTOR - index): WIDTH_SECTOR * (
                                              MIDDLE_SECTOR + index + 1)], frame, Urgency.IGNORE):
                    cv2.putText(frame, f"Move left by {index} steps", (10, 500), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (255, 255, 255), 1, 1)
                    break
                index += 1

            else:
                cv2.putText(frame, "Forward path completely blocked", (10, 500), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 255, 255), 1, 1)

        cv2.imwrite(f"temp_vid/{counter:08}_{OUTPUT_FRAME_NAME}", frame)
        counter += 1

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help="Source location")
    parser.add_argument("dest", help="Destination location")
    args = parser.parse_args()

    config = vars(args)
    main(config)