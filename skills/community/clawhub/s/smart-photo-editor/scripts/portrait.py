#!/home/guoxh/.openclaw/venv-clawd/bin/python
"""
Portrait Retouching Tool

AI-powered and traditional portrait enhancements:
- Skin smoothing (bilateral filter - preserves edges)
- Red-eye removal
- Blemish/dust removal (OpenCV inpainting)
- Teeth whitening
- Eye brightening/enhancement
- Face-aware brightness/contrast
- Sharpening

Uses OpenCV's built-in Haar Cascade for face/eye detection,
so no external models needed.

Usage:
    ./portrait.py input.jpg output.jpg --smooth 3 --enhance-eyes
    ./portrait.py input.jpg output.jpg --brightness 10 --contrast 15
    ./portrait.py input.jpg output.jpg --red-eye --whiten-teeth
    ./portrait.py input.jpg output.jpg --smooth 2 --denoise --face-region
"""
import argparse
import os
import sys
import json
import time
import numpy as np
import cv2

# Add parent directory to path for exif_utils
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

try:
    from exif_utils import ExifPreserver
    EXIF_PRESERVER = ExifPreserver  # Class reference
except ImportError:
    EXIF_PRESERVER = None


# ─────────────────────────────────────────────────────────────────
# Utility functions
# ─────────────────────────────────────────────────────────────────

def clamp(val, min_val=0, max_val=255):
    return max(min_val, min(max_val, val))


def get_face_cascade():
    """Load OpenCV's face detection cascade."""
    # OpenCV ships with pretrained Haar cascades
    cascade_paths = [
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml',
        cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml',
        cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml',
        cv2.data.haarcascades + 'haarcascade_frontalface_alt_tree.xml',
    ]
    
    for path in cascade_paths:
        if os.path.exists(path):
            return cv2.CascadeClassifier(path)
    return None


def get_eye_cascade():
    """Load OpenCV's eye detection cascade."""
    cascade_paths = [
        cv2.data.haarcascades + 'haarcascade_eye.xml',
        cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml',
    ]
    
    for path in cascade_paths:
        if os.path.exists(path):
            return cv2.CascadeClassifier(path)
    return None


def detect_face_roi(img: np.ndarray):
    """
    Detect face region in image.
    Returns (x, y, w, h) of the face bounding box, or None if not found.
    """
    cascade = get_face_cascade()
    if cascade is None:
        return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    
    # Detect faces (scale factor and minNeighbors tuned for portraits)
    faces = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80),
        maxSize=(600, 600)
    )
    
    if len(faces) == 0:
        return None
    
    # Return the largest face
    largest = max(faces, key=lambda f: f[2] * f[3])
    return tuple(largest)


def detect_eyes(img: np.ndarray, face_roi: tuple):
    """
    Detect eyes within a face region.
    Returns list of (x, y, w, h) eye bounding boxes relative to full image.
    """
    cascade = get_eye_cascade()
    if cascade is None:
        return []
    
    x, y, w, h = face_roi
    face_gray = cv2.cvtColor(img[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
    face_gray = cv2.equalizeHist(face_gray)
    
    eyes = cascade.detectMultiScale(
        face_gray,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(20, 20),
        maxSize=(150, 150)
    )
    
    # Convert to full-image coordinates
    eye_boxes = []
    for ex, ey, ew, eh in eyes:
        eye_boxes.append((x + ex, y + ey, ew, eh))
    
    return eye_boxes


def apply_clahe(img: np.ndarray, clip_limit=2.0, tile_size=8):
    """Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)."""
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))
    l = clahe.apply(l)
    lab = cv2.merge([l, a, b])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


# ─────────────────────────────────────────────────────────────────
# Portrait operations
# ─────────────────────────────────────────────────────────────────

