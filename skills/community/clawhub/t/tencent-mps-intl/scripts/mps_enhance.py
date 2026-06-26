#!/usr/bin/env python3
"""
Tencent Cloud MPS Video Enhancement Script

Features:
  Uses MPS video enhancement to fix various video quality issues and deliver a comprehensive
  picture quality improvement experience!
  Wraps the video enhancement API (defaults to Top-Speed Codec transcoding), supporting three
  presets: large-model enhancement, comprehensive enhancement, and artifact repair.

  Default preset template: 321002. If the user specifies parameter requirements (resolution,
  bitrate, enhancement capabilities, etc.), modifications are based on the 321002 preset template.

  Three preset modes (mutually exclusive, at most one may be selected):
    - diffusion (large-model enhancement): Reconstructs picture quality using a diffusion model;
      strongest effect but longer processing time.
    - comprehensive (comprehensive enhancement): Holistic picture quality optimization,
      balancing effect and efficiency.
    - artifact (artifact/ringing repair): Repairs compression-induced ringing artifacts and
      blocking artifacts.

  Mutual-exclusion constraints:
    - At most one of large-model enhancement, comprehensive enhancement, and artifact repair
      may be enabled at a time.
    - Large-model enhancement cannot be used together with super-resolution (SuperResolution)
      or denoising (Denoise).

COS Storage Convention:
  Specify the COS bucket name via the environment variable TENCENTCLOUD_COS_BUCKET.
  - Default input path:  {TENCENTCLOUD_COS_BUCKET}/input/   (COS object key starts with /input/)
  - Default output path: {TENCENTCLOUD_COS_BUCKET}/output/enhance/  (output directory: /output/enhance/)

  When using COS input, bucket/region are read automatically from the
  TENCENTCLOUD_COS_BUCKET / TENCENTCLOUD_COS_REGION environment variables.
  When --output-bucket is not explicitly specified, TENCENTCLOUD_COS_BUCKET is used as the
  output bucket automatically.
  When --output-dir is not explicitly specified, /output/enhance/ is used as the output
  directory automatically.

Usage:
  # Minimal usage: URL input + default preset template 321002
  # (output to TENCENTCLOUD_COS_BUCKET/output/enhance/)
  python mps_enhance.py --url https://example.com/video.mp4

  # COS input (recommended, using --cos-input-key)
  python mps_enhance.py --cos-input-key /input/video/test.mp4

  # Large-model enhancement preset (strength: strong)
  python mps_enhance.py --url https://example.com/video.mp4 --preset diffusion --diffusion-type strong

  # Comprehensive enhancement preset (strength: normal)
  python mps_enhance.py --url https://example.com/video.mp4 --preset comprehensive --comprehensive-type normal

  # Artifact repair preset (strength: strong)
  python mps_enhance.py --url https://example.com/video.mp4 --preset artifact --artifact-type strong

  # Custom resolution (width 1920, height auto-scaled)
  python mps_enhance.py --url https://example.com/video.mp4 --width 1920

  # Custom bitrate cap (unit: kbps)
  python mps_enhance.py --url https://example.com/video.mp4 --bitrate 3000

  # Enable both color enhancement and low-light enhancement
  python mps_enhance.py --url https://example.com/video.mp4 --color-enhance --low-light-enhance

  # Enable super-resolution (2×) + denoising + color enhancement
  # (cannot be used together with large-model enhancement)
  python mps_enhance.py --url https://example.com/video.mp4 --super-resolution --denoise --color-enhance

  # Enable scratch repair (old film restoration scenario)
  python mps_enhance.py --url https://example.com/video.mp4 --scratch-repair 0.8 --scene-type LQ_material

  # Use HDR enhancement
  python mps_enhance.py --url https://example.com/video.mp4 --hdr HDR10

  # Enable frame interpolation (target 60 fps)
  python mps_enhance.py --url https://example.com/video.mp4 --frame-rate 60

  # Specify enhancement scene (gaming video)
  python mps_enhance.py --url https://example.com/video.mp4 --scene-type game

  # Enable audio enhancement (denoising + volume normalization + beautification)
  python mps_enhance.py --url https://example.com/video.mp4 --audio-denoise --volume-balance --audio-beautify

  # Custom codec and container format
  python mps_enhance.py --url https://example.com/video.mp4 --codec h265 --container mp4

  # Dry run (print request parameters only, do not call the API)
  python mps_enhance.py --url https://example.com/video.mp4 --dry-run

Environment Variables:
  TENCENTCLOUD_SECRET_ID   - Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  - Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET       - COS bucket name (e.g. mybucket-125xxx; default: test_bucket)
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
    from mps_poll_task import poll_video_task, auto_upload_local_file, auto_download_outputs, auto_gen_compare
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
# Large-model enhancement dedicated templates (327001 ~ 327032)
# =============================================================================
# Real-person scene (Real) — for live-action footage; protects face and text regions
# Anime scene (Anime) — for anime-style content; enhances line and color-block features
# Jitter optimization (Jitter Opt) — reduces inter-frame jitter and texture flickering
# Maximum detail (Detail Max) — maximizes texture detail restoration
# Face fidelity (Face Fidelity) — preserves facial feature details to the greatest extent
# Old film restoration (Old Film) — severely degraded source; comprehensive enhancement + face enhancement + scratch removal
# Small face optimization - real (Real Small Face) — small/distant face optimization for real-person scenes
# Small face optimization - anime (Anime Small Face) — small/distant face optimization for anime scenes
#
# Template ID  Scene          Resolution  Description
# 327001       Real           720P        Real-person scene — large-model enhancement: denoising + super-resolution +
# comprehensive enhancement
# 327002       Anime          720P        Anime scene — large-model enhancement: denoising + super-resolution +
# comprehensive enhancement
# 327003       Real           1080P       Real-person scene — large-model enhancement: denoising + super-resolution +
# comprehensive enhancement
# 327004       Anime          1080P       Anime scene — large-model enhancement: denoising + super-resolution +
# comprehensive enhancement
# 327005       Real           2K          Real-person scene — large-model enhancement: denoising + super-resolution +
# comprehensive enhancement
# 327006       Anime          2K          Anime scene — large-model enhancement: denoising + super-resolution +
# comprehensive enhancement
# 327007       Real           4K          Real-person scene — large-model enhancement: denoising + super-resolution +
# comprehensive enhancement
# 327008       Anime          4K          Anime scene — large-model enhancement: denoising + super-resolution +
# comprehensive enhancement
# 327009       Jitter Opt      720P        Jitter optimization — large-model enhancement: denoising + super-resolution
# + comprehensive enhancement
# 327010       Jitter Opt      1080P       Jitter optimization — large-model enhancement: denoising + super-resolution
# + comprehensive enhancement
# 327011       Jitter Opt      2K          Jitter optimization — large-model enhancement: denoising + super-resolution
# + comprehensive enhancement
# 327012       Jitter Opt      4K          Jitter optimization — large-model enhancement: denoising + super-resolution
# + comprehensive enhancement
# 327013       Detail Max      720P        Maximum detail — large-model enhancement: denoising + super-resolution +
# comprehensive enhancement
# 327014       Detail Max      1080P       Maximum detail — large-model enhancement: denoising + super-resolution +
# comprehensive enhancement
# 327015       Detail Max      2K          Maximum detail — large-model enhancement: denoising + super-resolution +
# comprehensive enhancement
# 327016       Detail Max      4K          Maximum detail — large-model enhancement: denoising + super-resolution +
# comprehensive enhancement
# 327017       Face Fidelity   720P        Face fidelity — large-model enhancement: denoising + super-resolution +
# comprehensive enhancement
# 327018       Face Fidelity   1080P       Face fidelity — large-model enhancement: denoising + super-resolution +
# comprehensive enhancement
# 327019       Face Fidelity   2K          Face fidelity — large-model enhancement: denoising + super-resolution +
# comprehensive enhancement
# 327020       Face Fidelity   4K          Face fidelity — large-model enhancement: denoising + super-resolution +
# comprehensive enhancement
DIFFUSION_TEMPLATES = {
    # Real-person scene (Real)
    "real-720p": 327001,
    "real-1080p": 327003,
    "real-2k": 327005,
    "real-4k": 327007,
    # Anime scene (Anime)
    "anime-720p": 327002,
    "anime-1080p": 327004,
    "anime-2k": 327006,
    "anime-4k": 327008,
    # Jitter optimization (Jitter Opt)
    "jitter-720p": 327009,
    "jitter-1080p": 327010,
    "jitter-2k": 327011,
    "jitter-4k": 327012,
    # Maximum detail (Detail Max)
    "detail-720p": 327013,
    "detail-1080p": 327014,
    "detail-2k": 327015,
    "detail-4k": 327016,
    # Face fidelity (Face Fidelity)
    "face-720p": 327017,
    "face-1080p": 327018,
    "face-2k": 327019,
    "face-4k": 327020,
    # Old film / low-quality restoration (Old Film) — severely degraded source; comprehensive enhancement + face enhancement + scratch removal
    "old-720p": 327021,
    "old-1080p": 327022,
    "old-2k": 327023,
    "old-4k": 327024,
    # Small face optimization - real (Real Small Face) — small/distant face optimization for real-person scenes
    "real-small-face-720p": 327025,
    "real-small-face-1080p": 327026,
    "real-small-face-2k": 327027,
    "real-small-face-4k": 327028,
    # Small face optimization - anime (Anime Small Face) — small/distant face optimization for anime scenes
    "anime-small-face-720p": 327029,
    "anime-small-face-1080p": 327030,
    "anime-small-face-2k": 327031,
    "anime-small-face-4k": 327032,
}
DIFFUSION_TEMPLATE_DESC = {
    327001: "Real-person scene - 720P (face and text region protection)",
    327002: "Anime scene - 720P (anime line and color-block enhancement)",
    327003: "Real-person scene - 1080P (face and text region protection)",
    327004: "Anime scene - 1080P (anime line and color-block enhancement)",
    327005: "Real-person scene - 2K (face and text region protection)",
    327006: "Anime scene - 2K (anime line and color-block enhancement)",
    327007: "Real-person scene - 4K (face and text region protection)",
    327008: "Anime scene - 4K (anime line and color-block enhancement)",
    327009: "Jitter optimization - 720P (reduces inter-frame jitter and texture flickering)",
    327010: "Jitter optimization - 1080P (reduces inter-frame jitter and texture flickering)",
    327011: "Jitter optimization - 2K (reduces inter-frame jitter and texture flickering)",
    327012: "Jitter optimization - 4K (reduces inter-frame jitter and texture flickering)",
    327013: "Maximum detail - 720P (maximizes texture detail restoration)",
    327014: "Maximum detail - 1080P (maximizes texture detail restoration)",
    327015: "Maximum detail - 2K (maximizes texture detail restoration)",
    327016: "Maximum detail - 4K (maximizes texture detail restoration)",
    327017: "Face fidelity - 720P (preserves facial feature details to the greatest extent)",
    327018: "Face fidelity - 1080P (preserves facial feature details to the greatest extent)",
    327019: "Face fidelity - 2K (preserves facial feature details to the greatest extent)",
    327020: "Face fidelity - 4K (preserves facial feature details to the greatest extent)",
    327021: "Old film / low-quality restoration - 720P (severely degraded source; comprehensive enhancement + face enhancement + scratch removal)",
    327022: "Old film / low-quality restoration - 1080P (severely degraded source; comprehensive enhancement + face enhancement + scratch removal)",
    327023: "Old film / low-quality restoration - 2K (severely degraded source; comprehensive enhancement + face enhancement + scratch removal)",
    327024: "Old film / low-quality restoration - 4K (severely degraded source; comprehensive enhancement + face enhancement + scratch removal)",
    327025: "Real-person small face optimization - 720P (small/distant face optimization for real-person scenes)",
    327026: "Real-person small face optimization - 1080P (small/distant face optimization for real-person scenes)",
    327027: "Real-person small face optimization - 2K (small/distant face optimization for real-person scenes)",
    327028: "Real-person small face optimization - 4K (small/distant face optimization for real-person scenes)",
    327029: "Anime small face optimization - 720P (small/distant face optimization for anime scenes)",
    327030: "Anime small face optimization - 1080P (small/distant face optimization for anime scenes)",
    327031: "Anime small face optimization - 2K (small/distant face optimization for anime scenes)",
    327032: "Anime small face optimization - 4K (small/distant face optimization for anime scenes)",
}

# =============================================================================
# Default parameters for preset template 321002 (video enhancement — Top-Speed Codec transcoding)
# =============================================================================
PRESET_TEMPLATE_ID = 321002
PRESET_DEFAULTS = {
    "container": "mp4",
    "codec": "h265",
    "width": 0,           # 0 = keep original
    "height": 0,          # 0 = scale proportionally
    "bitrate": 0,         # 0 = keep original; Top-Speed Codec auto-optimizes
    "fps": 0,             # 0 = keep original
    "audio_codec": "aac",
    "audio_bitrate": 128,
    "audio_sample_rate": 44100,
}

# Enhancement preset type mapping
ENHANCE_PRESETS = {
    "diffusion": "Large-model enhancement (DiffusionEnhance)",
    "comprehensive": "Comprehensive enhancement (ImageQualityEnhance)",
    "artifact": "Artifact/ringing repair (ArtifactRepair)",
}

# Enhancement scene description mapping
SCENE_TYPE_DESC = {
    "common": "General — basic optimization for all video types",
    "AIGC": "AIGC — AI-powered overall resolution upscaling",
    "short_play": "Short drama — enhances facial and subtitle details",
    "short_video": "Short video — fixes complex and diverse quality issues",
    "game": "Gaming video — repairs motion blur and improves detail",
    "HD_movie_series": "Ultra-HD film/series — generates 4K 60fps HDR ultra-high-definition",
    "LQ_material": "Low-quality footage / old film restoration — resolution upscaling and damage repair",
    "lecture": "Live show / e-commerce / conference / lecture — beautifies and enhances facial appearance",
}


def get_cos_bucket():
    """Get the COS bucket name from environment variables."""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """Get the COS bucket region from environment variables; defaults to ap-guangzhou."""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


def get_credentials():
    """Get Tencent Cloud credentials from environment variables.
    """
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
          "  - COS path: --cos-input-key <key> (combined with environment variables or --cos-input-bucket/--cos-input-region)",  # NOCA:line-too-long(line cannot be shortened)
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


def validate_enhance_args(args):
    """
    Validate mutual exclusion constraints for enhancement parameters.

    Rules:
    - At most one of: large model enhancement (diffusion), comprehensive enhancement (comprehensive), artifact removal
    (artifact) can be enabled
    - Large model enhancement cannot be enabled simultaneously with super resolution (super_resolution)
    - Large model enhancement cannot be enabled simultaneously with denoising (denoise)
    """
    # Preset mode mutual exclusion validation
    if args.preset == "diffusion":
        if args.super_resolution:
            print("Error: Large model enhancement (diffusion) cannot be enabled simultaneously with super resolution (--super-resolution)", file=sys.stderr)  # NOCA:line-too-long(line cannot be shortened)
            sys.exit(1)
        if args.denoise:
            print("Error: Large model enhancement (diffusion) cannot be enabled simultaneously with denoising (--denoise)", file=sys.stderr)  # NOCA:line-too-long(line cannot be shortened)
            sys.exit(1)


def has_custom_params(args):
    """Detect whether the user has passed any custom transcoding/enhancement parameters."""
    return any([
        args.codec is not None,
        args.width is not None,
        args.height is not None,
        args.bitrate is not None,
        args.fps is not None,
        args.container is not None,
        args.audio_codec is not None,
        args.audio_bitrate is not None,
        args.preset is not None,
        args.super_resolution,
        args.denoise,
        args.color_enhance,
        args.low_light_enhance,
        args.scratch_repair is not None,
        args.hdr is not None,
        args.frame_rate is not None,
        args.scene_type is not None,
        args.audio_denoise,
        args.audio_separate is not None,
        args.volume_balance,
        args.audio_beautify,
    ])


def build_video_enhance(args):
    """
    Build the VideoEnhance configuration.

    Constructs video enhancement parameters based on the user's selected preset mode and additional enhancement
    switches.
    """
    video_enhance = {}

    # ---- Core enhancement capabilities (choose one of three, mutually exclusive) ----
    if args.preset == "diffusion":
        diffusion_type = args.diffusion_type or "normal"
        video_enhance["DiffusionEnhance"] = {
            "Switch": "ON",
            "Type": diffusion_type,
        }
    elif args.preset == "comprehensive":
        comprehensive_type = args.comprehensive_type or "weak"
        video_enhance["ImageQualityEnhance"] = {
            "Switch": "ON",
            "Type": comprehensive_type,
        }
    elif args.preset == "artifact":
        artifact_type = args.artifact_type or "weak"
        video_enhance["ArtifactRepair"] = {
            "Switch": "ON",
            "Type": artifact_type,
        }

    # ---- Stackable enhancement capabilities ----

    # Super resolution (note: cannot be enabled simultaneously with large model enhancement, already validated in
    # validate_enhance_args)
    if args.super_resolution:
        sr_config = {"Switch": "ON"}
        if args.sr_type:
            sr_config["Type"] = args.sr_type
        if args.sr_size:
            sr_config["Size"] = args.sr_size
        video_enhance["SuperResolution"] = sr_config

    # Denoising (note: cannot be enabled simultaneously with large model enhancement, already validated in
    # validate_enhance_args)
    if args.denoise:
        denoise_config = {"Switch": "ON"}
        if args.denoise_type:
            denoise_config["Type"] = args.denoise_type
        video_enhance["Denoise"] = denoise_config

    # Color enhancement
    if args.color_enhance:
        color_config = {"Switch": "ON"}
        if args.color_enhance_type:
            color_config["Type"] = args.color_enhance_type
        video_enhance["ColorEnhance"] = color_config

    # Low-light enhancement
    if args.low_light_enhance:
        video_enhance["LowLightEnhance"] = {
            "Switch": "ON",
            "Type": "normal",
        }

    # Scratch repair
    if args.scratch_repair is not None:
        video_enhance["ScratchRepair"] = {
            "Switch": "ON",
            "Intensity": args.scratch_repair,
        }

    # HDR
    if args.hdr:
        video_enhance["Hdr"] = {
            "Switch": "ON",
            "Type": args.hdr,
        }

    # Frame rate interpolation
    if args.frame_rate is not None:
        video_enhance["FrameRateWithDen"] = {
            "Switch": "ON",
            "FpsNum": args.frame_rate,
            "FpsDen": 1,
        }

    # Enhancement scene type
    if args.scene_type:
        video_enhance["EnhanceSceneType"] = args.scene_type

    return video_enhance if video_enhance else None


def build_audio_enhance(args):
    """
    Build the AudioEnhance configuration.
    """
    audio_enhance = {}

    # Audio denoising
    if args.audio_denoise:
        audio_enhance["Denoise"] = {"Switch": "ON"}

    # Audio separation
    if args.audio_separate:
        separate_config = {"Switch": "ON"}
        if args.audio_separate == "vocal":
            separate_config["Type"] = "normal"
            separate_config["Track"] = "vocal"
        elif args.audio_separate == "background":
            separate_config["Type"] = "normal"
            separate_config["Track"] = "background"
        elif args.audio_separate == "accompaniment":
            separate_config["Type"] = "music"
            separate_config["Track"] = "background"
        audio_enhance["Separate"] = separate_config

    # Volume balance
    if args.volume_balance:
        vb_config = {"Switch": "ON"}
        if args.volume_balance_type:
            vb_config["Type"] = args.volume_balance_type
        audio_enhance["VolumeBalance"] = vb_config

    # Audio beautification
    if args.audio_beautify:
        audio_enhance["Beautify"] = {
            "Switch": "ON",
            "Types": ["declick", "deesser"],
        }

    return audio_enhance if audio_enhance else None


def build_transcode_task(args):
    """
    Build transcode task parameters (including enhancement configuration).

    Strategy:
    - If the user specifies --template (large model enhancement dedicated template 327001~327032) → use that template
    directly
    - If the user does not specify any custom parameters → use preset template 321002 directly
    - If the user specifies custom parameters → build RawParameter based on 321002 defaults, overriding with user values
    """
    task = {}

    # Prioritize the large model enhancement dedicated template specified by the user
    if args.template:
        task["Definition"] = args.template
    elif not has_custom_params(args):
        # Pure preset template mode
        task["Definition"] = PRESET_TEMPLATE_ID
    else:
        # Custom parameter mode: based on preset template defaults, overridden by user values
        container = args.container if args.container else PRESET_DEFAULTS["container"]
        codec = args.codec if args.codec else PRESET_DEFAULTS["codec"]
        width = args.width if args.width is not None else PRESET_DEFAULTS["width"]
        height = args.height if args.height is not None else PRESET_DEFAULTS["height"]
        bitrate = args.bitrate if args.bitrate is not None else PRESET_DEFAULTS["bitrate"]
        fps = args.fps if args.fps is not None else PRESET_DEFAULTS["fps"]
        audio_codec = args.audio_codec if args.audio_codec else PRESET_DEFAULTS["audio_codec"]
        audio_bitrate = args.audio_bitrate if args.audio_bitrate is not None else PRESET_DEFAULTS["audio_bitrate"]

        video_template = {
            "Codec": codec,
            "Fps": fps,
            "Bitrate": bitrate,
            "Width": width,
            "Height": height,
            "ResolutionAdaptive": "open",
            "FillType": "black",
        }

        # TESHD scene-based configuration
        video_template["ScenarioBased"] = 1
        video_template["CompressType"] = "standard_compress"

        audio_template = {
            "Codec": audio_codec,
            "Bitrate": audio_bitrate,
            "SampleRate": PRESET_DEFAULTS["audio_sample_rate"],
            "AudioChannel": 2,
        }

        raw_parameter = {
            "Container": container,
            "RemoveVideo": 0,
            "RemoveAudio": 0,
            "VideoTemplate": video_template,
            "AudioTemplate": audio_template,
            "TEHDConfig": {
                "Type": "TEHD-100",
                "MaxVideoBitrate": 0,
            }
        }

        # ---- Build enhancement configuration ----
        enhance_config = {}

        video_enhance = build_video_enhance(args)
        if video_enhance:
            enhance_config["VideoEnhance"] = video_enhance

        audio_enhance = build_audio_enhance(args)
        if audio_enhance:
            enhance_config["AudioEnhance"] = audio_enhance

        if enhance_config:
            raw_parameter["EnhanceConfig"] = enhance_config

        task["RawParameter"] = raw_parameter

    # Override output filename (optional)
    if args.output_object_path:
        task["OutputObjectPath"] = args.output_object_path

    return task


def build_request_params(args):
    """Build complete ProcessMedia request parameters."""
    params = {}

    # Input
    params["InputInfo"] = build_input_info(args)

    # Output storage
    output_storage = build_output_storage(args)
    if output_storage:
        params["OutputStorage"] = output_storage

    # Output directory: defaults to /output/enhance/, can be overridden via --output-dir
    params["OutputDir"] = args.output_dir if args.output_dir else "/output/enhance/"

    # Transcode task (including enhancement configuration)
    transcode_task = build_transcode_task(args)
    params["MediaProcessTask"] = {
        "TranscodeTaskSet": [transcode_task]
    }

    # Callback configuration
    if args.notify_url:
        params["TaskNotifyConfig"] = {
            "NotifyType": "URL",
            "NotifyUrl": args.notify_url,
        }

    return params


def get_enhance_summary(args):
    """Generate enhancement capability summary text."""
    items = []

    if args.preset:
        preset_desc = ENHANCE_PRESETS.get(args.preset, args.preset)
        if args.preset == "diffusion":
            strength = args.diffusion_type or "normal"
        elif args.preset == "comprehensive":
            strength = args.comprehensive_type or "weak"
        elif args.preset == "artifact":
            strength = args.artifact_type or "weak"
        else:
            strength = ""
        items.append(f"🔥 {preset_desc} (strength: {strength})")

    if args.super_resolution:
        sr_type = args.sr_type or "lq"
        items.append(f"🔍 Super resolution (type: {sr_type}, 2x)")

    if args.denoise:
        denoise_type = args.denoise_type or "weak"
        items.append(f"🔇 Video denoising (strength: {denoise_type})")

    if args.color_enhance:
        color_type = args.color_enhance_type or "weak"
        items.append(f"🎨 Color enhancement (strength: {color_type})")

    if args.low_light_enhance:
        items.append("💡 Low-light enhancement")

    if args.scratch_repair is not None:
        items.append(f"🩹 Scratch removal (strength: {args.scratch_repair})")

    if args.hdr:
        items.append(f"🌈 HDR ({args.hdr})")

    if args.frame_rate is not None:
        items.append(f"🎬 Frame interpolation (target: {args.frame_rate}fps)")

    if args.scene_type:
        scene_desc = SCENE_TYPE_DESC.get(args.scene_type, args.scene_type)
        items.append(f"🎯 Scene: {scene_desc}")

    # Audio enhancement
    audio_items = []
    if args.audio_denoise:
        audio_items.append("denoising")
    if args.audio_separate:
        audio_items.append(f"separation({args.audio_separate})")
    if args.volume_balance:
        vb_type = args.volume_balance_type or "loudNorm"
        audio_items.append(f"volume balance({vb_type})")
    if args.audio_beautify:
        audio_items.append("beautify")
    if audio_items:
        items.append(f"🔊 Audio enhancement: {' + '.join(audio_items)}")

    return items


def _get_input_url(args):
    """Get the URL of the input source from arguments (used for comparison page)."""
    if getattr(args, 'url', None):
        return args.url
    # COS path → construct permanent URL
    cos_key = getattr(args, 'cos_input_key', None)
    if cos_key:
        bucket = getattr(args, 'cos_input_bucket', None) or get_cos_bucket()
        region = getattr(args, 'cos_input_region', None) or get_cos_region()
        if bucket:
            return f"https://{bucket}.cos.{region}.myqcloud.com/{cos_key.lstrip('/')}"
    return ""


def process_media(args):
    """Submit a video enhancement task."""
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
        print("✅ Video enhancement task submitted successfully!")
        print(f"   TaskId: {task_id}")
        print(f"\n## TaskId: {task_id}")
        print(f"   RequestId: {result.get('RequestId', 'N/A')}")

        if args.template:
            template_desc = DIFFUSION_TEMPLATE_DESC.get(args.template, f"Template {args.template}")
            print(f"   Template: Large model enhancement dedicated template {args.template} ({template_desc})")
        elif not has_custom_params(args):
            print(f"   Template: Preset template {PRESET_TEMPLATE_ID} (video enhancement)")
        else:
            codec = args.codec or PRESET_DEFAULTS["codec"]
            container = args.container or PRESET_DEFAULTS["container"]
            print(f"   Mode: Custom parameters (modified based on {PRESET_TEMPLATE_ID} preset parameters)")
            print(f"   Codec: {codec.upper()}, Container: {container.upper()}")
            if args.width:
                w = args.width
                h = args.height if args.height else "adaptive"
                print(f"   Resolution: {w} x {h}")
            if args.bitrate:
                print(f"   Bitrate: {args.bitrate} kbps")

            enhance_items = get_enhance_summary(args)
            if enhance_items:
                print("   Enhancement capabilities:")
                for item in enhance_items:
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
            # Auto generate comparison page
            compare_opt = getattr(args, 'compare', None)
            if compare_opt and task_result and _POLL_AVAILABLE:
                input_url = _get_input_url(args)
                compare_path = None if compare_opt == "auto" else compare_opt
                auto_gen_compare(task_result, input_url, media_type="video",
                                 title="Video Enhancement Effect Comparison", output_path=compare_path)
        else:
            print(f"\nNote: The task is being processed in the background. Use the following command to check progress:")  # NOCA:line-too-long(line cannot be shortened)
            print(f"  python scripts/mps_get_video_task.py --task-id {task_id}")

        return result

    except TencentCloudSDKException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS Video Enhancement — supports large model enhancement, comprehensive enhancement, artifact removal, and more presets to fully improve video quality",  # NOCA:line-too-long(line cannot be shortened)
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # URL input + default template (video enhancement 321002), output to TENCENTCLOUD_COS_BUCKET/output/enhance/
  python mps_enhance.py --url https://example.com/video.mp4

  # COS path input (recommended, use after local upload)
  python mps_enhance.py --cos-input-bucket mybucket-125xxx --cos-input-region ap-guangzhou --cos-input-key
  /input/video/test.mp4

  # COS input (bucket and region auto-read from environment variables)
  python mps_enhance.py --cos-input-key /input/video/test.mp4

  # Large model enhancement (strength: strong, best quality)
  python mps_enhance.py --url https://example.com/video.mp4 --preset diffusion --diffusion-type strong

  # Comprehensive enhancement (strength: normal, balanced quality and efficiency)
  python mps_enhance.py --url https://example.com/video.mp4 --preset comprehensive --comprehensive-type normal

  # Artifact removal (deblocking, strength: strong)
  python mps_enhance.py --url https://example.com/video.mp4 --preset artifact --artifact-type strong

  # Super-resolution + denoising + color enhancement (combined)
  python mps_enhance.py --url https://example.com/video.mp4 --super-resolution --denoise --color-enhance

  # Old film restoration (scratch repair + low-light enhancement + color enhancement)
  python mps_enhance.py --url https://example.com/video.mp4 \\
      --scratch-repair 0.8 --low-light-enhance --color-enhance --scene-type LQ_material

  # Game video enhancement (frame interpolation to 60fps + comprehensive enhancement)
  python mps_enhance.py --url https://example.com/video.mp4 \\
      --preset comprehensive --frame-rate 60 --scene-type game

  # Audio enhancement (denoising + volume balancing + beautification)
  python mps_enhance.py --url https://example.com/video.mp4 --audio-denoise --volume-balance --audio-beautify

  # Dry run (print request parameters only)
  python mps_enhance.py --url https://example.com/video.mp4 --preset diffusion --dry-run

Enhancement preset descriptions (choose one, mutually exclusive):
  diffusion      Large model enhancement — diffusion model-based quality reconstruction, strongest effect, longer
  processing time
  comprehensive  Comprehensive enhancement — overall quality optimization, balanced quality and efficiency
  artifact       Artifact removal — repairs compression artifacts and blocking artifacts

Mutual exclusion constraints:
  - Large model enhancement, comprehensive enhancement, and artifact removal: at most one can be enabled
  - Large model enhancement cannot be used together with super-resolution (--super-resolution)
  - Large model enhancement cannot be used together with denoising (--denoise)

Enhancement scene descriptions:
  common          General — basic optimization for all video types
  AIGC            AIGC — uses AI to improve overall video resolution
  short_play      Short drama — enhances facial and subtitle details
  short_video     Short video — optimizes complex and diverse quality issues
  game            Game video — fixes motion blur and improves detail
  HD_movie_series Ultra HD film/series — generates 4K 60fps HDR
  LQ_material     Low-quality footage / old film restoration — resolution upscaling and damage repair
  lecture         Show / e-commerce / conference / lecture — beautifies and enhances facial effects

Environment variables:
  TENCENTCLOUD_SECRET_ID   Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET       COS Bucket name (e.g. mybucket-125xxx, default: test_bucket)
  TENCENTCLOUD_COS_REGION       COS Bucket region (default: ap-guangzhou)
        """
    )

    # ---- Input source ----
    input_group = parser.add_argument_group("Input source (choose one of four)")
    input_group.add_argument("--local-file", type=str,
                             help="Local file path, automatically uploaded to COS before processing (requires TENCENTCLOUD_COS_BUCKET)")  # NOCA:line-too-long(line cannot be shortened)
    input_group.add_argument("--url", type=str, help="Video URL")

    # COS path input (new version, recommended) - use after local upload with COS path directly
    input_group.add_argument("--cos-input-bucket", type=str,
                             help="Input COS Bucket name (used with --cos-input-region/--cos-input-key)")
    input_group.add_argument("--cos-input-region", type=str,
                             help="Input COS Bucket region (e.g. ap-guangzhou)")
    input_group.add_argument("--cos-input-key", type=str,
                             help="Input COS object key (e.g. /input/video.mp4)")


    # ---- Output ----
    output_group = parser.add_argument_group("Output configuration (optional, defaults to TENCENTCLOUD_COS_BUCKET/output/enhance/)")  # NOCA:line-too-long(line cannot be shortened)
    output_group.add_argument("--output-bucket", type=str,
                              help="Output COS Bucket name (defaults to TENCENTCLOUD_COS_BUCKET environment variable)")
    output_group.add_argument("--output-region", type=str,
                              help="Output COS Bucket region (defaults to TENCENTCLOUD_COS_REGION environment variable, default: ap-guangzhou)")  # NOCA:line-too-long(line cannot be shortened)
    output_group.add_argument("--output-dir", type=str,
                              help="Output directory (default: /output/enhance/), must start and end with /")
    output_group.add_argument("--output-object-path", type=str,
                              help="Output file path, e.g. /output/{inputName}_enhance.{format}")

    # ---- Enhancement presets ----
    enhance_group = parser.add_argument_group("Enhancement presets (choose one, mutually exclusive)")
    enhance_group.add_argument("--preset", type=str,
                               choices=["diffusion", "comprehensive", "artifact"],
                               help="Enhancement preset mode: diffusion=large model enhancement | comprehensive=comprehensive enhancement | artifact=artifact removal")  # NOCA:line-too-long(line cannot be shortened)
    enhance_group.add_argument("--diffusion-type", type=str, choices=["weak", "normal", "strong"],
                               help="Large model enhancement strength (default: normal)")
    enhance_group.add_argument("--comprehensive-type", type=str, choices=["weak", "normal", "strong"],
                               help="Comprehensive enhancement strength (default: weak)")
    enhance_group.add_argument("--artifact-type", type=str, choices=["weak", "strong"],
                               help="Artifact removal strength (default: weak)")

    # ---- Stackable video enhancement capabilities ----
    video_enhance_group = parser.add_argument_group("Video enhancement capabilities (stackable, note mutual exclusion constraints)")  # NOCA:line-too-long(line cannot be shortened)
    video_enhance_group.add_argument("--super-resolution", action="store_true",
                                     help="Enable super-resolution (2x). Note: cannot be used with large model enhancement")  # NOCA:line-too-long(line cannot be shortened)
    video_enhance_group.add_argument("--sr-type", type=str, choices=["lq", "hq"],
                                     help="Super-resolution type: lq=low-quality noisy video | hq=high-quality video (default: lq)")  # NOCA:line-too-long(line cannot be shortened)
    video_enhance_group.add_argument("--sr-size", type=int, choices=[2],
                                     help="Super-resolution scale factor, currently only supports 2 (default: 2)")
    video_enhance_group.add_argument("--denoise", action="store_true",
                                     help="Enable video denoising. Note: cannot be used with large model enhancement")
    video_enhance_group.add_argument("--denoise-type", type=str, choices=["weak", "strong"],
                                     help="Denoising strength (default: weak)")
    video_enhance_group.add_argument("--color-enhance", action="store_true",
                                     help="Enable color enhancement")
    video_enhance_group.add_argument("--color-enhance-type", type=str, choices=["weak", "normal", "strong"],
                                     help="Color enhancement strength (default: weak)")
    video_enhance_group.add_argument("--low-light-enhance", action="store_true",
                                     help="Enable low-light enhancement")
    video_enhance_group.add_argument("--scratch-repair", type=float, metavar="INTENSITY",
                                     help="Enable scratch repair, intensity range 0.0~1.0 (e.g. 0.5, 0.8)")
    video_enhance_group.add_argument("--hdr", type=str, choices=["HDR10", "HLG"],
                                     help="Enable HDR enhancement (requires h264 or h265 encoding, bit depth 10)")
    video_enhance_group.add_argument("--frame-rate", type=int, metavar="FPS",
                                     help="Enable frame interpolation, target frame rate (Hz), e.g. 60. Has no effect if source frame rate >= target frame rate")  # NOCA:line-too-long(line cannot be shortened)
    video_enhance_group.add_argument("--scene-type", type=str,
                                     choices=["common", "AIGC", "short_play", "short_video", "game",
                                              "HD_movie_series", "LQ_material", "lecture"],
                                     help="Enhancement scene type (see epilog for details)")

    # ---- Audio enhancement ----
    audio_enhance_group = parser.add_argument_group("Audio enhancement (optional)")
    audio_enhance_group.add_argument("--audio-denoise", action="store_true",
                                     help="Enable audio denoising")
    audio_enhance_group.add_argument("--audio-separate", type=str,
                                     choices=["vocal", "background", "accompaniment"],
                                     help="Audio separation: vocal=extract vocals | background=extract background audio | accompaniment=extract accompaniment")  # NOCA:line-too-long(line cannot be shortened)
    audio_enhance_group.add_argument("--volume-balance", action="store_true",
                                     help="Enable volume balancing")
    audio_enhance_group.add_argument("--volume-balance-type", type=str, choices=["loudNorm", "gainControl"],
                                     help="Volume balance type: loudNorm=loudness normalization | gainControl=reduce sudden changes (default: loudNorm)")  # NOCA:line-too-long(line cannot be shortened)
    audio_enhance_group.add_argument("--audio-beautify", action="store_true",
                                     help="Enable audio beautification (noise removal + sibilance suppression)")

    # ---- Video transcoding parameters ----
    video_group = parser.add_argument_group("Video parameters (optional, uses preset template 321002 if not specified)")
    video_group.add_argument("--codec", type=str, choices=["h264", "h265", "h266", "av1", "vp9"],
                             help="Video codec (default: h265)")
    video_group.add_argument("--width", type=int, help="Video width / long side (px), e.g. 1920, 1280, 3840")
    video_group.add_argument("--height", type=int, help="Video height / short side (px), 0=scale proportionally")
    video_group.add_argument("--bitrate", type=int,
                             help="Video bitrate (kbps), 0=auto. TESHD will automatically optimize bitrate")
    video_group.add_argument("--fps", type=int, help="Video frame rate (Hz), 0=keep original")
    video_group.add_argument("--container", type=str, choices=["mp4", "hls", "flv"],
                             help="Container format (default: mp4)")

    # ---- Audio parameters ----
    audio_group = parser.add_argument_group("Audio parameters (optional)")
    audio_group.add_argument("--audio-codec", type=str, choices=["aac", "mp3", "copy"],
                             help="Audio codec (default: aac)")
    audio_group.add_argument("--audio-bitrate", type=int, help="Audio bitrate (kbps), default: 128")

    # ---- Large model enhancement dedicated templates ----
    diffusion_template_group = parser.add_argument_group(
        "Large model enhancement dedicated templates (327001~327032, specify template ID directly, highest priority)"
    )
    diffusion_template_group.add_argument(
        "--template", type=int, metavar="TEMPLATE_ID",
        help=(
            "Directly specify a large model enhancement dedicated template ID (327001~327032), takes priority over --preset and other enhancement parameters.\n"  # NOCA:line-too-long(line cannot be shortened)
            "Live-action scene (Real, face and text region protection): 327001(720P) 327003(1080P) 327005(2K) 327007(4K)\n"  # NOCA:line-too-long(line cannot be shortened)
            "Anime scene (Anime, anime line and color block enhancement): 327002(720P) 327004(1080P) 327006(2K) 327008(4K)\n"  # NOCA:line-too-long(line cannot be shortened)
            "Jitter optimization (JitterOpt, reduces inter-frame jitter): 327009(720P) 327010(1080P) 327011(2K) 327012(4K)\n"  # NOCA:line-too-long(line cannot be shortened)
            "Maximum detail (DetailMax, maximizes texture detail): 327013(720P) 327014(1080P) 327015(2K) 327016(4K)\n"
            "Face fidelity (FaceFidelity, preserves facial features): 327017(720P) 327018(1080P) 327019(2K) 327020(4K)\n"
            "Old film / low-quality restoration (OldFilm, comprehensive+face+scratch removal): 327021(720P) 327022(1080P) 327023(2K) 327024(4K)\n"  # NOCA:line-too-long(line cannot be shortened)
            "Real-person small face optimization (RealSmallFace, small/distant face): 327025(720P) 327026(1080P) 327027(2K) 327028(4K)\n"  # NOCA:line-too-long(line cannot be shortened)
            "Anime small face optimization (AnimeSmallFace, small/distant face): 327029(720P) 327030(1080P) 327031(2K) 327032(4K)"  # NOCA:line-too-long(line cannot be shortened)
        )
    )

    # ---- Other ----
    other_group = parser.add_argument_group("Other configuration")
    other_group.add_argument("--region", type=str, help="MPS service region (default: ap-guangzhou)")
    other_group.add_argument("--notify-url", type=str, help="Task completion callback URL")
    other_group.add_argument("--no-wait", action="store_true",
                             help="Submit task only, do not wait for result (by default, polls automatically until completion)")  # NOCA:line-too-long(line cannot be shortened)
    other_group.add_argument("--poll-interval", type=int, default=10,
                             help="Polling interval (seconds), default: 10")
    other_group.add_argument("--max-wait", type=int, default=1800,
                             help="Maximum wait time (seconds), default: 1800 (30 minutes)")
    other_group.add_argument("--verbose", "-v", action="store_true", help="Output verbose information")
    other_group.add_argument("--dry-run", action="store_true", help="Print request parameters only, do not call the API")  # NOCA:line-too-long(line cannot be shortened)
    other_group.add_argument("--download-dir", type=str, default=None,
                             help="Automatically download results to the specified directory after task completion (default: no download; specify a path to enable auto-download)")  # NOCA:line-too-long(line cannot be shortened)
    other_group.add_argument("--compare", nargs="?", const="auto", default=None, metavar="OUTPUT",
                             help="Automatically generate a comparison HTML page after task completion (optionally specify output path, auto-generated by default)")  # NOCA:line-too-long(line cannot be shortened)

    args = parser.parse_args()
    # --url: if a local path is provided, automatically switch to local upload mode
    if getattr(args, 'url', None) and not getattr(args, 'local_file', None):
        _val = args.url
        if not _val.startswith('http://') and not _val.startswith('https://'):
            print(f"Note: '{_val}' has no recognized scheme, treating as a local file by default", file=sys.stderr)
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

    has_url = bool(args.url)
    has_cos_path = bool(getattr(args, 'cos_input_key', None))

    if not has_url and not has_cos_path:
        parser.error("Please specify an input source: --url or --cos-input-key (with --cos-input-bucket/--cos-input-region or environment variables)")  # NOCA:line-too-long(line cannot be shortened)

    # Validate enhancement parameter mutual exclusion constraints
    validate_enhance_args(args)

    # Validate scratch_repair range
    if args.scratch_repair is not None and (args.scratch_repair < 0.0 or args.scratch_repair > 1.0):
        parser.error("--scratch-repair intensity must be in the range 0.0~1.0")

    # Print environment variable information
    cos_bucket_env = get_cos_bucket()
    cos_region_env = get_cos_region()

    # Print execution information
    print("=" * 60)
    print("Tencent Cloud MPS Video Enhancement")
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

    # Output information
    out_bucket = args.output_bucket or cos_bucket_env or "not set"
    out_region = args.output_region or cos_region_env
    # Set output directory, default to /output/enhance/
    out_dir = args.output_dir or "/output/enhance/"
    print(f"Output: COS - {out_bucket}:{out_dir} (region: {out_region})")

    if cos_bucket_env:
        print(f"COS Bucket (environment variable): {cos_bucket_env}")
    else:
        print("❌ TENCENTCLOUD_COS_BUCKET not set. Please configure it before retrying.", file=sys.stderr)
        sys.exit(1)

    if args.template:
        template_desc = DIFFUSION_TEMPLATE_DESC.get(args.template, f"Template {args.template}")
        print(f"Template: large model enhancement dedicated template {args.template} ({template_desc})")
    elif not has_custom_params(args):
        print(f"Template: preset template {PRESET_TEMPLATE_ID} (video enhancement)")
    else:
        print(f"Template: custom parameters (based on preset template {PRESET_TEMPLATE_ID})")
        enhance_items = get_enhance_summary(args)
        if enhance_items:
            print("Enhancement capabilities:")
            for item in enhance_items:
                print(f"  {item}")
    print("-" * 60)

    # Execute
    process_media(args)


if __name__ == "__main__":
    main()
