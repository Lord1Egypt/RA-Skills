#!/usr/bin/env python3
"""
腾讯云 MPS 图片理解/OCR/看图问答脚本

功能：
  调用 MPS ProcessImage 接口发起图片理解任务（ScheduleId=30200），支持 Gemini 系列模型，
  对输入图片进行 OCR 文字识别、视觉问答、图片分析等操作。
  通过 DescribeImageTaskDetail 轮询等待结果，返回模型回答的文本内容。

  支持两种模型选择方式：
    - 通过 --definition 指定模型快捷 ID（10000-10004），此时不使用 ScheduleId 和 StdExtInfo
    - 通过 --model-name 指定模型名称（默认 Google/gemini-2.5-flash），使用 ScheduleId + StdExtInfo

COS 存储约定：
  通过环境变量 TENCENTCLOUD_COS_BUCKET 指定输出 COS Bucket 名称。
  - 输出文件默认目录：/output/comprehend/

用法：
  # 使用 URL 输入图片，进行看图问答
  python scripts/mps_image_comprehend.py \\
      --url "https://example.com/photo.jpg" \\
      --prompt "请描述这张图片中的内容"

  # 使用 COS 输入图片，进行 OCR 文字识别
  python scripts/mps_image_comprehend.py \\
      --cos-input-key "/input/document.jpg" \\
      --prompt "请识别图片中的所有文字"

  # 指定模型快捷 ID
  python scripts/mps_image_comprehend.py \\
      --url "https://example.com/photo.jpg" \\
      --prompt "图片中有哪些物体？" \\
      --definition 10002

  # 指定模型名称 + 温度参数
  python scripts/mps_image_comprehend.py \\
      --url "https://example.com/photo.jpg" \\
      --prompt "分析这张图片的构图和色彩" \\
      --model-name "Google/gemini-2.5-flash-pro" \\
      --temperature 0.7

  # 使用本地文件（自动上传到 COS）
  python scripts/mps_image_comprehend.py \\
      --local-file ./photo.jpg \\
      --prompt "这是什么动物？"

  # 只提交任务，不等待结果（返回 TaskId）
  python scripts/mps_image_comprehend.py \\
      --url "https://example.com/photo.jpg" \\
      --prompt "描述图片内容" \\
      --no-wait

  # Dry-run 模式，仅打印请求参数不实际调用
  python scripts/mps_image_comprehend.py \\
      --url "https://example.com/photo.jpg" \\
      --prompt "识别图片中的文字" \\
      --dry-run

环境变量：
  TENCENTCLOUD_SECRET_ID    - 腾讯云 SecretId（必须）
  TENCENTCLOUD_SECRET_KEY   - 腾讯云 SecretKey（必须）
  TENCENTCLOUD_API_REGION   - MPS API 接入地域（必需）
  TENCENTCLOUD_COS_BUCKET   - 输出 COS Bucket（可被 --output-bucket 覆盖）
                              同时作为 --cos-input-key 的默认 Bucket
  TENCENTCLOUD_COS_REGION   - 输出 COS Region（可被 --output-region 覆盖）
                              同时作为 --cos-input-key 的默认 Region
"""

import argparse
import json
import os
import sys
from mps_auto_upgrade import check_sdk_version

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)

try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False

try:
    from mps_poll_task import poll_image_task, auto_upload_local_file
    _POLL_AVAILABLE = True
except ImportError:
    _POLL_AVAILABLE = False

