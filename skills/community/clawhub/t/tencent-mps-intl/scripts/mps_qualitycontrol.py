#!/usr/bin/env python3
"""
Tencent Cloud MPS Media Quality Control Script

Functionality:
  Invokes MPS media quality control capabilities (AiQualityControl) to perform automated quality inspection on
  audio/video.
  Supports input via URL or COS object path, automatically creates tasks and polls for results.

  API documentation: https://cloud.tencent.com/document/product/862/37578
  Data structure: https://cloud.tencent.com/document/api/862/37615#Ai Quality Control Task Input

Quality control template descriptions:
  - 60 (default): Format quality control template-Pro version, detects visual content issues (blur, screen corruption,
  etc.)
  - 70: Content quality control template-Pro version, detects playback issues (playback compatibility, stuttering,
  playback abnormalities)
  - 50: Audio Detection, detects audio content (audio quality, audio events)

COS storage conventions:
  COS Bucket name is specified via environment variable TENCENTCLOUD_COS_BUCKET.
  - Default input file path: {TENCENTCLOUD_COS_BUCKET}/input/   (i.e., COS Object starts with /input/)
  - Default output file path: {TENCENTCLOUD_COS_BUCKET}/output/quality_control/  (i.e., output directory is
  /output/quality_control/)

  When using COS input, bucket/region are automatically read from TENCENTCLOUD_COS_BUCKET/TENCENTCLOUD_COS_REGION
  environment variables.
  When --output-bucket is not explicitly specified, TENCENTCLOUD_COS_BUCKET is automatically used as the output Bucket.
  When --output-dir is not explicitly specified, /output/quality_control/ is automatically used as the output directory.

Usage:
  # Basic: Initiate quality control for a video URL (default template 60, detects visual blur/screen corruption issues)
  python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4

  # Playback compatibility detection (template 70): Detects if video can play normally, playback stuttering, playback
  abnormalities
  python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --definition 70

  # Visual quality detection (template 60, default): Detects visual blur, screen corruption, visual damage issues
  python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --definition 60

  # Audio quality control (template 50): Detects audio quality, audio events, and other audio content issues
  python scripts/mps_qualitycontrol.py --url https://example.com/audio.mp3 --definition 50

  # COS input (recommended, using --cos-input-key)
  python scripts/mps_qualitycontrol.py --cos-input-key /input/video.mp4

  # COS path input (recommended, after local upload)
  python scripts/mps_qualitycontrol.py --cos-input-bucket mybucket-125xxx --cos-input-region ap-guangzhou
  --cos-input-key /input/video.mp4

  # Async mode (only submit task, don't wait for results)
  python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --no-wait

  # Query existing task results
  python scripts/mps_get_video_task.py --task-id 1234567890-WorkflowTask-xxxxx

  # JSON format output
  python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --json

  # dry-run mode (only prints parameters, doesn't actually call)
  python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --dry-run

  # Specify region
  python scripts/mps_qualitycontrol.py --url https://example.com/video.mp4 --region ap-guangzhou

Parameter specification:
  All command-line parameters must use hyphen form (--no-wait, --dry-run, etc.),
  not underscore form (--no_wait, --dry_run, etc.).
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
except Exception:  # NOCA:broad-except(CLI script needs broad catch for user-friendly error reporting)
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
DEFAULT_DEFINITION = 60   # Format quality control-Pro version (default)
POLL_INTERVAL      = 5    # Polling interval (seconds)
POLL_TIMEOUT       = 600  # Maximum wait time (seconds)

DEFINITION_DESC = {
    50: "Audio Detection (audio quality/event detection)",


    60: "Format quality control-Pro version (visual blur/screen corruption/damage detection)",
    70: "Content quality control-Pro version (playback compatibility/stuttering/playback abnormality detection)",
}

# ─────────────────────────────────────────────
# Credentials
# ─────────────────────────────────────────────


def get_credentials():
    secret_id  = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        print("❌ Please configure environment variables TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY", file=sys.stderr)  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
        sys.exit(1)
    return credential.Credential(secret_id, secret_key)


# ─────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────


def get_cos_bucket():
    """Get COS Bucket name (from environment variable or default value)."""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")

def get_cos_region():  # NOCA:E302(function structure required for CLI)
    """Get COS Region (from environment variable or default value)."""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


def build_output_storage(args):
    """
    Build output storage information.

    Priority:
    1. Command line parameters --output-bucket / --output-region
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
# Placeholder detection
# ─────────────────────────────────────────────
def is_placeholder(value: str) -> bool:
    """Detect if a string is a placeholder format, such as <video URL>, YOUR_URL, <YOUR_VALUE>, etc."""
    if not value:
        return False
    stripped = value.strip()
    # Angle bracket-wrapped placeholders, e.g., <video URL>, <YOUR_URL>, <your-value>
    if stripped.startswith("<") and stripped.endswith(">"):
        return True
    # YOUR_ prefix placeholders, e.g., YOUR_URL, YOUR_BUCKET
    if stripped.upper().startswith("YOUR_"):
        return True
    return False


