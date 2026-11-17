#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
水印清除器 —— 投稿前清除生图服务加的角标水印

支持三种定位方式：
  --region "x,y,w,h"   像素坐标精确指定（最准，推荐）
  --corner br          角落方位，配合 --area 比例（tl/tr/bl/br/top/bottom）
  --auto               自动检测四角与底部条带（会输出置信度，建议先看预览）

清除方式（--method）：
  inpaint  OpenCV 区域修复，效果最好（需 opencv-python）
  fill     取水印外围主色填充，适合纯色/渐变背景（默认，零额外依赖）
  crop     裁掉水印区域（会改变构图，仅兜底）

用法:
  # 先生成预览，确认框选区域是否正确
  python scripts/remove_watermark.py --input ./raw --corner br --preview

  # 确认后清除
  python scripts/remove_watermark.py --input ./raw --corner br --method fill

  python scripts/remove_watermark.py --input ./raw/01.png --region "900,1010,180,60" --method inpaint

合规提醒：仅用于清除你自己生成的、拥有权利的图片上的工具水印。
去除他人作品的版权水印可能违反法律与平台规则。
"""
import argparse
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("[缺少依赖] 请先安装：pip install Pillow")

IMG_EXT = (".png", ".jpg", ".jpeg", ".webp", ".bmp")


# ---------------------------------------------------------------- 区域计算

def region_from_corner(size, corner, area):
    """按方位 + 比例算出水印矩形 (x, y, w, h)"""
    w, h = size
    aw, ah = area
    rw, rh = int(w * aw), int(h * ah)
    rw, rh = max(rw, 8), max(rh, 8)
    if corner == "tl":
        return 0, 0, rw, rh
    if corner == "tr":
        return w - rw, 0, rw, rh
    if corner == "bl":
        return 0, h - rh, rw, rh
    if corner == "br":
        return w - rw, h - rh, rw, rh
    if corner == "top":
        return (w - rw) // 2, 0, rw, rh
    if corner == "bottom":
        return (w - rw) // 2, h - rh, rw, rh
    raise SystemExit(f"[错误] 未知方位: {corner}")


def detect_auto(img):
    """
    自动检测：在四角与底部条带中，寻找"与区域主色差异大且占比适中"的异常像素块
    返回 (region, confidence, note)
    """
    w, h = img.size
    gray = img.convert("L")
    px = gray.load()
    best, best_score = None, 0.0
    zones = {
        "br": (int(w * 0.70), int(h * 0.88), w, h),
        "bl": (0, int(h * 0.88), int(w * 0.30), h),
        "tr": (int(w * 0.70), 0, w, int(h * 0.12)),
        "tl": (0, 0, int(w * 0.30), int(h * 0.12)),
    }
    for name, (x0, y0, x1, y1) in zones.items():
        vals = []
        step = max(1, (x1 - x0) // 60)
        for y in range(y0, y1, max(1, step)):
            for x in range(x0, x1, step):
                vals.append(px[x, y])
        if not vals:
            continue
        vals.sort()
        median = vals[len(vals) // 2]
        # 与中位数差异大的像素占比（水印通常是亮色文字/半透明块）
        diff = sum(1 for v in vals if abs(v - median) > 45)
        ratio = diff / len(vals)
        score = ratio if 0.01 < ratio < 0.6 else 0.0
        if score > best_score:
            best_score, best = score, name
    if not best:
        return None, 0.0, "未检测到明显水印（图像可能是干净的）"
    region = region_from_corner((w, h), best, (0.30, 0.10))
    return region, best_score, f"疑似水印位于 {best} 区域"


# ---------------------------------------------------------------- 清除实现

def clear_inpaint(img, region):
    """OpenCV 区域修复"""
    try:
        import cv2
        import numpy as np
    except ImportError:
        return None
    x, y, w, h = region
    arr = np.array(img.convert("RGB"))[:, :, ::-1]  # RGB -> BGR
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    mask[y:y + h, x:x + w] = 255
    out = cv2.inpaint(arr, mask, 5, cv2.INPAINT_TELEA)
    out = out[:, :, ::-1]  # BGR -> RGB
    return Image.fromarray(out).convert(img.mode)


def clear_fill(img, region):
    """取水印区域外围一圈的主色，填充该区域（区域外扩 3px，吃掉边缘残线）"""
    pad = 3
    x, y, w, h = region
    x, y = max(0, x - pad), max(0, y - pad)
    w, h = w + 2 * pad, h + 2 * pad
    W, H = img.size
    w, h = min(w, W - x), min(h, H - y)
    img = img.convert("RGB")
    # 采样外围环带像素
    band = 6
    samples = []
    for yy in range(max(0, y - band), min(H, y + h + band)):
        for xx in range(max(0, x - band), min(W, x + w + band)):
            inside = x <= xx < x + w and y <= yy < y + h
            if not inside:
                samples.append(img.getpixel((xx, yy)))
    if not samples:
        samples = [img.getpixel((0, 0))]
    samples.sort(key=lambda c: sum(c))
    color = samples[len(samples) // 2]  # 中位色，抗噪
    draw = ImageDraw.Draw(img)
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=color)
    return img


def clear_crop(img, region):
    """裁掉水印区域（会改变构图与画幅）"""
    x, y, w, h = region
    W, H = img.size
    # 优先裁掉底部或顶部整条
    if y + h >= H - 2:
        return img.crop((0, 0, W, max(1, y)))
    if y <= 2:
        return img.crop((0, min(H - 1, y + h), W, H))
    return img.crop((0, 0, W, y))


def process(src, dst, region, method, preview=False):
    img = Image.open(src)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    if preview:
        pv = img.convert("RGBA")
        overlay = Image.new("RGBA", pv.size, (255, 0, 0, 0))
        ImageDraw.Draw(overlay).rectangle(
            [region[0], region[1], region[0] + region[2] - 1, region[1] + region[3] - 1],
            fill=(255, 0, 0, 90), outline=(255, 0, 0, 220), width=2)
        Image.alpha_composite(pv, overlay).save(dst)
        return None

    if method == "inpaint":
        out = clear_inpaint(img, region)
        if out is None:
            out = clear_fill(img, region)
            method_used = "fill（未装 opencv，自动降级）"
        else:
            method_used = "inpaint"
    elif method == "crop":
        out, method_used = clear_crop(img, region), "crop"
    else:
        out, method_used = clear_fill(img, region), "fill"

    out.save(dst)
    return method_used


def main():
    ap = argparse.ArgumentParser(description="表情包水印清除")
    ap.add_argument("--input", "-i", required=True, help="图片文件或目录")
    ap.add_argument("--output", "-o", default="cleaned", help="输出目录")
    ap.add_argument("--region", help='像素坐标 "x,y,w,h"')
    ap.add_argument("--corner", choices=["tl", "tr", "bl", "br", "top", "bottom"],
                    help="水印方位")
    ap.add_argument("--area", default="0.30,0.10", help="水印区域占画面比例 宽,高（配合 --corner）")
    ap.add_argument("--auto", action="store_true", help="自动检测水印位置")
    ap.add_argument("--method", choices=["inpaint", "fill", "crop"], default="fill")
    ap.add_argument("--preview", action="store_true", help="只生成红色框选预览，不修改图片")
    args = ap.parse_args()

    src = os.path.abspath(args.input)
    files = ([os.path.basename(src)] if os.path.isfile(src)
             else sorted(f for f in os.listdir(src) if f.lower().endswith(IMG_EXT)))
    base = os.path.dirname(src) if os.path.isfile(src) else src
    if not files:
        sys.exit(f"[错误] 没找到图片: {src}")

    out_dir = os.path.abspath(args.output)
    os.makedirs(out_dir, exist_ok=True)

    # 自动检测时，用第一张确定区域，套用到全部
    global_region = None
    note = ""
    if args.auto:
        sample = Image.open(os.path.join(base, files[0]))
        global_region, conf, note = detect_auto(sample)
        print(f"[自动检测] {note}（置信度 {conf:.0%}）")
        if global_region:
            print(f"[自动检测] 区域 = x{global_region[0]} y{global_region[1]} "
                  f"{global_region[2]}×{global_region[3]}，将套用到全部图片")
        else:
            print("[自动检测] 未发现水印，如确实存在请改用 --region 精确指定")
            return

    print(f"[信息] 共 {len(files)} 张，模式: {'预览' if args.preview else '清除(' + args.method + ')'}\n")

    for i, fn in enumerate(files, 1):
        path = os.path.join(base, fn)
        if global_region:
            region = global_region
        elif args.region:
            region = tuple(int(v) for v in args.region.replace("，", ",").split(","))
            if len(region) != 4:
                sys.exit("[错误] --region 需为 x,y,w,h 四个数字")
        elif args.corner:
            aw, ah = (float(v) for v in args.area.replace("，", ",").split(","))
            region = region_from_corner(Image.open(path).size, args.corner, (aw, ah))
        else:
            sys.exit("[错误] 请用 --region / --corner / --auto 指定水印位置")

        suffix = "_preview.png" if args.preview else "_clean.png"
        dst = os.path.join(out_dir, os.path.splitext(fn)[0] + suffix)
        used = process(path, dst, region, args.method, args.preview)
        tag = "" if args.preview else f"  方式={used}"
        print(f"  {i:02d}. {fn} → {os.path.basename(dst)}{tag}")

    print(f"\n[完成] 输出目录: {out_dir}")
    if args.preview:
        print("[下一步] 打开预览图确认红框是否盖住水印；")
        print("         区域不准就调整 --region/--corner/--area，确认后去掉 --preview 正式清除。")
    print("[合规] 仅用于清除自己拥有权利的图片上的工具水印。")


if __name__ == "__main__":
    main()
