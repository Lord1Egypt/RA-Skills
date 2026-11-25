#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""画面版式体检：渲染前就抓出「文字贴边 / 被遮罩裁掉 / 压进字幕带」的问题。

为什么需要它
------------
白板渲染器按 region 揭示墨迹：某个区域只能揭示「矩形 region 减去后续区域」内的
墨迹。由此产生三类失败，都要到成片抽帧才被发现（白白浪费几十分钟渲染）：

1. **贴边/越画布**：图元画到 x<margin 或 x>W-margin，缩放成 1080×600 后字贴在
   画面边缘上，看起来就是「显示不全」。
2. **越遮罩**（更隐蔽）：文字压在 region 边界上，超出部分永远不被揭示。
   源图 PNG 是完整的，光看 PNG 查不出来——必须拿 region 去和墨迹做几何比对。
3. **压字幕**：图元画进 y≥762（画布坐标）的字幕带，烧录后被硬字幕压住。

v2 关键升级：**底图对比（--base）**
--------------------------------
项目1 这类「ImageGen 手绘线稿 + PIL 叠字」的片子，整张图到处是墨迹，直接量墨迹
边界只会量到线稿，量不到字。v2 用 `-enh.png` 与线稿底图做差，只留下**后画的
文字/卡片/便签**，再单独对这部分做边距与遮罩检查。没有底图时退化为全图检查。

用法
----
  python check_layout.py --image scene-01-xx-enh.png --spec spec-01.json
  python check_layout.py --image scene-01-xx-enh.png --annotation scene-01-xx.annotation.json
  python check_layout.py --image rich/scene-01-xx.png --base scene-01-xx.png \\
         --annotation scene-01-xx.annotation.json      # 底图对比模式
  python check_layout.py --dir .                       # 批量（自动找底图/标注）
  python check_layout.py --dir . --json report.json    # 输出机器可读报告
  python check_layout.py --dir . --fix specs/          # region 自动外扩（另存）

退出码：0 通过；1 有问题；2 用法/文件错误。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

import cv2
import numpy as np
from PIL import Image

DEFAULT_MARGIN = 24      # 距画布边缘的安全留白（1536×864 画布像素）
DEFAULT_SUBTOP = 762     # 字幕带起点（画布坐标）：1080×600 + MarginV36 + FS26 折算
TOL = 3                  # region 判定抖动容差 px
DIFF_THRESH = 30         # 底图对比阈值（0-255，越大越宽松）


# ---------------------------------------------------------------- 基础度量

