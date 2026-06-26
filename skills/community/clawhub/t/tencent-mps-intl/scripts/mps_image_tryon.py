#!/usr/bin/env python3
"""
Tencent Cloud MPS Image Try-On Script

Features:
  Based on a model image and clothing image(s), this script calls the MPS ProcessImage API to initiate an AI try-on
  task,
  polls for results via DescribeImageTaskDetail, and returns the output COS path.

  Supported try-on scenarios (specified via --schedule-id):
    - 30100: Regular clothing try-on (default, supports 1-2 clothing images)
    - 30101: Underwear try-on (supports only 1 clothing image)

COS Storage Convention:
  The output COS Bucket name is specified via the TENCENTCLOUD_COS_BUCKET environment variable.
  - Default output directory: /output/tryon/

Usage:
  # Minimal usage: model image + clothing image (URL, default waits for result)
  python scripts/mps_image_tryon.py \
      --model-url "https://example.com/model.jpg" \
      --cloth-url "https://example.com/cloth.jpg"

  # Model image using COS path input
  python scripts/mps_image_tryon.py \
      --model-cos-key "/input/model.jpg" \
      --cloth-url "https://example.com/cloth.jpg"

  # Model image + clothing image both using COS path input
  python scripts/mps_image_tryon.py \
      --model-cos-key "/input/model.jpg" \
      --cloth-cos-key "/input/cloth.jpg"

  # Clothing image using COS, specifying non-default Bucket
  python scripts/mps_image_tryon.py \
      --model-url "https://example.com/model.jpg" \
      --cloth-cos-key "/input/cloth.jpg" \
      --cloth-cos-bucket mybucket-125xxx --cloth-cos-region ap-shanghai

  # Multiple clothing images (front + back)
  python scripts/mps_image_tryon.py \
      --model-url "https://example.com/model.jpg" \
      --cloth-url "https://example.com/cloth-front.jpg" \
      --cloth-url "https://example.com/cloth-back.jpg"

  # Underwear scenario (supports only 1 clothing image)
  python scripts/mps_image_tryon.py \
      --model-url "https://example.com/model.jpg" \
      --cloth-url "https://example.com/underwear.jpg" \
      --schedule-id 30101

  # Additional prompt + random seed
  python scripts/mps_image_tryon.py \
      --model-url "https://example.com/model.jpg" \
      --cloth-url "https://example.com/cloth.jpg" \
      --ext-prompt "shirt buttons open" \
      --random-seed 48

  # Submit task only, do not wait for result (returns TaskId)
  python scripts/mps_image_tryon.py \
      --model-url "https://example.com/model.jpg" \
      --cloth-url "https://example.com/cloth.jpg" \
      --no-wait

  # Specify output Bucket and directory
  python scripts/mps_image_tryon.py \
      --model-url "https://example.com/model.jpg" \
      --cloth-url "https://example.com/cloth.jpg" \
      --output-bucket mybucket-125xxx --output-region ap-shanghai \
      --output-dir /custom/output/

Environment Variables:
  TENCENTCLOUD_SECRET_ID    - Tencent Cloud SecretId (required)
  TENCENTCLOUD_SECRET_KEY   - Tencent Cloud SecretKey (required)
  TENCENTCLOUD_API_REGION   - MPS API access region (optional, default ap-guangzhou)
  TENCENTCLOUD_COS_BUCKET   - Output COS Bucket (can be overridden by --output-bucket)
                              Also serves as default Bucket for --model-cos-key / --cloth-cos-key
  TENCENTCLOUD_COS_REGION   - Output COS Region (can be overridden by --output-region)
                              Also serves as default Region for --model-cos-key / --cloth-cos-key
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
    print("Error: Please install Tencent Cloud SDK first: pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# Default parameters
# =============================================================================
DEFAULT_SCHEDULE_ID = 30100
DEFAULT_OUTPUT_DIR = "/output/tryon/"
DEFAULT_FORMAT = "JPEG"
DEFAULT_IMAGE_SIZE = "2K"
DEFAULT_QUALITY = 85
DEFAULT_POLL_INTERVAL = 10
DEFAULT_TIMEOUT = 600


# =============================================================================
# Utility functions
# =============================================================================

def get_credentials():
    """Get Tencent Cloud credentials from environment variables; attempt auto-load if missing."""
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
    """Get output COS Bucket name from environment variables."""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """Get output COS Region from environment variables, default ap-guangzhou."""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


def create_mps_client(cred, region):
    """Create MPS client."""
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return mps_client.MpsClient(cred, region, client_profile)


def build_url_input(url):
    """Construct URL type input source."""
    return {
        "Type": "URL",
        "UrlInputInfo": {"Url": url},
    }


def build_cos_input(cos_key, cos_bucket=None, cos_region=None):
    """Construct COS type input source."""
    bucket = cos_bucket or get_cos_bucket()
    region = cos_region or get_cos_region()
    if not bucket:
        print(
            "Error: COS input requires Bucket specification; please set via corresponding --*-cos-bucket parameter or TENCENTCLOUD_COS_BUCKET environment variable",  # NOCA:line-too-long(content cannot be shortened)
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


def build_media_input(url=None, cos_key=None, cos_bucket=None, cos_region=None, label="Image"):
    """
    Construct media input source based on url or cos_key (mutually exclusive).
    Prefer url; if url is empty, use cos_key.
    """
    if url:
        return build_url_input(url)
    if cos_key:
        return build_cos_input(cos_key, cos_bucket, cos_region)
    print(f"Error: Please specify {label} input source (--*-url or --*-cos-key)", file=sys.stderr)
    sys.exit(1)


def build_request_payload(args):
    """Assemble ProcessImage request body."""
    # Collect clothing image list (merge url and cos-key, maintain order)
    cloth_inputs = []
    for url in (args.cloth_url or []):
        cloth_inputs.append(build_url_input(url))
    for key in (args.cloth_cos_key or []):
        cloth_inputs.append(build_cos_input(key, args.cloth_cos_bucket, args.cloth_cos_region))

    if not cloth_inputs:
        print("Error: Please specify at least one clothing image (--cloth-url or --cloth-cos-key)", file=sys.stderr)
        sys.exit(1)

    if args.schedule_id == 30101 and len(cloth_inputs) != 1:
        print("Error: Underwear scenario (--schedule-id 30101) currently supports only 1 clothing image", file=sys.stderr)  # NOCA:line-too-long(line cannot be shortened)
        sys.exit(1)

    addon_parameter = {
        "ImageSet": [{"Image": inp} for inp in cloth_inputs],
        "OutputConfig": {
            "Format": args.format,
            "ImageSize": args.image_size,
            "Quality": args.quality,
        },
    }

    if args.ext_prompt:
        addon_parameter["ExtPrompt"] = [{"Prompt": p} for p in args.ext_prompt]

    output_bucket = args.output_bucket or get_cos_bucket()
    output_region = args.output_region or get_cos_region()

    if not output_bucket:
        print(
            "Error: Missing output Bucket; please provide --output-bucket or set TENCENTCLOUD_COS_BUCKET",
            file=sys.stderr,
        )
        sys.exit(1)

    # Construct model image input
    model_input = build_media_input(
        url=args.model_url,
        cos_key=args.model_cos_key,
        cos_bucket=args.model_cos_bucket,
        cos_region=args.model_cos_region,
        label="Model image",
    )

    payload = {
        "InputInfo": model_input,
        "OutputStorage": {
            "Type": "COS",
            "CosOutputStorage": {
                "Bucket": output_bucket,
                "Region": output_region,
            },
        },
        "OutputDir": args.output_dir,
        "ScheduleId": args.schedule_id,
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
    """Submit ProcessImage request for outfit change task."""
    req = models.ProcessImageRequest()
    req.from_json_string(json.dumps(payload, ensure_ascii=False))
    resp = client.ProcessImage(req)
    result = json.loads(resp.to_json_string())
    # Compatible with SDK return format
    if "Response" in result:
        result = result["Response"]
    return result


# =============================================================================
# Parameter parsing
# =============================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS Image Try-On (ProcessImage ScheduleId=30100/30101)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Input parameters
    input_group = parser.add_argument_group("Input parameters")
    # Model image (URL or COS, choose one)
    model_group = input_group.add_mutually_exclusive_group(required=True)
    model_group.add_argument(
        "--model-url",
        help="Model image URL (mutually exclusive with --model-cos-key)",
    )
    model_group.add_argument(
        "--model-cos-key",
        help="Model image COS object Key (e.g., /input/model.jpg), mutually exclusive with --model-url",
    )
    input_group.add_argument(
        "--model-cos-bucket",
        help="Model image COS Bucket (default reads TENCENTCLOUD_COS_BUCKET)",
    )
    input_group.add_argument(
        "--model-cos-region",
        help="Model image COS Region (default reads TENCENTCLOUD_COS_REGION)",
    )
    # Clothing image (URL or COS, at least one, can be mixed)
    input_group.add_argument(
        "--cloth-url", action="append", default=[],
        help="Clothing image URL, can be repeated 1-2 times; can be mixed with --cloth-cos-key",
    )
    input_group.add_argument(
        "--cloth-cos-key", action="append", default=[],
        help="Clothing image COS object Key, can be repeated 1-2 times; can be mixed with --cloth-url",
    )
    input_group.add_argument(
        "--cloth-cos-bucket",
        help="Clothing image COS Bucket (default reads TENCENTCLOUD_COS_BUCKET)",
    )
    input_group.add_argument(
        "--cloth-cos-region",
        help="Clothing image COS Region (default reads TENCENTCLOUD_COS_REGION)",
    )

    # Try-on parameters
    tryon_group = parser.add_argument_group("Try-on parameters")
    tryon_group.add_argument(
        "--schedule-id", type=int, default=DEFAULT_SCHEDULE_ID,
        help="Try-on scene ID: 30100=regular clothing (default), 30101=underwear",
    )
    tryon_group.add_argument(
        "--ext-prompt", action="append",
        help="Additional prompt words, can be repeated multiple times (e.g., 'shirt buttons open')",
    )
    tryon_group.add_argument(
        "--random-seed", type=int,
        help="Random seed (StdExtInfo.ModelConfig.RandomSeed), fixed seed yields stable style",
    )
    tryon_group.add_argument(
        "--resource-id",
        help="Optional resource ID (business-side exclusive resource)",
    )

    # Output parameters
    output_group = parser.add_argument_group("Output parameters")
    output_group.add_argument(
        "--output-bucket",
        help="Output COS Bucket (default reads TENCENTCLOUD_COS_BUCKET)",
    )
    output_group.add_argument(
        "--output-region",
        help="Output COS Region (default reads TENCENTCLOUD_COS_REGION)",
    )
    output_group.add_argument(
        "--output-dir", default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default {DEFAULT_OUTPUT_DIR})",
    )
    output_group.add_argument(
        "--output-path",
        help="Custom output path (must include file extension, e.g., /output/tryon/result.jpg)",
    )
    output_group.add_argument(
        "--format", choices=["JPEG", "PNG"], default=DEFAULT_FORMAT,
        help="Output format (default JPEG)",
    )
    output_group.add_argument(
        "--image-size", choices=["1K", "2K", "4K"], default=DEFAULT_IMAGE_SIZE,
        help="Output size (default 2K)",
    )
    output_group.add_argument(
        "--quality", type=int, default=DEFAULT_QUALITY,
        help="Output quality 1-100 (default 85)",
    )

    # Task control
    task_group = parser.add_argument_group("Task control")
    task_group.add_argument(
        "--no-wait", action="store_true",
        help="Only submit task, do not wait for result (exit after returning TaskId)",
    )
    task_group.add_argument(
        "--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL,
        help=f"Polling interval in seconds (default {DEFAULT_POLL_INTERVAL})",
    )
    task_group.add_argument(
        "--timeout", type=int, default=DEFAULT_TIMEOUT,
        help=f"Maximum wait time in seconds (default {DEFAULT_TIMEOUT})",
    )

    # Authentication and region
    auth_group = parser.add_argument_group("Authentication and region")
    auth_group.add_argument(
        "--region",
        default=os.environ.get("TENCENTCLOUD_API_REGION", ""),
        help="MPS API access region (default reads TENCENTCLOUD_API_REGION, otherwise ap-guangzhou)",
    )
    auth_group.add_argument(
        "--secret-id",
        help="Tencent Cloud SecretId (if not provided, reads environment variable TENCENTCLOUD_SECRET_ID)",
    )
    auth_group.add_argument(
        "--secret-key",
        help="Tencent Cloud SecretKey (if not provided, reads environment variable TENCENTCLOUD_SECRET_KEY)",
    )

    args = parser.parse_args()

    # Validation: at least one clothing image
    if not args.cloth_url and not args.cloth_cos_key:
        parser.error("Please specify at least one clothing image: --cloth-url or --cloth-cos-key")

    return args


# =============================================================================
# Main workflow
# =============================================================================

def main():
    args = parse_args()

    # Command-line secrets override environment variables
    if args.secret_id:
        os.environ["TENCENTCLOUD_SECRET_ID"] = args.secret_id
    if args.secret_key:
        os.environ["TENCENTCLOUD_SECRET_KEY"] = args.secret_key

    cred = get_credentials()
    region = args.region
    client = create_mps_client(cred, region)

    payload = build_request_payload(args)

    print("🚀 Submitting image try-on task...")
    # Print model image source
    if args.model_url:
        print(f"   Model image: {args.model_url}")
    else:
        bucket = args.model_cos_bucket or get_cos_bucket()
        print(f"   Model image: COS - {bucket}:{args.model_cos_key}")
    # Print clothing image sources
    idx = 1
    for url in (args.cloth_url or []):
        print(f"   Clothing image {idx}: {url}")
        idx += 1
    for key in (args.cloth_cos_key or []):
        bucket = args.cloth_cos_bucket or get_cos_bucket()
        print(f"   Clothing image {idx}: COS - {bucket}:{key}")
        idx += 1
    print(f"   Scene ScheduleId: {args.schedule_id}")

    try:
        submit_result = submit_process_image(client, payload)
    except TencentCloudSDKException as e:
        print(f"Error: Task submission failed - {e}", file=sys.stderr)
        sys.exit(1)

    task_id = submit_result.get("TaskId", "N/A")
    print("✅ Image try-on task submitted successfully!")
    print(f"   TaskId: {task_id}")
    print(f"   RequestId: {submit_result.get('RequestId', 'N/A')}")
    print(f"\n## TaskId: {task_id}")

    if args.no_wait:
        print(json.dumps({"TaskId": task_id, "RequestId": submit_result.get("RequestId")},
                         ensure_ascii=False, indent=2))
        return

    # Poll for result
    if not _POLL_AVAILABLE:
        print("⚠️  Polling module unavailable, please query manually:", file=sys.stderr)
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
        print(f"\n⚠️  Polling timeout, task may still be processing.", file=sys.stderr)
        print(f"   Manual query available: python scripts/mps_get_image_task.py --task-id {task_id}", file=sys.stderr)
        sys.exit(1)

    # Output final result
    err_msg = task_result.get("ErrMsg") or ""
    if err_msg:
        print(f"\n❌ Try-on task failed: ErrCode={task_result.get('ErrCode')}, ErrMsg={err_msg}", file=sys.stderr)
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


[To-dos]


[To-dos]
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(1)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(1)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(1)
