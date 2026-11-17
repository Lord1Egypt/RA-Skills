#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信投稿素材包生成器 —— 严格按微信表情开放平台规范产出全部素材

自动生成：
  表情图/01.png…       240×240  PNG     ≤500KB   8~24 张
  缩略图/01.png…       120×120  PNG     ≤500KB
  表情封面图.png        240×240  PNG 透明底  ≤500KB
  聊天面板图标.png       50×50   PNG 透明底  ≤100KB
  详情页横幅.jpg        750×400  JPG 非白底  ≤500KB（无文字、带主题元素）
  赞赏引导图.png / 赞赏致谢图.png（可选，--with-tips）
  投稿清单.md           逐项校验结果

用法:
  # 从已加文案的图生成全套素材并打包（主图保留背景最稳妥）
  python scripts/wechat_pack.py --input ./sticker_out --name "生肖打工人" --zip

  # 完整投稿流程：主图带背景；封面/图标/横幅/赞赏图用圆形徽章（防暗夜掏洞）
  python scripts/wechat_pack.py --input ./sticker_out --raw-src ./cleaned --banner-src ./cleaned \
      --cover 01.png --icon 09.png --with-tips --zip --name "专辑名"

  # 高对比素材（主体与背景色距大）可用抠图模式
  python scripts/wechat_pack.py ... --transparent --showcase-style cutout

  # 图标裁剪不理想时微调：span=特写范围(越小越紧)，cy=特写中心高度(越小越靠上)
  python scripts/wechat_pack.py ... --icon 09.png --icon-span 0.40 --icon-cy 0.28

  # 只校验已有素材目录
  python scripts/wechat_pack.py --check ./wechat_submit
