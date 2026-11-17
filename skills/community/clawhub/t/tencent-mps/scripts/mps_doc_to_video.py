#!/usr/bin/env python3
"""
腾讯云 MPS AIGC 文档生成视频脚本

功能：
  使用 MPS AIGC 场景应用能力，将文档（PDF / PPTX / DOCX / PNG / JPG）自动生成讲解视频，
  适用于教学视频、产品讲解、内容速览等场景。
  封装 CreateDocToVideoTask + DescribeAigcTaskStatus 两个 API，
  支持创建任务 + 自动轮询等待结果。

核心能力：
  - 支持最多 3 个文档输入（PDF/PPTX/DOCX/PNG/JPG），单个不超过 10MB，最多 100 页
  - Prompt 描述生成意图（如"帮我生成一个教学视频"）
  - 可选 AI 配音（EnableTTS + VoiceId）
  - 支持中/英/日/韩/俄/法/西/德多语言生成
  - 支持指定生成视频的宽高比（16:9 / 9:16 / 1:1）与参考时长
  - 结果存储到 COS（可选，默认使用 MPS 临时存储）

⚠️ 计费提示：调用会产生实际费用，请参考 MPS 计费文档。

用法：
  # 最简用法：单文档 + prompt
  python3 mps_doc_to_video.py --url https://example.com/sample.pdf \\
      --prompt "根据文档内容，帮我生成一个教学视频"

  # 多文档输入（最多3个）
  python3 mps_doc_to_video.py \\
      --url https://example.com/a.pdf --url https://example.com/b.pptx \\
      --prompt "帮我把这两份文档整合成一个产品介绍视频"

  # 指定宽高比 + 语言 + 参考时长
  python3 mps_doc_to_video.py --url https://example.com/sample.docx \\
      --prompt "生成一个产品介绍视频" --aspect-ratio 9:16 --language en --reference-duration 60

  # 开启 AI 配音（需指定音色 ID）
  python3 mps_doc_to_video.py --url https://example.com/sample.pdf \\
      --prompt "生成教学视频" --enable-tts --voice-id v1_shUQBcs3N6VrPd9RMTf50H7M5kxeZ1VHIiWGDzq5Q9pE0HoEQ959hpulWHGFZSp3v4w=

  # 本地文档（自动上传到 COS 后传入 API）
  python3 mps_doc_to_video.py --local-file /path/to/sample.pdf \\
      --prompt "生成教学视频"

  # 结果存储到 COS
  python3 mps_doc_to_video.py --url https://example.com/sample.pdf \\
      --prompt "生成宣传片" --output-bucket mybucket-125xxx --output-region ap-guangzhou

  # 仅创建任务不等待
  python3 mps_doc_to_video.py --url https://example.com/sample.pdf --prompt "生成视频" --no-wait

  # 查询已有任务结果
  python3 mps_doc_to_video.py --task-id e084efaa-d25a-xxxx-xxxx-6b85e473c0e5

  # Dry Run（仅打印请求参数）
  python3 mps_doc_to_video.py --url https://example.com/sample.pdf --prompt "测试" --dry-run

环境变量：
  TENCENTCLOUD_SECRET_ID   - 腾讯云 SecretId
  TENCENTCLOUD_SECRET_KEY  - 腾讯云 SecretKey
  TENCENTCLOUD_COS_BUCKET  - COS Bucket 名称（可选，用于结果存储 / 本地文件上传）
  TENCENTCLOUD_COS_REGION  - COS Bucket 区域（默认 ap-guangzhou）
"""

import argparse
import json
import os
import sys
import time


# 同目录辅助模块
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
from mps_auto_upgrade import check_sdk_version

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

# COS SDK（可选，用于本地文件上传 / 生成临时URL）
try:
    from qcloud_cos import CosConfig, CosS3Client
    _COS_SDK_AVAILABLE = True
except ImportError:
    _COS_SDK_AVAILABLE = False

try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False


# =============================================================================
# 常量
# =============================================================================

DEFAULT_MODEL_NAME = "Wand"
DEFAULT_MODEL_VERSION = "1.0"

SUPPORTED_RATIOS = ["16:9", "9:16", "1:1"]

SUPPORTED_LANGUAGES = {
    "zh": "中文", "en": "英文", "ja": "日语", "ko": "韩语",
    "ru": "俄语", "fr": "法语", "es": "西班牙语", "de": "德语",
}

