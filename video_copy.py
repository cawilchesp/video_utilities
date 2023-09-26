import supervision as sv
import cv2

from tqdm import tqdm
import threading
from pathlib import Path

from print_info import print_video_info


def process_video(source, video_fps) -> None:
    target = f"{Path(source).parent}/{Path(source).stem}.avi"
    
    frame_generator = sv.get_video_frames_generator(source_path=source)
    video_info = sv.VideoInfo.from_video_path(video_path=source)
    video_info.fps = video_fps

    print_video_info(source, video_info)

    with sv.VideoSink(target_path=target, video_info=video_info) as sink:
        for frame in tqdm(frame_generator, total=video_info.total_frames, unit='frames'):
            sink.write_frame(frame=frame)

            # cv2.namedWindow('output', cv2.WINDOW_KEEPRATIO)
            # cv2.imshow('output', frame)
            # cv2.resizeWindow('output', 1280, 720)
            
            # # Stop if Esc key is pressed
            # if cv2.waitKey(1) & 0xFF == 27:
            #     break


if __name__ == "__main__":
    file_list = {
        1: ('D:/Data/CCT/CCT_P8_50m_60fps_030823.mp4', 59.94),
        # 2: ('D:/Data/video_2.avi', 30),
        # 3: ('D:/Data/video_3.avi', 29.97),
        # 4: ('D:/Data/video_4.mp4', 29.97)
    }

    threads = []
    for file in file_list.values():
        # Create the tracker threads
        threads.append(threading.Thread(target=process_video, args=file, daemon=True))
        
        # Start the tracker threads
        threads[-1].start()

    for thread in threads:
        # Wait for the tracker threads to finish
        thread.join()