"""
import argparse
import os
import random
import sys
import zipfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    sys.exit("[缺少依赖] 请先安装：pip install Pillow")

IMG_EXT = (".png", ".jpg", ".jpeg", ".webp", ".bmp")

# 微信表情开放平台规范（见 references/wechat-spec.md）
SPEC = {
    "sticker": dict(size=(240, 240), fmt="PNG", max_kb=500, n=(8, 24)),
    "thumb": dict(size=(120, 120), fmt="PNG", max_kb=500),
    "cover": dict(size=(240, 240), fmt="PNG", max_kb=500, alpha=True),
    "icon": dict(size=(50, 50), fmt="PNG", max_kb=100, alpha=True),
    "banner": dict(size=(750, 400), fmt="JPG", max_kb=500, no_white=True),
    "tip_guide": dict(size=(750, 560), fmt="PNG", max_kb=500),
    "tip_thanks": dict(size=(750, 750), fmt="PNG", max_kb=500),
}


def kb(path):
    return os.path.getsize(path) / 1024


# ---------------------------------------------------------------- 图像处理

def square_crop(img):
    w, h = img.size
    if w == h:
        return img
    s = min(w, h)
    return img.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))


def visibility(img):
    """返回 (平均亮度, 深色像素占比)。
    过浅（>185）→ 暗夜模式无填充感，审核驳回；深色像素（<60）在暗夜背景上会融合。"""
    small = img.convert("RGBA").resize((64, 64))
    raw = small.tobytes()
    total, dark, cnt = 0.0, 0, 0
    for i in range(0, len(raw), 4):
        if raw[i + 3] > 40:
            l = 0.299 * raw[i] + 0.587 * raw[i + 1] + 0.114 * raw[i + 2]
            total += l
            cnt += 1
            if l < 60:
                dark += 1
    return (total / cnt if cnt else 255.0), (dark / cnt if cnt else 0.0)


def subject_bbox(img, thresh=40):
    """不透明像素的紧致边界框（用于测量主体占画面比例）"""
    a = img.getchannel("A").point(lambda v: 255 if v > thresh else 0)
    return a.getbbox()


def zoom_to_canvas(img, canvas_size, fill=0.86):
    """按主体 bbox 裁剪并放大到占画布 fill 比例，居中放在透明画布上。
    解决"整幅场景缩到 50px 图标里主体小到看不清"的驳回问题。"""
    bbox = subject_bbox(img)
    if not bbox:
        return img.resize((canvas_size, canvas_size), Image.LANCZOS)
    im = img.crop(bbox)
    side = int(canvas_size * fill)
    scale = side / max(im.size)
    im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    canvas.paste(im, ((canvas_size - im.width) // 2, (canvas_size - im.height) // 2), im)
    return canvas


def head_crop(img, span=0.44, cy=0.30):
    """取原图上中部方形区域做头像特写（chibi 构图的头部集中在画面上中部）。
    span=方形边长占短边比例，cy=方形中心高度占画面高度比例。"""
    w, h = img.size
    s = int(min(w, h) * span)
    cx, cyy = int(w * 0.5), int(h * cy)
    x0 = max(0, min(w - s, cx - s // 2))
    y0 = max(0, min(h - s, cyy - s // 2))
    return img.crop((x0, y0, x0 + s, y0 + s))


def add_outline(img, width_ratio=0.05, dark_ratio=0.42):
    """给透明主体加同色系深色描边（微信暗夜模式下浅色形象需要，否则审核驳回）
    描边色 = 主体平均色 × dark_ratio，保持黏土风协调；并给主体留出边距。"""
    img = img.convert("RGBA")
    w, h = img.size
    # 采样主体平均色
    raw = img.resize((64, 64)).tobytes()
    rs = gs = bs = cnt = 0
    for i in range(0, len(raw), 4):
        if raw[i + 3] > 128:
            rs += raw[i]; gs += raw[i + 1]; bs += raw[i + 2]; cnt += 1
    if cnt:
        avg = (rs // cnt, gs // cnt, bs // cnt)
        stroke_color = tuple(int(v * dark_ratio) for v in avg)
    else:
        stroke_color = (58, 58, 58)

    # 主体缩小留边距，再膨胀 alpha 做描边
    margin = max(6, int(min(w, h) * 0.07))
    inner = img.resize((w - margin * 2, h - margin * 2), Image.LANCZOS)
    bw = max(2, int(min(w, h) * width_ratio) // 2)
    big = inner.getchannel("A").filter(ImageFilter.MaxFilter(bw * 2 + 1))
    stroke = Image.new("RGBA", (inner.width, inner.height), stroke_color + (255,))
    stroke.putalpha(big)
    stroked = Image.alpha_composite(stroke, inner)

    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.paste(stroked, (margin, margin), stroked)
    return canvas


def circle_badge(img, ring_ratio=0.035, feather=2):
    """圆形徽章裁切：图片内容裁成圆，圆外透明，外圈加同色系深色描边环。
    奶白黏土主体与奶油渐变背景色距过近，阈值抠图必然掏洞或残留
    （审核驳回"角色没有填充颜色、暗夜模式无法辨识"的根源）。
    圆形徽章不抠像素、确定性 100%，圆外透明合规，描边环保证暗夜模式可见。"""
    s = img.size[0]
    img = img.convert("RGBA")

    # 描边环颜色 = 图片边框平均色 × 0.62（同色系加深，明暗底都分离）
    raw = img.tobytes()
    w, h = img.size
    tot = [0, 0, 0]
    cnt = 0
    for x in range(0, w, max(1, w // 40)):
        for y in (0, h - 1):
            j = (y * w + x) * 4
            tot[0] += raw[j]; tot[1] += raw[j + 1]; tot[2] += raw[j + 2]
            cnt += 1
    for y in range(0, h, max(1, h // 40)):
        for x in (0, w - 1):
            j = (y * w + x) * 4
            tot[0] += raw[j]; tot[1] += raw[j + 1]; tot[2] += raw[j + 2]
            cnt += 1
    edge = tuple(v // cnt for v in tot)
    ring_col = tuple(int(v * 0.62) for v in edge) + (255,)

    scale = 4  # 4x 超采样画圆再缩小，边缘抗锯齿
    big = s * scale
    ring_w = max(2, int(s * ring_ratio))

    mask_circle = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask_circle).ellipse(
        [ring_w * scale, ring_w * scale, big - ring_w * scale, big - ring_w * scale],
        fill=255)
    mask_ring = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask_ring).ellipse([0, 0, big, big], fill=255)

    canvas = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ring = Image.new("RGBA", (s, s), ring_col)
    ring.putalpha(mask_ring.resize((s, s), Image.LANCZOS))
    canvas.paste(ring, (0, 0), ring)
    body = img.copy()
    body.putalpha(mask_circle.resize((s, s), Image.LANCZOS))
    canvas.alpha_composite(body)
    return canvas


def make_transparent(img, tol=42):
    """把与画面边缘连通的背景区域设为透明（主色色距 × 局部步进 双条件洪泛）。

    旧版按"与背景色的全局色距"抠图，会把颜色与背景相近的浅色主体内部
    一起抠掉，形象千疮百孔——这正是微信审核"角色形象没有填充颜色，
    暗夜模式下无法清晰辨识"的根源（白底预览看不出，暗夜气泡里全是洞）。
    现规则（两个条件须同时满足才吞掉一个像素）：
      1) 与边框主色的色距 ≤ tol*1.45 —— 保证只吞背景色系，浅色脸部不达标即停；
      2) 与来路像素的局部色差 ≤ max(6, tol//4) —— 沿平滑渐变爬行，遇轮廓截止；
      3) 且必须与画面边缘连通 —— 被主体包住的区域永远不会被误抠。
    tol 语义：抠图强度，默认 42；主体被误抠→调小，背景残留→调大。"""
    from collections import Counter, deque
    img = img.convert("RGBA")
    w, h = img.size
    n = w * h
    raw = img.tobytes()
    border = (list(range(0, w)) + list(range(n - w, n))
              + list(range(0, n, w)) + list(range(w - 1, n, w)))

    # 背景参考色 = 边框像素主色（量化取众数）。只用单一主色：
    # 多参考色会把与背景同色系的浅色主体（白脸/白爪）也当成背景吃掉。
    bucket = Counter()
    for i in border:
        j = i * 4
        bucket[(raw[j] // 12, raw[j + 1] // 12, raw[j + 2] // 12)] += 1
    key = bucket.most_common(1)[0][0]
    bg = (key[0] * 12 + 6, key[1] * 12 + 6, key[2] * 12 + 6)

    tol_g = int(tol * 1.45)
    step = max(6, tol // 4)

    def dist(i):
        j = i * 4
        return (abs(raw[j] - bg[0]) + abs(raw[j + 1] - bg[1])
                + abs(raw[j + 2] - bg[2]))

    bg_mask = bytearray(n)
    dq = deque()
    # 种子从严：只有明确的背景色才能从边缘起洪泛（tol*0.8）。
    # 主体（白爪/白脸）与背景色距通常在 0.8~1.4 倍 tol 之间，
    # 若用 tol_g 做种子阈值，踩到画面边界的白色爪子会把洪泛引进主体内部。
    for i in border:
        if dist(i) <= int(tol * 0.8):
            bg_mask[i] = 1
            dq.append(i)
    while dq:
        i = dq.popleft()
        j = i * 4
        ri, gi, bi = raw[j], raw[j + 1], raw[j + 2]
        x, y = i % w, i // w
        for k in ((i - 1) if x > 0 else -1, (i + 1) if x < w - 1 else -1,
                  (i - w) if y > 0 else -1, (i + w) if y < h - 1 else -1):
            if k >= 0 and not bg_mask[k]:
                m = k * 4
                if (abs(raw[m] - ri) + abs(raw[m + 1] - gi) + abs(raw[m + 2] - bi)) <= step \
                        and dist(k) <= tol_g:
                    bg_mask[k] = 1
                    dq.append(k)

    # 清除角落背景残留：主体=最大不透明连通域；其余贴着画面边缘的
    # 连通域都是没被主色罩住的背景块（渐变暗角、异色墙面），整体清透明。
    comp = [-1] * n
    comps = []  # (size, touches_border)
    for s in range(n):
        if bg_mask[s] or comp[s] >= 0:
            continue
        cid = len(comps)
        size = 0
        touch = False
        comp[s] = cid
        dq2 = deque([s])
        while dq2:
            i = dq2.popleft()
            size += 1
            x, y = i % w, i // w
            if x == 0 or x == w - 1 or y == 0 or y == h - 1:
                touch = True
            for k in ((i - 1) if x > 0 else -1, (i + 1) if x < w - 1 else -1,
                      (i - w) if y > 0 else -1, (i + w) if y < h - 1 else -1):
                if k >= 0 and not bg_mask[k] and comp[k] < 0:
                    comp[k] = cid
                    dq2.append(k)
        comps.append((size, touch))
    if comps:
        main = max(range(len(comps)), key=lambda c: comps[c][0])
        for i in range(n):
            if not bg_mask[i] and comp[i] != main and comps[comp[i]][1]:
                bg_mask[i] = 1

    # 输出：背景全透明；与背景相邻的主体边缘半透明，弱化白边锯齿
    out = [None] * n
    for i in range(n):
        j = i * 4
        if bg_mask[i]:
            out[i] = (raw[j], raw[j + 1], raw[j + 2], 0)
        else:
            x, y = i % w, i // w
            near_bg = ((x > 0 and bg_mask[i - 1]) or (x < w - 1 and bg_mask[i + 1])
                       or (y > 0 and bg_mask[i - w]) or (y < h - 1 and bg_mask[i + w]))
            a = raw[j + 3]
            if near_bg and dist(i) <= tol:  # 只羽化真正偏背景色的边缘像素
                out[i] = (raw[j], raw[j + 1], raw[j + 2], a * 2 // 3)
            else:
                out[i] = (raw[j], raw[j + 1], raw[j + 2], a)
    res = Image.new("RGBA", img.size)
    res.putdata(out)
    return res


def save_limited(img, path, max_kb, fmt="PNG", quality=90):
    """保存并把体积压到 max_kb 以内"""
    if fmt == "JPG":
        img = img.convert("RGB")
        q = quality
        while q >= 60:
            img.save(path, "JPEG", quality=q, optimize=True, progressive=True)
            if kb(path) <= max_kb:
                return kb(path), q
            q -= 8
        return kb(path), q
    img.save(path, "PNG", optimize=True)
    if kb(path) <= max_kb:
        return kb(path), None
    # 体积超标：逐级降色
    for colors in (192, 128, 64, 32):
        q = img.convert("RGBA").quantize(colors=colors, method=Image.FASTOCTREE).convert("RGBA")
        q.save(path, "PNG", optimize=True)
        if kb(path) <= max_kb:
            return kb(path), colors
    return kb(path), 32


def build_banner(src_dir, files, out_path, c1, c2, bg_tol=42, style="circle"):
    """750×400 横幅：彩色渐变 + 无文字原图排列 + 装饰，非白底。
    注意：官方要求横幅避免任何文字，务必传入未加文案的原图目录。
    style=circle 时角色以圆形徽章呈现（奶白主体抠图必然掏洞，禁用抠图）。"""
    W, H = 750, 400
    bg = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(bg)
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=(int(r1 + (r2 - r1) * t),
                                       int(g1 + (g2 - g1) * t),
                                       int(b1 + (b2 - b1) * t)))

    rnd = random.Random(20260817)
    # 装饰：半透明圆点
    for _ in range(26):
        x, y = rnd.randint(0, W), rnd.randint(0, H)
        r = rnd.randint(6, 26)
        col = (255, 255, 255) if rnd.random() < 0.6 else tuple(min(255, v + 40) for v in c2)
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)

    # 排列表情（尺寸自适应，保证不出画布）
    n = min(len(files), 5)
    if n:
        gap = 24
        size = min(170, (W - 40 - (n - 1) * gap) // n)
        total = n * size + (n - 1) * gap
        x0 = (W - total) // 2
        y0 = (H - size) // 2 - 14
        for i in range(n):
            im = Image.open(os.path.join(src_dir, files[i]))
            im = square_crop(im).resize((size, size), Image.LANCZOS)
            if style == "circle":
                im = circle_badge(im)
            else:
                im = make_transparent(im, bg_tol)
            ang = rnd.choice([-7, -4, 0, 4, 7])
            im = im.rotate(ang, resample=Image.BICUBIC, expand=False)
            bg.paste(im, (x0 + i * (size + gap), y0), im)

    size_kb, q = save_limited(bg, out_path, SPEC["banner"]["max_kb"], "JPG")
    return size_kb, q


def build_tips(src_dir, files, out_guide, out_thanks, c1, c2, bg_tol=42, style="circle"):
    """赞赏引导图 750×560 / 致谢图 750×750（用无文字原图）"""
    def paint(W, H, n):
        bg = Image.new("RGB", (W, H))
        d = ImageDraw.Draw(bg)
        for y in range(H):
            t = y / (H - 1)
            d.line([(0, y), (W, y)], fill=(int(c1[0] + (c2[0] - c1[0]) * t),
                                           int(c1[1] + (c2[1] - c1[1]) * t),
                                           int(c1[2] + (c2[2] - c1[2]) * t)))
        rnd = random.Random(7)
        for _ in range(18):
            x, y, r = rnd.randint(0, W), rnd.randint(0, H), rnd.randint(8, 30)
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255))
        cnt = min(n, 3)
        size = min(int(H * 0.52), int((W - 80) / cnt) - 20)
        total = cnt * size + (cnt - 1) * 20
        x0 = (W - total) // 2
        for i in range(cnt):
            im = Image.open(os.path.join(src_dir, files[i]))
            im = square_crop(im).resize((size, size), Image.LANCZOS)
            if style == "circle":
                im = circle_badge(im)
            else:
                im = make_transparent(im, bg_tol)
            bg.paste(im, (x0 + i * (size + 20), (H - size) // 2), im)
        return bg
    if files:
        save_limited(paint(750, 560, len(files)), out_guide, 500, "PNG")
        save_limited(paint(750, 750, len(files)), out_thanks, 500, "PNG")


def hex2rgb(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------- 校验

def check_file(path, kind, report):
    spec = SPEC[kind]
    name = os.path.basename(path)
    try:
        img = Image.open(path)
    except Exception as e:
        report.append((name, kind, "❌", f"无法读取: {e}"))
        return False
    ok = True
    msgs = []
    if img.size != spec["size"]:
        ok = False
        msgs.append(f"尺寸 {img.size[0]}×{img.size[1]} ≠ {spec['size'][0]}×{spec['size'][1]}")
    size_kb = kb(path)
    if size_kb > spec["max_kb"]:
        ok = False
        msgs.append(f"{size_kb:.0f}KB > {spec['max_kb']}KB")
    if spec.get("alpha") and img.mode != "RGBA":
        ok = False
        msgs.append("非透明底 RGBA")
    report.append((name, kind, "✅" if ok else "❌",
                   (f"{img.size[0]}×{img.size[1]} · {img.mode} · {size_kb:.0f}KB" +
                    (" · " + "；".join(msgs) if msgs else ""))))
    return ok


# ---------------------------------------------------------------- 主流程

def main():
    ap = argparse.ArgumentParser(description="微信投稿素材包生成器")
    ap.add_argument("--input", "-i", help="表情图目录（已加文案的方图）")
    ap.add_argument("--output", "-o", default="wechat_submit", help="输出目录")
    ap.add_argument("--name", default="sticker", help="专辑名，用于打包文件名")
    ap.add_argument("--cover", help="封面用哪张图（文件名），默认第一张")
    ap.add_argument("--icon", help="图标用哪张图（文件名），默认同封面")
    ap.add_argument("--transparent", action="store_true",
                    help="主图也去背景。⚠️ 奶白/浅色主体与背景色距近时抠图会掏洞"
                         "（审核驳回'没有填充颜色'），此类素材务必保持默认带背景")
    ap.add_argument("--bg-tol", type=int, default=42,
                    help="去背景容差（局部梯度步进，越大背景吞得越多；主体被误抠就调小），默认 42")
    ap.add_argument("--banner-color", default="#FFD9A0,#FF8F6B", help="横幅渐变色 起,止（禁止白色）")
    ap.add_argument("--banner-src", help="横幅与赞赏图用的【无文字】原图目录；官方要求横幅避免出现文字，若主图已叠文案，务必指向未加字的原图")
    ap.add_argument("--raw-src", help="封面/图标用的【无文字】原图目录（默认回落 banner-src，再回落 input）。审核要求封面图标无文字装饰")
    ap.add_argument("--outline", choices=["auto", "on", "off"], default="auto",
                    help="封面/图标深色描边：auto=主体过浅自动加（暗夜模式可见），on=强制，off=关闭")
    ap.add_argument("--showcase-style", choices=["circle", "cutout"], default="circle",
                    help="封面/图标/横幅/赞赏图的呈现样式：circle=圆形徽章（默认，奶白主体"
                         "必选，零抠图风险）；cutout=抠图透明底（仅限主体与背景色距大的素材）")
    ap.add_argument("--icon-span", type=float, default=0.44,
                    help="图标头像特写的方形边长占短边比例，默认 0.44（只取头部）")
    ap.add_argument("--icon-cy", type=float, default=0.30,
                    help="图标头像特写的中心高度占画面比例，默认 0.30（偏上取头部）")
    ap.add_argument("--cover-fill", type=float, default=0.86,
                    help="封面主体占画布比例，默认 0.86（主体过小会被认为不清晰）")
    ap.add_argument("--with-tips", action="store_true", help="额外生成赞赏引导图与致谢图")
    ap.add_argument("--no-thumb", action="store_true", help="不生成 120×120 缩略图")
    ap.add_argument("--zip", action="store_true", help="打包为 zip")
    ap.add_argument("--check", help="只校验已有素材目录，不生成")
    args = ap.parse_args()

    # ---- 仅校验模式
    if args.check:
        root = os.path.abspath(args.check)
        report = []
        pairs = [("表情图", "sticker"), ("缩略图", "thumb")]
        for folder, kind in pairs:
            d = os.path.join(root, folder)
            if os.path.isdir(d):
                for f in sorted(os.listdir(d)):
                    if f.lower().endswith(IMG_EXT):
                        check_file(os.path.join(d, f), kind, report)
        singles = [("表情封面图.png", "cover"), ("聊天面板图标.png", "icon"),
                   ("详情页横幅.jpg", "banner"), ("详情页横幅.png", "banner"),
                   ("赞赏引导图.png", "tip_guide"), ("赞赏致谢图.png", "tip_thanks")]
        for f, kind in singles:
            p = os.path.join(root, f)
            if os.path.exists(p):
                check_file(p, kind, report)
        if not report:
            sys.exit(f"[错误] {root} 下没找到可校验的素材")
        print(f"{'文件':<20} {'类型':<10} {'结果':<6} 详情")
        print("-" * 76)
        for r in report:
            print(f"{r[0]:<20} {r[1]:<10} {r[2]:<6} {r[3]}")
        bad = sum(1 for r in report if r[2] == "❌")
        print("-" * 76)
        print(f"[{'完成' if not bad else '不合规'}] 共 {len(report)} 项，不合格 {bad} 项")
        return 1 if bad else 0

    if not args.input:
        ap.error("生成模式需要 --input")

    src = os.path.abspath(args.input)
    files = sorted(f for f in os.listdir(src) if f.lower().endswith(IMG_EXT))
    if not files:
        sys.exit(f"[错误] {src} 里没有图片")

    n = len(files)
    lo, hi = SPEC["sticker"]["n"]
    if not (lo <= n <= hi):
        print(f"[警告] 表情数量 {n} 张，官方要求 {lo}~{hi} 张，提交会被拒")

    out = os.path.abspath(args.output)
    d_sticker = os.path.join(out, "表情图")
    d_thumb = os.path.join(out, "缩略图")
    os.makedirs(d_sticker, exist_ok=True)
    if not args.no_thumb:
        os.makedirs(d_thumb, exist_ok=True)

    c1, c2 = (hex2rgb(x.strip()) for x in args.banner_color.split(","))
    if sum(c1) > 700 or sum(c2) > 700:
        print("[警告] 横幅颜色过浅接近白色，官方明确要求避免白底，建议换深一点的颜色")

    print(f"[信息] 输入 {n} 张 → 输出目录 {out}\n")

    imgs = []
    for i, fn in enumerate(files, 1):
        im = Image.open(os.path.join(src, fn))
        im = square_crop(im).resize((240, 240), Image.LANCZOS)
        if args.transparent:
            im = make_transparent(im, args.bg_tol)
        p = os.path.join(d_sticker, f"{i:02d}.png")
        size_kb, _ = save_limited(im, p, SPEC["sticker"]["max_kb"])
        imgs.append(im)
        print(f"  表情图 {i:02d}.png  {size_kb:.0f}KB" + ("（透明底）" if args.transparent else "（保留原始背景）"))
        if not args.no_thumb:
            t = im.resize((120, 120), Image.LANCZOS)
            save_limited(t, os.path.join(d_thumb, f"{i:02d}.png"), SPEC["thumb"]["max_kb"])

    # 封面/图标图源：优先无文字原图（审核驳回高发：封面带文字或装饰）
    raw_dir = (os.path.abspath(args.raw_src) if args.raw_src
               else (os.path.abspath(args.banner_src) if args.banner_src else src))
    raw_files = sorted(f for f in os.listdir(raw_dir) if f.lower().endswith(IMG_EXT))
    if raw_dir == src and not args.transparent:
        print("[提示] 封面/图标将从主图取材。建议 --raw-src 指向未叠文案的原图目录")

    def finish_showcase(img, kind, already_transparent=False):
        """（按需去背景 →）暗夜模式双向检测 → 过浅自动加同色系深描边"""
        im = img if already_transparent else make_transparent(img, args.bg_tol)
        lum, dark_frac = visibility(im)
        outlined = False
        if args.outline == "on" or (args.outline == "auto" and lum > 185):
            im = add_outline(im)
            outlined = True
        note = f"亮度{lum:.0f}"
        if outlined:
            note += "，过浅→已加深色描边（暗夜模式可见）"
        elif dark_frac > 0.35:
            note += (f"，⚠️ 深色区域占 {dark_frac:.0%}，暗夜模式下易与背景融合，"
                     "建议换主色更亮的图，或人工确认")
        else:
            note += "，暗夜模式可见"
        print(f"  [暗夜检查] {kind}: {note}")
        return im

    # 封面（从无字原图取。circle=圆形徽章不抠像素；cutout=洪泛抠图+主体放大）
    cover_src = args.cover if args.cover in raw_files else raw_files[0]
    base = Image.open(os.path.join(raw_dir, cover_src)).convert("RGBA")
    sq = square_crop(base).resize((480, 480), Image.LANCZOS)
    if args.showcase_style == "circle":
        cover = circle_badge(sq.resize((240, 240), Image.LANCZOS))
        cover_note = "圆形徽章"
    else:
        cover_raw = make_transparent(sq, args.bg_tol)
        bbox = subject_bbox(cover_raw)
        fill_pct = 0
        if bbox:
            bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
            fill_pct = int(max(bw, bh) / 480 * 100)
        cover = zoom_to_canvas(cover_raw, 240, args.cover_fill)
        cover_note = f"主体占比 {max(fill_pct, int(args.cover_fill * 100))}%"
    cover = finish_showcase(cover, "封面", already_transparent=True)
    p_cover = os.path.join(out, "表情封面图.png")
    sk, _ = save_limited(cover, p_cover, SPEC["cover"]["max_kb"])
    print(f"  表情封面图.png  {sk:.0f}KB（取自 {cover_src}，{cover_note}）")

    # 图标（从无字原图取头像特写：只取头部、放大占满画面、无场景道具文字。
    # 审核驳回高发：整幅场景缩到 50px 后主体小到无法辨识）
    icon_src = args.icon if args.icon in raw_files else cover_src
    base = Image.open(os.path.join(raw_dir, icon_src)).convert("RGBA")
    sq = square_crop(base).resize((480, 480), Image.LANCZOS)
    head = head_crop(sq, args.icon_span, args.icon_cy).resize((100, 100), Image.LANCZOS)
    if args.showcase_style == "circle":
        icon = circle_badge(head, ring_ratio=0.06)
        icon_note = f"头部徽章 span={args.icon_span} cy={args.icon_cy}"
    else:
        icon = zoom_to_canvas(make_transparent(head, args.bg_tol), 100, 0.86)
        icon_note = f"头部特写抠图 span={args.icon_span} cy={args.icon_cy}"
    icon = finish_showcase(icon, "图标", already_transparent=True)
    icon = icon.resize((50, 50), Image.LANCZOS)
    p_icon = os.path.join(out, "聊天面板图标.png")
    sk, _ = save_limited(icon, p_icon, SPEC["icon"]["max_kb"])
    print(f"  聊天面板图标.png  {sk:.0f}KB（取自 {icon_src} {icon_note}）")

    # 横幅（用无文字原图，官方要求横幅避免任何文字）
    banner_dir = os.path.abspath(args.banner_src) if args.banner_src else src
    banner_files = sorted(f for f in os.listdir(banner_dir) if f.lower().endswith(IMG_EXT))
    if not args.banner_src:
        print("[警告] 未指定 --banner-src：横幅将直接使用主图。")
        print("       官方要求横幅避免任何文字；若主图已叠文案，请用 --banner-src 指向无字原图！")
    p_banner = os.path.join(out, "详情页横幅.jpg")
    sk, q = build_banner(banner_dir, banner_files, p_banner, c1, c2, args.bg_tol,
                         style=args.showcase_style)
    print(f"  详情页横幅.jpg  {sk:.0f}KB（quality={q}，图源 {os.path.basename(banner_dir)}）")

    # 赞赏图
    if args.with_tips:
        build_tips(banner_dir, banner_files, os.path.join(out, "赞赏引导图.png"),
                   os.path.join(out, "赞赏致谢图.png"), c1, c2, args.bg_tol,
                   style=args.showcase_style)
        print("  赞赏引导图.png / 赞赏致谢图.png")

    # 校验 + 报告
    report = []
    for f in sorted(os.listdir(d_sticker)):
        check_file(os.path.join(d_sticker, f), "sticker", report)
    if not args.no_thumb:
        for f in sorted(os.listdir(d_thumb)):
            check_file(os.path.join(d_thumb, f), "thumb", report)
    check_file(p_cover, "cover", report)
    check_file(p_icon, "icon", report)
    check_file(p_banner, "banner", report)

    bad = [r for r in report if r[2] == "❌"]
    lines = ["# 投稿素材校验报告", "",
             f"- 专辑名：{args.name}", f"- 表情数量：{n} 张（官方要求 8~24）",
             f"- 横幅配色：{args.banner_color}", "",
             "| 文件 | 类型 | 结果 | 详情 |", "|---|---|---|---|"]
    for nm, kind, res, detail in report:
        lines.append(f"| {nm} | {kind} | {res} | {detail} |")
    lines += ["", "## 提交前自查", "",
              "- [ ] **角色类型**：动物形象选「宠物动物角色-兔/猫/狗…」，不要选「人物角色」（驳回高发）",
              "- [ ] **暗夜模式**：封面/图标为圆形徽章+深色描边环，深色背景下清晰可辨",
              "- [ ] **图标是头部徽章**：只取头像放大，无场景道具文字（50px 下场景会糊成一团）",
              "- [ ] **浅色主体勿抠图**：奶白主体与浅色背景抠图会掏洞（驳回'没有填充颜色'），主图保留背景、封面图标用徽章",
              "- [ ] 横幅无文字、非白底、元素不变形",
              "- [ ] 封面/图标圆外透明、无白边、无锯齿、无文字与装饰图案",
              "- [ ] 全套无水印、无二维码、无网址、无 Logo",
              "- [ ] 各表情情绪不重复，含义词 ≤4 字且不重复",
              "- [ ] 名称 ≤8 字无标点，介绍 ≤80 字，无「官方/正版/认证」", ""]
    with open(os.path.join(out, "投稿清单.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n[校验] 共 {len(report)} 项，不合格 {len(bad)} 项")
    for r in bad:
        print(f"  ❌ {r[0]}: {r[3]}")

    if args.zip:
        zp = os.path.join(os.path.dirname(out), f"{args.name}-微信投稿素材.zip")
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            for root, _, fs in os.walk(out):
                for fn in fs:
                    full = os.path.join(root, fn)
                    z.write(full, os.path.relpath(full, out))
        print(f"[打包] {zp}（{os.path.getsize(zp)/1024:.0f}KB）")

    print(f"[完成] 素材目录: {out}")
    print("[提示] 上传入口：https://sticker.weixin.qq.com → 提交表情 → 按目录逐项上传")


if __name__ == "__main__":
    main()