# ─────────────────────────────────────────────
# Build input information
# ─────────────────────────────────────────────
def build_input_info(url: str = None,
                     cos_input_bucket: str = None, cos_input_region: str = None, cos_input_key: str = None,
                     region: str = DEFAULT_REGION) -> dict:
    # Method 1: URL input
    if url:
        if is_placeholder(url):
            print(f"❌ --url parameter value '{url}' is a placeholder, please replace with a real video URL", file=sys.stderr)  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
            sys.exit(1)
        return {"Type": "URL", "UrlInputInfo": {"Url": url}}

    # COS path input
    if cos_input_key:
        if is_placeholder(cos_input_key):
            print("❌ --cos-input-key parameter value contains placeholder, please replace with real value", file=sys.stderr)  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
            sys.exit(1)
        bucket = cos_input_bucket or os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
        r = cos_input_region or os.environ.get("TENCENTCLOUD_COS_REGION", region)
        if not bucket:
            print("❌ When using COS input, please specify --cos-input-bucket parameter or configure TENCENTCLOUD_COS_BUCKET environment variable", file=sys.stderr)  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
            sys.exit(1)
        return {
            "Type": "COS",
            "CosInputInfo": {"Bucket": bucket, "Region": r, "Object": cos_input_key if cos_input_key.startswith("/") else f"/{cos_input_key}"},  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
        }
    print("❌ Please specify input source: --url or --cos-input-key (with --cos-input-bucket/--cos-input-region or environment variables)", file=sys.stderr)  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    sys.exit(1)


# ─────────────────────────────────────────────
# Submit quality control task
# ─────────────────────────────────────────────
def submit_quality_check(client, input_info: dict, definition: int, output_storage: dict = None,
                         notify_url: str = None, output_dir: str = None) -> str:
    req = models.ProcessMediaRequest()
    req.InputInfo = models.MediaInputInfo()
    req.InputInfo.Type = input_info["Type"]

    if input_info["Type"] == "URL":
        req.InputInfo.UrlInputInfo = models.UrlInputInfo()
        req.InputInfo.UrlInputInfo.Url = input_info["UrlInputInfo"]["Url"]
    elif input_info["Type"] == "COS":
        req.InputInfo.CosInputInfo = models.CosInputInfo()
        req.InputInfo.CosInputInfo.Bucket = input_info["CosInputInfo"]["Bucket"]
        req.InputInfo.CosInputInfo.Region = input_info["CosInputInfo"]["Region"]
        req.InputInfo.CosInputInfo.Object = input_info["CosInputInfo"]["Object"]

    req.AiQualityControlTask = models.AiQualityControlTaskInput()
    req.AiQualityControlTask.Definition = definition

    # Set output storage (required for URL input)
    if output_storage:
        req.OutputStorage = models.TaskOutputStorage()
        req.OutputStorage.Type = output_storage["Type"]
        req.OutputStorage.CosOutputStorage = models.CosOutputStorage()
        req.OutputStorage.CosOutputStorage.Bucket = output_storage["CosOutputStorage"]["Bucket"]
        req.OutputStorage.CosOutputStorage.Region = output_storage["CosOutputStorage"]["Region"]

    # Set callback URL
    if notify_url:
        req.TaskNotifyConfig = models.TaskNotifyConfig()
        req.TaskNotifyConfig.Url = notify_url

    # Set output directory
    if output_dir:
        req.OutputDir = output_dir

    resp = client.ProcessMedia(req)
    return resp.TaskId


# ─────────────────────────────────────────────


# Query task results
# ─────────────────────────────────────────────
def get_task_result(client, task_id: str) -> dict:
    req = models.DescribeTaskDetailRequest()
    req.TaskId = task_id
    resp = client.DescribeTaskDetail(req)
    return json.loads(resp.to_json_string())


