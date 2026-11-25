#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""画布尺寸守卫（fit_canvas.py）——必须在 homogenize/crop 之前运行。

背景教训（2026-10-21 世校赛 V01-V04 重制时发现）：
ImageGen 返回的图片尺寸不确定，曾整批返回 1024x1024 方图（而非预期的
1536x1024）。白板流水线按 1536 宽设计（crop 窗口 (0,55,1536,919)），
PIL crop 越界区域会自动填充纯黑，导致成片右上角出现大块黑色矩形。

用法:
    python fit_canvas.py scene-01-1.png scene-01-2.png scene-01-3.png

行为:
- 宽度 >= 1536：不处理，打印 OK
- 宽度 < 1536：创建 1536xH 画布（底色取图像左缘 8 列的纸张均值色），
  原图水平居中贴入后覆盖保存。后续 homogenize 会把底色与纸张统一。
"""
import sys

import numpy as np
from PIL import Image

TARGET_W = 1536


def fit(f):
    im = Image.open(f).convert("RGB")
    w, h = im.size
    if w >= TARGET_W:
        print(f"{f}: {w}x{h} OK")
        return
    a = np.asarray(im)
    paper = tuple(a[:, :8].reshape(-1, 3).mean(axis=0).astype(int))
    canvas = Image.new("RGB", (TARGET_W, h), paper)
    canvas.paste(im, ((TARGET_W - w) // 2, 0))
    canvas.save(f)
    print(f"{f}: {w}x{h} -> 居中pad到 {TARGET_W}x{h}，底色 {paper}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for f in sys.argv[1:]:
        fit(f)
