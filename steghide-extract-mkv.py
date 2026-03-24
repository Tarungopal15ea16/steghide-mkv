import cv2
import subprocess
import sys
from pathlib import Path
import os 
import tempfile
import math
import getpass


def first_frame(video,password):

    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None, None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Error: Could not read the first frame.")
        return  None,None

    with tempfile.TemporaryDirectory() as tmpdir:
        bmp_path = os.path.join(tmpdir, "first_frame.bmp")
        txt_path = os.path.join(tmpdir, "metadata.txt")
        
        cv2.imwrite(bmp_path, frame)

        cmd = ["steghide", "extract", "-sf", bmp_path, "-xf", txt_path, "-p", password, "-f"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Steghide extraction failed: {result.stderr}")
                return None,None
            if os.path.exists(txt_path):
                with open(txt_path, "r") as f:
                    lines = f.readlines()
                    var1 = lines[0].strip() if len(lines) > 0 else None
                    var2 = lines[1].strip() if len(lines) > 1 else None
                    
                    return var2,var1
                os.remove(txt_path)
                os.remove(bmp_path)
            else:
                print("Extraction command reported success, but file was not found ")
                return None,None 

        except Exception as e:
            print(f"An error occurred during extraction: {e}")
            return None,None 

def extract_all(video, password, extension,name):
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    combined_data = bytearray()
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    ret, _ = cap.read()
    print(f"Starting extraction of {total_frames - 1} data frames...")

    with tempfile.TemporaryDirectory() as tmpdir:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 1)
        count = 0
        i = 1
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_path = os.path.join(tmpdir, f"frame_{i}.bmp")
            chunk_path = os.path.join(tmpdir, f"{i}.bin")
            

            cv2.imwrite(frame_path, frame)


            cmd = ["steghide", "extract", "-sf", frame_path, "-xf", chunk_path, "-p", password, "-f"]
            
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0 and os.path.exists(chunk_path):

                with open(chunk_path, "rb") as chunk_file:
                    combined_data.extend(chunk_file.read())
                os.remove(chunk_path)

            if os.path.exists(frame_path):
                os.remove(frame_path)

            if True: 
                if i % (math.ceil(total_frames/40)) == 0:
                    count = count + 1
                progress_bar = f"[{'/' * count}{'.' * (40 - count)}{math.floor((i*100)/total_frames)}%]"
                status_text = f"{i}/{total_frames}"
                print(f"\033[1;32m{progress_bar}\033[0m", end='\r')
                i = i +1

    cap.release()

    output_name = f"{name}{extension}"
    with open(output_name, "wb") as f:
        f.write(combined_data)

    print(f"\n\nDone! File reconstructed as: {output_name}")
    print(f"Total size recovered: {len(combined_data)} bytes")





if len(sys.argv) > 1 and len(sys.argv) < 4 :
    path1 = Path(sys.argv[1])
    prefix = path1.name.split('.')[0]
    extenstion1 = path1.suffix.lower()
    size1 = os.path.getsize(sys.argv[1])
    if len(sys.argv) == 3 :
        path2 = Path(sys.argv[2])
        prefix = path2.name.split('.')[0]
        name = prefix
    else:
        name = "Extracted"
    if extenstion1 not in ['.mkv']:
        print("provide .mkv format video")
    else:
        password = getpass.getpass("Enter Password to Decrypt:")
        extension,Name = first_frame(sys.argv[1],password)
        if extension is None or Name is None:  
            print("Incorrect password or File is corrupted")
        else:
            if name != "Extracted":
                extract_all(sys.argv[1],password,extension,name)
            else:
                extract_all(sys.argv[1],password,extension,Name)
else: 
    print("extract takes only one aurgument[video.mkv]")


