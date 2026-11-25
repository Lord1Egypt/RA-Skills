#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""成片核验：拿「增强图」和「渲染帧」对账，找出成片里真正丢掉的内容。

为什么不能只靠看 PNG
--------------------
`check_layout.py` 验的是「墨迹有没有被 region 覆盖」，属于**设计稿层面**。
但成片还可能在渲染环节出问题：帧率/缩放/遮罩时序/渲染中断，任何一环出岔，
源图 PNG 都是完整的，成片里却缺一块。这个脚本把「增强图应该有的墨迹」和
「成片最后一帧实际有的墨迹」做差，直接给覆盖率与缺失块清单。

判定标准
--------
- **覆盖率 ≥ 99%**：通过。低于 99% 说明成片里确实少画了东西。
- 缺失块按面积排序，给出 bbox 与它最可能是哪个 region（对照 annotation）。
- **文字层留白**：同目录有 `-base.png` 时只量 PIL 新增的墨迹（=文字/图元层，不含线稿），
  报出成片四边实际像素值；`--edge-fail` 可让它也参与失败判定。
- 另报整帧墨迹贴边（含底图线稿），仅供人工核对——线稿天然画到纸边，不算问题。

用法
----
  python check_render.py --dir ./V07-一址一证
  python check_render.py --dir ./V07-一址一证 --json report.json
  python check_render.py --dir . --min-coverage 0.99 --margin 12 --edge-fail

退出码：0 全部通过；1 有片段未通过；2 用法/文件错误。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_layout import (DEFAULT_MARGIN, added_mask, find_base, find_annotation,  # noqa: E402
                          ink_mask)

FFMPEG = os.environ.get("FFMPEG_PATH") or "ffmpeg"


def ffprobe_duration(path: str) -> float:
    out = subprocess.run([FFMPEG, "-i", path], capture_output=True, text=True,
                         errors="ignore").stderr
    m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", out)
    if not m:
        return 0.0
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def grab_frame(video: str, t: float, out_png: str) -> bool:
    r = subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", f"{t:.3f}",
                        "-i", video, "-frames:v", "1", out_png],
                       capture_output=True)
    return r.returncode == 0 and os.path.exists(out_png)


def find_video(ann_path: str):
    """按命名习惯找该幕的渲染产物。"""
    d, name = os.path.split(ann_path)
    stem = name.replace(".annotation.json", "")
    for cand in (f"{stem}-whiteboard.mp4", f"{stem}.mp4", f"{stem}-scene.mp4"):
        p = os.path.join(d, cand)
        if os.path.exists(p):
            return p
    hits = glob.glob(os.path.join(d, stem + "*.mp4"))
    return hits[0] if hits else None


def find_enh(ann_path: str):
    d, name = os.path.split(ann_path)
    stem = name.replace(".annotation.json", "")
    for cand in (os.path.join(d, stem + "-enh.png"), os.path.join(d, stem + ".png"),
                 os.path.join(d, "rich", stem + ".png")):
        if os.path.exists(cand):
            return cand
    return None


def coverage(enh_png: str, base_png: str | None, frame_png: str, dilate: int = 3):
    enh = Image.open(enh_png).convert("RGB")
    fr = Image.open(frame_png).convert("RGB")
    W, H = fr.size
    if enh.size != fr.size:
        enh_s = enh.resize(fr.size, Image.LANCZOS)
    else:
        enh_s = enh
    if base_png:
        b = Image.open(base_png).convert("RGB")
        b_s = b.resize(fr.size, Image.LANCZOS) if b.size != fr.size else b
        want = added_mask(enh_s, b_s, 34)
    else:
        want = ink_mask(enh_s, 55)
    got = ink_mask(fr, 55)
    if dilate > 0:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate * 2 + 1,) * 2)
        got = cv2.dilate(got, k)
    want_n = int((want > 0).sum())
    if want_n == 0:
        return 1.0, [], (W, H), 0, got, want
    miss = ((want > 0) & (got == 0)).astype(np.uint8)
    miss_n = int(miss.sum())
    k2 = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    n, _, stats, _ = cv2.connectedComponentsWithStats(cv2.dilate(miss, k2), 8)
    blobs = []
    for i in range(1, n):
        x, y, w, h, a = stats[i]
        if a < 60:
            continue
        blobs.append((int(x), int(y), int(x + w), int(y + h), int(a)))
    blobs.sort(key=lambda t: -t[4])
    return 1.0 - miss_n / want_n, blobs, (W, H), want_n, got, want


