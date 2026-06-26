#!/usr/bin/env python3
"""
Tencent Cloud MPS Image Processing Script

Features:
  Use MPS image processing capabilities, supporting image enhancement, noise reduction, super-resolution,
  beautification & filters, and other rich features!

  Supported processing capabilities (can be combined):
    1. Image encoding configuration (format conversion) — Format conversion (JPEG/PNG/BMP/WebP), quality adjustment
    2. Image enhancement configuration — Super-resolution, advanced super-resolution, noise reduction, comprehensive
    enhancement, color enhancement,
                                    detail enhancement, face enhancement, low-light enhancement
    3. Image erasure configuration — Erase icons/text/watermarks (supports automatic detection and specified regions)
    4. Blind watermark configuration — Add blind watermark, extract blind watermark, remove blind watermark
    5. Beautification configuration — Whitening/darkening/skin smoothing/face slimming/eye enlarging/lipstick/makeup
    and 20+ effects
    6. Filter configuration — Tokyo/Light Film/Delicious and other style filters
    7. Basic image transformation capabilities (scaling) — Percentage scaling, proportional scaling, fixed dimensions,
    crop and fill

COS Storage Convention:
  Specify COS Bucket name via environment variable TENCENTCLOUD_COS_BUCKET.
  - Default input file path: {TENCENTCLOUD_COS_BUCKET}/input/
  - Default output file path: {TENCENTCLOUD_COS_BUCKET}/output/image/

Usage:
  # Simplest usage: only specify input image (no processing, for connectivity testing)
  python mps_imageprocess.py --url https://example.com/image.jpg

  # === Image Encoding (Format Conversion) ===
  # Convert to PNG format
  python mps_imageprocess.py --url https://example.com/image.jpg --format PNG

  # Convert to WebP format + specify quality 80
  python mps_imageprocess.py --url https://example.com/image.jpg --format WebP --quality 80

  # === Image Enhancement ===
  # Super-resolution (2x enlargement)
  python mps_imageprocess.py --url https://example.com/image.jpg --super-resolution

  # Advanced super-resolution (specify target width/height)
  python mps_imageprocess.py --url https://example.com/image.jpg --advanced-sr --sr-width 3840 --sr-height 2160

  # Advanced super-resolution (ratio mode, 3x enlargement)
  python mps_imageprocess.py --url https://example.com/image.jpg --advanced-sr --sr-percent 3.0

  # Noise reduction (strong)
  python mps_imageprocess.py --url https://example.com/image.jpg --denoise strong

  # Comprehensive enhancement (strong)
  python mps_imageprocess.py --url https://example.com/image.jpg --quality-enhance strong

  # Color enhancement
  python mps_imageprocess.py --url https://example.com/image.jpg --color-enhance normal

  # Detail enhancement (intensity 0.8)
  python mps_imageprocess.py --url https://example.com/image.jpg --sharp-enhance 0.8

  # Face enhancement (intensity 0.5)
  python mps_imageprocess.py --url https://example.com/image.jpg --face-enhance 0.5

  # Low-light enhancement
  python mps_imageprocess.py --url https://example.com/image.jpg --lowlight-enhance

  # Combination: noise reduction + super-resolution + color enhancement
  python mps_imageprocess.py --url https://example.com/image.jpg \\
      --denoise weak --super-resolution --color-enhance normal

  # === Image Erasure ===
  # Auto-detect and erase icons and text
  python mps_imageprocess.py --url https://example.com/image.jpg --erase-detect logo text

  # Auto-detect and erase watermarks
  python mps_imageprocess.py --url https://example.com/image.jpg --erase-detect watermark

  # Specify region erasure (pixel coordinates)
  python mps_imageprocess.py --url https://example.com/image.jpg --erase-area 100,50,300,200

  # Specify region erasure (percentage coordinates)
  python mps_imageprocess.py --url https://example.com/image.jpg --erase-box 0.1,0.1,0.3,0.3

  # === Blind Watermark ===
  # Add blind watermark
  python mps_imageprocess.py --url https://example.com/image.jpg --add-watermark "test"

  # Extract blind watermark
  python mps_imageprocess.py --url https://example.com/image.jpg --extract-watermark

  # Remove blind watermark
  python mps_imageprocess.py --url https://example.com/image.jpg --remove-watermark

  # === Beautification ===
  # Whitening (intensity 50)
  python mps_imageprocess.py --url https://example.com/image.jpg --beauty Whiten:50

  # Skin smoothing + face slimming
  python mps_imageprocess.py --url https://example.com/image.jpg \\
      --beauty Smooth:60 --beauty BeautyThinFace:40

  # Lipstick (specify color)
  python mps_imageprocess.py --url https://example.com/image.jpg \\
      --beauty 'FaceFeatureLipsLut:50:#ff0000'

  # === Filters ===
  # Light Film filter (intensity 70)
  python mps_imageprocess.py --url https://example.com/image.jpg --filter Qingjiaopian:70

  # === Image Scaling ===
  # Percentage scaling (2x enlargement)
  python mps_imageprocess.py --url https://example.com/image.jpg --resize-percent 2.0

  # Proportional scaling to specified width/height (smaller rectangle)
  python mps_imageprocess.py --url https://example.com/image.jpg --resize-mode lfit --resize-width 800 --resize-height
  600

  # Fixed dimension scaling
  python mps_imageprocess.py --url https://example.com/image.jpg --resize-mode fixed --resize-width 1920
  --resize-height 1080

  # === Combination usage ===
  # Noise reduction + super-resolution + beautification + format conversion
  python mps_imageprocess.py --url https://example.com/image.jpg \\
      --denoise weak --super-resolution --beauty Whiten:30 --beauty Smooth:40 \\
      --format PNG --quality 90

  # === Orchestration Scenarios (ScheduleId, Tencent Cloud console preset AI capabilities) ===
  # AI Image Understanding (30200)
  python mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30200

  # AI Cutout (30030)
  python mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30030

  # AI Image Restoration (30040)
  python mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30040

  # AI Foreground Extraction (30031)
  python mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30031

  # AI Outpainting (30010, image extension)
  python mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30010

  # AI Text Watermark Erasure (30000)
  python mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30000

  # Dry Run (only print request parameters, not actually call API)
  python mps_imageprocess.py --url https://example.com/image.jpg --super-resolution --dry-run

Environment Variables:
  TENCENTCLOUD_SECRET_ID   - Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  - Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET       - COS Bucket name (e.g., mybucket-125xxx)
  TENCENTCLOUD_COS_REGION       - COS Bucket region (default ap-guangzhou)
"""

import argparse
import base64
import json
import os
import sys
from mps_auto_upgrade import check_sdk_version

# Polling module (same directory)
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)
try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
try:
    from mps_poll_task import poll_image_task, auto_upload_local_file, auto_download_outputs, auto_gen_compare
    _POLL_AVAILABLE = True
except ImportError:
    _POLL_AVAILABLE = False

