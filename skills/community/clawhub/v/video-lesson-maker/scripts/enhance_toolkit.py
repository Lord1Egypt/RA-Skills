# -*- coding: utf-8 -*-
"""画面增强图元工具箱（PIL 程序化绘制，零 AI 积分，V01 验证）。

提供与白板线稿统一的手绘风图元，供各项目编写自己的 enhance_*.py 调用：
- sketch_line / sketch_rect / sketch_ellipse：带抖动的双线手绘线条
- draw_star / draw_sun / draw_cloud / draw_arrow / draw_bubble：装饰元素
- draw_title（大标题+红波浪线）/ draw_label_card（标签牌）/ draw_stamp（完结印章）
- clean_hand_text：涂掉手部素材笔杆上的文字（形态学闭运算方案，V01 十四轮迭代的最终解）

风格基准（与 srt-whiteboard-animation 出图规范统一）：
    墨灰 #4A4A4A / 红 #C0392B / 橙 #E67E22 / 蓝 #2E86C1 / 便签底 #F8F2E3
    字体：标题楷体 simkai.ttf，标签微软雅黑粗体 msyhbd.ttc（Windows）
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

INK = (74, 74, 74)
RED = (192, 57, 43)
ORANGE = (230, 126, 34)
BLUE = (46, 134, 193)
PAPER_LIGHT = (248, 242, 227)

FONT_KAI = r"C:\Windows\Fonts\simkai.ttf"
FONT_YAHEI_BD = r"C:\Windows\Fonts\msyhbd.ttc"


def f_kai(size):
    return ImageFont.truetype(FONT_KAI, size)


def f_yahei(size):
    return ImageFont.truetype(FONT_YAHEI_BD, size)


# ---------------- 手绘风格图元 ----------------

def sketch_line(d, p0, p1, color, width=3, jitter=1.6, segs=10):
    pts = []
    for i in range(segs + 1):
        t = i / segs
        x = p0[0] + (p1[0] - p0[0]) * t + np.random.uniform(-jitter, jitter)
        y = p0[1] + (p1[1] - p0[1]) * t + np.random.uniform(-jitter, jitter)
        pts.append((x, y))
    d.line(pts, fill=color, width=width, joint="curve")


def sketch_rect(d, box, color, width=3, jitter=1.6):
    x0, y0, x1, y1 = box
    for off in [(-1.2, -1.2), (1.2, 1.2)]:
        b = (x0 + off[0], y0 + off[1], x1 + off[0], y1 + off[1])
        sketch_line(d, (b[0], b[1]), (b[2], b[1]), color, width, jitter)
        sketch_line(d, (b[2], b[1]), (b[2], b[3]), color, width, jitter)
        sketch_line(d, (b[2], b[3]), (b[0], b[3]), color, width, jitter)
        sketch_line(d, (b[0], b[3]), (b[0], b[1]), color, width, jitter)


def sketch_ellipse(d, box, color, width=3, jitter=1.6):
    x0, y0, x1, y1 = box
    d.ellipse(box, outline=color, width=width)
    d.ellipse((x0 + 1.5, y0 + 1.5, x1 - 1.5, y1 - 1.5), outline=color, width=max(2, width - 1))


def draw_star(d, cx, cy, r, color, width=3):
    for ang in [0, 90]:
        dx, dy = r * np.cos(np.radians(ang)), r * np.sin(np.radians(ang))
        sketch_line(d, (cx - dx, cy - dy), (cx + dx, cy + dy), color, width, 0.8, 4)
    for ang in [45, 135]:
        dx, dy = r * 0.45 * np.cos(np.radians(ang)), r * 0.45 * np.sin(np.radians(ang))
        sketch_line(d, (cx - dx, cy - dy), (cx + dx, cy + dy), color, width, 0.6, 3)


def draw_sun(d, cx, cy, r, color):
    sketch_ellipse(d, (cx - r, cy - r, cx + r, cy + r), color, 3)
    for ang in range(0, 360, 45):
        a = np.radians(ang)
        sketch_line(d, (cx + (r + 8) * np.cos(a), cy + (r + 8) * np.sin(a)),
                    (cx + (r + 20) * np.cos(a), cy + (r + 20) * np.sin(a)), color, 3, 1.0, 3)


def draw_cloud(d, cx, cy, s, color):
    w, h = s, s * 0.55
    d.arc((cx - w / 2, cy - h, cx - w / 6, cy + h * 0.3), 150, 350, fill=color, width=3)
    d.arc((cx - w / 3, cy - h * 1.2, cx + w / 3, cy + h * 0.4), 160, 20, fill=color, width=3)
    d.arc((cx + w / 6, cy - h, cx + w / 2, cy + h * 0.3), 190, 30, fill=color, width=3)
    sketch_line(d, (cx - w / 2 + 4, cy + h * 0.25), (cx + w / 2 - 4, cy + h * 0.25), color, 3, 1.2, 6)


def draw_arrow(d, cx, cy, ln, color, width=4):
    sketch_line(d, (cx - ln / 2, cy), (cx + ln / 2, cy), color, width, 1.4, 8)
    sketch_line(d, (cx + ln / 2, cy), (cx + ln / 2 - 22, cy - 14), color, width, 1.2, 3)
    sketch_line(d, (cx + ln / 2, cy), (cx + ln / 2 - 22, cy + 14), color, width, 1.2, 3)


def draw_bubble(d, box, color):
    x0, y0, x1, y1 = box
    sketch_ellipse(d, box, color, 3)
    d.ellipse((x0 + 18, y1 - 6, x0 + 44, y1 + 20), outline=color, width=3)
    d.ellipse((x0 + 2, y1 + 12, x0 + 22, y1 + 32), outline=color, width=3)


def draw_title(d, text, cx, y, size, color, font=None):
    """居中大标题 + 下方红色小波浪线"""
    font = font or f_kai(size)
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    d.text((cx - tw / 2 - bbox[0], y - bbox[1]), text, font=font, fill=color)
    x0, x1 = cx - tw / 2 + 6, cx + tw / 2 - 6
    pts = [(x0 + (x1 - x0) * i / 24, y + size + 16 + 6 * np.sin(i / 24 * np.pi * 3))
           for i in range(25)]
    d.line(pts, fill=RED, width=4, joint="curve")


def draw_label_card(d, box, text, font, ink=INK, text_color=None):
    """元素标签：手绘双线牌 + 居中文字"""
    x0, y0, x1, y1 = box
    sketch_rect(d, box, ink, 3, 1.4)
    tc = text_color or ink
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((x0 + x1) / 2 - tw / 2 - bbox[0], (y0 + y1) / 2 - th / 2 - bbox[1]),
           text, font=font, fill=tc)


def draw_stamp(d, cx, cy, r, text):
    """完结印章：双圈 + 文字"""
    sketch_ellipse(d, (cx - r, cy - r, cx + r, cy + r), RED, 4)
    sketch_ellipse(d, (cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10), RED, 3)
    font = f_kai(34)
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), text, font=font, fill=RED)


def draw_note(d, im, box, text, font=None, tape=True):
    """便签条：轮廓 + 淡色底 + 右上折角 + 居中文字（+ 左上胶带）"""
    x0, y0, x1, y1 = box
    sketch_rect(d, box, INK, 3, 1.5)
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((x0 + 6, y0 + 6, x1 - 6, y1 - 6), fill=PAPER_LIGHT + (70,))
    im.alpha_composite(overlay)
    d = ImageDraw.Draw(im)
    sketch_line(d, (x1 - 40, y0), (x1, y0 + 40), INK, 3, 1.2, 3)
    sketch_line(d, (x1 - 40, y0), (x1 - 40, y0 + 40), INK, 3, 1.0, 3)
    sketch_line(d, (x1 - 40, y0 + 40), (x1, y0 + 40), INK, 3, 1.0, 3)
    font = font or f_kai(42)
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((x0 + x1) / 2 - tw / 2 - bbox[0], (y0 + y1) / 2 - th / 2 - bbox[1]),
           text, font=font, fill=INK)
    if tape:
        d.rectangle((x0 + 30, y0 - 12, x0 + 110, y0 + 10), fill=(210, 190, 150),
                    outline=INK, width=2)


# ---------------- 手部素材去字 ----------------

def clean_hand_text(src, dst, fill_v=252, kernel=61):
    """涂掉手部素材笔杆上的文字（V01 十四轮迭代的最终可靠方案）。

    文字 = 纯白笔杆区内部的暗洞。用形态学闭运算填补白区内部的孔洞：
    只碰文字像素，不碰手指描边与笔杆边缘。
    典型战绩：V01 清除 11537 像素，手指/描边零损伤。
    """
    import cv2
    a = np.asarray(Image.open(src).convert("RGBA")).copy()
    r = a[..., 0].astype(int)
    g = a[..., 1].astype(int)
    b = a[..., 2].astype(int)
    al = a[..., 3]
    gray = (r + g + b) / 3
    white = ((gray > 240) & (al > 200) &
             (np.abs(r - g) < 6) & (np.abs(g - b) < 6)).astype(np.uint8)
    white_clean = cv2.morphologyEx(white, cv2.MORPH_CLOSE, np.ones((kernel, kernel), np.uint8))
    holes = (white_clean > 0) & (white == 0)
    a[holes, 0:3] = fill_v
    Image.fromarray(a).save(dst)
    return int(holes.sum())
