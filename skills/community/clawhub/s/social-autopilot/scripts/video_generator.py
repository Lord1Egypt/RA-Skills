import logging
import random
from datetime import datetime
from pathlib import Path

import numpy as np
from moviepy import AudioFileClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont

from bot.ig_config import OUTPUT_DIR, TEMPLATES_DIR

logger = logging.getLogger(__name__)

ANSWER_MAP = {"A": "option_a", "B": "option_b", "C": "option_c", "D": "option_d"}

# ── Visual design constants ──────────────────────────────────────────────────
VIDEO_W, VIDEO_H = 1080, 1920
VIDEO_DURATION = 15  # seconds

# Fonts — use bundled Liberation Sans (Arial-compatible), fall back to system Arial
_FONTS_DIR = Path(__file__).resolve().parent.parent / "fonts"
FONT_BOLD = str(_FONTS_DIR / "LiberationSans-Bold.ttf")
FONT_REGULAR = str(_FONTS_DIR / "LiberationSans-Regular.ttf")

# Colors (RGBA)
COLOR_QUESTION_BG = (20, 20, 50, 200)
COLOR_OPTION_BG = (255, 255, 255, 180)
COLOR_QUESTION_TEXT = (255, 255, 255)
COLOR_OPTION_TEXT = (30, 30, 50)
COLOR_ANSWER_TEXT = (255, 255, 255)
COLOR_HEADER_TEXT = (255, 200, 60)
COLOR_YEAR_TEXT = (255, 255, 255, 220)
COLOR_EXPLAIN_BG = (20, 20, 50, 210)
COLOR_EXPLAIN_TEXT = (230, 230, 240)
COLOR_EXPLAIN_TITLE = (255, 200, 60)

# Layout
CARD_MARGIN_X = 45
CARD_WIDTH = VIDEO_W - 2 * CARD_MARGIN_X
CARD_RADIUS = 24
CARD_PADDING = 30

# Gradient background palettes — (top_color, bottom_color)
GRADIENT_PALETTES = [
    ((25, 15, 60), (10, 30, 80)),      # deep purple → navy
    ((10, 40, 50), (5, 15, 45)),       # dark teal → midnight
    ((15, 30, 15), (10, 20, 50)),      # dark forest → navy
    ((50, 10, 30), (25, 10, 55)),      # burgundy → purple
    ((10, 20, 55), (30, 10, 45)),      # royal blue → plum
    ((40, 20, 10), (15, 15, 50)),      # dark brown → indigo
    ((10, 35, 45), (20, 10, 50)),      # ocean → violet
    ((35, 10, 50), (10, 25, 60)),      # magenta → teal-blue
]


def _generate_gradient_bg() -> Image.Image:
    top, bottom = random.choice(GRADIENT_PALETTES)
    img = Image.new("RGB", (VIDEO_W, VIDEO_H))
    draw = ImageDraw.Draw(img)
    for y in range(VIDEO_H):
        ratio = y / VIDEO_H
        r = int(top[0] + (bottom[0] - top[0]) * ratio)
        g = int(top[1] + (bottom[1] - top[1]) * ratio)
        b = int(top[2] + (bottom[2] - top[2]) * ratio)
        draw.line([(0, y), (VIDEO_W, y)], fill=(r, g, b))
    logger.info("Generated gradient background: %s → %s", top, bottom)
    return img


def _pick_music() -> Path:
    music_files = sorted(TEMPLATES_DIR.glob("*.mp3"))
    if not music_files:
        raise FileNotFoundError(f"No music files found in {TEMPLATES_DIR}")
    return random.choice(music_files)


def _load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(name, size)


def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        bbox = font.getbbox(test)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def _render_header_card(category: str) -> Image.Image:
    font = _load_font(FONT_BOLD, 34)
    label = "Previous Year UPSC Quiz"
    bbox = font.getbbox(label)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    pad_x, pad_y = 36, 16
    card_w = text_w + 2 * pad_x
    card_h = text_h + 2 * pad_y
    img = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, card_w, card_h), radius=20, fill=(100, 60, 180, 210))
    draw.text((pad_x, pad_y - bbox[1]), label, fill=COLOR_HEADER_TEXT, font=font)
    return img


