#!/usr/bin/env python3
"""
DashScope API 封装层（通过自有平台 SkillController 代理）
==========================================================
所有 DashScope 相关功能均通过自有平台接口（platform.delilegal.com）间接调用，
不再直连阿里百炼 dashscope.aliyuncs.com。

自有平台鉴权: Authorization: Bearer {platform_api_key}
platform_api_key 来源: voice_config.json['api_key']

接口清单:
  1. create_portrait_video           — 口播视频生成（wan2.7-i2v，支持 480P/720P）
  2. query_video_task               — 查询口播视频任务状态
  3. enroll_custom_voice            — 声音复刻（create_voice）
  4. generate_image                 — 文生图（wan2.7-image）
  5. synthesize_cloned_voice        — 复刻声音 TTS 合成
  6. upload_file_via_platform        — 三步上传到 OSS（prepareUploadFile → PUT OSS → saveFile）
"""

import json
import math
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ═══════════════════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════════════════

# 自有平台服务域名
PLATFORM_BASE = "https://platform.delilegal.com"

# Skill 标识（固定值）
SKILL_ID = "video-creator"
SKILL_VERSION = "1.0.2"

# Session ID：每次 Python 进程启动时生成一次，同一次调用内所有请求复用同一个 ID
_SESSION_ID: str = str(uuid.uuid4())

# 平台 SkillController 端点（代理所有 DashScope 调用）
ENDPOINT_PORTRAIT_VIDEO = f"{PLATFORM_BASE}/api/v1/skill/video/create"
"""口播视频生成（wan2.7-i2v，支持 480P/720P）"""

ENDPOINT_VIDEO_TASK = f"{PLATFORM_BASE}/api/v1/skill/video/task/{{task_id}}"
"""查询口播视频任务状态（GET）"""

ENDPOINT_VOICE_ENROLL = f"{PLATFORM_BASE}/api/v1/skill/voice/enroll"
"""声音复刻"""

ENDPOINT_IMAGE_GENERATION = f"{PLATFORM_BASE}/api/v1/skill/image/generate"
"""文生图（wan2.7-image）"""

ENDPOINT_TTS_SYNTHESIS = f"{PLATFORM_BASE}/api/v1/skill/voice/synthesize"
"""复刻声音 TTS 合成"""

# 文件上传端点（平台 OSS 三步走）
ENDPOINT_PREPARE_UPLOAD = f"{PLATFORM_BASE}/api/v1/file/prepareUploadFile"
"""获取上传临时链接（步骤一）"""
ENDPOINT_SAVE_FILE = f"{PLATFORM_BASE}/api/v1/file/saveFile"
"""保存文件记录（步骤三）"""

# VOICE_CONFIG 路径
VOICE_CONFIG_PATH = Path(__file__).parent.parent / "voice_config.json"
"""voice_config.json 路径，用于读取 platform_api_key"""

# 轮询配置
POLL_INTERVAL_SEC = 5    # 轮询间隔（秒）
POLL_TIMEOUT_SEC = 300   # 最长等待（秒）
PORTRAIT_MAX_DURATION = 15.0  # 口播视频最大音频时长

# 默认 Prompt
DEFAULT_PORTRAIT_PROMPT = (
    "人像保持 超写实，皮肤纹理清晰但平滑，零毛孔，肤色均匀，白皙透亮，"
    "无痘印雀斑，电影级布光，景深效果，8K分辨率，专业美容修图质感"
)


# ═══════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════

def _get_httpx():
    """延迟导入 httpx，若未安装则自动安装。"""
    import sys
    import subprocess
    try:
        import httpx  # noqa: F811
        return httpx
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "httpx", "certifi", "-q"],
            check=True,
        )
        import httpx
        return httpx


def _get_platform_api_key() -> str:
    """
    从 voice_config.json 读取自有平台 API Key。
    键路径：voice_config['api_key']

    所有调用自有平台服务（platform.delilegal.com）时，
    均需在 Header 中携带：Authorization: Bearer {api_key}
    """
    if VOICE_CONFIG_PATH.exists():
        with open(VOICE_CONFIG_PATH, encoding="utf-8") as f:
            cfg = json.load(f)
    else:
        cfg = {}
    return cfg.get("api_key", "").strip()