check_sdk_version()
try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.mps.v20190612 import mps_client, models
except ImportError:
    print("Error: Please install Tencent Cloud SDK first: pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# Beautification effect type descriptions
# =============================================================================
BEAUTY_EFFECT_TYPES = {
    "Whiten": "Whitening",
    "BlackAlpha1": "Darkening",
    "BlackAlpha2": "Stronger darkening",
    "FoundationAlpha2": "Whitening (pink-white)",
    "Clear": "Clarity",
    "Sharpen": "Sharpening",
    "Smooth": "Skin smoothing",
    "BeautyThinFace": "Face slimming",
    "NatureFace": "Natural face shape",
    "VFace": "V-face",
    "EnlargeEye": "Eye enlarging",
    "EyeLighten": "Eye brightening",
    "RemoveEyeBags": "Eye bag removal",
    "ThinNose": "Nose slimming",
    "RemoveLawLine": "Nasolabial fold removal",
    "CheekboneThin": "Cheekbone slimming",
    "FaceFeatureLipsLut": "Lipstick",
    "ToothWhiten": "Teeth whitening",
    "FaceFeatureSoftlight": "Soft light",
    "Makeup": "Makeup",
}

# Filter type descriptions
FILTER_TYPES = {
    "Dongjing": "Tokyo",
    "Qingjiaopian": "Light Film",
    "Meiwei": "Delicious",
}

# Scaling mode descriptions
RESIZE_MODES = {
    "percent": "Percentage scaling",
    "mfit": "Proportional scaling to larger rectangle",
    "lfit": "Proportional scaling to smaller rectangle",
    "fill": "Proportional scaling to larger rectangle with center cropping",
    "pad": "Proportional scaling to smaller rectangle with padding",
    "fixed": "Fixed width/height forced scaling",
}

# =============================================================================
# Orchestration Scenario (ScheduleId) Presets
# =============================================================================
# Preset orchestration workflows triggered via ProcessImage's ScheduleId.
# Orchestration templates are created in the console; the script only passes
# through the ScheduleId. When no extra processing parameters are needed, users
# can invoke the full capability by providing only InputInfo + ScheduleId.
SCHEDULE_PRESETS = {
    30000: "AI Text Watermark Erasure",
    30010: "AI Outpainting (Image Extension)",
    30030: "AI Cutout",
    30031: "AI Foreground Extraction",
    30040: "AI Image Restoration",
    30060: "Image Background Fusion (use mps_image_bg_fusion.py instead)",
    30100: "Image Outfit Change (use mps_image_tryon.py instead)",
    30101: "Lingerie Outfit Change (use mps_image_tryon.py instead)",
    30200: "AI Image Understanding",
}


def get_cos_bucket():
    """Get COS Bucket name from environment variables."""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """Get COS Bucket region from environment variables, default ap-guangzhou."""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


def get_credentials():
    """Get Tencent Cloud credentials from environment variables. If missing, try automatic loading from system files and retry."""  # NOCA:line-too-long(content cannot be shortened)
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        # Try automatic loading from system environment variable files
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] Environment variables not set, trying to load automatically from system files...", file=sys.stderr)  # NOCA:line-too-long(line cannot be shortened)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
        if not secret_id or not secret_key:
            if _LOAD_ENV_AVAILABLE:
                from mps_load_env import _print_setup_hint
                _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            else:
                print(
                    "\nError: TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY not set.\n"
                    "Please add these variables to /etc/environment, ~/.profile, etc.\n"
                )
            sys.exit(1)
    return credential.Credential(secret_id, secret_key)


def create_mps_client(cred, region):
    """Create MPS client."""
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")


    http_profile.reqMethod = "POST"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return mps_client.MpsClient(cred, region, client_profile)


def build_input_info(args):
    """
    Build input information.

    Supports two input methods:
    1. URL input: --url
    2. COS path input: --cos-input-key (with --cos-input-bucket/--cos-input-region or environment variables)
    """
    # Method 1: URL input
    if args.url:
        return {
            "Type": "URL",
            "UrlInputInfo": {
                "Url": args.url
            }
        }

    # Method 3: COS full path input (new version, recommended)
    cos_input_bucket = getattr(args, 'cos_input_bucket', None)
    cos_input_region = getattr(args, 'cos_input_region', None)
    cos_input_key = getattr(args, 'cos_input_key', None)

    if cos_input_key:
        bucket = cos_input_bucket or get_cos_bucket()
        region = cos_input_region or get_cos_region()
        if not bucket:
            print("Error: COS input requires Bucket specification. Please set via --cos-input-bucket parameter or TENCENTCLOUD_COS_BUCKET environment variable",  # NOCA:line-too-long(content cannot be shortened)
                  file=sys.stderr)
            sys.exit(1)
        return {
            "Type": "COS",
            "CosInputInfo": {
                "Bucket": bucket,
                "Region": region,
                "Object": cos_input_key if cos_input_key.startswith("/") else f"/{cos_input_key}"
            }
        }

    print("Error: Please specify an input source:\n"  # NOCA:E302(function structure required for CLI)
          "  - URL: --url <URL>\n"
          "  - COS path: --cos-input-key <key> (with environment variables or --cos-input-bucket/--cos-input-region)",
          file=sys.stderr)
    sys.exit(1)


def build_output_storage(args):
    """
    Build output storage information (COS type).

    Priority:
    1. Command line parameters --output-bucket / --output-region
    2. Environment variables TENCENTCLOUD_COS_BUCKET / TENCENTCLOUD_COS_REGION
    """
    # COS type
    bucket = args.output_bucket or get_cos_bucket()
    region = args.output_region or get_cos_region()

    if bucket and region:
        return {
            "Type": "COS",
            "CosOutputStorage": {
                "Bucket": bucket,
                "Region": region
            }
        }
    return None


# =============================================================================
# Image encoding configuration building
# =============================================================================
def build_encode_config(args):
    """Build image encoding configuration (EncodeConfig) — format conversion and quality adjustment."""
    if not args.format and args.quality is None:
        return None

    config = {}
    if args.format:
        config["Format"] = args.format
    if args.quality is not None:
        config["Quality"] = args.quality
    return config