def _render_question_card(question: str, year: str = "") -> Image.Image:
    font = _load_font(FONT_BOLD, 46)
    year_font = _load_font(FONT_BOLD, 38)
    max_text_w = CARD_WIDTH - 2 * CARD_PADDING
    lines = _wrap_text(question, font, max_text_w)
    line_height = 60
    text_block_h = len(lines) * line_height
    year_line_h = 52 if year else 0
    card_h = text_block_h + year_line_h + 2 * CARD_PADDING + 10
    img = Image.new("RGBA", (CARD_WIDTH, card_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        (0, 0, CARD_WIDTH, card_h), radius=CARD_RADIUS, fill=COLOR_QUESTION_BG
    )
    y = CARD_PADDING
    for line in lines:
        bbox = font.getbbox(line)
        line_w = bbox[2] - bbox[0]
        x = (CARD_WIDTH - line_w) // 2
        draw.text((x, y), line, fill=COLOR_QUESTION_TEXT, font=font)
        y += line_height
    if year:
        year_label = f"— UPSC {year} —"
        ybbox = year_font.getbbox(year_label)
        yw = ybbox[2] - ybbox[0]
        yx = (CARD_WIDTH - yw) // 2
        draw.text((yx, y + 6), year_label, fill=(255, 60, 60), font=year_font)
    return img


def _render_option_card(letter: str, text: str, is_answer: bool = False) -> Image.Image:
    letter_font = _load_font(FONT_BOLD, 38)
    text_font = _load_font(FONT_REGULAR, 36)
    max_text_w = CARD_WIDTH - 120
    lines = _wrap_text(text, text_font, max_text_w)
    line_height = 48
    text_block_h = len(lines) * line_height
    card_h = max(120, text_block_h + 78)
    img = Image.new("RGBA", (CARD_WIDTH, card_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    bg = (0, 180, 100, 200) if is_answer else COLOR_OPTION_BG
    draw.rounded_rectangle((0, 0, CARD_WIDTH, card_h), radius=card_h // 2, fill=bg)
    circle_r = 23
    circle_x, circle_y = 36, card_h // 2
    circle_bg = (100, 60, 180, 255) if not is_answer else (255, 255, 255, 255)
    draw.ellipse(
        (circle_x - circle_r, circle_y - circle_r,
         circle_x + circle_r, circle_y + circle_r),
        fill=circle_bg,
    )
    lbbox = letter_font.getbbox(letter)
    lw = lbbox[2] - lbbox[0]
    lh = lbbox[3] - lbbox[1]
    letter_color = (255, 255, 255) if not is_answer else (0, 140, 80)
    draw.text(
        (circle_x - lw // 2, circle_y - lh // 2 - lbbox[1]),
        letter, fill=letter_color, font=letter_font,
    )
    text_x = circle_x + circle_r + 22
    text_y = (card_h - text_block_h) // 2
    txt_color = COLOR_ANSWER_TEXT if is_answer else COLOR_OPTION_TEXT
    for line in lines:
        draw.text((text_x, text_y), line, fill=txt_color, font=text_font)
        text_y += line_height
    return img


def _render_answer_hint() -> Image.Image:
    font = _load_font(FONT_BOLD, 34)
    label = "Answer & Explanation in comments!"
    bbox = font.getbbox(label)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    pad_y = 16
    card_w = CARD_WIDTH
    card_h = text_h + 2 * pad_y
    img = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        (0, 0, card_w, card_h), radius=card_h // 2, fill=(100, 60, 180, 200)
    )
    x = (card_w - text_w) // 2
    draw.text((x, pad_y - bbox[1]), label, fill=COLOR_HEADER_TEXT, font=font)
    return img


def _render_bottom_banner() -> Image.Image:
    line1_font = _load_font(FONT_BOLD, 36)
    line2_font = _load_font(FONT_BOLD, 30)
    line1 = "{BRAND_NAME}"
    line2 = "30 Years (1995-2025) Topic Wise PYQs"
    l1_bbox = line1_font.getbbox(line1)
    l2_bbox = line2_font.getbbox(line2)
    l1_h = l1_bbox[3] - l1_bbox[1]
    l2_h = l2_bbox[3] - l2_bbox[1]
    pad = 22
    gap = 10
    card_h = l1_h + gap + l2_h + 2 * pad
    img = Image.new("RGBA", (CARD_WIDTH, card_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        (0, 0, CARD_WIDTH, card_h), radius=CARD_RADIUS, fill=(180, 40, 40, 220)
    )
    l1_w = l1_bbox[2] - l1_bbox[0]
    draw.text(
        ((CARD_WIDTH - l1_w) // 2, pad),
        line1, fill=(255, 255, 255), font=line1_font,
    )
    l2_w = l2_bbox[2] - l2_bbox[0]
    draw.text(
        ((CARD_WIDTH - l2_w) // 2, pad + l1_h + gap),
        line2, fill=(255, 220, 60), font=line2_font,
    )
    return img


def _pil_to_clip(img: Image.Image, pos, start, duration) -> ImageClip:
    arr = np.array(img)
    return (
        ImageClip(arr, is_mask=False, transparent=True)
        .with_position(pos)
        .with_start(start)
        .with_duration(duration)
    )


def _build_clips(question_data: dict, video_duration: float) -> list:
    year = question_data.get("year", "")
    clips = []

    header_img = _render_header_card(question_data.get("category", "General"))
    header_x = (VIDEO_W - header_img.width) // 2
    clips.append(_pil_to_clip(header_img, (header_x, 160), 0, video_duration))

    q_img = _render_question_card(question_data["question"], year)
    clips.append(_pil_to_clip(q_img, (CARD_MARGIN_X, 260), 0, video_duration))

    q_card_bottom = 260 + q_img.height + 40
    option_gap = 30
    options = [
        ("A", question_data["option_a"]),
        ("B", question_data["option_b"]),
        ("C", question_data["option_c"]),
        ("D", question_data["option_d"]),
    ]

    y = q_card_bottom
    for letter, text in options:
        opt_img = _render_option_card(letter, text, is_answer=False)
        clips.append(_pil_to_clip(opt_img, (CARD_MARGIN_X, y), 0, video_duration))
        y += opt_img.height + option_gap

    hint_img = _render_answer_hint()
    clips.append(_pil_to_clip(hint_img, (CARD_MARGIN_X, y + 10), 0, video_duration))

    banner_img = _render_bottom_banner()
    banner_y = VIDEO_H - banner_img.height - 60
    clips.append(_pil_to_clip(banner_img, (CARD_MARGIN_X, banner_y), 0, video_duration))

    return clips


def generate_video(
    question_data: dict,
    output_path: Path | None = None,
) -> Path:
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = OUTPUT_DIR / f"quiz_{timestamp}.mp4"

    logger.info("Generating video: %s", output_path.name)

    bg_img = _generate_gradient_bg()
    bg_clip = ImageClip(np.array(bg_img)).with_duration(VIDEO_DURATION)

    music_path = _pick_music()
    audio = AudioFileClip(str(music_path)).subclipped(0, VIDEO_DURATION)
    bg_clip = bg_clip.with_audio(audio)

    overlay_clips = _build_clips(question_data, VIDEO_DURATION)
    composite = CompositeVideoClip([bg_clip, *overlay_clips])

    composite.write_videofile(
        str(output_path),
        codec="libx264",
        audio_codec="aac",
        fps=30,
        ffmpeg_params=["-movflags", "+faststart"],
        logger=None,
    )

    audio.close()
    composite.close()

    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    logger.info("Video saved: %s (%.1f MB)", output_path.name, file_size_mb)

    return output_path