def bg_color(im: Image.Image) -> np.ndarray:
    """四角采样中位值 → 纸色基准。"""
    arr = np.asarray(im.convert("RGB"), dtype=np.float32)
    h, w = arr.shape[:2]
    m = max(3, min(h, w) // 50)
    corners = np.concatenate([
        arr[:m, :m].reshape(-1, 3), arr[:m, -m:].reshape(-1, 3),
        arr[-m:, :m].reshape(-1, 3), arr[-m:, -m:].reshape(-1, 3),
    ])
    return np.median(corners, axis=0)


def ink_mask(im: Image.Image, thresh: int = 55) -> np.ndarray:
    """墨迹 = 明显比纸色暗，或色差足够大（彩色笔画）。

    只用「与四角纸色的通道差」会把纸张渐变/纹理也算成墨迹（整张表格被误判成
    一团），所以主判据是亮度落差，彩色笔画再用色差兜底。
    """
    arr = np.asarray(im.convert("RGB"), dtype=np.float32)
    bg = bg_color(im)
    lum = arr @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    bg_lum = float(bg @ np.array([0.299, 0.587, 0.114], dtype=np.float32))
    darker = (bg_lum - lum) > thresh
    colorful = np.abs(arr - bg[None, None, :]).max(axis=2) > (thresh * 2)
    return (darker | colorful).astype(np.uint8)


def added_mask(enh: Image.Image, base: Image.Image, thresh: int = DIFF_THRESH) -> np.ndarray:
    """后画的图元 = 与线稿底图差异明显的像素。

    只保留「增强版有墨、底图没有」的部分：底图本身就有的线稿不计入，避免整幅
    手绘图把边界撑满、把真正的文字溢出淹没掉。
    """
    a = np.asarray(enh.convert("RGB"), dtype=np.int16)
    b = np.asarray(base.convert("RGB"), dtype=np.int16)
    if a.shape != b.shape:
        raise ValueError(f"底图尺寸 {b.shape[1]}x{b.shape[0]} ≠ 增强图 {a.shape[1]}x{a.shape[0]}")
    diff = np.abs(a - b).max(axis=2)
    m = (diff > thresh).astype(np.uint8)
    # 底图上原本有墨、enh 上被清除的部分不算「新增」
    enh_ink = ink_mask(enh, 55)
    return (m & enh_ink).astype(np.uint8)


def rect(r):
    return (int(r["x"]), int(r["y"]),
            int(r["x"] + r["width"]), int(r["y"] + r["height"]))


def load_regions(spec_path, ann_path):
    """读出 region 列表（含每块掩码外扩量 pad）。

    `maskPaddingPx` 是渲染器的掩码外扩（旧版 annotation 默认 22）：真实揭示范围是
    region ± pad。漏掉这一项会把「其实被外扩盖住」的墨迹误报成「永远不显示」，
    项目1 V07 首次体检就因此多报了 6 处。
    """
    if spec_path:
        d = json.load(open(spec_path, encoding="utf-8"))
        out = []
        for r in d["regions"]:
            pad = int(r.get("maskPaddingPx", r.get("pad", 0)) or 0)
            out.append({"region": dict(r), "pad": pad})
        return out, d.get("canvas")
    d = json.load(open(ann_path, encoding="utf-8"))
    out = []
    for e in d["elements"]:
        pad = int((e.get("reveal") or {}).get("maskPaddingPx",
                                              e.get("maskPaddingPx", 0)) or 0)
        out.append({"region": dict(e["region"]), "pad": pad})
    return out, d.get("canvas")


def clusters(mask: np.ndarray, min_area: int = 120):
    """连通域 → [(x0,y0,x1,y1,area)]，用极小膨胀把同一条笔画上的散点并起来。"""
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    grown = cv2.dilate(mask, k)
    n, _, stats, _ = cv2.connectedComponentsWithStats(grown, connectivity=8)
    out = []
    for i in range(1, n):
        x, y, w, h, a = stats[i]
        if a < min_area:
            continue
        out.append((int(x) + 2, int(y) + 1, int(x + w) - 2, int(y + h) - 1, int(a)))
    return out


# ---------------------------------------------------------------- 底图自动配对

def find_base(img_path: str):
    """按项目里的几种命名习惯找线稿底图；找不到返回 None。

    支持：
      scene-01-xxx-enh.png      → scene-01-xxx-base.png / scene-01-xxx.png
      rich/scene-01-xxx.png     → 上级目录同名 scene-01-xxx.png（增强在最内层）
    """
    d, name = os.path.split(img_path)
    stem = name
    if stem.endswith("-enh.png"):
        stem = stem[:-len("-enh.png")]
    else:
        stem = stem[:-len(".png")]
    cands = [
        os.path.join(d, stem + "-base.png"),
        os.path.join(d, stem + ".png"),
        os.path.join(os.path.dirname(d), stem + ".png"),
        os.path.join(d, "rich", stem + ".png"),
    ]
    for c in cands:
        if os.path.abspath(c) != os.path.abspath(img_path) and os.path.exists(c):
            return c
    return None


def find_annotation(img_path: str):
    d, name = os.path.split(img_path)
    stem = name[:-len("-enh.png")] if name.endswith("-enh.png") else name[:-len(".png")]
    for cand in (os.path.join(d, stem + ".annotation.json"),
                 os.path.join(os.path.dirname(d), stem + ".annotation.json")):
        if os.path.exists(cand):
            return cand
    return None


# ---------------------------------------------------------------- 核心检查

def _ov_area(a, b) -> int:
    x0, y0 = max(a[0], b[0]), max(a[1], b[1])
    x1, y1 = min(a[2], b[2]), min(a[3], b[3])
    return max(0, x1 - x0) * max(0, y1 - y0)


def _best_region(blob, boxes):
    bi, bo = None, 0
    for i, b in enumerate(boxes):
        o = _ov_area(blob, b)
        if o > bo:
            bi, bo = i, o
    return bi, bo


def _max_out(blob, b) -> int:
    x0, y0, x1, y1 = blob[:4]
    return max(b[0] - x0, b[1] - y0, x1 - b[2], y1 - b[3], 0)


def _cosmetic(blob, boxes) -> bool:
    """判定「装饰线级溢出」，可忽略。

    两类可忽略：
    - 细条（高度或宽度 ≤10px 且面积小）：手绘双线描边/胶带边的抖动，
      1536→1080 缩放后不足 4px，肉眼不可见。
    - 部分可见且只溢出 ≤6px：字/框的边角被切掉一丝。

    绝不可忽略：**整块完全落在所有 region 之外**——那意味着这部分内容在成片里
    从头到尾都不会出现（项目3 V12 第三幕便签就这样整块消失过）。
    """
    x0, y0, x1, y1, area = blob
    if min(x1 - x0, y1 - y0) <= 10 and area <= 1200:
        return True
    bi, ov = _best_region(blob, boxes)
    if bi is None or ov == 0:
        return False
    return _max_out(blob, boxes[bi]) <= 6


def check(image_path, spec_path, ann_path, margin, thresh, verbose=False,
          base_path=None, subtop=DEFAULT_SUBTOP, diff=True):
    enh = Image.open(image_path).convert("RGB")
    W, H = enh.size

    base = None
    mode = "full"
    if diff and base_path:
        base = Image.open(base_path).convert("RGB")
        if base.size != enh.size:
            print(f"  [warn] 底图 {base.size} ≠ 增强图 {enh.size}，退回全图模式")
            base = None
    if base is not None:
        ink = added_mask(enh, base)
        mode = "diff"
    else:
        ink = ink_mask(enh, thresh)

    items, canvas = load_regions(spec_path, ann_path)
    regs = [it["region"] for it in items]
    boxes = []
    for it in items:
        b = rect(it["region"])
        p = it["pad"]
        boxes.append((max(0, b[0] - p), max(0, b[1] - p),
                      min(W, b[2] + p), min(H, b[3] + p)))

    if canvas and (canvas.get("width") != W or canvas.get("height") != H):
        print(f"  [warn] spec canvas {canvas.get('width')}x{canvas.get('height')} "
              f"≠ 图片 {W}x{H}")

    issues = []

    # --- 检查 1：图元贴边 / 越界（逐块量，不只看整体 bbox）
    # 整体 bbox 只能告诉我们「有东西贴边」，逐块才能指出哪一个文字块贴边。
    blobs = clusters(ink, min_area=150)
    edge_bad = []
    for (x0, y0, x1, y1, a) in blobs:
        if min(x1 - x0, y1 - y0) < 8:       # 细线（下划线/箭头）不当作文字块
            continue
        sp = []
        if x0 < margin:
            sp.append(("左", margin - x0, x0))
        if y0 < margin:
            sp.append(("上", margin - y0, y0))
        if x1 > W - margin:
            sp.append(("右", x1 - (W - margin), W - x1))
        if y1 > H - margin:
            sp.append(("下", y1 - (H - margin), H - y1))
        if sp:
            edge_bad.append(((x0, y0, x1, y1, a), sp))

    ys, xs = np.where(ink > 0)
    gbox = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())) if len(xs) else None
    if edge_bad:
        label = "新增图元" if mode == "diff" else "墨迹"
        print(f"  [BAD] {len(edge_bad)} 处{label}贴边/越界（安全边距 {margin}px）")
        for (bb, sp) in sorted(edge_bad, key=lambda t: -max(s[1] for s in t[1])):
            desc = "、".join(f"{s}侧距边 {dist}px" if s[0] in "左右"
                             else f"{s}侧距边 {dist}px" for s, dist, _ in sp)
            print(f"        bbox=({bb[0]},{bb[1]},{bb[2]},{bb[3]}) 面积{bb[4]} | {desc}")
            issues.append({"type": "edge", "bbox": list(bb[:4]), "area": bb[4],
                           "sides": [{"side": s, "deficit": d} for s, d, _ in sp]})

    # --- 检查 2：压进字幕带
    band_bad = [b for b in blobs if b[3] > subtop and min(b[2] - b[0], b[3] - b[1]) >= 8]
    if band_bad:
        print(f"  [BAD] {len(band_bad)} 处图元伸进字幕带 (y>{subtop})，烧录后会被字幕压住")
        for bb in sorted(band_bad, key=lambda t: -t[3])[:6]:
            print(f"        bbox=({bb[0]},{bb[1]},{bb[2]},{bb[3]}) 下沿 {bb[3]} > {subtop}")
            issues.append({"type": "subtitle_band", "bbox": list(bb[:4])})

    # --- 检查 3：不会被任何 region 揭示的墨迹
    visit = np.zeros((H, W), dtype=np.uint8)
    for b in boxes:
        visit[max(0, b[1] - TOL):min(H, b[3] + TOL),
              max(0, b[0] - TOL):min(W, b[2] + TOL)] = 1
    orphan = ((ink > 0) & (visit == 0)).astype(np.uint8)
    orph = clusters(orphan)
    severe = [o for o in orph if not _cosmetic(o, boxes)]
    minor = [o for o in orph if _cosmetic(o, boxes)]
    if severe:
        print(f"  [BAD] {len(severe)} 处墨迹落在所有 region 之外 → 成片里永远不显示")
    if minor:
        print(f"  [ok ] 另有 {len(minor)} 处装饰线级溢出（≤6px，缩放后不足 4px，可忽略）")
    for (x0, y0, x1, y1, a) in sorted(severe, key=lambda t: -t[4]):
        blobby = (x0, y0, x1, y1, a)
        best, ov = _best_region(blobby, boxes)
        side = ""
        if best is not None and ov > 0:
            b = boxes[best]
            sp = []
            if x0 < b[0]:
                sp.append(f"左 {b[0] - x0}px")
            if y0 < b[1]:
                sp.append(f"上 {b[1] - y0}px")
            if x1 > b[2]:
                sp.append(f"右 {x1 - b[2]}px")
            if y1 > b[3]:
                sp.append(f"下 {y1 - b[3]}px")
            side = f" → 应在 region#{best}" + (f"（溢出 {'、'.join(sp)}）" if sp else "")
        elif best is not None:
            b = boxes[best]
            d = max(b[0] - x1, b[1] - y1, x0 - b[2], y0 - b[3], 0)
            side = f" → 完全落在 region#{best} 之外（相距 {d}px）：这部分内容不会出现"
        print(f"        bbox=({x0},{y0},{x1},{y1}) 面积{a}{side}")
        issues.append({"type": "masked", "bbox": [x0, y0, x1, y1],
                       "area": a, "region": best, "sides": side})

    if verbose and gbox:
        print(f"  [info] 整体 bbox={gbox}  模式={mode}")

    return {"image": image_path, "base": base_path, "mode": mode,
            "size": [W, H], "regions": len(regs), "issues": issues,
            "reg_boxes": boxes, "minor": len(minor), "gbox": list(gbox) if gbox else None}


