#!/usr/bin/env python3
"""
Tencent Cloud MPS Large Model Audio/Video Understanding Script

Features:
  Calls the MPS Large Model Audio/Video Understanding capability (AiAnalysisTask + VideoComprehension),
  controlling the understanding focus through prompts to achieve video/audio content analysis,
  scene recognition, summary generation, etc.

  API Documentation: https://cloud.tencent.com/document/product/862/126094
  API Description: ProcessMedia — AiAnalysisTask.Definition=33, ExtendedParameter carries mvc parameters

Core Parameters:
  --mode   : "video" (understand video frames + audio) or "audio" (audio only, audio is auto-extracted from video)
  --prompt : Large model prompt, determines understanding focus and output format (required, clearly describe analysis
  goals)
  --extend-url : Second audio/video URL for comparative analysis (max 1 extended URL, i.e. 2 files total for comparison)

Usage:
  # Basic: Video content understanding
  python scripts/mps_av_understand.py \\
      --url https://example.com/video.mp4 \\
      --mode video \\
      --prompt "Analyze the main content, scenes and key information of this video"

  # Audio mode (audio is auto-extracted when uploading video)
  python scripts/mps_av_understand.py \\
      --url https://example.com/video.mp4 \\
      --mode audio \\
      --prompt "Perform speech recognition on this audio and output the complete text"

  # Comparative analysis (two audio/video files)
  python scripts/mps_av_understand.py \\
      --url https://example.com/video1.mp4 \\
      --extend-url https://example.com/video2.mp4 \\
      --mode audio \\
      --prompt "Compare these two audio clips and analyze the differences in performance level"

  # COS input (recommended, using --cos-input-key)
  python scripts/mps_av_understand.py \\
      --cos-input-key /input/video.mp4 \\
      --mode video \\
      --prompt "Summarize the video content"

  # Async mode (submit task only, don't wait)
  python scripts/mps_av_understand.py \\
      --url https://example.com/video.mp4 \\
      --mode video --prompt "Analyze video content" --no-wait

  # Query existing task result
  python scripts/mps_av_understand.py --task-id 1234567890-WorkflowTask-xxxxx

  # JSON format output
  python scripts/mps_av_understand.py \\
      --url https://example.com/video.mp4 \\
      --mode video --prompt "Analyze video content" --json

  # dry-run mode (preview parameters, don't call API)
  python scripts/mps_av_understand.py \\
      --url https://example.com/video.mp4 \\
      --mode video --prompt "Analyze video content" --dry-run
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
    _le.load_env_files()  # NOCA:broad-except(intentional)
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

    _POLL_AVAILABLE = True
except ImportError:
    _POLL_AVAILABLE = False

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
DEFAULT_REGION     = os.environ.get("TENCENTCLOUD_API_REGION", "")
DEFAULT_DEFINITION = 33   # Preset video understanding template (officially recommended)
DEFAULT_MODE       = "video"
POLL_INTERVAL      = 10   # Polling interval (seconds)
POLL_TIMEOUT       = 600  # Maximum wait time (seconds)


# ─────────────────────────────────────────────
# SDK Client
# ─────────────────────────────────────────────

def get_client(region: str = DEFAULT_REGION):
    secret_id  = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        print("Error: Please set environment variables TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY",
              file=sys.stderr)
        sys.exit(1)
    cred = credential.Credential(secret_id, secret_key)
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return mps_client.MpsClient(cred, region, client_profile)


# ─────────────────────────────────────────────
# Build ExtendedParameter
# ─────────────────────────────────────────────

def build_extended_parameter(
    mode: str,
    prompt: str,
    extend_urls: list = None,
) -> str:
    """
    Build the JSON string for AiAnalysisTask.ExtendedParameter.

    Structure:
      {"mvc": {"mode": "video|audio", "prompt": "...", "extendData": [{"url": "..."}]}}

    Args:
        mode        : "video" or "audio"
        prompt      : Large model prompt
        extend_urls : Additional comparison file URL list (max 1, i.e. 2 files total)
    """
    mvc: dict = {
        "mode":   mode,
        "prompt": prompt,
    }
    if extend_urls:
        mvc["extendData"] = [{"url": u} for u in extend_urls[:1]]  # Max 1 extended URL

    return json.dumps({"mvc": mvc}, ensure_ascii=False)


# ─────────────────────────────────────────────
# Create Task
# ─────────────────────────────────────────────

def create_understand_task(
    client,
    url: str = None,
    cos_input_bucket: str = None,
    cos_input_region: str = None,
    cos_input_key: str = None,
    definition: int = DEFAULT_DEFINITION,
    mode: str = DEFAULT_MODE,
    prompt: str = "",
    extend_urls: list = None,
    region: str = DEFAULT_REGION,
) -> str:
    """
    Submit an audio/video understanding task, returns TaskId.
    """
    req = models.ProcessMediaRequest()

    # ── Input source ──
    input_info = models.MediaInputInfo()
    if url:
        input_info.Type = "URL"
        url_input = models.UrlInputInfo()
        url_input.Url = url
        input_info.UrlInputInfo = url_input
    elif cos_input_key:
        # COS path input
        input_info.Type = "COS"
        cos_input = models.CosInputInfo()
        bucket = cos_input_bucket or os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
        cos_region = cos_input_region or os.environ.get("TENCENTCLOUD_COS_REGION", region)
        if not bucket:
            print("Error: When using COS input, please specify --cos-input-bucket or set TENCENTCLOUD_COS_BUCKET environment variable", file=sys.stderr)  # NOCA:line-too-long(content cannot be shortened)
            sys.exit(1)
        cos_input.Bucket = bucket
        cos_input.Region = cos_region
        # Ensure key starts with /
        cos_input.Object = cos_input_key if cos_input_key.startswith("/") else f"/{cos_input_key}"
        input_info.CosInputInfo = cos_input
    else:
        print("Error: Please provide --url or --cos-input-key", file=sys.stderr)
        sys.exit(1)

    req.InputInfo = input_info

    # ── AiAnalysisTask ──
    ai_task = models.AiAnalysisTaskInput()
    ai_task.Definition = definition
    if prompt:  # Only build ExtendedParameter when prompt is provided
        ai_task.ExtendedParameter = build_extended_parameter(
            mode=mode,
            prompt=prompt,
            extend_urls=extend_urls,
        )
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


def poll_task(client, task_id: str, timeout: int = POLL_TIMEOUT) -> dict:
    start = time.time()
    print(f"⏳ Waiting for task to complete: {task_id}")
    while True:
        result = query_task(client, task_id)
        status = result.get("Status", "")
        if status in ("FINISH", "FAIL"):
            elapsed = int(time.time() - start)
            print(f"{'✅' if status == 'FINISH' else '❌'} Task {status}, took {elapsed}s")
            return result
        if time.time() - start > timeout:
            print(f"⚠️  Timeout ({timeout}s), task is still processing", file=sys.stderr)
            return result
        elapsed = int(time.time() - start)
        print(f"   [{elapsed}s] Status: {status}, continuing to wait...")
        time.sleep(POLL_INTERVAL)


# ─────────────────────────────────────────────
# Result Parsing
# ─────────────────────────────────────────────

def extract_result(task_detail: dict) -> dict:
    """Extract VideoComprehension result from WorkflowTask.AiAnalysisResultSet"""
    out = {
        "task_id":     task_detail.get("TaskId", ""),
        "status":      task_detail.get("Status", ""),
        "create_time": task_detail.get("CreateTime", ""),
        "finish_time": task_detail.get("FinishTime", ""),
        "comprehension": None,
        "error": None,
    }

    wf = task_detail.get("WorkflowTask", {}) or {}
    for item in wf.get("AiAnalysisResultSet", []):
        if item.get("Type") == "VideoComprehension":
            vc = item.get("VideoComprehensionTask", {}) or {}
            if vc.get("ErrCode", 0) != 0:
                out["error"] = {"code": vc["ErrCode"], "message": vc.get("Message", "")}
            else:
                task_out = vc.get("Output", {}) or {}
                out["comprehension"] = {
                    "result":      task_out.get("VideoComprehensionAnalysisResult", ""),
                    "progress":    vc.get("Progress", 0),
                    "begin_time":  vc.get("BeginProcessTime", ""),
                    "finish_time": vc.get("FinishTime", ""),
                }
            break
    return out


def print_result(result: dict, as_json: bool = False, output_dir: str = None):
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        sep = "=" * 60
        print(f"\n{sep}")
        print(f"Task ID : {result['task_id']}")
        print(f"Status  : {result['status']}")
        print(f"Finished: {result.get('finish_time', '-')}")
        if result.get("error"):
            err = result["error"]
            print(f"\n❌ Error: [{err['code']}] {err['message']}")
        elif result.get("comprehension"):
            comp = result["comprehension"]
            print(f"\n✅ Understanding Result (progress: {comp['progress']}%)")
            print("─" * 60)
            print(comp["result"])
        else:
            print("\n⚠️  No result yet (task may still be processing)")
        print(f"{sep}\n")

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        fname = f"av_understand_{result['task_id'].replace('/', '_')}.json"
        fpath = os.path.join(output_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Result saved: {fpath}")


# ─────────────────────────────────────────────
# CLI Entry
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS Large Model Audio/Video Understanding",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Input source (choose one of three)
    input_grp = parser.add_mutually_exclusive_group()
    input_grp.add_argument("--local-file", help="Local file path, auto-uploaded to COS before processing (requires TENCENTCLOUD_COS_BUCKET)")  # NOCA:line-too-long(line cannot be shortened)
    input_grp.add_argument("--url",        help="Audio/video URL (HTTP/HTTPS)")
    input_grp.add_argument("--task-id",    help="Directly query an existing task result (skip creation)")

    # COS path input (new version, consistent with mps_transcode.py etc.)
    parser.add_argument("--cos-input-bucket", help="COS Bucket name of the input file")
    parser.add_argument("--cos-input-region", help="COS Region of the input file (e.g. ap-guangzhou)")
    parser.add_argument("--cos-input-key",    help="COS Key of the input file (e.g. /input/video.mp4)")

    # Core understanding parameters
    parser.add_argument(
        "--mode", choices=["video", "audio"], default=DEFAULT_MODE,
        help=(
            "Understanding mode (default: video):\n"
            "  video — Understand video frame content\n"
            "  audio — Process audio only (audio is auto-extracted from video)"
        ),
    )
    parser.add_argument(
        "--prompt", default="",
        help="Large model prompt (strongly recommended, controls understanding focus and output format)",
    )
    parser.add_argument(
        "--extend-url", metavar="URL", action="append", dest="extend_urls",
        help="Second comparison audio/video URL (for comparative analysis with main input, max 1)",
    )

    # Task parameters
    parser.add_argument(
        "--definition", type=int, default=DEFAULT_DEFINITION,
        help=f"AiAnalysisTask template ID (default: {DEFAULT_DEFINITION}, preset video understanding template)",
    )
    parser.add_argument("--region", default=DEFAULT_REGION,
                        help=f"Region (default: {DEFAULT_REGION})")

    # Output control
    parser.add_argument("--no-wait",    action="store_true", help="Async mode: submit task only, don't wait for result")
    parser.add_argument("--json",       action="store_true", dest="json_output", help="JSON format output")
    parser.add_argument("--output-dir", help="Save result JSON to specified directory")
    parser.add_argument("--dry-run",    action="store_true", help="Only print parameter preview, don't call API")

    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed log information")

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
    # --url local path auto-conversion to local upload mode
    if getattr(args, 'url', None) and not getattr(args, 'local_file', None):
        _val = args.url
        if not _val.startswith('http://') and not _val.startswith('https://'):
            print(f"Note: '{_val}' has no source specified, treating as local file by default", file=sys.stderr)
            args.local_file = _val
            args.url = None

    # --local-file conflicts with COS input parameters
    if getattr(args, 'local_file', None):
        cos_conflicts = [x for x in [
            getattr(args, 'cos_input_bucket', None), getattr(args, 'cos_input_key', None)
        ] if x]
        if cos_conflicts:
            parser.error("--local-file cannot be used together with --cos-input-bucket / --cos-input-key")

    # Auto-upload local file
    if getattr(args, 'local_file', None):
        if not _POLL_AVAILABLE:
            print("Error: --local-file requires the mps_poll_task module", file=sys.stderr)
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
        if args.task_id:
            print(f"  task-id    = {args.task_id}")
        else:
            if args.url:
                print(f"  Input      = URL={args.url}")
            elif args.cos_input_key:
                bucket = args.cos_input_bucket or os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
                region = args.cos_input_region or os.environ.get("TENCENTCLOUD_COS_REGION", args.region)
                print(f"  Input      = COS - {bucket}:{args.cos_input_key} (region: {region})")
            print(f"  mode       = {args.mode}")
            print(f"  prompt     = {args.prompt!r}")
            print(f"  extend-url = {args.extend_urls}")
            print(f"  definition = {args.definition}")
            print(f"  region     = {args.region}")
            print(f"  no-wait    = {args.no_wait}")
            print(f"  verbose    = {args.verbose}")
        if args.prompt:
            ep = build_extended_parameter(args.mode, args.prompt, args.extend_urls)
            print(f"\n  ExtendedParameter =\n  {ep}")
        return

    client = get_client(args.region)

    # ── Query mode ──
    if args.task_id:
        print(f"🔍 Querying task: {args.task_id}")
        if args.verbose:
            print(f"   Client region: {args.region}")
        detail = query_task(client, args.task_id)
        result = extract_result(detail)
        print_result(result, as_json=args.json_output, output_dir=args.output_dir)
        return

    # ── Submit task ──
    has_input = bool(args.url) or bool(args.cos_input_key)
    if not has_input:
        parser.error("Please provide one of --url, --cos-input-key, or --task-id")

    # Determine input source display
    if args.url:
        src = f"URL={args.url}"
    else:
        bucket = args.cos_input_bucket or os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
        region = args.cos_input_region or os.environ.get("TENCENTCLOUD_COS_REGION", args.region)
        src = f"COS - {bucket}:{args.cos_input_key} (region: {region})"

    print(f"🚀 Submitting audio/video understanding task")
    print(f"   Input     : {src}")
    print(f"   mode      : {args.mode}")
    print(f"   prompt    : {args.prompt[:80]!r}{'...' if len(args.prompt) > 80 else ''}")
    if args.extend_urls:
        print(f"   Comparison: {args.extend_urls}")
    print(f"   definition: {args.definition}  region: {args.region}")

    if args.verbose:
        print(f"\n📋 Detailed parameters:")
        print(f"   bucket    : {args.cos_input_bucket or os.environ.get('TENCENTCLOUD_COS_BUCKET', 'N/A')}")
        print(f"   cos_region: {args.cos_input_region or os.environ.get('TENCENTCLOUD_COS_REGION', args.region)}")
        if args.cos_input_key:
            print(f"   cos_key   : {args.cos_input_key}")
        ep = build_extended_parameter(args.mode, args.prompt, args.extend_urls)
        print(f"   extended_param: {ep}")

    try:
        task_id = create_understand_task(
            client,
            url=args.url,
            cos_input_bucket=args.cos_input_bucket,
            cos_input_region=args.cos_input_region,
            cos_input_key=args.cos_input_key,
            definition=args.definition,
            mode=args.mode,
            prompt=args.prompt,
            extend_urls=args.extend_urls,
            region=args.region,
        )
        print("✅ Audio/video understanding task submitted successfully!")
        print(f"   TaskId: {task_id}")
        print(f"\n## TaskId: {task_id}")
        if args.verbose:
            print(f"   Polling interval: {POLL_INTERVAL}s  Max wait: {POLL_TIMEOUT}s")
    except TencentCloudSDKException as e:
        print(f"❌ Submission failed: {e}", file=sys.stderr)
        sys.exit(1)

    # ── Async mode ──
    if args.no_wait:
        result = {
            "task_id": task_id,
            "status":  "PROCESSING",
            "message": "Task submitted, use --task-id to query the result",
        }
        print_result(result, as_json=args.json_output, output_dir=args.output_dir)
        return

    # ── Synchronous wait ──
    try:
        if args.verbose:
            print(f"\n⏳ Starting to poll task status...")
        detail = poll_task(client, task_id)
        if args.verbose:
            print(f"✅ Task completed")
        result = extract_result(detail)
        print_result(result, as_json=args.json_output, output_dir=args.output_dir)
        if result.get("status") == "FAIL":
            sys.exit(1)
    except TencentCloudSDKException as e:
        print(f"❌ Query failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
