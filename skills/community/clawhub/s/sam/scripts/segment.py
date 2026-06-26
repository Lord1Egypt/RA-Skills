#!/usr/bin/env python3
"""SAM-based background removal. Outputs PNG with transparent background."""

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
    if checkpoint and os.path.exists(checkpoint):
        return checkpoint
    cache_dir = os.path.expanduser("~/.cache/sam")
    os.makedirs(cache_dir, exist_ok=True)
    filename, url = CHECKPOINTS[model_type]
    path = os.path.join(cache_dir, filename)
    if not os.path.exists(path):
        print(f"Downloading SAM {model_type} checkpoint (~{dict(vit_b=375,vit_l=1250,vit_h=2560)[model_type]}MB)...")
        urllib.request.urlretrieve(url, path, reporthook=lambda b, bs, t: print(f"\r  {min(b*bs,t)*100//t}%", end="", flush=True) if t > 0 else None)
        print()
    return path


def _load_sam(model_type, checkpoint):
    try:
        from segment_anything import SamPredictor, sam_model_registry
    except ImportError:
        print("Installing segment_anything...")
        os.system("pip install git+https://github.com/facebookresearch/segment-anything.git -q")
        from segment_anything import SamPredictor, sam_model_registry

    import torch

    ckpt = ensure_checkpoint(model_type, checkpoint)
    sam = sam_model_registry[model_type](checkpoint=ckpt)
    sam.to("cuda" if torch.cuda.is_available() else "cpu")
    return SamPredictor(sam)


def segment(image_path, output_path, checkpoint=None, model_type="vit_b", points=None):
    """Single-subject segmentation using one or more hint points."""
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
    print(f"Saved: {output_path}")


def segment_all(image_path, output_dir, checkpoint=None, model_type="vit_b", grid=16, iou_thresh=0.88, min_area=0.001):
    """Segment all distinct elements by probing a grid of points across the image.

    For each grid point, SAM predicts a mask. Duplicate/overlapping masks are
    deduplicated via IoU — only masks that don't substantially overlap an
    already-accepted mask are kept. Each unique element is saved as a separate
    transparent PNG.
    """
    from PIL import Image

    predictor = _load_sam(model_type, checkpoint)
    image = np.array(Image.open(image_path).convert("RGB"))
    h, w = image.shape[:2]
    predictor.set_image(image)

    os.makedirs(output_dir, exist_ok=True)
    min_pixels = int(h * w * min_area)

    # Build grid points
    xs = [int(w * (i + 0.5) / grid) for i in range(grid)]
    ys = [int(h * (j + 0.5) / grid) for j in range(grid)]
    grid_points = [[x, y] for y in ys for x in xs]

    accepted_masks = []  # list of (bool array, score)

    print(f"Probing {len(grid_points)} grid points ({grid}x{grid})...")
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

        # Deduplicate: skip if this mask overlaps heavily with an accepted one
        duplicate = False
        for prev_mask, _ in accepted_masks:
            intersection = (best & prev_mask).sum()
            union = (best | prev_mask).sum()
            if union > 0 and intersection / union > 0.5:
                duplicate = True
                break
        if not duplicate:
            accepted_masks.append((best, score))

    print(f"Found {len(accepted_masks)} unique elements")
    for i, (mask, _) in enumerate(accepted_masks):
        rgba = np.dstack([image, (mask * 255).astype(np.uint8)])
        out_path = os.path.join(output_dir, f"element_{i:03d}.png")
        Image.fromarray(rgba).save(out_path)
        print(f"  Saved: {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove image background using SAM")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output PNG path (single mode) or output directory (--all mode)")
    parser.add_argument("--checkpoint", help="Local SAM checkpoint path (auto-downloaded if omitted)")
    parser.add_argument("--model", default="vit_h", choices=["vit_b", "vit_l", "vit_h"],
                        help="Model size: vit_b (fast/small), vit_l (medium), vit_h (best quality)")
    parser.add_argument("--points", nargs="+", metavar="X,Y",
                        help="Foreground hint points, e.g. --points 320,240 400,300")
    parser.add_argument("--all", action="store_true",
                        help="Segment all elements via grid sampling; output is a directory")
    parser.add_argument("--grid", type=int, default=16,
                        help="Grid density for --all mode (default: 16, i.e. 16x16=256 probe points)")
    parser.add_argument("--iou-thresh", type=float, default=0.88,
                        help="Minimum predicted IoU to accept a mask (default: 0.88)")
    parser.add_argument("--min-area", type=float, default=0.001,
                        help="Minimum mask area as fraction of image (default: 0.001)")
    args = parser.parse_args()

    if args.all:
        segment_all(args.input, args.output, args.checkpoint, args.model,
                    args.grid, args.iou_thresh, args.min_area)
    else:
        points = [[int(v) for v in p.split(",")] for p in args.points] if args.points else None
        segment(args.input, args.output, args.checkpoint, args.model, points)