# ---------------------------------------------------------------- 自动修正

def fix_regions(regs, info, W, H):
    """把 region 撑到包住「本该由它揭示却被裁」的墨迹，且不侵入相邻 region。"""
    boxes = [rect(r) for r in regs]
    want = {}
    for it in info["issues"]:
        if it["type"] != "masked":
            continue
        b = it["bbox"]
        ri = it["region"]
        if ri is None:
            # 整块落在所有 region 之外：按最近距离归属（超过 200px 就不管，
            # 那已经不是「漂移」而是画错了位置）
            best, bd = None, 1e18
            for i, rb in enumerate(boxes):
                dx = max(rb[0] - b[2], b[0] - rb[2], 0)
                dy = max(rb[1] - b[3], b[1] - rb[3], 0)
                if dx + dy < bd:
                    best, bd = i, dx + dy
            if best is None or bd > 200:
                continue
            ri = best
        cur = want.get(ri, list(boxes[ri]))
        want[ri] = [min(cur[0], b[0]), min(cur[1], b[1]),
                    max(cur[2], b[2]), max(cur[3], b[3])]

    fixed = 0
    for ri, t in want.items():
        base = boxes[ri]
        q = [max(0, min(base[0], t[0])), max(0, min(base[1], t[1])),
             min(W, max(base[2], t[2])), min(H, max(base[3], t[3]))]
        for j, ob in enumerate(boxes):
            if j == ri:
                continue
            if q[2] <= ob[0] or q[0] >= ob[2] or q[3] <= ob[1] or q[1] >= ob[3]:
                continue                      # 无交叠
            # 有交叠：沿原 base 的方向把扩张止在邻块边界
            if base[2] <= ob[0]:
                q[2] = min(q[2], ob[0])
            if base[0] >= ob[2]:
                q[0] = max(q[0], ob[2])
            if base[3] <= ob[1]:
                q[3] = min(q[3], ob[1])
            if base[1] >= ob[3]:
                q[1] = max(q[1], ob[3])
        if q != list(base):
            print(f"    [fix] region#{ri} {tuple(base)} → {tuple(q)}")
            regs[ri]["x"], regs[ri]["y"] = q[0], q[1]
            regs[ri]["width"], regs[ri]["height"] = q[2] - q[0], q[3] - q[1]
            fixed += 1
    return fixed


