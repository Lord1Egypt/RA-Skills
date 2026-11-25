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
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

INK = (74, 74, 74)
RED = (192, 57, 43)
ORANGE = (230, 126, 34)
BLUE = (46, 134, 193)
PAPER_LIGHT = (248, 242, 227)

MARGIN = 24          # 画布安全留白（1536×864 画布像素）
EDGE_MARGIN = 8      # 小于此值视为贴边（缩放到 1080×600 后仅 ~6px）

# ---- 安全区（v1.4）：图元「画之前」就被夹进这里，而不是画完再靠人工发现 ----
# 1536×864 → 1080×600 缩放系数 0.703，所以 32px 画布边距 ≈ 22px 成片边距，
# 34px 顶边距 ≈ 24px，肉眼看上去才是「有留白」而不是「贴着边」。
SAFE_MARGIN = 34     # 左/右/下 最小距离
SAFE_TOP = 36        # 上 最小距离（标题更吃视觉，单独给大一档）
SUB_BAND_TOP = 756   # 字幕带上沿：y1 超过这条线，烧录后会被硬字幕压住
ENFORCE_SAFE = True  # 总开关（个别老片子要保持原样时可临时关掉）


def clamp_box(box, im=None, margin=None, top=None, bottom=None, tag=""):
    """把矩形整体移进安全区：不缩放（除非本身就比安全区还大），只平移。

    为什么是「平移」而不是「改绘制坐标」：绘制代码里的坐标是设计意图，
    自动钳制只在越界时兜底，并且打印 [clamp] 让作者知道哪块被挪了。
    """
    if im is None or not ENFORCE_SAFE:
        return box
    W, H = im.size
    m = SAFE_MARGIN if margin is None else margin
    t = SAFE_TOP if top is None else top
    b = SUB_BAND_TOP if bottom is None else bottom
    x0, y0, x1, y1 = [float(v) for v in box]
    w, h = x1 - x0, y1 - y0
    if w > W - 2 * m:
        w = W - 2 * m
    if h > b - t:
        h = b - t
    nx0 = min(max(x0, m), W - m - w)
    ny0 = min(max(y0, t), b - h)
    out = (nx0, ny0, nx0 + w, ny0 + h)
    if any(abs(a - c) > 0.5 for a, c in zip(out, (x0, y0, x1, y1))):
        print(f"  [clamp] {tag or 'box'} ({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})"
              f" → ({out[0]:.0f},{out[1]:.0f},{out[2]:.0f},{out[3]:.0f})")
    return out


def clamp_center(cx, cy, r, im, tag=""):
    """圆/星形图元：把圆心夹到「圆心 ± r 仍在安全区内」。"""
    if im is None or not ENFORCE_SAFE:
        return cx, cy
    W, H = im.size
    ncx = min(max(cx, SAFE_MARGIN + r), W - SAFE_MARGIN - r)
    ncy = min(max(cy, SAFE_TOP + r), SUB_BAND_TOP - r)
    if abs(ncx - cx) > 0.5 or abs(ncy - cy) > 0.5:
        print(f"  [clamp] {tag or 'center'} ({cx:.0f},{cy:.0f}) → ({ncx:.0f},{ncy:.0f})")
    return ncx, ncy

FONT_KAI = r"C:\Windows\Fonts\simkai.ttf"
FONT_YAHEI_BD = r"C:\Windows\Fonts\msyhbd.ttc"


def f_kai(size):
    return ImageFont.truetype(FONT_KAI, size)


def f_yahei(size):
    return ImageFont.truetype(FONT_YAHEI_BD, size)


# ---------------- 文字度量与自适应（防「文字贴边/被裁」核心工具） ----------------

def text_size(font, text):
    """单行文字的 (宽, 高)，已扣除字体自带的上下留白偏移。"""
    bb = font.getbbox(text)
    return bb[2] - bb[0], bb[3] - bb[1]


def block_size(font, lines, line_gap=8):
    """多行文字的 (宽, 高)。"""
    ws, hs = [], []
    for t in lines:
        w, h = text_size(font, t)
        ws.append(w)
        hs.append(h)
    return (max(ws) if ws else 0), sum(hs) + line_gap * max(0, len(lines) - 1)


