#!/usr/bin/env python3
"""
腾讯云 MPS AI 背景融合/生成脚本

功能：
  基于主图（前景/商品/主体图）与背景图，调用 MPS ProcessImage 接口发起 AI 背景融合任务，
  或仅传入主图 + Prompt 描述，自动生成全新背景（背景生成模式）。
  通过 DescribeImageTaskDetail 轮询等待结果，返回输出 COS 路径。

  支持两种模式（均使用 ScheduleId=30060）：
    - 背景融合：传入主图 + 背景图，将主体融合到指定背景场景中
    - 背景生成：仅传入主图 + Prompt，自动生成新背景（不传背景图）

COS 存储约定：
  通过环境变量 TENCENTCLOUD_COS_BUCKET 指定输出 COS Bucket 名称。
  - 输出文件默认目录：/output/bgfusion/

用法：
  # 背景融合（主图 + 背景图，等待结果）
  python scripts/mps_image_bg_fusion.py \\
      --subject-url "https://example.com/product.jpg" \\
      --bg-url "https://example.com/background.jpg"

  # 背景融合 + 附加 Prompt
  python scripts/mps_image_bg_fusion.py \\
      --subject-url "https://example.com/product.jpg" \\
      --bg-url "https://example.com/background.jpg" \\
      --prompt "将背景中的树叶替换为黄色"

  # 背景生成（只有主图 + Prompt，无背景图）
  python scripts/mps_image_bg_fusion.py \\
      --subject-url "https://example.com/product.jpg" \\
      --prompt "简约白色大理石桌面，柔和自然光"

  # 主图使用 COS 路径输入
  python scripts/mps_image_bg_fusion.py \\
      --subject-cos-key "/input/product.jpg" \\
      --bg-url "https://example.com/background.jpg"

  # 主图 + 背景图均使用 COS 路径输入
  python scripts/mps_image_bg_fusion.py \\
      --subject-cos-key "/input/product.jpg" \\
      --bg-cos-key "/input/background.jpg"

  # 背景生成 + 固定随机种子
  python scripts/mps_image_bg_fusion.py \\
      --subject-url "https://example.com/product.jpg" \\
      --prompt "现代简约家居客厅背景" \\
      --random-seed 42

  # 只提交任务，不等待结果（返回 TaskId）
  python scripts/mps_image_bg_fusion.py \\
      --subject-url "https://example.com/product.jpg" \\
      --prompt "简约白色大理石桌面" \\
      --no-wait

  # 指定输出格式与尺寸
  python scripts/mps_image_bg_fusion.py \\
      --subject-url "https://example.com/product.jpg" \\
      --prompt "户外草坪，阳光明媚" \\
      --format PNG --image-size 4K

环境变量：
  TENCENTCLOUD_SECRET_ID    - 腾讯云 SecretId（必须）
  TENCENTCLOUD_SECRET_KEY   - 腾讯云 SecretKey（必须）
  TENCENTCLOUD_API_REGION   - MPS API 接入地域（必需）
  TENCENTCLOUD_COS_BUCKET   - 输出 COS Bucket（可被 --output-bucket 覆盖）
                              同时作为 --subject-cos-key / --bg-cos-key 的默认 Bucket
  TENCENTCLOUD_COS_REGION   - 输出 COS Region（可被 --output-region 覆盖）
                              同时作为 --subject-cos-key / --bg-cos-key 的默认 Region
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
SCHEDULE_ID = 30060  # AI 背景融合/生成固定 ScheduleId
DEFAULT_OUTPUT_DIR = "/output/bgfusion/"
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
    addon_parameter = {
        "OutputConfig": {
            "Format": args.format,
            "ImageSize": args.image_size,
            "Quality": args.quality,
        },
    }

    # ExtPrompt：背景生成模式下必填，背景融合模式下可选
    if args.prompt:
        addon_parameter["ExtPrompt"] = [{"Prompt": p} for p in args.prompt]

    # ImageSet：传入背景图时为背景融合模式
    if args.bg_url or args.bg_cos_key:
        image_set = []
        if args.bg_url:
            image_set.append({"Image": build_url_input(args.bg_url)})
        elif args.bg_cos_key:
            image_set.append({
                "Image": build_cos_input(args.bg_cos_key, args.bg_cos_bucket, args.bg_cos_region)
            })
        addon_parameter["ImageSet"] = image_set

    output_bucket = args.output_bucket or get_cos_bucket()
    output_region = args.output_region or get_cos_region()

    if not output_bucket:
        print(
            "错误：缺少输出 Bucket，请传入 --output-bucket 或设置 TENCENTCLOUD_COS_BUCKET",
            file=sys.stderr,
        )
        sys.exit(1)

    # 构造主图输入
    subject_input = build_media_input(
        url=args.subject_url,
        cos_key=args.subject_cos_key,
        cos_bucket=args.subject_cos_bucket,
        cos_region=args.subject_cos_region,
        label="主图",
    )

    payload = {
        "InputInfo": subject_input,
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
    """调用 ProcessImage 提交背景融合/生成任务。"""
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
        description="腾讯云 MPS AI 背景融合/生成（ProcessImage ScheduleId=30060）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # 输入参数
    input_group = parser.add_argument_group("输入参数")
    # 主图（URL 或 COS，二选一）
    subject_group = input_group.add_mutually_exclusive_group(required=True)
    subject_group.add_argument(
        "--subject-url",
        help="主图（前景/商品/主体）URL（与 --subject-cos-key 二选一）",
    )
    subject_group.add_argument(
        "--subject-cos-key",
        help="主图 COS 对象 Key（如 /input/product.jpg），与 --subject-url 二选一",
    )
    input_group.add_argument(
        "--subject-cos-bucket",
        help="主图 COS Bucket（默认读取 TENCENTCLOUD_COS_BUCKET）",
    )
    input_group.add_argument(
        "--subject-cos-region",
        help="主图 COS Region（默认读取 TENCENTCLOUD_COS_REGION）",
    )
    # 背景图（URL 或 COS，二选一；不传则为背景生成模式）
    bg_group = input_group.add_mutually_exclusive_group()
    bg_group.add_argument(
        "--bg-url",
        help="背景图 URL；不传则为背景生成模式（与 --bg-cos-key 二选一）",
    )
    bg_group.add_argument(
        "--bg-cos-key",
        help="背景图 COS 对象 Key（如 /input/bg.jpg），与 --bg-url 二选一",
    )
    input_group.add_argument(
        "--bg-cos-bucket",
        help="背景图 COS Bucket（默认读取 TENCENTCLOUD_COS_BUCKET）",
    )
    input_group.add_argument(
        "--bg-cos-region",
        help="背景图 COS Region（默认读取 TENCENTCLOUD_COS_REGION）",
    )

    # 融合/生成参数
    fusion_group = parser.add_argument_group("融合/生成参数")
    fusion_group.add_argument(
        "--prompt", action="append",
        help="背景描述或融合需求提示词，可重复传入多次；背景生成模式下必填",
    )
    fusion_group.add_argument(
        "--random-seed", type=int,
        help="随机种子（StdExtInfo.ModelConfig.RandomSeed），固定种子可获得稳定风格",
    )
    fusion_group.add_argument(
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
        help="自定义输出路径（需带文件后缀，如 /output/bgfusion/result.jpg）",
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

    # 背景生成模式下必须提供 prompt
    if not args.bg_url and not args.bg_cos_key and not args.prompt:
        parser.error("背景生成模式下（不传背景图时）必须提供 --prompt 来描述要生成的背景")

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

    # 判断模式
    has_bg = bool(args.bg_url or args.bg_cos_key)
    mode = "背景融合" if has_bg else "背景生成"

    print(f"🚀 提交{mode}任务...")
    # 打印主图来源
    if args.subject_url:
        print(f"   主图: {args.subject_url}")
    else:
        bucket = args.subject_cos_bucket or get_cos_bucket()
        print(f"   主图: COS - {bucket}:{args.subject_cos_key}")
    # 打印背景图来源
    if has_bg:
        if args.bg_url:
            print(f"   背景图: {args.bg_url}")
        else:
            bucket = args.bg_cos_bucket or get_cos_bucket()
            print(f"   背景图: COS - {bucket}:{args.bg_cos_key}")
    # 打印 Prompt
    if args.prompt:
        for p in args.prompt:
            print(f"   Prompt: {p}")
    print(f"   模式: {mode}（ScheduleId={SCHEDULE_ID}）")

    try:
        submit_result = submit_process_image(client, payload)
    except TencentCloudSDKException as e:
        print(f"错误：提交任务失败 - {e}", file=sys.stderr)
        sys.exit(1)

    task_id = submit_result.get("TaskId", "N/A")
    print(f"✅ {mode}任务提交成功！")
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
        print(f"\n❌ {mode}任务失败：ErrCode={task_result.get('ErrCode')}，ErrMsg={err_msg}", file=sys.stderr)
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
