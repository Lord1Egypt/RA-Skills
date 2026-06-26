#!/usr/bin/env python3
"""
VLM Image Helper - Image preprocessing tool for VLM analysis.

Provides rotation, cropping, scaling, and enhancement operations
to help VLMs better analyze images, especially for OCR tasks.
"""

import argparse
import base64
import binascii
import json
import os
import sys
import tempfile
from io import BytesIO
from typing import Optional

try:
    from PIL import Image, ImageEnhance, ImageOps, UnidentifiedImageError
except ImportError:
    print("Error: Pillow library is required.")
    print("\nInstall with:")
    print("  pip install Pillow")
    print("  # or with uv:")
    print("  uv pip install Pillow")
    sys.exit(1)


def decode_base64_payload(source: str) -> bytes:
    """
    Decode raw base64 or a data URI into bytes.

    Args:
        source: Raw base64 string or data URI

    Returns:
        Decoded bytes
    """
    normalized = source.strip()
    if normalized.startswith("data:image"):
        _, _, normalized = normalized.partition(",")
        if not normalized:
            raise ValueError("Data URI is missing the base64 payload")

    normalized = "".join(normalized.split())
    if not normalized:
        raise ValueError("Base64 payload is empty")

    padding = (-len(normalized)) % 4
    if padding:
        normalized += "=" * padding

    try:
        return base64.b64decode(normalized, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError(f"Invalid base64 payload: {exc}") from exc


def load_decoded_image(source: str, source_kind: str) -> tuple[Image.Image, str]:
    """
    Load an image from decoded bytes.

    Args:
        source: Raw base64 string or data URI
        source_kind: Human-readable source type for error messages

    Returns:
        Tuple of (PIL Image, source kind)
    """
    try:
        image_data = decode_base64_payload(source)
        image = Image.open(BytesIO(image_data))
        image.load()
        return image, source_kind
    except (ValueError, UnidentifiedImageError) as exc:
        raise ValueError(f"Failed to load {source_kind} image: {exc}") from exc


def load_image(source: str, input_mode: str = "auto") -> tuple[Image.Image, str]:
    """
    Load image from file path, base64 string, or data URI.

    Args:
        source: File path, base64 encoded image string, or data URI
        input_mode: auto, path, base64, or data-uri

    Returns:
        Tuple of (PIL Image, source kind)
    """
    normalized = source.strip()

    if input_mode in ("auto", "path"):
        if os.path.exists(normalized):
            return Image.open(normalized), "path"
        if input_mode == "path":
            raise FileNotFoundError(f"Image file not found: {normalized}")

    if input_mode in ("auto", "data-uri") and normalized.startswith("data:image"):
        return load_decoded_image(normalized, "data URI")

    if input_mode in ("auto", "base64"):
        try:
            return load_decoded_image(normalized, "base64")
        except ValueError:
            if input_mode == "base64":
                raise

    raise ValueError(
        "Input is neither an existing file path nor a decodable base64 image. "
        "Use --input-mode to force interpretation."
    )


def rotate_image(img: Image.Image, angle: float) -> Image.Image:
    """
    Rotate image by specified angle.

    Args:
        img: PIL Image object
        angle: Rotation angle in degrees (positive = counter-clockwise)

    Returns:
        Rotated image
    """
    # expand=True ensures the entire rotated image is visible
    return img.rotate(angle, expand=True, resample=Image.BICUBIC)


def crop_image(img: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    """
    Crop image to specified bounding box.

    Args:
        img: PIL Image object
        box: (x1, y1, x2, y2) or (left, top, right, bottom)

    Returns:
        Cropped image
    """
    return img.crop(box)


# Semantic crop presets (percentage-based, no coordinates needed)
CROP_PRESETS = {
    # Quadrants (1/4 of image)
    "top-left":      (0, 0, 50, 50),
    "top-right":     (50, 0, 50, 50),
    "bottom-left":   (0, 50, 50, 50),
    "bottom-right":  (50, 50, 50, 50),
    # Horizontal halves
    "left-half":     (0, 0, 50, 100),
    "right-half":    (50, 0, 50, 100),
    "top-half":      (0, 0, 100, 50),
    "bottom-half":   (0, 50, 100, 50),
    # Center regions
    "center":        (25, 25, 50, 50),      # Center 50%
    "center-wide":   (10, 25, 80, 50),      # Center with more width
    "center-tall":   (25, 10, 50, 80),      # Center with more height
    "center-top":    (25, 0, 50, 50),       # Center top half
    "center-bottom": (25, 50, 50, 50),      # Center bottom half
}

# Semantic scale presets
SCALE_PRESETS = {
    "x2": 2.0,
    "x3": 3.0,
    "x4": 4.0,
}


def crop_by_preset(img: Image.Image, preset: str) -> Image.Image:
    """
    Crop image using a semantic preset name.

    Args:
        img: PIL Image object
        preset: One of: top-left, top-right, bottom-left, bottom-right,
                left-half, right-half, top-half, bottom-half,
                center, center-wide, center-tall, center-top, center-bottom

    Returns:
        Cropped image
    """
    if preset not in CROP_PRESETS:
        available = ", ".join(CROP_PRESETS.keys())
        raise ValueError(f"Unknown preset '{preset}'. Available: {available}")

    x_pct, y_pct, w_pct, h_pct = CROP_PRESETS[preset]
    return crop_percentage(img, x_pct, y_pct, w_pct, h_pct)


def crop_percentage(img: Image.Image, x_pct: float, y_pct: float,
                    width_pct: float, height_pct: float) -> Image.Image:
    """
    Crop image using percentage values.

    Args:
        img: PIL Image object
        x_pct: X offset as percentage (0-100)
        y_pct: Y offset as percentage (0-100)
        width_pct: Width as percentage (0-100)
        height_pct: Height as percentage (0-100)

    Returns:
        Cropped image
    """
    w, h = img.size
    left = int(w * x_pct / 100)
    top = int(h * y_pct / 100)
    right = int(w * (x_pct + width_pct) / 100)
    bottom = int(h * (y_pct + height_pct) / 100)
    return img.crop((left, top, right, bottom))


def scale_image(img: Image.Image, factor: float) -> Image.Image:
    """
    Scale image by specified factor.

    Args:
        img: PIL Image object
        factor: Scale factor (e.g., 2.0 for 2x zoom)

    Returns:
        Scaled image
    """
    if factor <= 0:
        raise ValueError("Scale factor must be positive")

    new_size = (int(img.width * factor), int(img.height * factor))
    return img.resize(new_size, resample=Image.LANCZOS)


def enhance_image(img: Image.Image,
                  brightness: float = 1.0,
                  contrast: float = 1.0,
                  sharpness: float = 1.0) -> Image.Image:
    """
    Enhance image brightness, contrast, and sharpness.

    Args:
        img: PIL Image object
        brightness: Brightness factor (1.0 = original, <1.0 darker, >1.0 brighter)
        contrast: Contrast factor (1.0 = original)
        sharpness: Sharpness factor (1.0 = original, >1.0 sharper)

    Returns:
        Enhanced image
    """
    if brightness != 1.0:
        img = ImageEnhance.Brightness(img).enhance(brightness)
    if contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(contrast)
    if sharpness != 1.0:
        img = ImageEnhance.Sharpness(img).enhance(sharpness)
    return img


def auto_enhance(img: Image.Image) -> Image.Image:
    """
    Apply automatic enhancement for better OCR/analysis.

    Includes auto-contrast and sharpening.
    """
    # Auto-contrast
    img = ImageOps.autocontrast(img, cutoff=2)

    # Mild sharpening
    img = ImageEnhance.Sharpness(img).enhance(1.5)

    return img


def save_image(img: Image.Image,
               output: Optional[str] = None,
               format: str = "PNG",
               return_base64: bool = False) -> str:
    """
    Save image to file or return as base64.

    Args:
        img: PIL Image object
        output: Output file path (if None, creates temp file)
        format: Image format (PNG, JPEG, etc.)
        return_base64: If True, return base64 string instead of file path

    Returns:
        File path or base64 string
    """
    if return_base64:
        from io import BytesIO
        buffer = BytesIO()
        # Convert RGBA to RGB for JPEG
        if format.upper() == "JPEG" and img.mode == "RGBA":
            img = img.convert("RGB")
        img.save(buffer, format=format)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

    if output is None:
        # Create temp file
        suffix = ".png" if format.upper() == "PNG" else f".{format.lower()}"
        fd, output = tempfile.mkstemp(suffix=suffix, prefix="vlm_helper_")
        os.close(fd)

    # Convert RGBA to RGB for JPEG
    if format.upper() == "JPEG" and img.mode == "RGBA":
        img = img.convert("RGB")

    img.save(output, format=format)
    return output


def process_pipeline(source: str,
                     operations: list[dict],
                     output: Optional[str] = None,
                     return_base64: bool = False,
                     format: str = "PNG",
                     input_mode: str = "auto") -> str:
    """
    Process image through a pipeline of operations.

    Args:
        source: Input image (file path or base64)
        operations: List of operation dicts with 'op' and parameters
        output: Output file path
        return_base64: Return base64 instead of file path
        format: Output image format

    Returns:
        File path or base64 string
    """
    img, _ = load_image(source, input_mode=input_mode)

    for op in operations:
        op_type = op.get('op', op.get('type', '')).lower()

        if op_type == 'rotate':
            angle = op.get('angle', 0)
            img = rotate_image(img, angle)

        elif op_type == 'crop':
            # Check for preset first
            if 'preset' in op:
                img = crop_by_preset(img, op['preset'])
            elif all(k in op for k in ['x_pct', 'y_pct', 'width_pct', 'height_pct']):
                img = crop_percentage(img, op['x_pct'], op['y_pct'],
                                     op['width_pct'], op['height_pct'])
            elif all(k in op for k in ['x1', 'y1', 'x2', 'y2']):
                img = crop_image(img, (op['x1'], op['y1'], op['x2'], op['y2']))
            elif all(k in op for k in ['left', 'top', 'right', 'bottom']):
                img = crop_image(img, (op['left'], op['top'], op['right'], op['bottom']))
            else:
                raise ValueError("Crop requires (x1,y1,x2,y2) or (x_pct,y_pct,width_pct,height_pct)")

        elif op_type == 'scale':
            factor = op.get('factor', 1.0)
            img = scale_image(img, factor)

        elif op_type == 'enhance':
            brightness = op.get('brightness', 1.0)
            contrast = op.get('contrast', 1.0)
            sharpness = op.get('sharpness', 1.0)
            img = enhance_image(img, brightness, contrast, sharpness)

        elif op_type == 'auto_enhance':
            img = auto_enhance(img)

        else:
            print(f"Warning: Unknown operation '{op_type}', skipping", file=sys.stderr)

    return save_image(img, output, format, return_base64)


def main():
    parser = argparse.ArgumentParser(
        description='VLM Image Helper - Preprocess images for better VLM analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Pass a file through unchanged and return base64
  %(prog)s input.png --base64

  # Crop by semantic preset (recommended - no coordinates needed!)
  %(prog)s input.png --crop-preset top-left -o cropped.png
  %(prog)s input.png --crop-preset center -o cropped.png

  # Scale by preset or factor
  %(prog)s input.png --scale-preset x2 -o scaled.png
  %(prog)s input.png --scale 1.5 -o scaled.png

  # Combine: crop center and zoom 2x
  %(prog)s input.png --crop-preset center --scale-preset x2 -o detail.png

  # Rotate image
  %(prog)s input.png --rotate 45 -o rotated.png

  # Crop region (coordinates - if you know them)
  %(prog)s input.png --crop 100,100,500,400 -o cropped.png

  # Enhance for OCR
  %(prog)s input.png --auto-enhance -o enhanced.png

  # Chain multiple operations
  %(prog)s input.png --rotate 90 --crop-preset center --scale-preset x2 -o output.png

  # Output as base64
  %(prog)s input.png --crop-preset center --scale-preset x2 --base64

  # Force raw base64 input
  %(prog)s "<base64>" --input-mode base64 --crop-preset center --base64

Crop presets: top-left, top-right, bottom-left, bottom-right,
              left-half, right-half, top-half, bottom-half,
              center, center-wide, center-tall, center-top, center-bottom

Scale presets: x2, x3, x4 (or use --scale with any number)
"""
    )

    parser.add_argument('input', help='Input image file path or base64 string')
    parser.add_argument(
        '--input-mode',
        choices=['auto', 'path', 'base64', 'data-uri'],
        default='auto',
        help='How to interpret the input (default: auto-detect path or base64)'
    )

    # Output options
    parser.add_argument('-o', '--output', help='Output file path (default: temp file)')
    parser.add_argument('--format', default='PNG', help='Output format (PNG, JPEG, etc.)')
    parser.add_argument('--base64', action='store_true', help='Output as base64 string')

    # Rotate operation
    parser.add_argument('--rotate', type=float, metavar='ANGLE',
                       help='Rotate image by angle in degrees')

    # Crop options (mutually exclusive)
    crop_group = parser.add_mutually_exclusive_group()
    crop_group.add_argument('--crop-preset', metavar='NAME',
                           help='Crop by preset name (top-left, center, etc.)')
    crop_group.add_argument('--crop', metavar='X1,Y1,X2,Y2',
                           help='Crop by coordinates (left,top,right,bottom)')
    crop_group.add_argument('--crop-pct', metavar='X,Y,W,H',
                           help='Crop by percentage (x_offset,y_offset,width,height)')

    # Scale options (mutually exclusive)
    scale_group = parser.add_mutually_exclusive_group()
    scale_group.add_argument('--scale-preset', metavar='NAME',
                            help='Scale by preset (x2, x3, x4)')
    scale_group.add_argument('--scale', type=float, metavar='FACTOR',
                            help='Scale by factor (e.g., 2 for 2x)')

    # Enhancement options
    parser.add_argument('--brightness', type=float, help='Brightness factor (1.0=original)')
    parser.add_argument('--contrast', type=float, help='Contrast factor (1.0=original)')
    parser.add_argument('--sharpness', type=float, help='Sharpness factor (1.0=original)')
    parser.add_argument('--auto-enhance', action='store_true',
                       help='Apply auto-enhancement for OCR')

    # Pipeline option
    parser.add_argument('--pipeline', metavar='JSON',
                       help='JSON string with array of operations')

    args = parser.parse_args()

    # Build operations list
    operations = []

    # From pipeline JSON
    if args.pipeline:
        try:
            operations.extend(json.loads(args.pipeline))
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in pipeline: {e}", file=sys.stderr)
            sys.exit(1)

    # From individual arguments
    if args.rotate is not None:
        operations.append({'op': 'rotate', 'angle': args.rotate})

    if args.crop_preset:
        operations.append({'op': 'crop', 'preset': args.crop_preset})

    if args.crop:
        try:
            coords = [int(x.strip()) for x in args.crop.split(',')]
            if len(coords) != 4:
                raise ValueError("Need 4 coordinates")
            operations.append({'op': 'crop', 'x1': coords[0], 'y1': coords[1],
                             'x2': coords[2], 'y2': coords[3]})
        except ValueError as e:
            print(f"Error: Invalid crop coordinates: {e}", file=sys.stderr)
            sys.exit(1)

    if args.crop_pct:
        try:
            vals = [float(x.strip()) for x in args.crop_pct.split(',')]
            if len(vals) != 4:
                raise ValueError("Need 4 values")
            operations.append({'op': 'crop', 'x_pct': vals[0], 'y_pct': vals[1],
                             'width_pct': vals[2], 'height_pct': vals[3]})
        except ValueError as e:
            print(f"Error: Invalid crop percentage: {e}", file=sys.stderr)
            sys.exit(1)

    if args.scale_preset:
        if args.scale_preset not in SCALE_PRESETS:
            available = ", ".join(SCALE_PRESETS.keys())
            print(f"Error: Unknown scale preset '{args.scale_preset}'. Available: {available}", file=sys.stderr)
            sys.exit(1)
        operations.append({'op': 'scale', 'factor': SCALE_PRESETS[args.scale_preset]})

    if args.scale is not None:
        operations.append({'op': 'scale', 'factor': args.scale})

    # Enhancement
    if args.auto_enhance:
        operations.append({'op': 'auto_enhance'})
    elif any([args.brightness, args.contrast, args.sharpness]):
        operations.append({
            'op': 'enhance',
            'brightness': args.brightness or 1.0,
            'contrast': args.contrast or 1.0,
            'sharpness': args.sharpness or 1.0
        })

    # Allow passthrough output so a file path can be converted directly to base64.
    wants_passthrough_output = args.base64 or args.output or args.format.upper() != 'PNG'
    if not operations and not wants_passthrough_output:
        print(
            "Error: No operations specified. Add an operation or request passthrough output "
            "with --base64 or -o/--output.",
            file=sys.stderr
        )
        sys.exit(1)

    # Process
    try:
        result = process_pipeline(
            source=args.input,
            operations=operations,
            output=args.output,
            return_base64=args.base64,
            format=args.format,
            input_mode=args.input_mode
        )
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
