#!/usr/bin/env python3
"""
腾讯云 MPS 图片换装脚本（AI 试衣）

功能：
  基于模特图与服装图，调用 MPS ProcessImage 接口发起 AI 换装任务（ImageTask.AiTryOnConfig），
  并通过 DescribeImageTaskDetail 轮询等待结果，返回输出路径。

  支持的换装模型：
    - WAND-tryon-1.0-lite：轻量版
    - WAND-tryon-1.0-flash：快速版（默认）
    - WAND-tryon-1.0-pro：专业版

COS 存储约定：
  通过环境变量 TENCENTCLOUD_COS_BUCKET 指定输出 COS Bucket 名称。
  - 输出文件默认目录：/output/tryon/

用法：
  # 最简用法：模特图 + 服装图（URL，默认等待结果）
  python3 scripts/mps_image_tryon.py \\
      --model-url "https://example.com/model.jpg" \\
      --cloth-url "https://example.com/cloth.jpg"

  # 指定模型
  python3 scripts/mps_image_tryon.py \\
      --model-url "https://example.com/model.jpg" \\
      --cloth-url "https://example.com/cloth.jpg" \\
      --model WAND-tryon-1.0-pro

  # 模特图使用 COS 路径输入
  python3 scripts/mps_image_tryon.py \\
      --model-cos-key "/input/model.jpg" \\
      --cloth-url "https://example.com/cloth.jpg"

  # 模特图 + 服装图均使用 COS 路径输入
  python3 scripts/mps_image_tryon.py \\
      --model-cos-key "/input/model.jpg" \\
      --cloth-cos-key "/input/cloth.jpg"

  # 多张服装图（1-4 张）
  python3 scripts/mps_image_tryon.py \\
      --model-url "https://example.com/model.jpg" \\
      --cloth-url "https://example.com/cloth-front.jpg" \\
      --cloth-url "https://example.com/cloth-back.jpg"

  # 本地文件换装（自动上传 COS 后传入 API，需配置 TENCENTCLOUD_COS_BUCKET）
  python3 scripts/mps_image_tryon.py \\
      --model-local /data/model.jpg \\
      --cloth-local /data/cloth.jpg

  # 附加提示词
  python3 scripts/mps_image_tryon.py \\
      --model-url "https://example.com/model.jpg" \\
      --cloth-url "https://example.com/cloth.jpg" \\
      --prompt "将衬衫换为红色"

  # 指定输出分辨率
  python3 scripts/mps_image_tryon.py \\
      --model-url "https://example.com/model.jpg" \\
      --cloth-url "https://example.com/cloth.jpg" \\
      --resolution 4K

  # 只提交任务，不等待结果（返回 TaskId）
  python3 scripts/mps_image_tryon.py \\
      --model-url "https://example.com/model.jpg" \\
      --cloth-url "https://example.com/cloth.jpg" \\
      --no-wait

  # 指定输出 Bucket 和目录
  python3 scripts/mps_image_tryon.py \\
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

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)
from mps_auto_upgrade import check_sdk_version

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
    print("错误：请先安装腾讯云 SDK：python3 -m pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# 默认参数
# =============================================================================
DEFAULT_MODEL = "WAND-tryon-1.0-flash"
MODEL_CHOICES = ["WAND-tryon-1.0-lite", "WAND-tryon-1.0-flash", "WAND-tryon-1.0-pro"]
DEFAULT_OUTPUT_DIR = "/output/tryon/"
DEFAULT_RESOLUTION = "1K"
DEFAULT_POLL_INTERVAL = 10
DEFAULT_TIMEOUT = 600


# =============================================================================
# 工具函数
# =============================================================================

def get_credentials():
    """从环境变量获取腾讯云凭证。若缺失则尝试从 dotenv 文件自动加载后重试。"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        # 凭证可能写在 ~/.env 等 dotenv 文件中而未导出，先尝试加载再重试
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
                    "请在 ~/.env、~/.bashrc、~/.profile 或 <SKILL_DIR>/.env 中添加这些变量。\n",
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
    http_profile.reqMethod = "POST"
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
    """组装 ProcessImage 请求体。AiTryOnConfig 部分使用 SDK 原生模型序列化。"""
    # 收集服装图列表
    cloth_inputs = []
    for url in (args.cloth_url or []):
        cloth_inputs.append({"Image": build_url_input(url)})
    for key in (args.cloth_cos_key or []):
        cloth_inputs.append({"Image": build_cos_input(key, args.cloth_cos_bucket, args.cloth_cos_region)})

    if not cloth_inputs:
        print("错误：请至少指定一张服装图（--cloth-url / --cloth-cos-key / --cloth-local）", file=sys.stderr)
        sys.exit(1)

    if len(cloth_inputs) > 4:
        print("错误：最多支持 4 张服装图，当前传入了 {} 张".format(len(cloth_inputs)), file=sys.stderr)
        sys.exit(1)

    # AiTryOnConfig
    ai_tryon_config = {"Model": args.model, "Resolution": args.resolution}
    if args.prompt:
        ai_tryon_config["Prompt"] = args.prompt

    payload = {
        "InputInfo": build_media_input(
            url=args.model_url,
            cos_key=args.model_cos_key,
            cos_bucket=args.model_cos_bucket,
            cos_region=args.model_cos_region,
            label="模特图",
        ),
        "OutputDir": args.output_dir,
        "ImageTask": {"AiTryOnConfig": ai_tryon_config},
        "AddOnParameter": {"ImageSet": cloth_inputs},
    }

    output_bucket = args.output_bucket or get_cos_bucket()
    output_region = args.output_region or get_cos_region()
    if not output_bucket:
        print(
            "错误：缺少输出 Bucket，请传入 --output-bucket 或设置 TENCENTCLOUD_COS_BUCKET",
            file=sys.stderr,
        )
        sys.exit(1)
    payload["OutputStorage"] = {
        "Type": "COS",
        "CosOutputStorage": {"Bucket": output_bucket, "Region": output_region},
    }

    if args.output_path:
        payload["OutputPath"] = args.output_path
    if args.resource_id:
        payload["ResourceId"] = args.resource_id

    return payload


