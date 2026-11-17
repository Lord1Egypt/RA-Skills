#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""零依赖图标生成器：手写 PNG 编码器 + 矢量符号渲染 + 圆角方形底。

为什么不用 Pillow / cairosvg：
    本机 `pip install pillow` 反复 SIGTERM（超时 / 代理），且为目标机器
    「打开即用」交付时不该引入二进制依赖。PNG 本身非常简单 ——
    IHDR + IDAT(zlib) + IEND + CRC32，标准库 zlib/struct 就能写。

用法：
    python gen_icons.py --spec "slug:#4F46E5,#818CF8,browser" -o out/
    python gen_icons.py --specs-file specs.txt -o out/
    python gen_icons.py --spec "app:#059669,#34D399,check" --size 512
    python gen_icons.py --list-symbols
    python gen_icons.py --preview-text "AI" --spec "x:#333,#999,text"

specs 文件每行一条： slug:main_hex,accent_hex,symbol[|lines=3]
符号集见 --list-symbols；也支持 symbol:text (用 --preview-text 指定文字)。

设计原则（踩坑总结，改前先看）：
    1. **符号用实心剪影，不要空心描边**。第一版想画「空心框 + 内挖空」，
       内挖空把符号本身吃掉了（浏览器成光板方块、盾牌里对勾消失、
       文件夹横线被吞、云朵箭头畸形）。实心剪影在 32px 缩略图下
       辨识度也高得多。
    2. 底色用「对角线双色渐变 + 圆角方形」最稳妥，识别度高且不和
       平台自带的方形平涂占位图撞脸。
    3. 符号占幅约 45%~60%，四周留白，别贴边。
    4. 尺寸 256 起步（平台多为 256/512），PNG 体积 3~6KB。