# =============================================================================
# Image enhancement configuration building
# =============================================================================
def build_enhance_config(args):
    """
    Build image enhancement configuration (EnhanceConfig).

    Includes: super-resolution, advanced super-resolution, denoising, comprehensive enhancement, color enhancement,
    detail enhancement, face enhancement, low-light enhancement.
    """
    has_enhance = any([
        args.super_resolution,
        args.advanced_sr,
        args.denoise is not None,
        args.quality_enhance is not None,
        args.color_enhance is not None,
        args.sharp_enhance is not None,
        args.face_enhance is not None,
        args.lowlight_enhance,
    ])
    if not has_enhance:
        return None

    config = {}

    # Super-resolution
    if args.super_resolution:
        sr_config = {
            "Switch": "ON",
            "Type": args.sr_type or "lq",
            "Size": 2,
        }
        config["SuperResolution"] = sr_config

    # Advanced super-resolution
    if args.advanced_sr:
        adv_sr = {
            "Switch": "ON",
            "Type": args.adv_sr_type or "standard",
        }
        if args.sr_percent is not None:
            adv_sr["Mode"] = "percent"
            adv_sr["Percent"] = args.sr_percent
        elif args.sr_width is not None or args.sr_height is not None:
            if args.sr_width and args.sr_height:
                adv_sr["Mode"] = args.sr_mode or "aspect"
                adv_sr["Width"] = args.sr_width
                adv_sr["Height"] = args.sr_height
            elif args.sr_long_side or args.sr_short_side:
                adv_sr["Mode"] = args.sr_mode or "aspect"
                if args.sr_long_side:
                    adv_sr["LongSide"] = args.sr_long_side
                if args.sr_short_side:
                    adv_sr["ShortSide"] = args.sr_short_side
            else:
                adv_sr["Mode"] = args.sr_mode or "aspect"
                if args.sr_width:
                    adv_sr["Width"] = args.sr_width
                if args.sr_height:
                    adv_sr["Height"] = args.sr_height
        else:
            adv_sr["Mode"] = "percent"
            adv_sr["Percent"] = 2.0
        config["AdvancedSuperResolutionConfig"] = adv_sr

    # Denoising
    if args.denoise is not None:
        config["Denoise"] = {
            "Switch": "ON",
            "Type": args.denoise,
        }

    # Comprehensive enhancement
    if args.quality_enhance is not None:
        config["ImageQualityEnhance"] = {
            "Switch": "ON",
            "Type": args.quality_enhance,
        }

    # Color enhancement
    if args.color_enhance is not None:
        config["ColorEnhance"] = {
            "Switch": "ON",
            "Type": args.color_enhance,
        }

    # Detail enhancement
    if args.sharp_enhance is not None:
        config["SharpEnhance"] = {
            "Switch": "ON",
            "Intensity": args.sharp_enhance,
        }

    # Face enhancement
    if args.face_enhance is not None:
        config["FaceEnhance"] = {
            "Switch": "ON",
            "Intensity": args.face_enhance,
        }

    # Low-light enhancement
    if args.lowlight_enhance:
        config["LowLightEnhance"] = {
            "Switch": "ON",
            "Type": "normal",
        }

    return config


# =============================================================================
# Image erasure configuration building
# =============================================================================
def parse_erase_area(area_str, area_type="pixel"):
    """
    Parse erasure area string.

    pixel format: x1,y1,x2,y2 (pixel coordinates)
    ratio format: x1,y1,x2,y2 (percentage coordinates)
    """
    parts = area_str.split(",")
    if len(parts) != 4:
        print(f"Error: Erasure area format incorrect '{area_str}', should be x1,y1,x2,y2", file=sys.stderr)
        sys.exit(1)

    try:
        coords = [float(p) for p in parts]
    except ValueError:
        print(f"Error: Erasure area coordinates must be numbers '{area_str}'", file=sys.stderr)
        sys.exit(1)

    area = {}
    if area_type == "pixel":
        area["AreaCoordSet"] = [int(c) for c in coords]
    else:
        area["BoundingBox"] = coords
        area["BoundingBoxUnitType"] = 1  # Percentage unit
    return area


def build_erase_config(args):
    """Build image erasure configuration (EraseConfig) — erase icons/text/watermarks."""
    has_erase = any([
        args.erase_detect,
        args.erase_area,
        args.erase_box,
    ])
    if not has_erase:
        return None

    erase_logo = {"Switch": "ON"}

    # Specify erasure area
    area_boxes = []

    # Pixel coordinate area
    if args.erase_area:
        for area_str in args.erase_area:
            area = parse_erase_area(area_str, "pixel")
            area["Type"] = args.erase_area_type or "logo"
            area_boxes.append(area)

    # Percentage coordinate area
    if args.erase_box:
        for box_str in args.erase_box:
            area = parse_erase_area(box_str, "ratio")
            area["Type"] = args.erase_area_type or "logo"
            area_boxes.append(area)

    if area_boxes:
        erase_logo["ImageAreaBoxes"] = area_boxes

    # Auto-detection types
    if args.erase_detect:
        erase_logo["DetectTypes"] = args.erase_detect

    return {"ImageEraseLogo": erase_logo}


# =============================================================================
# Blind Watermark Configuration Building
# =============================================================================
def build_blind_watermark_config(args):
    """Build blind watermark configuration (BlindWatermarkConfig) - add/extract/remove blind watermark."""
    has_watermark = any([
        args.add_watermark is not None,
        args.extract_watermark,
        args.remove_watermark,
    ])
    if not has_watermark:
        return None

    config = {}

    # Add blind watermark
    if args.add_watermark is not None:
        raw_bytes = args.add_watermark.encode("utf-8")
        # Give reminder when exceeding 4 bytes
        if len(raw_bytes) > 4:
            truncated = raw_bytes[:4].decode("utf-8", errors="replace")
            print(
                f"⚠️  Blind watermark text '{args.add_watermark}' UTF-8 encoding exceeds 4 bytes (total {len(raw_bytes)} bytes), "  # NOCA:line-too-long(line cannot be shortened)
                f"will be truncated to first 4 bytes (actually embedded: '{truncated}')",
                file=sys.stderr,
            )
        # Take first 4 bytes; pad with 0x00 if less than 4 bytes
        text_bytes = raw_bytes[:4].ljust(4, b'\x00')
        embed_text = base64.b64encode(text_bytes).decode("utf-8")

        config["AddBlindWatermark"] = {
            "Switch": "ON",
            "EmbedInfo": {
                "EmbedText": embed_text,
            }
        }

    # Extract blind watermark
    if args.extract_watermark:
        config["ExtractBlindWatermark"] = {"Switch": "ON"}

    # Remove blind watermark
    if args.remove_watermark:
        config["RemoveBlindWatermark"] = {"Switch": "ON"}

    return config


# =============================================================================
# Beauty Configuration Building
# =============================================================================
def parse_beauty_item(beauty_str):
    """
    Parse beauty effect string.

    Format: Type:Value or Type:Value:Color
    Example: Whiten:50 or FaceFeatureLipsLut:50:#ff0000
    """
    parts = beauty_str.split(":")
    if len(parts) < 2:
        print(f"Error: Beauty effect format incorrect '{beauty_str}', should be Type:Value (e.g., Whiten:50)", file=sys.stderr)  # NOCA:line-too-long(content cannot be shortened)
        sys.exit(1)

    effect_type = parts[0]
    if effect_type not in BEAUTY_EFFECT_TYPES:
        valid_types = ", ".join(BEAUTY_EFFECT_TYPES.keys())
        print(f"Error: Unsupported beauty effect '{effect_type}'. Supported types: {valid_types}", file=sys.stderr)
        sys.exit(1)

    try:
        value = int(parts[1])
    except ValueError:
        print(f"Error: Beauty effect strength must be integer '{parts[1]}'", file=sys.stderr)
        sys.exit(1)

    if value < 0 or value > 100:
        print(f"Error: Beauty effect strength range [0, 100], current is {value}", file=sys.stderr)
        sys.exit(1)

    item = {
        "Type": effect_type,
        "Switch": "ON",
        "Value": value,
    }

    # Optional color parameter (e.g., lipstick color)
    if len(parts) >= 3:
        color = parts[2]
        item["ExtInfo"] = json.dumps({"Color": color})

    return item


