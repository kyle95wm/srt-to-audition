from moviepy.editor import VideoFileClip
import pandas as pd
import re
from datetime import datetime, timedelta
import sys

# Function to convert time string to timedelta
def str_to_timedelta(time_str):
    return datetime.strptime(time_str, '%H:%M:%S,%f') - datetime(1900, 1, 1)

# Function to convert timedelta to SMPTE timecode (HH:MM:SS:FF)
def timedelta_to_smpte_timecode(t_delta, fps):
    total_seconds = int(t_delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    frames = int(((t_delta.total_seconds() - total_seconds) * fps))
    return f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"

# Function to extract frame rate from a video file
def get_frame_rate(video_file_path):
    with VideoFileClip(video_file_path) as clip:
        return clip.fps

def convert_srt_to_csv(srt_file_path, video_file_path):
    fps = get_frame_rate(video_file_path)
    csv_file_path = srt_file_path.replace('.srt', '.csv')

    with open(srt_file_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()

    entries = re.split(r'\n\n', srt_content.strip())
    csv_data = []
    for entry in entries:
        lines = entry.split('\n')
        if len(lines) >= 3:
            sequence = lines[0]
            times = re.split(r' --> ', lines[1])
            start_time = str_to_timedelta(times[0])
            end_time = str_to_timedelta(times[1])
            duration = end_time - start_time
            text = ' '.join(lines[2:]).replace('\n', ' ')
            csv_data.append({
                'Name': f'Marker {sequence}',
                'Start': timedelta_to_smpte_timecode(start_time, fps),
                'Duration': timedelta_to_smpte_timecode(duration, fps),
                'Time Format': f'{int(fps)} fps',
                'Type': 'Cue',
                'Description': text
            })

    csv_df = pd.DataFrame(csv_data)
    csv_df.to_csv(csv_file_path, index=False, sep='\t', header=True)
    print(f"Converted SRT file saved to {csv_file_path}")
    print(f"The frame rate of the video is: {fps} fps")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <source_srt_file_path> <source_video_file_path>")
    else:
        srt_file_path = sys.argv[1]
        video_file_path = sys.argv[2]
        convert_srt_to_csv(srt_file_path, video_file_path)
