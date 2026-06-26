

#!/usr/bin/env python3
"""
Tencent Cloud MPS Subtitle Removal Script

Features:
  Uses MPS intelligent erasure to automatically detect and seamlessly remove text
  in the lower-center region of a video — the top choice for TOP video dubbing
  and short drama overseas distribution!

  Wraps the "subtitle removal / watermark removal / face blur" API, defaulting to
  preset template 101 (subtitle removal — auto erase + standard model).
  If the user specifies additional parameters (aggressive erase, subtitle position
  adjustment, etc.), those are applied on top of the selected preset template.

  ⚠️ Important:
  By default, subtitles in the **lower-center region** of the video are detected.
  If subtitles are not fully removed, they may be located outside that region —
  use --area or --custom-area to specify the actual subtitle position.

  System preset templates (specified via --template):
    - 101  Subtitle removal (default)          — auto erase + standard model
    - 102  Subtitle removal + OCR extraction   — auto erase + standard model + OCR
    - 201  Watermark removal (advanced)        — advanced watermark erasure
    - 301  Face blur                           — auto-detect and blur faces
    - 302  Face and license plate blur         — auto-detect and blur faces and license plates

  Erase method (supported only by subtitle templates 101/102):
    - auto (auto erase, default): AI automatically detects and erases subtitles,
      default region is the lower-center area of the frame
    - custom (region erase): directly erases the specified region, suitable for
      scenes where subtitle position is fixed

  Erase model (supported only by subtitle templates 101/102):
    - standard (standard model, recommended): better detail-preserving erasure
    - area (area model): for stylized/shadowed/animated subtitles, erases a larger area

  Common area presets (specified via --position, percentage coordinates):
    - fullscreen   Full screen
    - top-half     Top half of screen
    - bottom-half  Bottom half of screen
    - center       Center of screen
    - left         Left side of screen
    - right        Right side of screen

COS Storage Conventions:
  Specify the COS bucket name via the TENCENTCLOUD_COS_BUCKET environment variable.
  - Default input path:  {TENCENTCLOUD_COS_BUCKET}/input/   (COS object key starts with /input/)
  - Default output path: {TENCENTCLOUD_COS_BUCKET}/output/erase/  (output directory is /output/erase/)

  When using COS input, bucket/region are automatically read from the
  TENCENTCLOUD_COS_BUCKET/TENCENTCLOUD_COS_REGION environment variables.
  When --output-bucket is not explicitly specified, TENCENTCLOUD_COS_BUCKET is used.
  When --output-dir is not explicitly specified, /output/erase/ is used.

Usage:
  # Simplest usage: URL input + default preset template 101 (auto erase lower-center subtitles)
  python mps_erase.py --url https://example.com/video.mp4

  # COS path input (recommended — upload locally first, then use)
  python mps_erase.py --cos-input-bucket mybucket-125xxx --cos-input-region ap-guangzhou --cos-input-key
  /input/video/test.mp4

  # COS input (bucket and region auto-read from environment variables)
  python mps_erase.py --cos-input-key /input/video/test.mp4

  # Subtitle removal + OCR extraction (template 102)
  python mps_erase.py --url https://example.com/video.mp4 --template 102

  # Watermark removal — advanced (template 201)
  python mps_erase.py --url https://example.com/video.mp4 --template 201

  # Face blur (template 301)
  python mps_erase.py --url https://example.com/video.mp4 --template 301

  # Face and license plate blur (template 302)
  python mps_erase.py --url https://example.com/video.mp4 --template 302

  # Aggressive erase mode (area model, larger erase area, for stylized/shadowed/animated subtitles)
  python mps_erase.py --url https://example.com/video.mp4 --model area

  # Subtitle in upper half of video (using position preset)
  python mps_erase.py --url https://example.com/video.mp4 --position top-half

  # Subtitle in lower half of video (using position preset)
  python mps_erase.py --url https://example.com/video.mp4 --position bottom-half

  # Subtitle on left side of video (vertical subtitle layout)
  python mps_erase.py --url https://example.com/video.mp4 --position left

  # Subtitle on right side of video (vertical subtitle layout)
  python mps_erase.py --url https://example.com/video.mp4 --position right

  # Subtitle at top of video (custom auto-erase region: top 0–25% of frame)
  python mps_erase.py --url https://example.com/video.mp4 --area 0,0,1,0.25

  # Multi-region erase (subtitles at both top and bottom)
  python mps_erase.py --url https://example.com/video.mp4 --area 0,0,1,0.15 --area 0,0.75,1,1

  # Region erase (fixed subtitle position — specify time range + region for direct erasure)
  python mps_erase.py --url https://example.com/video.mp4 \
      --method custom --custom-area 0,0,0,0.8,0.99,0.95

  # Time-range + region erase (erase bottom region within first 10 seconds)
  python mps_erase.py --url https://example.com/video.mp4 \
      --method custom --custom-area 0,10000,0,0.8,0.99,0.95

  # Subtitle removal + OCR subtitle extraction
  python mps_erase.py --url https://example.com/video.mp4 --ocr

  # Subtitle removal + OCR extraction + translate to English (short drama overseas distribution)
  python mps_erase.py --url https://example.com/video.mp4 --ocr --translate en

  # Subtitle removal + OCR extraction + translate to Japanese
  python mps_erase.py --url https://example.com/video.mp4 --ocr --translate ja

  # OCR recognition for multilingual subtitles
  python mps_erase.py --url https://example.com/video.mp4 --ocr --subtitle-lang multi

  # Output subtitle format as SRT
  python mps_erase.py --url https://example.com/video.mp4 --ocr --subtitle-format srt

  # Dry run (print request parameters only, do not call the API)
  python mps_erase.py --url https://example.com/video.mp4 --dry-run

Environment Variables:
  TENCENTCLOUD_SECRET_ID   - Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  - Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET       - COS bucket name (e.g. mybucket-125xxx, default: test_bucket)
  TENCENTCLOUD_COS_REGION       - COS bucket region (default: ap-guangzhou)
"""