def fit_font(font, lines, max_w, max_h=None, line_gap=8, min_size=13, tag=""):
    """把字号缩到刚好塞进 max_w × max_h，返回可用字体。

    这是「文字显示不全」的根治手段：定死字号 + 定死框宽 = 长句必然溢出框、
    甚至溢出画布。改成按可用宽度反算字号后，任何文案都不会破框。
    """
    lines = list(lines)
    size = int(getattr(font, "size", 24))
    while size > min_size:
        f = font.font_variant(size=size)
        w, h = block_size(f, lines, line_gap)
        if w <= max_w and (max_h is None or h <= max_h):
            if size != getattr(font, "size", size):
                print(f"    [fit] {tag or 'text'} 字号 {getattr(font, 'size', '?')}→{size}"
                      f"（限宽 {int(max_w)}px）")
            return f
        size -= 1
    f = font.font_variant(size=min_size)
    w, h = block_size(f, lines, line_gap)
    if w > max_w:
        print(f"    [text-overflow!] {tag or 'text'} 最小字号 {min_size} 仍超宽 "
              f"{int(w)}>{int(max_w)}px —— 请缩短文案或加宽框")
    return f


def safe_text(d, xy, text, font, fill=INK, box=None, pad=12, tag="text",
              line_gap=8, anchor=None):
    """画文字 + 越界自检；box 给定时先按框自动缩字号。

    与裸 d.text() 的区别：裸调用画到哪算哪，画布外/框外照样「画上去」，
    要到成片抽帧才发现贴边或被遮罩裁掉。这里画之前就量、就缩、就报警。

    xy 为左上角；box=(x0,y0,x1,y1) 时 xy 会被忽略并居中。
    """
    lines = text if isinstance(text, (list, tuple)) else [text]
    if box is not None:
        box = clamp_box(box, d.im, tag=f"{tag}:{str(text)[:12]}")
        _check_bounds(d.im, box, f"{tag}_box", margin=EDGE_MARGIN)
        x0, y0, x1, y1 = box
        avail_w, avail_h = (x1 - x0) - pad * 2, (y1 - y0) - pad * 2
        font = fit_font(font, lines, avail_w, avail_h, line_gap, tag=tag)
        tw, th = block_size(font, lines, line_gap)
        cx, cy = (x0 + x1) / 2 - tw / 2, (y0 + y1) / 2 - th / 2
    else:
        cx, cy = xy

    for t in lines:
        bb = font.getbbox(t)
        tw = bb[2] - bb[0]
        px = cx - bb[0] if box is not None else cx - bb[0]
        if anchor == "mid":
            px = cx - tw / 2 - bb[0]
        py = cy - bb[1]
        bb_abs = (px + bb[0], py + bb[1], px + bb[2], py + bb[3])
        _check_bounds(d.im, bb_abs, tag, margin=EDGE_MARGIN)
        d.text((px, py), t, font=font, fill=fill)
        cy += (bb[3] - bb[1]) + line_gap
    return font


def draw_text_center(d, cx, cy, text, font, fill=INK, tag="text", do_clamp=True):
    """居中写一行文字，并把它**真实的墨迹矩形**夹进安全区。

    为什么不用 d.text 直接算：`textbbox` 返回的是「绘制原点坐标系」的框，字体的
    ascender 留白会让墨迹比原点低 10~18px。按原点钳制会出现「日志说已夹到 756，
    实拍却在 772」的偏差（项目1 V03 第二幕实测）。这里统一按墨迹框钳制。
    """
    bb = d.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    ox = cx - tw / 2 - bb[0]
    oy = cy - th / 2 - bb[1]
    if do_clamp and d.im is not None:
        ink = (ox + bb[0], oy + bb[1], ox + bb[2], oy + bb[3])
        nb = clamp_box(ink, d.im, tag=f"{tag}:{str(text)[:10]}")
        ox += nb[0] - ink[0]
        oy += nb[1] - ink[1]
    d.text((ox, oy), text, font=font, fill=fill)
    return (ox + bb[0], oy + bb[1], ox + bb[2], oy + bb[3])


# ---------------- 布局记录器（让 spec 与实际绘制坐标永不漂移） ----------------

