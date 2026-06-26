#!/usr/bin/env python3
"""
Tencent Cloud MPS Highlight Reel Script

Features:
  Use MPS intelligent analysis to automatically capture and generate highlight clips in videos through AI algorithms.
  Supports various scenarios including VLOG, short dramas, football matches, basketball matches, and more.

  ⚠️ Important Notes:
  - This script only supports offline file processing, not live streams
  - ExtendedParameter must be selected from preset scene parameters; custom assembly or field extension is prohibited

  Underlying API: ProcessMedia (offline files)
  Fixed use of intelligent analysis preset template 26 (AiAnalysisTask.Definition=26), custom templates not supported

Preset Scenes (specified via --scene):
  - vlog          VLOG, scenery, drone videos (large model version)
  - vlog-panorama Panoramic camera (with panoramic optimization enabled, large model version)
  - short-drama   Short dramas, TV series, extracts main character appearances/BGM highlights (large model version)
  - football      Football matches, recognizes shots/goals/red-yellow cards/replays (advanced version)
  - basketball    Basketball matches (advanced version)
  - custom        Custom scene, can pass --prompt and --scenario (large model version)

COS Storage Convention:
  Specify COS Bucket name via environment variable TENCENTCLOUD_COS_BUCKET.
  - Default input file path: {TENCENTCLOUD_COS_BUCKET}/input/   (i.e., COS Object starts with /input/)
  - Default output file path: {TENCENTCLOUD_COS_BUCKET}/output/highlight/  (i.e., output directory is
  /output/highlight/)

Usage:
  # Football match highlights
  python mps_highlight.py --cos-input-key /input/football.mp4 --scene football

  # Short drama/TV series highlights
  python mps_highlight.py --cos-input-key /input/drama.mp4 --scene short-drama

  # VLOG panoramic camera
  python mps_highlight.py --url https://example.com/vlog.mp4 --scene vlog-panorama

  # Custom scene (large model version)
  python mps_highlight.py --url https://example.com/skiing.mp4 \
      --scene custom --prompt "skiing scene, output character highlights" --scenario "skiing"

  # Basketball match
  python mps_highlight.py --cos-input-key /input/basketball.mp4 --scene basketball

  # Dry Run (only prints request parameters, does not actually call API)
  python mps_highlight.py --cos-input-key /input/game.mp4 --scene football --dry-run

Environment Variables:
  TENCENTCLOUD_SECRET_ID   - Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  - Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET  - COS Bucket name (e.g., mybucket-125xxx)
  TENCENTCLOUD_COS_REGION  - COS Bucket region (default ap-guangzhou)
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
# Highlight Reel Preset Scene Parameters (fixed values, modification or extension prohibited)
# =============================================================================

# Intelligent analysis template ID (fixed use of preset template 26)
AI_ANALYSIS_DEFINITION = 26

# Preset scene parameter table (Extended Parameter fixed values, dynamic assembly prohibited)
SCENE_PRESETS = {
    "vlog": {
        "desc": "VLOG, scenery, drone videos",
        "version": "Large model version",
        "extended_parameter": {
            "hht": {
                "top_clip": 5,
                "force_cls": 10020,
                "model_segment_limit": [3, 6]
            }
        },
        "allow_top_clip": True,
    },
    "vlog-panorama": {
        "desc": "Panoramic camera (with panoramic optimization enabled)",
        "version": "Large model version",
        "extended_parameter": {
            "hht": {
                "top_clip": 5,
                "force_cls": 10020,
                "model_segment_limit": [3, 6],
                "use_panorama_direct": 1,
                "panorama_video": 1
            }
        },
        "allow_top_clip": True,
    },
    "short-drama": {
        "desc": "Short dramas, TV series, extracts main character appearances/BGM highlights",
        "version": "Large model version",
        "extended_parameter": {
            "hht": {
                "force_cls": "10010",
                "merge_type": 0,
                "need_vad": 1,
                "top_clip": 100,
                "res_save_type": 1,
                "scenario": "TV series highlights"
            }
        },
        "allow_top_clip": False,
    },
    "football": {
        "desc": "Football matches, recognizes shots/goals/red-yellow cards/replays",
        "version": "Advanced version",
        "extended_parameter": {
            "hht": {
                "force_cls": "4001",
                "merge_type": 0,
                "need_vad": 1,
                "top_clip": 100,
                "res_save_type": 1
            }
        },
        "allow_top_clip": False,
    },
    "basketball": {
        "desc": "Basketball matches",
        "version": "Advanced version",
        "extended_parameter": {
            "hht": {
                "force_cls": "4002",
                "merge_type": 0,
                "need_vad": 1,
                "top_clip": 100,
                "res_save_type": 1
            }
        },
        "allow_top_clip": False,
    },
    "custom": {
        "desc": "Custom scene, can pass --prompt and --scenario",
        "version": "Large model version",
        "extended_parameter_template": {
            "hht": {
                "top_clip": 5,
                "force_cls": 10020,
                "prompts": {
                    "multimodal_prompt": "{prompt}"
                },
                "scenario": "{scenario}",
                "model_segment_limit": [3, 6]
            }
        },
        "allow_top_clip": True,
    },
}


def get_cos_bucket():
    """Get COS Bucket name from environment variables."""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """Get COS Bucket region from environment variables, default ap-guangzhou."""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


def get_credentials():
    """Get Tencent Cloud credentials from environment variables. """  # NOCA:line-too-long(line cannot be shortened)
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


def build_extended_parameter(scene, top_clip=None, prompt=None, scenario=None):
    """
    Build ExtendedParameter parameter.

    ⚠️ Strictly retrieve from preset table, dynamic field assembly is prohibited.
    """
    if scene not in SCENE_PRESETS:
        raise ValueError(f"Unknown scene: {scene}")

    preset = SCENE_PRESETS[scene]

    if scene == "custom":
        # Custom scene: Use template to fill prompt and scenario
        template = preset["extended_parameter_template"]
        # Deep copy template
        import copy
        param = copy.deepcopy(template)

        # Fill prompt
        if prompt:
            param["hht"]["prompts"]["multimodal_prompt"] = prompt
        else:
            # If no prompt, remove prompts field
            del param["hht"]["prompts"]

        # Fill scenario
        if scenario:
            param["hht"]["scenario"] = scenario
        else:
            # If no scenario, remove scenario field
            del param["hht"]["scenario"]

        # Process top_clip
        if top_clip is not None and preset.get("allow_top_clip"):
            param["hht"]["top_clip"] = top_clip

        return param
    else:
        # Preset scene: Directly return fixed value
        import copy
        param = copy.deepcopy(preset["extended_parameter"])

        # Process top_clip (only allowed to override in specific scenes)
        if top_clip is not None and preset.get("allow_top_clip"):
            param["hht"]["top_clip"] = top_clip

        return param


def build_ai_analysis_task(args):
    """
    Build AI analysis task parameters (highlight reel).

    Fixed use of preset template 26, specify specific scene through ExtendedParameter.
    """
    # Build Extended Parameter
    extended_param = build_extended_parameter(
        args.scene,
        top_clip=args.top_clip,
        prompt=getattr(args, 'prompt', None),
        scenario=getattr(args, 'scenario', None)
    )

    task = {
        "Definition": AI_ANALYSIS_DEFINITION,
        "ExtendedParameter": json.dumps(extended_param, ensure_ascii=False)
    }

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

    # Output directory: default /output/highlight/
    params["OutputDir"] = args.output_dir if args.output_dir else "/output/highlight/"

    # AI analysis task (highlight reel)
    ai_analysis_task = build_ai_analysis_task(args)
    params["AiAnalysisTask"] = ai_analysis_task

    # Callback configuration
    if args.notify_url:
        params["TaskNotifyConfig"] = {
            "NotifyType": "URL",
            "NotifyUrl": args.notify_url,
        }

    return params


def get_scene_summary(args):
    """Generate scene configuration summary text."""
    items = []
    preset = SCENE_PRESETS.get(args.scene, {})

    items.append(f"🎬 Scene: {args.scene} ({preset.get('desc', '')})")
    items.append(f"📊 Billing version: {preset.get('version', '')}")

    # top_clip information
    if args.top_clip is not None:
        if preset.get("allow_top_clip"):
            items.append(f"🔢 Highlight clip count: Up to {args.top_clip} clips")
        else:
            items.append(f"⚠️ Note: --top-clip parameter does not take effect in {args.scene} scene")

    # Custom scene information
    if args.scene == "custom":
        if getattr(args, 'prompt', None):
            items.append(f"💬 Prompt: {args.prompt}")
        if getattr(args, 'scenario', None):
            items.append(f"📝 Scenario: {args.scenario}")

    return items


def process_media(args):
    """Initiate highlight reel task."""
    region = args.region or os.environ.get("TENCENTCLOUD_API_REGION", "")

    # 1. Get credentials and client
    cred = get_credentials()
    client = create_mps_client(cred, region)

    # 2. Build request
    params = build_request_params(args)

    if args.dry_run:
        print("=" * 60)
        print("[Dry Run mode]Only print request parameters, no actual API call")
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
        print("✅ Highlight reel task submitted successfully!")
        print(f"   TaskId: {task_id}")
        print(f"\n## TaskId: {task_id}")
        print(f"   RequestId: {result.get('RequestId', 'N/A')}")

        # Print scene information
        scene_items = get_scene_summary(args)
        if scene_items:
            print("   Configuration details:")
            for item in scene_items:
                print(f"     {item}")

        print()
        print("⚠️  Note: Highlight reel task processing time is long, please be patient.")

        if args.verbose:
            print("\nComplete response:")
            print(json.dumps(result, ensure_ascii=False, indent=2))

        # Automatic polling (unless specified --no-wait)
        no_wait = getattr(args, 'no_wait', False)
        if not no_wait and _POLL_AVAILABLE and task_id != 'N/A':
            poll_interval = getattr(args, 'poll_interval', 10)
            max_wait = getattr(args, 'max_wait', 1800)  # Highlight reel takes longer, default 30 minutes
            task_result = poll_video_task(task_id, region=region, interval=poll_interval,
                            max_wait=max_wait, verbose=args.verbose)
            # Automatically download results
            download_dir = getattr(args, 'download_dir', None)
            if download_dir and task_result and _POLL_AVAILABLE:
                auto_download_outputs(task_result, download_dir=download_dir)
        else:
            print(f"\nTip: Task is processing in background, you can use the following command to check progress:")
            print(f"  python scripts/mps_get_video_task.py --task-id {task_id}")

        return result

    except TencentCloudSDKException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)


        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS Highlight Reel — AI automatically extracts video highlight clips",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Football match highlight reel
  python mps_highlight.py --cos-input-key /input/football.mp4 --scene football

  # Short drama/video highlight
  python mps_highlight.py --cos-input-key /input/drama.mp4 --scene short-drama

  # VLOG panoramic camera
  python mps_highlight.py --url https://example.com/vlog.mp4 --scene vlog-panorama

  # Custom scene (large model version)
  python mps_highlight.py --url https://example.com/skiing.mp4 \\
      --scene custom --prompt "Skiing scene, output character highlights" --scenario "Skiing"

  # Basketball match
  python mps_highlight.py --cos-input-key /input/basketball.mp4 --scene basketball

  # Specify output clip count (only vlog/vlog-panorama/custom supported)
  python mps_highlight.py --cos-input-key /input/vlog.mp4 --scene vlog --top-clip 10

  # Dry Run (only print request parameters)
  python mps_highlight.py --cos-input-key /input/game.mp4 --scene football --dry-run

Preset scenes (--scene):
  vlog          VLOG, scenery, drone footage (large model version)
  vlog-panorama Panoramic camera (with panorama optimization, large model version)
  short-drama   Short drama, film/TV drama, extracts protagonist appearance/BGM highlights (large model version)
  football      Football match, recognizes shots/goals/red-yellow cards/replays (advanced version)
  basketball    Basketball match (advanced version)
  custom        Custom scene, can pass --prompt and --scenario (large model version)

⚠️ Important notes:
  - This script only supports processing offline files, not live streams
  - --top-clip is only allowed in vlog / vlog-panorama / custom scenes
  - --prompt and --scenario only take effect when --scene custom
  - ExtendedParameter must be selected from preset scene parameters, do not assemble manually

Environment variables:
  TENCENTCLOUD_SECRET_ID   Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET  COS Bucket name
  TENCENTCLOUD_COS_REGION  COS Bucket region (default ap-guangzhou)
        """
    )

    # ---- Input source ----
    input_group = parser.add_argument_group("Input source (choose one)")
    input_group.add_argument("--local-file", type=str,
                             help="Local file path, automatically uploaded to COS for processing (requires TENCENTCLOUD_COS_BUCKET configuration)")  # NOCA:line-too-long(line cannot be shortened)
    input_group.add_argument("--url", type=str, help="Video URL address")

    # COS path input (new version, recommended)
    input_group.add_argument("--cos-input-bucket", type=str,
                             help="Input COS Bucket name")
    input_group.add_argument("--cos-input-region", type=str,
                             help="Input COS Bucket region (e.g., ap-guangzhou)")
    input_group.add_argument("--cos-input-key", type=str,
                             help="Input COS object Key (e.g., /input/video.mp4)")


    # ---- Scene selection (required) ----
    scene_group = parser.add_argument_group("Scene selection (required)")
    scene_group.add_argument(
        "--scene", type=str, required=True,
        choices=list(SCENE_PRESETS.keys()),
        metavar="SCENE",
        help=(
            "Preset scene. Allowed values: "
            "vlog=VLOG scenery | "
            "vlog-panorama=Panoramic camera | "
            "short-drama=Short drama/video | "
            "football=Football match | "
            "basketball=Basketball match | "
            "custom=Custom scene"
        )
    )

    # ---- Custom scene parameters (only for custom scene) ----
    custom_group = parser.add_argument_group("Custom scene parameters (only effective with --scene custom)")
    custom_group.add_argument("--prompt", type=str,
                              help="multimodal_prompt content, describing the highlight content to extract")
    custom_group.add_argument("--scenario", type=str,
                              help="Scene name description")

    # ---- Output ----
    output_group = parser.add_argument_group("Output configuration (optional)")
    output_group.add_argument("--output-bucket", type=str,
                              help="Output COS Bucket name")
    output_group.add_argument("--output-region", type=str,
                              help="Output COS Bucket region")
    output_group.add_argument("--output-dir", type=str,
                              help="Output directory (default /output/highlight/)")
    output_group.add_argument("--output-object-path", type=str,
                              help="Output file path")

    # ---- Highlight configuration ----
    highlight_group = parser.add_argument_group("Highlight configuration")
    highlight_group.add_argument("--top-clip", type=int,
                                 help="Maximum number of highlight clips to output (only available for vlog/vlog-panorama/custom scenes, default 5)")  # NOCA:line-too-long(content cannot be shortened)

    # ---- Other ----
    other_group = parser.add_argument_group("Other configuration")
    other_group.add_argument("--region", type=str, help="MPS service region (default ap-guangzhou)")
    other_group.add_argument("--notify-url", type=str, help="Task completion callback URL")
    other_group.add_argument("--no-wait", action="store_true",
                             help="Only submit task, do not wait for result")
    other_group.add_argument("--poll-interval", type=int, default=10,
                             help="Polling interval (seconds), default 10")
    other_group.add_argument("--max-wait", type=int, default=1800,
                             help="Maximum wait time (seconds), default 1800 (30 minutes)")
    other_group.add_argument("--verbose", "-v", action="store_true", help="Output detailed information")
    other_group.add_argument("--dry-run", action="store_true", help="Only print parameters, do not call API")
    other_group.add_argument("--download-dir", type=str, default=None,
                             help="Automatically download results to specified directory after task completion (default: no download; automatically downloads if path specified)")  # NOCA:line-too-long(line cannot be shortened)

    args = parser.parse_args()
    # --url local path automatically converted to local upload mode
    if getattr(args, 'url', None) and not getattr(args, 'local_file', None):
        _val = args.url
        if not _val.startswith('http://') and not _val.startswith('https://'):
            print(f"Note: '{_val}' not specified as a source, defaulting to local file processing", file=sys.stderr)
            args.local_file = _val
            args.url = None

    # --local-file and COS input parameters are mutually exclusive
    if getattr(args, 'local_file', None):
        cos_conflicts = [x for x in [
            getattr(args, 'cos_input_bucket', None), getattr(args, 'cos_input_key', None)
        ] if x]
        if cos_conflicts:
            parser.error("--local-file cannot be used together with --cos-input-bucket / --cos-input-key")

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

    # ---- Validation ----
    # 1. Input source
    has_url = bool(args.url)
    has_cos_path = bool(getattr(args, 'cos_input_bucket', None) and
                        getattr(args, 'cos_input_region', None) and
                        getattr(args, 'cos_input_key', None))

    if not has_url and not has_cos_path:
        parser.error("Please specify input source: --url or --cos-input-key (with --cos-input-bucket/--cos-input-region or environment variables)")  # NOCA:line-too-long(content cannot be shortened)

    # 2. --top-clip only allowed in specific scenes
    if args.top_clip is not None:
        preset = SCENE_PRESETS.get(args.scene, {})
        if not preset.get("allow_top_clip"):
            allowed_scenes = [s for s, p in SCENE_PRESETS.items() if p.get("allow_top_clip")]
            parser.error(
                f"--top-clip parameter is only available in the following scenes: {', '.join(allowed_scenes)}. "
                f"Current scene '{args.scene}' does not support this parameter."
            )

    # 3. --prompt and --scenario only take effect in custom scene
    if args.prompt and args.scene != "custom":
        parser.error("--prompt only takes effect when --scene custom")
    if args.scenario and args.scene != "custom":
        parser.error("--scenario only takes effect when --scene custom")

    # Print environment variable information
    cos_bucket_env = get_cos_bucket()
    cos_region_env = get_cos_region()

    # Print execution information
    preset = SCENE_PRESETS.get(args.scene, {})
    print("=" * 60)
    print(f"Tencent Cloud MPS Highlight Reel — {preset.get('desc', args.scene)}")
    print("=" * 60)
    if args.url:
        print(f"Input: URL - {args.url}")
    elif getattr(args, 'cos_input_bucket', None):
        print(f"Input: COS - {args.cos_input_bucket}:{args.cos_input_key} (region: {args.cos_input_region})")
    else:
        bucket_display = getattr(args, 'cos_input_bucket', None) or cos_bucket_env or "Not set"
        region_display = getattr(args, 'cos_input_region', None) or cos_region_env
        print(f"Input: COS - {bucket_display}:{args.cos_input_key} (region: {region_display})")

    # Output information
    out_bucket = args.output_bucket or cos_bucket_env or "Not set"
    out_region = args.output_region or cos_region_env
    out_dir = args.output_dir or "/output/highlight/"
    print(f"Output: COS - {out_bucket}:{out_dir} (region: {out_region})")

    if cos_bucket_env:
        print(f"COS Bucket (environment variable): {cos_bucket_env}")
    else:
        print("❌ TENCENTCLOUD_COS_BUCKET not set. Please configure it before retrying.", file=sys.stderr)
        sys.exit(1)

    print(f"Scene: {args.scene} ({preset.get('version', '')})")

    # Print scene configuration
    scene_items = get_scene_summary(args)
    if scene_items:
        print("Configuration details:")
        for item in scene_items:
            print(f"  {item}")

    print()
    print("⚠️  Note: Highlight reel task processing time is long, please be patient.")
    print("-" * 60)

    # Execute
    process_media(args)


if __name__ == "__main__":
    main()