def mask_margin(mask, margin):
    """给定墨迹掩膜的 bbox 与四边越界情况。"""
    ys, xs = np.where(mask > 0)
    if not len(xs):
        return None, []
    W, H = mask.shape[1], mask.shape[0]
    bad = []
    if xs.min() < margin:
        bad.append(f"左 {margin - int(xs.min())}px")
    if ys.min() < margin:
        bad.append(f"上 {margin - int(ys.min())}px")
    if xs.max() > W - margin:
        bad.append(f"右 {int(xs.max()) - (W - margin)}px")
    if ys.max() > H - margin:
        bad.append(f"下 {int(ys.max()) - (H - margin)}px")
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())), bad


def check_one(ann_path, margin, min_cov, tmpdir, edge_fail=False):
    enh = find_enh(ann_path)
    vid = find_video(ann_path)
    name = os.path.basename(ann_path).replace(".annotation.json", "")
    if not enh or not vid:
        print(f"\n== {name} ==\n  跳过：{'缺增强图' if not enh else '缺渲染 mp4'}")
        return None
    ann = json.load(open(ann_path, encoding="utf-8"))
    dur = ffprobe_duration(vid) or (ann.get("sceneDurationMs", 0) / 1000.0)
    t = max(0.0, dur - 0.35)
    frame = os.path.join(tmpdir, name + "-last.png")
    if not grab_frame(vid, t, frame):
        print(f"\n== {name} ==\n  跳过：抽帧失败")
        return None
    base = find_base(enh)
    cov, blobs, size, want_n, got, want = coverage(enh, base, frame)
    added_box, added_edge = mask_margin(want, margin)     # 新增内容（=文字层）的四边留白
    ink_box, ink_edge = mask_margin(got, margin)          # 整帧墨迹（含底图线稿，仅供参考）
    ok = cov >= min_cov and (not edge_fail or not added_edge)
    print(f"\n== {name} ==  {size[0]}x{size[1]}  时长 {dur:.1f}s  "
          f"[{'diff' if base else 'full'}]")
    print(f"  内容覆盖率 {cov * 100:.2f}%  ({'✓' if cov >= min_cov else '✗ 阈值 %.1f%%' % (min_cov * 100)})")
    if added_box:
        tag = "✓ 在安全区内" if not added_edge else "✗ " + "，".join(added_edge)
        print(f"  文字层留白  L{added_box[0]}  T{added_box[1]}  "
              f"R{size[0] - 1 - added_box[2]}  B{size[1] - 1 - added_box[3]}   {tag}")
    if not ok and blobs:
        regs = [e["region"] for e in ann.get("elements", [])]
        for (x0, y0, x1, y1, a) in blobs[:8]:
            best, bd = None, 1e18
            for i, r in enumerate(regs):
                rx0, ry0 = r["x"], r["y"]
                rx1, ry1 = rx0 + r["width"], ry0 + r["height"]
                dx = max(rx0 - x1, x0 - rx1, 0)
                dy = max(ry0 - y1, y0 - ry1, 0)
                if dx + dy < bd:
                    best, bd = i, dx + dy
            tag = f" ← 疑似 region#{best}" if best is not None else ""
            print(f"  缺失 bbox=({x0},{y0},{x1},{y1}) 面积{a}{tag}")
    if ink_edge:
        print(f"  整帧墨迹贴边：{', '.join(ink_edge)}（含底图线稿，需人工确认是否文字）")
    return {"scene": name, "video": os.path.basename(vid), "duration": round(dur, 2),
            "coverage": round(cov, 4), "ok": ok, "missing": blobs[:8],
            "added_bbox": added_box, "added_edge": added_edge,
            "frame_ink_bbox": ink_box, "edge": ink_edge,
            "mode": "diff" if base else "full"}


def main():
    ap = argparse.ArgumentParser(description="成片核验：增强图 vs 渲染帧 内容覆盖率")
    ap.add_argument("--dir", required=True, help="片子目录（含 *.annotation.json）")
    ap.add_argument("--margin", type=int, default=12, help="文字层四边留白阈值 px（默认 12）")
    ap.add_argument("--min-coverage", type=float, default=0.99, help="覆盖率阈值（默认 0.99）")
    ap.add_argument("--edge-fail", action="store_true",
                    help="文字层留白不足时也算失败（默认只提示，不改变退出码）")
    ap.add_argument("--json", help="输出 JSON 报告")
    a = ap.parse_args()

    anns = sorted(glob.glob(os.path.join(a.dir, "**", "*.annotation.json"), recursive=True))
    if not anns:
        print("未找到 *.annotation.json")
        return 2
    tmpdir = tempfile.mkdtemp(prefix="vcov_")
    rows, bad = [], 0
    for ann in anns:
        r = check_one(ann, a.margin, a.min_coverage, tmpdir, a.edge_fail)
        if r:
            rows.append(r)
            bad += 0 if r["ok"] else 1
    print(f"\n合计 {len(rows)} 幕，{bad} 幕内容不完整")
    if a.json:
        json.dump({"dir": a.dir, "scenes": rows, "bad": bad},
                  open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"报告 → {a.json}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