SUPPORTED_DOC_EXTS = (".pdf", ".pptx", ".docx", ".png", ".jpg", ".jpeg")

MAX_FILES = 3
MAX_LOCAL_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# 轮询配置
DEFAULT_POLL_INTERVAL = 10   # 秒
DEFAULT_MAX_WAIT = 1800      # 最长等待30分钟


# =============================================================================
# COS 工具函数
# =============================================================================

def get_cos_bucket():
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    return os.environ.get("TENCENTCLOUD_COS_REGION", "ap-guangzhou")


def get_cos_presigned_url(bucket, region, key, secret_id=None, secret_key=None, expired=3600):
    """生成 COS 临时访问 URL（预签名 URL）。失败返回 None。"""
    if not _COS_SDK_AVAILABLE:
        print("警告：COS SDK 未安装，无法生成临时 URL。请安装：python3 -m pip install cos-python-sdk-v5",
              file=sys.stderr)
        return None

    secret_id = secret_id or os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = secret_key or os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        print("警告：缺少腾讯云密钥，无法生成临时 URL", file=sys.stderr)
        return None

    try:
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
        client = CosS3Client(config)
        return client.get_presigned_url(Method="GET", Bucket=bucket, Key=key, Expired=expired)
    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
        print(f"警告：生成临时 URL 失败: {e}", file=sys.stderr)
        return None


