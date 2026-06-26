#!/usr/bin/env python3
"""
腾讯云 MPS 换模特/换体型脚本

功能：
  基于原图（模特/场景图）与衣物图，调用 MPS ProcessImage 接口发起 AI 换模特任务，
  并通过 DescribeImageTaskDetail 轮询等待结果，返回输出 COS 路径。

  使用 ScheduleId=30110，支持指定目标体型和处理精度。

COS 存储约定：
  通过环境变量 TENCENTCLOUD_COS_BUCKET 指定输出 COS Bucket 名称。
  - 输出文件默认目录：/output/changemodel/

用法：
  # 最简用法：原图 URL + 衣物图 URL（默认 hourglass 体型）
  python scripts/mps_image_changemodel.py \\
      --url "https://example.com/model.jpg" \\
      --garment-url "https://example.com/garment.jpg"

  # 指定体型为 pear（梨形）
  python scripts/mps_image_changemodel.py \\
      --url "https://example.com/model.jpg" \\
      --garment-url "https://example.com/garment.jpg" \\
      --body-shape pear

  # 指定体型为 plus-size + 提高精度
  python scripts/mps_image_changemodel.py \\
      --url "https://example.com/model.jpg" \\
      --garment-url "https://example.com/garment.jpg" \\
      --body-shape plus-size --precision-scale 1.5

  # 原图使用 COS 路径输入
  python scripts/mps_image_changemodel.py \\
      --cos-input-key "/input/model.jpg" \\
      --garment-url "https://example.com/garment.jpg" \\
      --body-shape rectangle

  # 衣物图使用 COS 路径输入
  python scripts/mps_image_changemodel.py \\
      --url "https://example.com/model.jpg" \\
      --garment-cos-key "/input/garment.jpg" \\
      --body-shape apple

  # 原图使用本地文件（自动上传 COS）
  python scripts/mps_image_changemodel.py \\
      --local-file ./model.jpg \\
      --garment-url "https://example.com/garment.jpg" \\
      --body-shape hourglass

  # 只提交任务，不等待结果（返回 TaskId）
  python scripts/mps_image_changemodel.py \\
      --url "https://example.com/model.jpg" \\
      --garment-url "https://example.com/garment.jpg" \\
      --no-wait

  # 预览请求体（不实际调用 API）
  python scripts/mps_image_changemodel.py \\
      --url "https://example.com/model.jpg" \\
      --garment-url "https://example.com/garment.jpg" \\
      --body-shape pear --dry-run

  # 完成后自动下载结果到本地目录
  python scripts/mps_image_changemodel.py \\
      --url "https://example.com/model.jpg" \\
      --garment-url "https://example.com/garment.jpg" \\
      --download-dir ./results/

环境变量：
  TENCENTCLOUD_SECRET_ID    - 腾讯云 SecretId（必须）
  TENCENTCLOUD_SECRET_KEY   - 腾讯云 SecretKey（必须）
  TENCENTCLOUD_API_REGION   - MPS API 接入地域（必需）
  TENCENTCLOUD_COS_BUCKET   - 输出 COS Bucket（可被 --output-bucket 覆盖）
                              同时作为 --cos-input-key / --garment-cos-key 的默认 Bucket
  TENCENTCLOUD_COS_REGION   - 输出 COS Region（可被 --output-region 覆盖）
                              同时作为 --cos-input-key / --garment-cos-key 的默认 Region
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
SCHEDULE_ID = 30110  # 换模特/换体型固定 ScheduleId
DEFAULT_OUTPUT_DIR = "/output/changemodel/"
DEFAULT_BODY_SHAPE = "hourglass"
DEFAULT_PRECISION_SCALE = 1.0
BODY_SHAPE_CHOICES = ["hourglass", "rectangle", "plus-size", "apple", "pear"]
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


def build_request_payload(args, input_cos_key=None):
    """组装 ProcessImage 请求体。"""
    # 构造原图/模特图输入
    if input_cos_key:
        # 本地文件上传后使用 COS 输入
        input_info = build_cos_input(input_cos_key, args.cos_input_bucket, args.cos_input_region)
    else:
        input_info = build_media_input(
            url=args.url,
            cos_key=args.cos_input_key,
            cos_bucket=args.cos_input_bucket,
            cos_region=args.cos_input_region,
            label="原图/模特图",
        )

    # 构造衣物图输入
    garment_input = build_media_input(
        url=args.garment_url,
        cos_key=args.garment_cos_key,
        cos_bucket=args.garment_cos_bucket,
        cos_region=args.garment_cos_region,
        label="衣物图",
    )

    output_bucket = args.output_bucket or get_cos_bucket()
    output_region = args.output_region or get_cos_region()

    if not output_bucket:
        print(
            "错误：缺少输出 Bucket，请传入 --output-bucket 或设置 TENCENTCLOUD_COS_BUCKET",
            file=sys.stderr,
        )
        sys.exit(1)

    # 构造 StdExtInfo
    std_ext_info = json.dumps(
        {
            "ChangeGarmentModelConfig": {
                "BodyShape": args.body_shape,
                "PrecisionScale": args.precision_scale,
            }
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )

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
        "AddOnParameter": {"ImageSet": [{"Type": "garment", "Image": garment_input}]},
        "StdExtInfo": std_ext_info,
    }

    if args.output_path:
        payload["OutputPath"] = args.output_path


    return payload


def submit_process_image(client, payload):
    """调用 ProcessImage 提交换模特任务。"""
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
        description="腾讯云 MPS 换模特/换体型（ProcessImage ScheduleId=30110）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # 输入源(原图/模特图)
    input_group = parser.add_argument_group("输入源(原图/模特图)")
    source_group = input_group.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--url",
        help="原图/模特图 URL（与 --cos-input-key / --local-file 三选一）",
    )
    source_group.add_argument(
        "--cos-input-key",
        help="原图/模特图 COS 对象 Key（如 /input/model.jpg），与 --url / --local-file 三选一",
    )
    source_group.add_argument(
        "--local-file",
        help="原图/模特图本地路径（自动上传 COS），与 --url / --cos-input-key 三选一",
    )
    input_group.add_argument(
        "--cos-input-bucket",
        help="原图 COS Bucket（默认读取 TENCENTCLOUD_COS_BUCKET）",
    )
    input_group.add_argument(
        "--cos-input-region",
        help="原图 COS Region（默认读取 TENCENTCLOUD_COS_REGION）",
    )

    # 衣物图输入
    garment_group = parser.add_argument_group("衣物图输入")
    garment_mutex = garment_group.add_mutually_exclusive_group(required=True)
    garment_mutex.add_argument(
        "--garment-url",
        help="衣物图 URL（与 --garment-cos-key 二选一）",
    )
    garment_mutex.add_argument(
        "--garment-cos-key",
        help="衣物图 COS 对象 Key（如 /input/garment.jpg），与 --garment-url 二选一",
    )
    garment_group.add_argument(
        "--garment-cos-bucket",
        help="衣物图 COS Bucket（默认读取 TENCENTCLOUD_COS_BUCKET）",
    )
    garment_group.add_argument(
        "--garment-cos-region",
        help="衣物图 COS Region（默认读取 TENCENTCLOUD_COS_REGION）",
    )

    # 换模特参数
    model_group = parser.add_argument_group("换模特参数")
    model_group.add_argument(
        "--body-shape", choices=BODY_SHAPE_CHOICES, default=DEFAULT_BODY_SHAPE,
        help="目标体型：hourglass/rectangle/plus-size/apple/pear（默认 hourglass）",
    )
    model_group.add_argument(
        "--precision-scale", type=float, default=DEFAULT_PRECISION_SCALE,
        metavar="FLOAT",
        help="处理精度 [0.01, 2.0]，值越大精度越高速度越慢（默认 1.0）",
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
        help="自定义输出路径（需带文件后缀，如 /output/changemodel/result.jpg）",
    )
    output_group.add_argument(
        "--download-dir",
        help="任务完成后自动下载结果到本地目录",
    )

    # 任务控制
    task_group = parser.add_argument_group("任务控制")
    task_group.add_argument(
        "--dry-run", action="store_true",
        help="仅打印请求体，不实际调用 API",
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

    # 校验 precision-scale 范围
    if args.precision_scale < 0.01 or args.precision_scale > 2.0:
        parser.error("--precision-scale 取值范围为 [0.01, 2.0]")

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

    # 处理本地文件上传
    input_cos_key = None
    if args.local_file:
        upload_result = auto_upload_local_file(args.local_file)
        if not upload_result:
            print("错误：本地文件上传失败", file=sys.stderr)
            sys.exit(1)
        input_cos_key = upload_result["Key"]

    payload = build_request_payload(args, input_cos_key=input_cos_key)

    # --dry-run：仅打印请求体
    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print("🚀 提交换模特/换体型任务...")
    # 打印原图来源
    if args.url:
        print(f"   原图: {args.url}")
    elif args.local_file:
        print(f"   原图: 本地文件 {args.local_file} (已上传 COS)")
    else:
        bucket = get_cos_bucket()
        print(f"   原图: COS - {bucket}:{args.cos_input_key}")
    # 打印衣物图来源
    if args.garment_url:
        print(f"   衣物图: {args.garment_url}")
    else:
        bucket = args.garment_cos_bucket or get_cos_bucket()
        print(f"   衣物图: COS - {bucket}:{args.garment_cos_key}")
    print(f"   体型: {args.body_shape}")
    print(f"   精度: {args.precision_scale}")
    print(f"   ScheduleId: {SCHEDULE_ID}")

    try:
        submit_result = submit_process_image(client, payload)
    except TencentCloudSDKException as e:
        print(f"错误：提交任务失败 - {e}", file=sys.stderr)
        sys.exit(1)

    task_id = submit_result.get("TaskId", "N/A")
    print("✅ 换模特任务提交成功！")
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
        print(f"\n❌ 换模特任务失败：ErrCode={task_result.get('ErrCode')}，ErrMsg={err_msg}", file=sys.stderr)
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

    # --download-dir：自动下载结果
    if args.download_dir:
        auto_download_outputs(task_result, download_dir=args.download_dir)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已中断", file=sys.stderr)
        sys.exit(1)