def submit_process_image(client, payload):
    """调用 ProcessImage 提交换装任务。"""
    req = models.ProcessImageRequest()
    req.from_json_string(json.dumps(payload, ensure_ascii=False))
    resp = client.ProcessImage(req)
    return {"TaskId": resp.TaskId, "RequestId": resp.RequestId}


# =============================================================================
# 参数解析
# =============================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="腾讯云 MPS 图片换装（ProcessImage ImageTask.AiTryOnConfig）",
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
    model_group.add_argument(
        "--model-local",
        help="模特图本地文件路径，自动上传 COS 后传入 API（需配置 TENCENTCLOUD_COS_BUCKET）；与 --model-url / --model-cos-key 三选一",
    )
    input_group.add_argument(
        "--model-cos-bucket",
        help="模特图 COS Bucket（默认读取 TENCENTCLOUD_COS_BUCKET）",
    )
    input_group.add_argument(
        "--model-cos-region",
        help="模特图 COS Region（默认读取 TENCENTCLOUD_COS_REGION）",
    )
    # 服装图（URL 或 COS，1-4 张，可混用）
    input_group.add_argument(
        "--cloth-url", action="append", default=[],
        help="服装图 URL，可重复传入 1-4 次；与 --cloth-cos-key 可混用",
    )
    input_group.add_argument(
        "--cloth-cos-key", action="append", default=[],
        help="服装图 COS 对象 Key，可重复传入 1-4 次；与 --cloth-url 可混用",
    )
    input_group.add_argument(
        "--cloth-local", action="append", default=[],
        help="服装图本地文件路径，可重复传入 1-4 次，自动上传 COS 后传入 API；与 --cloth-url / --cloth-cos-key 可混用",
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
        "--model", choices=MODEL_CHOICES, default=DEFAULT_MODEL,
        help="换装模型：WAND-tryon-1.0-lite（轻量）/ WAND-tryon-1.0-flash（快速，默认）/ WAND-tryon-1.0-pro（专业）",
    )
    tryon_group.add_argument(
        "--prompt",
        help="换装指令（可选，为空时使用内置默认指令）",
    )
    tryon_group.add_argument(
        "--resource-id",
        help="可选的资源 ID（业务侧专属资源）",
    )

    # 输出参数
    output_group = parser.add_argument_group("输出参数")
    output_group.add_argument(
        "--resolution", choices=["1K", "2K", "4K"], default=DEFAULT_RESOLUTION,
        help="输出分辨率（默认 1K）",
    )
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
    auth_group.add_argument(
        "--secret-id",
        help="腾讯云 SecretId（不传则读取环境变量 TENCENTCLOUD_SECRET_ID）",
    )
    auth_group.add_argument(
        "--secret-key",
        help="腾讯云 SecretKey（不传则读取环境变量 TENCENTCLOUD_SECRET_KEY）",
    )

    args = parser.parse_args()

    # 本地文件自动上传（先上传到 COS，再以 COS Key 传入 API）
    if args.model_local or args.cloth_local:
        if not _POLL_AVAILABLE:
            print("错误：--model-local / --cloth-local 需要 mps_poll_task 模块支持", file=sys.stderr)
            sys.exit(1)

    if args.model_local:
        upload_result = auto_upload_local_file(args.model_local)
        if not upload_result:
            sys.exit(1)
        args.model_cos_key = upload_result["Key"]
        args.model_cos_bucket = upload_result["Bucket"]
        args.model_cos_region = upload_result["Region"]

    if args.cloth_local:
        for local_path in args.cloth_local:
            upload_result = auto_upload_local_file(local_path)
            if not upload_result:
                sys.exit(1)
            args.cloth_cos_key.append(upload_result["Key"])
            # 服装图统一使用同一 Bucket/Region（auto_upload_local_file 依据环境变量上传）
            if not args.cloth_cos_bucket:
                args.cloth_cos_bucket = upload_result["Bucket"]
            if not args.cloth_cos_region:
                args.cloth_cos_region = upload_result["Region"]

    # 校验：服装图至少一张
    if not args.cloth_url and not args.cloth_cos_key:
        parser.error("请至少指定一张服装图：--cloth-url / --cloth-cos-key / --cloth-local")

    return args


# =============================================================================
# 主流程
# =============================================================================

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def main():
    # 时序修复：先加载 .env，让 argparse default=os.environ.get(...) 能读到用户配置
    if _LOAD_ENV_AVAILABLE:
        try:
            _ensure_env_loaded(verbose=False)
        except Exception:
            pass
    args = parse_args()

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
    print(f"   模型: {args.model}")
    if args.prompt:
        print(f"   Prompt: {args.prompt}")

    if args.dry_run:
        print("\n【dry-run】请求体预览：")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    # 正常执行：需要密钥
    cred = get_credentials()
    client = create_mps_client(cred, region)

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
        print(f"   python3 scripts/mps_get_image_task.py --task-id {task_id}", file=sys.stderr)
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
        print(f"   可手动查询：python3 scripts/mps_get_image_task.py --task-id {task_id}", file=sys.stderr)
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