def _build_platform_headers(platform_api_key: Optional[str] = None) -> Dict[str, str]:
    """构建平台请求头（Authorization: Bearer + Content-Type + skill-id + skill-version + session-id）。"""
    key = platform_api_key or _get_platform_api_key()
    if not key:
        raise RuntimeError(
            "未找到平台 API Key，请在 voice_config.json 中设置 api_key"
        )
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "skill-id": SKILL_ID,
        "skill-version": SKILL_VERSION,
        "session-id": _SESSION_ID,
    }


def _unwrap_api_result(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    解包平台 WebApiResult 统一响应格式：
      { "success": bool, "code": int, "msg": str, "body": { ... } }
    返回 body 内容；失败则抛出异常（附带详细错误信息）。

    SkillController 的所有接口均返回 WebApiResult<T> 格式，
    T 的具体类型对应各接口的响应体（如 CreateVideoResp 等）。
    """
    if not data.get("success", False):
        # 尽可能提取详细错误信息
        code = data.get('code', 'N/A')
        msg = data.get('msg', '未知错误')
        body = data.get('body', {})
        # 有些接口会在 body 里放更详细的错误原因
        if isinstance(body, dict):
            reason = body.get('reason', body.get('error', ''))
            if reason:
                msg = f"{msg}（原因：{reason}）"
        raise RuntimeError(
            f"平台接口返回失败 (code={code}): {msg} | 完整响应: {data}"
        )
    return data.get("body", {})


# ═══════════════════════════════════════════════════════════
# 1. 口播视频生成（wan2.7-i2v，支持 480P/720P）
# ═══════════════════════════════════════════════════════════

def create_portrait_video(
    image_url: str,
    audio_url: str,
    prompt: str = DEFAULT_PORTRAIT_PROMPT,
    duration: int = 5,
    resolution: str = "720P",
    prompt_extend: bool = True,
    watermark: bool = False,
    platform_api_key: Optional[str] = None,
) -> str:
    """
    提交口播视频生成任务（异步），通过自有平台 SkillController 代理。

    接口: POST /api/v1/skill/video/create
    域名: platform.delilegal.com
    鉴权: Authorization: Bearer {platform_api_key}

    参数:
        image_url:       真人照片的 HTTPS URL
        audio_url:       TTS 音频的 HTTPS URL
        prompt:          口播画面 prompt（控制生成画面质感）
        duration:        视频时长（秒），范围 2-15，默认 5
        resolution:      分辨率，默认 "720P"，可选 "480P"
        prompt_extend:   是否开启 prompt 智能扩写，默认 True
        watermark:       是否添加水印，默认 False
        platform_api_key: 平台鉴权 key（可选，不传则从 voice_config.json 自动读取）

    返回:
        task_id: 异步任务 ID（对应 CreateVideoResp.taskId）

    异常:
        HTTPStatusError: 请求失败
        RuntimeError:    平台返回失败或缺少 taskId
    """
    httpx = _get_httpx()
    import os as _os, certifi
    _os.environ.setdefault("SSL_CERT_FILE", certifi.where())

    # duration 限制 2-15
    safe_duration = max(2, min(15, duration))

    payload: Dict[str, Any] = {
        "imageUrl": image_url,
        "audioUrl": audio_url,
        "prompt": prompt,
        "duration": safe_duration,
        "resolution": resolution,
        "promptExtend": prompt_extend,
        "watermark": watermark,
    }

    resp = httpx.post(
        ENDPOINT_PORTRAIT_VIDEO,
        headers=_build_platform_headers(platform_api_key),
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    body = _unwrap_api_result(resp.json())
    task_id = body.get("taskId", "")
    if not task_id:
        raise RuntimeError(f"创建视频任务成功但未获取到 taskId：{body}")
    return task_id


# ═══════════════════════════════════════════════════════════
# 2. 查询口播视频任务状态
# ═══════════════════════════════════════════════════════════

def query_video_task(
    task_id: str,
    platform_api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    查询口播视频异步任务状态，通过自有平台 SkillController 代理。

    接口: GET /api/v1/skill/video/task/{taskId}
    域名: platform.delilegal.com

    参数:
        task_id:         由 create_portrait_video 返回的任务 ID
        platform_api_key: 平台鉴权 key（可选，不传则从 voice_config.json 自动读取）

    返回:
        { "task_status": "PENDING"|"RUNNING"|"SUCCEEDED"|"FAILED"|..., "video_url": str|None }
        对应 VideoTaskResp: { taskStatus, videoUrl }

    异常:
        HTTPStatusError: 请求失败
    """
    httpx = _get_httpx()
    import os as _os, certifi
    _os.environ.setdefault("SSL_CERT_FILE", certifi.where())

    url = ENDPOINT_VIDEO_TASK.format(task_id=task_id)
    resp = httpx.get(
        url,
        headers=_build_platform_headers(platform_api_key),
        timeout=30,
    )
    resp.raise_for_status()
    body = _unwrap_api_result(resp.json())

    return {
        "task_status": body.get("taskStatus", ""),
        "video_url": body.get("videoUrl", ""),
    }


# ═══════════════════════════════════════════════════════════
# 3. 声音复刻（create_voice）
# ═══════════════════════════════════════════════════════════

def enroll_custom_voice(
    audio_url: str,
    prefix: str = "myvoice",
    language: str = "zh",
    target_model: str = "cosyvoice-v3.5-plus",
    platform_api_key: Optional[str] = None,
) -> str:
    """
    声音复刻，通过自有平台 SkillController 代理。

    接口: POST /api/v1/skill/voice/enroll
    域名: platform.delilegal.com

    参数:
        audio_url:       公网可访问的音频 URL（http/https）
        prefix:          声音前缀标识，默认 "myvoice"
        language:        语言提示，如 "zh", "en"，默认 "zh"
        target_model:    目标 TTS 模型，默认 "cosyvoice-v3.5-plus"
        platform_api_key: 平台鉴权 key（可选，不传则自动读取）

    返回:
        voice_id: 创建成功后的声音 ID（对应 EnrollVoiceResp.voiceId）

    异常:
        HTTPStatusError: 请求失败
        RuntimeError:    返回中无法解析 voiceId
    """
    httpx = _get_httpx()
    import os as _os, certifi
    _os.environ.setdefault("SSL_CERT_FILE", certifi.where())

    payload = {
        "audioUrl": audio_url,
        "prefix": prefix,
        "language": language,
        "targetModel": target_model,
    }

    resp = httpx.post(
        ENDPOINT_VOICE_ENROLL,
        headers=_build_platform_headers(platform_api_key),
        json=payload,
        timeout=120,
    )
    resp.raise_for_status()
    body = _unwrap_api_result(resp.json())
    voice_id = body.get("voiceId", "")
    if not voice_id:
        raise RuntimeError(f"声音复刻成功但未获取到 voiceId：{body}")
    return voice_id


# ═══════════════════════════════════════════════════════════
# 4. 文生图（wan2.7-image）
# ═══════════════════════════════════════════════════════════

def generate_image(
    prompt: str,
    size: str = "1920*1080",
    negative_prompt: str = "",
    seed: Optional[int] = None,
    watermark: bool = False,
    platform_api_key: Optional[str] = None,
) -> str:
    """
    文生图，通过自有平台 SkillController 代理。

    接口: POST /api/v1/skill/image/generate
    域名: platform.delilegal.com

    参数:
        prompt:          图片生成提示词（描述画面内容）
        size:            图片尺寸，格式 "宽*高"，默认 "1920*1080"
        negative_prompt: 反向提示词（不希望出现的元素），可选
        seed:            随机种子（不传则服务端随机），可选
        watermark:       是否添加水印，默认 False
        platform_api_key: 平台鉴权 key（可选，不传则自动读取）

    返回:
        image_url: 图片访问 URL（对应 GenerateImageResp.imageUrl）

    异常:
        HTTPStatusError: API 请求失败
        RuntimeError:    返回中缺少 imageUrl
    """
    httpx = _get_httpx()
    import os as _os, certifi
    _os.environ.setdefault("SSL_CERT_FILE", certifi.where())

    payload: Dict[str, Any] = {
        "prompt": prompt,
        "size": size,
        "negativePrompt": negative_prompt,
        "watermark": watermark,
    }
    if seed is not None:
        payload["seed"] = seed

    resp = httpx.post(
        ENDPOINT_IMAGE_GENERATION,
        headers=_build_platform_headers(platform_api_key),
        json=payload,
        timeout=120,
    )
    resp.raise_for_status()
    body = _unwrap_api_result(resp.json())
    image_url = body.get("imageUrl", "")
    if not image_url:
        raise RuntimeError(f"文生图成功但未获取到 imageUrl：{body}")
    return image_url


# ═══════════════════════════════════════════════════════════
# 5. 复刻声音 TTS 合成
# ═══════════════════════════════════════════════════════════

def synthesize_cloned_voice(
    text: str,
    voice_id: str,
    target_model: str = "cosyvoice-v3.5-plus",
    platform_api_key: Optional[str] = None,
    poll_interval: int = 5,
    poll_timeout: int = 120,
) -> str:
    """
    使用已复刻的声音进行 TTS 合成，通过自有平台 SkillController 代理。

    接口: POST /api/v1/skill/voice/synthesize
    域名: platform.delilegal.com

    注意：该接口为异步任务模式。
      - 成功时返回 { "taskId": "..." }，需要轮询获取结果
      - 轮询端点: GET /api/v1/skill/voice/task/{taskId}
      - 轮询成功: { "taskStatus": "SUCCEEDED", "audioUrl": "..." }
      - 若返回 audioUrl 为空或超时，抛出异常

    参数:
      text:            待合成的文本内容
      voice_id:        已复刻的声音 ID（由 enroll_custom_voice 返回）
      target_model:    TTS 模型名，默认 "cosyvoice-v3.5-plus"
      platform_api_key: 平台鉴权 key（可选，不传则自动读取）
      poll_interval:   轮询间隔秒数，默认 5
      poll_timeout:    最长轮询等待秒数，默认 120

    返回:
      audio_url: 合成音频的访问 URL

    异常:
      HTTPStatusError: API 请求失败
      RuntimeError:    返回中缺少 taskId/audioUrl 或轮询超时/失败
    """
    httpx = _get_httpx()
    import os as _os, certifi, time
    _os.environ.setdefault("SSL_CERT_FILE", certifi.where())

    # TTS 合成提交（异步）
    payload = {
        "text": text,
        "voiceId": voice_id,
        "targetModel": target_model,
    }

    resp = httpx.post(
        ENDPOINT_TTS_SYNTHESIS,
        headers=_build_platform_headers(platform_api_key),
        json=payload,
        timeout=120,
    )
    resp.raise_for_status()
    body = _unwrap_api_result(resp.json())

    # 优先从 body 中提取 taskId（异步模式）
    task_id = body.get("taskId", "")
    # 兼容：若 body 直接包含 audioUrl（同步模式），直接返回
    direct_audio_url = body.get("audioUrl", "")

    if direct_audio_url:
        return direct_audio_url

    if not task_id:
        raise RuntimeError(f"TTS 合成接口未返回 taskId 也没有 audioUrl：{body}")

    # ── 异步轮询获取结果 ──
    task_endpoint = f"{PLATFORM_BASE}/api/v1/skill/voice/task/{{task_id}}"
    waited = 0
    while waited < poll_timeout:
        time.sleep(poll_interval)
        waited += poll_interval

        poll_url = task_endpoint.format(task_id=task_id)
        poll_resp = httpx.get(
            poll_url,
            headers=_build_platform_headers(platform_api_key),
            timeout=30,
        )
        poll_resp.raise_for_status()
        poll_data = poll_resp.json()

        if not poll_data.get("success", False):
            # 非成功格式，可能是网关错误，继续等待
            continue

        poll_body = poll_data.get("body", {})
        status = poll_body.get("taskStatus", "")

        if status == "SUCCEEDED":
            audio_url = poll_body.get("audioUrl", "")
            if not audio_url:
                raise RuntimeError(f"TTS 任务成功但未获取到 audioUrl：{poll_body}")
            return audio_url
        elif status in ("FAILED", "CANCELLED", "UNKNOWN"):
            raise RuntimeError(f"TTS 任务失败，状态: {status}，详情: {poll_body}")

    raise TimeoutError(f"TTS 合成任务轮询超时（已等待 {poll_timeout}s）")


# ═══════════════════════════════════════════════════════════
# 6. 上传文件到 OSS（通过自有平台，三步走）
# ═══════════════════════════════════════════════════════════

def _calc_md5(file_path: str) -> str:
    """计算文件 MD5（十六进制小写）。"""
    import hashlib
    h = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def upload_file_via_platform(
    file_path: str,
    platform_api_key: str,
    prepare_url: str = ENDPOINT_PREPARE_UPLOAD,
    save_url: str = ENDPOINT_SAVE_FILE,
) -> str:
    """
    三步走方式上传文件到 OSS，通过自有平台接口完成。
    完成后返回平台返回的 fileUrl（带签名的 HTTPS 下载地址）。

    流程：
      步骤一：POST {prepare_url}  → 获取 OSS 上传临时链接（uploadUrl）和请求头
      步骤二：PUT  {uploadUrl}    → 直接上传文件二进制数据到 OSS
      步骤三：POST {save_url}     → 通知平台保存文件记录，获取 fileUrl

    平台接口域名: https://platform.delilegal.com
    鉴权方式: Authorization: Bearer {platform_api_key}

    参数:
        file_path:        本地文件路径
        platform_api_key: 自有平台的 API Key（Bearer Token）
                          来源：voice_config.json['api_key']
                          Header: Authorization: Bearer {platform_api_key}
        prepare_url:      步骤一接口，默认 ENDPOINT_PREPARE_UPLOAD
        save_url:         步骤三接口，默认 ENDPOINT_SAVE_FILE

    返回:
        fileUrl: 平台返回的带签名 HTTPS 文件访问地址

    步骤一请求体:
        { "fileHash": "<md5>", "fileName": "<filename>" }

    步骤一响应体示例:
        {
            "success": true, "code": 0,
            "body": {
                "uploadUrl": "https://...",
                "headers": { "x-oss-meta-author": "...", "Content-Type": "application/octet-stream" },
                "method": "PUT",
                "exist": false
            }
        }

    步骤三请求体:
        { "fileHash": "<md5>", "originalName": "<filename>" }

    步骤三响应体示例:
        {
            "success": true, "code": 0,
            "body": {
                "fileId": "...",
                "fileUrl": "https://...",
                ...
            }
        }

    异常:
        FileNotFoundError: 本地文件不存在
        RuntimeError:      任意步骤失败
    """
    httpx = _get_httpx()
    import os, certifi
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())

    source = Path(file_path)
    if not source.exists() or not source.is_file():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    file_name = source.name
    file_hash = _calc_md5(file_path)

    platform_headers = {
        "Authorization": f"Bearer {platform_api_key}",
        "Content-Type": "application/json",
    }

    # ── 步骤一：获取临时上传链接 ──────────────────────────────
    prepare_payload = {"fileHash": file_hash, "fileName": file_name}
    resp1 = httpx.post(prepare_url, headers=platform_headers, json=prepare_payload, timeout=30)
    resp1.raise_for_status()
    result1 = resp1.json()

    if not result1.get("success"):
        raise RuntimeError(
            f"[步骤一] prepareUploadFile 失败: {result1.get('msg', result1)}"
        )

    body1 = result1.get("body", {})
    upload_url = body1.get("uploadUrl", "")
    oss_headers_raw: Dict[str, str] = body1.get("headers", {})
    already_exists: bool = body1.get("exist", False)

    if not upload_url:
        raise RuntimeError(f"[步骤一] 响应中缺少 uploadUrl: {result1}")

    # ── 步骤二：上传文件到 OSS（PUT 请求，binary body）────────
    if not already_exists:
        # 构建 OSS 请求头：使用平台返回的 headers，并确保 Content-Type 正确
        oss_req_headers: Dict[str, str] = {}
        oss_req_headers.update(oss_headers_raw)
        if "Content-Type" not in oss_req_headers:
            oss_req_headers["Content-Type"] = "application/octet-stream"

        with open(file_path, "rb") as f:
            file_data = f.read()

        resp2 = httpx.put(
            upload_url,
            headers=oss_req_headers,
            content=file_data,
            timeout=180,
        )
        if resp2.status_code not in (200, 204):
            raise RuntimeError(
                f"[步骤二] 上传到 OSS 失败（HTTP {resp2.status_code}）: {resp2.text[:200]}"
            )

    # ── 步骤三：保存文件记录 ──────────────────────────────────
    save_payload = {"fileHash": file_hash, "originalName": file_name}
    resp3 = httpx.post(save_url, headers=platform_headers, json=save_payload, timeout=30)
    resp3.raise_for_status()
    result3 = resp3.json()

    if not result3.get("success"):
        raise RuntimeError(
            f"[步骤三] saveFile 失败: {result3.get('msg', result3)}"
        )

    body3 = result3.get("body", {})
    file_url = body3.get("fileUrl", "")
    if not file_url:
        raise RuntimeError(f"[步骤三] 响应中缺少 fileUrl: {result3}")

    return file_url


