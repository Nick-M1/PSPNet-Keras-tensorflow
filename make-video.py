import argparse
from os import listdir
from os.path import isfile, join

import skvideo.io
import cv2
import numpy as np

def main(args):
    TEMP_VID_DIR = "PART_2-Vids/Temp-frames"    # Path of 'temp_vid' directory (used to store frames of video)
    INPUT_FRAME_NAME = "output_img.png"         # Input - lots of frame images
    OUTPUT_VIDEO_NAME = f"PART_2-Vids/Outputs/{args['output_file_name']}"        # Output - a single mp4 video

    directory_list = listdir(TEMP_VID_DIR)

    num_frames = len([name for name in directory_list if isfile(join(TEMP_VID_DIR, name))])
    print(f"Number of frames in folder: {num_frames}")

    first_frame = cv2.imread(f'{TEMP_VID_DIR}/00000000_{INPUT_FRAME_NAME}', cv2.IMREAD_GRAYSCALE)

    out_video = np.empty([num_frames, first_frame.shape[0], first_frame.shape[1], 3], dtype=np.uint8)
    out_video = out_video.astype(np.uint8)

    for frame in range(num_frames - 1):
        out_video[frame] = cv2.imread(f"{TEMP_VID_DIR}/{frame:08d}_{INPUT_FRAME_NAME}")

    # Writes the output image sequences in a video file
    skvideo.io.vwrite(OUTPUT_VIDEO_NAME, out_video)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_video_name", help="Output file name", default="output_vid.mp4")
    args = parser.parse_args()

    config = vars(args)
    main(config)