#!/usr/bin/env python3
"""
Tencent Cloud MPS Image Processing Task Query Script

Features:
  Query the execution status and result details of image processing tasks submitted via ProcessImage by task ID.
  Tasks submitted within the last 7 days can be queried.

  Supports querying the overall task status (WAITING / PROCESSING / FINISH), as well as
  the execution results, output file paths, signed URLs, and image-to-text content of each sub-task.

Usage:
  # Query a specific task
  python mps_get_image_task.py --task-id 1234567890-ImageTask-80108cc3380155d98b2e3573a48a

  # Query and output the full JSON response
  python mps_get_image_task.py --task-id 1234567890-ImageTask-80108cc3380155d98b2e3573a48a --verbose

  # Output raw JSON only (convenient for pipeline processing)
  python mps_get_image_task.py --task-id 1234567890-ImageTask-80108cc3380155d98b2e3573a48a --json

Environment Variables:
  TENCENTCLOUD_SECRET_ID   - Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  - Tencent Cloud SecretKey
"""

import argparse
import json
import os
import sys
from mps_auto_upgrade import check_sdk_version

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

try:
    from qcloud_cos import CosConfig, CosS3Client
    _COS_SDK_AVAILABLE = True
except ImportError:
    _COS_SDK_AVAILABLE = False

try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
    def _ensure_env_loaded(**kwargs):
        return False


# Task status display mapping
STATUS_MAP = {
    "WAITING": "Waiting",
    "PROCESSING": "Processing",
    "FINISH": "Completed",
    "SUCCESS": "Success",
    "FAIL": "Failed",
}


def get_credentials():
    """Get Tencent Cloud credentials from environment variables. If missing, try auto-loading from system files."""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        # Try auto-loading from system environment variable files
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] Environment variables not set, attempting auto-load from system files...", file=sys.stderr)  # NOCA:line-too-long(content cannot be shortened)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
        if not secret_id or not secret_key:
            if _LOAD_ENV_AVAILABLE:
                from mps_load_env import _print_setup_hint, _TARGET_VARS
                _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            else:
                print(
                    "\nError: TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY not set.\n"
                    "Please add these variables in /etc/environment, ~/.profile, or similar files.\n",
                    file=sys.stderr,
                )
            sys.exit(1)
    return credential.Credential(secret_id, secret_key)


def create_mps_client(cred, region):
    """Create an MPS client."""
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    http_profile.reqMethod = "POST"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return mps_client.MpsClient(cred, region, client_profile)


def format_status(status):
    """Format status display."""
    return STATUS_MAP.get(status, status)


def print_output_info(output):
    """Print output file information."""
    if not output:
        return

    out_path = output.get("Path", "")
    signed_url = output.get("SignedUrl", "")
    content = output.get("Content", "")
    out_storage = output.get("OutputStorage", {}) or {}
    out_type = out_storage.get("Type", "")

    bucket = ""
    region = ""

    if out_type == "COS":
        cos_out = out_storage.get("CosOutputStorage", {}) or {}
        bucket = cos_out.get("Bucket", "")
        region = cos_out.get("Region", "")
        print(f"       Output: COS - {bucket}:{out_path} (region: {region})")
    elif out_type == "AWS-S3":
        s3_out = out_storage.get("S3OutputStorage", {}) or {}
        bucket = s3_out.get("S3Bucket", "")
        region = s3_out.get("S3Region", "")
        print(f"       Output: S3 - {bucket}:{out_path} (region: {region})")
    elif out_type == "VOD":
        vod_out = out_storage.get("VODOutputStorage", {}) or {}
        bucket = vod_out.get("Bucket", "")
        region = vod_out.get("Region", "")
        sub_app_id = vod_out.get("SubAppId", "")
        print(f"       Output: VOD - {bucket}:{out_path} (region: {region}, SubAppId: {sub_app_id})")
    elif out_path:
        print(f"       Output path: {out_path}")

    if signed_url:
        print(f"       Signed URL: {signed_url}")
    elif out_type == "COS" and bucket and out_path and _COS_SDK_AVAILABLE:
        try:
            cred = get_credentials()
            cos_config = CosConfig(Region=region, SecretId=cred.secret_id, SecretKey=cred.secret_key)
            cos_client = CosS3Client(cos_config)
            signed_url = cos_client.get_presigned_url(
                Bucket=bucket,
                Key=out_path,
                Method="GET",
                Expired=3600
            )
            print(f"       Signed URL (pre-signed, valid for 1 hour): {signed_url}")
        except Exception as e:  # NOCA:broad-except(CLI script needs to handle all exceptions)
            print(f"       Signed URL: (none) ⚠️  Failed to generate pre-signed URL: {e}")
    else:
        print(f"       Signed URL: (none)")

    if content:
        # Image-to-text result, truncate if too long
        display_content = content if len(content) <= 100 else content[:100] + "..."
        print(f"       Image-to-text result: {display_content}")