class _Layout:
    """随手绘图元登记自身的 bbox，供 make_spec.py 生成 region。

    为什么需要：region 坐标一旦靠手写维护，就会和 enhance_scenes.py 的绘制坐标
    漂移——项目3 就是因为「便签上移了、spec 里的 y 没跟着改」，13 幕出现整块
    内容永远不被揭示（成片里根本没有那块字）。
    """

    def __init__(self):
        self.elements = []
        self.canvas = None

    def begin(self, im):
        self.elements = []
        self.canvas = {"width": im.size[0], "height": im.size[1]}
        return self

    def add(self, tag, box):
        x0, y0, x1, y1 = [int(round(v)) for v in box]
        self.elements.append({"tag": str(tag)[:24], "x": x0, "y": y0,
                              "width": max(1, x1 - x0), "height": max(1, y1 - y0)})
        return self.elements[-1]

    def save(self, path):
        import json
        if not self.canvas:
            print("  [layout!] 未调用 LAYOUT.begin(im)，画布尺寸未知")
        json.dump({"canvas": self.canvas, "elements": self.elements},
                  open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"  layout -> {path}（{len(self.elements)} 块）")


LAYOUT = _Layout()


def _bg_color(im) -> np.ndarray:
    """四角采样中位数，作为该图的纸张/底色基准（深色背景图同样适用）。"""
    arr = np.asarray(im.convert("RGB"), dtype=np.float32)
    h, w = arr.shape[:2]
    m = max(3, min(h, w) // 50)
    corners = np.concatenate([
        arr[:m, :m].reshape(-1, 3), arr[:m, -m:].reshape(-1, 3),
        arr[-m:, :m].reshape(-1, 3), arr[-m:, -m:].reshape(-1, 3),
    ])
    return np.median(corners, axis=0)


def clear_area(im, box, feather=22):
    """软边清除 box 内的图像内容（用四角采样的底色覆盖）。

    用途：ImageGen 线稿常自带英文/中文标题（如 SCORECARD、Hands-on Operations），
    与增强中文标题同位冲突导致「文字看不清」。高斯羽化边缘避免生硬切割，
    深色背景图自动取深色底，同样适用。
    """
    _check_bounds(im, box, "clear_area")
    x0, y0, x1, y1 = [int(v) for v in box]
    w, h = im.size
    arr = np.asarray(im.convert("RGB"), dtype=np.float32)
    bg = _bg_color(im)
    mask = np.zeros((h, w), dtype=np.float32)
    mask[y0:y1, x0:x1] = 1.0
    k = feather * 2 + 1
    mask = cv2.GaussianBlur(mask, (k, k), feather / 2.5)[..., None]
    out = arr * (1.0 - mask) + bg[None, None, :] * mask
    im.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)))
    print(f"  clear_area {box} done")


def _check_bounds(im, box, tag="", margin=0):
    """画布越界/贴边自检。

    教训：
    - 项目2 V02 第三幕第 4 张口诀卡 x+width=1550 > 画布宽 1536，右边缘被裁，
      却直到成片质检才发现。
    - 项目3 十二片：40 余处图元贴边或压在 region 边界上，成片里表现为
      「文字显示不全」。所以在越界之外，还要对 margin 内的「贴边」告警。

    margin>0 时，落入 margin 内即报 [edge!]（缩放到 1080×600 后只剩几像素）。
    """
    w, h = im.size
    x0, y0, x1, y1 = [float(v) for v in box]
    if x0 < 0 or y0 < 0 or x1 > w or y1 > h:
        print(f"  [bounds!] {tag} box=({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f}) 超出画布 {w}x{h}")
        return False
    if margin > 0 and (x0 < margin or y0 < margin or x1 > w - margin or y1 > h - margin):
        side = []
        if x0 < margin:
            side.append(f"左 {margin - int(x0)}px")
        if y0 < margin:
            side.append(f"上 {margin - int(y0)}px")
        if x1 > w - margin:
            side.append(f"右 {int(x1) - (w - margin)}px")
        if y1 > h - margin:
            side.append(f"下 {int(y1) - (h - margin)}px")
        print(f"  [edge!] {tag} 贴边({', '.join(side)}) —— 成片里会压到画面边缘，请内缩")
    return True


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
    _check_bounds(d.im, box, "sketch_rect")
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
    cx, cy = clamp_center(cx, cy, r, d.im if hasattr(d, "im") else None, "star")
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


