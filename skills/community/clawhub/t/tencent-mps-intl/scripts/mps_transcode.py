#!/usr/bin/env python3
"""
Tencent Cloud MPS TESHD Transcoding Script

Features:
  Uses MPS TESHD transcoding to maximize compression while maintaining quality,
  significantly reducing bandwidth and storage costs!

  Uses preset template 100305 by default (TESHD-H265-MP4-1080P).
  If the user provides parameter requirements (resolution, bitrate, etc.),
  modifies the parameters based on the 100305 preset template.

COS Storage Convention:
  COS bucket name is specified via the TENCENTCLOUD_COS_BUCKET environment variable.
  - Default input file path: {TENCENTCLOUD_COS_BUCKET}/input/   (COS objects start with /input/)
  - Default output file path: {TENCENTCLOUD_COS_BUCKET}/output/transcode/ (output directory is /output/transcode/)

  When using COS input, bucket/region are automatically read from
  TENCENTCLOUD_COS_BUCKET/TENCENTCLOUD_COS_REGION environment variables.
  When --output-bucket is not explicitly specified, TENCENTCLOUD_COS_BUCKET is used as the output bucket.
  When --output-dir is not explicitly specified, /output/transcode/ is used as the output directory.

Usage:
  # Simplest usage: URL input + default template (output to TENCENTCLOUD_COS_BUCKET/output/transcode/)
  python mps_transcode.py --url https://example.com/video.mp4

  # COS input (recommended, using --cos-input-key)
  python mps_transcode.py --cos-input-key /input/video/test.mp4

  # COS input + explicitly specifying bucket (overrides environment variable)
  python mps_transcode.py --cos-input-bucket mybucket-125xxx \
      --cos-input-region ap-guangzhou --cos-input-key /input/video/test.mp4

  # Custom output COS location (overrides default /output/transcode/ directory)
  python mps_transcode.py --url https://example.com/video.mp4 \
      --output-bucket mybucket-125xxx --output-region ap-guangzhou --output-dir /custom_output/

  # Custom resolution (width 1920, height auto-scaling)
  python mps_transcode.py --url https://example.com/video.mp4 --width 1920

  # Custom resolution (720P)
  python mps_transcode.py --url https://example.com/video.mp4 --width 1280 --height 720

  # Custom maximum bitrate (unit kbps)
  python mps_transcode.py --url https://example.com/video.mp4 --bitrate 2000

  # Custom encoding format
  python mps_transcode.py --url https://example.com/video.mp4 --codec h264

  # Custom container format
  python mps_transcode.py --url https://example.com/video.mp4 --container hls

  # Custom frame rate
  python mps_transcode.py --url https://example.com/video.mp4 --fps 30

  # Using custom parameter override (fully custom mode, not using preset template)
  python mps_transcode.py --url https://example.com/video.mp4 \
      --codec h265 --width 1920 --height 1080 --bitrate 3000 --fps 30 --container mp4

  # Maximum compression mode
  python mps_transcode.py --url https://example.com/video.mp4 --compress-type ultra_compress

  # Quality priority mode
  python mps_transcode.py --url https://example.com/video.mp4 --compress-type low_compress

  # Specify scene-based transcoding (e.g., UGC short video)
  python mps_transcode.py --url https://example.com/video.mp4 --scene-type ugc

  # Set callback URL
  python mps_transcode.py --url https://example.com/video.mp4 --notify-url https://example.com/callback

Environment Variables:
  TENCENTCLOUD_SECRET_ID   - Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  - Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET       - COS Bucket name (e.g., mybucket-125xxx, default test_bucket)
  TENCENTCLOUD_COS_REGION       - COS Bucket region (default ap-guangzhou)
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
    print("Error: Please install Tencent Cloud SDK first: pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# Preset template 100305 default parameters (TESHD-H265-MP4-1080P)
# =============================================================================
PRESET_TEMPLATE_ID = 100305
PRESET_DEFAULTS = {
    "container": "mp4",
    "codec": "h265",
    "width": 1920,
    "height": 0,          # 0 means proportional scaling
    "bitrate": 0,         # 0 means keep same as original, optimized by TESHD
    "fps": 0,             # 0 means keep same as original
    "audio_codec": "aac",
    "audio_bitrate": 128,
    "audio_sample_rate": 44100,
}


def get_cos_bucket():
    """Get COS bucket name from environment variable."""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """Get COS bucket region from environment variable, default ap-guangzhou."""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


def get_credentials():
    """Get Tencent Cloud credentials from environment variables. If missing, try auto-loading from system files and retry."""  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        print("❌ TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY not found", file=sys.stderr)
        print("   Please configure them in ~/.env or <SKILL_DIR>/.env", file=sys.stderr)
        if _LOAD_ENV_AVAILABLE:
            from mps_load_env import _print_setup_hint
            _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
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
    # Check if new COS path parameters are used
    cos_input_bucket = getattr(args, 'cos_input_bucket', None)
    cos_input_region = getattr(args, 'cos_input_region', None)
    cos_input_key = getattr(args, 'cos_input_key', None)

    if cos_input_key:
        bucket = cos_input_bucket or get_cos_bucket()
        region = cos_input_region or get_cos_region()
        if not bucket:
            print("Error: COS input requires bucket specification. Please set via --cos-input-bucket parameter or TENCENTCLOUD_COS_BUCKET environment variable",  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
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

    print("Error: Please specify input source:\n"
          "  - URL: --url <URL>\n"
          "  - COS path: --cos-input-key <key> (with environment variables or --cos-input-bucket/--cos-input-region)",
          file=sys.stderr)
    sys.exit(1)


def build_output_storage(args):
    """
    Build output storage information.

    Priority:
    1. Command line parameters --output-bucket / --output-region
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