import argparse
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
    from mps_poll_task import poll_video_task, auto_upload_local_file, auto_download_outputs
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
    print("Error: Please install the Tencent Cloud SDK first: pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# Preset template default parameters (subtitle removal — auto erase + standard model)
# =============================================================================
DEFAULT_TEMPLATE_ID = 101
PRESET_DEFAULTS = {
    "erase_method": "auto",       # Auto erase
    "model": "standard",          # Standard model
    "ocr_switch": "OFF",          # OCR disabled
    "trans_switch": "OFF",        # Translation disabled
}

# System preset template descriptions
PRESET_TEMPLATES = {
    101: "Subtitle removal (auto erase + standard model)",
    102: "Subtitle removal + OCR extraction (Chinese/English, VTT format)",
    201: "Watermark removal (advanced)",
    301: "Face blur",
    302: "Face and license plate blur",
}

# Only subtitle-type templates (101/102) support erase method/model/region/OCR parameters
SUBTITLE_TEMPLATES = {101, 102}

# Translation target language descriptions
TRANSLATE_LANGS = {
    "zh": "Simplified Chinese",
    "en": "English",
    "ja": "Japanese",
    "ko": "Korean",
    "fr": "French",
    "es": "Spanish",
    "it": "Italian",
    "de": "German",
    "tr": "Turkish",
    "ru": "Russian",
    "pt": "Portuguese",
    "vi": "Vietnamese",
    "id": "Indonesian",
    "ms": "Malay",
    "th": "Thai",
    "ar": "Arabic",
    "hi": "Hindi",
}

# Common area presets (percentage coordinates, Unit=1)
AREA_PRESETS = {
    "fullscreen":   {"desc": "Full screen",        "coords": {"LeftTopX": 0.0000, "LeftTopY": 0.0000, "RightBottomX": 0.9999, "RightBottomY": 0.9999}},  # NOCA:line-too-long(content cannot be shortened)
    "top-half":     {"desc": "Top half of screen", "coords": {"LeftTopX": 0.0000, "LeftTopY": 0.0000, "RightBottomX": 0.9999, "RightBottomY": 0.5000}},  # NOCA:line-too-long(line cannot be shortened)
    "bottom-half":  {"desc": "Bottom half of screen", "coords": {"LeftTopX": 0.0000, "LeftTopY": 0.5000, "RightBottomX": 0.9999, "RightBottomY": 0.9999}},  # NOCA:line-too-long(content cannot be shortened)
    "center":       {"desc": "Center of screen",   "coords": {"LeftTopX": 0.1000, "LeftTopY": 0.3000, "RightBottomX": 0.9000, "RightBottomY": 0.7000}},  # NOCA:line-too-long(line cannot be shortened)
    "left":         {"desc": "Left side of screen", "coords": {"LeftTopX": 0.0000, "LeftTopY": 0.0000, "RightBottomX": 0.5000, "RightBottomY": 0.9999}},  # NOCA:line-too-long(content cannot be shortened)
    "right":        {"desc": "Right side of screen", "coords": {"LeftTopX": 0.5000, "LeftTopY": 0.0000, "RightBottomX": 0.9999, "RightBottomY": 0.9999}},  # NOCA:line-too-long(line cannot be shortened)
}


def get_cos_bucket():
    """Get the COS bucket name from environment variables."""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """Get the COS bucket region from environment variables, defaulting to ap-guangzhou."""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


def get_credentials():
    """Get Tencent Cloud credentials from environment variables. """  # NOCA:line-too-long(content cannot be shortened)
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        print("❌ TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY not found", file=sys.stderr)
        print("   Please configure them in ~/.env or <SKILL_DIR>/.env", file=sys.stderr)
        if _LOAD_ENV_AVAILABLE:
            from mps_load_env import _print_setup_hint
            _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
        sys.exit(1)
        return {
            "Type": "COS",
            "CosInputInfo": {
                "Bucket": bucket,
                "Region": region,
                "Object": cos_input_key if cos_input_key.startswith("/") else f"/{cos_input_key}"
            }
        }

    print("Error: Please specify an input source:\n"
          "  - URL: --url <URL>\n"
          "  - COS path: --cos-input-key <key> (combined with environment variables or --cos-input-bucket/--cos-input-region)",  # NOCA:line-too-long(content cannot be shortened)
          file=sys.stderr)
    sys.exit(1)


def build_output_storage(args):
    """
    Build output storage information.

    Priority:
    1. Command-line arguments --output-bucket / --output-region
    2. Environment variables TENCENTCLOUD_COS_BUCKET / TENCENTCLOUD_COS_REGION
    """
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


def parse_area_string(area_str):
    """
    Parse an area string into an EraseArea object.

    Format: LeftTopX,LeftTopY,RightBottomX,RightBottomY
    Example: 0,0.7,1,1 represents the bottom 30% of the frame
    Coordinates are percentage values (0~1), using percentage units.
    """
    parts = area_str.split(",")
    if len(parts) != 4:
        print(f"Error: Invalid area format '{area_str}', expected LeftTopX,LeftTopY,RightBottomX,RightBottomY (e.g. 0,0.7,1,1)",  # NOCA:line-too-long(line cannot be shortened)
              file=sys.stderr)
        sys.exit(1)
    try:
        left_top_x = float(parts[0])
        left_top_y = float(parts[1])
        right_bottom_x = float(parts[2])
        right_bottom_y = float(parts[3])
    except ValueError:
        print(f"Error: Area coordinates must be numeric '{area_str}'", file=sys.stderr)
        sys.exit(1)

    # Validate range
    for val, name in [(left_top_x, "LeftTopX"), (left_top_y, "LeftTopY"),
                      (right_bottom_x, "RightBottomX"), (right_bottom_y, "RightBottomY")]:
        if val < 0 or val > 1:
            print(f"Error: {name} value {val} is out of range [0, 1]", file=sys.stderr)
            sys.exit(1)

    return {
        "LeftTopX": left_top_x,
        "LeftTopY": left_top_y,
        "RightBottomX": right_bottom_x,
        "RightBottomY": right_bottom_y,
        "Unit": 1,  # Percentage unit
    }


def parse_custom_area_string(area_str):
    """
    Parse a custom erase area string into an EraseTimeArea object.

    Format: BeginMs,EndMs,LeftTopX,LeftTopY,RightBottomX,RightBottomY
    Example: 0,0,0,0.8,0.99,0.95 represents the bottom area of the entire video (BeginMs=0,EndMs=0 means the full
    duration)
    Example: 0,10000,0,0.8,0.99,0.95 represents the bottom area of the first 10 seconds

    ⚠️ Note: The coordinate range for custom erase areas is [0, 1) (exclusive of 1),
    which differs from the auto erase area range of [0, 1].
    """
    parts = area_str.split(",")
    if len(parts) != 6:
        print(f"Error: Invalid custom area format '{area_str}', "
              f"expected BeginMs,EndMs,LeftTopX,LeftTopY,RightBottomX,RightBottomY (e.g. 0,0,0,0.8,0.99,0.95)",
              file=sys.stderr)
        sys.exit(1)
    try:
        begin_ms = int(parts[0])
        end_ms = int(parts[1])
        left_top_x = float(parts[2])
        left_top_y = float(parts[3])
        right_bottom_x = float(parts[4])
        right_bottom_y = float(parts[5])
    except ValueError:
        print(f"Error: Invalid custom area parameter format '{area_str}'", file=sys.stderr)
        sys.exit(1)

    # Validate range: custom erase area coordinates are in [0, 1) (exclusive of 1)
    for val, name in [(left_top_x, "LeftTopX"), (left_top_y, "LeftTopY"),
                      (right_bottom_x, "RightBottomX"), (right_bottom_y, "RightBottomY")]:
        if val < 0 or val >= 1:
            print(f"Error: {name} value {val} is out of the custom erase area coordinate range [0, 1) (exclusive of 1). "  # NOCA:line-too-long(line cannot be shortened)
                  f"Tip: To cover up to the frame edge, use 0.99 instead of 1", file=sys.stderr)
            sys.exit(1)

    return {
        "BeginMs": begin_ms,
        "EndMs": end_ms,
        "Areas": [{
            "LeftTopX": left_top_x,
            "LeftTopY": left_top_y,
            "RightBottomX": right_bottom_x,
            "RightBottomY": right_bottom_y,
            "Unit": 1,  # Percentage unit
        }],
    }


def get_template_id(args):
    """Get the actual template ID to use."""
    return getattr(args, 'template', None) or DEFAULT_TEMPLATE_ID


def has_custom_params(args):
    """Detect whether the user has passed any custom parameters (requiring override of the preset template)."""
    return any([
        args.method is not None,
        args.model is not None,
        args.ocr,
        args.subtitle_lang is not None,
        args.subtitle_format is not None,
        args.translate is not None,
        args.area is not None and len(args.area) > 0,
        args.custom_area is not None and len(args.custom_area) > 0,
        args.position is not None,
    ])


def build_erase_subtitle_config(args):
    """
    Build the subtitle erase configuration (SmartEraseSubtitleConfig / UpdateSmartEraseSubtitleConfig).

    Based on the default values of the preset template 101, overridden by user-supplied parameters.
    """
    config = {}

    # Erase method
    method = args.method or PRESET_DEFAULTS["erase_method"]
    config["SubtitleEraseMethod"] = method

    # Erase model
    model = args.model or PRESET_DEFAULTS["model"]
    config["SubtitleModel"] = model

    # OCR subtitle extraction
    if args.ocr:
        config["OcrSwitch"] = "ON"
        # Subtitle language
        config["SubtitleLang"] = args.subtitle_lang or "zh_en"
        # Subtitle format
        config["SubtitleFormat"] = args.subtitle_format or "vtt"
        # Subtitle translation
        if args.translate:
            config["TransSwitch"] = "ON"
            config["TransDstLang"] = args.translate
        else:
            config["TransSwitch"] = "OFF"
    else:
        config["OcrSwitch"] = PRESET_DEFAULTS["ocr_switch"]
        config["TransSwitch"] = PRESET_DEFAULTS["trans_switch"]

    # Auto erase custom areas (--area or --position)
    if method == "auto":
        areas = []

        # Prefer --position preset
        if args.position:
            preset = AREA_PRESETS.get(args.position)
            if preset:
                coords = preset["coords"]
                areas.append({
                    "LeftTopX": coords["LeftTopX"],
                    "LeftTopY": coords["LeftTopY"],
                    "RightBottomX": coords["RightBottomX"],
                    "RightBottomY": coords["RightBottomY"],
                    "Unit": 1,
                })

        # --area parameter
        if args.area:
            for area_str in args.area:
                areas.append(parse_area_string(area_str))

        if areas:
            config["AutoAreas"] = areas

    # Custom area erase (--custom-area)
    if method == "custom":
        custom_areas = []
        if args.custom_area:
            for area_str in args.custom_area:
                custom_areas.append(parse_custom_area_string(area_str))
        if custom_areas:
            config["CustomAreas"] = custom_areas

    return config


def is_subtitle_template(args):
    """Determine whether the current template is a subtitle erase template (supports erase method/model/area/OCR parameters)."""  # NOCA:line-too-long(content cannot be shortened)
    return get_template_id(args) in SUBTITLE_TEMPLATES


def build_smart_erase_task(args):
    """
    Build smart erase task parameters.

    Strategy:
    - If the user has not specified any custom parameters → use the preset template directly
    - If the user has specified custom parameters (only supported for subtitle erase templates) → use Definition +
    OverrideParameter to override template parameters
    """
    task = {}
    template_id = get_template_id(args)

    if not has_custom_params(args):
        # Pure preset template mode
        task["Definition"] = template_id
    else:
        # Override template parameter mode: based on preset template, override with Override Parameter
        task["Definition"] = template_id

        override = {
            "EraseType": "subtitle",
            "EraseSubtitleConfig": build_erase_subtitle_config(args),
        }
        task["OverrideParameter"] = override

    # Output storage (optional)
    output_storage = build_output_storage(args)
    if output_storage:
        task["OutputStorage"] = output_storage
    # Output file path (optional)
    if args.output_object_path:
        task["OutputObjectPath"] = args.output_object_path
    return task


def build_request_params(args):
    """Build the complete ProcessMedia request parameters."""
    params = {}

    # Input
    params["InputInfo"] = build_input_info(args)

    # Output storage
    output_storage = build_output_storage(args)
    if output_storage:
        params["OutputStorage"] = output_storage

    # Output directory: defaults to /output/erase/, can be overridden via --output-dir
    params["OutputDir"] = args.output_dir if args.output_dir else "/output/erase/"

    # Smart erase task (subtitle removal)
    smart_erase_task = build_smart_erase_task(args)
    params["SmartEraseTask"] = smart_erase_task

    # Callback configuration
    if args.notify_url:
        params["TaskNotifyConfig"] = {
            "NotifyType": "URL",
            "NotifyUrl": args.notify_url,
        }

    return params


def get_erase_summary(args):
    """Generate a summary text of the subtitle removal configuration."""
    items = []

    # Erase method
    method = args.method or PRESET_DEFAULTS["erase_method"]
    if method == "auto":
        items.append("🔍 Erase method: Auto erase (AI detects and removes subtitles)")
    else:
        items.append("📐 Erase method: Region erase (directly erases the specified region)")

    # Erase model
    model = args.model or PRESET_DEFAULTS["model"]
    if model == "standard":
        items.append("🤖 Erase model: Standard model (recommended, better seamless detail restoration)")
    else:
        items.append("💪 Erase model: Region model (aggressive erase, suitable for stylized/shadowed/animated subtitles)")  # NOCA:line-too-long(line cannot be shortened)

    # Subtitle position
    if args.position:
        preset = AREA_PRESETS.get(args.position, {})
        desc = preset.get("desc", args.position)
        coords = preset.get("coords", {})
        items.append(f"📍 Subtitle position: {desc} — region [{coords.get('LeftTopX')}, {coords.get('LeftTopY')}, {coords.get('RightBottomX')}, {coords.get('RightBottomY')}]")  # NOCA:line-too-long(line cannot be shortened)
    elif args.area:
        items.append(f"📍 Custom auto-erase regions: {len(args.area)} region(s)")
        for i, area_str in enumerate(args.area, 1):
            items.append(f"     Region {i}: {area_str}")
    elif method == "auto":
        items.append("📍 Subtitle position: Default (lower-center of frame)")

    # Specified regions
    if args.custom_area:
        items.append(f"📐 Specified erase regions: {len(args.custom_area)} region(s)")
        for i, area_str in enumerate(args.custom_area, 1):
            items.append(f"     Region {i}: {area_str}")

    # OCR
    if args.ocr:
        lang = args.subtitle_lang or "zh_en"
        fmt = args.subtitle_format or "vtt"
        items.append(f"📝 OCR subtitle extraction: Enabled (language: {lang}, format: {fmt})")

        # Translation
        if args.translate:
            lang_desc = TRANSLATE_LANGS.get(args.translate, args.translate)
            items.append(f"🌐 Subtitle translation: {lang_desc} ({args.translate})")

    return items


def process_media(args):
    """Submit a subtitle removal task or query an existing task."""
    region = args.region or os.environ.get("TENCENTCLOUD_API_REGION", "")

    # 1. Get credentials and client
    cred = get_credentials()
    client = create_mps_client(cred, region)

    # 2. Build request
    params = build_request_params(args)

    if args.dry_run:
        print("=" * 60)
        print("[Dry Run Mode] Printing request parameters only, API will not be called")
        print("=" * 60)
        print(json.dumps(params, ensure_ascii=False, indent=2))
        return

    # Print request parameters (for debugging)
    if args.verbose:
        print("Request parameters:")
        print(json.dumps(params, ensure_ascii=False, indent=2))
        print()

    # 3. Submit the request
    try:
        req = models.ProcessMediaRequest()
        req.from_json_string(json.dumps(params))

        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        task_id = result.get('TaskId', 'N/A')
        print("✅ Subtitle removal task submitted successfully!")
        print(f"   TaskId: {task_id}")
        print(f"\n## TaskId: {task_id}")
        print(f"   RequestId: {result.get('RequestId', 'N/A')}")

        template_id = get_template_id(args)
        if not has_custom_params(args):
            print(f"   Template: Preset template {template_id} ({PRESET_TEMPLATES.get(template_id, '')})")
        else:
            print(f"   Mode: Custom parameters (overriding preset template {template_id})")

            erase_items = get_erase_summary(args)
            if erase_items:
                print("   Configuration details:")
                for item in erase_items:
                    print(f"     {item}")

        print()
        if is_subtitle_template(args):
            print("⚠️  Note: By default, subtitles in the lower-center area of the video are detected. If subtitles are not fully removed,")  # NOCA:line-too-long(line cannot be shortened)
            print("   they may be outside the default region. Use --position or --area to specify the actual subtitle location.")  # NOCA:line-too-long(line cannot be shortened)

        if args.verbose:
            print("\nFull response:")
            print(json.dumps(result, ensure_ascii=False, indent=2))

        # Auto-poll (unless --no-wait is specified)
        no_wait = getattr(args, 'no_wait', False)
        if not no_wait and _POLL_AVAILABLE and task_id != 'N/A':
            poll_interval = getattr(args, 'poll_interval', 10)
            max_wait = getattr(args, 'max_wait', 1800)
            task_result = poll_video_task(task_id, region=region, interval=poll_interval,
                            max_wait=max_wait, verbose=args.verbose)
            # Auto-download results
            download_dir = getattr(args, 'download_dir', None)
            if download_dir and task_result and _POLL_AVAILABLE:
                auto_download_outputs(task_result, download_dir=download_dir)
        else:
            print(f"\nNote: The task is being processed in the background. Use the following command to check progress:")  # NOCA:line-too-long(line cannot be shortened)
            print(f"  python scripts/mps_get_video_task.py --task-id {task_id}")

        return result

    except TencentCloudSDKException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS Intelligent Erasure — Subtitle Removal / Watermark Removal / Face Blur, the top choice for video localization and short drama overseas distribution",  # NOCA:line-too-long(line cannot be shortened)
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # URL input + default template (subtitle removal 101), output to TENCENTCLOUD_COS_BUCKET/output/erase/
  python mps_erase.py --url https://example.com/video.mp4

  # COS input (bucket and region auto-read from environment variables)
  python mps_erase.py --cos-input-key /input/video/test.mp4

  # Subtitle removal with OCR subtitle extraction (template 102)
  python mps_erase.py --url https://example.com/video.mp4 --template 102

  # Watermark removal - advanced (template 201)
  python mps_erase.py --url https://example.com/video.mp4 --template 201

  # Face blur (template 301)
  python mps_erase.py --url https://example.com/video.mp4 --template 301

  # Face and license plate blur (template 302)
  python mps_erase.py --url https://example.com/video.mp4 --template 302

  # Aggressive erasure (area model, suitable for stylized/shadowed/animated subtitles)
  python mps_erase.py --url https://example.com/video.mp4 --model area

  # Subtitles in the upper half of the screen (using position preset)
  python mps_erase.py --url https://example.com/video.mp4 --position top-half

  # Subtitles in the lower half of the screen (using position preset)
  python mps_erase.py --url https://example.com/video.mp4 --position bottom-half

  # Subtitles on the left side (vertical subtitles)
  python mps_erase.py --url https://example.com/video.mp4 --position left

  # Subtitles on the right side (vertical subtitles)
  python mps_erase.py --url https://example.com/video.mp4 --position right

  # Custom subtitle region (top 0~25% of the frame)
  python mps_erase.py --url https://example.com/video.mp4 --area 0,0,1,0.25

  # Multi-region erasure (subtitles at both top and bottom)
  python mps_erase.py --url https://example.com/video.mp4 --area 0,0,1,0.15 --area 0,0.75,1,1

  # Fixed-region erasure (subtitle position is fixed, erase the bottom region of the entire video)
  python mps_erase.py --url https://example.com/video.mp4 \
      --method custom --custom-area 0,0,0,0.8,0.99,0.95

  # Erase within a specific time range (erase bottom region within the first 10 seconds)
  python mps_erase.py --url https://example.com/video.mp4 \
      --method custom --custom-area 0,10000,0,0.8,0.99,0.95

  # Subtitle removal + OCR subtitle extraction
  python mps_erase.py --url https://example.com/video.mp4 --ocr

  # Subtitle removal + OCR extraction + translate to English (short drama overseas)
  python mps_erase.py --url https://example.com/video.mp4 --ocr --translate en

  # Subtitle removal + OCR extraction + translate to Japanese
  python mps_erase.py --url https://example.com/video.mp4 --ocr --translate ja

  # Dry Run (print request parameters only)
  python mps_erase.py --url https://example.com/video.mp4 --dry-run

Preset Templates (--template):
  101   Subtitle removal (default)              — auto erasure + standard model
  102   Subtitle removal with OCR extraction    — auto erasure + standard model + OCR extraction
  201   Watermark removal - advanced            — advanced watermark erasure
  301   Face blur                               — auto-detect and blur faces
  302   Face and license plate blur             — auto-detect and blur faces and license plates

Erasure Method (templates 101/102 only):
  auto      Auto erasure (default) — AI automatically detects and erases subtitles, default region is the lower-center
  of the frame
  custom    Fixed-region erasure   — directly erase the specified region, suitable for fixed subtitle positions

Erasure Model (templates 101/102 only):
  standard  Standard model (recommended) — better detail-preserving results for standard subtitle styles
  area      Area model (aggressive erasure) — for stylized/shadowed/animated subtitles, erases a larger area

Area Presets (--position, templates 101/102 only):
  fullscreen   Full screen
  top-half     Upper half of screen
  bottom-half  Lower half of screen
  center       Center of screen
  left         Left side of screen
  right        Right side of screen

⚠️ Important:
  By default, subtitles in the lower-center area of the video are detected. If subtitles are not
  fully erased, the subtitle position may be outside the default region — use --position or
  --area to specify the actual subtitle location.

Supported target languages for translation (--translate):
  zh=Chinese  en=English  ja=Japanese  ko=Korean  fr=French  es=Spanish
  it=Italian  de=German  tr=Turkish  ru=Russian  pt=Portuguese
  vi=Vietnamese  id=Indonesian  ms=Malay  th=Thai  ar=Arabic  hi=Hindi

Environment Variables:
  TENCENTCLOUD_SECRET_ID   Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET       COS Bucket name (e.g. mybucket-125xxx, default: test_bucket)
  TENCENTCLOUD_COS_REGION       COS Bucket region (default: ap-guangzhou)
        """
    )

    # ---- Input source ----
    input_group = parser.add_argument_group("Input source (choose one of four)")
    input_group.add_argument("--local-file", type=str,
                             help="Local file path; automatically uploaded to COS before processing (requires TENCENTCLOUD_COS_BUCKET)")  # NOCA:line-too-long(line cannot be shortened)
    input_group.add_argument("--url", type=str, help="Video URL")

    # COS path input (new, recommended) - used after local upload to reference the COS path directly
    input_group.add_argument("--cos-input-bucket", type=str,
                             help="Input COS Bucket name (used with --cos-input-region/--cos-input-key)")
    input_group.add_argument("--cos-input-region", type=str,
                             help="Input COS Bucket region (e.g. ap-guangzhou)")
    input_group.add_argument("--cos-input-key", type=str,
                             help="Input COS object key (e.g. /input/video.mp4)")

    # ---- Output ----
    output_group = parser.add_argument_group("Output configuration (optional, default output to TENCENTCLOUD_COS_BUCKET/output/erase/)")  # NOCA:line-too-long(line cannot be shortened)
    output_group.add_argument("--output-bucket", type=str,
                              help="Output COS Bucket name (defaults to TENCENTCLOUD_COS_BUCKET environment variable)")
    output_group.add_argument("--output-region", type=str,
                              help="Output COS Bucket region (defaults to TENCENTCLOUD_COS_REGION environment variable, default: ap-guangzhou)")  # NOCA:line-too-long(line cannot be shortened)
    output_group.add_argument("--output-dir", type=str,
                              help="Output directory (default: /output/erase/), must start and end with /")
    output_group.add_argument("--output-object-path", type=str,
                              help="Output file path, e.g. /output/{inputName}_erase.{format}")

    # ---- Template selection ----
    template_group = parser.add_argument_group("Template selection")
    template_group.add_argument(
        "--template", type=int,
        choices=list(PRESET_TEMPLATES.keys()),
        default=DEFAULT_TEMPLATE_ID,
        metavar="TEMPLATE_ID",
        help=(
            "Preset template ID (default: 101). Options: "
            "101=Subtitle removal | "
            "102=Subtitle removal with OCR extraction | "
            "201=Watermark removal - advanced | "
            "301=Face blur | "
            "302=Face and license plate blur"
        )
    )

    # ---- Erasure configuration (templates 101/102 only) ----
    erase_group = parser.add_argument_group("Erasure configuration (subtitle removal templates 101/102 only)")
    erase_group.add_argument("--method", type=str, choices=["auto", "custom"],
                             help="Erasure method: auto=auto erasure (default, AI detects subtitles) | custom=fixed-region erasure")  # NOCA:line-too-long(line cannot be shortened)
    erase_group.add_argument("--model", type=str, choices=["standard", "area"],
                             help="Erasure model: standard=standard model (recommended, better detail preservation) | "
                                  "area=area model (aggressive erasure, suitable for special subtitle styles)")

    # ---- Subtitle position (templates 101/102 only) ----
    position_group = parser.add_argument_group(
        "Subtitle/erasure region (default is lower-center of frame; specify actual position if subtitles are not erased, templates 101/102 only)")  # NOCA:line-too-long(line cannot be shortened)
    position_group.add_argument(
        "--position", type=str,
        choices=list(AREA_PRESETS.keys()),
        help=(
            "Area preset: "
            "fullscreen=full screen | top-half=upper half | bottom-half=lower half | "
            "center=center | left=left side | right=right side"
        )
    )
    position_group.add_argument("--area", type=str, action="append", metavar="X1,Y1,X2,Y2",
                                help="Custom auto-erasure region (percentage coordinates 0~1). Format: LeftTopX,LeftTopY,RightBottomX,RightBottomY. "  # NOCA:line-too-long(line cannot be shortened)
                                     "Example: 0,0,1,0.3 means the top 30%% of the frame. Can be specified multiple times for multi-region erasure.")  # NOCA:line-too-long(line cannot be shortened)
    position_group.add_argument("--custom-area", type=str, action="append",
                                metavar="BEGIN,END,X1,Y1,X2,Y2",
                                help="Fixed erasure region + time range (for --method custom). "
                                     "Format: BeginMs,EndMs,LeftTopX,LeftTopY,RightBottomX,RightBottomY. "
                                     "BeginMs=0,EndMs=0 means the entire duration. "
                                     "Example: 0,0,0,0.8,1,0.95 erases the bottom region for the full duration. Can be specified multiple times.")  # NOCA:line-too-long(line cannot be shortened)

    # ---- OCR & Translation (templates 101/102 only) ----
    ocr_group = parser.add_argument_group("OCR subtitle extraction & translation (optional, auto erasure mode of subtitle templates 101/102 only)")  # NOCA:line-too-long(line cannot be shortened)
    ocr_group.add_argument("--ocr", action="store_true",
                           help="Enable OCR subtitle extraction (auto-detect subtitle text and output subtitle file)")
    ocr_group.add_argument("--subtitle-lang", type=str, choices=["zh_en", "multi"],
                           help="Subtitle language: zh_en=Chinese/English (default) | multi=multilingual")
    ocr_group.add_argument("--subtitle-format", type=str, choices=["srt", "vtt"],
                           help="Subtitle file format: srt | vtt (default)")
    ocr_group.add_argument("--translate", type=str, metavar="LANG",
                           choices=list(TRANSLATE_LANGS.keys()),
                           help="Enable subtitle translation and specify target language (requires --ocr). "
                                "Supported: zh/en/ja/ko/fr/es/it/de/tr/ru/pt/vi/id/ms/th/ar/hi")

    # ---- Other ----
    other_group = parser.add_argument_group("Other configuration")
    other_group.add_argument("--region", type=str, help="MPS service region (default: ap-guangzhou)")
    other_group.add_argument("--notify-url", type=str, help="Callback URL for task completion")
    other_group.add_argument("--no-wait", action="store_true",
                             help="Submit task only, do not wait for result (default: polls until completion)")
    other_group.add_argument("--poll-interval", type=int, default=10,
                             help="Polling interval in seconds (default: 10)")
    other_group.add_argument("--max-wait", type=int, default=1800,
                             help="Maximum wait time in seconds (default: 1800, i.e. 30 minutes)")
    other_group.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    other_group.add_argument("--dry-run", action="store_true", help="Print request parameters only, do not call the API")  # NOCA:line-too-long(line cannot be shortened)
    other_group.add_argument("--download-dir", type=str, default=None,
                             help="Automatically download results to the specified directory after task completion (default: no download; specify a path to enable auto-download)")  # NOCA:line-too-long(line cannot be shortened)

    args = parser.parse_args()
    # --url: if the value is a local path, automatically switch to local upload mode
    if getattr(args, 'url', None) and not getattr(args, 'local_file', None):
        _val = args.url
        if not _val.startswith('http://') and not _val.startswith('https://'):
            print(f"Note: '{_val}' does not specify a source; treating as a local file by default", file=sys.stderr)
            args.local_file = _val
            args.url = None

    # --local-file is mutually exclusive with COS input arguments
    if getattr(args, 'local_file', None):
        cos_conflicts = [x for x in [
            getattr(args, 'cos_input_bucket', None), getattr(args, 'cos_input_key', None)
        ] if x]
        if cos_conflicts:
            parser.error("--local-file cannot be used together with --cos-input-bucket / --cos-input-key")

    # Auto-upload local file
    if getattr(args, 'local_file', None):
        if not _POLL_AVAILABLE:
            print("Error: --local-file requires the mps_poll_task module", file=sys.stderr)
            sys.exit(1)
        upload_result = auto_upload_local_file(args.local_file)
        if not upload_result:
            sys.exit(1)
        args.cos_input_key = upload_result["Key"]
        args.cos_input_bucket = upload_result["Bucket"]
        args.cos_input_region = upload_result["Region"]

    # 1. Input source validation
    has_url = bool(args.url)
    has_cos_path = bool(getattr(args, 'cos_input_key', None))

    if not has_url and not has_cos_path:
        parser.error("Please specify an input source: --url or --cos-input-key (with --cos-input-bucket/--cos-input-region or environment variables)")  # NOCA:line-too-long(line cannot be shortened)

    # 2. Non-subtitle templates do not support erasure method/model/region/OCR parameters
    if not is_subtitle_template(args):
        subtitle_only_params = [
            (args.method, "--method"),
            (args.model, "--model"),
            (args.ocr, "--ocr"),
            (args.subtitle_lang, "--subtitle-lang"),
            (args.subtitle_format, "--subtitle-format"),
            (args.translate, "--translate"),
            (args.area, "--area"),
            (args.custom_area, "--custom-area"),
            (args.position, "--position"),
        ]
        used = [name for val, name in subtitle_only_params if val]
        if used:
            template_id = get_template_id(args)
            parser.error(
                f"Parameter(s) {', '.join(used)} are only supported for subtitle removal templates (101/102); "
                f"current template {template_id} ({PRESET_TEMPLATES.get(template_id, '')}) does not support these parameters"  # NOCA:line-too-long(line cannot be shortened)
            )

    # 3. --translate requires --ocr
    if args.translate and not args.ocr:
        parser.error("--translate requires --ocr (OCR subtitle extraction) to be enabled")

    # 4. --subtitle-lang / --subtitle-format require --ocr
    if (args.subtitle_lang or args.subtitle_format) and not args.ocr:
        parser.error("--subtitle-lang / --subtitle-format require --ocr to be enabled")

    # 5. --custom-area requires --method custom
    if args.custom_area and (args.method is None or args.method != "custom"):
        parser.error("--custom-area must be used together with --method custom")

    # 5b. Pre-validate --custom-area coordinates (to avoid errors after printing the summary)
    if args.custom_area:
        for area_str in args.custom_area:
            parse_custom_area_string(area_str)  # validation failure inside will call sys.exit(1)

    # 6. --area / --position cannot be used together with --method custom
    if args.method == "custom" and (args.area or args.position):
        parser.error("--area / --position cannot be used together with --method custom. "
                     "For fixed-region erasure, use --custom-area")

    # 7. OCR is only supported in auto erasure mode
    if args.ocr and args.method == "custom":
        parser.error("OCR subtitle extraction is only supported in auto erasure mode (--method auto)")

    # Print environment variable info
    cos_bucket_env = get_cos_bucket()
    cos_region_env = get_cos_region()

    # Print execution summary
    template_id_display = get_template_id(args)
    template_name_display = PRESET_TEMPLATES.get(template_id_display, "")
    print("=" * 60)
    print(f"Tencent Cloud MPS Intelligent Erasure — {template_name_display}")
    print("=" * 60)
    if args.url:
        print(f"Input: URL - {args.url}")
    elif getattr(args, 'cos_input_bucket', None):
        # New COS path input
        print(f"Input: COS - {args.cos_input_bucket}:{args.cos_input_key} (region: {args.cos_input_region})")
    else:
        bucket_display = getattr(args, 'cos_input_bucket', None) or cos_bucket_env or "not set"
        region_display = getattr(args, 'cos_input_region', None) or cos_region_env
        print(f"Input: COS - {bucket_display}:{args.cos_input_key} (region: {region_display})")

    # Output info
    out_bucket = args.output_bucket or cos_bucket_env or "not set"
    out_region = args.output_region or cos_region_env
    out_dir = args.output_dir or "/output/erase/"
    print(f"Output: COS - {out_bucket}:{out_dir} (region: {out_region})")

    if cos_bucket_env:
        print(f"COS Bucket (env var): {cos_bucket_env}")
    else:
        print("❌ TENCENTCLOUD_COS_BUCKET not set. Please configure it before retrying.", file=sys.stderr)
        sys.exit(1)

    template_id = get_template_id(args)
    if not has_custom_params(args):
        print(f"Template: preset template {template_id} ({PRESET_TEMPLATES.get(template_id, '')})")
    else:
        print(f"Template: custom parameters (overriding preset template {template_id})")
        erase_items = get_erase_summary(args)
        if erase_items:
            print("Configuration details:")
            for item in erase_items:
                print(f"  {item}")

    print()
    if is_subtitle_template(args):
        print("⚠️  Note: By default, subtitles in the lower-center area of the video are detected. If subtitles")
        print("   are not fully erased, the subtitle position may be outside the default region — use")
        print("   --position or --area to specify the actual subtitle location.")
    print("-" * 60)

    # Execute
    process_media(args)

if __name__ == "__main__":
    main()