def parse_filter_item(filter_str):
    """
    Parse filter effect string.

    Format: Type:Value
    Example: Qingjiaopian:70
    """
    parts = filter_str.split(":")
    if len(parts) < 2:
        print(f"Error: Filter format incorrect '{filter_str}', should be Type:Value (e.g., Qingjiaopian:70)", file=sys.stderr)  # NOCA:line-too-long(line cannot be shortened)
        sys.exit(1)

    filter_type = parts[0]
    if filter_type not in FILTER_TYPES:
        valid_types = ", ".join(f"{k}({v})" for k, v in FILTER_TYPES.items())
        print(f"Error: Unsupported filter type '{filter_type}'. Supported types: {valid_types}", file=sys.stderr)
        sys.exit(1)

    try:
        value = int(parts[1])
    except ValueError:
        print(f"Error: Filter strength must be integer '{parts[1]}'", file=sys.stderr)
        sys.exit(1)

    if value < -100 or value > 100:
        print(f"Error: Filter strength range [-100, 100], current is {value}", file=sys.stderr)
        sys.exit(1)

    return {
        "Type": filter_type,
        "Switch": "ON",
        "Value": value,
    }


def build_beauty_config(args):
    """Build beauty configuration (BeautyConfig) - beauty effects and filters."""
    has_beauty = any([
        args.beauty,
        args.filter,
    ])
    if not has_beauty:
        return None

    config = {}

    # Beauty effects
    if args.beauty:
        effect_items = []
        for beauty_str in args.beauty:
            effect_items.append(parse_beauty_item(beauty_str))
        config["BeautyEffectItems"] = effect_items

    # Filters
    if args.filter:
        filter_items = []
        for filter_str in args.filter:
            filter_items.append(parse_filter_item(filter_str))
        config["BeautyFilterItems"] = filter_items

    return config


# =============================================================================
# Image Scaling Configuration Building
# =============================================================================
def build_transform_config(args):
    """Build image basic transformation configuration (TransformConfig) - scaling."""
    has_transform = any([
        args.resize_percent is not None,
        args.resize_mode is not None,
        args.resize_width is not None,
        args.resize_height is not None,
        args.resize_long_side is not None,
        args.resize_short_side is not None,
    ])
    if not has_transform:
        return None

    resize = {"Switch": "ON"}

    if args.resize_percent is not None:
        resize["Mode"] = "percent"
        resize["Percent"] = args.resize_percent
    elif args.resize_mode:
        resize["Mode"] = args.resize_mode
        if args.resize_width:
            resize["Width"] = args.resize_width
        if args.resize_height:
            resize["Height"] = args.resize_height
        if args.resize_long_side:
            resize["LongSide"] = args.resize_long_side
        if args.resize_short_side:
            resize["ShortSide"] = args.resize_short_side
    else:
        # Only width/height specified without mode, default lfit
        resize["Mode"] = "lfit"
        if args.resize_width:
            resize["Width"] = args.resize_width
        if args.resize_height:
            resize["Height"] = args.resize_height
        if args.resize_long_side:
            resize["LongSide"] = args.resize_long_side
        if args.resize_short_side:
            resize["ShortSide"] = args.resize_short_side

    return {"ImageResize": resize}


# =============================================================================
# Image Task Building
# =============================================================================
def build_image_task(args):
    """
    Build image processing parameters (ImageTask).

    Combine all image processing sub-configurations into ImageTask.
    """
    task = {}

    # 1. Image encoding configuration
    encode_config = build_encode_config(args)
    if encode_config:
        task["EncodeConfig"] = encode_config

    # 2. Image enhancement configuration
    enhance_config = build_enhance_config(args)
    if enhance_config:
        task["EnhanceConfig"] = enhance_config

    # 3. Image erasure configuration
    erase_config = build_erase_config(args)
    if erase_config:
        task["EraseConfig"] = erase_config

    # 4. Blind watermark configuration
    watermark_config = build_blind_watermark_config(args)
    if watermark_config:
        task["BlindWatermarkConfig"] = watermark_config

    # 5. Beauty configuration
    beauty_config = build_beauty_config(args)
    if beauty_config:
        task["BeautyConfig"] = beauty_config

    # 6. Image scaling configuration
    transform_config = build_transform_config(args)
    if transform_config:
        task["TransformConfig"] = transform_config

    return task if task else None


# =============================================================================
# Request Parameters Building
# =============================================================================
def build_request_params(args):
    """Build complete ProcessImage request parameters."""
    params = {}

    # Input
    params["InputInfo"] = build_input_info(args)

    # Output storage
    output_storage = build_output_storage(args)
    if output_storage:
        params["OutputStorage"] = output_storage

    # Output directory (default /output/image/ when not specified)
    output_dir = args.output_dir or "/output/image/"
    params["OutputDir"] = output_dir

    # Output path
    if args.output_path:
        params["OutputPath"] = args.output_path

    # Image processing parameters
    image_task = build_image_task(args)
    if image_task:
        params["ImageTask"] = image_task

    # Image processing template (optional)
    if args.definition:
        params["Definition"] = args.definition

    # Resource ID (optional)
    if args.resource_id:
        params["ResourceId"] = args.resource_id


    # Orchestration scene ID (optional)
    if args.schedule_id:
        params["ScheduleId"] = args.schedule_id

    return params
# =============================================================================
# Configuration Summary
# =============================================================================


