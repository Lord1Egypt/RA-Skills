#!/usr/bin/env python3
"""
Tencent Cloud MPS Image Inpainting Script

Features:
  Based on an original image and a mask image (RGBA, where the Alpha channel marks the repaint area),
  this script calls the MPS ProcessImage API to start an image inpainting task (ScheduleId=30061),
  repainting the masked area according to the Prompt editing instruction.
  Polls with DescribeImageTaskDetail and returns the output COS path.

  Mask requirement: an RGBA image whose Alpha channel marks the area to repaint.

COS Storage Convention:
  The output COS Bucket name is specified via the TENCENTCLOUD_COS_BUCKET environment variable.
  - Default output directory: /output/repaint/

Usage:
  # Original image URL + mask image URL + prompt (wait for result)
  python scripts/mps_image_repaint.py \
      --url "https://example.com/photo.jpg" \
      --mask-url "https://example.com/mask.png" \
      --prompt "Change the subject's vest color to red"

  # Original image COS path + mask COS path
  python scripts/mps_image_repaint.py \
      --cos-input-key "/input/photo.jpg" \
      --mask-cos-key "/input/mask.png" \
      --prompt "Replace the background with a seaside beach"

  # Local original image file (uploaded to COS automatically) + mask URL
  python scripts/mps_image_repaint.py \
      --local-file ./photo.jpg \
      --mask-url "https://example.com/mask.png" \
      --prompt "Change the skirt into a blue dress"

  # Mask image using an independent Bucket/Region
  python scripts/mps_image_repaint.py \
      --url "https://example.com/photo.jpg" \
      --mask-cos-key "/masks/mask.png" \
      --mask-cos-bucket "other-bucket-125xxx" \
      --mask-cos-region "ap-shanghai" \
      --prompt "Change the wall color to off-white"

  # Submit task only, do not wait for result (returns TaskId)
  python scripts/mps_image_repaint.py \
      --url "https://example.com/photo.jpg" \
      --mask-url "https://example.com/mask.png" \
      --prompt "Replace the vase with a ceramic vase" \
      --no-wait

  # Dry Run (print request payload only, do not call the API)
  python scripts/mps_image_repaint.py \
      --url "https://example.com/photo.jpg" \
      --mask-url "https://example.com/mask.png" \
      --prompt "Replace the chair with a wooden chair" \
      --dry-run

  # Automatically download results after completion
  python scripts/mps_image_repaint.py \
      --url "https://example.com/photo.jpg" \
      --mask-url "https://example.com/mask.png" \
      --prompt "Replace the sky with a starry sky" \
      --download-dir ./output

Environment Variables:
  TENCENTCLOUD_SECRET_ID    - Tencent Cloud SecretId (required)
  TENCENTCLOUD_SECRET_KEY   - Tencent Cloud SecretKey (required)
  TENCENTCLOUD_API_REGION   - MPS API access region (required)
  TENCENTCLOUD_COS_BUCKET   - Output COS Bucket (can be overridden by --output-bucket)
                              Also used as the default Bucket for --cos-input-key / --mask-cos-key
  TENCENTCLOUD_COS_REGION   - Output COS Region (can be overridden by --output-region)
                              Also used as the default Region for --cos-input-key / --mask-cos-key
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
SCHEDULE_ID = 30061
DEFAULT_OUTPUT_DIR = "/output/repaint/"
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
            "Error: COS input requires a Bucket. Please provide it through the corresponding --*-cos-bucket argument or the TENCENTCLOUD_COS_BUCKET environment variable",  # NOCA:line-too-long(line cannot be shortened)
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
    Build a media input source from url or cos_key (choose one).
    URL takes priority; if url is empty, cos_key is used.
    """
    if url:
        return build_url_input(url)
    if cos_key:
        return build_cos_input(cos_key, cos_bucket, cos_region)
    print(f"Error: Please specify the {label} input source (--*-url or --*-cos-key)", file=sys.stderr)
    sys.exit(1)


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
        print("Error: Please specify the original image source (--url, --cos-input-key, or --local-file)", file=sys.stderr)
        sys.exit(1)

    mask_input = build_media_input(
        url=args.mask_url,
        cos_key=args.mask_cos_key,
        cos_bucket=args.mask_cos_bucket,
        cos_region=args.mask_cos_region,
        label="mask image",
    )

    output_bucket = args.output_bucket or get_cos_bucket()
    output_region = args.output_region or get_cos_region()

    if not output_bucket:
        print(
            "Error: Missing output Bucket. Please pass --output-bucket or set TENCENTCLOUD_COS_BUCKET",
            file=sys.stderr,
        )
        sys.exit(1)

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
        "AddOnParameter": {
            "ExtPrompt": [{"Prompt": args.prompt}],
            "ImageSet": [{"Type": "mask", "Image": mask_input}],
        },
    }

    if args.output_path:
        payload["OutputPath"] = args.output_path

    return payload


