#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""九宫格表情图 → 单张表情素材（exp_*.png）

为什么：
  一张图里画 9 个表情，比出 9 张图省 8 次调用，而且 9 个表情的
  头大小/描边粗细/色板天然一致（分开画一定会飘，近景就是双描边）。

做的事：
  1. 按 rows×cols 均分切格；
  2. 每格白底转透明（并把被轮廓包住的白色补回来，白脸不会变透明）；
  3. 用「所有格里最大的那个头」统一缩放基准，保证 9 个表情一样大；
  4. 居中贴到统一画布上，输出 exp_<名字>.png；
  5. 顺手拼一张预览图，方便肉眼验收。

用法：
  python3 cut_sheet.py --sheet 九宫格.png --out-dir 角色/阿强 \
    --names 平静,开心,愤怒,悲伤,惊讶,无语,得意,崩溃,说话 \
    --size 300 --rows 3 --cols 3
"""

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

try:
    from scipy.ndimage import binary_closing, binary_fill_holes
except ImportError:
    binary_closing = binary_fill_holes = None


def white_to_alpha(img, threshold=238):
    """白底转透明，并把被轮廓包住的白色区域补回不透明。"""
    arr = np.array(img.convert("RGBA"))
    rgb = arr[..., :3].astype(np.int16)
    alpha = arr[..., 3]
    near_white = np.all(rgb >= threshold, axis=2)

    # 只把「不透明且不白」当轮廓，避免白底被当成前景
    foreground = (alpha > 10) & ~near_white
    if binary_closing is not None:
        closed = binary_closing(foreground, structure=np.ones((5, 5)))
        filled = binary_fill_holes(closed)
        holes = filled & ~foreground

    # 注意顺序：先补洞，再把「没被补到的白」抠掉。
    # 反过来的话，刚补回来的白口鼻/白衣服会被立刻抹成透明。
    alpha = np.where(holes, 255, alpha) if binary_closing is not None else alpha
    alpha = np.where(near_white & ~(holes if binary_closing is not None else False), 0, alpha)
    arr[..., 3] = alpha
    # 透明区域的 RGB 抹成白，避免边缘发黑
    arr[..., :3] = np.where(alpha[..., None] > 0, arr[..., :3], 255)
    return Image.fromarray(arr, "RGBA")


def main():
    ap = argparse.ArgumentParser(description="九宫格表情图切图")
    ap.add_argument("--sheet", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--names", required=True, help="逗号分隔，按 左→右、上→下")
    ap.add_argument("--size", type=int, default=300, help="输出方形边长")
    ap.add_argument("--rows", type=int, default=3)
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--fill", type=float, default=0.82, help="头部占画布比例")
    ap.add_argument("--preview", action="store_true", help="输出预览拼图")
    args = ap.parse_args()

    names = [n.strip() for n in args.names.split(",") if n.strip()]
    if len(names) != args.rows * args.cols:
        sys.exit(f"名字数（{len(names)}）和 rows×cols（{args.rows * args.cols}）不一致")

    sheet = Image.open(args.sheet).convert("RGBA")
    sw, sh = sheet.size
    cw, ch = sw // args.cols, sh // args.rows

    # 先把每格白底转透明，再统一算缩放
    cells = []
    for r in range(args.rows):
        for c in range(args.cols):
            box = (c * cw, r * ch, (c + 1) * cw, (r + 1) * ch)
            cells.append(white_to_alpha(sheet.crop(box)))

    # 统一基准：取所有格子里「头」的最大边，避免某些表情（比如崩溃）特别大
    spans = []
    for cell in cells:
        bbox = cell.getchannel("A").getbbox()
        if bbox:
            spans.append(max(bbox[2] - bbox[0], bbox[3] - bbox[1]))
    base = max(spans) if spans else cw

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = args.size
    inner = int(target * args.fill)

    tiles = []
    for name, cell in zip(names, cells):
        bbox = cell.getchannel("A").getbbox()
        if not bbox:
            print(f"  ! {name} 是空的，跳过", file=sys.stderr)
            continue
        head = cell.crop(bbox)
        scale = inner / base
        hw = max(1, int(round(head.width * scale)))
        hh = max(1, int(round(head.height * scale)))
        head = head.resize((hw, hh), Image.LANCZOS)

        canvas = Image.new("RGBA", (target, target), (0, 0, 0, 0))
        canvas.paste(head, ((target - hw) // 2, (target - hh) // 2), head)
        p = out_dir / f"exp_{name}.png"
        canvas.save(p, "PNG", optimize=True)
        tiles.append((name, canvas))
        print(f"  ✓ exp_{name}.png  {hw}×{hh} → {target}×{target}")

    if args.preview:
        cols = min(3, len(tiles))
        rows = (len(tiles) + cols - 1) // cols
        pv = Image.new("RGB", (target * cols, (target + 26) * rows), "white")
        d = ImageDraw.Draw(pv)
        for i, (name, im) in enumerate(tiles):
            x, y = (i % cols) * target, (i // cols) * (target + 26)
            bg = Image.new("RGB", (target, target), "white")
            bg.paste(im, (0, 0), im)
            pv.paste(bg, (x, y))
            d.text((x + 6, y + target + 4), name, fill="black")
        pp = out_dir / "_预览-表情.png"
        pv.save(pp)
        print(f"  ✓ 预览 {pp}")

    meta = {"base": base, "size": target, "cells": names}
    (out_dir / "_sheet_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
