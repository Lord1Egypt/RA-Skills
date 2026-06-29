#!/usr/bin/env python3
"""
Watermark Remover — Florence-2 detection + IOPaint (LaMa) inpainting pipeline.

Usage:
    python remove_watermark.py --input photo.jpg --output photo_clean.jpg
    python remove_watermark.py --input ./photos/ --output ./photos_clean/
    python remove_watermark.py --input dir/ --output out/ --suffix _clean
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Optional

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tiff", ".tif"}


def detect_watermarks_florence(image_path: Path, confidence: float = 0.5) -> list:
    """Detect watermarks using Florence-2 with natural language prompt."""
    try:
        from transformers import AutoProcessor, AutoModelForCausalLM
        from PIL import Image
        import torch
    except ImportError:
        print("ERROR: transformers, torch, and pillow required. Install with:")
        print("  pip install transformers torch pillow")
        sys.exit(1)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu" and hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device = "mps"

    model_id = "microsoft/Florence-2-base"
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, trust_remote_code=True
    ).to(device)

    image = Image.open(image_path)
    w, h = image.size

    # Try OCR mode first (best for text watermarks like MLS)
    boxes = []
    for task in ["<OCR_WITH_REGION>", "<OD>"]:
        inputs = processor(text=task, images=image, return_tensors="pt").to(device)
        with torch.no_grad():
            generated_ids = model.generate(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                max_new_tokens=1024,
                num_beams=3,
                do_sample=False,
            )
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
        parsed = processor.post_process_generation(generated_text, task=task, image_size=(w, h))

        parsed_key = list(parsed.keys())[0] if parsed else None

        if task == "<OCR_WITH_REGION>" and parsed_key:
            region = parsed[parsed_key]
            if "quad_boxes" in region:
                for box, text in zip(region["quad_boxes"], region["labels"]):
                    # Strip </s> token prefix from Florence-2
                    text = text.replace("</s>", "").strip() if isinstance(text, str) else ""
                    text_lower = text.lower()
                    is_watermark = any(kw in text_lower for kw in [
                        "mls", "vmls", "crmls", "nwnw", "listing", "©",
                        "copyright", "real estate", "properties", "fmls",
                    ])
                    if is_watermark:
                        # quad_boxes: [x1,y1,x2,y1,x2,y2,x1,y2]
                        xs = [box[i] for i in range(0, 8, 2)]
                        ys = [box[i] for i in range(1, 8, 2)]
                        boxes.append({
                            "box": [int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))],
                            "label": text,
                            "confidence": 1.0,
                        })

        elif task == "<OD>" and parsed_key:
            od = parsed[parsed_key]
            if "bboxes" in od:
                for box, label in zip(od["bboxes"], od["labels"]):
                    label_lower = label.lower()
                    if "watermark" in label_lower or "text" in label_lower or "logo" in label_lower:
                        x1, y1, x2, y2 = box
                        boxes.append({
                            "box": [int(x1), int(y1), int(x2), int(y2)],
                            "label": label,
                            "confidence": 1.0,
                        })

    # Fallback: try OCR-based detection if Florence-2 finds nothing
    if not boxes:
        boxes = detect_watermarks_ocr(image_path)

    return boxes


def detect_watermarks_ocr(image_path: Path) -> list:
    """Fallback watermark detection using PaddleOCR."""
    try:
        from paddleocr import PaddleOCR
    except ImportError:
        return []

    ocr = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)
    result = ocr.ocr(str(image_path), cls=True)

    boxes = []
    if result and result[0]:
        for line in result[0]:
            box_points = line[0]  # [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
            text = line[1][0].lower()
            conf = line[1][1]

            # Look for MLS-like patterns
            is_watermark = any(kw in text for kw in [
                "mls", "listing", "real estate", "properties",
                "©", "20", "copyright", "watermark",
            ])

            if is_watermark and conf >= 0.5:
                xs = [p[0] for p in box_points]
                ys = [p[1] for p in box_points]
                boxes.append({
                    "box": [int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))],
                    "label": f"ocr:{line[1][0]}",
                    "confidence": float(conf),
                })

    return boxes


def create_mask(boxes: list, image_size: tuple, padding: int = 10):
    """Create a binary mask from bounding boxes."""
    from PIL import Image, ImageDraw

    w, h = image_size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)

    for b in boxes:
        x1, y1, x2, y2 = b["box"]
        x1 = max(0, int(x1) - padding)
        y1 = max(0, int(y1) - padding)
        x2 = min(w, int(x2) + padding)
        y2 = min(h, int(y2) + padding)
        draw.rectangle([x1, y1, x2, y2], fill=255)

    return mask


def inpaint(image_path: Path, mask_path: Path, output_path: Path,
            model: str = "lama", device: Optional[str] = None) -> None:
    """Run IOPaint inpainting."""
    import subprocess

    if device is None:
        try:
            import torch
            device = "cuda" if torch.cuda.is_available() else "cpu"
        except ImportError:
            device = "cpu"

    # Use python -m iopaint to avoid PATH issues
    import sys
    py = sys.executable
    # IOPaint always uses --output as a directory; result is saved as
    # <output_dir>/<input_stem>.png
    out_dir = output_path.parent / f".iopaint_out_{image_path.stem}"
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        py, "-m", "iopaint", "run",
        f"--model={model}",
        f"--device={device}",
        f"--image={image_path}",
        f"--mask={mask_path}",
        f"--output={out_dir}",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"IOPaint error: {result.stderr}")
        sys.exit(1)

    # Move result to desired output path
    iopaint_result = out_dir / f"{image_path.stem}.png"
    if iopaint_result.exists():
        import shutil
        shutil.move(str(iopaint_result), str(output_path))
    shutil.rmtree(out_dir, ignore_errors=True)


def preserve_exif(source: Path, target: Path) -> None:
    """Copy EXIF data from source to target image."""
    try:
        from PIL import Image

        src_img = Image.open(source)
        dst_img = Image.open(target)

        if hasattr(src_img, "_getexif") and src_img._getexif():
            exif = src_img._getexif()
            dst_img.save(target, exif=exif)
    except Exception:
        pass  # EXIF preservation is best-effort


def process_single(input_path: Path, output_path: Path, args) -> dict:
    """Process a single image: detect + inpaint."""
    from PIL import Image

    start = time.time()
    result = {"input": str(input_path), "watermarks_found": 0}

    # Detect
    boxes = detect_watermarks_florence(input_path, args.confidence)
    result["watermarks_found"] = len(boxes)

    if not boxes:
        print(f"  No watermarks detected in {input_path.name}")
        # Copy through unchanged if no watermarks found
        if input_path != output_path:
            import shutil
            shutil.copy2(input_path, output_path)
        return result

    # Create mask
    image = Image.open(input_path)
    mask = create_mask(boxes, image.size, args.padding)

    mask_path = output_path.parent / f"{input_path.stem}_mask.png"
    mask.save(mask_path)

    if args.dry_run:
        print(f"  Found {len(boxes)} watermark(s) in {input_path.name}")
        print(f"  Mask saved to {mask_path}")
        for b in boxes:
            print(f"    [{b['box']}] {b['label']} (conf: {b['confidence']:.2f})")
        return result

    # Inpaint
    inpaint(input_path, mask_path, output_path, args.model, args.device)

    # Preserve EXIF
    if args.preserve_exif:
        preserve_exif(input_path, output_path)

    elapsed = time.time() - start
    print(f"  {input_path.name} -> {output_path.name} ({len(boxes)} watermark(s), {elapsed:.1f}s)")
    return result


def main():
    parser = argparse.ArgumentParser(description="Remove watermarks from images")
    parser.add_argument("--input", required=True, help="Input file or directory")
    parser.add_argument("--output", required=True, help="Output file or directory")
    parser.add_argument("--suffix", default="", help="Output filename suffix (e.g. _clean)")
    parser.add_argument("--detection", default="auto", choices=["auto", "ocr", "none"])
    parser.add_argument("--model", default="lama", help="IOPaint model (lama/mat/migan/ldm)")
    parser.add_argument("--device", default=None, help="cpu/cuda/mps (default: auto)")
    parser.add_argument("--confidence", type=float, default=0.5)
    parser.add_argument("--padding", type=int, default=10, help="Mask padding in pixels")
    parser.add_argument("--preserve-exif", action="store_true", default=True)
    parser.add_argument("--dry-run", action="store_true", help="Detect only, skip inpainting")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if input_path.is_dir():
        output_path.mkdir(parents=True, exist_ok=True)
        files = sorted(f for f in input_path.iterdir() if f.suffix.lower() in IMAGE_EXTENSIONS)
        print(f"Processing {len(files)} images from {input_path}")

        results = []
        for i, f in enumerate(files, 1):
            print(f"[{i}/{len(files)}] {f.name}...")
            out = output_path / (f.stem + args.suffix + f.suffix)
            results.append(process_single(f, out, args))

        detected = sum(r["watermarks_found"] for r in results)
        print(f"\nDone: {len(files)} images, {detected} watermark(s) found")

        # Save results summary
        summary_path = output_path / "removal_results.json"
        with open(summary_path, "w") as fh:
            json.dump(results, fh, indent=2)
        print(f"Results saved to {summary_path}")

    elif input_path.is_file():
        if args.suffix:
            output_path = output_path.parent / (output_path.stem + args.suffix + output_path.suffix)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Processing {input_path.name}...")
        result = process_single(input_path, output_path, args)
        if not args.dry_run:
            print(f"Done: output at {output_path}")
    else:
        print(f"ERROR: Input not found: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
