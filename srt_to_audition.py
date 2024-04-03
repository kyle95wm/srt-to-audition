import sys
import os
from moviepy.editor import VideoFileClip
import pandas as pd
import re
from datetime import datetime, timedelta

# Convert a time string into a timedelta object
def str_to_timedelta(time_str):
    return datetime.strptime(time_str, '%H:%M:%S,%f') - datetime(1900, 1, 1)

# Convert a timedelta object to SMPTE timecode format
def timedelta_to_smpte_timecode(t_delta, fps):
    total_seconds = int(t_delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    frames = int(((t_delta.total_seconds() - total_seconds) * fps))
    return f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"

# Extract the frame rate from the given video file
def get_frame_rate(video_file_path):
    try:
        with VideoFileClip(video_file_path) as clip:
            return clip.fps
    except Exception as e:
        print(f"Error extracting frame rate from video: {e}")
        sys.exit(1)

# Main function to convert SRT to CSV format
def convert_srt_to_csv(srt_file_path, video_file_path):
    # Check if the provided SRT and video file paths exist
    if not os.path.exists(srt_file_path):
        print(f"The SRT file does not exist: {srt_file_path}")
        sys.exit(1)
    if not os.path.exists(video_file_path):
        print(f"The video file does not exist: {video_file_path}")
        sys.exit(1)

    # Get the frame rate from the video file
    fps = get_frame_rate(video_file_path)
    # Define the output CSV file path
    csv_file_path = srt_file_path.replace('.srt', '.csv')

    try:
        # Read the SRT file content
        with open(srt_file_path, 'r', encoding='utf-8') as file:
            srt_content = file.read()
    except Exception as e:
        print(f"Error reading SRT file: {e}")
        sys.exit(1)

    try:
        # Process the SRT content and generate CSV data
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
                # Populate the CSV data dictionary
                csv_data.append({
                    'Name': text,
                    'Start': timedelta_to_smpte_timecode(start_time, fps),
                    'Duration': timedelta_to_smpte_timecode(duration, fps),
                    'Time Format': f'{fps} fps',
                    'Type': 'Cue',
                    'Description': ''  # Description remains empty
                })
        # Write the CSV data to a file
        pd.DataFrame(csv_data).to_csv(csv_file_path, index=False, sep='\t', header=True)
        print(f"Converted SRT file saved to {csv_file_path}")
        print(f"The frame rate of the video is: {fps} fps")
    except Exception as e:
        print(f"Error processing SRT file: {e}")
        sys.exit(1)

# Function to get user input with a prompt
def get_user_input(prompt):
    return input(prompt)

# Main entry point of the script
if __name__ == "__main__":
    if len(sys.argv) == 3:
        # Use command-line arguments if provided
        srt_file_path = sys.argv[1]
        video_file_path = sys.argv[2]
    else:
        # Enter interactive mode if command-line arguments are not provided
        print("You did not provide the required SRT and video file paths.")
        srt_file_path = get_user_input("Please enter the full path to the SRT file: ")
        video_file_path = get_user_input("Please enter the full path to the video file: ")

    # Call the main conversion function with the provided paths
    convert_srt_to_csv(srt_file_path, video_file_path)