def smooth_skin(img: np.ndarray, strength: float = 3.0,
                face_roi: tuple = None, preserve_features: bool = True) -> np.ndarray:
    """
    Smooth skin using bilateral filter.
    
    Args:
        img: Input image
        strength: Smoothing strength (1-10, default 3)
                  1-2: Subtle, 3-5: Medium, 6-10: Strong
        face_roi: Optional face bounding box to limit effect
        preserve_features: Keep edges/eyes sharp
    
    Returns:
        Smoothed image
    """
    # Bilateral filter params scale with strength
    d = int(strength) * 2 + 1  # Diameter of pixel neighborhood (must be odd)
    sigma_color = strength * 10  # Filter strength in color space
    sigma_space = strength * 10  # Filter strength in coordinate space
    
    if face_roi is not None:
        x, y, w, h = face_roi
        # Expand face region slightly for natural blending
        margin = int(h * 0.2)
        x1, y1 = max(0, x - margin), max(0, y - margin)
        x2, y2 = min(img.shape[1], x + w + margin), min(img.shape[0], y + h + margin)
        
        result = img.copy()
        
        # Apply bilateral to face region
        face = result[y1:y2, x1:x2]
        smoothed = cv2.bilateralFilter(face, d, sigma_color, sigma_space)
        result[y1:y2, x1:x2] = smoothed
        
        return result
    else:
        return cv2.bilateralFilter(img, d, sigma_color, sigma_space)


def denoise(img: np.ndarray, strength: int = 10) -> np.ndarray:
    """
    Reduce image noise while preserving detail.
    
    Args:
        strength: Denoising strength (1-30)
    
    Returns:
        Denoised image
    """
    return cv2.fastNlMeansDenoisingColored(img, None, strength, strength, 7, 21)


def sharpen(img: np.ndarray, strength: float = 1.0) -> np.ndarray:
    """
    Sharpen image using unsharp masking.
    
    Args:
        strength: Sharpening strength (0.5-3.0)
    
    Returns:
        Sharpened image
    """
    # Create sharpening kernel
    kernel = np.array([
        [-1, -1, -1],
        [-1,  9, -1],
        [-1, -1, -1]
    ])
    
    # Scale kernel strength
    identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    kernel = identity + (kernel - identity) * strength
    
    return cv2.filter2D(img, -1, kernel)


def remove_red_eye(img: np.ndarray, face_roi: tuple = None,
                   eye_rois: list = None) -> np.ndarray:
    """
    Remove red-eye effect from flash photography.
    
    Args:
        img: Input image
        face_roi: Face bounding box for auto-detection
        eye_rois: Optional pre-detected eye regions
    
    Returns:
        Image with red-eye corrected
    """
    result = img.copy()
    
    # Get regions to process
    if eye_rois:
        regions = eye_rois
    elif face_roi:
        eyes = detect_eyes(img, face_roi)
        regions = eyes if eyes else []
    else:
        # Try face detection first
        face = detect_face_roi(img)
        if face:
            eyes = detect_eyes(img, face)
            regions = eyes
        else:
            regions = []
    
    for ex, ey, ew, eh in regions:
        eye_region = result[ey:ey+eh, ex:ex+ew]
        
        # Convert to HSV to detect red/magenta tones
        hsv = cv2.cvtColor(eye_region, cv2.COLOR_BGR2HSV)
        
        # Create mask for red/magenta (red eye has hue ~0 or ~180)
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)
        
        if cv2.countNonZero(mask) > 10:  # Only process if significant red found
            # Replace red pixels with desaturated version of surrounding
            mean_val = cv2.mean(eye_region, mask=255-mask)[:3]
            
            # Create corrected region
            correction = np.full_like(eye_region, mean_val, dtype=np.uint8)
            
            # Blend: only where mask is active
            mask_3ch = cv2.merge([mask, mask, mask])
            alpha = mask_3ch.astype(float) / 255.0 * 0.8  # 80% correction
            
            corrected = (eye_region.astype(float) * (1 - alpha) +
                        correction.astype(float) * alpha).astype(np.uint8)
            
            result[ey:ey+eh, ex:ex+ew] = corrected
    
    return result