def draw_title(d, text, cx, y, size, color, font=None, panel=False):
    """居中大标题 + 下方红色小波浪线。

    panel=True 时先铺一块近不透明的纸色圆角底板并描手绘边：
    线稿顶部有插画/纹理、无法用 clear_area 清除时（如人物头部、深色背景），
    用底板保证标题在任何背景上都可读。

    v1.4：标题会被自动夹进安全区（y ≥ SAFE_TOP、左右各留 SAFE_MARGIN）。
    项目1 十部片子的标题原先都写在 y=18~22，成片里字顶距画面只 13px，
    肉眼就是「贴着边」——这是用户反馈「文字在边缘、显示不全」的主因。
    """
    font = font or f_kai(size)
    # 标题限宽 = 画布宽 - 两侧安全留白；超宽自动缩字号，绝不画到边上
    avail = d.im.size[0] - SAFE_MARGIN * 2
    font = fit_font(font, [text], avail, None, tag="title")
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    ny = max(y, SAFE_TOP)
    ncxx = min(max(cx, SAFE_MARGIN + tw / 2), d.im.size[0] - SAFE_MARGIN - tw / 2)
    if abs(ny - y) > 0.5 or abs(ncxx - cx) > 0.5:
        print(f"  [clamp] title「{text}」 cx {cx:.0f}→{ncxx:.0f}  y {y:.0f}→{ny:.0f}")
    cx, y = ncxx, ny
    tx, ty = cx - tw / 2 - bbox[0], y - bbox[1]
    if panel:
        px0, py0 = cx - tw / 2 - 28, y - 26
        px1, py1 = cx + tw / 2 + 28, y + size + 30
        _check_bounds(d.im, (px0, py0, px1, py1), "title_panel")
        # 用本图纸色铺实心底：既完全盖住线稿，又不会显出一块偏白的补丁
        d.rounded_rectangle((px0, py0, px1, py1), radius=14, fill=_page_rgb(d.im))
        sketch_rect(d, (px0, py0, px1, py1), color, 2, 1.2)
    d.text((tx, ty), text, font=font, fill=color)
    # 红色手绘波浪下划线：紧贴标题底部（y+size+7±5），不要下探到副标题
    # v1.4：原为 y+size+16±6（下探 22px），把紧随其后的副标题/小字顶到线下，
    # 视觉上像被红线划掉（项目1 V04 直接重叠、V02/V03/V09 只差 1–3px）。
    x0, x1 = cx - tw / 2 + 6, cx + tw / 2 - 6
    pts = [(x0 + (x1 - x0) * i / 24, y + size + 7 + 5 * np.sin(i / 24 * np.pi * 3))
           for i in range(25)]
    d.line(pts, fill=RED, width=4, joint="curve")
    LAYOUT.add(f"title:{text}", (tx, ty, tx + tw, ty + (size + 14)))


def _page_rgb(im) -> tuple[int, int, int]:
    """该图纸张底色（四角采样中位数）→ RGB 整数元组。

    填充一律用「本图纸色」而非固定的 PAPER_LIGHT：
    固定色与匀纸后的页面存在色差，卡片/便签会变成一块明显偏白的补丁；
    半透明又会让底下线稿透出来压字（用户两次反馈都与此有关）。
    → 纸色 + 全不透明 = 既盖住线稿、又与页面浑然一体。
    """
    return tuple(int(round(v)) for v in _bg_color(im))


def _opaque_fillover(im, box, color=None, alpha=255, inset=6, radius=0):
    """在 im 上铺一块底（盖住底下线稿，保证文字可读）。color 缺省取本图纸色。"""
    x0, y0, x1, y1 = box
    if color is None:
        color = _page_rgb(im)
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((x0 + inset, y0 + inset, x1 - inset, y1 - inset),
                 fill=color + (alpha,))
    im.alpha_composite(overlay)