def poll_task(client, task_id: str, timeout: int = POLL_TIMEOUT, interval: int = POLL_INTERVAL) -> dict:
    print(f"⏳ Waiting for quality control task to complete (TaskId: {task_id})...")
    elapsed = 0
    while elapsed < timeout:
        result = get_task_result(client, task_id)
        status = result.get("Status", "")
        if status == "FINISH":
            print(f"✅ Task completed (elapsed approximately {elapsed}s)")
            return result
        elif status in ("FAIL", "ERROR"):
            print(f"❌ Task failed: {result.get('ErrMsg', '')}", file=sys.stderr)
            return result
        print(f"   Status: {status}, waited {elapsed}s...")
        time.sleep(interval)
        elapsed += interval
    print(f"⚠️  Timeout ({timeout}s), returning last query result", file=sys.stderr)
    return get_task_result(client, task_id)


# ─────────────────────────────────────────────
# Extract quality control result set
# ─────────────────────────────────────────────
def extract_qc_result(result: dict) -> tuple:
    """
    Extract quality control conclusions and result set from DescribeTaskDetail return value.
    Returns (no_audio_video: str, quality_eval_score: int|None, result_set: list, result_set_type: str)

    DescribeTaskDetail structure for WorkflowTask tasks:
      {
        "TaskType": "WorkflowTask",
        "Status": "FINISH",
        "AiQualityControlTaskResult": {
          "Status": "SUCCESS",
          "ErrCode": 0,
          "ErrMsg": "",
          "Input": { "Definition": 60 },
          "Output": {
            "NoAudioVideo": "Yes"|"No",
            "QualityEvaluationScore": 80,
            "Container Diagnose Result Set": [  # Template 60: Format quality control results
              {
                "Type": "DecodeException",
                "Confidence": 95,
                "StartTimeOffset": 48.649,
                "EndTimeOffset": 48.7,
                "AreaCoordSet": [],
                "Suggestion": "review"
              },
              ...
            ],
            "Quality Evaluation Result Set": [  # Template 50: Audio quality control results
              ...
            ]
          }
        }
      }

    For ProcessMedia tasks, the structure is:
      {
        "TaskType": "ProcessMedia",
        "Status": "FINISH",
        "AiQualityControl": {
          ...  # NOCA:E302(function structure required for CLI)
        }
      }
    """
    # Prefer Ai Quality Control Task Result (WorkflowTask), fall back to Ai Quality Control (ProcessMedia)
    qc_task = result.get("AiQualityControlTaskResult") or result.get("AiQualityControl") or {}
    output = qc_task.get("Output") or {}

    no_av = output.get("NoAudioVideo", "")
    score = output.get("QualityEvaluationScore")

    # Prefer Container Diagnose Result Set (Template 60: Format QC - Pro version)
    # If empty, parse Quality Evaluation Result Set (Template 50: Audio QC, etc.)
    result_set = output.get("ContainerDiagnoseResultSet") or []
    result_set_type = "ContainerDiagnoseResultSet"

    if not result_set:
        result_set = output.get("QualityEvaluationResultSet") or []
        result_set_type = "QualityEvaluationResultSet"

    # Compatibility: some older versions or different field names
    if not result_set:
        result_set = (
            output.get("AiQualityControlResultSet")
            or result.get("AiQualityControlResultSet")
            or []
        )
        result_set_type = "Legacy"

    return no_av, score, result_set, result_set_type