def has_custom_params(args):
    """Detect if the user has passed any custom transcoding parameters."""
    return any([
        args.codec is not None,
        args.width is not None,
        args.height is not None,
        args.bitrate is not None,
        args.fps is not None,
        args.container is not None,
        args.audio_codec is not None,
        args.audio_bitrate is not None,
        args.scene_type is not None,  # NOCA:E302(function structure required for CLI)


        args.compress_type is not None,
    ])


def build_transcode_task(args):
    """
    Build transcoding task parameters.

    Strategy:
    - If user does not specify any custom parameters → directly use preset template 100305
    - If user specifies custom parameters → build RawParameter based on 100305 defaults, override with user values
    """
    task = {}

    if not has_custom_params(args):
        # Pure preset template mode
        task["Definition"] = PRESET_TEMPLATE_ID
    else:
        # Custom parameter mode: based on preset template default parameters, override with user values
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

        # Scenario-based configuration
        if args.scene_type or args.compress_type:
            video_template["ScenarioBased"] = 1
            if args.scene_type:
                video_template["SceneType"] = args.scene_type
            if args.compress_type:
                video_template["CompressType"] = args.compress_type
        else:
            # Default extreme compression mode
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
                "Type": "TEHD-100",   # TESHD-100 (Video TESHD)
                "MaxVideoBitrate": 0,  # No upper limit, automatically optimized by TESHD
            }
        }

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

    # Output directory: default /output/transcode/, user can override via --output-dir
    params["OutputDir"] = args.output_dir if args.output_dir else "/output/transcode/"

    # Transcoding task
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


def _get_input_url(args):
    """Get input source URL from parameters (for comparison page)."""
    if getattr(args, 'url', None):
        return args.url
    cos_key = getattr(args, 'cos_input_key', None)
    if cos_key:
        bucket = getattr(args, 'cos_input_bucket', None) or get_cos_bucket()
        region = getattr(args, 'cos_input_region', None) or get_cos_region()
        if bucket:
            return f"https://{bucket}.cos.{region}.myqcloud.com/{cos_key.lstrip('/')}"
    return ""


