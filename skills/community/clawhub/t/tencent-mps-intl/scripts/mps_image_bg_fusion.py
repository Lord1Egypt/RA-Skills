#!/usr/bin/env python3
"""
Tencent Cloud MPS AI Background Fusion/Generation Script

Features:
  Based on a subject image (foreground/product/main subject) and background image, calls the MPS ProcessImage API
  to initiate an AI background fusion task, or passes only the subject image + Prompt description
  to automatically generate a new background (background generation mode).
  Polls via DescribeImageTaskDetail to wait for results, returns the output COS path.

  Supports two modes (both use ScheduleId=30060):
    - Background Fusion: Pass subject image + background image, fuse the subject into the specified background scene
    - Background Generation: Pass only subject image + Prompt, automatically generate a new background (no background
    image)

COS Storage Convention:
  The output COS Bucket name is specified via the TENCENTCLOUD_COS_BUCKET environment variable.
  - Default output directory: /output/bgfusion/

Usage:
  # Background fusion (subject + background image, wait for result)
  python scripts/mps_image_bg_fusion.py \\
      --subject-url "https://example.com/product.jpg" \\
      --bg-url "https://example.com/background.jpg"

  # Background fusion + additional Prompt
  python scripts/mps_image_bg_fusion.py \\
      --subject-url "https://example.com/product.jpg" \\
      --bg-url "https://example.com/background.jpg" \\
      --prompt "Replace the leaves in the background with yellow"

  # Background generation (only subject + Prompt, no background image)
  python scripts/mps_image_bg_fusion.py \\
      --subject-url "https://example.com/product.jpg" \\
      --prompt "Minimalist white marble tabletop, soft natural light"

  # Subject image using COS path input
  python scripts/mps_image_bg_fusion.py \\
      --subject-cos-key "/input/product.jpg" \\
      --bg-url "https://example.com/background.jpg"

  # Subject + background image both using COS path input
  python scripts/mps_image_bg_fusion.py \\
      --subject-cos-key "/input/product.jpg" \\
      --bg-cos-key "/input/background.jpg"

  # Background generation + fixed random seed
  python scripts/mps_image_bg_fusion.py \\
      --subject-url "https://example.com/product.jpg" \\
      --prompt "Modern minimalist living room background" \\
      --random-seed 42

  # Submit task only, don't wait for result (returns TaskId)
  python scripts/mps_image_bg_fusion.py \\
      --subject-url "https://example.com/product.jpg" \\
      --prompt "Minimalist white marble tabletop" \\
      --no-wait

  # Specify output format and size
  python scripts/mps_image_bg_fusion.py \\
      --subject-url "https://example.com/product.jpg" \\
      --prompt "Outdoor lawn, sunny day" \\
      --format PNG --image-size 4K

Environment Variables:
  TENCENTCLOUD_SECRET_ID    - Tencent Cloud SecretId (required)
  TENCENTCLOUD_SECRET_KEY   - Tencent Cloud SecretKey (required)
  TENCENTCLOUD_API_REGION   - MPS API region (optional, default: ap-guangzhou)
  TENCENTCLOUD_COS_BUCKET   - Output COS Bucket (can be overridden by --output-bucket)
                              Also serves as default Bucket for --subject-cos-key / --bg-cos-key
  TENCENTCLOUD_COS_REGION   - Output COS Region (can be overridden by --output-region)
                              Also serves as default Region for --subject-cos-key / --bg-cos-key
"""

import argparse
import json
import os
import sys
from mps_auto_upgrade import check_sdk_version

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)

try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False

try:
    from mps_poll_task import poll_image_task
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
# Default Parameters
# =============================================================================
SCHEDULE_ID = 30060  # Fixed ScheduleId for AI background fusion/generation
DEFAULT_OUTPUT_DIR = "/output/bgfusion/"
DEFAULT_FORMAT = "JPEG"
DEFAULT_IMAGE_SIZE = "2K"
DEFAULT_QUALITY = 85
DEFAULT_POLL_INTERVAL = 10
DEFAULT_TIMEOUT = 600


# =============================================================================
# Utility Functions
# =============================================================================

def get_credentials():
    """Get Tencent Cloud credentials from environment variables, try auto-loading if missing."""
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


def get_cos_bucket():
    """Get the output COS Bucket name from environment variables."""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """Get the output COS Region from environment variables, default: ap-guangzhou."""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


