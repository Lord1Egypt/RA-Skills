#!/usr/bin/env python3
"""Deterministic fallback when the supplied Playwright renderer is unavailable."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os
import subprocess

root = Path(__file__).resolve().parents[1]

def chinese_font(size):
    candidates = []
    if os.environ.get("SELF_MEDIA_FONT"):
        candidates.append(Path(os.environ["SELF_MEDIA_FONT"]))
    for command in (("fc-match", "-f", "%{file}", "sans:lang=zh"),):
        try:
            matched = subprocess.run(command, capture_output=True, text=True, check=True, timeout=3).stdout.strip()
            if matched:
                candidates.append(Path(matched))
        except (OSError, subprocess.SubprocessError):
            pass
    roots = [Path.home() / "Library/Fonts", Path("/") / "Library" / "Fonts", Path("/") / "System" / "Library" / "Fonts", Path("/") / "usr" / "share" / "fonts", Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"]
    for folder in roots:
        if folder.is_dir():
            candidates.extend(path for pattern in ("*PingFang*", "*NotoSansCJK*", "*SourceHanSans*", "*WenQuanYi*", "*NotoSansSC*") for path in folder.glob(pattern))
    for candidate in candidates:
        if candidate.is_file():
            try:
                return ImageFont.truetype(str(candidate), size)
            except OSError:
                continue
    raise RuntimeError("未找到可用的中文字体；请安装 Noto Sans CJK/思源黑体，或设置 SELF_MEDIA_FONT")

bg = Image.open(root / "assets/icon-source.png").convert("RGB").resize((1600, 900))
canvas = Image.new("RGBA", (1600, 900), "#f9f5ec")
canvas.paste(bg, (0, 0))
overlay = Image.new("RGBA", (980, 900), (249, 245, 236, 250))
canvas.alpha_composite(overlay)
draw = ImageDraw.Draw(canvas)
color = "#12304a"
draw.text((96, 104), "免费开源 · EASY SKILLS", font=chinese_font(25), fill=color)
draw.line((96, 151, 420, 151), fill=color, width=3)
draw.multiline_text((96, 225), "多镜头\n视觉连续性检查", font=chinese_font(88), fill=color, spacing=13)
draw.text((96, 490), "角色 · 道具 · 光线 · 空间", font=chinese_font(34), fill=color)
draw.multiline_text((96, 555), "发现断裂，给出不改故事的\n最小修订建议", font=chinese_font(27), fill="#596367", spacing=10)
draw.text((96, 795), "一件事，一个好用的 Skill", font=chinese_font(23), fill="#586363")
canvas.convert("RGB").save(root / "assets/promo-1600x900.png")