def process_media(args):
    """Initiate TESHD transcoding task."""
    region = args.region or os.environ.get("TENCENTCLOUD_API_REGION", "")

    # 1. Get credentials and client
    cred = get_credentials()
    client = create_mps_client(cred, region)

    # 2. Build request
    params = build_request_params(args)

    if args.dry_run:
        print("=" * 60)
        print("[Dry Run Mode] Only printing request parameters, not actually calling API")
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
        req = models.ProcessMediaRequest()
        req.from_json_string(json.dumps(params))

        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        task_id = result.get('TaskId', 'N/A')
        print("✅ TESHD transcoding task submitted successfully!")
        print(f"   TaskId: {task_id}")
        print(f"\n## TaskId: {task_id}")
        print(f"   RequestId: {result.get('RequestId', 'N/A')}")

        if not has_custom_params(args):
            print(f"   Template: Preset template {PRESET_TEMPLATE_ID} (TESHD-H265-MP4-1080P)")
        else:
            codec = args.codec or PRESET_DEFAULTS["codec"]
            container = args.container or PRESET_DEFAULTS["container"]
            print(f"   Mode: Custom parameters (modified based on {PRESET_TEMPLATE_ID} preset parameters)")
            print(f"   Encoding: {codec.upper()}, Container: {container.upper()}")
            if args.width:
                w = args.width
                h = args.height if args.height else "auto"
                print(f"   Resolution: {w} x {h}")
            if args.bitrate:
                print(f"   Bitrate: {args.bitrate} kbps")
            compress = args.compress_type or "standard_compress"
            print(f"   Compression strategy: {compress}")

        if args.verbose:
            print("\nComplete response:")
            print(json.dumps(result, ensure_ascii=False, indent=2))

        # Auto polling (unless --no-wait specified)
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
                                 title="Video Transcoding Effect Comparison", output_path=compare_path)
        else:
            print()
            print(f"Tip: Task is processing in background, you can use the following command to check progress:")
            print(f"  python scripts/mps_get_video_task.py --task-id {task_id}")

        return result

    except TencentCloudSDKException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS TESHD Transcoding — Maximize compression while maintaining quality, saving bandwidth and storage costs",  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # URL input + default template (TESHD-H265-1080P), output to TENCENTCLOUD_COS_BUCKET/output/transcode/
  python mps_transcode.py --url https://example.com/video.mp4

  # COS path input (recommended, use after local upload)
  python mps_transcode.py --cos-input-bucket mybucket-125xxx \
      --cos-input-region ap-guangzhou --cos-input-key /input/video/test.mp4

  # COS input (bucket and region automatically obtained from environment variables)
  python mps_transcode.py --cos-input-key /input/video/test.mp4

  # Custom 720P + 2Mbps bitrate limit
  python mps_transcode.py --url https://example.com/video.mp4 --width 1280 --height 720 --bitrate 2000

  # Extreme compression mode
  python mps_transcode.py --url https://example.com/video.mp4 --compress-type ultra_compress

  # UGC short video scene optimization
  python mps_transcode.py --url https://example.com/video.mp4 --scene-type ugc

  # Custom output directory (override default /output/transcode/)
  python mps_transcode.py --url https://example.com/video.mp4 --output-dir /custom/

  # Dry Run (only print request parameters)
  python mps_transcode.py --url https://example.com/video.mp4 --dry-run

