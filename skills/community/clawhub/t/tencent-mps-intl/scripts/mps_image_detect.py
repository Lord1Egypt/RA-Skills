#!/usr/bin/env python3
"""
Tencent Cloud MPS Object Detection and Object Description Script

Features:
  Calls the MPS ProcessImage API to start an object detection and object description task,
  configured through StdExtInfo.ObjectDetectDescribeConfig.
  Supports two detection modes: text-based target prompts (Prompt) and point-based detection (Point).
  At least one mode must be provided.
  Polls with DescribeImageTaskDetail and returns the detection result JSON.

  Supported capabilities:
    - Text target detection: detect objects described in natural language
    - Point-based detection: detect objects based on coordinates in the image
    - Natural language description: generate text descriptions for detected objects
    - Cutout return: return transparent-background PNG files for detected objects

COS Storage Convention:
  The output COS Bucket name is specified via the TENCENTCLOUD_COS_BUCKET environment variable.
  - Default output directory: /output/object-detect/

Usage:
  # Text target detection (detect cats)
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "cat"

  # Multiple detection targets
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "cat" --prompt "dog"

  # Point-based detection
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --point "100,200"

  # Multiple detection points
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --point "100,200" --point "500,300"

  # Mixed text + point detection
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "cat" --point "100,200"

  # Enable natural language description
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "cat" --describe

  # Return cutout file (transparent PNG)
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "cat" --return-cutout

  # Set max result count and confidence threshold
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "person" --top-k 5 --confidence-threshold 0.8

  # Use English prompt and English output descriptions
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "cat" --prompt-language en --description-language en --describe

  # Use COS path input
  python scripts/mps_image_detect.py \
      --cos-input-key "/input/photo.jpg" \
      --prompt "cat"

  # Use a local file (uploaded to COS automatically)
  python scripts/mps_image_detect.py \
      --local-file ./photo.jpg \
      --prompt "cat" --describe

  # Submit task only, do not wait for result (returns TaskId)
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "cat" --no-wait

  # Dry Run (print request payload only, do not call the API)
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "cat" --dry-run

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
    from mps_poll_task import poll_image_task, auto_upload_local_file
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
DEFAULT_OUTPUT_DIR = "/output/object-detect/"
DEFAULT_TOP_K = 1
DEFAULT_CONFIDENCE_THRESHOLD = 0.5
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


def parse_point(point_str):
    """Parse a point string in the form 'X,Y' and return {"X": int, "Y": int}."""
    parts = point_str.strip().split(",")
    if len(parts) != 2:
        print(f"Error: Point format must be 'X,Y', got '{point_str}'", file=sys.stderr)
        sys.exit(2)
    try:
        return {"X": int(parts[0].strip()), "Y": int(parts[1].strip())}
    except ValueError:
        print(f"Error: Point values must be integers, got '{point_str}'", file=sys.stderr)
        sys.exit(2)


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
        print("Error: Please specify an input source (--url, --cos-input-key, or --local-file)", file=sys.stderr)
        sys.exit(1)

    detect_config = {
        "TopK": args.top_k,
        "ConfidenceThreshold": args.confidence_threshold,
        "SkipDescribe": not args.describe,
        "ReturnCutout": args.return_cutout,
        "PromptLanguage": args.prompt_language,
        "DescriptionLanguage": args.description_language,
    }
    if args.prompt:
        detect_config["Prompts"] = args.prompt
    if args.point:
        detect_config["Points"] = [parse_point(p) for p in args.point]

    std_ext_info = json.dumps(
        {"ObjectDetectDescribeConfig": detect_config},
        ensure_ascii=False,
        separators=(",", ":"),
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
        "ImageTask": {"EncodeConfig": {"Format": "PNG"}},
        "StdExtInfo": std_ext_info,
    }

    if args.output_path:
        payload["OutputPath"] = args.output_path

    return payload


def submit_process_image(client, payload):
    """Call ProcessImage to submit an object detection and description task."""
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
        description="Tencent Cloud MPS Object Detection and Object Description (ProcessImage + ObjectDetectDescribeConfig)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    input_group = parser.add_argument_group("Input source")
    input_group.add_argument(
        "--url",
        help="Image URL (choose one of --url / --cos-input-key / --local-file)",
    )
    input_group.add_argument(
        "--cos-input-key",
        help="Input COS object Key (e.g. /input/photo.jpg), mutually exclusive with --url / --local-file",
    )
    input_group.add_argument(
        "--cos-input-bucket",
        help="Input COS Bucket (default: reads TENCENTCLOUD_COS_BUCKET)",
    )
    input_group.add_argument(
        "--cos-input-region",
        help="Input COS Region (default: reads TENCENTCLOUD_COS_REGION)",
    )
    input_group.add_argument(
        "--local-file",
        help="Local file path; uploaded to COS automatically before processing (requires TENCENTCLOUD_COS_BUCKET)",
    )

    detect_group = parser.add_argument_group("Detection parameters")
    detect_group.add_argument(
        "--prompt", action="append",
        help="Text detection target, can be repeated (e.g. --prompt cat --prompt dog). At least one of --prompt or --point is required",  # NOCA:line-too-long(line cannot be shortened)
    )
    detect_group.add_argument(
        "--point", action="append",
        help="Point-based detection in 'X,Y' format, can be repeated (e.g. --point 100,200). At least one of --prompt or --point is required",  # NOCA:line-too-long(line cannot be shortened)
    )
    detect_group.add_argument(
        "--top-k", type=int, default=DEFAULT_TOP_K,
        help=f"Maximum number of results to return (default: {DEFAULT_TOP_K}, range: 1-20)",
    )
    detect_group.add_argument(
        "--confidence-threshold", type=float, default=DEFAULT_CONFIDENCE_THRESHOLD,
        help=f"Confidence threshold (default: {DEFAULT_CONFIDENCE_THRESHOLD}, range: 0-1)",
    )
    detect_group.add_argument(
        "--describe", action="store_true",
        help="Enable natural language description",
    )
    detect_group.add_argument(
        "--return-cutout", action="store_true",
        help="Return cutout file (transparent PNG)",
    )
    detect_group.add_argument(
        "--prompt-language", choices=["zh", "en"], default="zh",
        help="Language of input prompts (default: zh)",
    )
    detect_group.add_argument(
        "--description-language", choices=["zh", "en"], default="zh",
        help="Language of output descriptions (default: zh)",
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
        help="Custom output path (must include file extension, e.g. /output/object-detect/result.png)",
    )

    task_group = parser.add_argument_group("Task control")
    task_group.add_argument(
        "--no-wait", action="store_true",
        help="Submit the task only and return after TaskId is received",
    )
    task_group.add_argument(
        "--dry-run", action="store_true",
        help="Print the request payload only without calling the API",
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

    input_count = sum([
        bool(args.url),
        bool(args.cos_input_key),
        bool(args.local_file),
    ])
    if input_count == 0:
        parser.error("Please specify an input source: --url, --cos-input-key, or --local-file")
    if input_count > 1:
        parser.error("--url, --cos-input-key, and --local-file are mutually exclusive; please choose only one")

    if not args.prompt and not args.point:
        parser.error("Please specify at least one detection mode: --prompt or --point")

    if args.top_k < 1 or args.top_k > 20:
        parser.error("--top-k must be in the range 1-20")

    if args.confidence_threshold < 0 or args.confidence_threshold > 1:
        parser.error("--confidence-threshold must be in the range 0-1")

    return args


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

    print("🚀 Submitting object detection and description task...")
    if args.url:
        print(f"   Input: {args.url}")
    else:
        bucket = getattr(args, "cos_input_bucket", None) or get_cos_bucket()
        print(f"   Input: COS - {bucket}:{args.cos_input_key}")
    if args.prompt:
        for p in args.prompt:
            print(f"   Prompt: {p}")
    if args.point:
        for pt in args.point:
            print(f"   Point: {pt}")
    print(f"   TopK: {args.top_k}, Confidence threshold: {args.confidence_threshold}")
    if args.describe:
        print("   Description: enabled")
    if args.return_cutout:
        print("   Cutout return: enabled")

    try:
        submit_result = submit_process_image(client, payload)
    except TencentCloudSDKException as e:
        print(f"Error: Failed to submit task - {e}", file=sys.stderr)
        sys.exit(1)

    task_id = submit_result.get("TaskId", "N/A")
    print("✅ Object detection and description task submitted successfully!")
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
        print(f"\n❌ Object detection task failed: ErrCode={task_result.get('ErrCode')}, ErrMsg={err_msg}", file=sys.stderr)
        sys.exit(1)

    result_items = task_result.get("ImageProcessTaskResultSet") or []
    detections = []
    outputs = []

    for item in result_items:
        output = item.get("Output") or {}
        content_str = output.get("Content", "")
        try:
            content_data = json.loads(content_str) if content_str else {}
        except (json.JSONDecodeError, TypeError):
            content_data = {"raw": content_str}

        detection = {
            "status": item.get("Status"),
            "detection": content_data,
        }

        err = item.get("ErrMsg", "")
        if err:
            detection["err_msg"] = err

        if output.get("Path"):
            storage = (output.get("OutputStorage") or {}).get("CosOutputStorage") or {}
            path = output.get("Path", "")
            bucket = storage.get("Bucket", "")
            region_out = storage.get("Region", "")
            cutout_info = {
                "bucket": bucket,
                "region": region_out,
                "path": path,
                "cos_uri": f"cos://{bucket}{path}" if bucket and path else None,
                "url": f"https://{bucket}.cos.{region_out}.myqcloud.com{path}" if bucket and path else None,
            }
            detection["cutout"] = cutout_info
            outputs.append(cutout_info)

        detections.append(detection)

    final_result = {
        "TaskId": task_id,
        "Status": task_result.get("Status"),
        "CreateTime": task_result.get("CreateTime"),
        "FinishTime": task_result.get("FinishTime"),
        "Detections": detections,
    }
    if outputs:
        final_result["Outputs"] = outputs

    print(json.dumps(final_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(1)
