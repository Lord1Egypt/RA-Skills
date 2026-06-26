#!/usr/bin/env python3
"""
Tencent Cloud MPS Video Deduplication Script

Features:
  Calls MPS VideoRemake capability to modify video frames and bypass platform duplicate content detection.
  Uses AiAnalysisTask.Definition=29 (video deduplication preset template).

  API Documentation: https://cloud.tencent.com/document/product/862/124394

Supported deduplication modes (--mode, default PicInPic):
  PicInPic         Picture-in-Picture: shrinks the original video and embeds it in a new background
  BackgroundExtend Video Extension: inserts extended frames at scene transitions
  VerticalExtend   Vertical Padding: adds padding content above and below the video
  HorizontalExtend Horizontal Padding: adds padding content to the left and right of the video

Usage:
  # Simplest usage (default PicIn Pic mode, automatically waits for completion)
  python scripts/mps_dedupe.py --url https://example.com/video.mp4

  # Specify deduplication mode
  python scripts/mps_dedupe.py --url https://example.com/video.mp4 \\
      --mode VerticalExtend

  # COS input (recommended)
  python scripts/mps_dedupe.py --cos-input-key /input/video.mp4

  # Async submission (no waiting)
  python scripts/mps_dedupe.py --url https://example.com/video.mp4 --no-wait

  # dry-run preview (including Extended Parameter)
  python scripts/mps_dedupe.py --url https://example.com/video.mp4 --dry-run
"""

import sys
from mps_auto_upgrade import check_sdk_version
import os
import json
import time
import argparse

_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _script_dir)

try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
try:
    import mps_load_env as _le
    _le.load_env_files()
except Exception:  # NOCA:broad-except(CLI script needs to handle all exceptions)
    pass

