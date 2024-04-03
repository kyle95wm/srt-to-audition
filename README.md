# SRT-to-CSV Converter for Adobe Audition

This script, `srt_to_audition.py`, converts SRT subtitle files into CSV format compatible with Adobe Audition's markers. It uses the video file's frame rate to ensure accurate synchronization of markers.

This script is intended to be used in the realm of Audio Description mixing, where the SRT file is the AD script. The video file is used in order to properly align the AD cues along the timeline. Feel free to adapt this script for your purposes.

## Features

- **Frame Rate Synchronization**: Uses the video file's frame rate to accurately align subtitles with the timeline in Adobe Audition.
- **Interactive Mode**: If no arguments are provided, the script will interactively ask for the necessary file paths.
- **Indicator Processing**: Detects and processes cues with indicators like [FAST] or [FAST-ish], separating them into the "Description" field for enhanced cue context.
- **Error Handling**: Includes basic error checking for file existence and permissions, ensuring a smooth and informative user experience.
- **Easy to Use**: Simple command-line execution with clear instructions for both technical and non-technical users.
- **Customizable Output**: Generates a CSV file that can be easily imported into Adobe Audition, with options to modify script behavior to fit various workflows.

## Prerequisites

- Python 3.x: Ensure Python is installed on your system.
- `moviepy` library: Used for extracting frame rate from the video file. Install with `pip install moviepy` or `pip3 install moviepy`.
- `pandas` library: Used for data manipulation and CSV operations. Install with `pip install pandas` or `pip3 install pandas`.

Note: Installing `moviepy` will also handle the installation of `ffmpeg`, which is required for video file processing.

## Usage

1. Clone the repository or download the script `srt_to_audition.py`.
2. Ensure Python 3.x is installed on your system.
3. Install `moviepy` and `pandas` using `pip install moviepy pandas` or `pip3 install moviepy pandas`.
4. Run the script using the command:
   - If your system uses the `python` command: `python srt_to_audition.py <path_to_srt_file> <path_to_video_file>`
   - If your system uses the `python3` command: `python3 srt_to_audition.py <path_to_srt_file> <path_to_video_file>`

The script will generate a CSV file in the same directory as the SRT file, named after the SRT file with a `.csv` extension.

## Contributing

Contributions are welcome! If you have suggestions for improvements or bug fixes, please feel free to make a pull request or open an issue.

## License

Do whatever you want, I don't care.
