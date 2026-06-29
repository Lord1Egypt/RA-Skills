#!/home/guoxh/.openclaw/venv-clawd/bin/python
"""
OpenCV inpainting script for photo restoration
Removes: wires, spots, scratches, lines, rectangular regions
Supports: single operation, batch operation, multiple spots/lines
"""
import cv2
import numpy as np
import argparse
import os
import sys
import json

# EXIF preservation
try:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
    from exif_utils import ExifPreserver
    def _preserve_exif(src: str, dst: str):
        """Copy EXIF metadata from src to dst if possible."""
        try:
            p = ExifPreserver(src)
            if p.has_exif():
                p.apply_to_file(dst)
        except Exception:
            pass
    EXIF_AVAILABLE = True
except ImportError:
    def _preserve_exif(src, dst):
        pass
    EXIF_AVAILABLE = False


def inpaint_wire(image_path, output_path, y_pos, thickness=10, algorithm='ns'):
    """Remove horizontal wire from image"""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    h, w = img.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.line(mask, (0, y_pos), (w, y_pos), 255, thickness)

    algo = cv2.INPAINT_NS if algorithm == 'ns' else cv2.INPAINT_TELEA
    result = cv2.inpaint(img, mask, 5, algo)
    cv2.imwrite(output_path, result)
    _preserve_exif(image_path, output_path)
    return True


def inpaint_spot(image_path, output_path, x, y, radius=8, algorithm='telea'):
    """Remove circular spot/sensor dust"""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.circle(mask, (x, y), radius, 255, -1)

    algo = cv2.INPAINT_TELEA if algorithm == 'telea' else cv2.INPAINT_NS
    result = cv2.inpaint(img, mask, 5, algo)
    cv2.imwrite(output_path, result)
    _preserve_exif(image_path, output_path)
    return True


def inpaint_line(image_path, output_path, x1, y1, x2, y2, thickness=3, algorithm='ns'):
    """Remove line segment between two points (supports diagonal/angled lines)"""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    h, w = img.shape[:2]

    # Clip coordinates to image bounds
    x1, y1 = max(0, min(x1, w-1)), max(0, min(y1, h-1))
    x2, y2 = max(0, min(x2, w-1)), max(0, min(y2, h-1))

    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.line(mask, (x1, y1), (x2, y2), 255, thickness)

    algo = cv2.INPAINT_NS if algorithm == 'ns' else cv2.INPAINT_TELEA
    result = cv2.inpaint(img, mask, 5, algo)
    cv2.imwrite(output_path, result)
    _preserve_exif(image_path, output_path)
    return True


def inpaint_rect(image_path, output_path, x, y, w, h, feather=5, algorithm='ns'):
    """Remove rectangular region (watermarks, logos, text areas)"""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    img_h, img_w = img.shape[:2]

    # Clip rectangle to image bounds
    x, y = max(0, min(x, img_w-1)), max(0, min(y, img_h-1))
    x2, y2 = min(x + w, img_w), min(y + h, img_h)
    w, h = x2 - x, y2 - y

    if w <= 0 or h <= 0:
        raise ValueError(f"Invalid rectangle: width={w}, height={h}")

    # Create mask with optional feathering (soft edges for better blending)
    mask = np.zeros((img_h, img_w), dtype=np.uint8)
    if feather > 0:
        # Draw rectangle with gradient edges
        mask = cv2.rectangle(mask, (x, y), (x2, y2), 255, -1)
        # Apply Gaussian blur for feathered edges
        kernel_size = feather * 4 + 1
        mask = cv2.GaussianBlur(mask, (kernel_size, kernel_size), 0)
        # Normalize to 0-255 range
        mask = np.clip(mask, 0, 255).astype(np.uint8)
    else:
        cv2.rectangle(mask, (x, y), (x2, y2), 255, -1)

    algo = cv2.INPAINT_NS if algorithm == 'ns' else cv2.INPAINT_TELEA
    result = cv2.inpaint(img, mask, 5, algo)
    cv2.imwrite(output_path, result)
    _preserve_exif(image_path, output_path)
    return True


