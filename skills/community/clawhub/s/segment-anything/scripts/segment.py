#!/usr/bin/env python3
"""基于 SAM 的背景去除工具。输出透明背景的 PNG 文件。"""

import argparse
import os
import urllib.request

import numpy as np


CHECKPOINTS = {
    "vit_b": ("sam_vit_b_01ec64.pth", "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth"),
    "vit_l": ("sam_vit_l_0b3195.pth", "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth"),
    "vit_h": ("sam_vit_h_4b8939.pth", "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"),
}


def ensure_checkpoint(model_type, checkpoint=None):
    """确保模型权重文件存在，不存在则自动下载。"""
    if checkpoint and os.path.exists(checkpoint):
        return checkpoint
    cache_dir = os.path.expanduser("~/.cache/sam")
    os.makedirs(cache_dir, exist_ok=True)
    filename, url = CHECKPOINTS[model_type]
    path = os.path.join(cache_dir, filename)
    if not os.path.exists(path):
        size_mb = dict(vit_b=375, vit_l=1250, vit_h=2560)[model_type]
        print(f"正在下载 SAM {model_type} 权重文件（约 {size_mb}MB）...")
        urllib.request.urlretrieve(url, path, reporthook=lambda b, bs, t: print(f"\r  {min(b*bs,t)*100//t}%", end="", flush=True) if t > 0 else None)
        print()
    return path


def _load_sam(model_type, checkpoint):
    """加载 SAM 模型，首次运行时自动安装 segment_anything。"""
    try:
        from segment_anything import SamPredictor, sam_model_registry
    except ImportError:
        print("正在安装 segment_anything...")
        os.system("pip install git+https://github.com/facebookresearch/segment-anything.git -q")
        from segment_anything import SamPredictor, sam_model_registry

    import torch

    ckpt = ensure_checkpoint(model_type, checkpoint)
    sam = sam_model_registry[model_type](checkpoint=ckpt)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    sam.to(device)
    print(f"模型已加载至 {device}")
    return SamPredictor(sam)


def segment(image_path, output_path, checkpoint=None, model_type="vit_b", points=None):
    """单目标分割：使用一个或多个提示点提取前景主体。"""
    from PIL import Image

    predictor = _load_sam(model_type, checkpoint)
    image = np.array(Image.open(image_path).convert("RGB"))
    h, w = image.shape[:2]
    predictor.set_image(image)

    pts = np.array(points if points else [[w // 2, h // 2]])
    labels = np.ones(len(pts), dtype=int)
    masks, scores, _ = predictor.predict(point_coords=pts, point_labels=labels, multimask_output=True)

    best = masks[np.argmax(scores)]
    rgba = np.dstack([image, (best * 255).astype(np.uint8)])
    Image.fromarray(rgba).save(output_path)
    print(f"已保存: {output_path}")


def segment_all(image_path, output_dir, checkpoint=None, model_type="vit_b", grid=16, iou_thresh=0.88, min_area=0.001):
    """全元素分割：通过网格探测提取图像中所有独立元素。

    对每个网格点，SAM 预测一个掩码。通过 IoU 去重——仅保留与已接受掩码
    不存在大面积重叠的掩码。每个独立元素保存为单独的透明 PNG。
    """
    from PIL import Image

    predictor = _load_sam(model_type, checkpoint)
    image = np.array(Image.open(image_path).convert("RGB"))
    h, w = image.shape[:2]
    predictor.set_image(image)

    os.makedirs(output_dir, exist_ok=True)
    min_pixels = int(h * w * min_area)

    # 构建网格探测点
    xs = [int(w * (i + 0.5) / grid) for i in range(grid)]
    ys = [int(h * (j + 0.5) / grid) for j in range(grid)]
    grid_points = [[x, y] for y in ys for x in xs]

    accepted_masks = []  # 已接受的掩码列表: (bool数组, 分数)

    print(f"正在探测 {len(grid_points)} 个网格点（{grid}x{grid}）...")
    for pt in grid_points:
        masks, scores, _ = predictor.predict(
            point_coords=np.array([pt]),
            point_labels=np.array([1]),
            multimask_output=True,
        )
        best = masks[np.argmax(scores)]
        score = float(scores.max())

        if score < iou_thresh:
            continue
        if best.sum() < min_pixels:
            continue

        # 去重：跳过与已接受掩码高度重叠的结果
        duplicate = False
        for prev_mask, _ in accepted_masks:
            intersection = (best & prev_mask).sum()
            union = (best | prev_mask).sum()
            if union > 0 and intersection / union > 0.5:
                duplicate = True
                break
        if not duplicate:
            accepted_masks.append((best, score))

    print(f"共发现 {len(accepted_masks)} 个独立元素")
    for i, (mask, _) in enumerate(accepted_masks):
        rgba = np.dstack([image, (mask * 255).astype(np.uint8)])
        out_path = os.path.join(output_dir, f"element_{i:03d}.png")
        Image.fromarray(rgba).save(out_path)
        print(f"  已保存: {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="使用 SAM 去除图像背景")
    parser.add_argument("input", help="输入图像路径")
    parser.add_argument("output", help="输出 PNG 路径（单目标模式）或输出目录（--all 模式）")
    parser.add_argument("--checkpoint", help="本地 SAM 权重文件路径（省略时自动下载）")
    parser.add_argument("--model", default="vit_h", choices=["vit_b", "vit_l", "vit_h"],
                        help="模型大小: vit_b（快速）, vit_l（中等）, vit_h（最佳质量）")
    parser.add_argument("--points", nargs="+", metavar="X,Y",
                        help="前景提示点，例如 --points 320,240 400,300")
    parser.add_argument("--all", action="store_true",
                        help="网格扫描模式：提取所有元素，输出为目录")
    parser.add_argument("--grid", type=int, default=16,
                        help="--all 模式的网格密度（默认: 16，即 16x16=256 个探测点）")
    parser.add_argument("--iou-thresh", type=float, default=0.88,
                        help="接受掩码的最低预测 IoU（默认: 0.88）")
    parser.add_argument("--min-area", type=float, default=0.001,
                        help="掩码最小面积占图像比例（默认: 0.001）")
    args = parser.parse_args()

    if args.all:
        segment_all(args.input, args.output, args.checkpoint, args.model,
                    args.grid, args.iou_thresh, args.min_area)
    else:
        points = [[int(v) for v in p.split(",")] for p in args.points] if args.points else None
        segment(args.input, args.output, args.checkpoint, args.model, points)