check_sdk_version()
try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.mps.v20190612 import mps_client, models
except ImportError:
    print("Error: Tencent Cloud SDK not installed, please run: pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)

try:
    from mps_poll_task import auto_upload_local_file
    _POLL_AVAILABLE = True
except ImportError:
    _POLL_AVAILABLE = False

try:
    from qcloud_cos import CosConfig, CosS3Client
    _COS_SDK_AVAILABLE = True
except ImportError:
    _COS_SDK_AVAILABLE = False

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
DEFAULT_REGION     = os.environ.get("TENCENTCLOUD_API_REGION", "")
DEFAULT_DEFINITION = 29    # Video deduplication preset template ID
DEFAULT_MODE       = "PicInPic"
POLL_INTERVAL      = 15    # Polling interval (seconds)
POLL_TIMEOUT       = 3600  # Maximum wait time (seconds)

VALID_MODES = [
    "PicInPic", "BackgroundExtend", "VerticalExtend", "HorizontalExtend",
]

MODE_CN = {
    "PicInPic":         "Picture-in-Picture",
    "BackgroundExtend": "Video Extension",
    "VerticalExtend":   "Vertical Padding",
    "HorizontalExtend": "Horizontal Padding",
}

# ─────────────────────────────────────────────
# SDK Client
# ─────────────────────────────────────────────

def get_client(region: str = DEFAULT_REGION):  # NOCA:E302(function structure required for CLI)
    secret_id  = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        print("Error: Please set TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
        sys.exit(1)
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return mps_client.MpsClient(credential.Credential(secret_id, secret_key), region, client_profile)

# ─────────────────────────────────────────────
# COS Output Helper Functions
# ─────────────────────────────────────────────


def get_cos_bucket():
    """Get COS Bucket name from environment variables."""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """Get COS Bucket region from environment variables, default ap-guangzhou."""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


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


# ─────────────────────────────────────────────
# Build Extended Parameter
# ─────────────────────────────────────────────

def build_extended_parameter(mode: str) -> str:
    """
    Build JSON string for AiAnalysisTask.ExtendedParameter.
    Reference: https://cloud.tencent.com/document/product/862/124394
    """
    return json.dumps({"vremake": {"mode": mode}}, ensure_ascii=False)

# ─────────────────────────────────────────────
# Create Task
# ─────────────────────────────────────────────

def create_task(client, args) -> str:  # NOCA:E302(function structure required for CLI)
    """Submit video deduplication task, return TaskId."""
    req = models.ProcessMediaRequest()

    # Input source
    input_info = models.MediaInputInfo()
    if args.url:
        input_info.Type = "URL"
        url_input = models.UrlInputInfo()
        url_input.Url = args.url
        input_info.UrlInputInfo = url_input
    elif args.cos_input_key:
        input_info.Type = "COS"
        cos_input = models.CosInputInfo()
        bucket = args.cos_input_bucket or os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
        cos_region = args.cos_input_region or os.environ.get("TENCENTCLOUD_COS_REGION", args.region)
        if not bucket:
            print("Error: When using COS input, please specify --cos-input-bucket or set TENCENTCLOUD_COS_BUCKET environment variable", file=sys.stderr)  # NOCA:line-too-long(content cannot be shortened)
            sys.exit(1)
        cos_input.Bucket = bucket
        cos_input.Region = cos_region
        cos_input.Object = args.cos_input_key if args.cos_input_key.startswith("/") else f"/{args.cos_input_key}"
        input_info.CosInputInfo = cos_input
    else:
        print("Error: Please provide --url or --cos-input-key", file=sys.stderr)
        sys.exit(1)

    req.InputInfo = input_info

    # Output storage
    output_storage = build_output_storage(args)
    if output_storage:
        out_storage_obj = models.TaskOutputStorage()
        out_storage_obj.Type = output_storage["Type"]
        cos_out = models.CosOutputStorage()
        cos_out.Bucket = output_storage["CosOutputStorage"]["Bucket"]
        cos_out.Region = output_storage["CosOutputStorage"]["Region"]
        out_storage_obj.CosOutputStorage = cos_out
        req.OutputStorage = out_storage_obj
    req.OutputDir = getattr(args, "output_cos_dir", None) or "/output/dedupe/"

    # Ai Analysis Task
    ai_task = models.AiAnalysisTaskInput()
    ai_task.Definition = args.definition
    ai_task.ExtendedParameter = build_extended_parameter(args.mode)
    req.AiAnalysisTask = ai_task

    resp = client.ProcessMedia(req)
    return resp.TaskId

# ─────────────────────────────────────────────
# Query Task
# ─────────────────────────────────────────────


def query_task(client, task_id: str) -> dict:
    req = models.DescribeTaskDetailRequest()
    req.TaskId = task_id
    resp = client.DescribeTaskDetail(req)
    return json.loads(resp.to_json_string())

def poll_task(client, task_id: str, timeout: int = POLL_TIMEOUT) -> dict:  # NOCA:E302(function structure required for CLI)  # NOCA:line-too-long(line cannot be shortened)
    start = time.time()
    print(f"⏳ Waiting for task completion: {task_id}")
    while True:
        result = query_task(client, task_id)
        status = result.get("Status", "")
        if status in ("FINISH", "FAIL"):
            elapsed = int(time.time() - start)
            icon = "✅" if status == "FINISH" else "❌"
            print(f"{icon} Task {status}, elapsed {elapsed}s")
            return result
        if time.time() - start > timeout:
            print(f"⚠️  Timeout ({timeout}s), task still processing", file=sys.stderr)
            return result
        elapsed = int(time.time() - start)
        print(f"   [{elapsed}s] Status: {status}, continuing to wait...")
        time.sleep(POLL_INTERVAL)

# ─────────────────────────────────────────────
# Result Extraction
# ─────────────────────────────────────────────


def extract_result(task_detail: dict) -> dict:
    """Extract VideoRemake results from WorkflowTask.AiAnalysisResultSet"""
    wf = task_detail.get("WorkflowTask", {}) or {}
    out = {
        "task_id":     wf.get("TaskId", task_detail.get("TaskId", "")),
        "status":      wf.get("Status", task_detail.get("Status", "")),
        "create_time": task_detail.get("CreateTime", ""),
        "finish_time": task_detail.get("FinishTime", ""),
        "remake":      None,
        "error":       None,
    }
    for item in wf.get("AiAnalysisResultSet", []):
        if item.get("Type") == "VRemake":
            vr = item.get("VideoRemakeTask", {}) or {}
            if vr.get("ErrCode", 0) != 0:
                out["error"] = {"code": vr["ErrCode"], "message": vr.get("Message", "")}
            else:
                task_out = vr.get("Output", {}) or {}
                out["remake"] = {
                    "output_object_path": task_out.get("Path", ""),
                    "output_storage":     task_out.get("OutputStorage", {}),
                    "progress":           vr.get("Progress", 0),
                    "begin_time":         vr.get("BeginProcessTime", ""),
                    "finish_time":        vr.get("FinishTime", ""),
                }
            break
    return out

def print_result(result: dict, as_json: bool = False, output_dir: str = None):  # NOCA:E302(function structure required for CLI)  # NOCA:line-too-long(line cannot be shortened)
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        sep = "=" * 60
        print(f"\n{sep}")
        print(f"Task ID : {result['task_id']}")
        print(f"Status  : {result['status']}")
        print(f"Finish Time: {result.get('finish_time', '-')}")
        if result.get("error"):
            err = result["error"]
            print(f"\n❌ Error: [{err['code']}] {err['message']}")
        elif result.get("remake"):
            r = result["remake"]
            print(f"\n✅ Deduplication completed (progress: {r['progress']}%)")
            if r.get("output_object_path"):
                out_path = r["output_object_path"]
                print(f"   Output path: {out_path}")
                out_storage = r.get("output_storage") or {}
                out_type = out_storage.get("Type", "")
                if out_type == "COS" and _COS_SDK_AVAILABLE:
                    cos_out = out_storage.get("CosOutputStorage", {}) or {}
                    bucket = cos_out.get("Bucket", "")
                    region = cos_out.get("Region", "")
                    if bucket and region:
                        try:
                            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
                            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
                            cos_config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
                            cos_client = CosS3Client(cos_config)
                            signed_url = cos_client.get_presigned_url(
                                Bucket=bucket,
                                Key=out_path.lstrip("/"),
                                Method="GET",
                                Expired=3600  # NOCA:broad-except(intentional)
                            )
                            print(f"   🔗 Download link (pre-signed, valid for 1 hour): {signed_url}")
                        except Exception as e:  # NOCA:broad-except(CLI script needs to handle all exceptions)
                            print(f"   ⚠️  Failed to generate pre-signed URL: {e}")
        else:
            print("\n⚠️  No results yet (task may still be processing)")
        print(f"{sep}\n")

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        fname = f"dedupe_{result['task_id'].replace('/', '_')}.json"
        fpath = os.path.join(output_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Result saved: {fpath}")

# ─────────────────────────────────────────────
# CLI Entry
# ─────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS Video Deduplication (VideoRemake)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Input source (mutually exclusive)
    input_grp = parser.add_mutually_exclusive_group()
    input_grp.add_argument("--local-file", help="Local file path, automatically uploaded to COS for processing (requires TENCENTCLOUD_COS_BUCKET configuration)")  # NOCA:line-too-long(content cannot be shortened)
    input_grp.add_argument("--url",        help="Video URL (HTTP/HTTPS)")

    # COS path input
    parser.add_argument("--cos-input-bucket", help="COS Bucket name where input file resides")
    parser.add_argument("--cos-input-region", help="COS Region where input file resides (e.g., ap-guangzhou)")
    parser.add_argument("--cos-input-key",    help="COS Key of input file (e.g., /input/video.mp4)")

    # Deduplication mode (default PicIn Pic)
    parser.add_argument(
        "--mode", choices=VALID_MODES, default=DEFAULT_MODE,
        help=f"Deduplication mode (default {DEFAULT_MODE}): " + " / ".join(f"{m}({MODE_CN[m]})" for m in VALID_MODES),
    )

    # Task parameters
    parser.add_argument("--definition", type=int, default=DEFAULT_DEFINITION,
                        help=f"AiAnalysisTask template ID (default {DEFAULT_DEFINITION})")
    parser.add_argument("--region", default=DEFAULT_REGION,
                        help=f"Region (default {DEFAULT_REGION})")

    # Output control
    parser.add_argument("--output-bucket",  dest="output_bucket",  help="Output COS Bucket name (defaults to TENCENTCLOUD_COS_BUCKET environment variable)")  # NOCA:line-too-long(line cannot be shortened)
    parser.add_argument("--output-region",  dest="output_region",  help="Output COS Bucket region (defaults to TENCENTCLOUD_COS_REGION environment variable)")  # NOCA:line-too-long(content cannot be shortened)
    parser.add_argument("--output-cos-dir", dest="output_cos_dir", help="COS output directory (default /output/dedupe/), starts and ends with /")  # NOCA:line-too-long(line cannot be shortened)
    parser.add_argument("--no-wait",    action="store_true", help="Async mode: only submit task, do not wait for result")  # NOCA:line-too-long(content cannot be shortened)
    parser.add_argument("--json",       action="store_true", dest="json_output", help="JSON format output")
    parser.add_argument("--output-dir", help="Save result JSON to specified local directory")
    parser.add_argument("--dry-run",    action="store_true", help="Only print parameter preview (including ExtendedParameter), do not call API")  # NOCA:line-too-long(line cannot be shortened)
    parser.add_argument("--download-dir", type=str, default=None,
                        help="Automatically download result to specified directory after task completion (default: do not download)")  # NOCA:line-too-long(content cannot be shortened)

    args = parser.parse_args()

    # Auto-load environment variables (execute at entry point)
    if _LOAD_ENV_AVAILABLE:
        try:
            _ensure_env_loaded(verbose=getattr(args, "verbose", False))
        except SystemExit:
            raise
        except Exception as e:
            if getattr(args, "verbose", False):
                print(f"⚠️  Auto-load env failed: {e}", file=sys.stderr)

    # --url local path auto-conversion
    if getattr(args, 'url', None) and not getattr(args, 'local_file', None):
        _val = args.url
        if not _val.startswith('http://') and not _val.startswith('https://'):
            print(f"Note: '{_val}' source not specified, defaulting to local file processing", file=sys.stderr)
            args.local_file = _val
            args.url = None

    # --local-file conflicts with COS input parameters
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

    # ── dry-run ──
    if args.dry_run:
        print("🔍 dry-run parameter preview:")
        if args.url:
            src = f"URL={args.url}"
        elif args.cos_input_key:
            bucket = args.cos_input_bucket or os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
            region = args.cos_input_region or os.environ.get("TENCENTCLOUD_COS_REGION", args.region)
            src = f"COS={bucket}/{region}{args.cos_input_key}"
        else:
            src = "Not specified"
        print(f"  Input       = {src}")
        print(f"  mode       = {args.mode} ({MODE_CN.get(args.mode, '?')})")
        print(f"  definition = {args.definition}")
        print(f"  region     = {args.region}")
        print(f"  no-wait    = {args.no_wait}")
        if args.url or args.cos_input_key:
            ep = build_extended_parameter(args.mode)
            print(f"\n  ExtendedParameter =\n  {ep}")
        return

    client = get_client(args.region)

    # ── Submit task ──
    has_input = bool(args.url) or bool(args.cos_input_key)
    if not has_input:
        parser.error("Please provide --url or --cos-input-key")

    if args.url:
        src = f"URL={args.url}"
    else:
        bucket = args.cos_input_bucket or os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
        region = args.cos_input_region or os.environ.get("TENCENTCLOUD_COS_REGION", args.region)
        src = f"COS={bucket}/{region}{args.cos_input_key}"

    mode_cn = MODE_CN.get(args.mode, args.mode)
    print(f"🚀 Submitting video deduplication task")
    print(f"   Input  : {src}")
    print(f"   Mode  : {args.mode} ({mode_cn})")
    print(f"   Template  : {args.definition}  Region: {args.region}")

    try:
        task_id = create_task(client, args)
        print("✅ Video deduplication task submitted successfully!")
        print(f"   TaskId: {task_id}")
        print(f"\n## TaskId: {task_id}")
    except TencentCloudSDKException as e:
        print(f"❌ Submission failed: {e}", file=sys.stderr)
        sys.exit(1)

    # ── Async mode (--no-wait) ──
    if args.no_wait:
        result = {
            "task_id": task_id,
            "status":  "PROCESSING",
            "message": "Task submitted, use mps_get_video_task.py --task-id to query result",
        }
        print_result(result, as_json=args.json_output, output_dir=args.output_dir)
        return

    # ── Wait for completion (default) ──
    try:
        detail = poll_task(client, task_id)
        result = extract_result(detail)
        print_result(result, as_json=args.json_output, output_dir=args.output_dir)

        # --download-dir: Download output video to local directory
        download_dir = getattr(args, 'download_dir', None)
        if download_dir and result.get("remake") and not result.get("error"):
            remake = result["remake"]
            out_path = remake.get("output_object_path", "")
            out_storage = remake.get("output_storage") or {}
            out_type = out_storage.get("Type", "")
            if out_type == "COS" and out_path:
                cos_out = out_storage.get("CosOutputStorage", {}) or {}
                bucket = cos_out.get("Bucket", "")
                region = cos_out.get("Region", "")
                if bucket and region:
                    os.makedirs(download_dir, exist_ok=True)
                    filename = os.path.basename(out_path.lstrip("/"))
                    local_path = os.path.join(download_dir, filename)
                    print(f"\n📥 Downloading output video to: {local_path}")
                    try:
                        secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
                        secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
                        cos_config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
                        cos_client = CosS3Client(cos_config)  # NOCA:broad-except(intentional)
                        cos_client.download_file(Bucket=bucket, Key=out_path.lstrip("/"), DestFilePath=local_path)
                        size = os.path.getsize(local_path)
                        print(f"   ✅ Download successful ({size / 1024 / 1024:.2f} MB): {local_path}")
                    except Exception as e:  # NOCA:broad-except(CLI script needs to handle all exceptions)
                        print(f"   ❌ Download failed: {e}")
        if result.get("status") == "FAIL":
            sys.exit(1)
    except TencentCloudSDKException as e:
        print(f"❌ Query failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
