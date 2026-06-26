#!/usr/bin/env python3
"""
Tencent Cloud MPS Storyboard Split / Grid Split Script

Features:
  Based on the input image (comic/storyboard/grid image), this script calls the MPS ProcessImage API
  to start a storyboard split task, automatically splitting multi-panel comic or storyboard images
  into independent single images.
  Polls with DescribeImageTaskDetail and returns the output COS path.

  Uses ScheduleId=30050 and supports three split scenarios:
    - AI drama storyboard split (model-sampling=0.1, default)
    - Comic / long-strip storyboard split (model-sampling=1.0)
    - E-commerce grid split (model-sampling=0.85, text preservation recommended)

COS Storage Convention:
  The output COS Bucket name is specified via the TENCENTCLOUD_COS_BUCKET environment variable.
  - Default output directory: /output/split/

Usage:
  # AI drama storyboard split (default mode, model-sampling=0.1, erase text)
  python scripts/mps_image_split.py \
      --url "https://example.com/storyboard.jpg"

  # Comic storyboard split (model-sampling=1.0)
  python scripts/mps_image_split.py \
      --url "https://example.com/manga_page.jpg" \
      --model-sampling 1.0

  # E-commerce grid split (model-sampling=0.85, preserve text)
  python scripts/mps_image_split.py \
      --url "https://example.com/ecommerce_grid.jpg" \
      --model-sampling 0.85 --no-erase-text

  # Extract only image index 0 (0-based index)
  python scripts/mps_image_split.py \
      --url "https://example.com/storyboard.jpg" \
      --process-index 0

  # Use COS path input
  python scripts/mps_image_split.py \
      --cos-input-key "/input/manga.jpg"

  # Use a local file (uploaded to COS automatically)
  python scripts/mps_image_split.py \
      --local-file ./storyboard.png

  # Submit task only, do not wait for result (returns TaskId)
  python scripts/mps_image_split.py \
      --url "https://example.com/storyboard.jpg" \
      --no-wait

  # Dry Run (print request payload only, do not call the API)
  python scripts/mps_image_split.py \
      --url "https://example.com/storyboard.jpg" \
      --dry-run

  # Automatically download results after completion
  python scripts/mps_image_split.py \
      --url "https://example.com/storyboard.jpg" \
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
SCHEDULE_ID = 30050
DEFAULT_OUTPUT_DIR = "/output/split/"
DEFAULT_MODEL_SAMPLING = 0.1
DEFAULT_POLL_INTERVAL = 10
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
        input_info = build_cos_input(
            args.cos_input_key,
            getattr(args, "cos_input_bucket", None),
            getattr(args, "cos_input_region", None),
        )
    else:
        print("Error: Please specify an input source (--url or --cos-input-key)", file=sys.stderr)
        sys.exit(1)

    output_bucket = args.output_bucket or get_cos_bucket()
    output_region = args.output_region or get_cos_region()

    if not output_bucket:
        print(
            "Error: Missing output Bucket. Please pass --output-bucket or set TENCENTCLOUD_COS_BUCKET",
            file=sys.stderr,
        )
        sys.exit(1)

    storyboard_config = {
        "EraseText": args.erase_text,
        "ModelSamplingAuraFlow": args.model_sampling,
    }
    if args.process_index is not None:
        storyboard_config["ProcessIndex"] = args.process_index

    std_ext_info = json.dumps(
        {"StoryboardConfig": storyboard_config},
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
    """Call ProcessImage to submit a storyboard split task."""
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
        description="Tencent Cloud MPS Storyboard Split / Grid Split (ProcessImage ScheduleId=30050)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    input_group = parser.add_argument_group("Input source (choose one)")
    input_mutex = input_group.add_mutually_exclusive_group(required=True)
    input_mutex.add_argument(
        "--url",
        help="Image URL (choose one of --url / --cos-input-key / --local-file)",
    )
    input_mutex.add_argument(
        "--cos-input-key",
        help="COS object Key (e.g. /input/storyboard.jpg), mutually exclusive with --url / --local-file",
    )
    input_mutex.add_argument(
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

    split_group = parser.add_argument_group("Split parameters")
    split_group.add_argument(
        "--process-index", type=int, default=None,
        help="Specify the extracted image index (0-based). If omitted, all panels are extracted",
    )
    split_group.add_argument(
        "--erase-text", action="store_true", default=True, dest="erase_text",
        help="Erase text (enabled by default)",
    )
    split_group.add_argument(
        "--no-erase-text", action="store_false", dest="erase_text",
        help="Preserve text (recommended for e-commerce scenarios)",
    )
    split_group.add_argument(
        "--model-sampling", type=float, default=DEFAULT_MODEL_SAMPLING,
        metavar="FLOAT",
        help="Split effect control parameter: 0.1=AI drama storyboard (default), 1.0=comic storyboard, 0.85=e-commerce with text preserved",  # NOCA:line-too-long(line cannot be shortened)
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
        help="Custom output path (must include file extension, e.g. /output/split/result.jpg)",
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
    task_group.add_argument(
        "--download-dir", type=str, default=None,
        help="Automatically download outputs to the specified directory after completion",
    )

    auth_group = parser.add_argument_group("Authentication and region")
    auth_group.add_argument(
        "--region",
        default=os.environ.get("TENCENTCLOUD_API_REGION", ""),
        help="MPS API access region (default: reads TENCENTCLOUD_API_REGION, otherwise ap-guangzhou)",
    )

    return parser.parse_args()


# =============================================================================
# Main Flow
# =============================================================================

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def main():
    args = parse_args()

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
        args.url = None

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

    sampling_desc = {0.1: "AI drama storyboard", 1.0: "Comic storyboard", 0.85: "E-commerce grid"}
    mode_desc = sampling_desc.get(args.model_sampling, f"Custom({args.model_sampling})")

    print("🚀 Submitting storyboard split task...")
    if args.url:
        print(f"   Input: {args.url}")
    elif args.cos_input_key:
        bucket = getattr(args, "cos_input_bucket", None) or get_cos_bucket()
        print(f"   Input: COS - {bucket}:{args.cos_input_key}")
    print(f"   Mode: {mode_desc} (ScheduleId={SCHEDULE_ID}, ModelSampling={args.model_sampling})")
    print(f"   Erase text: {'yes' if args.erase_text else 'no'}")
    if args.process_index is not None:
        print(f"   Extract image index: {args.process_index}")
    else:
        print("   Extraction scope: all panels")

    try:
        submit_result = submit_process_image(client, payload)
    except TencentCloudSDKException as e:
        print(f"Error: Failed to submit task - {e}", file=sys.stderr)
        sys.exit(1)

    task_id = submit_result.get("TaskId", "N/A")
    print("✅ Storyboard split task submitted successfully!")
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
        print(f"\n❌ Storyboard split task failed: ErrCode={task_result.get('ErrCode')}, ErrMsg={err_msg}", file=sys.stderr)
        sys.exit(1)

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

    if args.download_dir and outputs and _POLL_AVAILABLE:
        auto_download_outputs(task_result, download_dir=args.download_dir)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(1)