def inpaint_batch(image_path, output_path, operations, default_algo='ns'):
    """
    Process multiple inpainting operations in a single pass (efficient)
    operations: list of dicts with 'type' and corresponding parameters
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    img_h, img_w = img.shape[:2]
    mask = np.zeros((img_h, img_w), dtype=np.uint8)

    # Build combined mask
    for op in operations:
        op_type = op.get('type')
        algo = op.get('algo', default_algo)

        if op_type == 'wire':
            y = op.get('y')
            thickness = op.get('thickness', 3)
            cv2.line(mask, (0, y), (img_w, y), 255, thickness)

        elif op_type == 'line':
            x1, y1 = op.get('x1'), op.get('y1')
            x2, y2 = op.get('x2'), op.get('y2')
            thickness = op.get('thickness', 3)
            # Clip coordinates
            x1, y1 = max(0, min(x1, img_w-1)), max(0, min(y1, img_h-1))
            x2, y2 = max(0, min(x2, img_w-1)), max(0, min(y2, img_h-1))
            cv2.line(mask, (x1, y1), (x2, y2), 255, thickness)

        elif op_type == 'spot':
            x, y = op.get('x'), op.get('y')
            radius = op.get('radius', 8)
            cv2.circle(mask, (x, y), radius, 255, -1)

        elif op_type == 'rect':
            x, y = op.get('x'), op.get('y')
            w, h = op.get('w'), op.get('h')
            feather = op.get('feather', 5)

            # Clip rectangle
            x, y = max(0, min(x, img_w-1)), max(0, min(y, img_h-1))
            x2, y2 = min(x + w, img_w), min(y + h, img_h)
            w, h = x2 - x, y2 - y

            if w > 0 and h > 0:
                if feather > 0:
                    temp_mask = np.zeros((img_h, img_w), dtype=np.uint8)
                    cv2.rectangle(temp_mask, (x, y), (x2, y2), 255, -1)
                    temp_mask = cv2.GaussianBlur(temp_mask, (feather*4+1, feather*4+1), 0)
                    mask = np.maximum(mask, temp_mask)
                else:
                    cv2.rectangle(mask, (x, y), (x2, y2), 255, -1)

    # Use Telea for mixed operations (usually faster for multiple regions)
    # Use NS for wires/lines (better for texture)
    algo = cv2.INPAINT_NS if 'wire' in [o.get('type') for o in operations] else cv2.INPAINT_TELEA

    result = cv2.inpaint(img, mask, 5, algo)
    cv2.imwrite(output_path, result)
    _preserve_exif(image_path, output_path)
    return True


def resize_for_api(image_path, output_path, max_dim=2048):
    """Resize image to fit within API limits while preserving aspect ratio"""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    h, w = img.shape[:2]

    if max(h, w) <= max_dim:
        cv2.imwrite(output_path, img)
        _preserve_exif(image_path, output_path)
        return False  # No resize needed

    # Calculate new dimensions
    if h > w:
        new_h = max_dim
        new_w = int(w * max_dim / h)
    else:
        new_w = max_dim
        new_h = int(h * max_dim / w)

    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    cv2.imwrite(output_path, resized)
    _preserve_exif(image_path, output_path)
    return True


def denoise_op(image_path, output_path, strength=10):
    """
    Reduce image noise using FastNlMeansDenoisingColored.
    strength: 1-30 (higher = more denoising, default 10)
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    strength = max(1, min(30, int(strength)))
    result = cv2.fastNlMeansDenoisingColored(img, None, strength, strength, 7, 21)
    cv2.imwrite(output_path, result)
    _preserve_exif(image_path, output_path)
    return True