# 向后兼容别名
def upload_to_oss_via_service(
    service_url: str,
    file_path: str,
    api_key: str,
    additional_params: Optional[Dict[str, str]] = None,
) -> str:
    """
    已废弃，请使用 upload_file_via_platform。
    此函数保留仅用于向后兼容，实际调用会转发到新实现。
    """
    return upload_file_via_platform(
        file_path=file_path,
        platform_api_key=api_key,
    )


# ═══════════════════════════════════════════════════════════
# 8. 下载视频 / 图片（直接返回，无需单独封装为接口调用）
# ═══════════════════════════════════════════════════════════

def download_file(url: str, output_path: Optional[str] = None) -> bytes:
    """
    从 URL 下载文件（视频或图片），响应中直接返回的 URL 就是可直接下载的。
    这是一个纯工具函数，对应的是对阿里云 OSS/CDN 的 GET 请求。

    参数:
        url:         文件下载 URL
        output_path: 保存到本地文件的路径（可选，不传则只返回二进制数据）

    返回:
        bytes: 文件二进制数据
    """
    httpx = _get_httpx()
    import os, certifi
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())

    resp = httpx.get(url, timeout=180, follow_redirects=True)
    resp.raise_for_status()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(resp.content)

    return resp.content


# ═══════════════════════════════════════════════════════════
# 便捷组合函数
# ═══════════════════════════════════════════════════════════