def submit_process_image(client, payload):
    """Call ProcessImage to submit an inpainting task."""
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
        description="Tencent Cloud MPS Image Inpainting (ProcessImage ScheduleId=30061)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    input_group = parser.add_argument_group("Input source (original image)")
    source_group = input_group.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--url",
        help="Original image URL (choose one of --url / --cos-input-key / --local-file)",
    )
    source_group.add_argument(
        "--cos-input-key",
        help="Original image COS object Key (e.g. /input/photo.jpg), mutually exclusive with --url / --local-file",
    )
    source_group.add_argument(
        "--local-file",
        help="Local path of the original image; uploaded to COS automatically before processing",
    )
    input_group.add_argument(
        "--cos-input-bucket",
        help="Original image COS Bucket (default: reads TENCENTCLOUD_COS_BUCKET)",
    )
    input_group.add_argument(
        "--cos-input-region",
        help="Original image COS Region (default: reads TENCENTCLOUD_COS_REGION)",
    )

    mask_group = parser.add_argument_group("Mask image input (choose one, required)")
    mask_mutex = mask_group.add_mutually_exclusive_group(required=True)
    mask_mutex.add_argument(
        "--mask-url",
        help="Mask image URL (RGBA with Alpha channel marking the repaint area), mutually exclusive with --mask-cos-key",  # NOCA:line-too-long(line cannot be shortened)
    )
    mask_mutex.add_argument(
        "--mask-cos-key",
        help="Mask image COS object Key (e.g. /input/mask.png), mutually exclusive with --mask-url",
    )
    mask_group.add_argument(
        "--mask-cos-bucket",
        help="Mask image COS Bucket (default: reads TENCENTCLOUD_COS_BUCKET)",
    )
    mask_group.add_argument(
        "--mask-cos-region",
        help="Mask image COS Region (default: reads TENCENTCLOUD_COS_REGION)",
    )

    repaint_group = parser.add_argument_group("Inpainting parameters")
    repaint_group.add_argument(
        "--prompt", required=True,
        help="Editing instruction (required), e.g. 'Change the subject\'s vest color to red'",
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
        help="Custom output path (must include file extension, e.g. /output/repaint/result.png)",
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
        "--download-dir",
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

    print("🚀 Submitting inpainting task...")
    if args.url:
        print(f"   Original image: {args.url}")
    else:
        bucket = getattr(args, "cos_input_bucket", None) or get_cos_bucket()
        print(f"   Original image: COS - {bucket}:{args.cos_input_key}")
    if args.mask_url:
        print(f"   Mask image: {args.mask_url}")
    else:
        bucket = args.mask_cos_bucket or get_cos_bucket()
        print(f"   Mask image: COS - {bucket}:{args.mask_cos_key}")
    print(f"   Prompt: {args.prompt}")
    print(f"   Mode: Inpainting (ScheduleId={SCHEDULE_ID})")

    try:
        submit_result = submit_process_image(client, payload)
    except TencentCloudSDKException as e:
        print(f"Error: Failed to submit task - {e}", file=sys.stderr)
        sys.exit(1)

    task_id = submit_result.get("TaskId", "N/A")
    print("✅ Inpainting task submitted successfully!")
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
        print(f"\n❌ Inpainting task failed: ErrCode={task_result.get('ErrCode')}, ErrMsg={err_msg}", file=sys.stderr)
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

    if args.download_dir and _POLL_AVAILABLE:
        auto_download_outputs(task_result, download_dir=args.download_dir)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(1)
