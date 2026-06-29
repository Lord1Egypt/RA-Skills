#!/home/guoxh/.openclaw/venv-clawd/bin/python
"""
Smart Crop Tool - Automatic intelligent cropping

Crops images to the most "interesting" region using saliency detection.
Supports: aspect ratio constraints, padding/margin control, and multiple
saliency algorithms.

Usage:
    ./smart_crop.py input.jpg output.jpg
    ./smart_crop.py input.jpg output.jpg --width 800 --height 600   # Fixed aspect ratio
    ./smart_crop.py input.jpg output.jpg --padding 0.1              # 10%% margin around subject
    ./smart_crop.py input.jpg output.jpg --algorithm spectral         # Force specific algorithm
    ./smart_crop.py input.jpg output.jpg --debug                    # Show saliency map overlay
"""
import argparse
import os
import sys
import json
import time
import numpy as np
import cv2

# EXIF preservation
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from exif_utils import ExifPreserver
    EXIF_PRESERVER = ExifPreserver
except ImportError:
    EXIF_PRESERVER = None


# ─────────────────────────────────────────────────────────────────
# Saliency detection
# ─────────────────────────────────────────────────────────────────

def detect_saliency_map(img: np.ndarray, algorithm: str = "finegrained") -> np.ndarray:
    """
    Compute saliency map for an image.
    
    Args:
        img: BGR image
        algorithm: "finegrained" | "spectral" | "edge"
    
    Returns:
        Saliency map as float32 image (0-1 range)
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if algorithm == "finegrained":
        # StaticSaliencyFineGrained - more precise, pixel-level
        try:
            saliency = cv2.saliency.StaticSaliencyFineGrained_create()
            success, saliency_map = saliency.computeSaliency(img)
            if success:
                return saliency_map.astype(np.float32)
        except Exception:
            pass
    
    if algorithm in ("finegrained", "spectral"):
        # StaticSaliencySpectralResidual - faster, good for most cases
        try:
            saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
            success, saliency_map = saliency.computeSaliency(img)
            if success:
                return saliency_map.astype(np.float32)
        except Exception:
            pass
    
    # Fallback: Edge/contrast-based saliency
    # Uses gradient magnitude as proxy for interesting content
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    grad_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    gradient_mag = np.sqrt(grad_x**2 + grad_y**2)
    
    # Normalize to 0-1
    saliency_map = gradient_mag.astype(np.float32)
    if saliency_map.max() > 0:
        saliency_map = saliency_map / saliency_map.max()
    
    # Blur to smooth
    saliency_map = cv2.GaussianBlur(saliency_map, (15, 15), 0)
    if saliency_map.max() > 0:
        saliency_map = saliency_map / saliency_map.max()
    
    return saliency_map


def saliency_map_to_bbox(saliency_map: np.ndarray,
                          threshold: float = 0.3,
                          min_area_ratio: float = 0.01,
                          max_area_ratio: float = 0.95) -> tuple:
    """
    Convert saliency map to a bounding box of the most salient region.
    
    Args:
        saliency_map: float32 saliency map (0-1)
        threshold: binarization threshold (fraction of max)
        min_area_ratio: min bounding box area as fraction of image
        max_area_ratio: max bounding box area as fraction of image
    
    Returns:
        (x, y, w, h) bounding box, or None if no good region found
    """
    h, w = saliency_map.shape
    
    # Binarize saliency map
    thresh_val = saliency_map.max() * threshold
    _, binary = cv2.threshold(
        (saliency_map * 255).astype(np.uint8),
        int(thresh_val * 255), 255,
        cv2.THRESH_BINARY
    )
    
    # Clean up with morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None
    
    min_area = (w * h) * min_area_ratio
    max_area = (w * h) * max_area_ratio
    
    # Filter by area and find the most salient (highest mean saliency)
    candidates = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area or area > max_area:
            continue
        
        x, y, cw, ch = cv2.boundingRect(cnt)
        
        # Score: mean saliency within the bounding box
        roi = saliency_map[y:y+ch, x:x+cw]
        score = roi.mean()
        
        candidates.append((score, x, y, cw, ch, area))
    
    if not candidates:
        # Fallback: use the top-k most salient pixels as center
        flat = saliency_map.flatten()
        top_k = int(len(flat) * 0.05)  # Top 5%
        cutoff = np.partition(flat, -top_k)[-top_k]
        
        # Find centroid of top salient pixels
        mask = (saliency_map >= cutoff).astype(np.uint8) * 255
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Find largest contour
            largest = max(contours, key=cv2.contourArea)
            x, y, cw, ch = cv2.boundingRect(largest)
            
            # Verify area constraints
            area = cw * ch
            if area >= min_area and area <= max_area:
                candidates.append((saliency_map[y:y+ch, x:x+cw].mean(), x, y, cw, ch, area))
    
    if not candidates:
        return None
    
    # Return the highest-scoring bounding box
    best = max(candidates, key=lambda c: c[0])
    return (best[1], best[2], best[3], best[4])


def refine_bbox_with_grabcut(img: np.ndarray, bbox: tuple,
                              iterations: int = 3) -> tuple:
    """
    Refine bounding box using GrabCut segmentation.
    
    Args:
        img: BGR image
        bbox: initial (x, y, w, h)
        iterations: GrabCut iterations
    
    Returns:
        Refined (x, y, w, h)
    """
    x, y, w, h = bbox
    
    # Ensure bbox is valid
    h_img, w_img = img.shape[:2]
    x, y = max(0, x), max(0, y)
    w = min(w, w_img - x)
    h = min(h, h_img - y)
    
    if w <= 5 or h <= 5:
        return bbox
    
    # GrabCut needs at least some foreground
    rect = (x, y, w, h)
    
    # Create mask
    mask = np.zeros(img.shape[:2], np.uint8)
    
    # Models
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    
    try:
        cv2.grabCut(img, mask, rect, bgd_model, fgd_model, iterations,
                   cv2.GC_INIT_WITH_RECT)
        
        # Create binary mask from GrabCut result
        # 0 = definite background, 1 = definite foreground
        # 2 = probable background, 3 = probable foreground
        grabcut_mask = np.where((mask == 2) | (mask == 0), 0, 1).astype(np.uint8)
        
        # Find bounding box of foreground
        contours, _ = cv2.findContours(grabcut_mask, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest = max(contours, key=cv2.contourArea)
            x2, y2, w2, h2 = cv2.boundingRect(largest)
            
            # Only refine if it makes sense (not too far from original)
            area_ratio = (w2 * h2) / (w * h)
            if 0.3 <= area_ratio <= 2.0:
                return (x2, y2, w2, h2)
    except Exception:
        pass
    
    return bbox


def smart_crop(img: np.ndarray,
               target_width: int = None,
               target_height: int = None,
               aspect_ratio: float = None,
               padding: float = 0.05,
               algorithm: str = "auto",
               refine_with_grabcut: bool = False,
               threshold: float = 0.3) -> np.ndarray:
    """
    Smart crop: find the most salient region and crop to it.
    
    Args:
        img: Input BGR image
        target_width: Desired output width (None = auto)
        target_height: Desired output height (None = auto)
        aspect_ratio: Force aspect ratio (w/h, e.g. 16/9)
        padding: Margin around subject (fraction, 0.0-0.3)
        algorithm: "auto" | "finegrained" | "spectral" | "edge"
        refine_with_grabcut: Use GrabCut to refine crop boundary
        threshold: Saliency threshold (0.1-0.8)
    
    Returns:
        Cropped image (or original if no good region found)
    """
    h_img, w_img = img.shape[:2]
    
    # Determine effective crop region
    if aspect_ratio:
        # Fit aspect ratio within image bounds
        img_aspect = w_img / h_img
        
        if aspect_ratio > img_aspect:
            # Target is wider than image: fit to width
            crop_w = w_img
            crop_h = int(w_img / aspect_ratio)
        else:
            # Target is taller than image: fit to height
            crop_h = h_img
            crop_w = int(h_img * aspect_ratio)
    elif target_width and target_height:
        crop_w, crop_h = target_width, target_height
    else:
        # No constraints: use saliency to find natural crop
        crop_w, crop_h = None, None
    
    # Compute saliency map
    algo = "finegrained" if algorithm == "auto" else algorithm
    saliency_map = detect_saliency_map(img, algorithm=algo)
    
    # Get bounding box of most salient region
    raw_bbox = saliency_map_to_bbox(saliency_map, threshold=threshold)
    
    if raw_bbox is None:
        # No salient region found: return original
        return img.copy()
    
    x_sal, y_sal, w_sal, h_sal = raw_bbox
    
    # Determine crop dimensions
    if crop_w and crop_h:
        # Use requested dimensions (aspect ratio mode)
        crop_w = min(crop_w, w_img)
        crop_h = min(crop_h, h_img)
        
        # Center the requested crop on the salient region
        center_x = x_sal + w_sal // 2
        center_y = y_sal + h_sal // 2
        
        x_crop = max(0, center_x - crop_w // 2)
        y_crop = max(0, center_y - crop_h // 2)
        
        # Clamp to image bounds
        x_crop = min(x_crop, w_img - crop_w)
        y_crop = min(y_crop, h_img - crop_h)
        
        crop_box = (x_crop, y_crop, crop_w, crop_h)
    else:
        # No target size: crop tightly around salient region + padding
        pad_w = int(w_sal * padding)
        pad_h = int(h_sal * padding)
        
        x_crop = max(0, x_sal - pad_w)
        y_crop = max(0, y_sal - pad_h)
        crop_w = min(w_img - x_crop, w_sal + 2 * pad_w)
        crop_h = min(h_img - y_crop, h_sal + 2 * pad_h)
        
        crop_box = (x_crop, y_crop, crop_w, crop_h)
    
    # Optionally refine with GrabCut
    if refine_with_grabcut:
        crop_box = refine_bbox_with_grabcut(img, crop_box)
    
    x, y, w, h = crop_box
    
    # Final clamp
    x, y = max(0, x), max(0, y)
    w = min(w, w_img - x)
    h = min(h, h_img - y)
    
    cropped = img[y:y+h, x:x+w]
    
    # Resize if target dimensions specified
    if target_width and target_height and not aspect_ratio:
        resized = cv2.resize(cropped, (target_width, target_height),
                           interpolation=cv2.INTER_LANCZOS4)
        return resized
    
    return cropped


def create_debug_overlay(img: np.ndarray, saliency_map: np.ndarray,
                         bbox: tuple, output_path: str):
    """Save debug visualization showing saliency map and detected region."""
    h, w = img.shape[:2]
    
    # Resize saliency map to match image
    saliency_display = cv2.resize(saliency_map, (w, h))
    
    # Apply colormap
    saliency_colored = cv2.applyColorMap(
        (saliency_display * 255).astype(np.uint8),
        cv2.COLORMAP_JET
    )
    
    # Create a side-by-side comparison
    debug_img = np.hstack([img, saliency_colored])
    
    # Draw bounding box on saliency side
    if bbox:
        x, y, bw, bh = bbox
        offset_x = w  # Offset because saliency map is in right half
        cv2.rectangle(debug_img,
                     (offset_x + x, y), (offset_x + x + bw, y + bh),
                     (0, 255, 0), 3)
    
    cv2.imwrite(output_path, debug_img)


# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────

def process(input_path: str, output_path: str,
           target_width: int = None,
           target_height: int = None,
           aspect_ratio: float = None,
           padding: float = 0.05,
           algorithm: str = "auto",
           grabcut: bool = False,
           threshold: float = 0.3,
           debug: bool = False,
           no_exif: bool = False,
           json_output: bool = False) -> dict:
    """Process smart crop."""
    start = time.time()
    
    img = cv2.imread(input_path)
    if img is None:
        return {"success": False, "error": f"Could not read: {input_path}"}
    
    h, w = img.shape[:2]
    
    # Compute saliency map for debug visualization
    algo = "finegrained" if algorithm == "auto" else algorithm
    saliency_map = detect_saliency_map(img, algorithm=algo)
    raw_bbox = saliency_map_to_bbox(saliency_map, threshold=threshold)
    
    # Process
    result = smart_crop(
        img,
        target_width=target_width,
        target_height=target_height,
        aspect_ratio=aspect_ratio,
        padding=padding,
        algorithm=algorithm,
        refine_with_grabcut=grabcut,
        threshold=threshold
    )
    
    cv2.imwrite(output_path, result)
    
    # EXIF preservation
    if not no_exif and EXIF_PRESERVER:
        try:
            preserver = EXIF_PRESERVER(input_path)
            if preserver.has_exif():
                preserver.apply_to_file(output_path)
        except Exception:
            pass
    
    # Debug overlay
    if debug:
        debug_path = output_path.rsplit('.', 1)[0] + '_debug.jpg'
        create_debug_overlay(img, saliency_map, raw_bbox, debug_path)
    
    elapsed_ms = int((time.time() - start) * 1000)
    
    rh, rw = result.shape[:2]
    
    result_dict = {
        "success": True,
        "input_size": [w, h],
        "output_size": [rw, rh],
        "saliency_bbox": [int(x) for x in raw_bbox] if raw_bbox else None,
        "elapsed_ms": elapsed_ms,
        "output": output_path
    }
    
    if json_output:
        print(json.dumps(result_dict), file=sys.stdout)
    else:
        print(f"✓ Smart crop complete in {elapsed_ms}ms")
        print(f"  Input:  {w}×{h} → Output: {rw}×{rh}")
        if raw_bbox:
            x, y, bw, bh = raw_bbox
            print(f"  Saliency region: ({x},{y}) {bw}×{bh}")
        if debug:
            print(f"  Debug overlay: {debug_path}")
    
    return result_dict


def main():
    parser = argparse.ArgumentParser(
        description="Smart Crop - Automatic intelligent cropping based on saliency detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.jpg output.jpg                           # Auto crop to salient region
  %(prog)s input.jpg output.jpg --aspect 16/9            # Crop to 16:9
  %(prog)s input.jpg output.jpg --aspect 4/3 --padding 0.1 # 4:3 with 10%% margin
  %(prog)s input.jpg output.jpg --width 800 --height 600  # Resize after crop
  %(prog)s input.jpg output.jpg --algorithm spectral      # Force spectral algorithm
  %(prog)s input.jpg output.jpg --grabcut                # Use GrabCut refinement
  %(prog)s input.jpg output.jpg --debug                   # Generate debug overlay
        """
    )
    
    parser.add_argument("input", help="Input image")
    parser.add_argument("output", help="Output image")
    
    # Crop dimensions
    parser.add_argument("--width", "-w", type=int,
                       help="Target width (with --height for exact size, without for aspect)")
    parser.add_argument("--height", "-H", type=int,
                       help="Target height (with --width for exact size)")
    parser.add_argument("--aspect", "-a", type=str, default=None,
                       help="Aspect ratio (e.g. 16/9, 4/3, 1/1, 3/2)")
    
    # Saliency control
    parser.add_argument("--padding", "-p", type=float, default=0.05,
                       help="Margin around subject (0.0-0.3, default: 0.05)")
    parser.add_argument("--threshold", "-t", type=float, default=0.3,
                       help="Saliency threshold (0.1-0.8, default: 0.3)")
    parser.add_argument("--algorithm", type=str, default="auto",
                       choices=["auto", "finegrained", "spectral", "edge"],
                       help="Saliency algorithm (default: auto)")
    parser.add_argument("--grabcut", "-g", action="store_true",
                       help="Use GrabCut to refine crop boundary")
    
    # Output options
    parser.add_argument("--debug", "-d", action="store_true",
                       help="Generate debug saliency map overlay")
    parser.add_argument("--no-exif", action="store_true",
                       help="Do not preserve EXIF metadata")
    parser.add_argument("--json", action="store_true",
                       help="Output JSON results")
    
    args = parser.parse_args()
    
    # Parse aspect ratio
    aspect_ratio = None
    if args.aspect:
        try:
            if '/' in args.aspect:
                w, h = args.aspect.split('/')
                aspect_ratio = float(w) / float(h)
            else:
                aspect_ratio = float(args.aspect)
        except ValueError:
            print(f"Error: Invalid aspect ratio: {args.aspect}", file=sys.stderr)
            sys.exit(1)
    
    # Validate
    if args.padding < 0 or args.padding > 0.5:
        print("Error: --padding must be between 0.0 and 0.5", file=sys.stderr)
        sys.exit(1)
    
    if args.threshold < 0.05 or args.threshold > 0.95:
        print("Error: --threshold must be between 0.05 and 0.95", file=sys.stderr)
        sys.exit(1)
    
    if args.width and args.height and aspect_ratio:
        print("Error: Cannot use --width/--height with --aspect simultaneously",
              file=sys.stderr)
        sys.exit(1)
    
    # Create output directory
    out_dir = os.path.dirname(args.output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    try:
        result = process(
            args.input, args.output,
            target_width=args.width,
            target_height=args.height,
            aspect_ratio=aspect_ratio,
            padding=args.padding,
            algorithm=args.algorithm,
            grabcut=args.grabcut,
            threshold=args.threshold,
            debug=args.debug,
            no_exif=args.no_exif,
            json_output=args.json
        )
        sys.exit(0 if result["success"] else 1)
    except Exception as e:
        if args.json:
            print(json.dumps({"success": False, "error": str(e)}), file=sys.stdout)
        else:
            print(f"Error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