def create_mps_client(cred, region):
    """Create an MPS client."""
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return mps_client.MpsClient(cred, region, client_profile)


def build_url_input(url):
    """Build URL type input source."""
    return {
        "Type": "URL",
        "UrlInputInfo": {"Url": url},
    }


def build_cos_input(cos_key, cos_bucket=None, cos_region=None):
    """Build COS type input source."""
    bucket = cos_bucket or get_cos_bucket()
    region = cos_region or get_cos_region()
    if not bucket:
        print(
            "Error: COS input requires a Bucket. Please specify via the corresponding --*-cos-bucket argument or TENCENTCLOUD_COS_BUCKET environment variable",  # NOCA:line-too-long(line cannot be shortened)
            file=sys.stderr,
        )
        sys.exit(1)
    return {
        "Type": "COS",
        "CosInputInfo": {
            "Bucket": bucket,
            "Region": region,
            "Object": cos_key if cos_key.startswith("/") else f"/{cos_key}",
        },
    }


def build_media_input(url=None, cos_key=None, cos_bucket=None, cos_region=None, label="image"):
    """
    Build media input source from url or cos_key (choose one).
    URL takes priority; if url is empty, cos_key is used.
    """
    if url:
        return build_url_input(url)
    if cos_key:
        return build_cos_input(cos_key, cos_bucket, cos_region)
    print(f"Error: Please specify the {label} input source (--*-url or --*-cos-key)", file=sys.stderr)
    sys.exit(1)


def build_request_payload(args):
    """Assemble the ProcessImage request body."""
    addon_parameter = {
        "OutputConfig": {
            "Format": args.format,
            "ImageSize": args.image_size,
            "Quality": args.quality,
        },
    }

    # ExtPrompt: required in background generation mode, optional in background fusion mode
    if args.prompt:
        addon_parameter["ExtPrompt"] = [{"Prompt": p} for p in args.prompt]

    # ImageSet: background fusion mode when background image is provided
    if args.bg_url or args.bg_cos_key:
        image_set = []
        if args.bg_url:
            image_set.append({"Image": build_url_input(args.bg_url)})
        elif args.bg_cos_key:
            image_set.append({
                "Image": build_cos_input(args.bg_cos_key, args.bg_cos_bucket, args.bg_cos_region)
            })
        addon_parameter["ImageSet"] = image_set

    output_bucket = args.output_bucket or get_cos_bucket()
    output_region = args.output_region or get_cos_region()

    if not output_bucket:
        print(
            "Error: Missing output Bucket. Please pass --output-bucket or set TENCENTCLOUD_COS_BUCKET",
            file=sys.stderr,
        )
        sys.exit(1)

    # Build subject image input
    subject_input = build_media_input(
        url=args.subject_url,
        cos_key=args.subject_cos_key,
        cos_bucket=args.subject_cos_bucket,
        cos_region=args.subject_cos_region,
        label="subject image",
    )

    payload = {
        "InputInfo": subject_input,
        "OutputStorage": {
            "Type": "COS",
            "CosOutputStorage": {
                "Bucket": output_bucket,
                "Region": output_region,
            },
        },
        "OutputDir": args.output_dir,
        "ScheduleId": SCHEDULE_ID,
        "AddOnParameter": addon_parameter,
    }

    if args.output_path:
        payload["OutputPath"] = args.output_path

    if args.resource_id:
        payload["ResourceId"] = args.resource_id

    if args.random_seed is not None:
        payload["StdExtInfo"] = json.dumps(
            {"ModelConfig": {"RandomSeed": args.random_seed}},
            ensure_ascii=False,
            separators=(",", ":"),
        )

    return payload


def submit_process_image(client, payload):
    """Call ProcessImage to submit a background fusion/generation task."""
    req = models.ProcessImageRequest()
    req.from_json_string(json.dumps(payload, ensure_ascii=False))
    resp = client.ProcessImage(req)
    result = json.loads(resp.to_json_string())
    # Compatible with SDK response format
    if "Response" in result:
        result = result["Response"]
    return result


