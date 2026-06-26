# -*- coding: utf-8 -*-
"""
Video Face Fusion All-in-One Script.
Submits a SubmitVideoFaceFusionJob task and automatically polls until complete.
"""

import base64
import json
import os
import subprocess
import sys
import time


def ensure_dependencies():
    try:
        import tencentcloud  # noqa: F401
    except ImportError:
        print("[INFO] tencentcloud-sdk-python not found. Installing...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "tencentcloud-sdk-python", "-q"],
            stdout=sys.stderr,
            stderr=sys.stderr,
        )
        print("[INFO] tencentcloud-sdk-python installed successfully.", file=sys.stderr)


ensure_dependencies()

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.vclm.v20240523 import vclm_client, models


# ===================== Credentials =====================

def get_credentials():
    """Get Tencent Cloud credentials from environment variables."""
    secret_id = os.getenv("TENCENTCLOUD_SECRET_ID")
    secret_key = os.getenv("TENCENTCLOUD_SECRET_KEY")

    if not secret_id or not secret_key:
        error_msg = {
            "error": "CREDENTIALS_NOT_CONFIGURED",
            "message": (
                "Tencent Cloud API credentials not found in environment variables. "
                "Please set TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY."
            ),
            "guide": {
                "step1": "开通视频创作服务: https://console.cloud.tencent.com/vclm",
                "step2": "获取 API 密钥: https://console.cloud.tencent.com/cam/capi",
                "step3_linux": 'export TENCENTCLOUD_SECRET_ID="your_id" && export TENCENTCLOUD_SECRET_KEY="your_key"',
                "step3_windows": '$env:TENCENTCLOUD_SECRET_ID="your_id"; $env:TENCENTCLOUD_SECRET_KEY="your_key"',
            },
        }
        print(json.dumps(error_msg, ensure_ascii=False, indent=2))
        sys.exit(1)

    token = os.getenv("TENCENTCLOUD_TOKEN")
    if token:
        return credential.Credential(secret_id, secret_key, token)
    return credential.Credential(secret_id, secret_key)


# ===================== Client =====================

def build_vclm_client(cred, region="ap-guangzhou"):
    """Build VCLM API client."""
    http_profile = HttpProfile()
    http_profile.endpoint = "vclm.tencentcloudapi.com"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return vclm_client.VclmClient(cred, region, client_profile)


# ===================== Image Helpers =====================

