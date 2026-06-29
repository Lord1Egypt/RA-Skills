#!/usr/bin/env python3
"""
图片去水印工具 — 基于 OpenCV inpainting 算法
支持自动检测水印区域和手动指定水印区域两种模式。
"""

import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np


def detect_watermark_region(image: np.ndarray) -> tuple | None:
    """
    自动检测可能的水印区域。
    策略：检测图像右下角和左下角的高频纹理区域（水印通常位于角落）。
    返回 (x1, y1, x2, y2) 或 None。
    """
    h, w = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 检查右下角 1/4 区域
    regions = [
        ("右下角", gray[h * 3 // 4 :, w * 3 // 4 :], w * 3 // 4, h * 3 // 4),
        ("左下角", gray[h * 3 // 4 :, : w // 4], 0, h * 3 // 4),
        ("右上角", gray[: h // 4, w * 3 // 4 :], w * 3 // 4, 0),
        ("左上角", gray[: h // 4, : w // 4], 0, 0),
    ]

    best_region = None
    best_variance = 0

    for name, region, ox, oy in regions:
        if region.size == 0:
            continue
        # 计算局部方差（水印区域方差通常较高）
        local_var = np.var(region.astype(np.float64))
        # 边缘检测强度
        edges = cv2.Canny(region, 50, 150)
        edge_ratio = np.count_nonzero(edges) / region.size

        # 综合评分
        score = local_var * 0.4 + edge_ratio * 100 * 0.6

        if score > best_variance:
            best_variance = score
            rh, rw = region.shape[:2]
            best_region = (name, ox, oy, ox + rw, oy + rh)

    if best_variance < 50:  # 阈值太低说明没有明显水印
        return None

    return best_region[1:]  # (x1, y1, x2, y2)


def remove_watermark(
    input_path: str,
    output_path: str,
    x1: int = None,
    y1: int = None,
    x2: int = None,
    y2: int = None,
    auto: bool = True,
    inpaint_radius: int = 5,
) -> dict:
    """
    执行去水印操作。
    """
    img = cv2.imread(input_path)
    if img is None:
        return {"success": False, "error": f"无法读取图片: {input_path}"}

    h, w = img.shape[:2]

    # 确定水印区域
    if all(v is not None for v in [x1, y1, x2, y2]):
        mask_x1, mask_y1 = max(0, x1), max(0, y1)
        mask_x2, mask_y2 = min(w, x2), min(h, y2)
        method = "手动选区"
    elif auto:
        region = detect_watermark_region(img)
        if region is None:
            return {
                "success": True,
                "warning": "未检测到明显水印区域，图片可能无需去水印",
                "output": output_path,
                "method": "自动检测",
                "file_size": Path(input_path).stat().st_size,
            }
        mask_x1, mask_y1, mask_x2, mask_y2 = region
        method = "自动检测"
    else:
        return {"success": False, "error": "请指定水印区域 (--x1 --y1 --x2 --y2) 或使用 --auto"}

    # 验证区域有效性
    if mask_x2 <= mask_x1 or mask_y2 <= mask_y1:
        return {"success": False, "error": "水印区域无效"}

    # 创建水印掩膜
    mask = np.zeros((h, w), dtype=np.uint8)
    # 在掩膜区域检测水印（使用自适应阈值找到水印像素）
    roi = img[mask_y1:mask_y2, mask_x1:mask_x2]
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # 使用自适应阈值检测水印（水印通常是半透明的，亮度不同）
    thresh = cv2.adaptiveThreshold(
        roi_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 8
    )
    # 膨胀使掩膜更完整
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=1)

    mask[mask_y1:mask_y2, mask_x1:mask_x2] = thresh

    # 使用 Telea 算法修复
    result = cv2.inpaint(img, mask, inpaint_radius, cv2.INPAINT_TELEA)

    # 保存结果
    cv2.imwrite(output_path, result)

    input_size = Path(input_path).stat().st_size
    output_size = Path(output_path).stat().st_size

    return {
        "success": True,
        "output": output_path,
        "method": method,
        "region": {"x1": mask_x1, "y1": mask_y1, "x2": mask_x2, "y2": mask_y2},
        "input_size": input_size,
        "output_size": output_size,
        "image_size": {"width": w, "height": h},
    }


def main():
    parser = argparse.ArgumentParser(description="图片去水印工具")
    parser.add_argument("input", help="输入图片路径")
    parser.add_argument("-o", "--output", help="输出图片路径（默认: 原文件名_nowm.ext）")
    parser.add_argument("--x1", type=int, help="水印区域左上角 X")
    parser.add_argument("--y1", type=int, help="水印区域左上角 Y")
    parser.add_argument("--x2", type=int, help="水印区域右下角 X")
    parser.add_argument("--y2", type=int, help="水印区域右下角 Y")
    parser.add_argument("--auto", action="store_true", default=True, help="自动检测水印（默认）")
    parser.add_argument("--no-auto", action="store_true", help="禁用自动检测")
    parser.add_argument("--radius", type=int, default=5, help="修复半径 (1-20, 默认5)")

    args = parser.parse_args()

    # 确定输出路径
    input_path = Path(args.input)
    if not input_path.exists():
        print(json.dumps({"success": False, "error": f"文件不存在: {args.input}"}))
        sys.exit(1)

    if args.output:
        output_path = args.output
    else:
        output_path = str(input_path.parent / f"{input_path.stem}_nowm{input_path.suffix}")

    auto = args.auto and not args.no_auto

    result = remove_watermark(
        input_path=str(input_path),
        output_path=output_path,
        x1=args.x1,
        y1=args.y1,
        x2=args.x2,
        y2=args.y2,
        auto=auto,
        inpaint_radius=args.radius,
    )

    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
