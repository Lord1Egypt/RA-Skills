#!/usr/bin/env python3
"""
腾讯云 MPS 图片局部重绘脚本（Inpainting）

功能：
  基于原图与遮罩图（RGBA，Alpha 通道标记重绘区域），调用 MPS ProcessImage 接口
  发起图片局部重绘任务（ScheduleId=30061），根据 Prompt 编辑指令对遮罩区域进行重绘。
  通过 DescribeImageTaskDetail 轮询等待结果，返回输出 COS 路径。

  遮罩图要求：RGBA 格式图片，Alpha 通道（透明度通道）标记需要重绘的区域。

COS 存储约定：
  通过环境变量 TENCENTCLOUD_COS_BUCKET 指定输出 COS Bucket 名称。
  - 输出文件默认目录：/output/repaint/

用法：
  # 原图 URL + 遮罩图 URL + Prompt（等待结果）
  python scripts/mps_image_repaint.py \
      --url "https://example.com/photo.jpg" \
      --mask-url "https://example.com/mask.png" \
      --prompt "将人物背心的颜色换为红色"

  # 原图 COS 路径 + 遮罩图 COS 路径
  python scripts/mps_image_repaint.py \
      --cos-input-key "/input/photo.jpg" \
      --mask-cos-key "/input/mask.png" \
      --prompt "将背景替换为海边沙滩"

  # 原图本地文件（自动上传 COS）+ 遮罩图 URL
  python scripts/mps_image_repaint.py \
      --local-file ./photo.jpg \
      --mask-url "https://example.com/mask.png" \
      --prompt "将裙子换成蓝色连衣裙"

  # 遮罩图使用独立 Bucket/Region
  python scripts/mps_image_repaint.py \
      --url "https://example.com/photo.jpg" \
      --mask-cos-key "/masks/mask.png" \
      --mask-cos-bucket "other-bucket-125xxx" \
      --mask-cos-region "ap-shanghai" \
      --prompt "将墙面颜色改为米白色"

  # 只提交任务，不等待结果（返回 TaskId）
  python scripts/mps_image_repaint.py \
      --url "https://example.com/photo.jpg" \
      --mask-url "https://example.com/mask.png" \
      --prompt "将花瓶换成陶瓷花瓶" \
      --no-wait

  # Dry Run（仅打印请求参数，不实际调用 API）
  python scripts/mps_image_repaint.py \
      --url "https://example.com/photo.jpg" \
      --mask-url "https://example.com/mask.png" \
      --prompt "将椅子换成木质椅子" \
      --dry-run

  # 任务完成后自动下载结果
  python scripts/mps_image_repaint.py \
      --url "https://example.com/photo.jpg" \
      --mask-url "https://example.com/mask.png" \
      --prompt "将天空换成星空" \
      --download-dir ./output

环境变量：
  TENCENTCLOUD_SECRET_ID    - 腾讯云 SecretId（必须）
  TENCENTCLOUD_SECRET_KEY   - 腾讯云 SecretKey（必须）
  TENCENTCLOUD_API_REGION   - MPS API 接入地域（必需）
  TENCENTCLOUD_COS_BUCKET   - 输出 COS Bucket（可被 --output-bucket 覆盖）
                              同时作为 --cos-input-key / --mask-cos-key 的默认 Bucket
  TENCENTCLOUD_COS_REGION   - 输出 COS Region（可被 --output-region 覆盖）
                              同时作为 --cos-input-key / --mask-cos-key 的默认 Region
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
SCHEDULE_ID = 30061  # 图片局部重绘固定 ScheduleId
DEFAULT_OUTPUT_DIR = "/output/repaint/"
DEFAULT_POLL_INTERVAL = 10
DEFAULT_TIMEOUT = 300


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
            "错误：COS 输入需要指定 Bucket，请通过对应 --*-cos-bucket 参数或 TENCENTCLOUD_COS_BUCKET 环境变量设置",
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


def build_media_input(url=None, cos_key=None, cos_bucket=None, cos_region=None, label="图片"):
    """
    根据 url 或 cos_key 构造媒体输入源（二选一）。
    优先使用 url；若 url 为空则使用 cos_key。
    """
    if url:
        return build_url_input(url)
    if cos_key:
        return build_cos_input(cos_key, cos_bucket, cos_region)
    print(f"错误：请指定{label}输入源（--*-url 或 --*-cos-key）", file=sys.stderr)
    sys.exit(1)


def build_request_payload(args):
    """组装 ProcessImage 请求体。"""
    # 构造原图输入
    if args.url:
        input_info = build_url_input(args.url)
    elif args.cos_input_key:
        input_info = build_cos_input(
            args.cos_input_key,
            getattr(args, 'cos_input_bucket', None),
            getattr(args, 'cos_input_region', None),
        )
    else:
        print("错误：请指定原图输入源（--url、--cos-input-key 或 --local-file）", file=sys.stderr)
        sys.exit(1)

    # 构造遮罩图输入
    mask_input = build_media_input(
        url=args.mask_url,
        cos_key=args.mask_cos_key,
        cos_bucket=args.mask_cos_bucket,
        cos_region=args.mask_cos_region,
        label="遮罩图",
    )

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
        "ScheduleId": SCHEDULE_ID,
        "AddOnParameter": {
            "ExtPrompt": [{"Prompt": args.prompt}],
            "ImageSet": [{"Type": "mask", "Image": mask_input}],
        },
    }

    if args.output_path:
        payload["OutputPath"] = args.output_path


    return payload


def submit_process_image(client, payload):
    """调用 ProcessImage 提交局部重绘任务。"""
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
        description="腾讯云 MPS 图片局部重绘 / Inpainting（ProcessImage ScheduleId=30061）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # 输入源（原图）
    input_group = parser.add_argument_group("输入源（原图）")
    source_group = input_group.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--url",
        help="原图 URL（与 --cos-input-key / --local-file 三选一）",
    )
    source_group.add_argument(
        "--cos-input-key",
        help="原图 COS 对象 Key（如 /input/photo.jpg），与 --url / --local-file 三选一",
    )
    source_group.add_argument(
        "--local-file",
        help="原图本地文件路径，自动上传到 COS 后处理（需配置 TENCENTCLOUD_COS_BUCKET）",
    )
    input_group.add_argument(
        "--cos-input-bucket",
        help="原图 COS Bucket（默认读取 TENCENTCLOUD_COS_BUCKET）",
    )
    input_group.add_argument(
        "--cos-input-region",
        help="原图 COS Region（默认读取 TENCENTCLOUD_COS_REGION）",
    )

    # 遮罩图输入
    mask_group = parser.add_argument_group("遮罩图输入（二选一，必填）")
    mask_mutex = mask_group.add_mutually_exclusive_group(required=True)
    mask_mutex.add_argument(
        "--mask-url",
        help="遮罩图 URL（RGBA 带 Alpha 通道，Alpha 标记重绘区域）；与 --mask-cos-key 二选一",
    )
    mask_mutex.add_argument(
        "--mask-cos-key",
        help="遮罩图 COS 对象 Key（如 /input/mask.png），与 --mask-url 二选一",
    )
    mask_group.add_argument(
        "--mask-cos-bucket",
        help="遮罩图 COS Bucket（默认读取 TENCENTCLOUD_COS_BUCKET）",
    )
    mask_group.add_argument(
        "--mask-cos-region",
        help="遮罩图 COS Region（默认读取 TENCENTCLOUD_COS_REGION）",
    )

    # 重绘参数
    repaint_group = parser.add_argument_group("重绘参数")
    repaint_group.add_argument(
        "--prompt", required=True,
        help="编辑指令（必填，如「将人物背心的颜色换为红色」）",
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
        help="自定义输出路径（需带文件后缀，如 /output/repaint/result.png）",
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
    task_group.add_argument(
        "--download-dir",
        help="任务完成后自动下载结果到指定目录（默认：不下载）",
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

    # 本地文件自动上传
    if args.local_file:
        if not _POLL_AVAILABLE:
            print("错误：--local-file 需要 mps_poll_task 模块支持", file=sys.stderr)
            sys.exit(1)
        upload_result = auto_upload_local_file(args.local_file)
        if not upload_result:
            sys.exit(1)
        args.cos_input_key = upload_result["Key"]
        args.cos_input_bucket = upload_result["Bucket"]
        args.cos_input_region = upload_result["Region"]
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

    print("🚀 提交局部重绘任务...")
    # 打印原图来源
    if args.url:
        print(f"   原图: {args.url}")
    else:
        bucket = getattr(args, 'cos_input_bucket', None) or get_cos_bucket()
        print(f"   原图: COS - {bucket}:{args.cos_input_key}")
    # 打印遮罩图来源
    if args.mask_url:
        print(f"   遮罩图: {args.mask_url}")
    else:
        bucket = args.mask_cos_bucket or get_cos_bucket()
        print(f"   遮罩图: COS - {bucket}:{args.mask_cos_key}")
    # 打印 Prompt
    print(f"   Prompt: {args.prompt}")
    print(f"   模式: 局部重绘（ScheduleId={SCHEDULE_ID}）")

    try:
        submit_result = submit_process_image(client, payload)
    except TencentCloudSDKException as e:
        print(f"错误：提交任务失败 - {e}", file=sys.stderr)
        sys.exit(1)

    task_id = submit_result.get("TaskId", "N/A")
    print("✅ 局部重绘任务提交成功！")
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
        print(f"\n❌ 局部重绘任务失败：ErrCode={task_result.get('ErrCode')}，ErrMsg={err_msg}", file=sys.stderr)
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
    if args.download_dir and _POLL_AVAILABLE:
        auto_download_outputs(task_result, download_dir=args.download_dir)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已中断", file=sys.stderr)
        sys.exit(1)
