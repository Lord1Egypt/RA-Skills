# -*- coding: utf-8 -*-
"""清除 ImageGen 线稿右下角「AI生成 / WORKBUDDY」水印（V02 验证 v2）。

原理：水印在右下角候选框内，是比纸色略亮的半透明白层。
v2 策略（盒内无暗色图案时）：从候选框**正上方**取等宽干净纸纹，整盒移植覆盖，
边缘高斯羽化融合。若盒内检测到暗色图案（星星/线条），退回到仅替换比纸亮的像素。

用法：
    python remove_watermark.py <图1.png> [图2.png ...] [--out-dir DIR]
    默认原地覆盖；--out-dir 指定则输出到该目录（同名）。
"""
import argparse
import glob
import os

import numpy as np
from PIL import Image, ImageFilter


def remove_one(src, dst):
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    h, w = a.shape[:2]
    # 候选框：右下角（覆盖 AI生成 + WORKBUDDY>）
    bx0, by0, bx1, by1 = w - 140, h - 64, w - 4, h - 4
    bw, bh = bx1 - bx0, by1 - by0
    box = a[by0:by1, bx0:bx1]
    bp = box.mean(axis=2)
    # 纸纹源：候选框正上方等宽区域（角落上方通常是干净纸底）
    dy0 = max(0, by0 - 70)
    donor = a[dy0:by0 - 10, bx0:bx1]
    if donor.shape[0] < bh:                      # 高度不够时从左侧补
        donor = a[by0:by1, max(0, bx0 - 40 - bw):bx0 - 40]
    dp = donor.mean(axis=2)
    has_dark = (bp < 150).any() or (dp < 150).any() or dp.std() > 6

    if not has_dark and donor.shape[:2] == (bh, bw):
        # 整盒移植：干净纸纹直接覆盖，边缘羽化
        mask = np.ones((bh, bw), np.float32)
        m = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))
        m = np.asarray(m).astype(np.float32) / 255.0
        out = box * (1 - m[..., None]) + donor * m[..., None]
        n = int((m[..., None] > 0.5).sum())
    else:
        # 退回：仅替换比纸亮的像素（保护盒内深色图案）
        paper = np.median(dp.reshape(-1, 3), axis=0)
        bright = (bp > paper.mean() + 4).astype(np.float32)
        m = Image.fromarray((bright * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))
        m = np.asarray(m).astype(np.float32) / 255.0
        out = box * (1 - m[..., None]) + donor * m[..., None]
        n = int((bright > 0.5).sum())
    a[by0:by1, bx0:bx1] = out.astype(np.int16)
    Image.fromarray(a.astype(np.uint8)).save(dst)
    return n


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out-dir", default=None)
    a = ap.parse_args()
    files = []
    for p in a.inputs:
        files += glob.glob(p) if any(c in p for c in "*?[") else [p]
    for f in files:
        dst = os.path.join(a.out_dir, os.path.basename(f)) if a.out_dir else f
        n = remove_one(f, dst)
        print(f"{os.path.basename(f)}: 处理像素 {n} -> {dst}")
