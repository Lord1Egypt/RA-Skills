"""Generates quiz question images styled like a UPSC question paper."""

import logging
import os
import tempfile

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

IMG_WIDTH = 1080
PADDING_X = 80
PADDING_Y = 40
TEXT_AREA_WIDTH = IMG_WIDTH - 2 * PADDING_X
OPTION_INDENT = 40

BG_COLOR = "#FDF8F0"
TEXT_COLOR = "#1a1a1a"


def _get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Load a serif-style font. Falls back through system fonts."""
    font_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts")

    if bold:
        candidates = [
            (font_dir, "NotoSerif-Bold.ttf"),
            (font_dir, "DejaVuSerif-Bold.ttf"),
            ("/usr/share/fonts/truetype/dejavu", "DejaVuSerif-Bold.ttf"),
            ("/usr/share/fonts/truetype/dejavu", "DejaVuSans-Bold.ttf"),
        ]
    else:
        candidates = [
            (font_dir, "NotoSerif-Regular.ttf"),
            (font_dir, "DejaVuSerif.ttf"),
            ("/usr/share/fonts/truetype/dejavu", "DejaVuSerif.ttf"),
            ("/usr/share/fonts/truetype/dejavu", "DejaVuSans.ttf"),
        ]

    for directory, name in candidates:
        path = os.path.join(directory, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)

    for p in ["/System/Library/Fonts/Times.ttc", "/System/Library/Fonts/Helvetica.ttc"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)

    return ImageFont.load_default()


def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Word-wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test = f"{current_line} {word}".strip()
        bbox = font.getbbox(test)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def generate_question_image(q: dict) -> str:
    """Generate an image styled like a UPSC question paper screenshot.

    Layout — just question and options, no header/footer:
        Q.  <question text>

            (a) option 1
            (b) option 2
            (c) option 3
            (d) option 4
    """
    question_font = _get_font(28)
    option_font = _get_font(26)

    opts = q["options"]
    year = q.get("year", "")

    # Wrap question text (year rendered separately in red)
    q_text = f"Q.  {q['question']}"
    question_lines = _wrap_text(q_text, question_font, TEXT_AREA_WIDTH)

    year_tag = f"UPSC {year}" if year else ""

    # Wrap options with UPSC-style labels
    option_labels = ["(a)", "(b)", "(c)", "(d)"]
    option_max_w = TEXT_AREA_WIDTH - OPTION_INDENT
    wrapped_options = []
    for i, opt in enumerate(opts):
        full = f"{option_labels[i]}  {opt}"
        wrapped = _wrap_text(full, option_font, option_max_w)
        wrapped_options.append(wrapped)

    # Calculate line heights
    line_sp = 10
    q_line_h = question_font.getbbox("Ay")[3] + line_sp
    opt_line_h = option_font.getbbox("Ay")[3] + line_sp

    # Total content height
    year_block_h = (15 + q_line_h) if year else 0
    content_h = (
        len(question_lines) * q_line_h
        + year_block_h                              # year tag line
        + 30                                        # gap before options
        + sum(len(lines) * opt_line_h for lines in wrapped_options)
        + 16 * 3                                    # gaps between options
    )

    img_h = content_h + 2 * PADDING_Y

    img = Image.new("RGB", (IMG_WIDTH, img_h), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # --- Diagonal watermark ---
    wm_font = _get_font(36)
    wm_text = "{BRAND_NAME}"
    wm_color = "#f0ebe3"  # very subtle, just above background
    # Create a temporary image for rotated watermark
    wm_bbox = wm_font.getbbox(wm_text)
    wm_w = wm_bbox[2] - wm_bbox[0]
    wm_h = wm_bbox[3] - wm_bbox[1]
    spacing_x = wm_w + 80
    spacing_y = wm_h + 100
    for wy in range(-img_h, img_h * 2, spacing_y):
        for wx in range(-IMG_WIDTH, IMG_WIDTH * 2, spacing_x):
            # Create small image, draw text, rotate, paste
            txt_img = Image.new("RGBA", (wm_w + 20, wm_h + 20), (0, 0, 0, 0))
            txt_draw = ImageDraw.Draw(txt_img)
            txt_draw.text((10, 10), wm_text, fill=wm_color, font=wm_font)
            rotated = txt_img.rotate(30, expand=True, fillcolor=(0, 0, 0, 0))
            img.paste(rotated, (wx, wy), rotated)

    y = PADDING_Y

    # --- Question ---
    for line in question_lines:
        draw.text((PADDING_X, y), line, fill=TEXT_COLOR, font=question_font)
        y += q_line_h

    # --- Year tag (red) ---
    if year_tag:
        y += 15
        draw.text((PADDING_X, y), year_tag, fill="#c0392b", font=question_font)
        y += q_line_h

    y += 30

    # --- Options ---
    opt_x = PADDING_X + OPTION_INDENT
    for i, lines in enumerate(wrapped_options):
        for line in lines:
            draw.text((opt_x, y), line, fill=TEXT_COLOR, font=option_font)
            y += opt_line_h
        if i < 3:
            y += 16

    # Save to temp file
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    img.save(tmp.name, "PNG")
    logger.info("Generated question paper image: %s", tmp.name)
    return tmp.name
