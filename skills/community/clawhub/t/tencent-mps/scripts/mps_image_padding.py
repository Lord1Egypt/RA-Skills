#!/usr/bin/env python3
"""
腾讯云 MPS 图片扩图/画布扩展脚本

功能：
  调用 MPS ProcessImage 接口发起图片扩图任务（ScheduleId=30010），
  将原图扩展到指定宽高比或目标尺寸，自动生成扩展区域内容。
  通过 DescribeImageTaskDetail 轮询等待结果，返回输出 COS 路径。

  支持三种扩图模式：
    - 按宽高比扩图：指定目标宽高比（如 16:9、4:3、1:1）
    - 按目标尺寸扩图：指定目标宽度和/或高度（建议 1K 级别）
    - 混合模式：同时指定宽高比和目标尺寸

COS 存储约定：
  通过环境变量 TENCENTCLOUD_COS_BUCKET 指定输出 COS Bucket 名称。
  - 输出文件默认目录：/output/padding/

用法：
  # 按宽高比扩图（将图片扩展为 16:9）
  python scripts/mps_image_padding.py \\
      --url "https://example.com/image.jpg" \\
      --aspect-ratio "16:9"

  # 按宽高比扩图（正方形）
  python scripts/mps_image_padding.py \\
      --url "https://example.com/image.jpg" \\
      --aspect-ratio "1:1"

  # 按像素尺寸扩图（指定目标宽高）
  python scripts/mps_image_padding.py \\
      --url "https://example.com/image.jpg" \\
      --image-width 1280 --image-height 720

  # 仅指定目标宽度（高度自适应）
  python scripts/mps_image_padding.py \\
      --url "https://example.com/image.jpg" \\
      --image-width 1920

  # 使用 COS 路径输入
  python scripts/mps_image_padding.py \\
      --cos-input-key "/input/photo.jpg" \\
      --aspect-ratio "4:3"

  # 使用本地文件输入（自动上传到 COS）
  python scripts/mps_image_padding.py \\
      --local-file "/path/to/image.jpg" \\
      --aspect-ratio "16:9"

  # 只提交任务，不等待结果（返回 TaskId）
  python scripts/mps_image_padding.py \\
      --url "https://example.com/image.jpg" \\
      --aspect-ratio "16:9" \\
      --no-wait

  # Dry Run（仅打印请求参数，不实际调用 API）
  python scripts/mps_image_padding.py \\
      --url "https://example.com/image.jpg" \\
      --image-width 1280 --image-height 720 \\
      --dry-run

  # 指定输出目录和下载结果
  python scripts/mps_image_padding.py \\
      --url "https://example.com/image.jpg" \\
      --aspect-ratio "16:9" \\
      --output-dir "/output/my_padding/" \\
      --download-dir ./results/

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
    from mps_poll_task import poll_image_task, auto_upload_local_file, auto_download_outputs
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
SCHEDULE_ID = 30010  # 图片扩图/画布扩展固定 ScheduleId
DEFAULT_OUTPUT_DIR = "/output/padding/"
DEFAULT_POLL_INTERVAL = 10
DEFAULT_TIMEOUT = 600


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


def build_request_payload(args):
    """组装 ProcessImage 请求体。"""
    # 构造 AddOnParameter.OutputConfig
    output_config = {}
    if args.aspect_ratio:
        output_config["AspectRatio"] = args.aspect_ratio
    if args.image_width:
        output_config["ImageWidth"] = args.image_width
    if args.image_height:
        output_config["ImageHeight"] = args.image_height

    addon_parameter = {
        "OutputConfig": output_config,
    }

    output_bucket = args.output_bucket or get_cos_bucket()
    output_region = args.output_region or get_cos_region()

    if not output_bucket:
        print(
            "错误：缺少输出 Bucket，请传入 --output-bucket 或设置 TENCENTCLOUD_COS_BUCKET",
            file=sys.stderr,
        )
        sys.exit(1)

    # 构造输入源
    if args.url:
        input_info = build_url_input(args.url)
    elif args.cos_input_key:
        input_info = build_cos_input(args.cos_input_key, args.cos_input_bucket, args.cos_input_region)
    else:
        print("错误：请指定输入源（--url、--cos-input-key 或 --local-file）", file=sys.stderr)
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
        "ScheduleId": SCHEDULE_ID,
        "AddOnParameter": addon_parameter,
    }

    if args.output_path:
        payload["OutputPath"] = args.output_path


    return payload


def submit_process_image(client, payload):
    """调用 ProcessImage 提交图片扩图任务。"""
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
        description="腾讯云 MPS 图片扩图/画布扩展（ProcessImage ScheduleId=30010）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # 输入源（三选一）
    input_group = parser.add_argument_group("输入源（三选一：--url / --cos-input-key / --local-file）")
    input_source = input_group.add_mutually_exclusive_group(required=True)
    input_source.add_argument(
        "--url",
        help="图片 URL 地址（与 --cos-input-key / --local-file 三选一）",
    )
    input_source.add_argument(
        "--cos-input-key",
        help="输入 COS 对象 Key（如 /input/image.jpg），与 --url / --local-file 三选一",
    )
    input_source.add_argument(
        "--local-file",
        help="本地文件路径，自动上传到 COS 后处理（需配置 TENCENTCLOUD_COS_BUCKET）",
    )
    input_group.add_argument(
        "--cos-input-bucket",
        help="输入 COS Bucket（默认读取 TENCENTCLOUD_COS_BUCKET）",
    )
    input_group.add_argument(
        "--cos-input-region",
        help="输入 COS Region（默认读取 TENCENTCLOUD_COS_REGION）",
    )

    # 扩图参数
    padding_group = parser.add_argument_group("扩图参数（至少指定一项）")
    padding_group.add_argument(
        "--aspect-ratio",
        help=(
            "目标宽高比（如 '16:9'、'4:3'、'1:1'）。"
            "与 --image-width/--image-height 配合：同时指定宽高则忽略此参数；"
            "仅指定此参数时根据原图自适应调整"
        ),
    )
    padding_group.add_argument(
        "--image-width", type=int,
        help="目标宽度（像素）。建议 1K 级别（如 1280），不推荐 2K 及以上",
    )
    padding_group.add_argument(
        "--image-height", type=int,
        help="目标高度（像素）。建议 1K 级别（如 720），不推荐 2K 及以上",
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
    output_group.add_argument(
        "--output-path",
        help="自定义输出路径（需带文件后缀，如 /output/padding/result.jpg）",
    )

    # 任务控制
    task_group = parser.add_argument_group("任务控制")
    task_group.add_argument(
        "--no-wait", action="store_true",
        help="只提交任务，不等待结果（返回 TaskId 后退出）",
    )
    task_group.add_argument(
        "--dry-run", action="store_true",
        help="仅打印请求参数，不实际调用 API",
    )
    task_group.add_argument(
        "--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL,
        help=f"轮询间隔秒数（默认 {DEFAULT_POLL_INTERVAL}）",
    )
    task_group.add_argument(
        "--timeout", type=int, default=DEFAULT_TIMEOUT,
        help=f"最长等待时间秒数（默认 {DEFAULT_TIMEOUT}）",
    )
    task_group.add_argument(
        "--download-dir",
        help="任务完成后自动下载结果到指定目录（默认不下载）",
    )

    # 认证与地域
    auth_group = parser.add_argument_group("认证与地域")
    auth_group.add_argument(
        "--region",
        default=os.environ.get("TENCENTCLOUD_API_REGION", ""),
        help="MPS API 接入地域（默认读取 TENCENTCLOUD_API_REGION，否则 ap-guangzhou）",
    )

    args = parser.parse_args()

    # 验证：至少指定一个扩图参数
    if not args.aspect_ratio and not args.image_width and not args.image_height:
        parser.error("请至少指定 --aspect-ratio、--image-width 或 --image-height 之一")

    return args


# =============================================================================
# 主流程
# =============================================================================

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def main():
    args = parse_args()

    # 本地文件自动上传到 COS
    if args.local_file:
        if not _POLL_AVAILABLE:
            print("错误：--local-file 需要 mps_poll_task 模块支持", file=sys.stderr)
            sys.exit(1)
        upload_result = auto_upload_local_file(args.local_file)
        if not upload_result:
            sys.exit(1)
        # 将上传结果转换为 COS 输入
        args.cos_input_key = upload_result["Key"]
        args.cos_input_bucket = upload_result.get("Bucket")
        args.cos_input_region = upload_result.get("Region")
        args.url = None  # 确保使用 COS 输入

    cred = get_credentials()
    region = args.region
    client = create_mps_client(cred, region)

    payload = build_request_payload(args)

    # Dry Run 模式
    if args.dry_run:
        print("=" * 60)
        print("【Dry Run 模式】仅打印请求参数，不实际调用 API")
        print("=" * 60)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    # 打印扩图参数摘要
    print("🚀 提交图片扩图任务...")
    if args.url:
        print(f"   输入: {args.url}")
    elif args.cos_input_key:
        bucket = getattr(args, 'cos_input_bucket', None) or get_cos_bucket()
        print(f"   输入: COS - {bucket}:{args.cos_input_key}")
    if args.aspect_ratio:
        print(f"   目标宽高比: {args.aspect_ratio}")
    if args.image_width:
        print(f"   目标宽度: {args.image_width}px")
    if args.image_height:
        print(f"   目标高度: {args.image_height}px")
    print(f"   模式: 图片扩图/画布扩展（ScheduleId={SCHEDULE_ID}）")

    try:
        submit_result = submit_process_image(client, payload)
    except TencentCloudSDKException as e:
        print(f"错误：提交任务失败 - {e}", file=sys.stderr)
        sys.exit(1)

    task_id = submit_result.get("TaskId", "N/A")
    print("✅ 图片扩图任务提交成功！")
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
    if err_msg:
        print(f"\n❌ 图片扩图任务失败：ErrCode={task_result.get('ErrCode')}，ErrMsg={err_msg}", file=sys.stderr)
        sys.exit(1)

    # 提取输出路径
    outputs = []
    for item in task_result.get("ImageProcessTaskResultSet") or []:
        output = item.get("Output") or {}
        storage = (output.get("OutputStorage") or {}).get("CosOutputStorage") or {}
        path = output.get("Path", "")
        bucket = storage.get("Bucket", "")
        region_out = storage.get("Region", "")
        outputs.append({
            "bucket": bucket,
            "region": region_out,
            "path": path,
            "cos_uri": f"cos://{bucket}{path}" if bucket and path else None,
            "url": f"https://{bucket}.cos.{region_out}.myqcloud.com{path}" if bucket and path else None,
        })

    final_result = {
        "TaskId": task_id,
        "Status": task_result.get("Status"),
        "CreateTime": task_result.get("CreateTime"),
        "FinishTime": task_result.get("FinishTime"),
        "Outputs": outputs,
    }

    print(json.dumps(final_result, ensure_ascii=False, indent=2))

    # 自动下载结果
    if args.download_dir and outputs and _POLL_AVAILABLE:
        auto_download_outputs(task_result, download_dir=args.download_dir)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已中断", file=sys.stderr)
        sys.exit(1)