# ─────────────────────────────────────────────
# Format output
# ─────────────────────────────────────────────
def format_result(result: dict) -> str:
    lines = []

    task_status = result.get("Status", "")
    if task_status:
        lines.append(f"Task status: {task_status}")

    qc_task = result.get("AiQualityControl") or {}
    sub_status = qc_task.get("Status", "")
    err_code   = qc_task.get("ErrCode") or 0
    err_msg    = qc_task.get("ErrMsg", "")
    if sub_status:
        lines.append(f"QC subtask status: {sub_status}")
    if err_code != 0:
        lines.append(f"Error code: {err_code}  Error message: {err_msg}")

    qc_input = qc_task.get("Input") or {}
    definition = qc_input.get("Definition")
    if definition is not None:
        desc = DEFINITION_DESC.get(int(definition), str(definition))
        lines.append(f"QC template: {definition} — {desc}")

    no_av, score, result_set, result_set_type = extract_qc_result(result)

    if no_av:
        flag = "Yes" if no_av == "Yes" else "No"
        lines.append(f"No audio/video content: {flag} (NoAudioVideo={no_av})")

    if score is not None:
        lines.append(f"Quality score: {score} / 100")

    lines.append("")  # Blank line separator

    if not result_set:
        lines.append("No quality issues detected (or no QC conclusions yet, use --json to view raw data)")
        return "\n".join(lines)

    lines.append(f"Quality issue list ({len(result_set)} items, data source: {result_set_type}):")
    for idx, item in enumerate(result_set, 1):
        item_type   = item.get("Type", "Unknown")
        confidence  = item.get("Confidence", "")
        start       = item.get("StartTimeOffset")
        end         = item.get("EndTimeOffset")
        suggestion  = item.get("Suggestion", "")
        area        = item.get("AreaCoordSet") or []

        line = f"  {idx}. [{item_type}]"
        if confidence != "":
            line += f"  confidence={confidence}"
        if start is not None and end is not None:
            line += f"  time_range={start}s~{end}s"
        elif start is not None:
            line += f"  start={start}s"
        if suggestion:
            line += f"  suggestion={suggestion}"
        if area:
            line += f"  coordinates={area}"
        lines.append(line)

    return "\n".join(lines)