def get_task_summary(args):
    """Generate image processing configuration summary text."""
    items = []

    # Encoding configuration
    if args.format or args.quality is not None:
        fmt = args.format or "Original format"
        quality = f"Quality {args.quality}" if args.quality is not None else "Original quality"
        items.append(f"🖼️  Encoding configuration: Format={fmt}, {quality}")

    # Enhancement configuration
    if args.super_resolution:
        sr_type = args.sr_type or "lq"
        items.append(f"🔍 Super-resolution: 2x upscaling (type: {sr_type})")

    if args.advanced_sr:
        adv_type = args.adv_sr_type or "standard"
        if args.sr_percent is not None:
            items.append(f"🔍 Advanced super-resolution: {args.sr_percent}x upscaling (type: {adv_type})")
        elif args.sr_width or args.sr_height:
            w = args.sr_width or "Adaptive"
            h = args.sr_height or "Adaptive"
            items.append(f"🔍 Advanced super-resolution: Target {w}x{h} (type: {adv_type})")
        else:
            items.append(f"🔍 Advanced super-resolution: 2x upscaling (type: {adv_type})")

    if args.denoise:
        items.append(f"🔇 Denoising: {args.denoise}")

    if args.quality_enhance:
        items.append(f"✨ Comprehensive enhancement: {args.quality_enhance}")

    if args.color_enhance:
        items.append(f"🎨 Color enhancement: {args.color_enhance}")

    if args.sharp_enhance is not None:
        items.append(f"🔬 Detail enhancement: Intensity {args.sharp_enhance}")

    if args.face_enhance is not None:
        items.append(f"👤 Face enhancement: Intensity {args.face_enhance}")

    if args.lowlight_enhance:
        items.append("🌙 Low-light enhancement: Enabled")

    # Erasure configuration
    if args.erase_detect:
        items.append(f"🧹 Automatic detection erasure: {', '.join(args.erase_detect)}")
    if args.erase_area:
        items.append(f"🧹 Specified area erasure (pixels): {len(args.erase_area)} areas")
    if args.erase_box:
        items.append(f"🧹 Specified area erasure (percentage): {len(args.erase_box)} areas")

    # Blind watermark
    if args.add_watermark is not None:
        items.append(f"💧 Add blind watermark: '{args.add_watermark}'")
    if args.extract_watermark:
        items.append("💧 Extract blind watermark: Enabled")
    if args.remove_watermark:
        items.append("💧 Remove blind watermark: Enabled")

    # Beauty enhancement
    if args.beauty:
        for beauty_str in args.beauty:
            parts = beauty_str.split(":")
            effect_type = parts[0]
            value = parts[1] if len(parts) > 1 else "Default"
            desc = BEAUTY_EFFECT_TYPES.get(effect_type, effect_type)
            items.append(f"💄 Beauty effect: {desc}({effect_type}) Intensity={value}")

    # Filter
    if args.filter:
        for filter_str in args.filter:
            parts = filter_str.split(":")
            filter_type = parts[0]
            value = parts[1] if len(parts) > 1 else "Default"
            desc = FILTER_TYPES.get(filter_type, filter_type)
            items.append(f"🎬 Filter: {desc}({filter_type}) Intensity={value}")

    # Scaling
    if args.resize_percent is not None:
        items.append(f"📐 Scaling: {args.resize_percent}x")
    elif args.resize_mode:
        mode_desc = RESIZE_MODES.get(args.resize_mode, args.resize_mode)
        w = args.resize_width or "Adaptive"
        h = args.resize_height or "Adaptive"
        items.append(f"📐 Scaling: {mode_desc}({args.resize_mode}) → {w}x{h}")
    elif args.resize_width or args.resize_height:
        w = args.resize_width or "Adaptive"
        h = args.resize_height or "Adaptive"
        items.append(f"📐 Scaling: Proportional scaling → {w}x{h}")

    return items


def _get_input_url(args):
    """Get the URL of the input source from arguments (for comparison page)."""
    if getattr(args, 'url', None):
        return args.url
    cos_key = getattr(args, 'cos_input_key', None)
    if cos_key:
        bucket = getattr(args, 'cos_input_bucket', None) or get_cos_bucket()
        region = getattr(args, 'cos_input_region', None) or get_cos_region()
        if bucket:
            return f"https://{bucket}.cos.{region}.myqcloud.com/{cos_key.lstrip('/')}"
    return ""


# =============================================================================
# Main Process
# =============================================================================
def process_image(args):
    """Initiate image processing task."""
    region = args.region or os.environ.get("TENCENTCLOUD_API_REGION", "")

    # 1. Get credentials and client
    cred = get_credentials()
    client = create_mps_client(cred, region)

    # 2. Build request
    params = build_request_params(args)

    if args.dry_run:
        print("=" * 60)
        print("[Dry Run Mode]Only printing request parameters, not actually calling API")
        print("=" * 60)
        print(json.dumps(params, ensure_ascii=False, indent=2))
        return

    # Print request parameters (for debugging)
    if args.verbose:
        print("Request parameters:")
        print(json.dumps(params, ensure_ascii=False, indent=2))
        print()

    # 3. Initiate call
    try:
        req = models.ProcessImageRequest()
        req.from_json_string(json.dumps(params))

        resp = client.ProcessImage(req)
        result = json.loads(resp.to_json_string())

        task_id = result.get('TaskId', 'N/A')
        print("✅ Image processing task submitted successfully!")
        print(f"   TaskId: {task_id}")
        print(f"\n## TaskId: {task_id}")
        print(f"   RequestId: {result.get('RequestId', 'N/A')}")

        summary = get_task_summary(args)
        if summary:
            print("   Processing details:")
            for item in summary:
                print(f"     {item}")
        else:
            if args.definition:
                print(f"   Template: Preset template {args.definition}")
            elif args.schedule_id:
                preset_name = SCHEDULE_PRESETS.get(args.schedule_id)
                if preset_name:
                    print(f"   Orchestration Scenario: {args.schedule_id} ({preset_name})")
                else:
                    print(f"   Orchestration Scenario: {args.schedule_id}")
            else:
                print("   Mode: Direct processing (no processing parameters specified)")

        if args.verbose:
            print("\nComplete response:")
            print(json.dumps(result, ensure_ascii=False, indent=2))

        # Automatic polling (unless --no-wait is specified)
        no_wait = getattr(args, 'no_wait', False)
        if not no_wait and _POLL_AVAILABLE and task_id != 'N/A':
            poll_interval = getattr(args, 'poll_interval', 5)
            max_wait = getattr(args, 'max_wait', 300)
            task_result = poll_image_task(task_id, region=region, interval=poll_interval,
                            max_wait=max_wait, verbose=args.verbose)
            # Auto-download results
            download_dir = getattr(args, 'download_dir', None)
            if download_dir and task_result and _POLL_AVAILABLE:
                auto_download_outputs(task_result, download_dir=download_dir)
            # Auto-generate comparison page
            compare_opt = getattr(args, 'compare', None)
            if compare_opt and task_result and _POLL_AVAILABLE:
                input_url = _get_input_url(args)
                compare_path = None if compare_opt == "auto" else compare_opt
                auto_gen_compare(task_result, input_url, media_type="image",
                                 title="Image Processing Effect Comparison", output_path=compare_path)
        else:
            print(f"\nNote: Task is processing in background, use the following command to check progress:")
            print(f"  python scripts/mps_get_image_task.py --task-id {task_id}")

        return result

    except TencentCloudSDKException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS Image Processing — Supports rich capabilities including image enhancement, denoising, super-resolution, beautification & filters",  # NOCA:line-too-long(content cannot be shortened)
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # === Input Methods ===
  # URL input
  python mps_imageprocess.py --url https://example.com/image.jpg --format PNG

  # COS path input (recommended, use after local upload)
  python mps_imageprocess.py --cos-input-bucket mybucket-125xxx --cos-input-region ap-guangzhou --cos-input-key
  /input/image.jpg --format PNG

  # COS input (bucket and region automatically obtained from environment variables)
  python mps_imageprocess.py --cos-input-key /input/image/test.jpg --format PNG

  # === Format Conversion ===
  python mps_imageprocess.py --url https://example.com/image.jpg --format PNG
  python mps_imageprocess.py --url https://example.com/image.jpg --format WebP --quality 80

  # === Image Enhancement ===
  # Super-resolution (2x magnification)
  python mps_imageprocess.py --url https://example.com/image.jpg --super-resolution

  # Advanced super-resolution (specify target dimensions)
  python mps_imageprocess.py --url https://example.com/image.jpg --advanced-sr --sr-width 3840 --sr-height 2160
  # Advanced super-resolution (magnification mode)
  python mps_imageprocess.py --url https://example.com/image.jpg --advanced-sr --sr-percent 3.0

  # Denoise + Color enhancement
  python mps_imageprocess.py --url https://example.com/image.jpg --denoise strong --color-enhance normal

  # Low-light enhancement
  python mps_imageprocess.py --url https://example.com/image.jpg --lowlight-enhance

  # === Image Erasure ===
  # Auto-detect and erase icons and text
  python mps_imageprocess.py --url https://example.com/image.jpg --erase-detect logo text

  # Auto-detect and erase watermarks
  python mps_imageprocess.py --url https://example.com/image.jpg --erase-detect watermark

  # Specify area to erase (pixel coordinates)
  python mps_imageprocess.py --url https://example.com/image.jpg --erase-area 100,50,300,200

  # Specify area to erase (percentage coordinates)
  python mps_imageprocess.py --url https://example.com/image.jpg --erase-box 0.1,0.1,0.3,0.3

  # === Blind Watermark ===
  python mps_imageprocess.py --url https://example.com/image.jpg --add-watermark "test"
  python mps_imageprocess.py --url https://example.com/image.jpg --extract-watermark
  python mps_imageprocess.py --url https://example.com/image.jpg --remove-watermark

  # === Beautification ===
  python mps_imageprocess.py --url https://example.com/image.jpg --beauty Whiten:50
  python mps_imageprocess.py --url https://example.com/image.jpg --beauty Smooth:60 --beauty BeautyThinFace:40
  python mps_imageprocess.py --url https://example.com/image.jpg --beauty 'FaceFeatureLipsLut:50:#ff0000'

  # === Filters ===
  python mps_imageprocess.py --url https://example.com/image.jpg --filter Qingjiaopian:70

  # === Scaling ===
  python mps_imageprocess.py --url https://example.com/image.jpg --resize-percent 2.0
  python mps_imageprocess.py --url https://example.com/image.jpg --resize-mode lfit --resize-width 800 --resize-height
  600

  # === Combined Usage ===
  python mps_imageprocess.py --url https://example.com/image.jpg \\
      --denoise weak --super-resolution --beauty Whiten:30 --format PNG

  # === Orchestration Scenarios (ScheduleId, console preset capabilities) ===
  # AI Image Understanding / AI Cutout / AI Image Restoration / AI Foreground Extraction / AI Outpainting / AI Text Watermark Erasure
  python mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30200
  python mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30030
  python mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30040
  python mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30031
  python mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30010
  python mps_imageprocess.py --url https://example.com/image.jpg --schedule-id 30000

  # Dry Run (only print request parameters)
  python mps_imageprocess.py --url https://example.com/image.jpg --super-resolution --dry-run

