#!/usr/bin/env python3
"""
Utility functions for slide-to-video converter.
Includes path definitions, configuration loading, and text processing utilities.
"""

import json
import re
import sys
from pathlib import Path
from difflib import SequenceMatcher


# ============================================================
# Project paths (auto-detected from script location)
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SLIDES_DIR = PROJECT_ROOT / "slides"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
OUTPUT_DIR = PROJECT_ROOT / "output"
IMAGES_DIR = OUTPUT_DIR / "images"
AUDIO_DIR = OUTPUT_DIR / "audio"
VIDEO_DIR = OUTPUT_DIR / "video"
SCRIPT_JSON = SLIDES_DIR / "subtitles.json"
PDF_PATH = SLIDES_DIR / "presentation.pdf"
PPTX_PATH = SLIDES_DIR / "presentation.pptx"
CONFIG_PATH = PROJECT_ROOT / "assets" / "config.json"


# ============================================================
# Configuration loading
# ============================================================

def load_config() -> dict:
    """Load config.json with defaults."""
    defaults = {
        "tts": {
            "voice_name": "Chelsie",
            "lang_code": "zh",
            "speech_speed": 1.0,
            "base_temperature": 0.3,
        },
        "edge_tts": {
            "voice": "zh-CN-YunyangNeural",
            "rate": "+0%",
            "volume": "+0%",
        },
        "validation": {
            "threshold": 0.6,
            "max_retries": 5,
            "chars_per_sec": 15,
            "duration_tolerance": 2.0,
        },
        "video": {
            "fps": 24,
            "fps_fast": 8,
            "video_codec": "libx264",
            "audio_codec": "aac",
        },
        "image": {
            "dpi": 300,
            "dpi_fast": 150,
            "width": 1920,
            "height": 1080,
            "width_fast": 1280,
            "height_fast": 720,
        },
        "subtitle": {
            "font": "/System/Library/Fonts/PingFang.ttc",
            "font_size": 32,
            "color": "white",
            "stroke_color": "black",
            "stroke_width": 2,
            "margin_bottom": 40,
            "line_max_chars": 35,
            "padding_h": 30,
        },
        "stt": {
            "model_id": "SenseVoiceSmall",
        },
    }
    
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            user_cfg = json.load(f)
        for section in defaults:
            if section in user_cfg:
                defaults[section].update(user_cfg[section])
    
    return defaults


def get_config_section(section: str, default: dict = None) -> dict:
    """
    Get a specific section from the configuration.
    
    Args:
        section: Section name (e.g., "tts", "video", "validation")
        default: Default value if section not found
    
    Returns:
        Dictionary containing the section configuration
    """
    config = load_config()
    return config.get(section, default or {})


def get_tts_config() -> dict:
    """Get TTS configuration section."""
    return get_config_section("tts")


def get_video_config() -> dict:
    """Get video configuration section."""
    return get_config_section("video")


def get_validation_config() -> dict:
    """Get validation configuration section."""
    return get_config_section("validation")


def get_stt_config() -> dict:
    """Get STT configuration section."""
    return get_config_section("stt")


def get_edge_tts_config() -> dict:
    """Get Edge TTS configuration section."""
    return get_config_section("edge_tts")


