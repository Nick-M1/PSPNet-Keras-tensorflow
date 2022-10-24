import argparse
from os import listdir
from os.path import isfile, join

import skvideo.io
import cv2
import numpy as np

def main(args):
    directory_list = sorted(listdir(args.input_path))

    num_frames = len([name for name in directory_list if isfile(join(args.input_path, name))])
    print(f"Number of frames in folder: {num_frames}")

    any_frame_name = directory_list[0]
    any_frame = cv2.imread(f'{args.input_path}/{any_frame_name}', cv2.IMREAD_GRAYSCALE)

    out_video = np.empty([num_frames, any_frame.shape[0], any_frame.shape[1], 3], dtype=np.uint8)
    out_video = out_video.astype(np.uint8)

    for idx, frame_name in enumerate(directory_list):
        out_video[idx] = cv2.imread(f"{args.input_path}/{frame_name}")

    # Writes the output image sequences in a video file
    skvideo.io.vwrite(args.output_video_name, out_video)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help="Path of frames directory", default="PART_1-Vids/Temp-frames/Seg-files")
    parser.add_argument("-o", "--output_video_name", help="Output file path + name", default="PART_1-Vids/Outputs/output_vid.mp4")

    args = parser.parse_args()
    main(args)