"""
import argparse
import math
import os
import struct
import sys
import zlib

DEFAULT_SIZE = 256
DEFAULT_RADIUS_RATIO = 56 / 256.0   # 圆角半径占边长比例
SS = 2                              # 超采样倍数（2x2 够用，4x4 慢 4 倍收益小）


# --------------------------------------------------------------------------- #
# 颜色 / 几何工具
# --------------------------------------------------------------------------- #
def hex2rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def seg_dist(px, py, ax, ay, bx, by):
    """点到线段距离。用于画对勾、箭头杆、任意角度笔画。"""
    vx, vy = bx - ax, by - ay
    wx, wy = px - ax, py - ay
    L2 = vx * vx + vy * vy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, (wx * vx + wy * vy) / L2))
    return math.hypot(px - (ax + t * vx), py - (ay + t * vy))


def bar_dist(px, py, x0, x1, y0, y1):
    """轴对齐矩形距离，<=0 表示在矩形内部（含边界）。用于画窗口/文件夹/横线。"""
    dx = max(x0 - px, 0.0, px - x1)
    dy = max(y0 - py, 0.0, py - y1)
    return math.hypot(dx, dy)


def rounded_square_alpha(fx, fy, size, radius):
    """圆角方形覆盖度，边缘 1px 抗锯齿。返回 0..1。"""
    cx = min(max(fx, radius), size - radius)
    cy = min(max(fy, radius), size - radius)
    d = math.hypot(fx - cx, fy - cy)
    if d <= radius - 1:
        return 1.0
    if d >= radius:
        return 0.0
    return radius - d


# --------------------------------------------------------------------------- #
# 符号库（归一化坐标 0..1，返回 True 表示该点在符号内）
# --------------------------------------------------------------------------- #
def sym_browser(x, y):
    """实心窗口 + 挖空屏幕 + 标题栏三圆点 + 两条内容线。

    注意实现顺序：先判外框 -> 再判屏幕挖空（屏幕里画白线）-> 最后挖标题栏圆点。
    若先挖圆点，圆点会被后续的外框判定覆盖掉。
    """
    if bar_dist(x, y, 0.275, 0.725, 0.300, 0.700) > 0:
        return False
    # 屏幕区域挖空
    if bar_dist(x, y, 0.305, 0.695, 0.420, 0.670) <= 0:
        # 屏幕内两条白色内容线
        if 0.345 <= x <= 0.655 and (0.470 <= y <= 0.500 or 0.550 <= y <= 0.580):
            return True
        return False
    # 标题栏三个镂空圆点
    if 0.330 <= y <= 0.390:
        for cx in (0.330, 0.378, 0.426):
            if math.hypot(x - cx, y - 0.360) <= 0.018:
                return False
    return True


def sym_cloud(x, y):
    """云（三圆并集）+ 向上箭头，语义=上传 / 部署 / 云端。"""
    circles = [(0.395, 0.475, 0.105), (0.520, 0.420, 0.140), (0.645, 0.485, 0.098)]
    cloud = any((x - cx) ** 2 + (y - cy) ** 2 <= r * r for cx, cy, r in circles)
    # 云底切平（只保留 y <= 0.575 的部分），避免三圆下方露出三个圆弧
    if cloud and 0.395 <= x <= 0.645 and 0.470 <= y <= 0.575:
        return True
    if cloud and 0.440 <= x <= 0.600 and y <= 0.470:
        return True
    # 箭头杆
    if 0.625 <= y <= 0.775 and abs(x - 0.520) <= 0.028:
        return True
    # 箭头三角头（尖朝上）：从上到下线性加宽
    if 0.595 <= y <= 0.690:
        t = (y - 0.595) / 0.095
        if abs(x - 0.520) <= 0.020 + t * 0.098:
            return True
    return False


def sym_shield(x, y):
    """盾牌实心剪影 + 内部对勾挖空，语义=证书 / 安全 / 续期。"""
    inside = False
    if 0.245 <= y <= 0.600:
        inside = 0.265 <= x <= 0.735
    elif 0.600 < y <= 0.790:
        t = (y - 0.600) / 0.190
        half = 0.235 * (1 - t) ** 0.78         # 幂次控制收尖弧度
        inside = abs(x - 0.500) <= half
    if not inside:
        return False
    d1 = seg_dist(x, y, 0.375, 0.490, 0.455, 0.570)
    d2 = seg_dist(x, y, 0.455, 0.570, 0.628, 0.390)
    return min(d1, d2) > 0.031                  # 对勾位置挖空


def sym_folder(x, y):
    """文件夹剪影 + 三条镂空横线，语义=归档 / 整理 / 文件。"""
    if bar_dist(x, y, 0.235, 0.500, 0.295, 0.390) <= 0:
        return True                             # 标签页
    if bar_dist(x, y, 0.235, 0.775, 0.360, 0.730) <= 0:
        if 0.300 <= x <= 0.710:
            for y0, y1 in ((0.470, 0.505), (0.545, 0.580), (0.620, 0.655)):
                if y0 <= y <= y1:
                    return False
        return True
    return False


def sym_check(x, y):
    """圆环 + 对勾，语义=完成 / 签到 / 通过。"""
    d = math.hypot(x - 0.5, y - 0.5)
    ring = 0.245 <= d <= 0.335
    d1 = seg_dist(x, y, 0.370, 0.505, 0.455, 0.590)
    d2 = seg_dist(x, y, 0.455, 0.590, 0.640, 0.400)
    return ring or min(d1, d2) <= 0.036


def sym_download(x, y):
    """向下箭头 + 底部托线，语义=下载 / 导出。"""
    if 0.220 <= y <= 0.360 and abs(x - 0.500) <= 0.028:
        return True
    if 0.320 <= y <= 0.420:
        t = (y - 0.320) / 0.100
        if abs(x - 0.500) <= 0.100 - t * 0.080:   # 从上到下收尖
            return True
    if 0.560 <= y <= 0.600 and 0.250 <= x <= 0.750:
        return True
    return False


def sym_arrow_up(x, y):
    """向上箭头，语义=发布 / 上传 / 升级。"""
    if 0.380 <= y <= 0.700 and abs(x - 0.500) <= 0.030:
        return True
    if 0.260 <= y <= 0.395:
        t = (y - 0.260) / 0.135
        if abs(x - 0.500) <= 0.022 + t * 0.115:
            return True
    return False


def sym_gear(x, y):
    """齿轮：圆环 + 8 齿 + 中心挖空，语义=配置 / 设置 / 自动化。"""
    d = math.hypot(x - 0.5, y - 0.5)
    if d <= 0.180:
        return d >= 0.075                        # 中心镂空
    if d <= 0.300:
        return True
    if d <= 0.410:
        ang = math.atan2(y - 0.5, x - 0.5)
        step = math.pi / 4
        phase = abs(((ang + step / 2) % step) - step / 2)
        return phase < step * 0.20               # 8 个齿
    return False


def sym_search(x, y):
    """放大镜：圆环 + 手柄，语义=搜索 / 检索。"""
    d = math.hypot(x - 0.435, y - 0.435)
    ring = 0.155 <= d <= 0.245
    handle = seg_dist(x, y, 0.545, 0.545, 0.740, 0.740) <= 0.045
    return ring or handle


def sym_lock(x, y):
    """锁：锁体 + 锁梁，语义=安全 / 授权。"""
    if bar_dist(x, y, 0.300, 0.700, 0.470, 0.760) <= 0:
        return not (0.470 <= x <= 0.530 and 0.580 <= y <= 0.660)   # 钥匙孔挖空
    if 0.230 <= y <= 0.490:
        d = math.hypot(x - 0.5, y - 0.490)
        if 0.115 <= d <= 0.185 and y <= 0.490:
            return True
    return False


def sym_text(x, y):
    """文字符号占位（需配合 --text）。实际渲染由 render() 特判。"""
    return False


SYMBOLS = {
    "browser": sym_browser,
    "cloud": sym_cloud,
    "shield": sym_shield,
    "folder": sym_folder,
    "check": sym_check,
    "download": sym_download,
    "arrow-up": sym_arrow_up,
    "gear": sym_gear,
    "search": sym_search,
    "lock": sym_lock,
}


# --------------------------------------------------------------------------- #
# 渲染
# --------------------------------------------------------------------------- #
def make_text_mask(text, size, box_ratio=0.62):
    """用内嵌 5x7 点阵字渲染文字遮罩。零依赖，够用于 1~3 个大写字母/数字。

    返回 set((px, py)) —— 需要点亮的像素集合。仅在 symbol == "text" 时使用。
    """
    # 5x7 点阵：仅覆盖常用大写字母 + 数字，够拼缩写图标
    FONT = {
        "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
        "B": ["11110", "10001", "11110", "10001", "10001", "10001", "11110"],
        "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
        "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
        "E": ["11111", "10000", "11110", "10000", "10000", "10000", "11111"],
        "F": ["11111", "10000", "11110", "10000", "10000", "10000", "10000"],
        "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
        "H": ["10001", "10001", "11111", "10001", "10001", "10001", "10001"],
        "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
        "J": ["00111", "00010", "00010", "00010", "10010", "10010", "01100"],
        "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
        "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
        "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
        "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
        "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
        "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
        "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
        "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
        "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
        "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
        "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
        "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
        "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
        "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
        "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
        "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
        "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
        "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
        "2": ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
        "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
        "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
        "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
        "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
        "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
        "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
        "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
        "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
        " ": ["00000"] * 7,
    }
    text = text.upper()
    chars = [c for c in text if c in FONT]
    if not chars:
        return set()
    cw, ch = 5, 7
    gap = 1
    total_w = len(chars) * cw + (len(chars) - 1) * gap
    scale = int(size * box_ratio / max(total_w, ch))
    scale = max(scale, 1)
    glyph_w = total_w * scale
    glyph_h = ch * scale
    ox = (size - glyph_w) // 2
    oy = (size - glyph_h) // 2
    px = set()
    for i, c in enumerate(chars):
        rows = FONT[c]
        bx = ox + i * (cw + gap) * scale
        for ry, line in enumerate(rows):
            for rx, bit in enumerate(line):
                if bit != "1":
                    continue
                for sy in range(scale):
                    for sx in range(scale):
                        px.add((bx + rx * scale + sx, oy + ry * scale + sy))
    return px


def render(main_hex, accent_hex, sym_name, size=DEFAULT_SIZE,
           radius=None, text=None, rotate=0.0, shadow=False):
    """渲染色块行列表，每行是 RGBA bytes（供 write_png 使用）。

    流程：2x2 超采样 -> 分别统计「底色覆盖」与「符号覆盖」->
    底色用对角线渐变着色，符号叠白，最后写 alpha 做圆角抗锯齿。
    """
    main = hex2rgb(main_hex)
    accent = hex2rgb(accent_hex)
    radius = radius if radius is not None else round(size * DEFAULT_RADIUS_RATIO)

    text_mask = make_text_mask(text, size) if (sym_name == "text" and text) else None
    sym = SYMBOLS.get(sym_name)

    cos_r, sin_r = math.cos(-rotate), math.sin(-rotate)

    def in_symbol(fx, fy):
        if text_mask is not None:
            return (int(fx), int(fy)) in text_mask
        nx, ny = fx / size, fy / size
        if rotate:
            # 绕中心逆旋转，让符号看起来转了 rotate 弧度
            dx, dy = nx - 0.5, ny - 0.5
            nx = 0.5 + dx * cos_r - dy * sin_r
            ny = 0.5 + dx * sin_r + dy * cos_r
        return bool(sym) and sym(nx, ny)

    rows = []
    total = SS * SS
    for y in range(size):
        row = bytearray()
        for x in range(size):
            cov_shape = 0.0
            cov_sym = 0.0
            for sy in range(SS):
                for sx in range(SS):
                    fx = x + (sx + 0.5) / SS
                    fy = y + (sy + 0.5) / SS
                    if rounded_square_alpha(fx, fy, size, radius) > 0:
                        cov_shape += 1.0
                        if in_symbol(fx, fy):
                            cov_sym += 1.0
            shape_a = cov_shape / total
            if shape_a <= 0:
                row += b"\x00\x00\x00\x00"
                continue
            # 用 shape_a 归一，避免边缘处符号被二次衰减
            sym_a = (cov_sym / total) / max(shape_a, 1e-6)
            t = (x + y) / (2.0 * size)              # 对角线渐变参数
            base = tuple(main[i] + (accent[i] - main[i]) * t for i in range(3))
            if shadow:
                base = tuple(c * 0.88 for c in base)
            col = tuple(base[i] + (255 - base[i]) * sym_a for i in range(3))
            row += bytes(int(round(min(255, max(0, c)))) for c in col)
            row.append(int(round(255 * shape_a)))
        rows.append(bytes(row))
    return rows


def write_png(path, rows, width, height):
    """手写 PNG。IHDR(color type 6 = RGBA) + IDAT(zlib deflate) + IEND。"""
    raw = bytearray()
    for r in rows:
        raw.append(0)          # filter type 0 (None)，逐行
        raw.extend(r)

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def parse_spec(s):
    """解析 "slug:#main,#accent,symbol" 或 "slug:#main,#accent,text|text=WB"

    注意：颜色值里**不要**再出现冒号；用 partition(":") 只切第一个冒号，
    避免 slug 里含冒号或后续字段被误切（踩过：split(":") 只有 2 段就报错）。
    """
    body, _, optstr = s.partition("|")
    opts = {}
    for kv in optstr.split(","):
        if "=" in kv:
            k, v = kv.split("=", 1)
            opts[k.strip()] = v.strip()
    head, sep, tail = body.partition(":")
    if not sep:
        raise ValueError(f"spec 缺少 ':' 分隔符，格式应为 slug:main,accent,symbol —— 收到 {s!r}")
    slug = head.strip()
    fields = [f.strip() for f in tail.split(",") if f.strip()]
    if len(fields) < 3:
        raise ValueError(
            f"spec 字段不足，需要 main,accent,symbol 三个（收到 {len(fields)} 个: "
            f"{tail!r}）—— 完整格式 slug:main,accent,symbol")
    if not slug:
        raise ValueError(f"spec 的 slug 为空 —— 收到 {s!r}")
    return {"slug": slug, "main": fields[0], "accent": fields[1],
            "symbol": fields[2], "opts": opts}


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="零依赖图标生成器（手写 PNG 编码 + 矢量符号）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  python gen_icons.py --spec \"my-tool:#4F46E5,#818CF8,browser\" -o out/\n"
               "  python gen_icons.py --specs-file specs.txt -o out/\n"
               "  python gen_icons.py --list-symbols\n")
    ap.add_argument("--spec", action="append", default=[],
                    help="一条规格 slug:#main,#accent,symbol，可重复")
    ap.add_argument("--specs-file", default=None,
                    help="规格文件，每行一条（# 开头为注释）")
    ap.add_argument("-o", "--out", default=".", help="输出目录（默认当前目录）")
    ap.add_argument("--size", type=int, default=DEFAULT_SIZE,
                    help=f"边长像素（默认 {DEFAULT_SIZE}）")
    ap.add_argument("--radius", type=int, default=None,
                    help="圆角半径像素（默认按边长 21.9%）")
    ap.add_argument("--text", default=None,
                    help='symbol 为 text 时渲染的文字（大写字母/数字，1~4 个）')
    ap.add_argument("--rotate", type=float, default=0.0,
                    help="符号旋转角度（度）")
    ap.add_argument("--shadow", action="store_true", help="底色压暗 12%%，做弱化变体")
    ap.add_argument("--list-symbols", action="store_true", help="列出可用符号后退出")
    a = ap.parse_args(argv)

    if a.list_symbols:
        print("可用符号：")
        for k, fn in sorted(SYMBOLS.items()):
            doc = (fn.__doc__ or "").strip().splitlines()[0]
            print(f"  {k:<12}{doc}")
        if a.text is None:
            print("  text        点阵文字（配 --text）")
        print(f"\n外加 text（--text 指定文字）")
        return 0

    specs = list(a.spec)
    if a.specs_file:
        if not os.path.exists(a.specs_file):
            print(f"ERROR: specs 文件不存在: {a.specs_file}", file=sys.stderr)
            return 2
        with open(a.specs_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    specs.append(line)
    if not specs:
        ap.print_help()
        return 2

    radius = a.radius if a.radius is not None else round(a.size * DEFAULT_RADIUS_RATIO)
    os.makedirs(a.out, exist_ok=True)

    print(f"{'slug':<36}{'symbol':<12}{'px':>6}{'bytes':>9}")
    print("-" * 63)
    rc = 0
    for raw in specs:
        try:
            sp = parse_spec(raw)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            rc = 1
            continue
        sym = sp["symbol"]
        text = sp["opts"].get("text", a.text)
        if sym not in SYMBOLS and sym != "text":
            print(f"WARN: 未知符号 {sym!r}，跳过 {sp['slug']}（用 --list-symbols 查看）",
                  file=sys.stderr)
            rc = 1
            continue
        if sym == "text" and not text:
            print(f"WARN: symbol=text 但未给 --text，跳过 {sp['slug']}", file=sys.stderr)
            rc = 1
            continue
        rot = math.radians(float(sp["opts"].get("rotate", a.rotate)))
        rows = render(sp["main"], sp["accent"], sym, size=a.size, radius=radius,
                      text=text, rotate=rot,
                      shadow=sp["opts"].get("shadow", "").lower() in ("1", "true", "yes"))
        path = os.path.join(a.out, sp["slug"] + ".png")
        n = write_png(path, rows, a.size, a.size)
        print(f"{sp['slug']:<36}{sym:<12}{a.size:>6}{n:>9}")
    print(f"\n输出目录: {os.path.abspath(a.out)}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
