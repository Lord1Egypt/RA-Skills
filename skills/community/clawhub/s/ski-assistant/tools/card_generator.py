#!/usr/bin/env python3
"""
小红书分享卡片生成器（纯本地操作，无任何网络请求）
用法:
  python tools/card_generator.py score-card '<json>'
  python tools/card_generator.py progress-card '<json>'
  python tools/card_generator.py milestone-card '<json>'

安全说明:
  - 纯本地图片生成，不发起任何网络请求
  - 仅在 ~/.ski-assistant/exports/ 目录写入图片文件
  - 不读取用户隐私数据，仅使用用户提供的卡片参数
  - 不执行 shell、subprocess 或访问外部 API

依赖: pip install Pillow（可选，缺失时提示安装）
"""

import json
import os
import sys
from datetime import datetime
from typing import Tuple, Dict

# 数据目录
_DATA_DIR = os.environ.get("SKI_ASSISTANT_DATA_DIR",
                           os.path.join(os.path.expanduser("~"), ".ski-assistant"))
_EXPORTS_DIR = os.path.join(_DATA_DIR, "exports")

# 小红书图片规格
XHS_WIDTH = 1080
XHS_HEIGHT = 1440

# 配色方案
COLORS = {
    "bg_top": (25, 55, 95),
    "bg_bottom": (60, 120, 160),
    "accent": (255, 140, 60),
    "accent_light": (255, 200, 120),
    "white": (255, 255, 255),
    "text_primary": (40, 40, 40),
    "text_light": (255, 255, 255),
    "card_bg": (255, 255, 255, 230),
    "score_high": (80, 180, 120),
    "score_mid": (255, 180, 60),
    "score_low": (230, 100, 100),
}

DIM_LABELS = {"posture": "基础姿态", "turning": "转弯技术",
              "freestyle": "自由式", "overall": "综合滑行"}


def _check_pillow():
    try:
        from PIL import Image, ImageDraw, ImageFont
        return True, (Image, ImageDraw, ImageFont)
    except ImportError:
        return False, None


def _get_font(ImageFont, size: int, bold: bool = False):
    paths = (["/System/Library/Fonts/PingFang.ttc",
              "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
              "C:/Windows/Fonts/simhei.ttf"] if bold else
             ["/System/Library/Fonts/PingFang.ttc",
              "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
              "C:/Windows/Fonts/msyh.ttc"])
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    try:
        return ImageFont.load_default()
    except Exception:
        return None


def _score_color(score: float) -> Tuple[int, int, int]:
    if score >= 8:
        return COLORS["score_high"]
    elif score >= 6:
        return COLORS["score_mid"]
    return COLORS["score_low"]


def _gradient_bg(Image, w, h):
    img = Image.new("RGB", (w, h))
    px = img.load()
    t, b = COLORS["bg_top"], COLORS["bg_bottom"]
    for y in range(h):
        r = y / h
        for x in range(w):
            px[x, y] = (int(t[0]*(1-r)+b[0]*r), int(t[1]*(1-r)+b[1]*r), int(t[2]*(1-r)+b[2]*r))
    return img


def generate_score_card(params: dict) -> str:
    ok, pil = _check_pillow()
    if not ok:
        return json.dumps({"error": "缺少 Pillow 依赖，请运行: pip install Pillow"}, ensure_ascii=False)

    Image, ImageDraw, ImageFont = pil
    resort = params.get("resort", "未知雪场")
    run_name = params.get("run_name", "")
    date = params.get("date", datetime.now().strftime("%Y-%m-%d"))
    scores = params.get("scores", {})
    highlights = params.get("highlights", [])
    style = params.get("style", "casual")

    valid = [v for v in scores.values() if isinstance(v, (int, float)) and v > 0]
    total = sum(valid) / len(valid) if valid else 0

    img = _gradient_bg(Image, XHS_WIDTH, XHS_HEIGHT)
    draw = ImageDraw.Draw(img)
    ft = _get_font(ImageFont, 48, True)
    fb = _get_font(ImageFont, 32)
    fs = _get_font(ImageFont, 24)
    fsc = _get_font(ImageFont, 120, True)

    y = 60
    draw.text((XHS_WIDTH//2, y), "🏂 滑雪日记", font=ft, fill=COLORS["text_light"], anchor="mm")
    y += 80
    draw.text((XHS_WIDTH//2, y), resort, font=fb, fill=COLORS["accent_light"], anchor="mm")
    y += 50
    if run_name:
        draw.text((XHS_WIDTH//2, y), f"{run_name} | {date}", font=fs, fill=COLORS["text_light"], anchor="mm")
        y += 60

    y += 40
    draw.text((XHS_WIDTH//2, y), f"{total:.1f}", font=fsc, fill=_score_color(total), anchor="mm")
    draw.text((XHS_WIDTH//2+120, y+20), "/10", font=fb, fill=COLORS["text_light"], anchor="mm")
    y += 140

    margin = 80
    cw = XHS_WIDTH - margin*2
    y += 20
    for dim, label in DIM_LABELS.items():
        s = scores.get(dim, 0)
        if s <= 0:
            continue
        draw.text((margin+20, y+10), label, font=fs, fill=COLORS["text_light"])
        bar_bg = Image.new("RGBA", (cw-200, 24), (230, 230, 230, 180))
        img.paste(bar_bg, (margin+120, y+8), bar_bg)
        fw = int((cw-200)*min(s/10, 1.0))
        bar = Image.new("RGBA", (fw, 24), (*_score_color(s), 220))
        img.paste(bar, (margin+120, y+8), bar)
        draw.text((XHS_WIDTH-margin-20, y+10), f"{s}", font=fs, fill=COLORS["text_light"], anchor="rm")
        y += 50
    y += 30

    if highlights:
        y += 20
        ch = min(80+len(highlights)*50, 300)
        ov = Image.new("RGBA", (cw, ch), COLORS["card_bg"])
        img.paste(ov, (margin, y), ov)
        cy = y+20
        draw.text((XHS_WIDTH//2, cy), "✨ AI教练点评", font=fb, fill=COLORS["accent"], anchor="mm")
        cy += 50
        for h in highlights[:3]:
            draw.text((margin+30, cy), f"• {h}", font=fs, fill=COLORS["text_primary"])
            cy += 45

    y = XHS_HEIGHT-100
    tags = f"#滑雪  #{resort.replace('滑雪场','').replace('滑雪','')}"
    draw.text((XHS_WIDTH//2, y), tags, font=fs, fill=COLORS["text_light"], anchor="mm")

    os.makedirs(_EXPORTS_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = os.path.join(_EXPORTS_DIR, f"xhs_score_{ts}.jpg")
    img.save(out, "JPEG", quality=95)

    return json.dumps({"success": True, "output_path": out, "total_score": round(total, 1), "style": style},
                      ensure_ascii=False, indent=2)


def generate_progress_card(params: dict) -> str:
    return json.dumps({"error": "进步对比卡片尚未实现，请使用 score-card"}, ensure_ascii=False)


def generate_milestone_card(params: dict) -> str:
    return json.dumps({"error": "里程碑卡片尚未实现，请使用 score-card"}, ensure_ascii=False)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    params = json.loads(sys.argv[2])

    funcs = {"score-card": generate_score_card,
             "progress-card": generate_progress_card,
             "milestone-card": generate_milestone_card}
    if cmd not in funcs:
        print(json.dumps({"error": f"未知命令: {cmd}"}, ensure_ascii=False))
        sys.exit(1)

    print(funcs[cmd](params))
