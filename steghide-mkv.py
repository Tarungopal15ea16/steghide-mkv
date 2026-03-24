import cv2
import subprocess
import sys
from pathlib import Path
import os 
import tempfile
import math
import getpass

def hide_split(file, frames, size):
    chunk_size = math.ceil(size / (frames - 1))
    temp_paths = [' ']
    
    with open(file, "rb") as f:
        for i in range(1, frames):
            fd, path = tempfile.mkstemp(prefix=f"chunk_{i}_", suffix=".bin")
            os.close(fd)
            
            chunk_data = f.read(chunk_size)
            if not chunk_data: 
                break
                
            with open(path, "wb") as chunk_file:
                chunk_file.write(chunk_data)
            temp_paths.append(path)
            
    return temp_paths

def credentials(Name, extension):
    fs, path = tempfile.mkstemp(prefix="credentials_", suffix=".txt")
    os.close(fs)
    with open(path, "w") as cred:
        cred.write(f"{password}\n{extension}")
    return path

def embid(temp_files, main_file, video, frames, password,name):
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    out = cv2.VideoWriter(name + '.mkv',cv2.CAP_FFMPEG,fourcc, fps, (width, height))
    
    print(f"Starting embedding process across {frames} frames...")
    count = 0
    for i in range(0, frames):
        ret, frame = cap.read()
        if not ret:
            break
            
        fi, path = tempfile.mkstemp(prefix=f"frame_{i}_", suffix=".bmp")
        os.close(fi)
        cv2.imwrite(path, frame)
        
        
        if i == 0:
            file_to_hide = main_file 
            cmd = ["steghide", "embed", "-cf", path, "-ef", file_to_hide, "-p", password, "-f"]

        elif i < len(temp_files):
            file_to_hide = temp_files[i]
            cmd = ["steghide", "embed", "-cf", path, "-ef", file_to_hide, "-p", password, "-f"]
        else:
            out.write(frame)
            del frame
            if i % (math.ceil(frames/40)) == 0:
                count = count + 1
            progress_bar = f"[{'/' * count}{'.' * (40 - count)}{math.floor((i*100)/frames)}%]"
            status_text = f"{i}/{frames}"
            print(f"\033[1;32m{progress_bar}\033[0m", end='\r')
            continue
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Steghide Error at frame {i}: {result.stderr}")
            else:
                stealth_frame = cv2.imread(path)
                out.write(stealth_frame)
                del stealth_frame
                
                if True: 
                    if i % (math.ceil(frames/40)) == 0:
                        count = count + 1
                    progress_bar = f"[{'/' * count}{'.' * (40 - count)}{math.floor((i*100)/frames)}%]"
                    status_text = f"{i}/{frames}"
                    print(f"\033[1;32m{progress_bar}\033[0m", end='\r')
            os.remove(file_to_hide)            
        except subprocess.TimeoutExpired:
            print(f"Timeout at frame {i}")
            break
            
        if os.path.exists(path):
            os.remove(path)


    cap.release()
    out.release()
    
    if os.path.exists(main_file):
        os.remove(main_file)
    for chunk in temp_files:
        if os.path.exists(chunk):
            os.remove(chunk)

    print(f"Success! Lossless mkv created as {name + '.mkv'}")
    return None 

if len(sys.argv) < 5 and len(sys.argv) > 2:
    path1 = Path(sys.argv[1]) 
    path2 = Path(sys.argv[2])
    if len(sys.argv) == 4 :
        path3 = Path(sys.argv[3])
        prefix = path3.name.split('.')[0]
        name = prefix
    else:
        prefix = path1.name.split('.')[0]
        name = prefix
    prefix2 = path2.name.split('.')[0]
    extenstion1 = path1.suffix.lower()
    extenstion2 = path2.suffix.lower() 
    Name = name + '_.mpv'
    size1 = os.path.getsize(sys.argv[1])
    size2 = os.path.getsize(sys.argv[2])
    
    if extenstion1 in ['.mp4','.mov','.mkv','.avi','.webm','.wmv','.flv','.avchd','.3gp']:

        if True:
            print("Calculating total frames...")
            frame_count = 0
            cap = cv2.VideoCapture(sys.argv[1])
            while cap.isOpened():
                ret, frame = cap.read()
                
                if not ret:
                    break
                frame_count += 1
            h = cap.get(4)
            w = cap.get(3)
            cap.release()
            #
            if (h*w/10) >= (size2/(frame_count-1)):
                if frame_count <= 1:
                    print("Error: Video is too short to hide data.")
                    sys.exit()
                password = getpass.getpass("Enter password to encrypt: ")
                print(f"Splitting secret data into {frame_count - 1} chunks...")
                temp_files = hide_split(sys.argv[2], frame_count, size2)
                credential = credentials(prefix2, extenstion2)
                
                embid(temp_files, credential, sys.argv[1], frame_count, password,name)
            else:
                print("File Size is too large to hide in this video.")
                print("Try using a larger Video File.")
    else:
        print("No Video file Submitted")
        print("Format: python steghide-mp4.py [video_file] [file_to_hide]")
else:
    print("steghide-mp4.py needs exactly two arguments.")
    print("Format: steghide-mkv embed [video_file] [file_to_hide]")