check_sdk_version()
try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.mps.v20190612 import mps_client, models
except ImportError:
    print("错误：请先安装腾讯云 SDK：pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# 默认参数
# =============================================================================
SCHEDULE_ID = 30200  # 图片理解固定 ScheduleId
DEFAULT_OUTPUT_DIR = "/output/comprehend/"
DEFAULT_MODEL_NAME = "Google/gemini-2.5-flash"
DEFAULT_POLL_INTERVAL = 10
DEFAULT_TIMEOUT = 600

DEFINITION_MAP = {
    10000: "gemini-2.5-flash-lite",
    10001: "gemini-2.5-flash",
    10002: "gemini-2.5-flash-pro",
    10003: "gemini-3-flash",
    10004: "gemini-3-pro",
}


# =============================================================================
# 工具函数
# =============================================================================

def get_credentials():
    """从环境变量获取腾讯云凭证，若缺失则尝试自动加载。"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] 环境变量未设置，尝试从系统文件自动加载...", file=sys.stderr)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
        if not secret_id or not secret_key:
            if _LOAD_ENV_AVAILABLE:
                from mps_load_env import _print_setup_hint
                _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            else:
                print(
                    "\n错误：TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY 未设置。\n"
                    "请在 ~/.env、~/.profile 等文件中添加这些变量。\n",
                    file=sys.stderr,
                )
            sys.exit(1)
    return credential.Credential(secret_id, secret_key)


def get_cos_bucket():
    """从环境变量获取输出 COS Bucket 名称。"""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """从环境变量获取输出 COS Region。"""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


def create_mps_client(cred, region):
    """创建 MPS 客户端。"""
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return mps_client.MpsClient(cred, region, client_profile)


def build_url_input(url):
    """构造 URL 类型输入源。"""
    return {
        "Type": "URL",
        "UrlInputInfo": {"Url": url},
    }


def build_cos_input(cos_key, cos_bucket=None, cos_region=None):
    """构造 COS 类型输入源。"""
    bucket = cos_bucket or get_cos_bucket()
    region = cos_region or get_cos_region()
    if not bucket:
        print(
            "错误：COS 输入需要指定 Bucket，请通过 --cos-input-bucket 参数或 TENCENTCLOUD_COS_BUCKET 环境变量设置",
            file=sys.stderr,
        )
        sys.exit(1)
    return {
        "Type": "COS",
        "CosInputInfo": {
            "Bucket": bucket,
            "Region": region,
            "Object": cos_key if cos_key.startswith("/") else f"/{cos_key}",
        },
    }


# =============================================================================
# 请求构建
# =============================================================================

def build_request_payload(args):
    """组装 ProcessImage 请求体。"""
    # 构造输入源
    if args.url:
        input_info = build_url_input(args.url)
    elif args.cos_input_key:
        input_info = build_cos_input(args.cos_input_key, args.cos_input_bucket, args.cos_input_region)
    elif args.local_file:
        # 本地文件需先上传到 COS，然后以 COS 输入方式处理
        upload_result = auto_upload_local_file(args.local_file)
        if not upload_result:
            print("错误：本地文件上传失败", file=sys.stderr)
            sys.exit(1)
        input_info = build_cos_input(upload_result["Key"])
    else:
        print("错误：请指定输入源（--url、--cos-input-key 或 --local-file）", file=sys.stderr)
        sys.exit(1)

    output_bucket = args.output_bucket or get_cos_bucket()
    output_region = args.output_region or get_cos_region()

    if not output_bucket:
        print(
            "错误：缺少输出 Bucket，请传入 --output-bucket 或设置 TENCENTCLOUD_COS_BUCKET",
            file=sys.stderr,
        )
        sys.exit(1)

    payload = {
        "InputInfo": input_info,
        "OutputStorage": {
            "Type": "COS",
            "CosOutputStorage": {
                "Bucket": output_bucket,
                "Region": output_region,
            },
        },
        "OutputDir": args.output_dir,
    }

    # 模型选择逻辑
    if args.definition is not None:
        # 使用 Definition 快捷 ID（不使用 ScheduleId 和 StdExtInfo）
        payload["Definition"] = args.definition
    else:
        # 使用 ScheduleId + StdExtInfo
        payload["ScheduleId"] = SCHEDULE_ID
        model_config = {"ModelName": args.model_name or DEFAULT_MODEL_NAME}
        if args.temperature is not None:
            model_config["Temperature"] = args.temperature
        if args.top_p is not None:
            model_config["TopP"] = args.top_p
        if args.top_k is not None:
            model_config["TopK"] = args.top_k
        payload["StdExtInfo"] = json.dumps(
            {"ModelConfig": model_config},
            ensure_ascii=False,
            separators=(",", ":"),
        )

    # AddOnParameter 始终携带 ExtPrompt
    payload["AddOnParameter"] = {"ExtPrompt": [{"Prompt": args.prompt}]}

    return payload


# =============================================================================
# API 调用
# =============================================================================

def submit_process_image(client, payload):
    """调用 ProcessImage 提交图片理解任务。"""
    req = models.ProcessImageRequest()
    req.from_json_string(json.dumps(payload, ensure_ascii=False))
    resp = client.ProcessImage(req)
    result = json.loads(resp.to_json_string())
    # 兼容 SDK 返回格式
    if "Response" in result:
        result = result["Response"]
    return result


# =============================================================================
# 参数解析
# =============================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="腾讯云 MPS 图片理解/OCR/看图问答（ProcessImage ScheduleId=30200，Gemini 系列模型）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # 输入源
    input_group = parser.add_argument_group("输入源（三选一）")
    source_group = input_group.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--url",
        help="图片 URL（HTTP/HTTPS 直链）",
    )
    source_group.add_argument(
        "--cos-input-key",
        help="图片 COS 对象 Key（如 /input/photo.jpg）",
    )
    source_group.add_argument(
        "--local-file",
        help="本地图片文件路径（自动上传到 COS）",
    )
    input_group.add_argument(
        "--cos-input-bucket",
        help="输入 COS Bucket（默认读取 TENCENTCLOUD_COS_BUCKET）",
    )
    input_group.add_argument(
        "--cos-input-region",
        help="输入 COS Region（默认读取 TENCENTCLOUD_COS_REGION）",
    )

    # 图片理解参数
    comprehend_group = parser.add_argument_group("图片理解参数")
    comprehend_group.add_argument(
        "--prompt", required=True,
        help="对图片的提问或分析指令（必须）",
    )
    model_group = comprehend_group.add_mutually_exclusive_group()
    model_group.add_argument(
        "--definition", type=int,
        choices=list(DEFINITION_MAP.keys()),
        help="模型快捷 ID（与 --model-name 二选一）：10000=gemini-2.5-flash-lite, "
             "10001=gemini-2.5-flash, 10002=gemini-2.5-flash-pro, "
             "10003=gemini-3-flash, 10004=gemini-3-pro",
    )
    model_group.add_argument(
        "--model-name",
        help=f"模型名称（与 --definition 二选一，默认 {DEFAULT_MODEL_NAME}）",
    )
    comprehend_group.add_argument(
        "--temperature", type=float,
        help="生成温度，控制随机性（0.0-1.0）",
    )
    comprehend_group.add_argument(
        "--top-p", type=float,
        help="nucleus sampling 参数（0.0-1.0）",
    )
    comprehend_group.add_argument(
        "--top-k", type=int,
        help="top-k sampling 参数",
    )

    # 输出参数
    output_group = parser.add_argument_group("输出参数")
    output_group.add_argument(
        "--output-bucket",
        help="输出 COS Bucket（默认读取 TENCENTCLOUD_COS_BUCKET）",
    )
    output_group.add_argument(
        "--output-region",
        help="输出 COS Region（默认读取 TENCENTCLOUD_COS_REGION）",
    )
    output_group.add_argument(
        "--output-dir", default=DEFAULT_OUTPUT_DIR,
        help=f"输出目录（默认 {DEFAULT_OUTPUT_DIR}）",
    )

    # 任务控制
    task_group = parser.add_argument_group("任务控制")
    task_group.add_argument(
        "--dry-run", action="store_true",
        help="仅打印请求参数，不实际调用 API",
    )
    task_group.add_argument(
        "--no-wait", action="store_true",
        help="只提交任务，不等待结果（返回 TaskId 后退出）",
    )
    task_group.add_argument(
        "--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL,
        help=f"轮询间隔秒数（默认 {DEFAULT_POLL_INTERVAL}）",
    )
    task_group.add_argument(
        "--timeout", type=int, default=DEFAULT_TIMEOUT,
        help=f"最长等待时间秒数（默认 {DEFAULT_TIMEOUT}）",
    )

    # 认证与地域
    auth_group = parser.add_argument_group("认证与地域")
    auth_group.add_argument(
        "--region",
        default=os.environ.get("TENCENTCLOUD_API_REGION", ""),
        help="MPS API 接入地域（默认读取 TENCENTCLOUD_API_REGION，否则 ap-guangzhou）",
    )

    args = parser.parse_args()
    return args


# =============================================================================
# 主流程
# =============================================================================

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def main():
    args = parse_args()

    cred = get_credentials()
    region = args.region
    client = create_mps_client(cred, region)

    payload = build_request_payload(args)

    # Dry-run 模式
    if args.dry_run:
        print("=" * 60)
        print("【Dry Run 模式】仅打印请求参数，不实际调用 API")
        print("=" * 60)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    # 确定模型信息
    if args.definition is not None:
        model_info = f"Definition={args.definition} ({DEFINITION_MAP.get(args.definition, '未知')})"
    else:
        model_info = f"ModelName={args.model_name or DEFAULT_MODEL_NAME}"

    print(f"🚀 提交图片理解任务...")
    # 打印输入来源
    if args.url:
        print(f"   输入: {args.url}")
    elif args.cos_input_key:
        bucket = args.cos_input_bucket or get_cos_bucket()
        print(f"   输入: COS - {bucket}:{args.cos_input_key}")
    elif args.local_file:
        print(f"   输入: 本地文件 - {args.local_file}")
    print(f"   Prompt: {args.prompt}")
    print(f"   模型: {model_info}")
    if args.definition is not None:
        print(f"   模式: Definition 快捷模式")
    else:
        print(f"   模式: ScheduleId={SCHEDULE_ID}")

    try:
        submit_result = submit_process_image(client, payload)
    except TencentCloudSDKException as e:
        print(f"错误：提交任务失败 - {e}", file=sys.stderr)
        sys.exit(1)

    task_id = submit_result.get("TaskId", "N/A")
    print(f"✅ 图片理解任务提交成功！")
    print(f"   TaskId: {task_id}")
    print(f"   RequestId: {submit_result.get('RequestId', 'N/A')}")
    print(f"\n## TaskId: {task_id}")

    if args.no_wait:
        print(json.dumps({"TaskId": task_id, "RequestId": submit_result.get("RequestId")},
                         ensure_ascii=False, indent=2))
        return

    # 轮询等待结果
    if not _POLL_AVAILABLE:
        print("⚠️  轮询模块不可用，请手动查询：", file=sys.stderr)
        print(f"   python scripts/mps_get_image_task.py --task-id {task_id}", file=sys.stderr)
        print(json.dumps({"TaskId": task_id}, ensure_ascii=False, indent=2))
        return

    task_result = poll_image_task(
        task_id=task_id,
        region=region,
        interval=args.poll_interval,
        max_wait=args.timeout,
        verbose=False,
    )

    if task_result is None:
        print(f"\n⚠️  轮询超时，任务可能仍在处理中。", file=sys.stderr)
        print(f"   可手动查询：python scripts/mps_get_image_task.py --task-id {task_id}", file=sys.stderr)
        sys.exit(1)

    # 输出最终结果
    err_msg = task_result.get("ErrMsg") or ""
    if err_msg and err_msg != "OK":
        print(f"\n❌ 图片理解任务失败：ErrCode={task_result.get('ErrCode')}，ErrMsg={err_msg}", file=sys.stderr)
        sys.exit(1)

    # 提取 Content 文本结果
    content = None
    for item in task_result.get("ImageProcessTaskResultSet") or []:
        output = item.get("Output") or {}
        content = output.get("Content")
        if content:
            break

    final_result = {
        "TaskId": task_id,
        "Status": task_result.get("Status"),
        "CreateTime": task_result.get("CreateTime"),
        "FinishTime": task_result.get("FinishTime"),
        "Content": content,
    }

    print(json.dumps(final_result, ensure_ascii=False, indent=2))

    if content:
        print("\n--- 图片理解结果 ---")
        print(content)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已中断", file=sys.stderr)
        sys.exit(1)