def upload_to_cos(local_path, bucket, region, cos_key=None, secret_id=None, secret_key=None):
    """上传本地文档到 COS，返回预签名 URL。失败则 sys.exit(1)。"""
    import uuid as _uuid

    if not _COS_SDK_AVAILABLE:
        print("❌ 错误：COS SDK 未安装，无法上传本地文件。请安装：python3 -m pip install cos-python-sdk-v5",
              file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(local_path):
        print(f"❌ 错误：本地文件不存在: {local_path}", file=sys.stderr)
        sys.exit(1)

    file_size = os.path.getsize(local_path)
    if file_size > MAX_LOCAL_FILE_SIZE:
        print(f"❌ 错误：本地文件超过 10MB 限制（当前 {file_size / 1024 / 1024:.2f} MB）: {local_path}",
              file=sys.stderr)
        sys.exit(1)

    ext = os.path.splitext(local_path)[1].lower()
    if ext not in SUPPORTED_DOC_EXTS:
        print(f"❌ 错误：不支持的文档格式 {ext}，支持：pdf/pptx/docx/png/jpg", file=sys.stderr)
        sys.exit(1)

    secret_id = secret_id or os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = secret_key or os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        print("❌ 错误：上传本地文件需要 TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
        sys.exit(1)

    if not cos_key:
        ts = int(time.time())
        uid = str(_uuid.uuid4())[:8]
        filename = os.path.basename(local_path)
        cos_key = f"doc_to_video_input/{ts}_{uid}_{filename}"
    cos_key = cos_key.lstrip("/")

    try:
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
        client = CosS3Client(config)
        print(f"⬆️  上传本地文档到 COS: {local_path} → {bucket}/{cos_key}", file=sys.stderr)
        client.upload_file(
            Bucket=bucket, LocalFilePath=local_path, Key=cos_key,
            PartSize=10, MAXThread=5, EnableMD5=False
        )
    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
        print(f"❌ 上传 COS 失败: {e}", file=sys.stderr)
        sys.exit(1)

    url = get_cos_presigned_url(bucket, region, cos_key, secret_id, secret_key, expired=3600)
    if not url:
        url = f"https://{bucket}.cos.{region}.myqcloud.com/{cos_key}"
        print(f"⚠️  预签名失败，使用公开 URL（需桶为公读）: {url}", file=sys.stderr)
    else:
        print("✅ 上传成功，预签名 URL 已生成", file=sys.stderr)
    return url


def ensure_signed_url(url, expired=86400):
    """
    若 url 是裸 COS URL（无 query 签名），自动重签为带签名的临时 URL。

    Returns:
        (final_url, status): status ∈ {'not_url','already_signed','auto_signed','sign_failed','not_cos'}
    """
    if not url or not isinstance(url, str):
        return url, 'not_url'
    if not url.startswith(("http://", "https://")):
        return url, 'not_url'
    from urllib.parse import urlparse
    parsed = urlparse(url)
    if parsed.query:
        return url, 'already_signed'
    import re
    m = re.match(
        r"https?://([\w\-]+)\.cos\.([\w\-]+)\.(?:myqcloud\.com|tencentcos\.cn)/(.+)",
        url,
    )
    if not m:
        return url, 'not_cos'
    bucket, region, key = m.group(1), m.group(2), m.group(3)
    signed = get_cos_presigned_url(bucket, region, key, expired=expired)
    if signed and '?' in signed:
        return signed, 'auto_signed'
    return url, 'sign_failed'


def print_storage_hint(statuses):
    """根据 ensure_signed_url 返回的一组状态，打印对应的存储/有效期提示语。"""
    if not statuses:
        return
    modes = set(statuses)
    if modes == {'already_signed'}:
        print("\n⚠️  MPS 临时存储，链接有效期有限，请尽快下载使用。")
    elif 'auto_signed' in modes and 'sign_failed' not in modes:
        print("\n💡 视频已写回您的 COS 桶（永久保存）；已自动生成 24 小时临时签名链接，过期后请重新签名访问。")
    elif 'sign_failed' in modes:
        print("\n⚠️  视频已写回您的 COS 桶，但临时签名生成失败（请检查 cos-python-sdk-v5 与 TENCENTCLOUD_SECRET_ID/KEY）；")
        print("    若桶为私有读，需手动签名后访问。")
    elif modes == {'not_cos'}:
        print("\n💡 视频 URL 由第三方源站提供，访问时效以源站为准。")
    else:
        print("\n💡 视频链接可能来自不同来源，请按需自行验证有效期。")


# =============================================================================
# 凭证与客户端
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


def create_mps_client(cred, region):
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    http_profile.reqMethod = "POST"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return mps_client.MpsClient(cred, region, client_profile)


# =============================================================================
# 参数构建
# =============================================================================

def build_store_cos_param(args):
    """构建 CosInfo 存储参数。"""
    bucket_name = args.output_bucket or get_cos_bucket()
    bucket_region = args.output_region or get_cos_region()
    if not bucket_name:
        return None
    cos_param = {"CosBucketName": bucket_name, "CosBucketRegion": bucket_region}
    if args.output_dir:
        cos_param["CosBucketPath"] = args.output_dir
    return cos_param


def build_create_params(args):
    """构建 CreateDocToVideoTask 请求参数。"""
    # 收集所有文档来源（URL + 本地文件），统一转为 FileUrl 列表
    file_urls = []
    if args.url:
        file_urls.extend(args.url)

    if getattr(args, "local_file", None):
        upload_bucket = args.output_bucket or get_cos_bucket()
        upload_region = args.output_region or get_cos_region()
        if not upload_bucket:
            print("❌ 错误：--local-file 需要配置 COS Bucket（--output-bucket 或 TENCENTCLOUD_COS_BUCKET）",
                  file=sys.stderr)
            sys.exit(1)
        for local_path in args.local_file:
            url = upload_to_cos(local_path, upload_bucket, upload_region)
            file_urls.append(url)

    doc_input = {
        "FileUrl": file_urls,
        "Prompt": args.prompt,
        "ModelName": args.model_name,
        "ModelVersion": args.model_version,
    }

    if args.aspect_ratio:
        doc_input["Ratio"] = args.aspect_ratio
    if args.language:
        doc_input["Language"] = args.language
    if args.reference_duration:
        doc_input["ReferenceDuration"] = args.reference_duration
    if args.enable_tts:
        doc_input["EnableTTS"] = True
        if args.voice_id:
            doc_input["VoiceId"] = args.voice_id

    params = {"Input": doc_input}

    cos_param = build_store_cos_param(args)
    if cos_param:
        params["CosInfo"] = cos_param

    return params, file_urls


# =============================================================================
# API 调用
# =============================================================================

def create_doc_to_video_task(client, params):
    """调用 CreateDocToVideoTask API 创建任务。"""
    req = models.CreateDocToVideoTaskRequest()
    req.from_json_string(json.dumps(params))
    resp = client.CreateDocToVideoTask(req)
    return json.loads(resp.to_json_string())


def describe_aigc_task_status(client, task_id):
    """
    调用 DescribeAigcTaskStatus 查询文档生视频任务状态。

    响应结构（tencentcloud-sdk-python >= 3.1.139 已正式建模，见 requirements.txt）：
        {TaskId, TaskType, TaskStatus, OutputUrl, CreateTime, ScheduledTime,
         FinishedTime, TaskResultCode, TaskResultMsg, RequestBody, RequestId}
    其中 TaskStatus 已确认真实枚举值包含 PENDING（等待中）/ PROCESSING（执行中）/
    FINISHED（已完成）/ FAILED（失败），已通过真实任务全链路验证。
    OutputUrl 为单个字符串（非数组），失败或未完成时可能为 null。
    """
    req = models.DescribeAigcTaskStatusRequest()
    req.TaskId = task_id
    resp = client.DescribeAigcTaskStatus(req)
    return json.loads(resp.to_json_string())


def _extract_doc_to_video_result(result):
    """从 DescribeAigcTaskStatus 原始响应中提取文档生视频任务的状态与结果。"""
    status = result.get("TaskStatus", "")
    output_url = result.get("OutputUrl")
    return {
        "status": status or "UNKNOWN",
        "video_urls": [output_url] if output_url else [],
        "message": result.get("TaskResultMsg", ""),
        "raw": result,
    }


STATUS_MAP = {
    "PENDING": "等待中", "WAITING": "等待中",
    "PROCESSING": "执行中", "RUNNING": "执行中",
    "FINISHED": "已完成", "FAILED": "失败",
}


def poll_task_result(client, task_id, poll_interval, max_wait, verbose=False):
    """轮询等待任务完成。"""
    elapsed = 0
    while elapsed < max_wait:
        try:
            result = describe_aigc_task_status(client, task_id)
        except TencentCloudSDKException as e:
            print(f"\n⚠️  查询失败: {e}，{poll_interval}s 后重试...", file=sys.stderr)
            time.sleep(poll_interval)
            elapsed += poll_interval
            continue

        parsed = _extract_doc_to_video_result(result)
        status = parsed["status"]
        status_text = STATUS_MAP.get(status, status)

        if status == "FINISHED":
            return parsed
        if status == "FAILED":
            print(f"\n❌ 任务失败: {parsed.get('message', '未知错误')}", file=sys.stderr)
            if verbose:
                print(json.dumps(parsed["raw"], ensure_ascii=False, indent=2))
            sys.exit(1)

        print(f"\r⏳ 任务状态: {status_text}（已等待 {elapsed}s / 最长 {max_wait}s）", end="", flush=True)
        time.sleep(poll_interval)
        elapsed += poll_interval

    print(f"\n⚠️  等待超时（已等待 {max_wait}s），任务仍在进行中。", file=sys.stderr)
    print(f"   请稍后使用 --task-id {task_id} 查询结果。", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# 参数校验
# =============================================================================

def validate_args(args, parser):
    if args.task_id:
        create_only_params = [
            (args.url, "--url"),
            (getattr(args, "local_file", None), "--local-file"),
            (args.prompt, "--prompt"),
            (args.aspect_ratio, "--aspect-ratio"),
            (args.language, "--language"),
            (args.reference_duration, "--reference-duration"),
            (args.enable_tts, "--enable-tts"),
            (args.no_wait, "--no-wait"),
        ]
        used = [name for val, name in create_only_params if val]
        if used:
            parser.error(f"--task-id 用于查询已有任务，不能与创建任务参数 {', '.join(used)} 同时使用")
        return

    file_count = (len(args.url) if args.url else 0) + \
                 (len(getattr(args, "local_file", None) or []))
    if file_count == 0:
        parser.error("请至少指定一个文档来源：--url 或 --local-file")
    if file_count > MAX_FILES:
        parser.error(f"文档数量最多 {MAX_FILES} 个，当前指定 {file_count} 个")

    if not args.prompt:
        parser.error("请指定 --prompt（生成视频的描述文本，最多2000字符）")
    if len(args.prompt) > 2000:
        parser.error(f"--prompt 超过2000字符限制（当前 {len(args.prompt)} 字符）")

    if getattr(args, "local_file", None):
        for p in args.local_file:
            if not os.path.isfile(p):
                parser.error(f"--local-file 文件不存在: {p}")
            ext = os.path.splitext(p)[1].lower()
            if ext not in SUPPORTED_DOC_EXTS:
                parser.error(f"--local-file 不支持的文档格式 {ext}，支持：pdf/pptx/docx/png/jpg")

    if args.aspect_ratio and args.aspect_ratio not in SUPPORTED_RATIOS:
        parser.error(f"不支持的宽高比: {args.aspect_ratio}，支持: {', '.join(SUPPORTED_RATIOS)}")

    if args.language and args.language not in SUPPORTED_LANGUAGES:
        parser.error(
            f"不支持的语言: {args.language}，支持: {', '.join(SUPPORTED_LANGUAGES.keys())}"
        )

    if args.reference_duration is not None:
        if not (15 <= args.reference_duration <= 1200):
            parser.error(f"--reference-duration 取值范围为 [15, 1200] 秒，当前: {args.reference_duration}")

    if args.enable_tts and not args.voice_id:
        parser.error("开启 --enable-tts 时建议指定 --voice-id 音色 ID（否则使用平台默认音色）")


# =============================================================================
# 主流程
# =============================================================================

def run(args):
    region = args.region or os.environ.get("TENCENTCLOUD_API_REGION", "ap-guangzhou")
    cred = get_credentials()
    client = create_mps_client(cred, region)

    # 模式1：查询已有任务
    if args.task_id:
        if args.dry_run:
            print("=" * 60)
            print("【Dry Run 模式】仅打印请求参数，不实际调用 API")
            print("=" * 60)
            print(json.dumps({"Action": "DescribeAigcTaskStatus", "TaskId": args.task_id}, ensure_ascii=False, indent=2))
            return

        print("=" * 60)
        print("腾讯云 MPS AIGC 文档生视频 — 查询任务")
        print("=" * 60)
        print(f"TaskId: {args.task_id}")
        print("-" * 60)

        try:
            result = describe_aigc_task_status(client, args.task_id)
            parsed = _extract_doc_to_video_result(result)
            status = parsed["status"]
            status_text = STATUS_MAP.get(status, status)
            print(f"任务状态: {status_text}")

            if status == "FINISHED":
                video_urls = parsed["video_urls"]
                print(f"生成视频数量: {len(video_urls)}")
                statuses = []
                for i, url in enumerate(video_urls, 1):
                    final_url, st = ensure_signed_url(url)
                    print(f"  视频 {i}: {final_url}")
                    statuses.append(st)
                print_storage_hint(statuses)
            elif status == "FAILED":
                print(f"失败原因: {parsed.get('message', '未知')}")
            elif status == "UNKNOWN":
                print(f"⚠️  {parsed.get('message', '')}")

            if args.verbose:
                print("\n完整响应：")
                print(json.dumps(result, ensure_ascii=False, indent=2))

        except TencentCloudSDKException as e:
            print(f"❌ 查询失败: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # 模式2：创建任务
    params, file_urls = build_create_params(args)

    if args.dry_run:
        print("=" * 60)
        print("【Dry Run 模式】仅打印请求参数，不实际调用 API")
        print("=" * 60)
        print(json.dumps(params, ensure_ascii=False, indent=2))
        return

    print("=" * 60)
    print("腾讯云 MPS AIGC 文档生成视频")
    print("=" * 60)
    print(f"模型: {args.model_name} v{args.model_version}")
    print(f"文档数量: {len(file_urls)}")
    for i, url in enumerate(file_urls, 1):
        print(f"  文档 {i}: {url}")
    prompt_display = args.prompt[:80] + "..." if len(args.prompt) > 80 else args.prompt
    print(f"Prompt: {prompt_display}")
    if args.aspect_ratio:
        print(f"宽高比: {args.aspect_ratio}")
    if args.language:
        print(f"语言: {SUPPORTED_LANGUAGES.get(args.language, args.language)}")
    if args.reference_duration:
        print(f"参考时长: {args.reference_duration}s")
    if args.enable_tts:
        print(f"AI配音: 开启{f'（音色: {args.voice_id}）' if args.voice_id else ''}")
    print("-" * 60)

    if args.verbose:
        print("请求参数：")
        print(json.dumps(params, ensure_ascii=False, indent=2))
        print()

    try:
        result = create_doc_to_video_task(client, params)
        task_id = result.get("TaskId", "N/A")
        request_id = result.get("RequestId", "N/A")

        print("✅ 文档生视频任务提交成功！")
        print(f"   TaskId: {task_id}")
        print(f"   RequestId: {request_id}")
        print(f"\n## TaskId: {task_id}")

        if args.no_wait:
            print("\n提示：使用以下命令查询任务结果：")
            print(f"  python3 scripts/mps_doc_to_video.py --task-id {task_id}")
            return result

        print(f"\n正在等待任务完成（轮询间隔 {args.poll_interval}s，最长等待 {args.max_wait}s）...")
        poll_result = poll_task_result(client, task_id, args.poll_interval, args.max_wait, args.verbose)

        video_urls = poll_result["video_urls"]
        print(f"\n✅ 任务完成！生成视频数量: {len(video_urls)}")
        statuses = []
        for i, url in enumerate(video_urls, 1):
            final_url, st = ensure_signed_url(url)
            print(f"  视频 {i}: {final_url}")
            statuses.append(st)
        print_storage_hint(statuses)

        # 自动下载生成视频
        download_dir = getattr(args, "download_dir", None)
        if download_dir and video_urls:
            import urllib.request
            os.makedirs(download_dir, exist_ok=True)
            print(f"\n📥 自动下载生成视频到: {os.path.abspath(download_dir)}")
            for i, url in enumerate(video_urls, 1):
                local_path = os.path.join(download_dir, f"doc_to_video_{i}.mp4")
                try:
                    urllib.request.urlretrieve(url, local_path)
                    size = os.path.getsize(local_path)
                    print(f"   [{i}] ✅ {local_path} ({size / 1024 / 1024:.2f} MB)")
                except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
                    print(f"   [{i}] ❌ 下载失败: {e}")

        if args.verbose:
            print("\n完整响应：")
            print(json.dumps(poll_result["raw"], ensure_ascii=False, indent=2))

        return poll_result

    except TencentCloudSDKException as e:
        print(f"❌ 请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    # 时序修复：先加载 .env，让 argparse default=os.environ.get(...) 能读到用户配置
    if _LOAD_ENV_AVAILABLE:
        try:
            _ensure_env_loaded(verbose=False)
        except Exception:  # NOCA:broad-except(env loading must not crash the script)
            pass

    parser = argparse.ArgumentParser(
        description="腾讯云 MPS AIGC 文档生成视频 —— 将 PDF/PPTX/DOCX/图片文档自动生成讲解视频",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 单文档 + prompt
  python3 mps_doc_to_video.py --url https://example.com/sample.pdf \\
      --prompt "根据文档内容，帮我生成一个教学视频"

  # 多文档输入（最多3个）
  python3 mps_doc_to_video.py \\
      --url https://example.com/a.pdf --url https://example.com/b.pptx \\
      --prompt "整合成一个产品介绍视频"

  # 指定宽高比 + 语言
  python3 mps_doc_to_video.py --url https://example.com/sample.docx \\
      --prompt "生成产品介绍视频" --aspect-ratio 9:16 --language en

  # 开启 AI 配音
  python3 mps_doc_to_video.py --url https://example.com/sample.pdf \\
      --prompt "生成教学视频" --enable-tts --voice-id v1_xxxxxx

  # 本地文档（自动上传 COS）
  python3 mps_doc_to_video.py --local-file /path/to/sample.pdf --prompt "生成教学视频"

  # 查询任务结果
  python3 mps_doc_to_video.py --task-id e084efaa-d25a-xxxx-xxxx-6b85e473c0e5

  # Dry Run
  python3 mps_doc_to_video.py --url https://example.com/sample.pdf --prompt "测试" --dry-run

支持的文档格式：pdf / pptx / docx / png / jpg（最多3个，单个不超过10MB，最多100页）
支持的宽高比：16:9（默认）/ 9:16 / 1:1
支持的语言：zh（默认）/ en / ja / ko / ru / fr / es / de

环境变量：
  TENCENTCLOUD_SECRET_ID   腾讯云 SecretId
  TENCENTCLOUD_SECRET_KEY  腾讯云 SecretKey
  TENCENTCLOUD_COS_BUCKET  COS Bucket 名称（可选，用于结果存储/本地文件上传）
  TENCENTCLOUD_COS_REGION  COS Bucket 区域（默认 ap-guangzhou）
        """
    )

    # ---- 任务查询 ----
    query_group = parser.add_argument_group("任务查询（查询已有任务，与创建任务互斥）")
    query_group.add_argument("--task-id", type=str, help="查询已有任务的 TaskId")

    # ---- 文档输入 ----
    doc_group = parser.add_argument_group("文档输入（至少指定一种，最多3个文档）")
    doc_group.add_argument("--url", type=str, action="append",
                            help="文档 URL（可多次指定，最多3个）。支持 pdf/pptx/docx/png/jpg，单个不超过10MB")
    doc_group.add_argument("--local-file", type=str, action="append", metavar="FILE",
                            help="本地文档路径（可多次指定）。脚本自动上传到 COS 后生成预签名 URL 传入 API。"
                                 "需配置 TENCENTCLOUD_COS_BUCKET 或 --output-bucket")

    # ---- 生成内容 ----
    content_group = parser.add_argument_group("生成内容")
    content_group.add_argument("--prompt", type=str, help="生成视频的 prompt 描述（最多2000字符，必填）")
    content_group.add_argument("--model-name", type=str, default=DEFAULT_MODEL_NAME,
                                help=f"文档生成视频模型名称（默认 {DEFAULT_MODEL_NAME}）")
    content_group.add_argument("--model-version", type=str, default=DEFAULT_MODEL_VERSION,
                                help=f"模型版本号（默认 {DEFAULT_MODEL_VERSION}）")

    # ---- 输出配置 ----
    output_group = parser.add_argument_group("输出配置")
    output_group.add_argument("--aspect-ratio", type=str, choices=SUPPORTED_RATIOS,
                               help="生成视频的宽高比：16:9（默认）/ 9:16 / 1:1")
    output_group.add_argument("--language", type=str, choices=list(SUPPORTED_LANGUAGES.keys()),
                               help="生成视频的语言，默认 zh（中文）")
    output_group.add_argument("--reference-duration", type=int,
                               help="生成视频的时长参考（秒），取值范围 [15, 1200]，仅供大模型参考，非精确时长")
    output_group.add_argument("--enable-tts", action="store_true",
                               help="开启 AI 配音功能")
    output_group.add_argument("--voice-id", type=str,
                               help="AI 配音音色 ID（仅 --enable-tts 时生效）")

    # ---- COS 存储 ----
    cos_group = parser.add_argument_group(
        "COS 存储配置（可选；不配置则使用 MPS 临时存储；配置后写回您的桶永久保存，自动生成24小时临时签名链接）"
    )
    cos_group.add_argument("--output-bucket", type=str,
                            help="COS Bucket 名称（默认取 TENCENTCLOUD_COS_BUCKET 环境变量）")
    cos_group.add_argument("--output-region", type=str,
                            help="COS Bucket 区域（默认取 TENCENTCLOUD_COS_REGION 环境变量，默认 ap-guangzhou）")
    cos_group.add_argument("--output-dir", type=str, default="/output/doc-to-video/",
                            help="COS 存储桶中的输出目录路径（默认: /output/doc-to-video/）")

    # ---- 执行控制 ----
    control_group = parser.add_argument_group("执行控制")
    control_group.add_argument("--no-wait", action="store_true", help="仅创建任务，不等待结果。稍后用 --task-id 查询")
    control_group.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL,
                                help=f"轮询间隔（秒），默认 {DEFAULT_POLL_INTERVAL}")
    control_group.add_argument("--max-wait", type=int, default=DEFAULT_MAX_WAIT,
                                help=f"最长等待时间（秒），默认 {DEFAULT_MAX_WAIT}")

    # ---- 其他 ----
    other_group = parser.add_argument_group("其他配置")
    other_group.add_argument("--region", type=str, help="MPS 服务区域（默认 ap-guangzhou）")
    other_group.add_argument("--verbose", "-v", action="store_true", help="输出详细信息")
    other_group.add_argument("--dry-run", action="store_true", help="仅打印请求参数，不实际调用 API")
    other_group.add_argument("--download-dir", type=str, default=None,
                              help="任务完成后自动下载生成视频到指定目录（默认：不下载；指定路径后自动下载）")

    args = parser.parse_args()

    validate_args(args, parser)
    run(args)


if __name__ == "__main__":
    main()
