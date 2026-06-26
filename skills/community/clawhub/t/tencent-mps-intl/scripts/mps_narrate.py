#!/usr/bin/env python3
"""
Tencent Cloud MPS AI Narration Remix Script

Features:
  Input original video, automatically complete narration script generation, script matching, AI voiceover, subtitle
  removal, etc. in one stop,
  Output new video with narration script, voiceover, and subtitles.

  Encapsulates ProcessMedia API, fixed use of intelligent analysis preset template 35 (AiAnalysisTask.Definition=35).

Preset scenes (specified via --scene):
  - short-drama          Short drama video with on-screen subtitles (default, includes erasure)
  - short-drama-no-erase Short drama video without on-screen subtitles (erasure disabled)

Default behavior:
  - Erasure (eraseOff): Enabled (eraseOff=0), can be disabled via --no-erase
  - Transition (concatTransition): flashwhite, duration 0.3s
  - Voiceover voice (voiceId): Not specified (uses MPS default system voice), engine fixed to auto
  - Output video count (outputVideoCount): 1, can be specified via --output-count, maximum 5
  - Narration mode (onlyNarration): 1 (pure narration video)
  - Output language (outputLanguage): zh

Multi-episode video support:
  - First episode passed via --url or --cos-input-key
  - Subsequent episodes passed via --extra-urls in order (resolution must match first episode)

COS storage convention:
  COS Bucket name specified via environment variable TENCENTCLOUD_COS_BUCKET.
  - Input file default path: {TENCENTCLOUD_COS_BUCKET}/input/   (COS Object starts with /input/)
  - Output file default path: {TENCENTCLOUD_COS_BUCKET}/output/narrate/ (output directory is /output/narrate/)

Usage:
  # Single episode short drama narration (default with erasure, output 1 video)
  python mps_narrate.py --url https://example.com/drama_ep01.mp4 --scene short-drama

  # COS input (recommended, using --cos-input-key)
  python mps_narrate.py --cos-input-key /input/drama_ep01.mp4 --scene short-drama

  # Three-episode short drama combined narration, output 3 different versions
  python mps_narrate.py \\
      --url https://example.com/ep01.mp4 \\
      --extra-urls https://example.com/ep02.mp4 https://example.com/ep03.mp4 \\
      --scene short-drama \\
      --output-count 3

  # Original video has no subtitles, disable erasure
  python mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama-no-erase

  # Dry Run (preview escaped Extended Parameter)
  python mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama --dry-run

Environment variables:
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
    print("Error: Please install Tencent Cloud SDK first: pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# Preset scene parameters (complete enumeration, no extensions allowed)
# =============================================================================

# Intelligent analysis template ID (fixed use of preset template 35)
AI_ANALYSIS_TEMPLATE_ID = 35

# Preset scene configurations
PRESET_SCENES = {
    "short-drama": {
        "desc": "Short drama video with on-screen subtitles (default, includes erasure)",
        "erase_off": False,
        "extended_param": {
            "reel": {
                "processType": "narrate",
                "narrateParam": {
                    "onlyNarration": 1,
                    "concatTransition": "flashwhite",
                    "concatTransitionDuration": 0.3
                },
                "outputLanguage": "zh",
                "ttsParam": {
                    "engine": "auto"
                }
            }
        }
    },
    "short-drama-no-erase": {
        "desc": "Short drama video without on-screen subtitles (erasure disabled)",
        "erase_off": True,
        "extended_param": {
            "reel": {
                "processType": "narrate",
                "narrateParam": {
                    "onlyNarration": 1,
                    "concatTransition": "flashwhite",
                    "concatTransitionDuration": 0.3
                },
                "outputLanguage": "zh",
                "eraseParam": {
                    "eraseOff": 1
                },
                "ttsParam": {
                    "engine": "auto"
                }
            }
        }
    }
}


def get_cos_bucket():
    """Get COS Bucket name from environment variables."""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """Get COS Bucket region from environment variables, default ap-guangzhou."""
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

    print("Error: Please specify input source:\n"
          "  - URL: --url <URL>\n"
          "  - COS path: --cos-input-key <key> (with environment variables or --cos-input-bucket/--cos-input-region)",
          file=sys.stderr)
    sys.exit(1)


def build_output_storage(args):
    """
    Build output storage information.

    Priority:
    1. Command line arguments --output-bucket / --output-region
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


