#!/usr/bin/env python3
"""
Tencent Cloud MPS Intelligent Subtitle Script

Features:
  Uses MPS intelligent subtitle functionality to extract subtitles from videos
  via ASR speech recognition and OCR text recognition, with support for
  large model translation into other languages. The top choice for video
  dubbing, short drama overseas distribution, and subtitle extraction!

  Wraps the "Intelligent Subtitle" API and supports three processing modes:
    - ASR subtitle recognition (default): Extracts subtitles via speech recognition, supports 30+ source languages
    - OCR subtitle recognition: Extracts subtitles via on-screen text recognition (suitable for hard subtitle scenarios)
    - Pure subtitle translation: Translates existing subtitle files without recognition

  System preset templates (recommended to use Definition method; refer to the console for specific subtitle template
  IDs):  # noqa: E501
    - 110167  ASR subtitle recognition (example)

  Subtitle processing types (ProcessType):
    - 0  ASR subtitle recognition (default) — extracts subtitles via speech recognition
    - 1  Pure subtitle translation           — translates existing subtitle files to other languages
    - 2  OCR subtitle recognition            — extracts subtitles via on-screen text recognition

  Subtitle language types (SubtitleType):
    - 0  Source language subtitles (default)
    - 1  Translated language subtitles (requires translation enabled)
    - 2  Bilingual subtitles: source + translated language (requires translation enabled)

COS Storage Conventions:
  Specify the COS Bucket name via the environment variable TENCENTCLOUD_COS_BUCKET.
  - Default input path:  {TENCENTCLOUD_COS_BUCKET}/input/   (i.e., COS Object starts with /input/)
  - Default output path: {TENCENTCLOUD_COS_BUCKET}/output/subtitle/  (i.e., output directory is /output/subtitle/)

  When using COS input, bucket/region are automatically read from the
  TENCENTCLOUD_COS_BUCKET/TENCENTCLOUD_COS_REGION environment variables.
  When --output-bucket is not explicitly specified, TENCENTCLOUD_COS_BUCKET is used as the output bucket.
  When --output-dir is not explicitly specified, /output/subtitle/ is used as the output directory.

Usage:
  # Simplest usage: ASR subtitle recognition (source language subtitles, auto-detect language)
  python mps_subtitle.py --url https://example.com/video.mp4

  # Specify video source language as Chinese
  python mps_subtitle.py --url https://example.com/video.mp4 --src-lang zh

  # ASR recognition + translate to English (bilingual subtitles)
  python mps_subtitle.py --url https://example.com/video.mp4 --src-lang zh --translate en

  # ASR recognition + translate to English, output translated language subtitles only
  python mps_subtitle.py --url https://example.com/video.mp4 --src-lang zh --translate en --subtitle-type 1

  # ASR recognition + translate to both English and Japanese (multi-language translation)
  python mps_subtitle.py --url https://example.com/video.mp4 --src-lang zh --translate en/ja

  # OCR subtitle recognition (suitable for hard subtitles, stylized text, etc.)
  python mps_subtitle.py --url https://example.com/video.mp4 --process-type ocr --src-lang zh_en

  # OCR recognition + translate to English
  python mps_subtitle.py --url https://example.com/video.mp4 --process-type ocr --src-lang zh_en --translate en

  # OCR recognition + custom recognition area (bottom 30% of the frame)
  python mps_subtitle.py --url https://example.com/video.mp4 --process-type ocr --src-lang zh_en \
      --ocr-area 0,0.7,1,1

  # Pure subtitle translation (translate an existing subtitle file)
  python mps_subtitle.py --url https://example.com/video.mp4 --process-type translate --translate en

  # Output subtitles in SRT format
  python mps_subtitle.py --url https://example.com/video.mp4 --subtitle-format srt

  # Use a preset template
  python mps_subtitle.py --url https://example.com/video.mp4 --template 110167

  # COS input (recommended, use --cos-input-key)
  python mps_subtitle.py --cos-input-key /input/video/test.mp4

  # Custom output path
  python mps_subtitle.py --url https://example.com/video.mp4 \
      --output-object-path /output/{inputName}_subtitle.{format}

  # ASR hotword library (improves recognition accuracy for technical terms)
  python mps_subtitle.py --url https://example.com/video.mp4 --hotwords-id hwd-xxxxx

  # Dry Run (print request parameters only, do not actually call the API)
  python mps_subtitle.py --url https://example.com/video.mp4 --dry-run

Environment Variables:
  TENCENTCLOUD_SECRET_ID        - Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY       - Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET       - COS Bucket name (e.g., mybucket-125xxx, default: test_bucket)
  TENCENTCLOUD_COS_REGION       - COS Bucket region (default: ap-guangzhou)
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
# Processing type mappings
# =============================================================================
PROCESS_TYPE_MAP = {
    "asr": 0,        # ASR speech recognition subtitles
    "translate": 1,  # Pure subtitle translation
    "ocr": 2,        # OCR text recognition subtitles
}

PROCESS_TYPE_DESC = {
    0: "ASR speech recognition subtitles",
    1: "Pure subtitle translation",
    2: "OCR text recognition subtitles",
}

# Subtitle language type descriptions
SUBTITLE_TYPE_DESC = {
    0: "Source language subtitles",
    1: "Translated language subtitles",
    2: "Source + translated language bilingual subtitles",
}

# Commonly supported source languages for ASR recognition
ASR_SRC_LANGUAGES = {
    "auto": "Auto-detect (pure subtitle translation mode only)",
    "zh": "Simplified Chinese",
    "en": "English",
    "ja": "Japanese",
    "ko": "Korean",
    "zh-PY": "Chinese-English-Cantonese",
    "zh_medical": "Chinese Medical",
    "vi": "Vietnamese",
    "ms": "Malay",
    "id": "Indonesian",
    "fil": "Filipino",
    "th": "Thai",
    "pt": "Portuguese",
    "tr": "Turkish",
    "ar": "Arabic",
    "es": "Spanish",
    "hi": "Hindi",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "zh_dialect": "Chinese Dialect",
    "zh_en": "Chinese-English (for OCR recognition)",
    "yue": "Cantonese",
    "ru": "Russian",
    "prime_zh": "Chinese-English Dialect",
    "multi": "Other multilingual (for OCR recognition)",
}

# Translation target languages (common subset; full list supports 200+ languages)
TRANSLATE_DST_LANGUAGES = {
    "zh": "Simplified Chinese",
    "zh-TW": "Traditional Chinese",
    "en": "English",
    "ja": "Japanese",
    "ko": "Korean",
    "fr": "French",
    "fr-CA": "French (Canada)",
    "es": "Spanish",
    "pt": "Portuguese",
    "pt-BR": "Portuguese (Brazil)",
    "de": "German",
    "it": "Italian",
    "ru": "Russian",
    "ar": "Arabic",
    "hi": "Hindi",
    "th": "Thai",
    "vi": "Vietnamese",
    "id": "Indonesian",
    "ms": "Malay",
    "tr": "Turkish",
    "nl": "Dutch",
    "pl": "Polish",
    "sv": "Swedish",
    "da": "Danish",
    "fi": "Finnish",
    "no": "Norwegian",
    "cs": "Czech",
    "el": "Greek",
    "ro": "Romanian",
    "hu": "Hungarian",
    "uk": "Ukrainian",
    "he": "Hebrew",
    "fil": "Filipino",
    "yue": "Cantonese",
}


def get_cos_bucket():
    """Get the COS Bucket name from environment variables."""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """Get the COS Bucket region from environment variables, defaulting to ap-guangzhou."""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


def get_credentials():
    """Get Tencent Cloud credentials from environment variables. """  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
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
          "  - COS path: --cos-input-key <key> (combined with environment variables or --cos-input-bucket/--cos-input-region)",  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
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


def parse_ocr_area(area_str):
    """
    Parse an OCR area string into an AutoAreas object.

    Format: LeftTopX,LeftTopY,RightBottomX,RightBottomY
    Example: 0,0.7,1,1 represents the bottom 30% area
    Coordinates are percentage values (0~1), using percentage units.
    """
    parts = area_str.split(",")
    if len(parts) != 4:
        print(f"Error: Incorrect OCR area format '{area_str}', expected LeftTopX,LeftTopY,RightBottomX,RightBottomY (e.g. 0,0.7,1,1)",  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
              file=sys.stderr)
        sys.exit(1)
    try:
        left_top_x = float(parts[0])
        left_top_y = float(parts[1])
        right_bottom_x = float(parts[2])
        right_bottom_y = float(parts[3])
    except ValueError:
        print(f"Error: OCR area coordinates must be numeric '{area_str}'", file=sys.stderr)
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


def build_raw_parameter(args):
    """
    Build the RawParameter for SmartSubtitlesTask.

    Includes: SubtitleType, VideoSrcLanguage, SubtitleFormat, TranslateSwitch,
              TranslateDstLanguage, ProcessType, AsrHotWordsConfigure,
              SelectingSubtitleAreasConfig, and other parameters.
    """
    raw = {}

    # ------ Processing type (Process Type) ------
    process_type_str = args.process_type or "asr"
    process_type = PROCESS_TYPE_MAP.get(process_type_str, 0)
    raw["ProcessType"] = process_type

    # ------ Video source language (Video Src Language) ------
    if args.src_lang:
        raw["VideoSrcLanguage"] = args.src_lang
    else:
        # Default source language
        if process_type == 0:
            raw["Video Src Language"] = "zh"  # ASR default: Chinese
        elif process_type == 1:
            raw["Video Src Language"] = "auto"  # Pure translation default: auto-detect
        elif process_type == 2:
            raw["Video Src Language"] = "zh_en"  # OCR default: Chinese + English

    # ------ Translation switch and target language ------
    if args.translate:
        raw["TranslateSwitch"] = "ON"
        raw["TranslateDstLanguage"] = args.translate
    else:
        raw["TranslateSwitch"] = "OFF"

    # ------ Subtitle language type (Subtitle Type) ------
    if args.subtitle_type is not None:
        raw["SubtitleType"] = args.subtitle_type
    else:
        # Auto-infer
        if args.translate:
            raw["Subtitle Type"] = 2  # With translation: default source language + translated language
        else:
            raw["Subtitle Type"] = 0  # Without translation: default source language

    # ------ Subtitle file format (Subtitle Format) ------
    if args.subtitle_format:
        raw["SubtitleFormat"] = args.subtitle_format
    else:
        # Default format
        if process_type == 0:
            # ASR mode: must specify format for multilingual translation
            if args.translate:
                raw["SubtitleFormat"] = "vtt"
            else:
                raw["Subtitle Format"] = "vtt"  # ASR default: vtt
        elif process_type == 1:
            raw["Subtitle Format"] = "original"  # Pure translation default: same as source file
        elif process_type == 2:
            raw["Subtitle Format"] = "vtt"  # OCR default: vtt

    # ------ ASR hotword library ------
    if args.hotwords_id:
        raw["AsrHotWordsConfigure"] = {
            "Switch": "ON",
            "LibraryId": args.hotwords_id,
        }

    # ------ OCR area configuration (OCR mode only) ------
    if process_type == 2 and args.ocr_area:
        auto_areas = []
        for area_str in args.ocr_area:
            auto_areas.append(parse_ocr_area(area_str))

        selecting_config = {
            "AutoAreas": auto_areas,
        }
        # Optional sample video dimensions
        if args.sample_width:
            selecting_config["SampleWidth"] = args.sample_width
        if args.sample_height:
            selecting_config["SampleHeight"] = args.sample_height

        raw["SelectingSubtitleAreasConfig"] = selecting_config

    # ------ Extended parameters ------
    if args.ext_info:
        raw["ExtInfo"] = args.ext_info

    return raw


def build_smart_subtitles_task(args):
    """
    Build smart subtitle task parameters.

    Strategy:
    - If --template specifies a template ID → use Definition mode
    - Otherwise → use RawParameter custom parameter mode (Definition=0)
    """
    task = {}

    if args.template:
        # Preset template mode
        task["Definition"] = args.template

        # If custom parameters are also provided, build Raw Parameter to override
        if has_custom_params(args):
            task["RawParameter"] = build_raw_parameter(args)
    else:
        # Custom parameter mode (Definition=0 enables Raw Parameter)
        task["Definition"] = 0
        task["RawParameter"] = build_raw_parameter(args)

    # User extension field
    if args.user_ext_para:
        task["UserExtPara"] = args.user_ext_para

    # Output storage (task level)
    output_storage = build_output_storage(args)
    if output_storage:
        task["OutputStorage"] = output_storage

    # Output file path
    if args.output_object_path:
        task["OutputObjectPath"] = args.output_object_path

    return task


def has_custom_params(args):
    """Detect whether the user has passed any custom subtitle parameters (requiring RawParameter to be built)."""
    return any([
        args.process_type is not None,
        args.src_lang is not None,
        args.translate is not None,
        args.subtitle_type is not None,
        args.subtitle_format is not None,
        args.hotwords_id is not None,
        args.ocr_area is not None and len(args.ocr_area) > 0,
        args.ext_info is not None,
    ])


def build_request_params(args):
    """Build the complete ProcessMedia request parameters."""
    params = {}

    # Input
    params["InputInfo"] = build_input_info(args)

    # Output storage
    output_storage = build_output_storage(args)
    if output_storage:
        params["OutputStorage"] = output_storage

    # Output directory: defaults to /output/subtitle/, can be overridden via --output-dir
    params["OutputDir"] = args.output_dir if args.output_dir else "/output/subtitle/"

    # Smart subtitle task
    smart_subtitles_task = build_smart_subtitles_task(args)
    params["SmartSubtitlesTask"] = smart_subtitles_task

    # Callback configuration
    if args.notify_url:
        params["TaskNotifyConfig"] = {
            "NotifyType": "URL",
            "NotifyUrl": args.notify_url,
        }

    return params


def get_subtitle_summary(args):
    """Generate intelligent subtitle configuration summary text."""
    items = []

    # Process type
    process_type_str = args.process_type or "asr"
    process_type = PROCESS_TYPE_MAP.get(process_type_str, 0)
    desc = PROCESS_TYPE_DESC.get(process_type, "Unknown")
    items.append(f"📝 Process Type: {desc}({process_type_str})")

    # Source language
    src_lang = args.src_lang
    if not src_lang:
        if process_type == 0:
            src_lang = "zh"
        elif process_type == 1:
            src_lang = "auto"
        elif process_type == 2:
            src_lang = "zh_en"
    src_lang_desc = ASR_SRC_LANGUAGES.get(src_lang, src_lang)
    items.append(f"🗣️ Source Language: {src_lang_desc}({src_lang})")

    # Translation
    if args.translate:
        # Supports multiple languages, separated by /
        dst_langs = args.translate.split("/")
        lang_descs = []
        for lang in dst_langs:
            lang_desc = TRANSLATE_DST_LANGUAGES.get(lang, lang)
            lang_descs.append(f"{lang_desc}({lang})")
        items.append(f"🌐 Translation Target: {', '.join(lang_descs)}")
    else:
        items.append("🌐 Translation: Disabled")

    # Subtitle language type
    subtitle_type = args.subtitle_type
    if subtitle_type is None:
        subtitle_type = 2 if args.translate else 0
    st_desc = SUBTITLE_TYPE_DESC.get(subtitle_type, "Unknown")
    items.append(f"📋 Subtitle Type: {st_desc}(SubtitleType={subtitle_type})")

    # Subtitle format
    fmt = args.subtitle_format
    if not fmt:
        if process_type == 1:
            fmt = "original"
        else:
            fmt = "vtt"
    items.append(f"📄 Subtitle Format: {fmt}")

    # Hotword library
    if args.hotwords_id:
        items.append(f"🔤 ASR Hotword Library: {args.hotwords_id}")

    # OCR area
    if args.ocr_area:
        items.append(f"📐 OCR Recognition Area: {len(args.ocr_area)} region(s)")
        for i, area_str in enumerate(args.ocr_area, 1):
            items.append(f"     Region {i}: {area_str}")

    return items


def process_media(args):
    """Submit an intelligent subtitle task."""
    region = args.region or os.environ.get("TENCENTCLOUD_API_REGION", "")

    # 1. Get credentials and client
    cred = get_credentials()
    client = create_mps_client(cred, region)

    # 2. Build request
    params = build_request_params(args)

    if args.dry_run:
        print("=" * 60)
        print("[Dry Run Mode] Only printing request parameters, not calling API")
        print("=" * 60)
        print(json.dumps(params, ensure_ascii=False, indent=2))
        return

    # Print request parameters (for debugging)
    if args.verbose:
        print("Request parameters:")
        print(json.dumps(params, ensure_ascii=False, indent=2))
        print()

    # 3. Submit the call
    try:
        req = models.ProcessMediaRequest()
        req.from_json_string(json.dumps(params))

        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        task_id = result.get('TaskId', 'N/A')
        print("✅ Intelligent subtitle task submitted successfully!")
        print(f"   TaskId: {task_id}")
        print(f"\n## TaskId: {task_id}")
        print(f"   RequestId: {result.get('RequestId', 'N/A')}")

        if args.template and not has_custom_params(args):
            print(f"   Template: Preset template {args.template}")
        else:
            process_type_str = args.process_type or "asr"
            process_type = PROCESS_TYPE_MAP.get(process_type_str, 0)
            desc = PROCESS_TYPE_DESC.get(process_type, "Unknown")
            print(f"   Mode: Custom parameters ({desc})")

        subtitle_items = get_subtitle_summary(args)
        if subtitle_items:
            print("   Configuration details:")
            for item in subtitle_items:
                print(f"     {item}")

        if args.verbose:
            print("\nFull response:")
            print(json.dumps(result, ensure_ascii=False, indent=2))

        # Auto polling (unless --no-wait is specified)
        no_wait = getattr(args, 'no_wait', False)
        if not no_wait and _POLL_AVAILABLE and task_id != 'N/A':
            poll_interval = getattr(args, 'poll_interval', 10)
            max_wait = getattr(args, 'max_wait', 1800)
            task_result = poll_video_task(task_id, region=region, interval=poll_interval,
                            max_wait=max_wait, verbose=args.verbose)
            # Auto download results
            download_dir = getattr(args, 'download_dir', None)
            if download_dir and task_result and _POLL_AVAILABLE:
                auto_download_outputs(task_result, download_dir=download_dir)
        else:
            print(f"\nNote: The task is being processed in the background. Use the following command to check progress:")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
            print(f"  python scripts/mps_get_video_task.py --task-id {task_id}")

        return result

    except TencentCloudSDKException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS Intelligent Subtitle — Extract video subtitles via ASR/OCR, supports LLM-based translation, ideal for video dubbing and short drama globalization",  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # ASR subtitle recognition (simplest usage, default Chinese + VTT format)
  python mps_subtitle.py --url https://example.com/video.mp4

  # Specify source language as English
  python mps_subtitle.py --url https://example.com/video.mp4 --src-lang en

  # ASR recognition + translate to English (default bilingual subtitle output)
  python mps_subtitle.py --url https://example.com/video.mp4 --src-lang zh --translate en

  # ASR recognition + translate to English, output translated subtitles only
  python mps_subtitle.py --url https://example.com/video.mp4 --src-lang zh --translate en --subtitle-type 1

  # ASR recognition + multi-language translation (English and Japanese)
  python mps_subtitle.py --url https://example.com/video.mp4 --src-lang zh --translate en/ja

  # OCR subtitle recognition (hard subtitle scenario)
  python mps_subtitle.py --url https://example.com/video.mp4 --process-type ocr --src-lang zh_en

  # OCR + custom region (recognize subtitles only in the bottom 30% of the frame)
  python mps_subtitle.py --url https://example.com/video.mp4 --process-type ocr --src-lang zh_en \\
      --ocr-area 0,0.7,1,1

  # OCR + translate to English
  python mps_subtitle.py --url https://example.com/video.mp4 --process-type ocr --src-lang zh_en --translate en

  # Subtitle translation only (translate existing subtitle file, no recognition)
  python mps_subtitle.py --url https://example.com/video.mp4 --process-type translate --translate en

  # Output SRT format
  python mps_subtitle.py --url https://example.com/video.mp4 --subtitle-format srt

  # Use preset template (check subtitle template ID in the console)
  python mps_subtitle.py --url https://example.com/video.mp4 --template 110167

  # ASR hotword library (improves recognition accuracy for technical terms)
  python mps_subtitle.py --url https://example.com/video.mp4 --hotwords-id hwd-xxxxx

  # COS path input (recommended, use after local upload)
  python mps_subtitle.py --cos-input-bucket mybucket-125xxx --cos-input-region ap-guangzhou --cos-input-key
  /input/video/test.mp4

  # COS input (bucket and region auto-fetched from environment variables)
  python mps_subtitle.py --cos-input-key /input/video/test.mp4

  # Dry Run (print request parameters only)
  python mps_subtitle.py --url https://example.com/video.mp4 --dry-run

Process type description (--process-type):
  asr         ASR speech recognition subtitle (default) — extract subtitles via speech recognition
  ocr         OCR text recognition subtitle             — extract hard subtitles via on-screen text recognition
  translate   Subtitle translation only                 — translate existing subtitle file, no recognition

Subtitle language type (--subtitle-type):
  0   Source language subtitle (default, when no translation)
  1   Translated language subtitle
  2   Source language + translated language bilingual subtitle (default, when translation is enabled)

Common ASR source languages (--src-lang):
  zh=Simplified Chinese  en=English  ja=Japanese  ko=Korean  zh-PY=Chinese-English-Cantonese
  vi=Vietnamese  ms=Malay  id=Indonesian  th=Thai  fr=French
  de=German  es=Spanish  pt=Portuguese  ru=Russian  ar=Arabic
  yue=Cantonese  zh_dialect=Chinese dialect  prime_zh=Chinese-English dialect

OCR source languages (--src-lang):
  zh_en=Chinese-English  multi=Other multilingual

Translation target languages (--translate, separate multiple languages with /, e.g. en/ja):
  zh=Chinese  en=English  ja=Japanese  ko=Korean  fr=French  es=Spanish
  de=German  it=Italian  ru=Russian  pt=Portuguese  ar=Arabic
  th=Thai  vi=Vietnamese  id=Indonesian  ms=Malay  tr=Turkish
  nl=Dutch  pl=Polish  sv=Swedish  See API docs for more languages

Environment variables:
  TENCENTCLOUD_SECRET_ID   Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET       COS Bucket name (e.g. mybucket-125xxx, default test_bucket)
  TENCENTCLOUD_COS_REGION       COS Bucket region (default ap-guangzhou)
        """
    )

    # ---- Input source ----
    input_group = parser.add_argument_group("Input source (choose one of four)")
    input_group.add_argument("--local-file", type=str,
                             help="Local file path, automatically uploaded to COS before processing (requires TENCENTCLOUD_COS_BUCKET)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    input_group.add_argument("--url", type=str, help="Video URL")

    # COS path input (new version, recommended) - for direct use of COS path after local upload
    input_group.add_argument("--cos-input-bucket", type=str,
                             help="Input COS Bucket name (used with --cos-input-region/--cos-input-key)")
    input_group.add_argument("--cos-input-region", type=str,
                             help="Input COS Bucket region (e.g. ap-guangzhou)")
    input_group.add_argument("--cos-input-key", type=str,
                             help="Input COS object key (e.g. /input/video.mp4)")


    # ---- Output ----
    output_group = parser.add_argument_group("Output configuration (optional, default output to TENCENTCLOUD_COS_BUCKET/output/subtitle/)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    output_group.add_argument("--output-bucket", type=str,
                              help="Output COS Bucket name (default from TENCENTCLOUD_COS_BUCKET environment variable)")
    output_group.add_argument("--output-region", type=str,
                              help="Output COS Bucket region (default from TENCENTCLOUD_COS_REGION environment variable, default ap-guangzhou)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    output_group.add_argument("--output-dir", type=str,
                              help="Output directory (default /output/subtitle/), must start and end with /")
    output_group.add_argument("--output-object-path", type=str,
                              help="Output subtitle file path, e.g. /output/{inputName}_subtitle.{format}")

    # ---- Subtitle processing type ----
    subtitle_group = parser.add_argument_group("Subtitle processing configuration")
    subtitle_group.add_argument("--process-type", type=str,
                                choices=["asr", "ocr", "translate"],
                                help="Subtitle processing type: asr=ASR speech recognition (default) | ocr=OCR text recognition | "  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
                                     "translate=Subtitle translation only")
    subtitle_group.add_argument("--src-lang", type=str,
                                help="Video source language. ASR mode: zh/en/ja/ko etc. (default zh); "
                                     "OCR mode: zh_en/multi (default zh_en); "
                                     "Translation-only mode: auto or specify language (default auto)")
    subtitle_group.add_argument("--subtitle-type", type=int, choices=[0, 1, 2],
                                help="Subtitle language type: 0=source language | 1=translated language | 2=source+translated bilingual (default). "  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
                                     "Without translation only 0 is supported; with translation 1 or 2 is supported")
    subtitle_group.add_argument("--subtitle-format", type=str, choices=["vtt", "srt", "original"],
                                help="Subtitle file format: vtt=WebVTT (default) | srt=SRT | "
                                     "original=same as source file (translation-only mode only)")

    # ---- Translation ----
    translate_group = parser.add_argument_group("Translation configuration (optional, bilingual subtitle output by default when enabled)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    translate_group.add_argument("--translate", type=str, metavar="LANG",
                                 help="Translation target language, e.g. en/ja/ko/zh etc. "
                                      "Separate multiple languages with /, e.g. en/ja means translate to both English and Japanese")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)

    # ---- ASR configuration ----
    asr_group = parser.add_argument_group("ASR speech recognition configuration (optional, ASR mode only)")
    asr_group.add_argument("--hotwords-id", type=str,
                           help="ASR hotword library ID (improves recognition accuracy for technical terms), e.g. hwd-xxxxx")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)

    # ---- OCR configuration ----
    ocr_group = parser.add_argument_group("OCR text recognition configuration (optional, OCR mode only)")
    ocr_group.add_argument("--ocr-area", type=str, action="append", metavar="X1,Y1,X2,Y2",
                           help="OCR recognition area (percentage coordinates 0~1). "
                                "Format: LeftTopX,LeftTopY,RightBottomX,RightBottomY. "
                                "Example: 0,0.7,1,1 means recognize subtitles only in the bottom 30%% of the frame. Can be specified multiple times")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    ocr_group.add_argument("--sample-width", type=int,
                           help="Width of the sample video/image (pixels), used with --ocr-area")
    ocr_group.add_argument("--sample-height", type=int,
                           help="Height of the sample video/image (pixels), used with --ocr-area")

    # ---- Template ----
    template_group = parser.add_argument_group("Template configuration (optional)")
    template_group.add_argument("--template", type=int, metavar="ID",
                                help="Intelligent subtitle preset template ID (e.g. 110167). "
                                     "If not specified, uses custom parameter mode (Definition=0 + RawParameter)")

    # ---- Advanced ----
    advanced_group = parser.add_argument_group("Advanced configuration (optional)")
    advanced_group.add_argument("--user-ext-para", type=str,
                                help="User extension field, not required in general scenarios")
    advanced_group.add_argument("--ext-info", type=str,
                                help="Custom extension parameters (JSON string)")

    # ---- Other ----
    other_group = parser.add_argument_group("Other configuration")
    other_group.add_argument("--region", type=str, help="MPS service region (default ap-guangzhou)")
    other_group.add_argument("--notify-url", type=str, help="Task completion callback URL")
    other_group.add_argument("--no-wait", action="store_true",
                             help="Submit task only, do not wait for result (default polls automatically until completion)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    other_group.add_argument("--poll-interval", type=int, default=10,
                             help="Polling interval (seconds), default 10")
    other_group.add_argument("--max-wait", type=int, default=1800,
                             help="Maximum wait time (seconds), default 1800 (30 minutes)")
    other_group.add_argument("--verbose", "-v", action="store_true", help="Output detailed information")
    other_group.add_argument("--dry-run", action="store_true", help="Print request parameters only, do not actually call the API")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    other_group.add_argument("--download-dir", type=str, default=None,
                             help="Automatically download results to the specified directory after task completion (default: no download; specify a path to enable auto-download)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)

    args = parser.parse_args()
    # --url auto-converts local path to local upload mode
    if getattr(args, 'url', None) and not getattr(args, 'local_file', None):
        _val = args.url
        if not _val.startswith('http://') and not _val.startswith('https://'):
            print(f"Notice: '{_val}' has no scheme specified, treating as local file by default", file=sys.stderr)
            args.local_file = _val
            args.url = None

    # --local-file and COS input parameters are mutually exclusive
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

    # 1. Input source
    has_url = bool(args.url)
    has_cos_path = bool(getattr(args, 'cos_input_key', None))

    if not has_url and not has_cos_path:
        parser.error("Please specify an input source: --url or --cos-input-key (with --cos-input-bucket/--cos-input-region or environment variables)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)

    # 2. Process type validation
    process_type_str = args.process_type or "asr"

    # Translation-only mode requires translation to be enabled
    if process_type_str == "translate" and not args.translate:
        parser.error("Translation-only mode (--process-type translate) requires --translate target language to be specified")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)

    # Translation-only mode does not support subtitle-type=0 (no translation)
    if process_type_str == "translate" and args.subtitle_type == 0:
        parser.error("Translation-only mode (--process-type translate) does not support --subtitle-type 0 (source language), "  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
                     "please use 1 (translated language) or 2 (bilingual)")

    # 3. Translation validation
    if not args.translate and args.subtitle_type is not None and args.subtitle_type > 0:
        parser.error("--subtitle-type 1 or 2 requires translation to be enabled (--translate)")

    # 4. OCR area is only used in OCR mode
    if args.ocr_area and process_type_str != "ocr":
        parser.error("--ocr-area is only available in OCR recognition mode (--process-type ocr)")

    # 5. Hotword library is only used in ASR mode
    if args.hotwords_id and process_type_str != "asr":
        parser.error("--hotwords-id is only available in ASR speech recognition mode (--process-type asr or default)")

    # 6. 'original' format is only used in translation-only mode
    if args.subtitle_format == "original" and process_type_str != "translate":
        parser.error("Subtitle format 'original' is only available in translation-only mode (--process-type translate)")

    # 7. sample-width / sample-height requires --ocr-area
    if (args.sample_width or args.sample_height) and not args.ocr_area:
        parser.error("--sample-width / --sample-height must be used with --ocr-area")

    # Print environment variable info
    cos_bucket_env = get_cos_bucket()
    cos_region_env = get_cos_region()

    # Print execution info
    print("=" * 60)
    print("Tencent Cloud MPS Intelligent Subtitle")
    print("=" * 60)
    if args.url:
        print(f"Input: URL - {args.url}")
    elif getattr(args, 'cos_input_bucket', None):
        # New COS path input
        print(f"Input: COS - {args.cos_input_bucket}:{args.cos_input_key} (region: {args.cos_input_region})")
    else:
        bucket_display = getattr(args, 'cos_input_bucket', None) or cos_bucket_env or "Not set"
        region_display = getattr(args, 'cos_input_region', None) or cos_region_env
        print(f"Input: COS - {bucket_display}:{args.cos_input_key} (region: {region_display})")

    # Output info
    out_bucket = args.output_bucket or cos_bucket_env or "Not set"
    out_region = args.output_region or cos_region_env
    # Set output directory, default /output/subtitle/
    out_dir = args.output_dir or "/output/subtitle/"
    print(f"Output: COS - {out_bucket}:{out_dir} (region: {out_region})")

    if cos_bucket_env:
        print(f"COS Bucket (environment variable): {cos_bucket_env}")
    else:
        print("❌ TENCENTCLOUD_COS_BUCKET not set. Please configure it before retrying.", file=sys.stderr)
        sys.exit(1)

    if args.template and not has_custom_params(args):
        print(f"Template: Preset template {args.template}")
    else:
        print("Template: Custom parameter mode (Definition=0 + RawParameter)")

    # Configuration summary
    subtitle_items = get_subtitle_summary(args)
    if subtitle_items:
        print("Configuration details:")
        for item in subtitle_items:
            print(f"  {item}")

    print("-" * 60)

    # Execute
    process_media(args)


if __name__ == "__main__":
    main()