def draw_label_card(d, box, text, font, ink=INK, text_color=None, line_gap=8, pad=16):
    """元素标签：近不透明纸底 + 手绘双线牌 + 居中文字。

    底必须近乎不透明：半透明底会让底下线稿透出来压住文字（用户反馈「绘画与
    文字重叠看不见文字」的直接原因之一）。

    text 可以是 str（单行）或 list[str]（多行，逐行居中；块内窄卡必备）。
    文字会按卡片内宽自动缩字号——定死字号 + 窄卡片必然溢出牌外，成片里就是
    「字跑出框外被裁」。
    """
    box = clamp_box(box, d.im, tag="card:" + str(text)[:12])
    _check_bounds(d.im, box, "label_card", margin=EDGE_MARGIN)
    x0, y0, x1, y1 = box
    d.rectangle((x0 + 6, y0 + 6, x1 - 6, y1 - 6), fill=_page_rgb(d.im))
    sketch_rect(d, box, ink, 3, 1.4)
    tc = text_color or ink
    lines = text if isinstance(text, (list, tuple)) else [text]
    font = fit_font(font, lines, (x1 - x0) - pad * 2, (y1 - y0) - pad, line_gap,
                    tag="label_card")
    heights = []
    for t in lines:
        bb = d.textbbox((0, 0), t, font=font)
        heights.append(bb[3] - bb[1])
    total_h = sum(heights) + line_gap * (len(lines) - 1)
    cy = (y0 + y1) / 2 - total_h / 2
    for t, th in zip(lines, heights):
        bb = d.textbbox((0, 0), t, font=font)
        tw = bb[2] - bb[0]
        d.text(((x0 + x1) / 2 - tw / 2 - bb[0], cy - th / 2 - bb[1]),
               t, font=font, fill=tc)
        cy += th + line_gap
    LAYOUT.add("card:" + str(lines[0])[:16], box)


def draw_stamp(d, cx, cy, r, text):
    """完结印章：双圈 + 文字。

    v1.4：①圆心夹进安全区（原 V02/V09 的印章圆心距右边缘仅 4px，成片里被裁）；
    ②文字按内圆直径自动缩字号——「分水岭」「三地合规」这类长印文原来会顶出圆外。
    """
    cx, cy = clamp_center(cx, cy, r, d.im if hasattr(d, "im") else None, "stamp:" + str(text))
    sketch_ellipse(d, (cx - r, cy - r, cx + r, cy + r), RED, 4)
    sketch_ellipse(d, (cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10), RED, 3)
    font = fit_font(f_kai(34), [text], (r - 14) * 2, None, tag="stamp")
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), text, font=font, fill=RED)


def draw_note(d, im, box, text, font=None, tape=True, pad=24, line_gap=8):
    """便签条：轮廓 + 近不透明纸底 + 右上折角 + 居中文字（+ 左上胶带）。

    底近乎不透明（alpha 255），盖住底下线稿——此前 alpha 70 的半透明底
    会透出线稿压住文字，导致「绘画与文字重叠看不见文字」。

    ⚠️ 所有装饰（胶带、折角）都必须画在 box 之内：胶带原先画在 y0-12，
    而 annotation region 从 y0 起算，导致 27 个场景的胶带上沿 12px 永远不被
    揭示（项目3 版式体检固定复现）。文字同样按内宽自动缩字号。
    """
    box = clamp_box(box, im, tag="note:" + str(text)[:12])
    _check_bounds(im, box, "note", margin=EDGE_MARGIN)
    x0, y0, x1, y1 = box
    _opaque_fillover(im, box, _page_rgb(im), 255)
    d = ImageDraw.Draw(im)
    sketch_rect(d, box, INK, 3, 1.5)
    sketch_line(d, (x1 - 40, y0), (x1, y0 + 40), INK, 3, 1.2, 3)
    sketch_line(d, (x1 - 40, y0), (x1 - 40, y0 + 40), INK, 3, 1.0, 3)
    sketch_line(d, (x1 - 40, y0 + 40), (x1, y0 + 40), INK, 3, 1.0, 3)
    lines = text if isinstance(text, (list, tuple)) else [text]
    font = font or f_kai(42)
    font = fit_font(font, lines, (x1 - x0) - pad * 2, (y1 - y0) - pad, line_gap,
                    tag="note")
    heights = []
    for t in lines:
        bb = d.textbbox((0, 0), t, font=font)
        heights.append(bb[3] - bb[1])
    total_h = sum(heights) + line_gap * (len(lines) - 1)
    cy = (y0 + y1) / 2 - total_h / 2
    for t, th in zip(lines, heights):
        bb = d.textbbox((0, 0), t, font=font)
        tw = bb[2] - bb[0]
        d.text(((x0 + x1) / 2 - tw / 2 - bb[0], cy - th / 2 - bb[1]),
               t, font=font, fill=INK)
        cy += th + line_gap
    if tape:
        # 胶带画在框内（y0+2 起），不再越过上边界
        d.rectangle((x0 + 30, y0 + 2, x0 + 110, y0 + 24), fill=(210, 190, 150),
                    outline=INK, width=2)
    LAYOUT.add("note:" + str(lines[0])[:16], box)


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