def poll_video_task_until_done(
    task_id: str,
    poll_interval: int = POLL_INTERVAL_SEC,
    poll_timeout: int = POLL_TIMEOUT_SEC,
    platform_api_key: Optional[str] = None,
) -> str:
    """
    轮询等待口播视频任务完成，成功后返回 video_url。
    这是一个同步阻塞函数，适合批量调用；异步场景请使用 query_video_task 自行轮询。

    参数:
        task_id:         任务 ID
        poll_interval:   轮询间隔（秒），默认 5
        poll_timeout:    最长等待时间（秒），默认 300
        platform_api_key: 平台鉴权 key（可选，不传则自动读取）

    返回:
        video_url: 生成视频的下载 URL

    异常:
        TimeoutError: 任务超时
        RuntimeError: 任务失败
    """
    import time

    waited = 0
    while waited < poll_timeout:
        time.sleep(poll_interval)
        waited += poll_interval

        result = query_video_task(task_id, platform_api_key)
        status = result["task_status"]
        print(f"  口播任务状态：{status}（已等待 {waited}s）")

        if status == "SUCCEEDED":
            video_url = result["video_url"]
            if not video_url:
                raise RuntimeError(f"任务成功但未找到 video_url：{result}")
            return video_url
        elif status in ("FAILED", "CANCELLED", "UNKNOWN"):
            raise RuntimeError(f"口播任务失败，状态: {status}")

    raise TimeoutError(f"口播视频任务超时（已等待 {poll_timeout}s）")


