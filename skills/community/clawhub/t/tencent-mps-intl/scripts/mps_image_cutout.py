#!/usr/bin/env python3
"""
Tencent Cloud MPS Precise Cutout Script

Features:
  Calls the MPS ProcessImage API to start a precise cutout task (ScheduleId=30030),
  accurately separates the foreground subject from the background of the input image,
  and outputs a PNG image with transparency.
  Polls with DescribeImageTaskDetail and returns the output COS path.

  Supports three tunable cutout parameters (passed through StdExtInfo):
    - TransparencyThreshold: pixels with Alpha below this value become fully transparent
    - OpaqueThreshold: pixels with Alpha above this value become fully opaque
    - EdgeSamplingStep: edge color sampling step; lower values are recommended for finer boundaries

COS Storage Convention:
  The output COS Bucket name is specified via the TENCENTCLOUD_COS_BUCKET environment variable.
  - Default output directory: /output/cutout/

Usage:
  # Minimal usage: URL input, wait for result
  python scripts/mps_image_cutout.py \
      --url "https://example.com/photo.jpg"

  # Use COS path input
  python scripts/mps_image_cutout.py \
      --cos-input-key "/input/photo.jpg"

  # Use a local file (uploaded to COS automatically before processing)
  python scripts/mps_image_cutout.py \
      --local-file ./photo.jpg

  # Custom cutout parameters
  python scripts/mps_image_cutout.py \
      --url "https://example.com/photo.jpg" \
      --transparency-threshold 20 \
      --opaque-threshold 150 \
      --edge-sampling-step 2

  # Submit task only, do not wait for result (returns TaskId)
  python scripts/mps_image_cutout.py \
      --url "https://example.com/photo.jpg" \
      --no-wait

  # Dry Run (print request payload only, do not call the API)
  python scripts/mps_image_cutout.py \
      --url "https://example.com/photo.jpg" \
      --dry-run

  # Automatically download the result after completion
  python scripts/mps_image_cutout.py \
      --url "https://example.com/photo.jpg" \
      --download-dir ./output

Environment Variables:
  TENCENTCLOUD_SECRET_ID    - Tencent Cloud SecretId (required)
  TENCENTCLOUD_SECRET_KEY   - Tencent Cloud SecretKey (required)
  TENCENTCLOUD_API_REGION   - MPS API access region (required)
  TENCENTCLOUD_COS_BUCKET   - Output COS Bucket (can be overridden by --output-bucket)
                              Also used as the default Bucket for --cos-input-key
  TENCENTCLOUD_COS_REGION   - Output COS Region (can be overridden by --output-region)
                              Also used as the default Region for --cos-input-key
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
    from mps_poll_task import poll_image_task, auto_upload_local_file, auto_download_outputs
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
SCHEDULE_ID = 30030
DEFAULT_OUTPUT_DIR = "/output/cutout/"
DEFAULT_TRANSPARENCY_THRESHOLD = 30
DEFAULT_OPAQUE_THRESHOLD = 127
DEFAULT_EDGE_SAMPLING_STEP = 5
DEFAULT_POLL_INTERVAL = 5
DEFAULT_TIMEOUT = 300


# =============================================================================
# Utility Functions
# =============================================================================

def get_credentials():
    """Get Tencent Cloud credentials from environment variables, try auto-loading if missing."""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] Environment variables are not set, attempting automatic loading from system files...", file=sys.stderr)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
        if not secret_id or not secret_key:
            if _LOAD_ENV_AVAILABLE:
                from mps_load_env import _print_setup_hint
                _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            else:
                print(
                    "\nError: TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY is not set.\n"
                    "Please add these variables to ~/.env, ~/.profile, or similar files.\n",
                    file=sys.stderr,
                )
            sys.exit(1)
    return credential.Credential(secret_id, secret_key)


def get_cos_bucket():
    """Get output COS Bucket name from environment variables."""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """Get output COS Region from environment variables."""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


def create_mps_client(cred, region):
    """Create MPS client."""
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return mps_client.MpsClient(cred, region, client_profile)


def build_url_input(url):
    """Build URL input source."""
    return {
        "Type": "URL",
        "UrlInputInfo": {"Url": url},
    }


def build_cos_input(cos_key, cos_bucket=None, cos_region=None):
    """Build COS input source."""
    bucket = cos_bucket or get_cos_bucket()
    region = cos_region or get_cos_region()
    if not bucket:
        print(
            "Error: COS input requires a Bucket. Please provide it through --cos-input-bucket or the TENCENTCLOUD_COS_BUCKET environment variable",  # NOCA:line-too-long(line cannot be shortened)
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


def build_request_payload(args):
    """Assemble the ProcessImage request payload."""
    if args.url:
        input_info = build_url_input(args.url)
    elif args.cos_input_key:
        input_info = build_cos_input(args.cos_input_key, args.cos_input_bucket, args.cos_input_region)
    else:
        print("Error: Please specify an input source (--url, --cos-input-key, or --local-file)", file=sys.stderr)
        sys.exit(1)

    output_bucket = args.output_bucket or get_cos_bucket()
    output_region = args.output_region or get_cos_region()

    if not output_bucket:
        print(
            "Error: Missing output Bucket. Please pass --output-bucket or set TENCENTCLOUD_COS_BUCKET",
            file=sys.stderr,
        )
        sys.exit(1)

    std_ext_info = json.dumps(
        {
            "CutoutConfig": {
                "TransparencyThreshold": args.transparency_threshold,
                "OpaqueThreshold": args.opaque_threshold,
                "EdgeSamplingStep": args.edge_sampling_step,
            }
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )

    payload = {
        "InputInfo": input_info,
        "OutputStorage": {
            "Type": "COS",
            "CosOutputStorage": {
                "Bucket": output_bucket,
                "Region": output_region,
            },
        },
        "OutputDir": args.output_dir,
        "ScheduleId": SCHEDULE_ID,
        "StdExtInfo": std_ext_info,
    }

    if args.output_path:
        payload["OutputPath"] = args.output_path

    return payload


def submit_process_image(client, payload):
    """Call ProcessImage to submit a precise cutout task."""
    req = models.ProcessImageRequest()
    req.from_json_string(json.dumps(payload, ensure_ascii=False))
    resp = client.ProcessImage(req)
    result = json.loads(resp.to_json_string())
    if "Response" in result:
        result = result["Response"]
    return result


# =============================================================================
# Argument Parsing
# =============================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS Precise Cutout (ProcessImage ScheduleId=30030)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    input_group = parser.add_argument_group("Input source (choose one: --url / --cos-input-key / --local-file)")
    source_group = input_group.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--url",
        help="Input image URL (choose one of --url / --cos-input-key / --local-file)",
    )
    source_group.add_argument(
        "--cos-input-key",
        help="Input image COS object Key (e.g. /input/photo.jpg), mutually exclusive with --url / --local-file",
    )
    source_group.add_argument(
        "--local-file",
        help="Local file path; uploaded to COS automatically before processing (requires TENCENTCLOUD_COS_BUCKET)",
    )
    input_group.add_argument(
        "--cos-input-bucket",
        help="Input COS Bucket (default: reads TENCENTCLOUD_COS_BUCKET)",
    )
    input_group.add_argument(
        "--cos-input-region",
        help="Input COS Region (default: reads TENCENTCLOUD_COS_REGION)",
    )

    cutout_group = parser.add_argument_group("Cutout parameters (CutoutConfig)")
    cutout_group.add_argument(
        "--transparency-threshold", type=int, default=DEFAULT_TRANSPARENCY_THRESHOLD,
        help=f"Transparency threshold: pixels with Alpha below this become fully transparent (default: {DEFAULT_TRANSPARENCY_THRESHOLD})",
    )
    cutout_group.add_argument(
        "--opaque-threshold", type=int, default=DEFAULT_OPAQUE_THRESHOLD,
        help=f"Opaque threshold: pixels with Alpha above this become fully opaque (default: {DEFAULT_OPAQUE_THRESHOLD})",
    )
    cutout_group.add_argument(
        "--edge-sampling-step", type=int, default=DEFAULT_EDGE_SAMPLING_STEP,
        help=f"Edge color sampling step (default: {DEFAULT_EDGE_SAMPLING_STEP}). Lowering it to around 2 can reduce edge bleeding for finer boundaries",  # NOCA:line-too-long(line cannot be shortened)
    )

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
        help="Custom output path (must include file extension, e.g. /output/cutout/result.png)",
    )
    output_group.add_argument(
        "--download-dir",
        help="Automatically download outputs to the specified directory after completion",
    )

    task_group = parser.add_argument_group("Task control")
    task_group.add_argument(
        "--dry-run", action="store_true",
        help="Print the request payload only without calling the API",
    )
    task_group.add_argument(
        "--no-wait", action="store_true",
        help="Submit the task only and return after TaskId is received",
    )
    task_group.add_argument(
        "--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL,
        help=f"Polling interval in seconds (default: {DEFAULT_POLL_INTERVAL})",
    )
    task_group.add_argument(
        "--timeout", type=int, default=DEFAULT_TIMEOUT,
        help=f"Maximum wait time in seconds (default: {DEFAULT_TIMEOUT})",
    )

    auth_group = parser.add_argument_group("Authentication and region")
    auth_group.add_argument(
        "--region",
        default=os.environ.get("TENCENTCLOUD_API_REGION", ""),
        help="MPS API access region (default: reads TENCENTCLOUD_API_REGION, otherwise ap-guangzhou)",
    )

    args = parser.parse_args()

    if args.local_file:
        if not _POLL_AVAILABLE:
            print("Error: --local-file requires mps_poll_task module support", file=sys.stderr)
            sys.exit(1)
        upload_result = auto_upload_local_file(args.local_file)
        if not upload_result:
            sys.exit(1)
        args.cos_input_key = upload_result["Key"]
        args.cos_input_bucket = upload_result["Bucket"]
        args.cos_input_region = upload_result["Region"]

    return args


# =============================================================================
# Main Flow
# =============================================================================

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def main():
    args = parse_args()

    cred = get_credentials()
    region = args.region
    client = create_mps_client(cred, region)

    payload = build_request_payload(args)

    if args.dry_run:
        print("=" * 60)
        print("[Dry Run] Printing request payload only, API will not be called")
        print("=" * 60)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print("🚀 Submitting precise cutout task...")
    if args.url:
        print(f"   Input: {args.url}")
    elif args.cos_input_key:
        bucket = args.cos_input_bucket or get_cos_bucket()
        print(f"   Input: COS - {bucket}:{args.cos_input_key}")
    print(f"   ScheduleId: {SCHEDULE_ID} (precise cutout)")
    print(f"   Transparency threshold: {args.transparency_threshold}")
    print(f"   Opaque threshold: {args.opaque_threshold}")
    print(f"   Edge sampling step: {args.edge_sampling_step}")

    try:
        submit_result = submit_process_image(client, payload)
    except TencentCloudSDKException as e:
        print(f"Error: Failed to submit task - {e}", file=sys.stderr)
        sys.exit(1)

    task_id = submit_result.get("TaskId", "N/A")
    print("✅ Precise cutout task submitted successfully!")
    print(f"   TaskId: {task_id}")
    print(f"   RequestId: {submit_result.get('RequestId', 'N/A')}")
    print(f"\n## TaskId: {task_id}")

    if args.no_wait:
        print(json.dumps({"TaskId": task_id, "RequestId": submit_result.get("RequestId")}, ensure_ascii=False, indent=2))
        return

    if not _POLL_AVAILABLE:
        print("⚠️  Polling module is unavailable. Please query manually:", file=sys.stderr)
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
        print("\n⚠️  Polling timed out. The task may still be processing.", file=sys.stderr)
        print(f"   You can query it manually: python scripts/mps_get_image_task.py --task-id {task_id}", file=sys.stderr)
        sys.exit(1)

    err_msg = task_result.get("ErrMsg") or ""
    if err_msg:
        print(f"\n❌ Cutout task failed: ErrCode={task_result.get('ErrCode')}, ErrMsg={err_msg}", file=sys.stderr)
        sys.exit(1)

    if args.download_dir and _POLL_AVAILABLE:
        auto_download_outputs(task_result, download_dir=args.download_dir)

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
