#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给角色生成「会说话」的嘴巴叠加层（mouth.png + mouth.json）

为什么：
  整身表情图是静态的，说话时嘴不动，看着像「配音的纸片人」。
  做法是在工程里给角色挂一个「嘴」图层，说话时用缩放在 开/合 之间抖动。

关键点：
  每个表情的嘴位置/大小都不一样（AI 每张单独画的），所以先自动检测
  每个 exp_<表情>.png 里嘴的包围盒，换算到整身画布坐标，写进 mouth.json。

输入（角色目录）：
  face.json          —— 脸部贴图中心/缩放（compose_bodies.py 用的同一份）
  exp_<表情>.png      —— 280×280 表情贴图
输出（角色目录）：
  mouth.png          —— 张开的嘴（黑色圆角形状，透明底，居中）
  mouth.json         —— { 表情: {x, y, w, h, open} }，x/y 为整身画布归一化坐标
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    sys.exit("缺少 Pillow：pip install Pillow")

EXPRESSIONS = ["平静", "开心", "愤怒", "悲伤", "惊讶", "无语", "得意", "崩溃"]

# 嘴巴精灵画布尺寸（正方形，嘴居中；真正宽度靠 scaleX 缩放）
SPRITE = 120
MOUTH_W = 108      # 精灵里嘴的宽度
MOUTH_H = 84       # 精灵里嘴的高度（张到最大时）


