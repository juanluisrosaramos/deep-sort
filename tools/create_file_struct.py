# vim: expandtab:ts=4:sw=4
import os
import errno
import argparse
import numpy as np
import cv2
import time

from threading import Thread
from queue import Queue

def save_image(src, path,image_id, image_ext="jpg", jpg_quality=None, png_compression=None):

    filename = f"{image_id}.{image_ext}" 
    path = os.path.join(path, filename)
    #TODO check if path exists    
    if image_ext == "jpg":    
        cv2.imwrite(path, src,
                    (cv2.IMWRITE_JPEG_QUALITY, jpg_quality) if jpg_quality else None)
    elif image_ext == "png":        
        cv2.imwrite(path, src,
                    (cv2.IMWRITE_PNG_COMPRESSION, png_compression) if png_compression else None)
    else:
        raise Exception("Unsupported image format")

        #return data

def create_file_structure(name_dir,path="."):
    """Create file structure followin MotChanllenge recomendations
    name
        -.
            ├── det
            │   └── det.txt
            ├── img1
            │   ├── 000001.jpg
            ├── MOT16-03-raw.webm
            └── seqinfo.ini

    Parameters
    ----------
    name : str
        Name of the main folder
    path : str
        Main path with input videos
    """    
    try:
        name_dir = os.path.join(path, name_dir)
        det_dir = os.path.join(name_dir, 'det')
        images_dir = os.path.join(name_dir, 'img1')
        os.makedirs(images_dir)
        os.makedirs(det_dir)
    except OSError as exception:
        if exception.errno == errno.EEXIST and os.path.isdir(name_dir):
            pass
        else:
            raise ValueError(
                "Failed to created output directory '%s'" % name_dir)
    return images_dir

def create_frames(input_video,path="."):
    """Create frames of the detections input video
   

    Parameters
    ----------
    input_video : str
        Name of the input file
    dir_name : str
        path to save frames images
    """
    cap = cv2.VideoCapture(input_video)       
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    #TODO get detections size from the model cfg
    frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    frame_num = 0
    while cap.isOpened():
            success,image = cap.read()
            if success == False:
                break
            #image = cap.read()
            image_id = f"{frame_num:06d}"            
            #filename = os.path.join(path,image_id)
            frame_num += 1             
            save_image(image, path,image_id)
            print(frame_num)           
            

def parse_args():
    """Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Create file structure as MotChallenge")
    parser.add_argument(
        "-video",
        default="",
        help="Path to video input.")
    parser.add_argument(
        "-detection", help="Path to detections file"
        "standard MOT detections Directory structure file from detectron2-pipeline "
        "MOTChallenge structure: [sequence]/det/det.txt", default=None)
    parser.add_argument(
        "-name", help="Input directory. Will be created if it does not"
        " exist.", default="detections")
    parser.add_argument(
        "-path", help="Path with input videos files"
        " exist.", default=".")
    
    return parser.parse_args()


def main():
    """
    python tools/create_file_struct.py -video /media/juanluis/data1/mapubli/videos/gente3.mp4 
    -detection ~/workingrrr/mapubli/detectron2-pipeline/predictions.txt 
    -name test -path /media/juanluis/data1/mapubli/videos/
    """
    args = parse_args()
    directory = create_file_structure(args.name, args.path)
    frames = create_frames(args.video,directory)

if __name__ == "__main__":
    main()