# ─────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS Media Quality Control",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("--local-file", help="Local file path, automatically uploaded to COS before processing (requires TENCENTCLOUD_COS_BUCKET)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    input_group.add_argument("--url",        help="Audio/video URL (HTTP/HTTPS)")

    # COS path input (new version, consistent with mps_transcode.py, etc.)
    parser.add_argument("--cos-input-bucket", type=str,
                        help="COS Bucket name where the input file is located")
    parser.add_argument("--cos-input-region", type=str,
                        help="COS Region of the input file (e.g., ap-guangzhou)")
    parser.add_argument("--cos-input-key", type=str,
                        help="COS Key of the input file (e.g., /input/video.mp4)")

    parser.add_argument(
        "--definition", type=int, default=DEFAULT_DEFINITION,
        choices=[50, 60, 70],
        help=(
            "QC template ID (default 60):\n"
            "  50 = Audio Detection (audio quality/events)\n"
            "  60 = Format QC - Pro (blur/screen corruption, default)\n"
            "  70 = Content QC - Pro (playback compatibility/stutter)"
        ),
    )
    parser.add_argument("--region",   default=DEFAULT_REGION, help=f"Region (default {DEFAULT_REGION})")
    parser.add_argument("--output-bucket", type=str, help="Output COS Bucket name (defaults to env var TENCENTCLOUD_COS_BUCKET)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    parser.add_argument("--output-region", type=str, help="Output COS Region (defaults to env var TENCENTCLOUD_COS_REGION)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    parser.add_argument("--output-dir", type=str, help="Output directory path (e.g., /output/quality_control/)")
    parser.add_argument("--notify-url", type=str, help="Task completion callback URL (optional)")
    parser.add_argument("--no-wait",  action="store_true",    help="Async mode: submit task only, do not wait for results")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    parser.add_argument("--json",     action="store_true",    dest="json_output", help="Output raw results in JSON format")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)
    parser.add_argument("--dry-run",  action="store_true",    help="Print parameters only, do not actually call the API")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)


    # Check for underscore-style arguments before parse_args, strictly reject non-standard usage.
    # Reason: Python argparse internally converts --no-wait to no_wait, but external calls must use hyphen form;
    #         underscore form (--no_wait) is not recognized by argparse and will be silently ignored as unknown args,
    #         causing logic errors that are hard to debug, so we intercept early and provide a clear message.
    _underscore_map = {
        "--output-dir":  "--output-dir",
        "--notify-url":  "--notify-url",
        "--no-wait":     "--no-wait",
        "--dry-run":     "--dry-run",
        "--json-output": "--json",
    }
    for raw_arg in sys.argv[1:]:
        arg_name = raw_arg.split("=")[0]
        if arg_name in _underscore_map:
            correct = _underscore_map[arg_name]
            print(
                f"Error: Non-standard argument name, please use hyphen form '{correct}', "
                f"underscore form '{arg_name}' is not allowed",
                file=sys.stderr,
            )
            sys.exit(2)

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
    # --url auto-convert local path to local upload mode
    if getattr(args, 'url', None) and not getattr(args, 'local_file', None):
        _val = args.url
        if not _val.startswith('http://') and not _val.startswith('https://'):
            print(f"Note: '{_val}' has no source specified, treating as local file by default", file=sys.stderr)
            args.local_file = _val
            args.url = None

    # --local-file and COS input parameters are mutually exclusive
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

    # Check input source
    has_url = bool(args.url)
    has_cos_path = bool(getattr(args, 'cos_input_key', None))

    if not has_url and not has_cos_path:
        parser.error("Please specify --url or --cos-input-key (with --cos-input-bucket/--cos-input-region or environment variables)")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)

    # Placeholder detection
    if args.url and is_placeholder(args.url):
        parser.error(f"--url parameter value '{args.url}' is a placeholder, please replace with a real video URL")
    if has_cos_path:
        if is_placeholder(args.cos_input_key):
            parser.error("--cos-input-key parameter value contains a placeholder, please replace with a real value")

    # dry-run
    if args.dry_run:
        print("🔍 dry-run mode, parameters:")
        if args.url:
            print(f"  Input:      URL={args.url}")
        else:
            bucket_d = getattr(args, 'cos_input_bucket', None) or os.environ.get("TENCENTCLOUD_COS_BUCKET", "not set")
            print(f"  Input:      COS={bucket_d}:{args.cos_input_key}")
        print(f"  Definition: {args.definition} ({DEFINITION_DESC.get(args.definition, '')})")
        print(f"  Region:     {args.region}")
        print(f"  No-wait:    {args.no_wait}")
        return

    cred   = get_credentials()
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    client = mps_client.MpsClient(cred, args.region, client_profile)

    # Submit new task
    input_info = build_input_info(
        url=args.url,
        cos_input_bucket=getattr(args, 'cos_input_bucket', None),
        cos_input_region=getattr(args, 'cos_input_region', None),
        cos_input_key=getattr(args, 'cos_input_key', None),
        region=args.region
    )

    # URL input requires output storage to be set
    output_storage = None
    if args.url:
        output_storage = build_output_storage(args)
        if not output_storage:
            print("❌ Output storage must be specified for URL input", file=sys.stderr)
            print("   Please configure env vars TENCENTCLOUD_COS_BUCKET and TENCENTCLOUD_COS_REGION,", file=sys.stderr)
            print("   or use --output-bucket and --output-region parameters", file=sys.stderr)
            sys.exit(1)

    def_desc   = DEFINITION_DESC.get(args.definition, str(args.definition))
    print(f"🚀 Submitting media quality control task")
    if args.url:
        print(f"   Input:    URL={args.url}")
    else:
        bucket_d = getattr(args, 'cos_input_bucket', None) or os.environ.get("TENCENTCLOUD_COS_BUCKET", "not set")
        region_d = getattr(args, 'cos_input_region', None) or os.environ.get("TENCENTCLOUD_COS_REGION", args.region)
        print(f"   Input:    COS={bucket_d}:{args.cos_input_key} (region: {region_d})")
    print(f"   Template: {args.definition} — {def_desc}")
    print(f"   Region:   {args.region}")
    if output_storage:
        print(f"   Output:   COS={output_storage['CosOutputStorage']['Bucket']} (region: {output_storage['CosOutputStorage']['Region']})")  # noqa: E501  # NOCA:line-too-long(content cannot be shortened)

    try:
        task_id = submit_quality_check(
            client, input_info, args.definition, output_storage,
            notify_url=getattr(args, 'notify_url', None),
            output_dir=getattr(args, 'output_dir', None)
        )
    except TencentCloudSDKException as e:
        print(f"❌ Failed to submit task: {e}", file=sys.stderr)
        sys.exit(1)

    print("✅ Media quality control task submitted successfully!")
    print(f"   TaskId: {task_id}")
    print(f"\n## TaskId: {task_id}")

    if args.no_wait:
        print("ℹ️  Async mode, use the following command to query results:")
        print(f"   python scripts/mps_get_video_task.py --task-id {task_id}")
        return

    try:
        result = poll_task(client, task_id)
    except TencentCloudSDKException as e:
        print(f"❌ Failed to query task: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\n📋 Quality control results:")
        print(format_result(result))
if __name__ == "__main__":
    main()
