#!/usr/bin/env python3
"""拼贴封面 — 小红书穿搭合集视觉锤:5 套 look 竖条并排 + 顶部粗黑标题。
对齐:用人脸检测,按"脸的大小"统一缩放(人物等大),按"脸顶"统一对齐(头齐)。

用法:
    python3 build_cover.py "<标题>" <输出.png> <look1> ... <look5>
"""
import os
import sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

_HERE = os.path.dirname(os.path.abspath(__file__))
CN_FONT = os.path.join(_HERE, "fonts", "NotoSansSC.ttf")   # 可变字重,用 Black
W, H = 1080, 1440
HEAD_Y = 0.215     # 脸顶对齐线:在标题下方留出空隙,人物不顶到标题
FEET_Y = 0.955     # 脚底对齐线:底部也留一点余量

_F = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
_P = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")


def detect_face(im):
    """稳健人脸检测:正脸+侧脸+镜像侧脸,多参数;只取上 60% 区域内最大的。
    返回 (cx, top, h) 原图像素;失败返回 None。"""
    gray = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
    Hh, Ww = gray.shape
    cands = []
    for casc in (_F, _P):
        for mn in (5, 3):
            for (x, y, w, h) in casc.detectMultiScale(gray, 1.1, mn, minSize=(40, 40)):
                cands.append((x, y, w, h))
    flip = cv2.flip(gray, 1)
    for (x, y, w, h) in _P.detectMultiScale(flip, 1.1, 4, minSize=(40, 40)):
        cands.append((Ww - (x + w), y, w, h))
    if not cands:
        return None

    def pick(cx_lo, cx_hi, y_hi):
        sel = [c for c in cands
               if cx_lo <= (c[0] + c[2] / 2) / Ww <= cx_hi and c[1] < Hh * y_hi]
        return max(sel, key=lambda c: c[2] * c[3]) if sel else None

    # 真脸在"靠顶+水平居中";假脸多在偏侧/偏下。先严后松。
    c = pick(0.30, 0.70, 0.45) or pick(0.20, 0.80, 0.55) or pick(0.0, 1.0, 0.6)
    if not c:
        return None
    x, y, w, h = c
    return x + w / 2, y, h


def head_cx_top(im):
    """兜底:暗像素估头顶y与人物中心x(原图像素)。"""
    sw, sh = 64, 96
    g = np.array(im.convert("L").resize((sw, sh)))
    mask = g < 110
    rows = mask.sum(1)
    top = next((r for r in range(sh) if rows[r] >= 5), 0)
    cols = mask.sum(0)
    cx = (np.arange(sw) * cols).sum() / max(cols.sum(), 1)
    return cx / sw * im.width, top / sh * im.height


def feet_y(im, cx_frac=0.5):
    """脚底:只在人物所在竖条(cx±0.18)内找最低暗像素,忽略别处家具。"""
    sw, sh = 64, 96
    g = np.array(im.convert("L").resize((sw, sh)))
    mask = g < 110
    c0 = max(0, int((cx_frac - 0.18) * sw))
    c1 = min(sw, int((cx_frac + 0.18) * sw))
    rows = mask[:, c0:c1].sum(1)
    bot = next((r for r in range(sh - 1, -1, -1) if rows[r] >= 2), sh - 1)
    return (bot + 1) / sh * im.height


def aligned_panel(im, pw, ph):
    """脸顶@HEAD_Y、脚底@FEET_Y 双锚定(头脚都对齐、全身入镜),水平居中到人物。
    头顶用人脸检测(可靠,忽略撩发手臂等干扰),脚底用最低暗像素。"""
    im = im.convert("RGB")
    face = detect_face(im)
    if face:
        fcx, ftop, _ = face
    else:
        fcx, ftop = head_cx_top(im)
    fy = feet_y(im, fcx / im.width)
    span = max(fy - ftop, 0.3 * im.height)
    scale = ((FEET_Y - HEAD_Y) * ph) / span        # 头-脚跨度 → 目标跨度
    # 上限:短跨度(脚检测偏高)时别把人放过大裁到头;脚不够到底用地板色补
    scale = min(scale, ph / im.height * 1.04)
    nw, nh = round(im.width * scale), round(im.height * scale)
    big = im.resize((nw, nh), Image.LANCZOS)
    oy = round(HEAD_Y * ph - ftop * scale)         # 脸顶对齐(脚底随之对齐)
    ox = round(pw / 2 - fcx * scale)               # 人物水平居中
    wall = big.crop((0, 0, nw, max(1, nh // 25))).resize((1, 1)).getpixel((0, 0))
    floor = big.crop((0, nh - max(1, nh // 25), nw, nh)).resize((1, 1)).getpixel((0, 0))
    panel = Image.new("RGB", (pw, ph), wall)
    ImageDraw.Draw(panel).rectangle([0, int(FEET_Y * ph), pw, ph], fill=floor)
    panel.paste(big, (ox, oy))
    return panel


def main():
    title, out, looks = sys.argv[1], sys.argv[2], sys.argv[3:]
    n = len(looks)
    pw = W // n
    canvas = Image.new("RGB", (W, H), "white")
    for i, p in enumerate(looks):
        canvas.paste(aligned_panel(Image.open(p), pw, H), (i * pw, 0))

    # 极轻顶部渐变(浅墙上保证白字可读)
    gh = int(H * 0.14)
    grad = Image.new("L", (1, gh), 0)
    for y in range(gh):
        grad.putpixel((0, y), int(60 * (1 - y / gh)))
    grad = grad.resize((W, gh))
    dark = Image.new("RGB", (W, gh), (0, 0, 0))
    canvas.paste(Image.composite(dark, canvas.crop((0, 0, W, gh)), grad), (0, 0))

    _draw_title(canvas, title)
    canvas.save(out, quality=92)
    print(f"✅ 封面(人脸对齐) {out}")


def _draw_title(canvas, title):
    """对标小红书封面字:Black 粗字重 + 斜体 + 白字 + 细描边 + 轻投影。"""
    W = canvas.width
    size = int(W * 0.085)
    font = ImageFont.truetype(CN_FONT, size)
    try:
        font.set_variation_by_name("Black")
    except Exception:
        pass
    while font.getbbox(title)[2] > W * 0.82 and size > 40:
        size -= 2
        font = ImageFont.truetype(CN_FONT, size)
        try:
            font.set_variation_by_name("Black")
        except Exception:
            pass
    bb = font.getbbox(title)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = int(size * 0.6)
    layer = Image.new("RGBA", (tw + 2 * pad, th + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ox, oy = pad - bb[0], pad - bb[1]
    r = max(2, size // 22)                                  # 细描边
    for dx in range(-r, r + 1):
        for dy in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                d.text((ox + dx, oy + dy), title, font=font, fill=(50, 50, 50, 255))
    d.text((ox, oy), title, font=font, fill=(255, 255, 255, 255))
    # 斜体(右倾)
    shear = 0.16
    lw, lh = layer.size
    layer = layer.transform((lw + int(lh * shear), lh), Image.AFFINE,
                            (1, shear, -shear * lh, 0, 1, 0), resample=Image.BICUBIC)
    # 轻投影
    alpha = layer.split()[3]
    shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 150), mask=alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(4))
    px = (W - layer.width) // 2
    py = int(canvas.height * 0.038)
    canvas.paste(shadow, (px + 4, py + 5), shadow)
    canvas.paste(layer, (px, py), layer)


if __name__ == "__main__":
    main()