Environment variables:
  TENCENTCLOUD_SECRET_ID   Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET      COS Bucket name (e.g., mybucket-125xxx, default test_bucket)
  TENCENTCLOUD_COS_REGION      COS Bucket region (default ap-guangzhou)
        """
    )

    # ---- Input source ----
    input_group = parser.add_argument_group("Input source (choose one)")
    input_group.add_argument("--local-file", type=str,
                             help="Local file path, automatically upload to COS then process (requires TENCENTCLOUD_COS_BUCKET configuration)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    input_group.add_argument("--url", type=str, help="Video URL address")

    # COS path input (new version, recommended) - for direct COS path usage after local upload
    input_group.add_argument("--cos-input-bucket", type=str,
                             help="Input COS Bucket name (use with --cos-input-region/--cos-input-key)")
    input_group.add_argument("--cos-input-region", type=str,
                             help="Input COS Bucket region (e.g., ap-guangzhou)")
    input_group.add_argument("--cos-input-key", type=str,
                             help="Input COS object Key (e.g., /input/video.mp4)")

    # ---- Output ----
    output_group = parser.add_argument_group("Output configuration (optional, default output to TENCENTCLOUD_COS_BUCKET/output/transcode/)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    output_group.add_argument("--output-bucket", type=str,
                              help="Output COS Bucket name (default from TENCENTCLOUD_COS_BUCKET environment variable)")
    output_group.add_argument("--output-region", type=str,
                              help="Output COS Bucket region (default from TENCENTCLOUD_COS_REGION environment variable, default ap-guangzhou)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    output_group.add_argument("--output-dir", type=str,
                              help="Output directory (default /output/transcode/), starts and ends with /")
    output_group.add_argument("--output-object-path", type=str,
                              help="Output file path, e.g., /output/{inputName}_transcode.{format}")

    # ---- Video transcoding parameters ----
    video_group = parser.add_argument_group("Video parameters (optional, use preset template 100305 if not specified)")
    video_group.add_argument("--codec", type=str, choices=["h264", "h265", "h266", "av1", "vp9"],
                             help="Video encoding format (default h265)")
    video_group.add_argument("--width", type=int, help="Video width/long side (px), e.g., 1920, 1280, 854")
    video_group.add_argument("--height", type=int, help="Video height/short side (px), 0=scale proportionally")
    video_group.add_argument("--bitrate", type=int,
                             help="Video bitrate (kbps), 0=auto. TESHD automatically optimizes bitrate")
    video_group.add_argument("--fps", type=int, help="Video frame rate (Hz), 0=keep original")
    video_group.add_argument("--container", type=str, choices=["mp4", "hls", "flv", "mp3", "m4a"],
                             help="Container format (default mp4)")

    # ---- Audio parameters ----
    audio_group = parser.add_argument_group("Audio parameters (optional)")
    audio_group.add_argument("--audio-codec", type=str, choices=["aac", "mp3", "copy"],
                             help="Audio encoding format (default aac)")
    audio_group.add_argument("--audio-bitrate", type=int, help="Audio bitrate (kbps), default 128")

    # ---- TESHD strategy ----
    tehd_group = parser.add_argument_group("TESHD strategy (optional)")
    tehd_group.add_argument("--compress-type", type=str,
                            choices=["ultra_compress", "standard_compress", "high_compress", "low_compress"],
                            help="Compression strategy: ultra_compress=extreme compression | standard_compress=comprehensive optimal | "  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
                                 "high_compress=bitrate priority | low_compress=quality priority")
    tehd_group.add_argument("--scene-type", type=str,
                            choices=["normal", "pgc", "materials_video", "ugc",
                                     "e-commerce_video", "educational_video"],
                            help="Video scene: normal=general | pgc=high-definition film/TV | ugc=UGC short video | "
                                 "e-commerce_video=e-commerce | educational_video=education")

    # ---- Other ----
    other_group = parser.add_argument_group("Other configuration")
    other_group.add_argument("--region", type=str, help="MPS service region (default ap-guangzhou)")
    other_group.add_argument("--notify-url", type=str, help="Task completion callback URL")
    other_group.add_argument("--no-wait", action="store_true",
                             help="Only submit task, do not wait for result (default automatically polls until completion)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    other_group.add_argument("--poll-interval", type=int, default=10,
                             help="Polling interval (seconds), default 10")
    other_group.add_argument("--max-wait", type=int, default=1800,
                             help="Maximum wait time (seconds), default 1800 (30 minutes)")
    other_group.add_argument("--verbose", "-v", action="store_true", help="Output detailed information")
    other_group.add_argument("--dry-run", action="store_true", help="Only print request parameters, not actually call API")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    other_group.add_argument("--download-dir", type=str, default=None,
                             help="Automatically download results to specified directory after task completion (default: no download; automatically downloads when path specified)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    other_group.add_argument("--compare", nargs="?", const="auto", default=None, metavar="OUTPUT",
                             help="Automatically generate comparison HTML page after task completion (optionally specify output path, auto-generated by default)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)

    args = parser.parse_args()
    # --url local path automatically converted to local upload mode
    if getattr(args, 'url', None) and not getattr(args, 'local_file', None):
        _val = args.url
        if not _val.startswith('http://') and not _val.startswith('https://'):
            print(f"Tip: '{_val}' source not specified, default to local file processing", file=sys.stderr)
            args.local_file = _val
            args.url = None

    # --local-file mutually exclusive with COS input parameters
    if getattr(args, 'local_file', None):
        cos_conflicts = [x for x in [
            getattr(args, 'cos_input_bucket', None), getattr(args, 'cos_input_key', None)
        ] if x]
        if cos_conflicts:
            parser.error("--local-file cannot be used together with --cos-input-bucket / --cos-input-key")

    # Local file auto upload
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

    # Validate input
    has_url = bool(args.url)
    has_cos_path = bool(getattr(args, 'cos_input_key', None))

    if not has_url and not has_cos_path:
        parser.error("Please specify input source: --url or --cos-input-key (with --cos-input-bucket/--cos-input-region or environment variables)")  # NOCA:line-too-long(content cannot be shortened)

    # Print environment variable information
    cos_bucket_env = get_cos_bucket()
    cos_region_env = get_cos_region()

    # Print execution information
    print("=" * 60)
    print("Tencent Cloud MPS TESHD Transcoding")
    print("=" * 60)
    if args.url:
        print(f"Input: URL - {args.url}")
    else:
        bucket_display = getattr(args, 'cos_input_bucket', None) or cos_bucket_env or "Not set"
        region_display = getattr(args, 'cos_input_region', None) or cos_region_env
        print(f"Input: COS - {bucket_display}:{args.cos_input_key} (region: {region_display})")

    # Output information
    out_bucket = args.output_bucket or cos_bucket_env or "Not set"
    out_region = args.output_region or cos_region_env
    # Set output directory, default /output/transcode/
    out_dir = args.output_dir or "/output/transcode/"
    print(f"Output: COS - {out_bucket}:{out_dir} (region: {out_region})")

    if cos_bucket_env:
        print(f"COS Bucket (environment variable): {cos_bucket_env}")
    else:
        print("❌ TENCENTCLOUD_COS_BUCKET not set. Please configure it before retrying.", file=sys.stderr)
        sys.exit(1)

    if not has_custom_params(args):
        print(f"Template: Preset template {PRESET_TEMPLATE_ID} (TESHD-H265-MP4-1080P)")
    else:
        print("Template: Custom parameters (modified based on preset template 100305)")
    print("-" * 60)

    # Execute
    process_media(args)
if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