# ═══════════════════════════════════════════════════════════
# 接口汇总说明
# ═══════════════════════════════════════════════════════════

"""
接口清单（统一通过自有平台代理，域名: platform.delilegal.com）:

| # | 函数                       | 方法 | 路径                          | 说明                          |
|---|----------------------------|------|-------------------------------|-------------------------------|
| 1 | create_portrait_video      | POST | /api/v1/skill/video/create    | 口播视频生成(wan2.7, 480P~720P)|
| 2 | query_video_task           | GET  | /api/v1/skill/video/task/{id} | 查询异步任务状态                |
| 3 | enroll_custom_voice        | POST | /api/v1/skill/voice/enroll    | 声音复刻(create_voice)         |
| 4 | generate_image             | POST | /api/v1/skill/image/generate  | 文生图(wan2.7-image)           |
| 5 | synthesize_cloned_voice    | POST | /api/v1/skill/voice/synthesize| 复刻声音TTS合成                |
| - | download_file              | GET  | {API 返回的下载 URL}          | 下载视频/图片（直接返回）        |

OSS 上传（三步走）:
| 6 | upload_file_via_platform     | —    | —（内部三步）                    | 入口函数            |
|6-1|   [内部] prepareUploadFile   | POST | /api/v1/file/prepareUploadFile  | 步骤一：获取临时链接  |
|6-2|   [内部] PUT OSS             | PUT  | {uploadUrl}（阿里云 OSS）        | 步骤二：上传文件     |
|6-3|   [内部] saveFile            | POST | /api/v1/file/saveFile           | 步骤三：保存记录     |

统一鉴权: Authorization: Bearer {platform_api_key}
  platform_api_key 来源: voice_config.json['api_key']
  所有函数的 platform_api_key 参数均可省略，省略时自动从 voice_config.json 读取
"""