Processing Capabilities:
  1. Image Encoding   Format conversion (JPEG/PNG/BMP/WebP), quality adjustment
  2. Image Enhancement   Super-resolution, advanced super-resolution, denoising, comprehensive enhancement, color
  enhancement, detail enhancement, face enhancement, low-light enhancement
  3. Image Erasure   Erase icons/text/watermarks (supports auto-detection and specified areas)
  4. Blind Watermark   Add/extract/remove blind watermarks (text embedding)
  5. Beautification   20+ beautification effects (whitening/skin smoothing/face slimming/enlarged eyes/lipstick/makeup
  etc.)
  6. Filters   Tokyo/Light Film/Delicious style filters
  7. Image Scaling   Percentage scaling, proportional scaling, fixed dimensions, cropping & padding

Orchestration Scenarios (--schedule-id, console preset AI capabilities):
  30000  AI Text Watermark Erasure
  30010  AI Outpainting (Image Extension)
  30030  AI Cutout
  30031  AI Foreground Extraction
  30040  AI Image Restoration
  30200  AI Image Understanding
  (For outfit change use mps_image_tryon.py; for background fusion use mps_image_bg_fusion.py)

Beautification Effect Types (--beauty Type:Value):
  Whiten=Whitening  BlackAlpha1=Darkening  BlackAlpha2=Strong Darkening  FoundationAlpha2=Pink White
  Clear=Clarity  Sharpen=Sharpening  Smooth=Skin Smoothing
  BeautyThinFace=Facial Slimming  NatureFace=Natural Face Shape  VFace=V-Shaped Face
  EnlargeEye=Enlarged Eyes  EyeLighten=Eye Brightening  RemoveEyeBags=Remove Eye Bags
  ThinNose=Nose Slimming  RemoveLawLine=Remove Nasolabial Folds  CheekboneThin=Cheekbone Slimming
  FaceFeatureLipsLut=Lipstick  ToothWhiten=Teeth Whitening
  FaceFeatureSoftlight=Soft Light  Makeup=Makeup

Filter Types (--filter Type:Value):
  Dongjing=Tokyo  Qingjiaopian=Light Film  Meiwei=Delicious

Scaling Modes (--resize-mode):
  percent=Percentage scaling  mfit=Proportional scaling to larger rectangle  lfit=Proportional scaling to smaller
  rectangle
  fill=Proportional scaling + center cropping  pad=Proportional scaling + padding  fixed=Fixed width/height forced
  scaling