def resolve_image_input(value):
    """Resolve input value to URL or base64 encoded data.

    Returns dict: {"Url": ...} or {"Base64": ...}
    """
    if value.startswith("http://") or value.startswith("https://"):
        return {"Url": value}
    elif os.path.isfile(value):
        with open(value, "rb") as f:
            raw_data = f.read()
        b64 = base64.b64encode(raw_data).decode("utf-8")
        return {"Base64": b64}
    else:
        # Try as base64 string
        if len(value) > 100 and "/" not in value and "\\" not in value:
            return {"Base64": value}
        else:
            print(json.dumps({
                "error": "INVALID_INPUT",
                "message": f"Input '{value}' is neither a valid URL nor an existing file path.",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)


# ===================== Argument Parsing =====================

def parse_args():
    """Parse command-line arguments."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Tencent Cloud Video Face Fusion CLI (submit + auto-poll)"
    )
    parser.add_argument(
        "--video-url", required=True,
        help="Video template URL (mp4, <=1G, <=20s, resolution<=4k, fps<=25)"
    )
    parser.add_argument(
        "--template", required=True, nargs="+",
        help="Template face image(s): URL or local file path. One per face to replace in the video."
    )
    parser.add_argument(
        "--face", required=True, nargs="+",
        help="User face image(s): URL or local file path. Must match --template count one-to-one."
    )
    parser.add_argument(
        "--logo-add", type=int, default=1, choices=[0, 1],
        help="Add AI synthesis label (0: no, 1: yes). Default: 1"
    )
    parser.add_argument(
        "--poll-interval", type=int, default=10,
        help="Polling interval in seconds (default: 10)"
    )
    parser.add_argument(
        "--max-poll-time", type=int, default=600,
        help="Max total polling time in seconds (default: 600 = 10min)"
    )
    parser.add_argument(
        "--no-poll", action="store_true",
        help="Submit task only, do not poll (returns JobId)"
    )
    parser.add_argument(
        "--region", default="ap-guangzhou",
        help="Tencent Cloud region (default: ap-guangzhou)"
    )

    args = parser.parse_args()

    # Validate template and face count match
    if len(args.template) != len(args.face):
        print(json.dumps({
            "error": "FACE_COUNT_MISMATCH",
            "message": (
                f"Number of --template ({len(args.template)}) must match "
                f"number of --face ({len(args.face)}). "
                "Each template face pairs with one user face."
            ),
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    if len(args.template) > 6:
        print(json.dumps({
            "error": "TOO_MANY_FACES",
            "message": f"Maximum 6 face pairs supported, got {len(args.template)}.",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    return args


# ===================== Submit Task =====================

def submit_task(client, video_url, template_images, face_images, logo_add=1):
    """Submit a SubmitVideoFaceFusionJob request and return the response."""
    template_infos = []
    merge_infos = []

    for i, (tpl_input, face_input) in enumerate(zip(template_images, face_images)):
        face_id = str(i)

        # Build TemplateInfo
        tpl_image = resolve_image_input(tpl_input)
        template_info = {
            "TemplateFaceID": face_id,
            "TemplateFaceImage": tpl_image,
        }
        template_infos.append(template_info)

        # Build MergeInfo
        merge_image = resolve_image_input(face_input)
        merge_info = {
            "TemplateFaceID": face_id,
            "MergeFaceImage": merge_image,
        }
        merge_infos.append(merge_info)

    params = {
        "VideoUrl": video_url,
        "TemplateInfos": template_infos,
        "MergeInfos": merge_infos,
        "LogoAdd": logo_add,
    }

    req = models.SubmitVideoFaceFusionJobRequest()
    req.from_json_string(json.dumps(params))
    resp = client.SubmitVideoFaceFusionJob(req)
    return json.loads(resp.to_json_string())


# ===================== Query Task =====================

def query_task(client, job_id):
    """Query task status via DescribeVideoFaceFusionJob."""
    req = models.DescribeVideoFaceFusionJobRequest()
    req.from_json_string(json.dumps({"JobId": job_id}))
    resp = client.DescribeVideoFaceFusionJob(req)
    return json.loads(resp.to_json_string())


# Task status constants
JOB_STATUS_WAIT = "WAIT"
JOB_STATUS_RUN = "RUN"
JOB_STATUS_FAIL = "FAIL"
JOB_STATUS_DONE = "DONE"


def poll_task(client, job_id, poll_interval, max_poll_time):
    """Poll task status until done/failed or timeout."""
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed > max_poll_time:
            print(json.dumps({
                "error": "POLL_TIMEOUT",
                "message": f"Task {job_id} did not complete within {max_poll_time}s.",
                "job_id": job_id,
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        response = query_task(client, job_id)
        status = response.get("Status", "")

        if status == JOB_STATUS_DONE:
            return response
        elif status == JOB_STATUS_FAIL:
            print(json.dumps({
                "error": "TASK_FAILED",
                "job_id": job_id,
                "status": status,
                "error_code": response.get("ErrorCode", ""),
                "error_message": response.get("ErrorMessage", ""),
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        print(
            f"[INFO] Job {job_id} status: {status}, "
            f"elapsed: {int(elapsed)}s, next poll in {poll_interval}s...",
            file=sys.stderr,
        )
        time.sleep(poll_interval)


# ===================== Main =====================

def main():
    args = parse_args()
    cred = get_credentials()
    client = build_vclm_client(cred, args.region)

    try:
        # Step 1: Submit task
        print("[INFO] Submitting video face fusion task...", file=sys.stderr)
        submit_resp = submit_task(
            client,
            video_url=args.video_url,
            template_images=args.template,
            face_images=args.face,
            logo_add=args.logo_add,
        )

        job_id = submit_resp.get("JobId", "")
        if not job_id:
            print(json.dumps({
                "error": "NO_JOB_ID",
                "message": "Failed to get JobId from SubmitVideoFaceFusionJob response.",
                "response": submit_resp,
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        print(f"[INFO] Task submitted, JobId: {job_id}", file=sys.stderr)

        # If --no-poll, return JobId immediately
        if args.no_poll:
            print(json.dumps({
                "job_id": job_id,
                "request_id": submit_resp.get("RequestId", ""),
                "message": "Task submitted. Use query_job.py to poll for results.",
            }, ensure_ascii=False, indent=2))
            return

        # Step 2: Poll for result
        print(
            f"[INFO] Polling for results (interval={args.poll_interval}s, "
            f"max={args.max_poll_time}s)...",
            file=sys.stderr,
        )
        response = poll_task(client, job_id, args.poll_interval, args.max_poll_time)

        # Step 3: Output result
        result = {
            "job_id": job_id,
            "status": "success",
            "result_video_url": response.get("ResultVideoUrl", ""),
        }

        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(
            f"\n[INFO] Video face fusion completed! URL: {result['result_video_url']}",
            file=sys.stderr,
        )
        print("[INFO] Note: Video URL is valid for 24 hours. Please save promptly.", file=sys.stderr)

    except TencentCloudSDKException as err:
        print(json.dumps({
            "error": "VCLM_API_ERROR",
            "code": err.code if hasattr(err, "code") else "UNKNOWN",
            "message": str(err),
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as err:
        print(json.dumps({
            "error": "UNEXPECTED_ERROR",
            "message": str(err),
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