def ensure_directory(path: Path) -> Path:
    """
    Ensure directory exists and return the path.
    
    Args:
        path: Directory path to ensure exists
    
    Returns:
        The same path for chaining
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_slide_range_description(slide_nums: list[int]) -> str:
    """
    Convert list of slide numbers to human-readable description.
    
    Args:
        slide_nums: List of slide numbers
    
    Returns:
        String description like "slides 1-5" or "slide 3"
    """
    if not slide_nums:
        return "no slides"
    if len(slide_nums) == 1:
        return f"slide {slide_nums[0]}"
    if len(slide_nums) == len(range(min(slide_nums), max(slide_nums) + 1)):
        return f"slides {min(slide_nums)}-{max(slide_nums)}"
    return f"slides {sorted(slide_nums)}"


def format_percentage(value: float) -> str:
    """Format float as percentage string (e.g., 0.85 -> '85%')."""
    return f"{value * 100:.0f}%"


def format_bool(value: bool) -> str:
    """Format boolean as 'Yes' or 'No'."""
    return "Yes" if value else "No"


def format_list(items: list, max_items: int = 5) -> str:
    """Format list with truncation if too long."""
    if len(items) <= max_items:
        return str(items)
    return f"[{items[0]}, {items[1]}, ..., {items[-1]}] ({len(items)} items)"


# ============================================================
# Text processing utilities
# ============================================================

def normalize_text(text: str) -> str:
    """Normalize text for comparison: lowercase, remove punctuation, trim spaces."""
    # Remove punctuation and convert to lowercase
    text = re.sub(r'[^\w\s]', '', text.lower())
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def compute_similarity(text1: str, text2: str) -> float:
    """Compute similarity between two texts using SequenceMatcher."""
    norm1 = normalize_text(text1)
    norm2 = normalize_text(text2)
    return SequenceMatcher(None, norm1, norm2).ratio()


def compute_char_coverage(text1: str, text2: str) -> float:
    """Compute character coverage: how much of text1 appears in text2."""
    if not text1:
        return 0.0
    
    norm1 = normalize_text(text1)
    norm2 = normalize_text(text2)
    
    # Count characters from text1 that appear in text2
    matched_chars = sum(1 for char in norm1 if char in norm2)
    return matched_chars / len(norm1) if norm1 else 0.0


# ============================================================
# Script parsing
# ============================================================

def parse_json_subtitles(json_path: Path = None) -> dict:
    """Parse subtitles.json → {slide_num: {"title": str, "text": str}, ...}"""
    if json_path is None:
        json_path = SCRIPT_JSON
    if not json_path.exists():
        flush_print(f"[WARN] JSON subtitles not found: {json_path}")
        return {}
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    slides = {}
    for key, text in data.items():
        slide_num = None
        
        # Try different key formats
        if key.startswith("slide_"):
            try:
                slide_num = int(key.split("_")[1])
            except (ValueError, IndexError):
                continue
        else:
            # Try parsing as pure number
            try:
                slide_num = int(key)
            except ValueError:
                continue
        
        if slide_num is not None:
            slides[slide_num] = {"title": f"Slide {slide_num}", "text": text}
    
    return slides


def parse_slide_range(slide_range: str) -> list[int]:
    """Parse slide range string like '1-5' or '1,3,5' into list of numbers."""
    nums = set()
    for part in slide_range.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            for n in range(int(a), int(b) + 1):
                nums.add(n)
        else:
            nums.add(int(part))
    return sorted(nums)


# ============================================================
# Output formatting
# ============================================================

def flush_print(*args, **kwargs):
    """Print with immediate flush."""
    print(*args, **kwargs, flush=True)


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format."""
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    ms = int((seconds - total) * 1000)
    if h > 0:
        return f"{h}h {m}m {s}s"
    elif m > 0:
        return f"{m}m {s}.{ms:03d}s"
    else:
        return f"{s}.{ms:03d}s"


# ============================================================
# File utilities
# ============================================================

def ensure_directories():
    """Ensure all required directories exist."""
    for directory in [SLIDES_DIR, IMAGES_DIR, AUDIO_DIR, VIDEO_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def get_audio_duration(audio_path: str) -> float:
    """Get audio duration in seconds."""
    import wave
    with wave.open(audio_path, "r") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return frames / rate


def get_video_duration(video_path: str) -> float:
    """Get video duration via ffprobe."""
    import subprocess
    result = subprocess.run(
        ["ffprobe", "-v", "quiet",
         "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1",
         video_path],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        return float(result.stdout.strip())
    return 0.0


# ============================================================
# Text segmentation for subtitles
# ============================================================

def split_subtitle_segments(text: str, max_chars: int = 30) -> list[str]:
    """Split text into subtitle segments at sentence-ending punctuation."""
    parts = re.split(r'([。！？!?])', text)
    raw = []
    cur = ""
    for p in parts:
        cur += p
        if p in "。！？!?":
            if cur.strip():
                raw.append(cur.strip())
            cur = ""
    if cur.strip():
        raw.append(cur.strip())

    # Further split long segments at commas
    segments = []
    for s in raw:
        if len(s) <= max_chars:
            segments.append(s)
        else:
            sub = re.split(r'([，、；;,])', s)
            buf = ""
            for sp in sub:
                if buf and sp in "，、；;,":
                    buf += sp
                    if len(buf) >= max_chars * 0.5:
                        segments.append(buf.strip())
                        buf = ""
                elif sp in "，、；;,":
                    buf += sp
                else:
                    buf += sp
            if buf.strip():
                segments.append(buf.strip())
    return segments


def allocate_timings(sentences: list[str], total_dur: float) -> list[tuple]:
    """Allocate time proportionally by character count."""
    total_chars = sum(len(s) for s in sentences)
    if total_chars == 0:
        return []
    timings = []
    t = 0.0
    for s in sentences:
        d = (len(s) / total_chars) * total_dur
        timings.append((s, t, t + d))
        t += d
    return timings


def wrap_text(text: str, max_chars: int = 35) -> str:
    """Wrap Chinese text for subtitle display."""
    lines = []
    cur = ""
    for ch in text:
        cur += ch
        if ch in "。！？；，、" and len(cur) >= max_chars * 0.6:
            lines.append(cur)
            cur = ""
        elif len(cur) >= max_chars:
            bp = -1
            for i in range(len(cur) - 1, max(0, len(cur) - 10), -1):
                if cur[i] in "。！？；，、,. ":
                    bp = i + 1
                    break
            if bp > 0:
                lines.append(cur[:bp])
                cur = cur[bp:]
            else:
                lines.append(cur)
                cur = ""
    if cur:
        lines.append(cur)
    return "\n".join(lines)