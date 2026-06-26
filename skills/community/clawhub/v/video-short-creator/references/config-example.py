"""
Example configuration for video-short-creator scripts.

Copy this to your project as config.py and customize for your video.
Then run: python scripts/step1_generate_review.py --config path/to/config.py
"""

from pathlib import Path

# === Project Paths ===
WORKSPACE = Path(r"C:\Users\yourname\project")
VIDEO_DIR = WORKSPACE / "clips"       # Folder containing source video clips
OUTPUT_DIR = WORKSPACE / "output"     # Output folder (created automatically)

# === Project Settings ===
PROJECT_NAME = "my_video"             # Used for output filename: {PROJECT_NAME}_FINAL.mp4
VOICE = "zh-CN-YunxiNeural"           # edge-tts voice (see: edge-tts --list-voices)
TARGET_W, TARGET_H = 1920, 1080      # Output resolution
XFADE_DUR = 0.8                       # Cross-fade transition duration (seconds)

# === Subtitle Settings ===
SUBTITLE_FONT_SIZE = 14               # Font size for burned subtitles
SUBTITLE_MARGIN_V = 50                # Bottom margin (pixels from bottom edge)

# === Script Segments ===
# Each segment has:
#   id: unique identifier (seg1, seg2, ...)
#   text: narration text for TTS
#   videos: list of source clips with start time and max duration
SCRIPT = [
    {
        "id": "seg1",
        "text": "Opening narration for the first segment.",
        "videos": [
            {"file": "intro.mp4", "start": 0, "max_dur": 10},
        ],
    },
    {
        "id": "seg2",
        "text": "Second segment with technical details.",
        "videos": [
            {"file": "demo.mp4", "start": 5, "max_dur": 20},
            {"file": "closeup.mp4", "start": 0, "max_dur": 5},
        ],
    },
    {
        "id": "seg3",
        "text": "Closing with a call to action.",
        "videos": [
            {"file": "outro.mp4", "start": 0, "max_dur": 10},
        ],
    },
]

# === Available Chinese Voices (edge-tts) ===
# zh-CN-YunxiNeural       - Young male (default, energetic)
# zh-CN-YunjianNeural     - Male (narrator style)
# zh-CN-XiaoxiaoNeural    - Female (conversational)
# zh-CN-XiaoyiNeural      - Female (gentle)
# zh-CN-YunyangNeural     - Male (news anchor)
# zh-CN-XiaohanNeural     - Female (warm)
# zh-CN-XiaomengNeural    - Female (cute)
# zh-CN-XiaomoNeural      - Female (mature)
# zh-CN-XiaoqiuNeural     - Female (cheerful)
# zh-CN-XiaoshuangNeural  - Female (child)
# zh-CN-XiaoxuanNeural    - Female (literary)
# zh-CN-XiaoruiNeural     - Female (empathetic)
# zh-CN-XiaoyanNeural     - Female (professional)
# zh-CN-XiaozhenNeural    - Female (news)