def sharpen_op(image_path, output_path, strength=1.0):
    """
    Sharpen image using unsharp masking.
    strength: 0.5-3.0 (higher = more sharpening, default 1.0)
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    strength = max(0.5, min(3.0, float(strength)))

    # Build sharpening kernel from identity kernel
    # identity + (sharp - identity) * strength
    sharp_kernel = np.array([
        [-1, -1, -1],
        [-1,  9, -1],
        [-1, -1, -1]
    ])
    identity = np.array([
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ])
    kernel = identity + (sharp_kernel - identity) * strength

    result = cv2.filter2D(img, -1, kernel)
    cv2.imwrite(output_path, result)
    _preserve_exif(image_path, output_path)
    return True


def adjust_op(image_path, output_path, brightness=0, contrast=0, gamma=1.0):
    """
    Apply brightness, contrast, and gamma adjustment to image.
    brightness: -100 to 100 (pixel offset)
    contrast: -100 to 100 (factor)
    gamma: 0.1 to 3.0 (gamma curve)
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    # Clamp values
    brightness = max(-100, min(100, float(brightness)))
    contrast   = max(-100, min(100, float(contrast)))
    gamma      = max(0.1, min(3.0, float(gamma)))

    result = img.astype(np.float32)

    # Brightness: add offset
    if brightness != 0:
        result = result + (brightness * 2.55)

    # Contrast: adjust around midpoint (128)
    if contrast != 0:
        factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
        result = factor * (result - 128) + 128

    # Gamma correction
    if gamma != 1.0:
        # Build gamma LUT
        lut = np.array([
            int(((i / 255.0) ** (1.0 / gamma)) * 255)
            for i in range(256)
        ], dtype=np.uint8)
        result = lut[np.clip(result, 0, 255).astype(np.uint8)]
    else:
        result = np.clip(result, 0, 255)

    result = result.astype(np.uint8)
    cv2.imwrite(output_path, result)
    _preserve_exif(image_path, output_path)
    return True


def parse_multi_spots(spots_str):
    """Parse multiple spots from command line: x1,y1,r1;x2,y2,r2;..."""
    spots = []
    if not spots_str:
        return spots
    for part in spots_str.split(';'):
        parts = part.strip().split(',')
        if len(parts) >= 2:
            x, y = int(parts[0]), int(parts[1])
            radius = int(parts[2]) if len(parts) >= 3 else 8
            spots.append({'x': x, 'y': y, 'radius': radius})
    return spots


def parse_multi_lines(lines_str):
    """Parse multiple lines from command line: x1,y1,x2,y2;x1,y1,x2,y2;..."""
    lines = []
    if not lines_str:
        return lines
    for part in lines_str.split(';'):
        parts = part.strip().split(',')
        if len(parts) >= 4:
            x1, y1, x2, y2 = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
            thickness = int(parts[4]) if len(parts) >= 5 else 3
            lines.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'thickness': thickness})
    return lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="OpenCV inpainting for photo restoration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single operations
  %(prog)s input.jpg output.jpg --type wire --y 760 --thickness 12
  %(prog)s input.jpg output.jpg --type spot --x 70 --y 155 --radius 8
  %(prog)s input.jpg output.jpg --type line --x1 100 --y1 200 --x2 500 --y2 400
  %(prog)s input.jpg output.jpg --type rect --x 50 --y 50 --w 300 --h 100

  # Multiple spots in one command
  %(prog)s input.jpg output.jpg --type spots --spots "100,150,8;200,300,10;50,400,6"

  # Multiple lines in one command
  %(prog)s input.jpg output.jpg --type lines --lines "0,100,800,100,3;100,200,500,400,5"

  # Batch processing from JSON file
  %(prog)s input.jpg output.jpg --type batch --batch tasks.json

  # Denoise (reduce noise in low-light photos)
  %(prog)s input.jpg output.jpg --type denoise --strength 15

  # Sharpen (enhance edges and focus)
  %(prog)s input.jpg output.jpg --type sharpen --strength 1.5

  # Brightness/contrast/gamma adjustment
  %(prog)s input.jpg output.jpg --type adjust --brightness 15 --contrast 10 --gamma 0.9

  # JSON format example (tasks.json):
  # {
  #   "operations": [
  #     {"type": "spot", "x": 100, "y": 150, "radius": 8},
  #     {"type": "wire", "y": 500, "thickness": 5},
  #     {"type": "denoise", "strength": 10}
  #   ]
  # }

