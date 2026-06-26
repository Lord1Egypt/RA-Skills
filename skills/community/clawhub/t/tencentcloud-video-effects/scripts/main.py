# -*- coding: utf-8 -*-
"""
视频特效 (SubmitTemplateToVideoJob + DescribeTemplateToVideoJob)
异步接口，提交视频特效任务后轮询状态直到完成，返回结果视频 URL。
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


# 支持的图片格式
SUPPORTED_IMAGE_FORMATS = {"png", "jpg", "jpeg", "webp", "bmp", "tiff"}

# 图片文件大小限制：10MB
MAX_IMAGE_SIZE = 10 * 1024 * 1024


def get_credentials():
    """从环境变量获取腾讯云 API 密钥。"""
    secret_id = os.getenv("TENCENTCLOUD_SECRET_ID")
    secret_key = os.getenv("TENCENTCLOUD_SECRET_KEY")

    if not secret_id or not secret_key:
        error_msg = {
            "error": "CREDENTIALS_NOT_CONFIGURED",
            "message": (
                "Tencent Cloud API credentials not found. "
                "Please set TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY."
            ),
            "guide": {
                "step1": "开通视频特效服务: https://console.cloud.tencent.com/vtc/creation/video-special",
                "step2": "获取 API 密钥: https://console.cloud.tencent.com/cam/capi",
                "step3": 'export TENCENTCLOUD_SECRET_ID="your_id" && export TENCENTCLOUD_SECRET_KEY="your_key"',
            },
        }
        print(json.dumps(error_msg, ensure_ascii=False, indent=2))
        sys.exit(1)

    token = os.getenv("TENCENTCLOUD_TOKEN")
    if token:
        return credential.Credential(secret_id, secret_key, token)
    return credential.Credential(secret_id, secret_key)


def build_vclm_client(cred):
    """构建 VCLM 客户端。"""
    http_profile = HttpProfile()
    http_profile.endpoint = "vclm.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return vclm_client.VclmClient(cred, "ap-guangzhou", client_profile)


def parse_args():
    """解析命令行参数。"""
    import argparse

    parser = argparse.ArgumentParser(
        description="腾讯云视频特效 (SubmitTemplateToVideoJob + DescribeTemplateToVideoJob)"
    )
    parser.add_argument("template_name", nargs="?", help="特效模板名称，如 hug")
    parser.add_argument("pic_input", nargs="?", help="输入图片 URL 或本地文件路径")
    parser.add_argument("--logo-add", type=int, default=1, choices=[0, 1],
                        help="是否添加 AI 生成标识：1=添加, 0=不添加 (默认: 1)")
    parser.add_argument("--resolution", default="360p",
                        help="视频输出分辨率 (默认: 360p)")
    parser.add_argument("--bgm", action="store_true",
                        help="是否添加背景音乐 (默认: 不添加)")
    parser.add_argument("--poll-interval", type=int, default=5,
                        help="轮询间隔秒数 (默认: 5)")
    parser.add_argument("--max-poll-time", type=int, default=600,
                        help="最大轮询时间秒数 (默认: 600)")
    parser.add_argument("--no-poll", action="store_true",
                        help="仅提交任务，不轮询结果 (返回 JobId)")

    args = parser.parse_args()

    if not args.template_name or not args.pic_input:
        print(json.dumps({
            "error": "NO_INPUT",
            "message": "缺少必要参数：特效模板名称和输入图片。",
            "usage": {
                "url": 'python3 main.py hug "https://example.com/human.png"',
                "file": 'python3 main.py hug /path/to/image.png (≤10MB)',
            },
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    return args


def build_image_param(pic_input):
    """根据输入构建 Image 参数，支持 URL 和本地文件。"""
    if pic_input.startswith("http://") or pic_input.startswith("https://"):
        # URL 方式
        return {"Url": pic_input}
    elif os.path.isfile(pic_input):
        # 本地文件方式，读取并 base64 编码
        file_size = os.path.getsize(pic_input)
        if file_size > MAX_IMAGE_SIZE:
            print(json.dumps({
                "error": "FILE_TOO_LARGE",
                "message": f"本地文件 {file_size} 字节，超过 10MB 限制，请使用 URL 方式。",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        # 检查文件格式
        ext = os.path.splitext(pic_input)[1].lower().lstrip(".")
        if ext not in SUPPORTED_IMAGE_FORMATS:
            print(json.dumps({
                "error": "UNSUPPORTED_FORMAT",
                "message": f"不支持的图片格式: .{ext}，支持格式: {', '.join(sorted(SUPPORTED_IMAGE_FORMATS))}",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        with open(pic_input, "rb") as f:
            raw_data = f.read()
        image_base64 = base64.b64encode(raw_data).decode("utf-8")
        return {"Image": image_base64}
    else:
        print(json.dumps({
            "error": "INVALID_INPUT",
            "message": f"输入 '{pic_input}' 既不是有效的 URL 也不是存在的文件。",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


def submit_template_to_video_job(client, template, images, logo_add, resolution, bgm):
    """提交视频特效任务。"""
    req = models.SubmitTemplateToVideoJobRequest()
    params = {
        "Template": template,
        "Images": images,
        "LogoAdd": logo_add,
        "Resolution": resolution,
        "BGM": bgm,
    }

    req.from_json_string(json.dumps(params))
    resp = client.SubmitTemplateToVideoJob(req)
    return json.loads(resp.to_json_string())


def describe_template_to_video_job(client, job_id):
    """查询视频特效任务状态。"""
    req = models.DescribeTemplateToVideoJobRequest()
    req.from_json_string(json.dumps({"JobId": job_id}))
    resp = client.DescribeTemplateToVideoJob(req)
    return json.loads(resp.to_json_string())


def poll_job(client, job_id, poll_interval, max_poll_time):
    """轮询任务状态直到完成或超时。"""
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed > max_poll_time:
            print(json.dumps({
                "error": "POLL_TIMEOUT",
                "message": f"任务 {job_id} 在 {max_poll_time} 秒内未完成。",
                "job_id": job_id,
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        result = describe_template_to_video_job(client, job_id)
        status = result.get("Status", "")

        if status == "DONE":
            return result
        elif status == "FAIL":
            print(json.dumps({
                "error": "JOB_FAILED",
                "message": result.get("ErrorMessage", "任务失败"),
                "error_code": result.get("ErrorCode", ""),
                "job_id": job_id,
                "status": status,
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        print(
            f"[INFO] 任务 {job_id} 状态: {status}, "
            f"已耗时: {int(elapsed)}s, {poll_interval}s 后再次查询...",
            file=sys.stderr,
        )
        time.sleep(poll_interval)


def main():
    args = parse_args()
    cred = get_credentials()
    client = build_vclm_client(cred)

    try:
        # 构建图片参数
        image_param = build_image_param(args.pic_input)
        images = [image_param]

        # Step 1: 提交视频特效任务
        print("[INFO] 正在提交视频特效任务...", file=sys.stderr)
        submit_resp = submit_template_to_video_job(
            client, args.template_name, images,
            args.logo_add, args.resolution, args.bgm,
        )

        job_id = submit_resp.get("JobId")
        if not job_id:
            print(json.dumps({
                "error": "NO_JOB_ID",
                "message": "未能从 SubmitTemplateToVideoJob 响应中获取 JobId。",
                "response": submit_resp,
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        print(f"[INFO] 任务已提交, JobId: {job_id}", file=sys.stderr)

        if args.no_poll:
            print(json.dumps({
                "job_id": job_id,
                "message": "任务已提交，请稍后使用 JobId 查询结果。",
            }, ensure_ascii=False, indent=2))
            return

        # Step 2: 轮询任务结果
        data = poll_job(client, job_id, args.poll_interval, args.max_poll_time)

        result = {
            "ResultVideoUrl": data.get("ResultVideoUrl", ""),
        }

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