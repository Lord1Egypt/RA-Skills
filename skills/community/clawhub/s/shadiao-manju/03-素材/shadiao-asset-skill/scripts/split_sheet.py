#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""九宫格切表情

用法：
  python3 split_sheet.py 表情九宫格.png --out 角色/阿强/
  python3 split_sheet.py 表情九宫格.png --out 角色/阿强/ --size 1024

默认按 3×3 等分，按顺序命名：
  exp_平静.png exp_开心.png exp_愤怒.png exp_悲伤.png exp_惊讶.png
  exp_无语.png exp_得意.png exp_崩溃.png _cell9.png
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("缺少 Pillow：pip install Pillow")

NAMES = ["平静", "开心", "愤怒", "悲伤", "惊讶", "无语", "得意", "崩溃", ""]


def main():
    ap = argparse.ArgumentParser(description="九宫格切表情")
    ap.add_argument("image", help="九宫格图片")
    ap.add_argument("--out", required=True, help="输出目录（角色目录）")
    ap.add_argument("--rows", type=int, default=3)
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--size", type=int, default=0, help="每格输出边长，0=保持原尺寸")
    args = ap.parse_args()

    src = Path(args.image)
    if not src.is_file():
        sys.exit(f"找不到图片：{src}")

    img = Image.open(src).convert("RGBA")
    w, h = img.size
    cw, ch = w // args.cols, h // args.rows
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    i = 0
    for r in range(args.rows):
        for c in range(args.cols):
            cell = img.crop((c * cw, r * ch, (c + 1) * cw, (r + 1) * ch))
            if args.size:
                cell = cell.resize((args.size, args.size), Image.LANCZOS)
            name = NAMES[i] if i < len(NAMES) and NAMES[i] else f"_cell{i + 1}"
            path = out_dir / f"exp_{name}.png" if name != f"_cell{i + 1}" else out_dir / f"{name}.png"
            cell.save(path, "PNG", optimize=True)
            print(f"  ✓ {path}")
            i += 1

    print(f"\n完成：{i} 张 → {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