Algorithms:
  ns     - Navier-Stokes (better for textures, default for wire/line)
  telea  - Telea (faster, better for small regions, default for spot)
"""
    )

    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path")
    parser.add_argument("--type",
                        choices=["wire", "spot", "line", "rect", "resize",
                                 "spots", "lines", "batch", "denoise", "sharpen", "adjust"],
                        required=True,
                        help="Operation type (spots=multiple spots, lines=multiple lines, batch=JSON config)")

    # Wire parameters
    parser.add_argument("--y", type=int, help="Y position for horizontal wire")

    # Line parameters
    parser.add_argument("--x1", type=int, help="Start X for line segment")
    parser.add_argument("--y1", type=int, help="Start Y for line segment")
    parser.add_argument("--x2", type=int, help="End X for line segment")
    parser.add_argument("--y2", type=int, help="End Y for line segment")

    # Spot parameters
    parser.add_argument("--x", type=int, help="X position for spot center")
    parser.add_argument("--spots", type=str, help="Multiple spots: x1,y1,r1;x2,y2,r2;... (radius optional)")

    # Lines parameters
    parser.add_argument("--lines", type=str, help="Multiple lines: x1,y1,x2,y2,t;x1,y1,x2,y2,t;... (thickness optional)")

    # Rectangle parameters
    parser.add_argument("--w", type=int, help="Width for rectangle region")
    parser.add_argument("--h", type=int, help="Height for rectangle region")

    # Batch parameters
    parser.add_argument("--batch", type=str, help="Path to JSON config file for batch processing")

    # Common parameters
    parser.add_argument("--thickness", type=int, default=3, help="Line/wire thickness (default: 3)")
    parser.add_argument("--radius", type=int, default=8, help="Spot radius (default: 8)")
    parser.add_argument("--feather", type=int, default=5, help="Edge feathering for rect (default: 5, 0=sharp)")
    parser.add_argument("--max-dim", type=int, default=2048, help="Max dimension for resize (default: 2048)")
    parser.add_argument("--algo", choices=["ns", "telea"], default=None,
                        help="Inpainting algorithm (auto-selected by default)")

    # Denoise / Sharpen / Adjust parameters
    parser.add_argument("--strength", type=float, default=10,
                        help="Strength for denoise/sharpen (denoise: 1-30, sharpen: 0.5-3.0)")
    parser.add_argument("--brightness", type=float, default=0,
                        help="Brightness adjustment for adjust (-100 to 100)")
    parser.add_argument("--contrast", type=float, default=0,
                        help="Contrast adjustment for adjust (-100 to 100)")
    parser.add_argument("--gamma", type=float, default=1.0,
                        help="Gamma correction for adjust (0.1-3.0, 1.0=no change)")

    args = parser.parse_args()

    # Create output directory if needed
    out_dir = os.path.dirname(args.output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)

    try:
        # Handle batch processing from JSON file
        if args.type == "batch":
            if not args.batch:
                print("Error: --batch <file.json> is required for batch type", file=sys.stderr)
                sys.exit(1)

            if not os.path.exists(args.batch):
                print(f"Error: Batch file not found: {args.batch}", file=sys.stderr)
                sys.exit(1)

            with open(args.batch, 'r') as f:
                config = json.load(f)

            operations = config.get('operations', [])
            if not operations:
                print("Error: No operations found in batch file", file=sys.stderr)
                sys.exit(1)

            algo = args.algo if args.algo else 'ns'
            inpaint_batch(args.input, args.output, operations, algo)
            print(f"✓ Batch processing completed ({len(operations)} operations): {args.output}")

        # Handle multiple spots in one command
        elif args.type == "spots":
            spots = parse_multi_spots(args.spots)
            if not spots:
                print("Error: --spots is required for spots type (format: x,y,r;x,y,r;...)", file=sys.stderr)
                sys.exit(1)

            operations = []
            for spot in spots:
                operations.append({
                    'type': 'spot',
                    'x': spot['x'],
                    'y': spot['y'],
                    'radius': spot['radius']
                })

            algo = args.algo if args.algo else 'telea'
            inpaint_batch(args.input, args.output, operations, algo)
            print(f"✓ {len(spots)} spots removed: {args.output}")

        # Handle multiple lines in one command
        elif args.type == "lines":
            lines = parse_multi_lines(args.lines)
            if not lines:
                print("Error: --lines is required for lines type (format: x1,y1,x2,y2,t;...)", file=sys.stderr)
                sys.exit(1)

            operations = []
            for line in lines:
                operations.append({
                    'type': 'line',
                    'x1': line['x1'],
                    'y1': line['y1'],
                    'x2': line['x2'],
                    'y2': line['y2'],
                    'thickness': line['thickness']
                })

            algo = args.algo if args.algo else 'ns'
            inpaint_batch(args.input, args.output, operations, algo)
            print(f"✓ {len(lines)} lines removed: {args.output}")

        # Single operations
        elif args.type == "wire":
            if args.y is None:
                print("Error: --y is required for wire type", file=sys.stderr)
                sys.exit(1)
            inpaint_wire(args.input, args.output, args.y, args.thickness, args.algo or 'ns')
            print(f"✓ Wire removed at Y={args.y}, thickness={args.thickness}: {args.output}")

        elif args.type == "line":
            if None in [args.x1, args.y1, args.x2, args.y2]:
                print("Error: --x1, --y1, --x2, --y2 are all required for line type", file=sys.stderr)
                sys.exit(1)
            inpaint_line(args.input, args.output, args.x1, args.y1, args.x2, args.y2, args.thickness, args.algo or 'ns')
            print(f"✓ Line removed from ({args.x1},{args.y1}) to ({args.x2},{args.y2}): {args.output}")

        elif args.type == "spot":
            if args.x is None or args.y is None:
                print("Error: --x and --y are required for spot type", file=sys.stderr)
                sys.exit(1)
            inpaint_spot(args.input, args.output, args.x, args.y, args.radius, args.algo or 'telea')
            print(f"✓ Spot removed at ({args.x},{args.y}), radius={args.radius}: {args.output}")

        elif args.type == "rect":
            if None in [args.x, args.y, args.w, args.h]:
                print("Error: --x, --y, --w, --h are all required for rect type", file=sys.stderr)
                sys.exit(1)
            inpaint_rect(args.input, args.output, args.x, args.y, args.w, args.h, args.feather, args.algo or 'ns')
            print(f"✓ Rectangle removed at ({args.x},{args.y}) size={args.w}x{args.h}, feather={args.feather}: {args.output}")

        elif args.type == "resize":
            resized = resize_for_api(args.input, args.output, args.max_dim)
            if resized:
                print(f"✓ Image resized to <={args.max_dim}px: {args.output}")
            else:
                print(f"✓ Image already within limits: {args.output}")

        elif args.type == "denoise":
            denoise_op(args.input, args.output, args.strength)
            print(f"✓ Denoised (strength={args.strength}): {args.output}")

        elif args.type == "sharpen":
            sharpen_op(args.input, args.output, args.strength)
            print(f"✓ Sharpened (strength={args.strength}): {args.output}")

        elif args.type == "adjust":
            adjust_op(args.input, args.output,
                     brightness=args.brightness,
                     contrast=args.contrast,
                     gamma=args.gamma)
            print(f"✓ Adjusted (b={args.brightness}, c={args.contrast}, g={args.gamma}): {args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
