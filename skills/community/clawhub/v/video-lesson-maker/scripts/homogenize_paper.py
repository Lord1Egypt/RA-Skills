# -*- coding: utf-8 -*-
"""纸底均匀化：抹平线稿图的纸张底色，消除纸纹不均导致的渲染斑驳边界。

原理：白板渲染器按背景色阈值（match_bg≈28）识别"哪些像素是纸底"；
源图纸纹噪声一旦超过该阈值，渲染画面就会出现斑驳边界。
做法：从四角内缩取样得到纸张代表色，把与代表色差异 < threshold 的像素统一染平
（线条颜色距纸色远，不受影响；抗锯齿边缘轻微收窄，可接受）。

用法：
    python homogenize_paper.py <输入.png> <输出.png> [--threshold 52] [--inset 40] [--patch 30]
"""
import argparse
import numpy as np
from PIL import Image


def homogenize(src, dst, threshold=52, inset=40, patch=30):
    im = Image.open(src).convert("RGB")
    arr = np.asarray(im).astype(np.int16)
    h, w = arr.shape[:2]
    ins, p = inset, patch
    corners = [
        arr[ins:ins + p, ins:ins + p],
        arr[ins:ins + p, w - ins - p:w - ins],
        arr[h - ins - p:h - ins, ins:ins + p],
        arr[h - ins - p:h - ins, w - ins - p:w - ins],
    ]
    target = np.median(np.concatenate([c.reshape(-1, 3) for c in corners]), axis=0)
    dist = np.sqrt(((arr - target) ** 2).sum(axis=2))
    mask = dist < threshold
    arr[mask] = target.astype(np.int16)
    Image.fromarray(arr.astype(np.uint8)).save(dst)
    return target.tolist(), int(mask.sum()), float(mask.mean())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--threshold", type=int, default=52)
    ap.add_argument("--inset", type=int, default=40)
    ap.add_argument("--patch", type=int, default=30)
    a = ap.parse_args()
    t, n, r = homogenize(a.src, a.dst, a.threshold, a.inset, a.patch)
    print(f"paper={t}  染平 {n}px ({r*100:.1f}%)  -> {a.dst}")