def build_extended_parameter(scene_config, output_count):
    """
    Build ExtendedParameter.

    Constructs based on preset scene configuration and dynamically injects outputVideoCount.
    """
    extended_param = json.loads(json.dumps(scene_config["extended_param"]))  # Deep copy

    # Dynamically inject output Video Count
    if "reel" not in extended_param:
        extended_param["reel"] = {}
    extended_param["reel"]["outputVideoCount"] = output_count

    return extended_param


def build_request_params(args):
    """Build complete ProcessMedia request parameters."""
    params = {}

    # Input
    params["InputInfo"] = build_input_info(args)

    # Output storage
    output_storage = build_output_storage(args)
    if output_storage:
        params["OutputStorage"] = output_storage

    # Output directory: default /output/narrate/, can be overridden by user via --output-dir
    params["OutputDir"] = args.output_dir if args.output_dir else "/output/narrate/"

    # Get preset scene configuration
    scene_config = PRESET_SCENES[args.scene]

    # Build Extended Parameter
    extended_param = build_extended_parameter(scene_config, args.output_count)
    extended_param_str = json.dumps(extended_param, ensure_ascii=False)

    # AI analysis task (fixed using preset template 35)
    ai_analysis_task = {
        "Definition": AI_ANALYSIS_TEMPLATE_ID,
        "ExtendedParameter": extended_param_str
    }

    params["AiAnalysisTask"] = ai_analysis_task

    # Callback configuration
    if args.notify_url:
        params["TaskNotifyConfig"] = {
            "NotifyType": "URL",
            "NotifyUrl": args.notify_url,
        }

    return params


def process_media(args):
    """Initiate AI narration remix task."""
    region = args.region or os.environ.get("TENCENTCLOUD_API_REGION", "")

    # 1. Get credentials and client
    cred = get_credentials()
    client = create_mps_client(cred, region)

    # 2. Build request
    params = build_request_params(args)

    if args.dry_run:
        print("=" * 60)
        print("[Dry Run mode] Only printing request parameters, not actually calling API")
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
        print("✅ AI narration remix task submitted successfully!")
        print(f"   TaskId: {task_id}")
        print(f"\n## TaskId: {task_id}")
        print(f"   RequestId: {result.get('RequestId', 'N/A')}")
        print(f"   Scene: {args.scene} ({PRESET_SCENES[args.scene]['desc']})")
        print(f"   Output count: {args.output_count}")

        if args.extra_urls:
            print(f"   Input videos: 1 main video + {len(args.extra_urls)} additional videos")
        else:
            print(f"   Input videos: 1")

        if args.verbose:
            print("\nComplete response:")
            print(json.dumps(result, ensure_ascii=False, indent=2))

        # Auto-polling (unless --no-wait specified)
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
            print()
            print(f"Note: Task is processing in the background, you can use the following command to check progress:")
            print(f"  python scripts/mps_get_video_task.py --task-id {task_id}")

        return result

    except TencentCloudSDKException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS AI Narration Remix — Input original video, automatically generate narration script and create narration video",  # NOCA:line-too-long(line cannot be shortened)
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # URL input + default scene (short-drama, including erasure), output to TENCENTCLOUD_COS_BUCKET/output/narrate/
  python mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama

  # COS path input (recommended, use after local upload)
  python mps_narrate.py --cos-input-bucket mybucket-125xxx --cos-input-region ap-guangzhou --cos-input-key
  /input/drama.mp4 --scene short-drama

  # COS input (bucket and region automatically obtained from environment variables)
  python mps_narrate.py --cos-input-key /input/drama.mp4 --scene short-drama

  # Original video has no subtitles, disable erasure
  python mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama-no-erase

  # Multi-episode video combined narration (first episode with --url, subsequent episodes with --extra-urls)
  python mps_narrate.py \\
      --url https://example.com/ep01.mp4 \\
      --extra-urls https://example.com/ep02.mp4 https://example.com/ep03.mp4 \\
      --scene short-drama

  # Output 3 different versions of videos
  python mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama --output-count 3

  # Dry Run (only print request parameters)
  python mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama --dry-run

  # Do not wait for task completion, only submit
  python mps_narrate.py --url https://example.com/drama.mp4 --scene short-drama --no-wait

