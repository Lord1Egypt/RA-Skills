#!/usr/bin/env python3
"""Deterministic fallback used only when the supplied Playwright renderer cannot launch."""
from pathlib import Path
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

if len(sys.argv) != 3:
    raise SystemExit("usage: render_promo_fallback.py INPUT OUTPUT")
font = subprocess.check_output(["fc-match", "-f", "%{file}", "PingFang SC"], text=True).strip()
if not font or not Path(font).is_file():
    raise SystemExit("no usable Chinese font discovered by fontconfig")
source = Image.open(sys.argv[1]).convert("RGB")
canvas = source.resize((1600, 900), Image.Resampling.LANCZOS)
draw = ImageDraw.Draw(canvas)
title = ImageFont.truetype(font, 76)
identity = ImageFont.truetype(font, 37)
subtitle = ImageFont.truetype(font, 29)
ink, coral = "#162438", "#C96650"
draw.rounded_rectangle((88, 176, 104, 384), radius=8, fill=coral)
draw.text((130, 166), "视频参考素材分工表", font=title, fill=ink)
draw.text((134, 270), "每张参考，各司其职", font=identity, fill=ink)
draw.text((134, 332), "身份·地点·风格·动作，一表梳清", font=subtitle, fill=ink)
canvas.save(sys.argv[2], "PNG", optimize=True)
