# -*- coding: utf-8 -*-
"""
Query Video Face Fusion Job status and result.
"""

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


def parse_args():
    """Parse command-line arguments."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Query Tencent Cloud Video Face Fusion Job Status"
    )
    parser.add_argument(
        "--job-id", required=True,
        help="JobId returned from SubmitVideoFaceFusionJob"
    )
    parser.add_argument(
        "--region", default="ap-guangzhou",
        help="Tencent Cloud region (default: ap-guangzhou)"
    )

    return parser.parse_args()


def query_task(client, job_id):
    """Query task status via DescribeVideoFaceFusionJob."""
    req = models.DescribeVideoFaceFusionJobRequest()
    req.from_json_string(json.dumps({"JobId": job_id}))
    resp = client.DescribeVideoFaceFusionJob(req)
    return json.loads(resp.to_json_string())


def main():
    args = parse_args()
    cred = get_credentials()
    client = build_vclm_client(cred, args.region)

    try:
        response = query_task(client, args.job_id)
        status = response.get("Status", "")

        result = {
            "job_id": args.job_id,
            "status": status,
        }

        if status == "DONE":
            result["result_video_url"] = response.get("ResultVideoUrl", "")
            result["message"] = "Task completed successfully."
        elif status == "FAIL":
            result["error_code"] = response.get("ErrorCode", "")
            result["error_message"] = response.get("ErrorMessage", "")
            result["message"] = "Task failed."
        elif status == "WAIT":
            result["message"] = "Task is waiting in queue."
        elif status == "RUN":
            result["message"] = "Task is running."
        else:
            result["message"] = f"Unknown status: {status}"

        result["request_id"] = response.get("RequestId", "")

        print(json.dumps(result, ensure_ascii=False, indent=2))

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
