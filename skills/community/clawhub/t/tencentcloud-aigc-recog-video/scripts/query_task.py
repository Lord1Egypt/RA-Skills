# -*- coding: utf-8 -*-
"""
tencentcloud-aigc-recog-video: Query Video Moderation Task Detail
Calls the DescribeTaskDetail API to query the status and results of a video
moderation task created by CreateVideoModerationTask.

Usage:
  python query_task.py <task_id>
  python query_task.py --task-id <task_id>
  python query_task.py --task-id <task_id> --show-all-snapshots
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
                "step1": "开通视频内容安全服务: https://console.cloud.tencent.com/cms/video/overview",
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


# ============================================================
# Part 2: Command-line argument parsing
# ============================================================

def parse_args():
    """
    Parse command-line arguments.
    Supports: positional arg (task ID), --task-id, --show-all-snapshots
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Query Tencent Cloud Video Moderation Task Detail (DescribeTaskDetail)"
    )
    parser.add_argument(
        "task", nargs="?", default=None,
        help="Task ID to query (positional argument)"
    )
    parser.add_argument(
        "--task-id", dest="task_id", default=None,
        help="Specify Task ID to query"
    )
    parser.add_argument(
        "--show-all-snapshots", dest="show_all_snapshots", action="store_true",
        default=False,
        help="Show all snapshot results in detail (default: only show flagged snapshots)"
    )

    args = parser.parse_args()
    return args


def get_task_id(args):
    """
    Determine task ID from command-line arguments.
    Returns the task ID string.

    Priority: --task-id > positional arg
    """
    task_id = None

    if args.task_id:
        task_id = args.task_id
    elif args.task is not None:
        task_id = args.task
    else:
        print(json.dumps({
            "error": "NO_TASK_ID",
            "message": "未提供任务 ID。",
            "usage": {
                "positional": "python query_task.py <task_id>",
                "flag": "python query_task.py --task-id <task_id>",
            },
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    return task_id.strip()


# ============================================================
# Part 3: API call and result output
# ============================================================

def describe_task_detail(cred, task_id):
    """
    Call Tencent Cloud DescribeTaskDetail API to query the status and results
    of a video moderation task.
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
    req = models.DescribeTaskDetailRequest()
    req.TaskId = task_id

    # Send request
    resp = client.DescribeTaskDetail(req)
    return resp


def format_output(resp, show_all_snapshots=False):
    """
    Parse DescribeTaskDetail response and output structured JSON result.
    """
    resp_dict = json.loads(resp.to_json_string())

    status = resp_dict.get("Status", "")
    result = {
        "task_id": resp_dict.get("TaskId", ""),
        "status": status,
    }

    # If task is still running or pending, return status info only
    if status in ("PENDING", "RUNNING"):
        result["message"] = "任务仍在处理中，请稍后再查询"
        result["request_id"] = resp_dict.get("RequestId", "")
        return result

    # If task errored or cancelled
    if status in ("ERROR", "CANCELLED"):
        result["message"] = f"任务异常，状态: {status}"
        error_msg = resp_dict.get("ErrorMessage", "")
        if error_msg:
            result["error_message"] = error_msg
        result["request_id"] = resp_dict.get("RequestId", "")
        return result

    # Task FINISH — extract results
    if status == "FINISH":
        # Overall suggestion
        suggestion = resp_dict.get("Suggestion", "")
        result["suggestion"] = suggestion

        # Overall label
        label = resp_dict.get("Label", "")
        result["label"] = label

        # Created time and updated time
        created_at = resp_dict.get("CreatedAt", "")
        updated_at = resp_dict.get("UpdatedAt", "")
        if created_at:
            result["created_at"] = created_at
        if updated_at:
            result["updated_at"] = updated_at

        # Audio text (if any)
        audio_text = resp_dict.get("AudioText", "")
        if audio_text:
            result["audio_text"] = audio_text

        # ImageSegments - snapshot detection results
        image_segments = resp_dict.get("ImageSegments", [])
        if image_segments:
            flagged_snapshots = []
            total_snapshots = len(image_segments)
            for seg in image_segments:
                seg_result = seg.get("Result", {})
                seg_suggestion = seg_result.get("Suggestion", "")

                if show_all_snapshots or seg_suggestion != "Pass":
                    snapshot = {
                        "offset_time": seg.get("OffsetTime", ""),
                        "suggestion": seg_suggestion,
                        "label": seg_result.get("Label", ""),
                        "score": seg_result.get("Score", 0),
                    }
                    sub_label = seg_result.get("SubLabel", "")
                    if sub_label:
                        snapshot["sub_label"] = sub_label
                    url = seg_result.get("Url", "")
                    if url:
                        snapshot["snapshot_url"] = url
                    flagged_snapshots.append(snapshot)

            result["total_snapshots"] = total_snapshots
            result["flagged_snapshots"] = flagged_snapshots

        # AudioSegments - audio detection results
        audio_segments = resp_dict.get("AudioSegments", [])
        if audio_segments:
            flagged_audio = []
            total_audio = len(audio_segments)
            for seg in audio_segments:
                seg_result = seg.get("Result", {})
                seg_suggestion = seg_result.get("Suggestion", "")

                if show_all_snapshots or seg_suggestion != "Pass":
                    audio_item = {
                        "offset": seg.get("Offset", 0),
                        "duration": seg.get("Duration", ""),
                        "suggestion": seg_suggestion,
                        "label": seg_result.get("Label", ""),
                        "score": seg_result.get("Score", 0),
                    }
                    sub_label = seg_result.get("SubLabel", "")
                    if sub_label:
                        audio_item["sub_label"] = sub_label
                    text = seg_result.get("Text", "")
                    if text:
                        audio_item["text"] = text
                    flagged_audio.append(audio_item)

            result["total_audio_segments"] = total_audio
            result["flagged_audio_segments"] = flagged_audio

        result["request_id"] = resp_dict.get("RequestId", "")
        return result

    # Unknown status
    result["message"] = f"未知任务状态: {status}"
    result["raw_response"] = resp_dict
    return result


# ============================================================
# Main function
# ============================================================

def main():
    args = parse_args()
    task_id = get_task_id(args)
    cred = get_credentials()

    try:
        resp = describe_task_detail(cred, task_id)
        result = format_output(resp, show_all_snapshots=args.show_all_snapshots)
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