# =============================================================================
# Argument Parsing
# =============================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS AI Background Fusion/Generation (ProcessImage ScheduleId=30060)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Input parameters
    input_group = parser.add_argument_group("Input parameters")
    # Subject image (URL or COS, choose one)
    subject_group = input_group.add_mutually_exclusive_group(required=True)
    subject_group.add_argument(
        "--subject-url",
        help="Subject (foreground/product/main) image URL (mutually exclusive with --subject-cos-key)",
    )
    subject_group.add_argument(
        "--subject-cos-key",
        help="Subject image COS object Key (e.g. /input/product.jpg), mutually exclusive with --subject-url",
    )
    input_group.add_argument(
        "--subject-cos-bucket",
        help="Subject image COS Bucket (default: reads TENCENTCLOUD_COS_BUCKET)",
    )
    input_group.add_argument(
        "--subject-cos-region",
        help="Subject image COS Region (default: reads TENCENTCLOUD_COS_REGION)",
    )
    # Background image (URL or COS, choose one; omit for background generation mode)
    bg_group = input_group.add_mutually_exclusive_group()
    bg_group.add_argument(
        "--bg-url",
        help="Background image URL; omit for background generation mode (mutually exclusive with --bg-cos-key)",
    )
    bg_group.add_argument(
        "--bg-cos-key",
        help="Background image COS object Key (e.g. /input/bg.jpg), mutually exclusive with --bg-url",
    )
    input_group.add_argument(
        "--bg-cos-bucket",
        help="Background image COS Bucket (default: reads TENCENTCLOUD_COS_BUCKET)",
    )
    input_group.add_argument(
        "--bg-cos-region",
        help="Background image COS Region (default: reads TENCENTCLOUD_COS_REGION)",
    )

    # Fusion/generation parameters
    fusion_group = parser.add_argument_group("Fusion/generation parameters")
    fusion_group.add_argument(
        "--prompt", action="append",
        help="Background description or fusion requirement prompt, can be specified multiple times; required in background generation mode",  # NOCA:line-too-long(content cannot be shortened)
    )
    fusion_group.add_argument(
        "--random-seed", type=int,
        help="Random seed (StdExtInfo.ModelConfig.RandomSeed), fixed seed produces consistent style",
    )
    fusion_group.add_argument(
        "--resource-id",
        help="Optional resource ID (business-specific resource)",
    )

    # Output parameters
    output_group = parser.add_argument_group("Output parameters")
    output_group.add_argument(
        "--output-bucket",
        help="Output COS Bucket (default: reads TENCENTCLOUD_COS_BUCKET)",
    )
    output_group.add_argument(
        "--output-region",
        help="Output COS Region (default: reads TENCENTCLOUD_COS_REGION)",
    )
    output_group.add_argument(
        "--output-dir", default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    output_group.add_argument(
        "--output-path",
        help="Custom output path (must include file extension, e.g. /output/bgfusion/result.jpg)",
    )
    output_group.add_argument(
        "--format", choices=["JPEG", "PNG"], default=DEFAULT_FORMAT,
        help="Output format (default: JPEG)",
    )
    output_group.add_argument(
        "--image-size", choices=["1K", "2K", "4K"], default=DEFAULT_IMAGE_SIZE,
        help="Output size (default: 2K)",
    )
    output_group.add_argument(
        "--quality", type=int, default=DEFAULT_QUALITY,
        help="Output quality 1-100 (default: 85)",
    )

    # Task control
    task_group = parser.add_argument_group("Task control")
    task_group.add_argument(
        "--no-wait", action="store_true",
        help="Submit task only, don't wait for result (exit after returning TaskId)",
    )
    task_group.add_argument(
        "--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL,
        help=f"Polling interval in seconds (default: {DEFAULT_POLL_INTERVAL})",
    )
    task_group.add_argument(
        "--timeout", type=int, default=DEFAULT_TIMEOUT,
        help=f"Maximum wait time in seconds (default: {DEFAULT_TIMEOUT})",
    )

    # Authentication and region
    auth_group = parser.add_argument_group("Authentication and region")
    auth_group.add_argument(
        "--region",
        default=os.environ.get("TENCENTCLOUD_API_REGION", ""),
        help="MPS API region (default: reads TENCENTCLOUD_API_REGION, otherwise ap-guangzhou)",
    )
    auth_group.add_argument(
        "--secret-id",
        help="Tencent Cloud SecretId (reads env var TENCENTCLOUD_SECRET_ID if not provided)",
    )
    auth_group.add_argument(
        "--secret-key",
        help="Tencent Cloud SecretKey (reads env var TENCENTCLOUD_SECRET_KEY if not provided)",
    )

    args = parser.parse_args()

    # In background generation mode, prompt is required
    if not args.bg_url and not args.bg_cos_key and not args.prompt:
        parser.error("In background generation mode (when no background image is provided), --prompt is required to describe the background to generate")  # NOCA:line-too-long(line cannot be shortened)

    return args


# =============================================================================
# Main Flow
# =============================================================================

def main():
    args = parse_args()

    # Command line secrets override environment variables
    if args.secret_id:
        os.environ["TENCENTCLOUD_SECRET_ID"] = args.secret_id
    if args.secret_key:
        os.environ["TENCENTCLOUD_SECRET_KEY"] = args.secret_key

    cred = get_credentials()
    region = args.region
    client = create_mps_client(cred, region)

    payload = build_request_payload(args)

    # Determine mode
    has_bg = bool(args.bg_url or args.bg_cos_key)
    mode = "Background Fusion" if has_bg else "Background Generation"

    print(f"🚀 Submitting {mode} task...")
    # Print subject image source
    if args.subject_url:
        print(f"   Subject: {args.subject_url}")
    else:
        bucket = args.subject_cos_bucket or get_cos_bucket()
        print(f"   Subject: COS - {bucket}:{args.subject_cos_key}")
    # Print background image source
    if has_bg:
        if args.bg_url:
            print(f"   Background: {args.bg_url}")
        else:
            bucket = args.bg_cos_bucket or get_cos_bucket()
            print(f"   Background: COS - {bucket}:{args.bg_cos_key}")
    # Print Prompt
    if args.prompt:
        for p in args.prompt:
            print(f"   Prompt: {p}")
    print(f"   Mode: {mode} (ScheduleId={SCHEDULE_ID})")

    try:
        submit_result = submit_process_image(client, payload)
    except TencentCloudSDKException as e:
        print(f"Error: Failed to submit task - {e}", file=sys.stderr)
        sys.exit(1)

    task_id = submit_result.get("TaskId", "N/A")
    print(f"✅ {mode} task submitted successfully!")
    print(f"   TaskId: {task_id}")
    print(f"   RequestId: {submit_result.get('RequestId', 'N/A')}")
    print(f"\n## TaskId: {task_id}")

    if args.no_wait:
        print(json.dumps({"TaskId": task_id, "RequestId": submit_result.get("RequestId")},
                         ensure_ascii=False, indent=2))
        return

    # Poll and wait for result
    if not _POLL_AVAILABLE:
        print("⚠️  Polling module not available, please query manually:", file=sys.stderr)
        print(f"   python scripts/mps_get_image_task.py --task-id {task_id}", file=sys.stderr)
        print(json.dumps({"TaskId": task_id}, ensure_ascii=False, indent=2))
        return

    task_result = poll_image_task(
        task_id=task_id,
        region=region,
        interval=args.poll_interval,
        max_wait=args.timeout,
        verbose=False,
    )

    if task_result is None:
        print(f"\n⚠️  Polling timed out, task may still be processing.", file=sys.stderr)
        print(f"   You can query manually: python scripts/mps_get_image_task.py --task-id {task_id}", file=sys.stderr)
        sys.exit(1)

    # Output final result
    err_msg = task_result.get("ErrMsg") or ""
    if err_msg:
        print(f"\n❌ {mode} task failed: ErrCode={task_result.get('ErrCode')}, ErrMsg={err_msg}", file=sys.stderr)
        sys.exit(1)

    # Extract output paths
    outputs = []
    for item in task_result.get("ImageProcessTaskResultSet") or []:
        output = item.get("Output") or {}
        storage = (output.get("OutputStorage") or {}).get("CosOutputStorage") or {}
        path = output.get("Path", "")
        bucket = storage.get("Bucket", "")
        region_out = storage.get("Region", "")
        outputs.append({
            "bucket": bucket,
            "region": region_out,
            "path": path,
            "cos_uri": f"cos://{bucket}{path}" if bucket and path else None,
            "url": f"https://{bucket}.cos.{region_out}.myqcloud.com{path}" if bucket and path else None,
        })

    final_result = {
        "TaskId": task_id,
        "Status": task_result.get("Status"),
        "CreateTime": task_result.get("CreateTime"),
        "FinishTime": task_result.get("FinishTime"),
        "Outputs": outputs,
    }

    print(json.dumps(final_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(1)