Environment Variables:
  TENCENTCLOUD_SECRET_ID   Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET       COS Bucket name (e.g., mybucket-125xxx)
  TENCENTCLOUD_COS_REGION       COS Bucket region (default ap-guangzhou)
        """
    )
    # ---- Input Source ----
    input_group = parser.add_argument_group("Input Source (choose one)")
    input_group.add_argument("--local-file", type=str,
                             help="Local file path, automatically uploaded to COS for processing (requires TENCENTCLOUD_COS_BUCKET configuration)")  # NOCA:line-too-long(line cannot be shortened)
    input_group.add_argument("--url", type=str, help="Image URL address")

    # COS path input (new version, recommended) - for direct use of COS paths after local upload
    input_group.add_argument("--cos-input-bucket", type=str,
                             help="Input COS Bucket name (use with --cos-input-region/--cos-input-key)")
    input_group.add_argument("--cos-input-region", type=str,
                             help="Input COS Bucket region (e.g., ap-guangzhou)")
    input_group.add_argument("--cos-input-key", type=str,
                             help="Input COS object Key (e.g., /input/image.jpg)")


    # ---- Output ----
    output_group = parser.add_argument_group("Output Configuration (optional)")
    output_group.add_argument("--output-bucket", type=str,
                              help="Output COS Bucket name (default: TENCENTCLOUD_COS_BUCKET environment variable)")
    output_group.add_argument("--output-region", type=str,
                              help="Output COS Bucket region (default: TENCENTCLOUD_COS_REGION environment variable)")
    output_group.add_argument("--output-dir", type=str,
                              help="Output directory, starting and ending with / (e.g., /output/)")
    output_group.add_argument("--output-path", type=str,
                              help="Output file path (e.g., /output/{inputName}.{format})")

    # ---- Image Encoding (Format Conversion) ----
    encode_group = parser.add_argument_group("Image Encoding Configuration (Format Conversion)")
    encode_group.add_argument("--format", type=str, choices=["JPEG", "PNG", "BMP", "WebP"],
                              help="Output image format (default: keep original format)")
    encode_group.add_argument("--quality", type=int,
                              help="Image quality [1-100] (default: keep original quality)")

    # ---- Image Enhancement ----
    enhance_group = parser.add_argument_group("Image Enhancement Configuration")
    enhance_group.add_argument("--super-resolution", action="store_true",
                               help="Enable super-resolution (2x magnification)")
    enhance_group.add_argument("--sr-type", type=str, choices=["lq", "hq"],
                               help="Super-resolution type: lq=for low-quality with noise (default) | hq=for high-quality")  # NOCA:line-too-long(line cannot be shortened)
    enhance_group.add_argument("--advanced-sr", action="store_true",
                               help="Enable advanced super-resolution")
    enhance_group.add_argument("--adv-sr-type", type=str, choices=["standard", "super", "ultra"],
                               help="Advanced super-resolution type: standard=general (default) | super=advanced super | ultra=advanced ultra")  # NOCA:line-too-long(line cannot be shortened)
    enhance_group.add_argument("--sr-mode", type=str, choices=["percent", "aspect", "fixed"],
                               help="Advanced super-resolution output mode: percent=magnification | aspect=proportional (default) | fixed=fixed")  # NOCA:line-too-long(line cannot be shortened)
    enhance_group.add_argument("--sr-percent", type=float,
                               help="Advanced super-resolution magnification (with --sr-mode percent, e.g., 2.0 means 2x)")  # NOCA:line-too-long(line cannot be shortened)
    enhance_group.add_argument("--sr-width", type=int,
                               help="Advanced super-resolution target width (not exceeding 4096)")
    enhance_group.add_argument("--sr-height", type=int,
                               help="Advanced super-resolution target height (not exceeding 4096)")
    enhance_group.add_argument("--sr-long-side", type=int,
                               help="Advanced super-resolution target long side (not exceeding 4096)")
    enhance_group.add_argument("--sr-short-side", type=int,
                               help="Advanced super-resolution target short side (not exceeding 4096)")

    enhance_group.add_argument("--denoise", type=str, choices=["weak", "strong"],
                               help="Denoising: weak=mild denoising | strong=strong denoising")
    enhance_group.add_argument("--quality-enhance", type=str, choices=["weak", "normal", "strong"],
                               help="Comprehensive enhancement: weak=mild | normal=moderate | strong=strong")
    enhance_group.add_argument("--color-enhance", type=str, choices=["weak", "normal", "strong"],
                               help="Color enhancement: weak=mild | normal=moderate | strong=strong")
    enhance_group.add_argument("--sharp-enhance", type=float,
                               help="Detail enhancement strength [0.0-1.0]")
    enhance_group.add_argument("--face-enhance", type=float,
                               help="Face enhancement strength [0.0-1.0]")
    enhance_group.add_argument("--lowlight-enhance", action="store_true",
                               help="Enable low-light enhancement")

    # ---- Image Erasure ----
    erase_group = parser.add_argument_group("Image Erasure Configuration")
    erase_group.add_argument("--erase-detect", type=str, nargs="+",
                             choices=["logo", "text", "watermark"],
                             help="Auto-detect and erase types: logo=icons | text=text | watermark=watermarks (multiple selections allowed)")  # NOCA:line-too-long(line cannot be shortened)
    erase_group.add_argument("--erase-area", type=str, action="append", metavar="X1,Y1,X2,Y2",
                             help="Specify erasure area (pixel coordinates). Format: x1,y1,x2,y2. Can be specified multiple times")  # NOCA:line-too-long(line cannot be shortened)
    erase_group.add_argument("--erase-box", type=str, action="append", metavar="X1,Y1,X2,Y2",
                             help="Specify erasure area (percentage coordinates 0~1). Format: x1,y1,x2,y2. Can be specified multiple times")  # NOCA:line-too-long(line cannot be shortened)
    erase_group.add_argument("--erase-area-type", type=str, choices=["logo", "text"],
                             help="Specified area erasure type: logo=icons (default) | text=text")

    # ---- Blind Watermark ----
    watermark_group = parser.add_argument_group("Blind Watermark Configuration")
    watermark_group.add_argument("--add-watermark", type=str, metavar="TEXT",
                                 help="Add blind watermark (text, up to 4 bytes)")
    watermark_group.add_argument("--extract-watermark", action="store_true",
                                 help="Extract blind watermark")
    watermark_group.add_argument("--remove-watermark", action="store_true",
                                 help="Remove blind watermark")

    # ---- Beautification ----
    beauty_group = parser.add_argument_group("Beautification Configuration")
    beauty_group.add_argument("--beauty", type=str, action="append", metavar="TYPE:VALUE",
                              help="Beautification effect. Format: Type:Value (e.g., Whiten:50)."
                                   "Lipstick can include color: FaceFeatureLipsLut:50:#ff0000."
                                   "Can be specified multiple times for cumulative effects. Strength range [0-100]")

    # ---- Filters ----
    filter_group = parser.add_argument_group("Filter Configuration")
    filter_group.add_argument("--filter", type=str, action="append", metavar="TYPE:VALUE",
                              help="Filter effect. Format: Type:Value (e.g., Qingjiaopian:70)."
                                   "Types: Dongjing=Tokyo | Qingjiaopian=Light Film | Meiwei=Delicious."
                                   "Strength range [-100, 100]")

    # ---- Image Scaling ----
    resize_group = parser.add_argument_group("Image Scaling Configuration")
    resize_group.add_argument("--resize-percent", type=float,
                              help="Percentage scaling factor [0.1-10.0] (e.g., 2.0 means 2x magnification)")
    resize_group.add_argument("--resize-mode", type=str,
                              choices=list(RESIZE_MODES.keys()),
                              help="Scaling mode: percent=percentage | mfit=proportional to larger rectangle | lfit=proportional to smaller rectangle | "  # NOCA:line-too-long(line cannot be shortened)
                                   "fill=proportional cropping | pad=proportional padding | fixed=fixed dimensions")
    resize_group.add_argument("--resize-width", type=int,
                              help="Target width [1-16384]")
    resize_group.add_argument("--resize-height", type=int,
                              help="Target height [1-16384]")
    resize_group.add_argument("--resize-long-side", type=int,
                              help="Target long side [1-16384] (used when width/height not specified)")
    resize_group.add_argument("--resize-short-side", type=int,
                              help="Target short side [1-16384] (used when width/height not specified)")

    # ---- Advanced Options ----
    advanced_group = parser.add_argument_group("Advanced Options")
    advanced_group.add_argument("--definition", type=int,
                                help="Image processing template ID (specify when using preset templates)")
    advanced_group.add_argument("--schedule-id", type=int,
                                help="Orchestration scenario ID: "
                                     "30000=AI Text Watermark Erasure | 30010=AI Outpainting | "
                                     "30030=AI Cutout | 30031=AI Foreground Extraction | "
                                     "30040=AI Image Restoration | 30200=AI Image Understanding. "
                                     "For outfit change use mps_image_tryon.py, for background fusion use mps_image_bg_fusion.py")  # NOCA:line-too-long(line cannot be shortened)
    advanced_group.add_argument("--resource-id", type=str,
                                help="Resource ID (default: account primary resource ID)")

    # ---- Other ----
    other_group = parser.add_argument_group("Other Configuration")
    other_group.add_argument("--region", type=str, help="MPS service region (default ap-guangzhou)")
    other_group.add_argument("--no-wait", action="store_true",
                             help="Only submit task, do not wait for result (default: automatically polls until completion)")  # NOCA:line-too-long(line cannot be shortened)
    other_group.add_argument("--poll-interval", type=int, default=5,
                             help="Polling interval (seconds), default 5")
    other_group.add_argument("--max-wait", type=int, default=300,
                             help="Maximum wait time (seconds), default 300 (5 minutes)")
    other_group.add_argument("--verbose", "-v", action="store_true", help="Output detailed information")
    other_group.add_argument("--dry-run", action="store_true", help="Only print request parameters, do not actually call API")  # NOCA:line-too-long(line cannot be shortened)
    other_group.add_argument("--download-dir", type=str, default=None,
                             help="Automatically download results to specified directory after task completion (default: no download; automatically downloads when path specified)")  # NOCA:line-too-long(line cannot be shortened)
    other_group.add_argument("--compare", nargs="?", const="auto", default=None, metavar="OUTPUT",
                             help="Automatically generate comparison HTML page after task completion (optionally specify output path, auto-generated by default)")  # NOCA:line-too-long(line cannot be shortened)

    args = parser.parse_args()
    # --url local path automatically converted to local upload mode
    if getattr(args, 'url', None) and not getattr(args, 'local_file', None):
        _val = args.url
        if not _val.startswith('http://') and not _val.startswith('https://'):
            print(f"Note: '{_val}' not specified as a source, defaulting to local file processing", file=sys.stderr)
            args.local_file = _val
            args.url = None

    # --local-file conflicts with COS input parameters
    if getattr(args, 'local_file', None):
        cos_conflicts = [x for x in [
            getattr(args, 'cos_input_bucket', None), getattr(args, 'cos_input_key', None)
        ] if x]
        if cos_conflicts:
            parser.error("--local-file cannot be used simultaneously with --cos-input-bucket / --cos-input-key")

    # Local file auto-upload
    if getattr(args, 'local_file', None):
        if not _POLL_AVAILABLE:
            print("Error: --local-file requires mps_poll_task module support", file=sys.stderr)
            sys.exit(1)
        upload_result = auto_upload_local_file(args.local_file)
        if not upload_result:
            sys.exit(1)
        args.cos_input_key = upload_result["Key"]
        args.cos_input_bucket = upload_result["Bucket"]
        args.cos_input_region = upload_result["Region"]

    has_url = bool(args.url)
    has_cos_path = bool(getattr(args, 'cos_input_key', None))

    if not has_url and not has_cos_path:
        parser.error("Please specify input source: --url or --cos-input-key (with --cos-input-bucket/--cos-input-region or environment variables)")  # NOCA:line-too-long(line cannot be shortened)

    # 2. Quality range
    if args.quality is not None and (args.quality < 1 or args.quality > 100):
        parser.error("--quality range is [1, 100]")

    # 3. Detail enhancement strength range
    if args.sharp_enhance is not None and (args.sharp_enhance < 0 or args.sharp_enhance > 1):
        parser.error("--sharp-enhance range is [0.0, 1.0]")

    # 4. Face enhancement strength range
    if args.face_enhance is not None and (args.face_enhance < 0 or args.face_enhance > 1):
        parser.error("--face-enhance range is [0.0, 1.0]")

    # 5. Scaling percentage range
    if args.resize_percent is not None and (args.resize_percent < 0.1 or args.resize_percent > 10):
        parser.error("--resize-percent range is [0.1, 10.0]")

    # 6. Super-resolution + Advanced super-resolution mutually exclusive
    if args.super_resolution and args.advanced_sr:
        parser.error("--super-resolution and --advanced-sr cannot be used simultaneously, please choose one")

    # 7. Blind watermark operations mutually exclusive
    watermark_count = sum([
        args.add_watermark is not None,
        args.extract_watermark,
        args.remove_watermark,
    ])
    if watermark_count > 1:
        parser.error("--add-watermark, --extract-watermark, --remove-watermark cannot be used simultaneously, please choose one")  # NOCA:line-too-long(line cannot be shortened)

    # Print environment variable information
    cos_bucket_env = get_cos_bucket()
    cos_region_env = get_cos_region()

    # Print execution information
    print("=" * 60)
    print("Tencent Cloud MPS Image Processing")
    print("=" * 60)
    if args.url:
        print(f"Input: URL - {args.url}")
    elif getattr(args, 'cos_input_bucket', None):
        # New version COS path input
        print(f"Input: COS - {args.cos_input_bucket}:{args.cos_input_key} (region: {args.cos_input_region})")
    else:
        bucket_display = getattr(args, 'cos_input_bucket', None) or cos_bucket_env or "Not set"
        region_display = getattr(args, 'cos_input_region', None) or cos_region_env
        print(f"Input: COS - {bucket_display}:{args.cos_input_key} (region: {region_display})")

    # Output information
    out_bucket = args.output_bucket or cos_bucket_env or "Not set"
    out_region = args.output_region or cos_region_env
    # Set output directory, default to /output/image/
    out_dir = args.output_dir or "/output/image/"
    print(f"Output: COS - {out_bucket}:{out_dir} (region: {out_region})")

    if cos_bucket_env:
        print(f"COS Bucket (environment variable): {cos_bucket_env}")
    else:
        print("❌ TENCENTCLOUD_COS_BUCKET not set. Please configure it before retrying.", file=sys.stderr)
        sys.exit(1)

    # Processing summary
    summary = get_task_summary(args)
    if summary:
        print("Processing Configuration:")
        for item in summary:
            print(f"  {item}")
    elif args.definition:
        print(f"Template: Preset template {args.definition}")
    elif args.schedule_id:
        preset_name = SCHEDULE_PRESETS.get(args.schedule_id)
        if preset_name:
            print(f"Orchestration Scenario: {args.schedule_id} ({preset_name})")
        else:
            print(f"Orchestration Scenario: {args.schedule_id}")
    else:
        print("⚠️  No processing parameters specified, image will not be processed")

    print("-" * 60)

    # Execute
    process_image(args)
if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