# ---------------------------------------------------------------- CLI

def run_one(img, spec, ann, a, out_spec=None, base=None):
    print(f"\n== {os.path.basename(img)} ==")
    if base is None and a.base != "off":
        base = a.base if (a.base and a.base not in ("auto", "off")) else find_base(img)
    if base and os.path.abspath(base) == os.path.abspath(img):
        base = None
    info = check(img, spec, ann, a.margin, a.thresh, a.verbose,
                 base_path=base, subtop=a.subtop, diff=(a.base != "off"))
    if base:
        print(f"   [mode] 底图对比：{os.path.basename(base)}")
    if not info["issues"]:
        m = info.get("minor", 0)
        print(f"  ✓ 通过：{info['regions']} 个 region，图元全部可见且在安全区内"
              + (f"（{m} 处装饰线级溢出可忽略）" if m else ""))
        return 0, info
    print(f"  → 共 {len(info['issues'])} 处问题")
    if out_spec and spec:
        d = json.load(open(spec, encoding="utf-8"))
        n = fix_regions(d["regions"], info, info["size"][0], info["size"][1])
        if n:
            od = os.path.dirname(out_spec)
            if od:
                os.makedirs(od, exist_ok=True)
            json.dump(d, open(out_spec, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            print(f"    已写出 → {out_spec}")
            left = len(check(img, out_spec, None, a.margin, a.thresh,
                             base_path=base, subtop=a.subtop)["issues"])
            print(f"    复核：剩余 {left} 处" +
                  ("（贴边项要改绘制坐标，改 region 解决不了）" if left else " ✓"))
    return 1, info


def main():
    ap = argparse.ArgumentParser(description="画面版式体检：查文字贴边、被遮罩裁切、压字幕")
    ap.add_argument("--image")
    ap.add_argument("--spec", help="spec-0N.json")
    ap.add_argument("--annotation", help="或 *.annotation.json")
    ap.add_argument("--dir", help="批量：目录下所有 *-enh.png（或 rich/*.png）")
    ap.add_argument("--base", default="auto",
                    help="线稿底图：auto（默认，自动找）/ off（关掉，全图模式）/ 具体路径")
    ap.add_argument("--margin", type=int, default=DEFAULT_MARGIN, help="安全留白 px（默认 24）")
    ap.add_argument("--subtop", type=int, default=DEFAULT_SUBTOP,
                    help="字幕带上沿（画布 y，默认 762；设 9999 可关闭该检查）")
    ap.add_argument("--thresh", type=int, default=55, help="墨迹亮度落差阈值（默认 55）")
    ap.add_argument("--fix", help="修正输出目录（按同名 spec-0N.json 写回）")
    ap.add_argument("--json", help="把结果写成 JSON 报告")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    report = {"margin": a.margin, "subtop": a.subtop, "scenes": []}

    if a.dir:
        imgs = sorted(glob.glob(os.path.join(a.dir, "**", "*-enh.png"), recursive=True))
        # 兼容「增强图直接覆盖原名」的片子（如项目1 V01：增强图在 rich/ 下）：
        # 按子目录逐个补齐，避免整棵树里只要有 *-enh.png 就漏掉这些目录。
        have = {os.path.dirname(p) for p in imgs}
        for sub in sorted(glob.glob(os.path.join(a.dir, "*"))):
            if not os.path.isdir(sub):
                continue
            src = sub if os.path.basename(sub) == "rich" else os.path.join(sub, "rich")
            if not os.path.isdir(src) or src in have:
                continue
            rich = [p for p in glob.glob(os.path.join(src, "*.png"))
                    if "-preview" not in p and "hand" not in p]
            if rich:
                imgs += rich
        imgs = sorted(set(imgs))
        if not imgs:
            print("未找到 *-enh.png（也没有 rich/*.png）")
            return 2
        bad = 0
        for img in imgs:
            d = os.path.dirname(img)
            # spec 优先（spec-01.json），否则 annotation
            m = re.match(r"scene-(\d+)", os.path.basename(img))
            spec = os.path.join(d, f"spec-{m.group(1)}.json") if m else None
            if spec and not os.path.exists(spec):
                spec = None
            ann = find_annotation(img) or (img[:-len("-enh.png")] + ".annotation.json"
                                           if img.endswith("-enh.png") else None)
            if spec is None and (ann is None or not os.path.exists(ann)):
                print(f"\n== {os.path.basename(img)} ==\n  跳过：找不到 spec / annotation")
                continue
            base = find_base(img) if a.base == "auto" else (
                None if a.base == "off" else a.base)
            if base and os.path.abspath(base) == os.path.abspath(img):
                base = None
            out = os.path.join(a.fix, os.path.basename(spec)) if (a.fix and spec) else None
            rc, info = run_one(img, spec, None if spec else ann, a, out, base)
            bad += rc
            report["scenes"].append({
                "image": os.path.relpath(img, a.dir), "base": base,
                "mode": info["mode"], "issues": info["issues"],
                "minor": info["minor"], "gbox": info["gbox"],
            })
        print(f"\n合计 {len(imgs)} 张，{bad} 张有问题")
        report["total"] = len(imgs)
        report["bad"] = bad
        if a.json:
            json.dump(report, open(a.json, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=2)
            print(f"报告 → {a.json}")
        return 0 if bad == 0 else 1

    if not a.image:
        ap.error("需要 --image 或 --dir")
    base = find_base(a.image) if a.base == "auto" else (None if a.base == "off" else a.base)
    if a.spec:
        out = a.fix or a.spec.replace(".json", ".fixed.json")
        rc, _ = run_one(a.image, a.spec, None, a, out, base)
        return rc
    rc, _ = run_one(a.image, None, a.annotation, a, None, base)
    return rc


if __name__ == "__main__":
    sys.exit(main())