def print_image_process_results(result_set):
    """Print image processing sub-task results."""
    if not result_set:
        print("   Sub-tasks: None")
        return

    for i, item in enumerate(result_set, 1):
        status = item.get("Status", "")
        err_msg = item.get("ErrMsg", "")
        message = item.get("Message", "")
        progress = item.get("Progress", None)

        status_str = format_status(status)
        progress_str = f" ({progress}%)" if progress is not None else ""

        err_str = ""
        if err_msg:
            err_str = f" | Error code: {err_msg}"
            if message and message != status:
                err_str += f" - {message}"

        print(f"   [{i}] Status: {status_str}{progress_str}{err_str}")

        # Print output information
        output = item.get("Output")
        if output:
            print_output_info(output)


def query_task(args):
    """Query image processing task details."""
    region = args.region or os.environ.get("TENCENTCLOUD_API_REGION", "ap-guangzhou")

    # 1. Get credentials and client
    cred = get_credentials()
    client = create_mps_client(cred, region)

    # 2. Build request
    params = {"TaskId": args.task_id}

    # 3. Make API call
    try:
        req = models.DescribeImageTaskDetailRequest()
        req.from_json_string(json.dumps(params))

        resp = client.DescribeImageTaskDetail(req)
        result = json.loads(resp.to_json_string())

        # JSON-only output mode
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return result

        # Parse response
        task_type = result.get("TaskType", "")
        status = result.get("Status", "")
        err_code = result.get("ErrCode") or 0
        err_msg = result.get("ErrMsg", "")
        message = result.get("Message", "")
        create_time = result.get("CreateTime", "")
        finish_time = result.get("FinishTime", "")

        # Invalid TaskId: API returns success but task doesn't exist (Status is empty/None)
        if not status and not task_type and not create_time:
            print(f"❌ Task does not exist or has expired (over 7 days): {args.task_id}", file=sys.stderr)
            sys.exit(1)

        print("=" * 60)
        print("Tencent Cloud MPS Image Processing Task Details")
        print("=" * 60)
        print(f"   TaskId:      {args.task_id}")
        print(f"   Task type:   {task_type}")
        print(f"   Status:      {format_status(status)}", end="")
        if err_code != 0:
            print(f" | Error code: {err_code}", end="")
        if err_msg:
            print(f" | {err_msg}", end="")
        if message:
            print(f" - {message}", end="")
        print()
        print(f"   Created:     {create_time}")
        if finish_time:
            print(f"   Completed:   {finish_time}")
        print("-" * 60)

        # Sub-task results
        result_set = result.get("ImageProcessTaskResultSet", [])
        if result_set:
            print("   Sub-task results:")
            print_image_process_results(result_set)
        else:
            print("   Sub-task results: None yet")

        print("-" * 60)
        print(f"   RequestId: {result.get('RequestId', 'N/A')}")

        # Verbose mode: output full JSON
        if args.verbose:
            print("\nFull response:")
            print(json.dumps(result, ensure_ascii=False, indent=2))

        return result

    except TencentCloudSDKException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS Image Processing Task Query — Query status and results of tasks submitted via ProcessImage",  # NOCA:line-too-long(line cannot be shortened)
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Query a specific task
  python mps_get_image_task.py --task-id 1234567890-ImageTask-80108cc3380155d98b2e3573a48a

  # Query and output the full JSON response
  python mps_get_image_task.py --task-id 1234567890-ImageTask-80108cc3380155d98b2e3573a48a --verbose

  # Output raw JSON only (convenient for pipeline processing)
  python mps_get_image_task.py --task-id 1234567890-ImageTask-80108cc3380155d98b2e3573a48a --json

Environment Variables:
  TENCENTCLOUD_SECRET_ID   Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  Tencent Cloud SecretKey
        """
    )

    parser.add_argument("--task-id", type=str, required=True,
                        help="Image processing task ID, returned by the ProcessImage API")
    parser.add_argument("--region", type=str,
                        help="MPS service region (default: ap-guangzhou)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Output the full JSON response")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON only, without formatted summary")

    args = parser.parse_args()

    print("=" * 60)
    print("Tencent Cloud MPS Image Processing Task Query")
    print("=" * 60)
    print(f"TaskId: {args.task_id}")
    print("-" * 60)

    query_task(args)


if __name__ == "__main__":
    main()
