#!/usr/bin/env python3
"""
腾讯云 MPS 图片换装脚本

功能：
  基于模特图与服装图，调用 MPS ProcessImage 接口发起 AI 换装任务，
  并通过 DescribeImageTaskDetail 轮询等待结果，返回输出 COS 路径。

  支持的换装场景（通过 --schedule-id 指定）：
    - 30100：普通衣物换装（默认，支持 1-2 张服装图）
    - 30101：内衣换装（仅支持 1 张服装图）

COS 存储约定：
  通过环境变量 TENCENTCLOUD_COS_BUCKET 指定输出 COS Bucket 名称。
  - 输出文件默认目录：/output/tryon/

用法：
  # 最简用法：模特图 + 服装图（URL，默认等待结果）
  python scripts/mps_image_tryon.py \\
      --model-url "https://example.com/model.jpg" \\
      --cloth-url "https://example.com/cloth.jpg"

  # 模特图使用 COS 路径输入
  python scripts/mps_image_tryon.py \\
      --model-cos-key "/input/model.jpg" \\
      --cloth-url "https://example.com/cloth.jpg"

  # 模特图 + 服装图均使用 COS 路径输入
  python scripts/mps_image_tryon.py \\
      --model-cos-key "/input/model.jpg" \\
      --cloth-cos-key "/input/cloth.jpg"

  # 服装图使用 COS，指定非默认 Bucket
  python scripts/mps_image_tryon.py \\
      --model-url "https://example.com/model.jpg" \\
      --cloth-cos-key "/input/cloth.jpg" \\
      --cloth-cos-bucket mybucket-125xxx --cloth-cos-region ap-shanghai

  # 多张服装图（正面 + 背面）
  python scripts/mps_image_tryon.py \\
      --model-url "https://example.com/model.jpg" \\
      --cloth-url "https://example.com/cloth-front.jpg" \\
      --cloth-url "https://example.com/cloth-back.jpg"

  # 内衣场景（只支持 1 张服装图）
  python scripts/mps_image_tryon.py \\
      --model-url "https://example.com/model.jpg" \\
      --cloth-url "https://example.com/underwear.jpg" \\
      --schedule-id 30101

  # 附加提示词 + 随机种子
  python scripts/mps_image_tryon.py \\
      --model-url "https://example.com/model.jpg" \\
      --cloth-url "https://example.com/cloth.jpg" \\
      --ext-prompt "衬衫扣子打开" \\
      --random-seed 48

  # 只提交任务，不等待结果（返回 TaskId）
  python scripts/mps_image_tryon.py \\
      --model-url "https://example.com/model.jpg" \\
      --cloth-url "https://example.com/cloth.jpg" \\
      --no-wait

  # 指定输出 Bucket 和目录
  python scripts/mps_image_tryon.py \\
      --model-url "https://example.com/model.jpg" \\
      --cloth-url "https://example.com/cloth.jpg" \\
      --output-bucket mybucket-125xxx --output-region ap-shanghai \\
      --output-dir /custom/output/

环境变量：
  TENCENTCLOUD_SECRET_ID    - 腾讯云 SecretId（必须）
  TENCENTCLOUD_SECRET_KEY   - 腾讯云 SecretKey（必须）
  TENCENTCLOUD_API_REGION   - MPS API 接入地域（必需）
  TENCENTCLOUD_COS_BUCKET   - 输出 COS Bucket（可被 --output-bucket 覆盖）
                              同时作为 --model-cos-key / --cloth-cos-key 的默认 Bucket
  TENCENTCLOUD_COS_REGION   - 输出 COS Region（可被 --output-region 覆盖）
                              同时作为 --model-cos-key / --cloth-cos-key 的默认 Region
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
    from mps_poll_task import poll_image_task
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
DEFAULT_SCHEDULE_ID = 30100
DEFAULT_OUTPUT_DIR = "/output/tryon/"
DEFAULT_FORMAT = "JPEG"
DEFAULT_IMAGE_SIZE = "2K"
DEFAULT_QUALITY = 85
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
    # 收集服装图列表（url 和 cos-key 合并，按顺序）
    cloth_inputs = []
    for url in (args.cloth_url or []):
        cloth_inputs.append(build_url_input(url))
    for key in (args.cloth_cos_key or []):
        cloth_inputs.append(build_cos_input(key, args.cloth_cos_bucket, args.cloth_cos_region))

    if not cloth_inputs:
        print("错误：请至少指定一张服装图（--cloth-url 或 --cloth-cos-key）", file=sys.stderr)
        sys.exit(1)

    if args.schedule_id == 30101 and len(cloth_inputs) != 1:
        print("错误：内衣场景（--schedule-id 30101）当前仅支持 1 张服装图片", file=sys.stderr)
        sys.exit(1)

    addon_parameter = {
        "ImageSet": [{"Image": inp} for inp in cloth_inputs],
        "OutputConfig": {
            "Format": args.format,
            "ImageSize": args.image_size,
            "Quality": args.quality,
        },
    }

    if args.ext_prompt:
        addon_parameter["ExtPrompt"] = [{"Prompt": p} for p in args.ext_prompt]

    output_bucket = args.output_bucket or get_cos_bucket()
    output_region = args.output_region or get_cos_region()

    if not output_bucket:
        print(
            "错误：缺少输出 Bucket，请传入 --output-bucket 或设置 TENCENTCLOUD_COS_BUCKET",
            file=sys.stderr,
        )
        sys.exit(1)

    # 构造模特图输入
    model_input = build_media_input(
        url=args.model_url,
        cos_key=args.model_cos_key,
        cos_bucket=args.model_cos_bucket,
        cos_region=args.model_cos_region,
        label="模特图",
    )

    payload = {
        "InputInfo": model_input,
        "OutputStorage": {
            "Type": "COS",
            "CosOutputStorage": {
                "Bucket": output_bucket,
                "Region": output_region,
            },
        },
        "OutputDir": args.output_dir,
        "ScheduleId": args.schedule_id,
        "AddOnParameter": addon_parameter,
    }

    if args.output_path:
        payload["OutputPath"] = args.output_path

    if args.resource_id:
        payload["ResourceId"] = args.resource_id

    if args.random_seed is not None:
        payload["StdExtInfo"] = json.dumps(
            {"ModelConfig": {"RandomSeed": args.random_seed}},
            ensure_ascii=False,
            separators=(",", ":"),
        )

    return payload


def submit_process_image(client, payload):
    """调用 ProcessImage 提交换装任务。"""
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
        description="腾讯云 MPS 图片换装（ProcessImage ScheduleId=30100/30101）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # 输入参数
    input_group = parser.add_argument_group("输入参数")
    # 模特图（URL 或 COS，二选一）
    model_group = input_group.add_mutually_exclusive_group(required=True)
    model_group.add_argument(
        "--model-url",
        help="模特图 URL（与 --model-cos-key 二选一）",
    )
    model_group.add_argument(
        "--model-cos-key",
        help="模特图 COS 对象 Key（如 /input/model.jpg），与 --model-url 二选一",
    )
    input_group.add_argument(
        "--model-cos-bucket",
        help="模特图 COS Bucket（默认读取 TENCENTCLOUD_COS_BUCKET）",
    )
    input_group.add_argument(
        "--model-cos-region",
        help="模特图 COS Region（默认读取 TENCENTCLOUD_COS_REGION）",
    )
    # 服装图（URL 或 COS，至少一个，可混用）
    input_group.add_argument(
        "--cloth-url", action="append", default=[],
        help="服装图 URL，可重复传入 1-2 次；与 --cloth-cos-key 可混用",
    )
    input_group.add_argument(
        "--cloth-cos-key", action="append", default=[],
        help="服装图 COS 对象 Key，可重复传入 1-2 次；与 --cloth-url 可混用",
    )
    input_group.add_argument(
        "--cloth-cos-bucket",
        help="服装图 COS Bucket（默认读取 TENCENTCLOUD_COS_BUCKET）",
    )
    input_group.add_argument(
        "--cloth-cos-region",
        help="服装图 COS Region（默认读取 TENCENTCLOUD_COS_REGION）",
    )

    # 换装参数
    tryon_group = parser.add_argument_group("换装参数")
    tryon_group.add_argument(
        "--schedule-id", type=int, default=DEFAULT_SCHEDULE_ID,
        help="换装场景 ID：30100=普通衣物（默认），30101=内衣",
    )
    tryon_group.add_argument(
        "--ext-prompt", action="append",
        help="附加提示词，可重复传入多次（如 '衬衫扣子打开'）",
    )
    tryon_group.add_argument(
        "--random-seed", type=int,
        help="随机种子（StdExtInfo.ModelConfig.RandomSeed），固定种子可获得稳定风格",
    )
    tryon_group.add_argument(
        "--resource-id",
        help="可选的资源 ID（业务侧专属资源）",
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
        help="自定义输出路径（需带文件后缀，如 /output/tryon/result.jpg）",
    )
    output_group.add_argument(
        "--format", choices=["JPEG", "PNG"], default=DEFAULT_FORMAT,
        help="输出格式（默认 JPEG）",
    )
    output_group.add_argument(
        "--image-size", choices=["1K", "2K", "4K"], default=DEFAULT_IMAGE_SIZE,
        help="输出尺寸（默认 2K）",
    )
    output_group.add_argument(
        "--quality", type=int, default=DEFAULT_QUALITY,
        help="输出质量 1-100（默认 85）",
    )

    # 任务控制
    task_group = parser.add_argument_group("任务控制")
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
    auth_group.add_argument(
        "--secret-id",
        help="腾讯云 SecretId（不传则读取环境变量 TENCENTCLOUD_SECRET_ID）",
    )
    auth_group.add_argument(
        "--secret-key",
        help="腾讯云 SecretKey（不传则读取环境变量 TENCENTCLOUD_SECRET_KEY）",
    )

    args = parser.parse_args()

    # 校验：服装图至少一张
    if not args.cloth_url and not args.cloth_cos_key:
        parser.error("请至少指定一张服装图：--cloth-url 或 --cloth-cos-key")

    return args


# =============================================================================
# 主流程
# =============================================================================

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def main():
    args = parse_args()

    # 命令行传入的 secret 覆盖环境变量
    if args.secret_id:
        os.environ["TENCENTCLOUD_SECRET_ID"] = args.secret_id
    if args.secret_key:
        os.environ["TENCENTCLOUD_SECRET_KEY"] = args.secret_key

    cred = get_credentials()
    region = args.region
    client = create_mps_client(cred, region)

    payload = build_request_payload(args)

    print("🚀 提交图片换装任务...")
    # 打印模特图来源
    if args.model_url:
        print(f"   模特图: {args.model_url}")
    else:
        bucket = args.model_cos_bucket or get_cos_bucket()
        print(f"   模特图: COS - {bucket}:{args.model_cos_key}")
    # 打印服装图来源
    idx = 1
    for url in (args.cloth_url or []):
        print(f"   服装图 {idx}: {url}")
        idx += 1
    for key in (args.cloth_cos_key or []):
        bucket = args.cloth_cos_bucket or get_cos_bucket()
        print(f"   服装图 {idx}: COS - {bucket}:{key}")
        idx += 1
    print(f"   场景 ScheduleId: {args.schedule_id}")

    try:
        submit_result = submit_process_image(client, payload)
    except TencentCloudSDKException as e:
        print(f"错误：提交任务失败 - {e}", file=sys.stderr)
        sys.exit(1)

    task_id = submit_result.get("TaskId", "N/A")
    print("✅ 图片换装任务提交成功！")
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
        print(f"\n❌ 换装任务失败：ErrCode={task_result.get('ErrCode')}，ErrMsg={err_msg}", file=sys.stderr)
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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已中断", file=sys.stderr)
        sys.exit(1)
