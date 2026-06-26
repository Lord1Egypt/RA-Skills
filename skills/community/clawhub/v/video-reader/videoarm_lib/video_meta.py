"""Video metadata extraction."""

import json
import subprocess


def get_video_meta(video_path: str) -> dict:
    """Return fps, total_frames, duration, has_audio for a video file."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json",
         "-show_format", "-show_streams", video_path],
        capture_output=True, text=True, timeout=15,
    )
    data = json.loads(result.stdout)

    vs = next(s for s in data["streams"] if s["codec_type"] == "video")
    has_audio = any(s["codec_type"] == "audio" for s in data["streams"])

    num, den = map(int, vs["r_frame_rate"].split("/"))
    fps = num / den if den else 0
    duration = float(data["format"]["duration"])
    total_frames = int(duration * fps)

    return {
        "fps": fps,
        "total_frames": total_frames,
        "duration": round(duration, 2),
        "has_audio": has_audio,
    }