def whiten_teeth(img: np.ndarray, face_roi: tuple = None, strength: float = 0.3) -> np.ndarray:
    """
    Whiten teeth in portrait. Targets lower-face region.
    
    Args:
        img: Input image
        face_roi: Face bounding box to define lower-face region
        strength: Whitening strength (0.1-0.8)
    
    Returns:
        Image with whitened teeth
    """
    result = img.copy()
    
    if face_roi is None:
        face_roi = detect_face_roi(img)
    
    if face_roi is None:
        return result  # No face detected, skip
    
    x, y, w, h = face_roi
    
    # Teeth region: lower 30% of face, center 60%
    margin_x = int(w * 0.2)
    tx1 = x + margin_x
    tx2 = x + w - margin_x
    ty1 = y + int(h * 0.65)
    ty2 = y + int(h * 0.85)
    
    teeth_region = result[ty1:ty2, tx1:tx2]
    
    # Convert to LAB for brightness manipulation
    lab = cv2.cvtColor(teeth_region, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Increase L (lightness) and reduce yellow tint (b channel)
    # White teeth: higher L, lower b (less yellow)
    l = cv2.add(l, int(strength * 30))
    b = cv2.subtract(b, int(strength * 20))
    
    lab = cv2.merge([l, a, b])
    corrected = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    # Blend only the teeth area using color-based mask
    hsv = cv2.cvtColor(teeth_region, cv2.COLOR_BGR2HSV)
    # Skin color range (to exclude from blending)
    skin_mask = cv2.inRange(hsv, (0, 10, 30), (30, 150, 200))
    skin_mask = cv2.GaussianBlur(skin_mask, (5, 5), 0)
    skin_mask = cv2.resize(skin_mask, (corrected.shape[1], corrected.shape[0]))
    
    # Apply blending
    alpha = (255 - skin_mask).astype(float) / 255.0 * strength
    alpha_3ch = cv2.merge([alpha, alpha, alpha])
    
    result[ty1:ty2, tx1:tx2] = (
        teeth_region.astype(float) * (1 - alpha_3ch) +
        corrected.astype(float) * alpha_3ch
    ).astype(np.uint8)
    
    return result


def enhance_eyes(img: np.ndarray, face_roi: tuple = None,
                 brightness_boost: float = 0.2,
                 saturation_boost: float = 0.15,
                 sharpen_eyes: bool = True) -> np.ndarray:
    """
    Brighten and enhance eyes in portrait.
    
    Args:
        img: Input image
        face_roi: Face bounding box
        brightness_boost: How much to brighten eyes (0-0.5)
        saturation_boost: How much to boost eye color saturation (0-0.5)
        sharpen_eyes: Apply slight sharpening to eye region
    
    Returns:
        Image with enhanced eyes
    """
    result = img.copy()
    
    if face_roi is None:
        face_roi = detect_face_roi(img)
    
    if face_roi is None:
        return result
    
    eyes = detect_eyes(img, face_roi)
    
    for ex, ey, ew, eh in eyes:
        # Expand eye region slightly for context
        margin = int(ew * 0.3)
        ex1 = max(0, ex - margin)
        ey1 = max(0, ey - margin)
        ex2 = min(img.shape[1], ex + ew + margin)
        ey2 = min(img.shape[0], ey + eh + margin)
        
        eye_region = result[ey1:ey2, ex1:ex2]
        
        # Brightness: increase L in LAB
        lab = cv2.cvtColor(eye_region, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l = np.clip(l.astype(int) + int(brightness_boost * 100), 0, 255).astype(np.uint8)
        lab = cv2.merge([l, a, b])
        bright = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Saturation: boost S in HSV
        hsv = cv2.cvtColor(bright, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        s = np.clip(s.astype(int) + int(saturation_boost * 100), 0, 255).astype(np.uint8)
        hsv = cv2.merge([h, s, v])
        saturated = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        # Blend back
        result[ey1:ey2, ex1:ex2] = saturated
        
        # Sharpen if requested
        if sharpen_eyes:
            kernel = np.array([[-0.5, -0.5, -0.5],
                             [-0.5,  4.0, -0.5],
                             [-0.5, -0.5, -0.5]]) * 0.5
            sharpened = cv2.filter2D(result[ey1:ey2, ex1:ex2], -1, kernel)
            result[ey1:ey2, ex1:ex2] = sharpened
    
    return result


def adjust_face_brightness(img: np.ndarray, face_roi: tuple = None,
                           brightness: float = 0,
                           contrast: float = 0,
                           gamma: float = 1.0) -> np.ndarray:
    """
    Apply brightness/contrast/gamma adjustment to face region.
    
    Args:
        brightness: -100 to 100 (mapped to pixel offset)
        contrast: -100 to 100 (mapped to multiplier)
        gamma: 0.1 to 3.0 (gamma correction)
    
    Returns:
        Image with adjusted face
    """
    result = img.copy()
    
    if face_roi is None:
        face_roi = detect_face_roi(img)
    
    if face_roi is None:
        return result
    
    x, y, w, h = face_roi
    
    # Expand slightly for natural look
    margin = int(h * 0.1)
    x1, y1 = max(0, x - margin), max(0, y - margin)
    x2, y2 = min(img.shape[1], x + w + margin), min(img.shape[0], y + h + margin)
    
    face = result[y1:y2, x1:x2].astype(np.float32)
    
    # Brightness: add offset
    if brightness != 0:
        face = face + (brightness * 2.55)
    
    # Contrast: multiply
    if contrast != 0:
        factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
        face = factor * (face - 128) + 128
    
    # Gamma correction
    if gamma != 1.0:
        face = 255 * np.power(np.clip(face / 255.0, 0, 1), 1.0 / gamma)
    
    face = np.clip(face, 0, 255).astype(np.uint8)
    
    # Soft edge blend
    mask = np.ones_like(face, dtype=float)
    feather = margin * 2
    if feather > 0:
        mask = cv2.GaussianBlur(mask, (feather*2+1, feather*2+1), 0)
    
    original = result[y1:y2, x1:x2].astype(np.float32)
    blended = original * (1 - mask) + face.astype(np.float32) * mask
    result[y1:y2, x1:x2] = np.clip(blended, 0, 255).astype(np.uint8)
    
    return result


def remove_blemishes(img: np.ndarray, face_roi: tuple = None,
                      radius: int = 5, threshold: int = 15) -> np.ndarray:
    """
    Remove small blemishes/spots from face using inpainting.
    Uses template matching to find spots that differ from surroundings.
    
    Args:
        face_roi: Face bounding box to limit search
        radius: Spot radius to check
        threshold: How different a pixel must be to be considered a blemish
    
    Returns:
        Image with blemishes removed
    """
    result = img.copy()
    
    if face_roi is None:
        face_roi = detect_face_roi(img)
    
    if face_roi is None:
        return result
    
    x, y, w, h = face_roi
    
    # Work on face region only
    face = result[y:y+h, x:x+w]
    face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    
    # Compute local mean using blur
    local_mean = cv2.blur(face_gray, (radius*2+1, radius*2+1))
    
    # Find pixels that differ significantly from local mean
    diff = cv2.absdiff(face_gray, local_mean)
    _, blemish_mask = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    
    # Clean up mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    blemish_mask = cv2.morphologyEx(blemish_mask, cv2.MORPH_OPEN, kernel)
    blemish_mask = cv2.morphologyEx(blemish_mask, cv2.MORPH_CLOSE, kernel)
    
    # Inpaint only the blemish pixels
    if cv2.countNonZero(blemish_mask) > 0:
        mask_3ch = cv2.merge([blemish_mask, blemish_mask, blemish_mask])
        inpainted = cv2.inpaint(face, mask_3ch, radius, cv2.INPAINT_TELEA)
        result[y:y+h, x:x+w] = inpainted
    
    return result


def auto_skin_tone_enhance(img: np.ndarray, face_roi: tuple = None) -> np.ndarray:
    """
    Enhance natural skin tone - warm, healthy look.
    """
    result = img.copy()
    
    if face_roi is None:
        face_roi = detect_face_roi(img)
    
    if face_roi is None:
        return result
    
    x, y, w, h = face_roi
    
    # Expand for natural blending
    margin = int(h * 0.15)
    x1, y1 = max(0, x - margin), max(0, y - margin)
    x2, y2 = min(img.shape[1], x + w + margin), min(img.shape[0], y + h + margin)
    
    skin = result[y1:y2, x1:x2]
    
    # Slight warm shift: increase R slightly, decrease B slightly
    # Keep G roughly same
    skin = skin.astype(np.float32)
    skin[:, :, 2] = np.clip(skin[:, :, 2] * 1.05, 0, 255)  # R
    skin[:, :, 0] = np.clip(skin[:, :, 0] * 0.97, 0, 255)  # B
    
    # Slight saturation boost
    hsv = cv2.cvtColor(skin.astype(np.uint8), cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = np.clip(s.astype(float) * 1.1, 0, 255).astype(np.uint8)
    hsv = cv2.merge([h, s, v])
    skin = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    # Blend
    mask = np.ones_like(skin, dtype=float) * 0.7  # 70% blend
    blended = (result[y1:y2, x1:x2].astype(float) * (1 - mask) +
               skin.astype(float) * mask)
    
    result[y1:y2, x1:x2] = np.clip(blended, 0, 255).astype(np.uint8)
    
    return result


# ─────────────────────────────────────────────────────────────────
# Main processing pipeline
# ─────────────────────────────────────────────────────────────────

def process_portrait(input_path: str, output_path: str,
                    smooth: float = None,
                    denoise_strength: int = None,
                    sharpen_strength: float = None,
                    red_eye: bool = False,
                    whiten_teeth_strength: float = None,
                    enhance_eyes: bool = False,
                    brightness: float = None,
                    contrast: float = None,
                    gamma: float = None,
                    blemish_removal: bool = False,
                    skin_tone: bool = False,
                    auto_detect: bool = True,
                    no_exif: bool = False,
                    json_output: bool = False,
                    **kwargs) -> dict:
    """
    Process portrait photo with requested enhancements.
    
    Returns:
        dict with success status, operations performed, elapsed time
    """
    start = time.time()
    operations = []
    
    # Read image
    img = cv2.imread(input_path)
    if img is None:
        return {"success": False, "error": f"Could not read: {input_path}"}
    
    # Detect face once
    face_roi = None
    eye_rois = []
    if auto_detect:
        face_roi = detect_face_roi(img)
        if face_roi:
            eye_rois = detect_eyes(img, face_roi)
            if json_output:
                x, y, w, h = face_roi
                print(json.dumps({"face_detected": True,
                                 "face_roi": [int(x), int(y), int(w), int(h)],
                                 "eyes_detected": len(eye_rois)}),
                     file=sys.stderr)
        else:
            if json_output:
                print(json.dumps({"face_detected": False}), file=sys.stderr)
    
    result = img.copy()
    
    # Build processing chain
    if smooth is not None:
        result = smooth_skin(result, strength=smooth,
                            face_roi=face_roi if auto_detect else None)
        operations.append(f"smooth({smooth})")
    
    if denoise_strength is not None:
        result = denoise(result, strength=denoise_strength)
        operations.append(f"denoise({denoise_strength})")
    
    if blemish_removal and face_roi:
        result = remove_blemishes(result, face_roi=face_roi)
        operations.append("blemish_removal")
    
    if red_eye:
        result = remove_red_eye(result, face_roi=face_roi, eye_rois=eye_rois)
        operations.append("red_eye_removal")
    
    if whiten_teeth_strength is not None and face_roi:
        result = whiten_teeth(result, face_roi=face_roi,
                             strength=whiten_teeth_strength)
        operations.append(f"teeth_whitening({whiten_teeth_strength})")
    
    if enhance_eyes:
        result = enhance_eyes(result, face_roi=face_roi)
        operations.append("eye_enhancement")
    
    if brightness is not None or contrast is not None or gamma is not None:
        b = brightness if brightness is not None else 0
        c = contrast if contrast is not None else 0
        g = gamma if gamma is not None else 1.0
        result = adjust_face_brightness(result, face_roi=face_roi,
                                        brightness=b, contrast=c, gamma=g)
        ops_str = f"face_adjust(b={b},c={c},g={g})"
        operations.append(ops_str)
    
    if skin_tone:
        result = auto_skin_tone_enhance(result, face_roi=face_roi)
        operations.append("skin_tone_enhancement")
    
    if sharpen_strength is not None:
        result = sharpen(result, strength=sharpen_strength)
        operations.append(f"sharpen({sharpen_strength})")
    
    # Save output
    cv2.imwrite(output_path, result)
    
    # Apply EXIF preservation
    elapsed_ms = int((time.time() - start) * 1000)
    
    if not no_exif and EXIF_PRESERVER:
        try:
            preserver = EXIF_PRESERVER(input_path)
            if preserver.has_exif():
                preserver.apply_to_file(output_path)
        except Exception as e:
            print(f"Warning: EXIF preservation failed: {e}", file=sys.stderr)
    
    result_dict = {
        "success": True,
        "operations": operations,
        "elapsed_ms": elapsed_ms,
        "output": output_path
    }
    
    if json_output:
        print(json.dumps(result_dict), file=sys.stdout)
    else:
        print(f"✓ Portrait retouching complete in {elapsed_ms}ms")
        print(f"  Operations: {', '.join(operations) if operations else 'none'}")
        print(f"  Output: {output_path}")
    
    return result_dict


# ─────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Portrait Retouching Tool - skin smoothing, red-eye removal, etc.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.jpg output.jpg --smooth 3
  %(prog)s input.jpg output.jpg --smooth 2 --enhance-eyes --red-eye
  %(prog)s input.jpg output.jpg --brightness 10 --contrast 15 --face-region
  %(prog)s input.jpg output.jpg --blemish-removal --skin-tone
  %(prog)s input.jpg output.jpg --all --face-region
        """
    )
    
    parser.add_argument("input", help="Input portrait image")
    parser.add_argument("output", help="Output image path")
    
    # Skin enhancements
    parser.add_argument("--smooth", type=float, default=None,
                       help="Skin smoothing strength (1-10, default: off)")
    parser.add_argument("--denoise", type=int, default=None,
                       help="Denoise strength (1-30, default: off)")
    parser.add_argument("--blemish-removal", action="store_true",
                       help="Remove small blemishes/spots")
    parser.add_argument("--skin-tone", action="store_true",
                       help="Enhance natural skin tone (warm, healthy)")
    
    # Feature enhancements
    parser.add_argument("--red-eye", action="store_true",
                       help="Remove red-eye from flash photos")
    parser.add_argument("--whiten-teeth", type=float, default=None,
                       help="Teeth whitening strength (0.1-0.8)")
    parser.add_argument("--enhance-eyes", action="store_true",
                       help="Brighten and sharpen eyes")
    
    # Global adjustments
    parser.add_argument("--brightness", type=float, default=None,
                       help="Face brightness adjustment (-100 to 100)")
    parser.add_argument("--contrast", type=float, default=None,
                       help="Face contrast adjustment (-100 to 100)")
    parser.add_argument("--gamma", type=float, default=None,
                       help="Face gamma correction (0.1-3.0, 1.0=no change)")
    parser.add_argument("--sharpen", type=float, default=None,
                       help="Sharpening strength (0.5-3.0)")
    
    # Presets
    parser.add_argument("--all", action="store_true",
                       help="Apply all enhancements with sensible defaults")
    parser.add_argument("--subtle", action="store_true",
                       help="Apply subtle all enhancements (conservative)")
    
    # Detection control
    parser.add_argument("--no-auto-detect", action="store_true",
                       help="Disable automatic face/eye detection")
    parser.add_argument("--face-region", action="store_true",
                       help="Limit effects to detected face region")
    
    # Output options
    parser.add_argument("--no-exif", action="store_true",
                       help="Do not preserve EXIF metadata")
    parser.add_argument("--json", action="store_true",
                       help="Output JSON results")
    
    args = parser.parse_args()
    
    # Handle presets
    if args.all:
        args.smooth = args.smooth or 2.0
        args.denoise = args.denoise or 5
        args.enhance_eyes = True
        args.red_eye = True
        args.skin_tone = True
        args.blemish_removal = True
    
    if args.subtle:
        args.smooth = args.smooth or 1.5
        args.enhance_eyes = True
        args.skin_tone = True
        args.red_eye = True
    
    # Validate
    if args.smooth is not None and not (0.5 <= args.smooth <= 10):
        print("Error: --smooth must be between 0.5 and 10", file=sys.stderr)
        sys.exit(1)
    
    if args.denoise is not None and not (1 <= args.denoise <= 30):
        print("Error: --denoise must be between 1 and 30", file=sys.stderr)
        sys.exit(1)
    
    if args.whiten_teeth is not None and not (0.1 <= args.whiten_teeth <= 0.8):
        print("Error: --whiten-teeth must be between 0.1 and 0.8", file=sys.stderr)
        sys.exit(1)
    
    auto_detect = not args.no_auto_detect
    
    # Create output directory
    out_dir = os.path.dirname(args.output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    # Process
    try:
        result = process_portrait(
            args.input, args.output,
            smooth=args.smooth,
            denoise_strength=args.denoise,
            sharpen_strength=args.sharpen,
            red_eye=args.red_eye,
            whiten_teeth_strength=args.whiten_teeth,
            enhance_eyes=args.enhance_eyes,
            brightness=args.brightness,
            contrast=args.contrast,
            gamma=args.gamma,
            blemish_removal=args.blemish_removal,
            skin_tone=args.skin_tone,
            auto_detect=auto_detect,
            no_exif=args.no_exif,
            json_output=args.json
        )
        sys.exit(0 if result["success"] else 1)
    except Exception as e:
        if args.json:
            print(json.dumps({"success": False, "error": str(e)}), file=sys.stdout)
        else:
            print(f"Error: {e}", file=sys.stderr)
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    import traceback
    main()