def build_sprite(path: Path):
    """生成一张「张开的嘴」贴图：近黑圆角形状，居中，透明底。"""
    img = Image.new("RGBA", (SPRITE, SPRITE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x0 = (SPRITE - MOUTH_W) / 2
    x1 = (SPRITE + MOUTH_W) / 2
    y0 = (SPRITE - MOUTH_H) / 2
    y1 = (SPRITE + MOUTH_H) / 2
    d.rounded_rectangle([x0, y0, x1, y1], radius=MOUTH_H / 2, fill=(20, 20, 22, 255))
    # 一点点内侧亮边，闭合时更接近原画的手绘线
    img = img.filter(ImageFilter.GaussianBlur(1.2))
    img.save(path, "PNG", optimize=True)
    return SPRITE, SPRITE


def dark_mask(img: Image.Image):
    """返回 (w, h, mask)，mask[i] = True 表示该像素是深色（描边/嘴/眼睛）。"""
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    bg.alpha_composite(img)
    rgb = bg.convert("RGB")
    px = rgb.load()
    w, h = rgb.size
    mask = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if max(r, g, b) < 100:
                mask[y][x] = True
    return w, h, mask


def components(w, h, mask, region):
    """在 region(x0,y0,x1,y1) 内做连通域，返回 [{x0,y0,x1,y1,area}]。"""
    rx0, ry0, rx1, ry1 = region
    seen = [[False] * w for _ in range(h)]
    out = []
    for y in range(ry0, ry1):
        for x in range(rx0, rx1):
            if not mask[y][x] or seen[y][x]:
                continue
            stack = [(x, y)]
            seen[y][x] = True
            minx = maxx = x
            miny = maxy = y
            area = 0
            while stack:
                cx, cy = stack.pop()
                area += 1
                if cx < minx:
                    minx = cx
                if cx > maxx:
                    maxx = cx
                if cy < miny:
                    miny = cy
                if cy > maxy:
                    maxy = cy
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if rx0 <= nx < rx1 and ry0 <= ny < ry1 and mask[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx] = True
                        stack.append((nx, ny))
            out.append({"x0": minx, "y0": miny, "x1": maxx + 1, "y1": maxy + 1, "area": area})
    return out


def detect_mouth(exp_path: Path, face: dict):
    """检测表情贴图里嘴巴的位置，返回 (u, v, w, h, open) 或 None（表情贴图像素坐标）。"""
    img = Image.open(exp_path).convert("RGBA")
    ew, eh = img.size
    w, h, mask = dark_mask(img)

    # 嘴在脸的下半部，取 62%~92% 高度；横向只取中间 30%~70%，避开眉毛/耳朵
    # v0.8：先用 alpha 边界框把「头」框出来，再在头的下半部找嘴。
    # 这样九宫格切出来的表情（头居中、留白多）和旧的手绘表情（头顶满画布）都能用。
    hb = img.getchannel("A").getbbox()
    if not hb:
        return None
    hx0, hy0, hx1, hy1 = hb
    hw_, hh_ = hx1 - hx0, hy1 - hy0
    region = (
        int(hx0 + hw_ * 0.26), int(hy0 + hh_ * 0.56),
        int(hx0 + hw_ * 0.74), int(hy0 + hh_ * 0.86),
    )
    comps = components(w, h, mask, region)
    if not comps:
        return None

    cx = ew / 2
    cands = []
    for c in comps:
        bw = c["x1"] - c["x0"]
        bh = c["y1"] - c["y0"]
        if c["area"] < 30:
            continue
        # 鼻子是个圆点、嘴是横向的长条：宽高比 < 2 的一律不当嘴
        # （熊猫头的鼻子就长在嘴上头，不排除会把嘴叠到鼻子上）
        if bw / max(1, bh) < 1.5:
            continue
        # 嘴必须完整落在搜索区里（贴边说明是鼻头/下巴/西装，不是嘴）
        if c["y0"] <= region[1] + 2 or c["y1"] >= region[3] - 2:
            continue
        if c["x0"] <= region[0] + 1 or c["x1"] >= region[2] - 1:
            continue
        center = (c["x0"] + c["x1"]) / 2
        cands.append((abs(center - cx) - c["area"] * 0.02, c, bw, bh))
    if not cands:
        return None

    cands.sort(key=lambda t: t[0])
    _, c, bw, bh = cands[0]
    u = (c["x0"] + c["x1"]) / 2
    v = (c["y0"] + c["y1"]) / 2
    # 判定「已经是大张嘴」：高度占比大，或宽度过宽（红嘴/哭嘴）
    is_open = bh > eh * 0.10 or bw > ew * 0.34
    return u, v, bw, bh, is_open


def process(char_dir: Path):
    face_path = char_dir / "face.json"
    if not face_path.is_file():
        print(f"  ! 跳过 {char_dir.name}：缺 face.json", file=sys.stderr)
        return 0
    face = json.loads(face_path.read_text(encoding="utf-8-sig"))
    scale = float(face.get("scale", 1.0))

    # 整身画布尺寸（取 full_平静 的尺寸，没有就用 1024×1536）
    ref_full = char_dir / "full_平静.png"
    if ref_full.is_file():
        cw, ch = Image.open(ref_full).size
    else:
        cw, ch = 1024, 1536

    sprite_w, sprite_h = build_sprite(char_dir / "mouth.png")

    out = {
        "_sprite": {
            "width": SPRITE,
            "height": SPRITE,
            "mouthW": MOUTH_W,
            "mouthH": MOUTH_H,
            "closedHeight": 7,
        }
    }
    for emo in EXPRESSIONS:
        p = char_dir / f"exp_{emo}.png"
        if not p.is_file():
            continue
        hit = detect_mouth(p, face)
        if not hit:
            print(f"  ! {char_dir.name} {emo}：没检测到嘴，跳过", file=sys.stderr)
            continue
        u, v, bw, bh, is_open = hit
        # 表情贴图按 scale 放大后，贴在 (face.x*cw, face.y*ch) 为中心的位置
        ex_w = p and Image.open(p).size[0]
        px = face.get("x", 0.5) * cw - (ex_w * scale) / 2
        py = face.get("y", 0.5) * ch - (Image.open(p).size[1] * scale) / 2
        mx = px + u * scale
        my = py + v * scale
        mw = bw * scale
        out[emo] = {
            "x": round(mx / cw, 4),
            "y": round(my / ch, 4),
            "w": round(mw / cw, 4),
            "h": round((bh * scale) / ch, 4),
            "open": bool(is_open),
        }

    # 人工修正：mouth.override.json 里把不准的表情改掉或删掉（null = 不叠加）
    # 自动检测在「鼻子和嘴靠得太近」时会抓错（比如熊猫头的愤怒/悲伤），这时用它兜底。
    ov_path = char_dir / "mouth.override.json"
    if ov_path.is_file():
        try:
            override = json.loads(ov_path.read_text(encoding="utf-8-sig"))
            fixed = 0
            for k, v in override.items():
                if k.startswith("_"):
                    continue
                if v is None:
                    out.pop(k, None)
                else:
                    out[k] = v
                fixed += 1
            if fixed:
                print(f"  · {char_dir.name}：mouth.override 修正 {fixed} 项")
        except Exception as e:  # noqa: BLE001
            print(f"  ! {char_dir.name} mouth.override.json 读取失败：{e}", file=sys.stderr)

    (char_dir / "mouth.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    n_open = sum(1 for k, v in out.items() if not k.startswith("_") and v["open"])
    print(f"  ✓ {char_dir.name}：定位 {len(out) - 1} 个表情的嘴，其中 {n_open} 个已经是张嘴（不叠加）")
    return len(out) - 1


def main():
    ap = argparse.ArgumentParser(description="生成说话嘴叠加层")
    ap.add_argument("--season-dir", help="季目录（自动扫描 03-素材/角色/*）")
    ap.add_argument("--char-dir", help="只处理某个角色目录")
    args = ap.parse_args()

    if args.char_dir:
        d = Path(args.char_dir)
        process(d)
        # 调试图
        return

    if not args.season_dir:
        sys.exit("给 --season-dir 或 --char-dir")
    root = Path(args.season_dir) / "03-素材" / "角色"
    if not root.is_dir():
        sys.exit(f"找不到角色目录：{root}")
    total = 0
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        total += process(d)
    print(f"完成：{total} 个表情嘴巴定位")


if __name__ == "__main__":
    main()
