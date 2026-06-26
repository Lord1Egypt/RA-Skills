# -*- coding: utf-8 -*-
"""
Submit Video Face Fusion Job only (does not poll).
Returns JobId for subsequent querying via query_job.py.
"""

import base64
import json
import os
import subprocess
import sys


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
        }
        print(json.dumps(error_msg, ensure_ascii=False, indent=2))
        sys.exit(1)

    token = os.getenv("TENCENTCLOUD_TOKEN")
    if token:
        return credential.Credential(secret_id, secret_key, token)
    return credential.Credential(secret_id, secret_key)


def build_vclm_client(cred, region="ap-guangzhou"):
    """Build VCLM API client."""
    http_profile = HttpProfile()
    http_profile.endpoint = "vclm.tencentcloudapi.com"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return vclm_client.VclmClient(cred, region, client_profile)


def resolve_image_input(value):
    """Resolve input value to URL or base64 encoded data."""
    if value.startswith("http://") or value.startswith("https://"):
        return {"Url": value}
    elif os.path.isfile(value):
        with open(value, "rb") as f:
            raw_data = f.read()
        b64 = base64.b64encode(raw_data).decode("utf-8")
        return {"Base64": b64}
    else:
        if len(value) > 100 and "/" not in value and "\\" not in value:
            return {"Base64": value}
        else:
            print(json.dumps({
                "error": "INVALID_INPUT",
                "message": f"Input '{value}' is neither a valid URL nor an existing file path.",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)


def parse_args():
    """Parse command-line arguments."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Submit Tencent Cloud Video Face Fusion Job"
    )
    parser.add_argument(
        "--video-url", required=True,
        help="Video template URL (mp4, <=1G, <=20s, resolution<=4k, fps<=25)"
    )
    parser.add_argument(
        "--template", required=True, nargs="+",
        help="Template face image(s): URL or local file path"
    )
    parser.add_argument(
        "--face", required=True, nargs="+",
        help="User face image(s): URL or local file path. Must match --template count."
    )
    parser.add_argument(
        "--logo-add", type=int, default=1, choices=[0, 1],
        help="Add AI synthesis label (0: no, 1: yes). Default: 1"
    )
    parser.add_argument(
        "--region", default="ap-guangzhou",
        help="Tencent Cloud region (default: ap-guangzhou)"
    )

    args = parser.parse_args()

    if len(args.template) != len(args.face):
        print(json.dumps({
            "error": "FACE_COUNT_MISMATCH",
            "message": (
                f"Number of --template ({len(args.template)}) must match "
                f"number of --face ({len(args.face)})."
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


def submit_task(client, video_url, template_images, face_images, logo_add=1):
    """Submit a SubmitVideoFaceFusionJob request."""
    template_infos = []
    merge_infos = []

    for i, (tpl_input, face_input) in enumerate(zip(template_images, face_images)):
        face_id = str(i)

        tpl_image = resolve_image_input(tpl_input)
        template_infos.append({
            "TemplateFaceID": face_id,
            "TemplateFaceImage": tpl_image,
        })

        merge_image = resolve_image_input(face_input)
        merge_infos.append({
            "TemplateFaceID": face_id,
            "MergeFaceImage": merge_image,
        })

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


def main():
    args = parse_args()
    cred = get_credentials()
    client = build_vclm_client(cred, args.region)

    try:
        print("[INFO] Submitting video face fusion task...", file=sys.stderr)
        response = submit_task(
            client,
            video_url=args.video_url,
            template_images=args.template,
            face_images=args.face,
            logo_add=args.logo_add,
        )

        job_id = response.get("JobId", "")
        result = {
            "job_id": job_id,
            "request_id": response.get("RequestId", ""),
            "message": "Task submitted. Use query_job.py to poll for results.",
        }

        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"[INFO] Task submitted, JobId: {job_id}", file=sys.stderr)

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