Preset scenes:
  short-drama          Short drama video, has subtitles on screen (default, includes erasure)
  short-drama-no-erase Short drama video, no subtitles on screen (disable erasure)

Environment variables:
  TENCENTCLOUD_SECRET_ID   Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET       COS Bucket name (e.g., mybucket-125xxx, default test_bucket)
  TENCENTCLOUD_COS_REGION       COS Bucket region (default ap-guangzhou)
        """
    )

    # Input parameters (choose one of three)
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("--local-file", help="Local file path, automatically uploaded to COS then processed (requires TENCENTCLOUD_COS_BUCKET configuration)")  # NOCA:line-too-long(content cannot be shortened)
    input_group.add_argument("--url", help="Input video URL (first episode)")

    # COS path input
    parser.add_argument("--cos-input-bucket", dest="cos_input_bucket", help="COS input Bucket name")
    parser.add_argument("--cos-input-region", dest="cos_input_region", help="COS input Bucket region")
    parser.add_argument("--cos-input-key", dest="cos_input_key", help="COS input Object Key")
    # Multi-episode video support
    parser.add_argument("--extra-urls", nargs="+", help="Episode 2 and subsequent video URLs (in order, resolution must match first episode)")  # NOCA:line-too-long(line cannot be shortened)

    # Scene (required)
    parser.add_argument("--scene", required=True, choices=list(PRESET_SCENES.keys()),
                        help="Preset scene (required)")

    # Output count
    parser.add_argument("--output-count", type=int, default=1,
                        help="Output video count, default 1, maximum 5 (truncated to 5 if exceeds 5)")

    # Output configuration
    parser.add_argument("--output-bucket", dest="output_bucket", help="Output COS Bucket")
    parser.add_argument("--output-region", dest="output_region", help="Output COS Region")
    parser.add_argument("--output-dir", dest="output_dir", help="Output directory (default /output/narrate/)")

    # Other
    parser.add_argument("--region", help="MPS service region (default ap-guangzhou)")
    parser.add_argument("--notify-url", dest="notify_url", help="Callback URL")
    parser.add_argument("--no-wait", action="store_true", help="Only submit task, do not poll and wait")
    parser.add_argument("--poll-interval", type=int, default=10, help="Polling interval (seconds, default 10)")
    parser.add_argument("--max-wait", type=int, default=1800, help="Maximum wait time (seconds, default 1800)")
    parser.add_argument("--dry-run", action="store_true", help="Only print request parameters, not actually call API")
    parser.add_argument("--verbose", "-v", action="store_true", help="Output detailed information")
    parser.add_argument("--download-dir", type=str, default=None,
                        help="Automatically download results to specified directory after task completion (default: do not download; automatically downloads when path is specified)")  # NOCA:line-too-long(content cannot be shortened)

    args = parser.parse_args()
    # --url local path automatically converted to local upload mode
    if getattr(args, 'url', None) and not getattr(args, 'local_file', None):
        _val = args.url
        if not _val.startswith('http://') and not _val.startswith('https://'):
            print(f"Note: '{_val}' source not specified, defaulting to local file processing", file=sys.stderr)
            args.local_file = _val
            args.url = None

    # --local-file mutually exclusive with COS input parameters
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

    # Parameter validation
    if args.output_count < 1:
        print("Error: --output-count must be greater than or equal to 1", file=sys.stderr)
        sys.exit(1)
    if args.output_count > 5:
        print(f"Warning: --output-count exceeds maximum value 5, truncated to 5", file=sys.stderr)
        args.output_count = 5

    # Multi-episode video notice
    if args.extra_urls:
        print(f"Note: Multi-episode video mode, total {len(args.extra_urls) + 1} videos")
        print(f"  Episode 1 (main video): {args.url or getattr(args, 'cos_input_key', None)}")
        for i, url in enumerate(args.extra_urls, 2):
            print(f"  Episode {i}: {url}")
        print("  Note: All video resolutions must be consistent\n")

    process_media(args)
if __name__ == "__main__":
    main()
