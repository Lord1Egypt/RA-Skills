# -*- coding: utf-8 -*-
"""
tencentcloud-aigc-recog-video: Create Video Moderation Task
Calls the CreateVideoModerationTask API with Type=VIDEO_AIGC to create a video
moderation task for AI-generated video detection.

Usage:
  python create_task.py "https://example.com/video.mp4"
  python create_task.py --url "https://example.com/video.mp4"
  python create_task.py --data-id my_id --url "https://example.com/video.mp4"
"""

import json
import os
import sys

try:
    from tencentcloud.common import credential  # noqa: E402
    from tencentcloud.common.profile.client_profile import ClientProfile  # noqa: E402
    from tencentcloud.common.profile.http_profile import HttpProfile  # noqa: E402
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException  # noqa: E402
    from tencentcloud.vm.v20210922 import vm_client, models  # noqa: E402
except ImportError:
    print("错误: 缺少依赖 tencentcloud-sdk-python，请执行: pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)


# ============================================================
# Part 1: Credential checking
# ============================================================

def get_credentials():
    """
    Check Tencent Cloud API credential environment variables.
    Supports TENCENTCLOUD_TOKEN for temporary credentials (STS Token).
    Outputs a configuration guide and exits if missing.
    """
    secret_id = os.getenv("TENCENTCLOUD_SECRET_ID")
    secret_key = os.getenv("TENCENTCLOUD_SECRET_KEY")
    token = os.getenv("TENCENTCLOUD_TOKEN")

    if not secret_id or not secret_key:
        missing = []
        if not secret_id:
            missing.append("TENCENTCLOUD_SECRET_ID")
        if not secret_key:
            missing.append("TENCENTCLOUD_SECRET_KEY")
        error_msg = {
            "error": "CREDENTIALS_NOT_CONFIGURED",
            "message": f"缺少环境变量: {', '.join(missing)}",
            "guide": {
                "step1": "开通AI生成视频检测: https://console.cloud.tencent.com/cms/clouds/LLM",
                "step2": "获取 API 密钥: https://console.cloud.tencent.com/cam/capi",
                "step3_linux": (
                    'export TENCENTCLOUD_SECRET_ID="your_secret_id"\n'
                    'export TENCENTCLOUD_SECRET_KEY="your_secret_key"'
                ),
                "step3_windows": (
                    '$env:TENCENTCLOUD_SECRET_ID = "your_secret_id"\n'
                    '$env:TENCENTCLOUD_SECRET_KEY = "your_secret_key"'
                ),
            },
        }
        print(json.dumps(error_msg, ensure_ascii=False, indent=2))
        sys.exit(1)

    # Support temporary credentials (STS Token)
    if token:
        cred = credential.Credential(secret_id, secret_key, token)
    else:
        cred = credential.Credential(secret_id, secret_key)

    return cred


def get_biz_type():
    """
    Get the BizType from TENCENTCLOUD_AIGC_RECOG_VIDEO_BIZ_TYPE environment variable.
    Each user must use their own BizType; exits with error if empty.
    """
    biz_type = os.getenv("TENCENTCLOUD_AIGC_RECOG_VIDEO_BIZ_TYPE", "").strip()

    if not biz_type:
        error_msg = {
            "error": "BIZ_TYPE_NOT_CONFIGURED",
            "message": "缺少环境变量: TENCENTCLOUD_AIGC_RECOG_VIDEO_BIZ_TYPE",
            "guide": {
                "step1": "在腾讯云控制台获取视频AI生成检测配套策略: https://console.cloud.tencent.com/cms/clouds/manage",
                "step2_linux": 'export TENCENTCLOUD_AIGC_RECOG_VIDEO_BIZ_TYPE="your_biz_type"',
                "step2_windows": '$env:TENCENTCLOUD_AIGC_RECOG_VIDEO_BIZ_TYPE = "your_biz_type"',
            },
        }
        print(json.dumps(error_msg, ensure_ascii=False, indent=2))
        sys.exit(1)

    return biz_type


# ============================================================
# Part 2: Command-line argument parsing
# ============================================================

def parse_args():
    """
    Parse command-line arguments.
    Supports: positional arg (video URL), --url, --data-id
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Create Tencent Cloud Video Moderation Task (CreateVideoModerationTask VIDEO_AIGC)"
    )
    parser.add_argument(
        "video", nargs="?", default=None,
        help="Video URL (positional argument)"
    )
    parser.add_argument(
        "--url", dest="video_url", default=None,
        help="Specify video URL"
    )
    parser.add_argument(
        "--data-id", dest="data_id", default=None,
        help="Business data identifier for correlating results (optional, max 128 chars)"
    )

    args = parser.parse_args()
    return args


def is_url(s):
    """Check if a string looks like a URL."""
    return s.startswith("http://") or s.startswith("https://")


def get_video_url(args):
    """
    Determine video URL from command-line arguments.
    Returns the video URL string.

    Priority: --url > positional arg
    """
    video_url = None

    if args.video_url:
        video_url = args.video_url
    elif args.video is not None:
        if is_url(args.video):
            video_url = args.video
        else:
            print(json.dumps({
                "error": "INVALID_INPUT",
                "message": f"输入不是有效的视频 URL: {args.video}",
                "hint": "视频审核仅支持 URL 输入方式，请提供有效的视频 URL（以 http:// 或 https:// 开头）",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
    else:
        print(json.dumps({
            "error": "NO_INPUT",
            "message": "未提供待检测视频 URL。",
            "usage": {
                "url": 'python create_task.py "https://example.com/video.mp4"',
                "url_flag": 'python create_task.py --url "https://example.com/video.mp4"',
            },
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    return video_url


# ============================================================
# Part 3: API call and result output
# ============================================================

def create_video_moderation_task(cred, video_url, data_id=None, biz_type=None):
    """
    Call Tencent Cloud CreateVideoModerationTask API with Type=VIDEO_AIGC
    for AI-generated video detection.
    Returns the parsed API response.
    """
    # Configure HTTP Profile
    http_profile = HttpProfile()
    http_profile.endpoint = "vm.tencentcloudapi.com"

    # Configure Client Profile
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    # Create client (Region: Guangzhou, default for VM service)
    client = vm_client.VmClient(cred, "ap-guangzhou", client_profile)

    # Build request
    req = models.CreateVideoModerationTaskRequest()

    # Set Type at request level (required top-level parameter per API doc)
    req.Type = "VIDEO_AIGC"

    # Set BizType
    if biz_type:
        req.BizType = biz_type

    # Set video input
    task_input = models.TaskInput()

    input_info = models.StorageInfo()
    input_info.Url = video_url
    input_info.Type = "URL"
    task_input.Input = input_info

    if data_id:
        task_input.DataId = data_id

    req.Tasks = [task_input]

    # Send request
    resp = client.CreateVideoModerationTask(req)
    return resp


def format_output(resp):
    """
    Parse API response and output structured JSON result.
    """
    resp_dict = json.loads(resp.to_json_string())

    results = resp_dict.get("Results", [])
    if not results:
        return {
            "error": "NO_RESULTS",
            "message": "API 未返回任务结果",
            "request_id": resp_dict.get("RequestId", ""),
        }

    first_result = results[0]
    result = {
        "task_id": first_result.get("TaskId", ""),
        "data_id": first_result.get("DataId", ""),
        "code": first_result.get("Code", ""),
        "message": first_result.get("Message", ""),
        "request_id": resp_dict.get("RequestId", ""),
    }

    # If Code is non-empty and not "OK", the task creation failed
    if result["code"] and result["code"] != "OK":
        result["status"] = "CREATE_FAILED"
    else:
        result["status"] = "CREATED"

    return result


# ============================================================
# Main function
# ============================================================

def main():
    args = parse_args()
    video_url = get_video_url(args)
    cred = get_credentials()
    biz_type = get_biz_type()

    try:
        resp = create_video_moderation_task(
            cred,
            video_url=video_url,
            data_id=args.data_id,
            biz_type=biz_type,
        )
        result = format_output(resp)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except TencentCloudSDKException as err:
        print(json.dumps({
            "error": "API_ERROR",
            "code": err.code,
            "message": err.message,
            "request_id": err.requestId or "",
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
