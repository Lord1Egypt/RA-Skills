#!/usr/bin/env python3
"""
腾讯云 MPS 目标检测与物体描述脚本

功能：
  调用 MPS ProcessImage 接口发起目标检测与物体描述任务，
  通过 StdExtInfo.ObjectDetectDescribeConfig 配置检测参数。
  支持文本检测目标（Prompt）和坐标点检测（Point）两种方式，至少提供一种。
  通过 DescribeImageTaskDetail 轮询等待结果，返回检测结果 JSON。

  支持功能：
    - 文本检测目标：通过自然语言描述需要检测的物体
    - 坐标点检测：指定图片上的坐标点来检测物体
    - 自然语言描述：对检测到的物体进行语言描述
    - 抠图返回：返回检测物体的透明背景 PNG 文件

COS 存储约定：
  通过环境变量 TENCENTCLOUD_COS_BUCKET 指定输出 COS Bucket 名称。
  - 输出文件默认目录：/output/object-detect/

用法：
  # 文本检测目标（检测猫）
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "猫"

  # 多个检测目标
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "猫" --prompt "狗"

  # 坐标点检测
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --point "100,200"

  # 多个坐标点检测
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --point "100,200" --point "500,300"

  # 文本 + 坐标点混合检测
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "猫" --point "100,200"

  # 启用自然语言描述
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "猫" --describe

  # 返回抠图文件（透明背景 PNG）
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "猫" --return-cutout

  # 指定最大返回数量和置信度阈值
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "人" --top-k 5 --confidence-threshold 0.8

  # 使用英文 Prompt 和英文描述输出
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "cat" --prompt-language en --description-language en --describe

  # COS 路径输入
  python scripts/mps_image_detect.py \
      --cos-input-key "/input/photo.jpg" \
      --prompt "猫"

  # 本地文件输入（自动上传到 COS）
  python scripts/mps_image_detect.py \
      --local-file ./photo.jpg \
      --prompt "猫" --describe

  # 只提交任务，不等待结果（返回 TaskId）
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "猫" --no-wait

  # Dry Run（仅打印请求参数，不实际调用 API）
  python scripts/mps_image_detect.py \
      --url "https://example.com/photo.jpg" \
      --prompt "猫" --dry-run

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
DEFAULT_OUTPUT_DIR = "/output/object-detect/"
DEFAULT_TOP_K = 1
DEFAULT_CONFIDENCE_THRESHOLD = 0.5
DEFAULT_POLL_INTERVAL = 5
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


def parse_point(point_str):
    """解析坐标点字符串，格式为 'X,Y'，返回 {"X": int, "Y": int}。"""
    parts = point_str.strip().split(",")
    if len(parts) != 2:
        print(f"错误：坐标格式应为 'X,Y'，收到 '{point_str}'", file=sys.stderr)
        sys.exit(2)
    try:
        return {"X": int(parts[0].strip()), "Y": int(parts[1].strip())}
    except ValueError:
        print(f"错误：坐标值必须为整数，收到 '{point_str}'", file=sys.stderr)
        sys.exit(2)


def build_request_payload(args):
    """组装 ProcessImage 请求体。"""
    # 构造输入源
    if args.url:
        input_info = build_url_input(args.url)
    elif args.cos_input_key:
        input_info = build_cos_input(
            args.cos_input_key,
            getattr(args, 'cos_input_bucket', None),
            getattr(args, 'cos_input_region', None),
        )
    else:
        print("错误：请指定输入源（--url、--cos-input-key 或 --local-file）", file=sys.stderr)
        sys.exit(1)

    # 构造 ObjectDetectDescribeConfig
    detect_config = {
        "TopK": args.top_k,
        "ConfidenceThreshold": args.confidence_threshold,
        "SkipDescribe": not args.describe,
        "ReturnCutout": args.return_cutout,
        "PromptLanguage": args.prompt_language,
        "DescriptionLanguage": args.description_language,
    }
    if args.prompt:
        detect_config["Prompts"] = args.prompt
    if args.point:
        detect_config["Points"] = [parse_point(p) for p in args.point]

    std_ext_info = json.dumps(
        {"ObjectDetectDescribeConfig": detect_config},
        ensure_ascii=False,
        separators=(",", ":"),
    )

    # 构造输出存储
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
        "ImageTask": {"EncodeConfig": {"Format": "PNG"}},
        "StdExtInfo": std_ext_info,
    }

    if args.output_path:
        payload["OutputPath"] = args.output_path


    return payload


def submit_process_image(client, payload):
    """调用 ProcessImage 提交目标检测与物体描述任务。"""
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
        description="腾讯云 MPS 目标检测与物体描述（ProcessImage + ObjectDetectDescribeConfig）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # 输入源
    input_group = parser.add_argument_group("输入源")
    input_group.add_argument(
        "--url",
        help="图片 URL 地址（与 --cos-input-key / --local-file 三选一）",
    )
    input_group.add_argument(
        "--cos-input-key",
        help="输入 COS 对象 Key（如 /input/photo.jpg），与 --url / --local-file 三选一",
    )
    input_group.add_argument(
        "--cos-input-bucket",
        help="输入 COS Bucket（默认读取 TENCENTCLOUD_COS_BUCKET）",
    )
    input_group.add_argument(
        "--cos-input-region",
        help="输入 COS Region（默认读取 TENCENTCLOUD_COS_REGION）",
    )
    input_group.add_argument(
        "--local-file",
        help="本地文件路径，自动上传到 COS 后处理（需配置 TENCENTCLOUD_COS_BUCKET）",
    )

    # 检测参数
    detect_group = parser.add_argument_group("检测参数")
    detect_group.add_argument(
        "--prompt", action="append",
        help="文本检测目标，可重复传入多次（如 --prompt 猫 --prompt 狗）。与 --point 至少提供一种",
    )
    detect_group.add_argument(
        "--point", action="append",
        help="坐标点检测，格式为 'X,Y'，可重复传入多次（如 --point 100,200）。与 --prompt 至少提供一种",
    )
    detect_group.add_argument(
        "--top-k", type=int, default=DEFAULT_TOP_K,
        help=f"最大返回结果数（默认 {DEFAULT_TOP_K}，取值范围 1-20）",
    )
    detect_group.add_argument(
        "--confidence-threshold", type=float, default=DEFAULT_CONFIDENCE_THRESHOLD,
        help=f"置信度阈值（默认 {DEFAULT_CONFIDENCE_THRESHOLD}，范围 0-1）",
    )
    detect_group.add_argument(
        "--describe", action="store_true",
        help="启用自然语言描述",
    )
    detect_group.add_argument(
        "--return-cutout", action="store_true",
        help="返回抠图文件（透明背景 PNG）",
    )
    detect_group.add_argument(
        "--prompt-language", choices=["zh", "en"], default="zh",
        help="输入 Prompt 的语言（默认 zh）",
    )
    detect_group.add_argument(
        "--description-language", choices=["zh", "en"], default="zh",
        help="输出描述的语言（默认 zh）",
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
        help="自定义输出路径（需带文件后缀，如 /output/object-detect/result.png）",
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

    # 认证与地域
    auth_group = parser.add_argument_group("认证与地域")
    auth_group.add_argument(
        "--region",
        default=os.environ.get("TENCENTCLOUD_API_REGION", ""),
        help="MPS API 接入地域（默认读取 TENCENTCLOUD_API_REGION，否则 ap-guangzhou）",
    )

    args = parser.parse_args()

    # 输入源互斥校验
    input_count = sum([
        bool(args.url),
        bool(args.cos_input_key),
        bool(args.local_file),
    ])
    if input_count == 0:
        parser.error("请指定输入源：--url、--cos-input-key 或 --local-file")
    if input_count > 1:
        parser.error("--url、--cos-input-key 和 --local-file 不能同时使用，请选择其一")

    # 检测方式校验：至少提供一种
    if not args.prompt and not args.point:
        parser.error("请至少指定一种检测方式：--prompt 或 --point")

    # top-k 范围校验
    if args.top_k < 1 or args.top_k > 20:
        parser.error("--top-k 取值范围为 1-20")

    # 置信度阈值范围校验
    if args.confidence_threshold < 0 or args.confidence_threshold > 1:
        parser.error("--confidence-threshold 取值范围为 0-1")

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
        args.url = None

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

    print("🚀 提交目标检测与物体描述任务...")
    # 打印输入来源
    if args.url:
        print(f"   输入: {args.url}")
    else:
        bucket = getattr(args, 'cos_input_bucket', None) or get_cos_bucket()
        print(f"   输入: COS - {bucket}:{args.cos_input_key}")
    # 打印检测参数
    if args.prompt:
        for p in args.prompt:
            print(f"   Prompt: {p}")
    if args.point:
        for pt in args.point:
            print(f"   Point: {pt}")
    print(f"   TopK: {args.top_k}，置信度阈值: {args.confidence_threshold}")
    if args.describe:
        print("   描述: 已启用")
    if args.return_cutout:
        print("   抠图: 已启用")

    try:
        submit_result = submit_process_image(client, payload)
    except TencentCloudSDKException as e:
        print(f"错误：提交任务失败 - {e}", file=sys.stderr)
        sys.exit(1)

    task_id = submit_result.get("TaskId", "N/A")
    print("✅ 目标检测与描述任务提交成功！")
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
        print(f"\n❌ 目标检测任务失败：ErrCode={task_result.get('ErrCode')}，ErrMsg={err_msg}", file=sys.stderr)
        sys.exit(1)

    # 提取检测结果
    result_items = task_result.get("ImageProcessTaskResultSet") or []
    detections = []
    outputs = []

    for item in result_items:
        output = item.get("Output") or {}
        content_str = output.get("Content", "")
        try:
            content_data = json.loads(content_str) if content_str else {}
        except (json.JSONDecodeError, TypeError):
            content_data = {"raw": content_str}

        detection = {
            "status": item.get("Status"),
            "detection": content_data,
        }

        err = item.get("ErrMsg", "")
        if err:
            detection["err_msg"] = err

        # 抠图文件路径（如果有）
        if output.get("Path"):
            storage = (output.get("OutputStorage") or {}).get("CosOutputStorage") or {}
            path = output.get("Path", "")
            bucket = storage.get("Bucket", "")
            region_out = storage.get("Region", "")
            cutout_info = {
                "bucket": bucket,
                "region": region_out,
                "path": path,
                "cos_uri": f"cos://{bucket}{path}" if bucket and path else None,
                "url": f"https://{bucket}.cos.{region_out}.myqcloud.com{path}" if bucket and path else None,
            }
            detection["cutout"] = cutout_info
            outputs.append(cutout_info)

        detections.append(detection)

    final_result = {
        "TaskId": task_id,
        "Status": task_result.get("Status"),
        "CreateTime": task_result.get("CreateTime"),
        "FinishTime": task_result.get("FinishTime"),
        "Detections": detections,
    }
    if outputs:
        final_result["Outputs"] = outputs

    print(json.dumps(final_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已中断", file=sys.stderr)
        sys.exit(1)
