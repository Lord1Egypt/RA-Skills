#!/usr/bin/env python3
"""
产品介绍视频自动生成脚本
功能：文案TTS → 字幕生成 → 图片视频合成 → 字幕嵌入
成本策略：默认使用免费edge-tts；指定--voice myvoice + --clone-audio-url/file 时复刻声音后合成
"""

import argparse
import asyncio
import base64
import json
import math
import mimetypes
import os
import re
import random
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Any, List, Optional, Tuple


# ─────────────────────────────────────────────
# 配置与常量
# ─────────────────────────────────────────────

# macOS Python SSL 证书修复
import certifi
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

VOICE_CONFIG_PATH = Path(__file__).parent.parent / "voice_config.json"

EDGE_TTS_VOICES = {
    "zh-CN": "zh-CN-XiaoxiaoNeural",
    "zh-TW": "zh-TW-HsiaoYuNeural",
    "en-US": "en-US-JennyNeural",
    "en-GB": "en-GB-SoniaNeural",
    "ja-JP": "ja-JP-NanamiNeural",
    "ko-KR": "ko-KR-SunHiNeural",
    "fr-FR": "fr-FR-DeniseNeural",
    "de-DE": "de-DE-KatjaNeural",
}

EDGE_TTS_MALE_VOICES = {
    "zh-CN": "zh-CN-YunjianNeural",
    "zh-TW": "zh-TW-YunJheNeural",
    "en-US": "en-US-GuyNeural",
    "en-GB": "en-GB-RyanNeural",
    "ja-JP": "ja-JP-KeitaNeural",
    "ko-KR": "ko-KR-InJoonNeural",
    "fr-FR": "fr-FR-HenriNeural",
    "de-DE": "de-DE-ConradNeural",
}

DEFAULT_RESOLUTION = (1920, 1080)
MAX_CHARS_PER_LINE_ZH = 24   # 中文每行最多字符数（1920宽度，字号24，约24字/行）
MAX_CHARS_PER_LINE_EN = 42   # 英文每行最多字符数

# 图片过渡特效配置
TRANSITION_DURATION = 0.6      # 每段过渡持续时间（秒）
SEGMENT_PADDING_SEC = TRANSITION_DURATION  # 每段视频尾部留出过渡空间；xfade offset 用视频时长算时，padding 被 xfade 重叠精确抵消，SRT 仍基于音频时长
TRANSITION_EFFECTS = [
    "wipeleft",       # 百叶窗近似：左擦除（多竖条感）
    "wipeup",         # 百叶窗近似：上擦除（多横条感）
    "circleopen",      # 圆形展开
    "slideleft",      # 新图从左滑入（从左到右移动感）
    "fade",           # 淡入淡出
]
# 自定义特效：百叶窗（blinds）+ 放大局部到全局（zoom）通过 per-segment 滤镜实现
BLINDS_STRIPES = 8              # 百叶窗条纹数量

# 口播视频相关常量
PORTRAIT_SEGMENT_PREFIX = ("口播：", "口播:", "【口播】", "[口播]")
PORTRAIT_MAX_DURATION_SEC = 15.0          # 超出此时长降级为图片视频
WAN2_POLL_INTERVAL = 5     # 轮询间隔（秒）
WAN2_POLL_TIMEOUT = 300    # 最长等待（秒）


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def log(msg: str, level: str = "INFO"):
    prefix = {"INFO": "ℹ️ ", "WARN": "⚠️ ", "ERR": "❌", "OK": "✅"}.get(level, "")
    print(f"{prefix} {msg}")


def load_voice_config() -> dict:
    """加载 voice_config.json，不存在则返回空字典"""
    if VOICE_CONFIG_PATH.exists():
        with open(VOICE_CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_voice_config(api_key: str = "", voice_id: str = ""):
    """将 api_key 和/或 voice_id 写入 voice_config.json。"""
    cfg = load_voice_config()
    if api_key:
        cfg["api_key"] = api_key
    if voice_id:
        cfg["voice_id"] = voice_id
    with open(VOICE_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    log(f"voice_config.json 已更新：voice_id={voice_id[:20] if voice_id else '（未变）'}...", "OK")



def load_platform_api_key() -> str:
    """
    从 voice_config.json 读取自有平台的 API Key。
    键路径：voice_config['api_key']

    所有调用自有平台服务（platform.delilegal.com）时，
    均需在 Header 中携带：Authorization: Bearer {api_key}

    Returns:
        api_key (str): 平台鉴权 key，若未配置则返回空字符串
    """
    cfg = load_voice_config()
    return cfg.get("api_key", "").strip()



def build_audio_data_uri(local_audio_path: str) -> Optional[str]:
    """将本地音频文件通过平台 OSS 上传，返回公网可访问的 URL（非 data URI）。"""
    source = Path(local_audio_path)
    if not source.exists() or not source.is_file():
        log(f"音频文件不存在：{local_audio_path}", "WARN")
        return None

    try:
        url = upload_file_for_temp_url(local_audio_path)
        log(f"音频文件已上传到 OSS：{url[:80]}...", "OK")
        return url
    except Exception as e:
        log(f"本地音频上传 OSS 失败：{e}", "WARN")
        return None


def enroll_my_voice(
    audio_url: str,
    prefix: str,
    language: str,
) -> Optional[str]:
    """
    调用自有平台声音复刻接口创建 voice_id。
    接口: POST /api/v1/skill/voice/enroll（platform.delilegal.com）
    voice_id 仅在内存中使用，不写入 voice_config.json。
    失败时返回 None。
    """
    try:
        from dashscope_api import enroll_custom_voice
    except ImportError:
        sys.path.insert(0, str(Path(__file__).parent))
        from dashscope_api import enroll_custom_voice

    try:
        voice_id = enroll_custom_voice(
            audio_url=audio_url,
            prefix=prefix,
            language=language,
        )
        log(f"自动复刻成功，voice_id：{voice_id}", "OK")
        return voice_id
    except Exception as e:
        log(f"自动复刻失败：{e}", "WARN")
        return None


# ─────────────────────────────────────────────
# 口播视频模块（wan2.7-i2v-2026-04-25）
# ─────────────────────────────────────────────

def detect_portrait_segment(segment: str) -> Optional[str]:
    """
    检测文案首段是否含口播前缀（如"口播：xxx"）。
    若是则返回去除前缀后的纯文本；否则返回 None。
    """
    for prefix in PORTRAIT_SEGMENT_PREFIX:
        if segment.startswith(prefix):
            return segment[len(prefix):].strip()
    return None


def upload_file_for_temp_url(local_path: str) -> str:
    """
    上传本地文件到平台 OSS，返回带签名的 HTTPS 下载地址（fileUrl）。

    鉴权：自动从 voice_config.json['api_key'] 读取平台 API Key。
    Header: Authorization: Bearer {platform_api_key}

    三步流程（通过 platform.delilegal.com 完成上传）：
      步骤一：POST /api/v1/file/prepareUploadFile → 获取 OSS 上传临时链接
      步骤二：PUT  {uploadUrl}（OSS 直传，binary body）→ 上传文件到 OSS
      步骤三：POST /api/v1/file/saveFile → 保存文件记录，获取 fileUrl

    参数 api_key 保留是为了兼容调用方，实际不再用于平台鉴权（平台 key 自动从配置读取）。
    """
    try:
        import requests as _requests
        import certifi
        import hashlib
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "requests", "certifi", "-q"], check=True)
        import requests as _requests
        import certifi
        import hashlib

    import os
    os.environ["SSL_CERT_FILE"] = certifi.where()

    # 从 voice_config.json 读取平台 API Key
    platform_api_key = load_platform_api_key()
    if not platform_api_key:
        raise RuntimeError(
            "未找到平台 API Key，请在 voice_config.json 中设置 api_key"
        )

    source = Path(local_path)
    file_name = source.name

    # 计算文件 MD5
    h = hashlib.md5()
    with open(local_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    file_hash = h.hexdigest()

    platform_headers = {
        "Authorization": f"Bearer {platform_api_key}",
        "Content-Type": "application/json",
    }
    prepare_url = "https://platform.delilegal.com/api/v1/file/prepareUploadFile"
    save_url = "https://platform.delilegal.com/api/v1/file/saveFile"

    # 步骤一：获取上传临时链接
    resp1 = _requests.post(
        prepare_url,
        headers=platform_headers,
        json={"fileHash": file_hash, "fileName": file_name},
        timeout=30,
    )
    if resp1.status_code != 200 or not resp1.json().get("success"):
        raise RuntimeError(f"[步骤一] prepareUploadFile 失败（{resp1.status_code}）：{resp1.text}")
    body1 = resp1.json().get("body", {})
    upload_url = body1.get("uploadUrl", "")
    oss_headers = body1.get("headers", {})
    already_exists = body1.get("exist", False)

    if not upload_url:
        raise RuntimeError(f"[步骤一] 响应中缺少 uploadUrl：{resp1.json()}")

    # 步骤二：PUT 上传文件到 OSS（exist=True 时可跳过）
    if not already_exists:
        put_headers = dict(oss_headers)
        if "Content-Type" not in put_headers:
            put_headers["Content-Type"] = "application/octet-stream"
        with open(local_path, "rb") as f:
            file_data = f.read()
        resp2 = _requests.put(upload_url, headers=put_headers, data=file_data, timeout=180)
        if resp2.status_code not in (200, 204):
            raise RuntimeError(f"[步骤二] 上传到 OSS 失败（{resp2.status_code}）：{resp2.text[:200]}")

    # 步骤三：保存文件记录
    resp3 = _requests.post(
        save_url,
        headers=platform_headers,
        json={"fileHash": file_hash, "originalName": file_name},
        timeout=30,
    )
    if resp3.status_code != 200 or not resp3.json().get("success"):
        raise RuntimeError(f"[步骤三] saveFile 失败（{resp3.status_code}）：{resp3.text}")
    body3 = resp3.json().get("body", {})
    file_url = body3.get("fileUrl", "")
    if not file_url:
        raise RuntimeError(f"[步骤三] 响应中缺少 fileUrl：{resp3.json()}")

    return file_url


async def create_portrait_video(
    portrait_path: str,
    audio_path: str,
    output_path: str,
    api_key: str,
    quality: str = "standard",
    duration: float = 5.0,
    prompt: str = "人像保持 超写实，皮肤纹理清晰但平滑，零毛孔，肤色均匀，白皙透亮，无痘印雀斑，电影级布光，景深效果，8K分辨率，专业美容修图质感",
) -> bool:
    """
    通过自有平台接口生成真人口播视频（异步），统一使用 wan2.7-i2v 模型。
    resolution 由 quality 参数决定：standard → 480P，high → 720P。
    成功返回 True；失败抛出异常，由调用方捕获并降级为图片视频。
    """
    try:
        from dashscope_api import create_portrait_video as api_create_video, query_video_task as api_query_task
    except ImportError:
        sys.path.insert(0, str(Path(__file__).parent))
        from dashscope_api import create_portrait_video as api_create_video, query_video_task as api_query_task

    resolution = "720P" if quality == "high" else "480P"

    log("上传真人照片到平台 OSS...")
    image_url = upload_file_for_temp_url(portrait_path)
    log("上传口播音频到平台 OSS...")
    audio_url_remote = upload_file_for_temp_url(audio_path)

    log(f"提交口播视频生成任务（wan2.7-i2v，{resolution}）...")
    task_id = api_create_video(
        image_url=image_url,
        audio_url=audio_url_remote,
        prompt=prompt,
        duration=max(2, min(15, math.ceil(duration))),
        resolution=resolution,
    )
    log(f"口播任务已提交，task_id: {task_id}，等待完成...")

    waited = 0
    while waited < WAN2_POLL_TIMEOUT:
        await asyncio.sleep(WAN2_POLL_INTERVAL)
        waited += WAN2_POLL_INTERVAL
        result = api_query_task(task_id)
        task_status = result["task_status"]
        log(f"  口播任务状态：{task_status}（已等待 {waited}s）")
        if task_status == "SUCCEEDED":
            video_url = result["video_url"]
            if not video_url:
                raise RuntimeError(f"口播任务成功但未找到 video_url：{result}")
            log("下载生成的口播视频...")
            httpx = __import__("httpx") if "httpx" in sys.modules else None
            if httpx is None:
                httpx = __import__("httpx")
            dl = httpx.get(video_url, timeout=180, follow_redirects=True)
            dl.raise_for_status()
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as fout:
                fout.write(dl.content)
            log(f"口播视频已保存：{output_path}", "OK")
            return True
        elif task_status in ("FAILED", "CANCELLED", "UNKNOWN"):
            raise RuntimeError(f"口播任务失败，状态: {task_status}")
    raise TimeoutError(f"口播视频任务超时（已等待 {WAN2_POLL_TIMEOUT}s）")


def select_tts_strategy(voice_arg: Optional[str]) -> str:
    """
    根据用户参数决定 TTS 方案。
    voice_id 不再从配置文件读取，由调用方在运行时提供。
    返回值：'myvoice' | 'edge_tts'
    """
    if voice_arg and "myvoice" in voice_arg.lower():
        return "myvoice"
    return "edge_tts"


def parse_script(script_path: str) -> List[str]:
    """
    解析文案脚本文件，返回段落列表。
    支持格式：
      - 每行一段（空行忽略）
      - "第N段：内容" 或 "N. 内容" 前缀（自动去除前缀）
    """
    with open(script_path, encoding="utf-8") as f:
        raw_lines = f.readlines()

    segments = []
    for line in raw_lines:
        line = line.strip()
        if not line:
            continue
        # 去除常见序号前缀
        line = re.sub(r'^(第\d+段[：:]\s*|\d+[\.、]\s*)', '', line)
        if line:
            segments.append(line)

    return segments


def collect_images(images_dir: str) -> List[Path]:
    """收集图片目录下所有支持的图片，按文件名排序"""
    supported = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    images_dir = Path(images_dir)
    images = sorted(
        [p for p in images_dir.iterdir() if p.suffix.lower() in supported],
        key=lambda p: p.name
    )
    return images


def validate_inputs(segments: List[str], images: List[Path]):
    """校验文案段落数与图片数量是否一致"""
    if len(segments) != len(images):
        log(f"文案段落数（{len(segments)}）与图片数量（{len(images)}）不一致！", "ERR")
        log("文案段落：", "ERR")
        for i, s in enumerate(segments, 1):
            log(f"  {i}. {s[:40]}{'...' if len(s)>40 else ''}", "ERR")
        log("图片文件：", "ERR")
        for i, p in enumerate(images, 1):
            log(f"  {i}. {p.name}", "ERR")
        sys.exit(1)


def extract_segment_number(filename: str) -> Optional[int]:
    """
    从文件名中提取段落序号。
    支持格式：第1步.png、01.png、img_3.jpg、3-xxx.png 等。
    优先匹配 "第N步/第N段" 模式，其次匹配文件名中的阿拉伯数字。
    """
    # 优先：中文序号 "第N步"/"第N段"
    m = re.search(r'第(\d+)', filename)
    if m:
        return int(m.group(1))
    # 其次：独立数字（取最大的数字，避免误匹配如 "1080x1920"）
    nums = [int(x) for x in re.findall(r'\d+', filename)]
    if nums:
        return max(nums)
    return None


def match_images_to_segments(segments: List[str], images: List[Path]) -> Tuple[List[Optional[Path]], List[int]]:
    """
    将已有图片按文件名中的序号智能匹配到对应段落（1-based）。

    返回:
        matched: 长度等于 segments 的列表，每个元素为匹配到的 Path 或 None
        matched_indices: 已成功匹配的段落索引列表（0-based）
    """
    num_to_img: dict[int, Path] = {}
    for img in images:
        num = extract_segment_number(img.name)
        if num is not None:
            num_to_img[num] = img

    matched: List[Optional[Path]] = [None] * len(segments)
    matched_indices: List[int] = []
    for i in range(len(segments)):
        seg_num = i + 1  # 1-based
        if seg_num in num_to_img:
            matched[i] = num_to_img[seg_num]
            matched_indices.append(i)
            log(f"  段落 {seg_num} → 已有图片：{num_to_img[seg_num].name}", "OK")

    return matched, matched_indices


async def fill_missing_images(
    segments: List[str],
    matched: List[Optional[Path]],
    resolution: str,
    api_key: str,
    output_dir: Path,
    image_style: str = "",
    scene_descriptions: Optional[List[str]] = None,
) -> List[Path]:
    """
    对 matched 列表中为 None 的段落，自动生成配图并合并返回完整的图片列表。

    返回完整的 images 列表（长度等于 segments），每项都有值。
    """
    missing_indices = [i for i, m in enumerate(matched) if m is None]
    if not missing_indices:
        return [m for m in matched if m is not None]  # type: ignore[return-value]

    missing_segments = [segments[i] for i in missing_indices]
    missing_descriptions = None
    if scene_descriptions:
        missing_descriptions = [scene_descriptions[i] for i in missing_indices]

    log(f"需为 {len(missing_indices)} 个缺失段落自动生成配图：{missing_indices}")

    gen_images = await generate_images_for_segments(
        missing_segments, resolution, api_key, output_dir, image_style,
        scene_descriptions=missing_descriptions,
    )

    # 按生成顺序填回 matched 列表
    result: List[Path] = []
    gen_idx = 0
    for i in range(len(segments)):
        if matched[i] is not None:
            result.append(matched[i])  # type: ignore[arg-type]
        else:
            result.append(gen_images[gen_idx])
            gen_idx += 1
    return result


def get_audio_duration(audio_path: str) -> float:
    """使用 ffprobe 获取音频时长（秒）"""
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def strip_punctuation(text: str) -> str:
    """只去除每行最后一个标点符号，中间的标点保留。"""
    lines = text.split('\n')
    result = []
    for line in lines:
        line = line.strip()
        if line:
            # 去掉行尾最后一个标点（中文/英文标点均覆盖）
            line = re.sub(r'[^\w\s\u4e00-\u9fff\u3400-\u4dbf]$', '', line)
        result.append(line)
    return '\n'.join(result)


def seconds_to_srt_time(seconds: float) -> str:
    """将秒数转换为 SRT 时间格式 HH:MM:SS,mmm"""
    ms = int((seconds % 1) * 1000)
    s = int(seconds) % 60
    m = int(seconds) // 60 % 60
    h = int(seconds) // 3600
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _visual_width(text: str) -> float:
    """计算文本视觉宽度：中文/全角=1，英文/符号=0.5"""
    width = 0.0
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff' or '\u3400' <= ch <= '\u4dbf' or '\u3000' <= ch <= '\u303f' or '\uff00' <= ch <= '\uffef':
            width += 1.0
        else:
            width += 0.5
    return width


def _char_index_at_width(text: str, max_width: float) -> int:
    """找到视觉宽度刚好不超过 max_width 的字符索引"""
    width = 0.0
    for i, ch in enumerate(text):
        char_w = 1.0 if ('\u4e00' <= ch <= '\u9fff' or '\u3400' <= ch <= '\u4dbf' or '\u3000' <= ch <= '\u303f' or '\uff00' <= ch <= '\uffef') else 0.5
        if width + char_w > max_width:
            return i
        width += char_w
    return len(text)


def wrap_subtitle_text(text: str, lang: str) -> str:
    """按视觉宽度自动换行字幕文本，优先在标点符号处断行，不拆英文单词。"""
    max_chars = MAX_CHARS_PER_LINE_ZH if lang.startswith("zh") else MAX_CHARS_PER_LINE_EN
    if _visual_width(text) <= max_chars:
        return text

    lines = []
    buf = ""
    for ch in text:
        buf += ch
        # 到达行宽时，尝试在标点处断行；否则强制断行
        if _visual_width(buf) >= max_chars:
            # 在 buf 末尾附近找标点（优先在行尾断）
            split_pos = -1
            # 先找最近的标点（在 buf 的后 1/3 范围内）
            search_start = max(0, len(buf) - int(max_chars))
            for j in range(len(buf) - 1, search_start - 1, -1):
                if buf[j] in "，。！？、；：,.!?;:":
                    split_pos = j + 1
                    break
            if split_pos < 0:
                split_pos = len(buf)
                # 英文单词保护：如果断点前后都是英文字母，回退到单词开头
                if split_pos > 0 and split_pos < len(buf):
                    def _is_word_char(c):
                        return c.isascii() and c.isalpha()
                    if _is_word_char(buf[split_pos - 1]) and _is_word_char(buf[split_pos]):
                        left = split_pos
                        while left > search_start and _is_word_char(buf[left - 1]):
                            left -= 1
                        if left > search_start:
                            split_pos = left
            lines.append(buf[:split_pos])
            buf = buf[split_pos:]

    if buf:
        lines.append(buf)

    return "\n".join(lines)


def generate_srt(segments: List[str], durations: List[float], lang: str) -> str:
    """
    生成 SRT 字幕内容字符串（自动去除标点符号）。

    对于需要换行的长文本，拆分为多个字幕条目，
    每个条目的显示时长按字数比例分配，确保每段字幕都有显示机会。
    SRT 时间线严格跟随音频时间线，不累加 padding。
    """
    srt_lines = []
    current_time = 0.0
    entry_idx = 1

    for text, duration in zip(segments, durations):
        # 去除标点
        clean_text = strip_punctuation(text)
        # 自动换行（可能包含 \n 分隔的多行）
        wrapped = wrap_subtitle_text(clean_text, lang)
        sub_lines = [line for line in wrapped.split('\n') if line.strip()]

        if len(sub_lines) <= 1:
            # 无需拆分，整段显示一个字幕条目
            srt_lines.append(str(entry_idx))
            srt_lines.append(
                f"{seconds_to_srt_time(current_time)} --> "
                f"{seconds_to_srt_time(current_time + duration)}"
            )
            srt_lines.append(sub_lines[0] if sub_lines else clean_text)
            srt_lines.append("")
            entry_idx += 1
        else:
            # 按视觉宽度比例分配每行的显示时长
            total_width = sum(_visual_width(line) for line in sub_lines)
            allocated = 0.0
            for line in sub_lines:
                proportion = (
                    _visual_width(line) / total_width
                    if total_width > 0
                    else 1.0 / len(sub_lines)
                )
                line_duration = duration * proportion
                start = current_time + allocated
                end = start + line_duration
                srt_lines.append(str(entry_idx))
                srt_lines.append(
                    f"{seconds_to_srt_time(start)} --> {seconds_to_srt_time(end)}"
                )
                srt_lines.append(line)
                srt_lines.append("")
                entry_idx += 1
                allocated += line_duration

        # SRT 时间线严格跟随音频时间线，不累加 padding
        current_time += duration

    return "\n".join(srt_lines)


# ─────────────────────────────────────────────
# TTS 模块
# ─────────────────────────────────────────────

URL_PATTERN = re.compile(r"(?:https?://)?(?:www\.)?[\w-]+(?:\.[\w-]+)+(?:/[^\s]*)?")

def preprocess_for_tts(text: str) -> str:
    """为 TTS 引擎预处理文本，解决 URL/域名被逐字母念的问题。

    把域名中的 '.' 替换为 '点'，例如：
      open.delilegal.com -> open点delilegal点com
      www.delilegal.com  -> www点delilegal点com
    这样中/英混合 TTS（尤其是 CosyVoice 复刻声音）会把域名按词/音节发音，
    而不是逐个字母念。
    """
    def _replace_url(match: re.Match) -> str:
        raw = match.group(0)
        # 去掉 http:// 或 https:// 前缀
        cleaned = re.sub(r"^https?://", "", raw)
        # 把 . 替换为 点
        return cleaned.replace(".", "点")

    return URL_PATTERN.sub(_replace_url, text)


async def synthesize_edge_tts(text: str, output_path: str, lang: str, gender: str = "female"):
    """
    使用 edge-tts 合成语音（免费）。
    gender: 'female'（默认）或 'male'，选择对应语言的男/女声。
    """
    try:
        import edge_tts
    except ImportError:
        log("edge-tts 未安装，正在安装...", "WARN")
        subprocess.run([sys.executable, "-m", "pip", "install", "edge-tts", "-q"], check=True)
        import edge_tts

    if gender == "male" and lang in EDGE_TTS_MALE_VOICES:
        voice = EDGE_TTS_MALE_VOICES[lang]
    else:
        voice = EDGE_TTS_VOICES.get(lang, EDGE_TTS_VOICES["zh-CN"])
    log(f"edge-tts 声音：{voice}（{gender}）")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


def synthesize_myvoice(text: str, output_path: str, voice_id: str) -> bool:
    """
    使用复刻的我的声音合成语音。
    通过自有平台接口: POST /api/v1/skill/voice/synthesize
    voice_id 由调用方在运行时传入（不复用配置文件）。
    失败时返回 False，调用方降级到 edge-tts。
    """
    if not voice_id:
        return False

    try:
        from dashscope_api import synthesize_cloned_voice
    except ImportError:
        sys.path.insert(0, str(Path(__file__).parent))
        from dashscope_api import synthesize_cloned_voice

    try:
        audio_url = synthesize_cloned_voice(text=text, voice_id=voice_id)
        # 从返回的 audioUrl 下载音频并保存
        import requests as _reqs
        dl = _reqs.get(audio_url, timeout=120)
        dl.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(dl.content)
        # 记录音频时长
        try:
            import subprocess as _sp
            r = _sp.run([
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                output_path
            ], capture_output=True, text=True)
            dur = float(r.stdout.strip())
            log(f"  复刻声音音频已保存：{output_path}（时长 {dur:.2f}s）")
        except:
            log(f"  复刻声音音频已保存：{output_path}")
        return True
    except Exception as e:
        # 尽可能打印详细错误信息（如余额不足、401、403等）
        err_msg = str(e)
        # 如果是 httpx.HTTPStatusError，提取状态码和响应内容
        try:
            import httpx as _hx
            if isinstance(e, _hx.HTTPStatusError):
                resp = e.response
                err_msg = (
                    f"HTTP {resp.status_code}：{resp.text[:500]}"
                )
        except Exception:
            pass
        log(f"我的声音API调用失败：{err_msg}，将降级为 edge-tts", "WARN")
        return False


async def synthesize_segment(
    text: str,
    output_path: str,
    strategy: str,
    lang: str,
    voice_id: str = "",
    edge_tts_gender: str = "female"
):
    """合成单段音频，根据策略自动选择引擎。

    注：TTS 输入文本会经过 preprocess_for_tts 预处理（例如将域名中的点替换为"点"），
    但 segments 列表中的原始文本不会被修改，字幕仍显示原始文案。
    """
    tts_text = preprocess_for_tts(text)
    if strategy == "myvoice":
        success = synthesize_myvoice(tts_text, output_path, voice_id)
        if success:
            save_voice_config(voice_id=voice_id)
        else:
            await synthesize_edge_tts(tts_text, output_path, lang, edge_tts_gender)
    else:
        await synthesize_edge_tts(tts_text, output_path, lang, edge_tts_gender)


async def synthesize_all_segments(
    segments: List[str],
    audio_dir: str,
    strategy: str,
    lang: str,
    voice_id: str = "",
    edge_tts_gender: str = "female"
) -> List[str]:
    """
    批量合成所有段落的音频。
    返回音频文件路径列表。
    """
    audio_dir = Path(audio_dir)
    audio_dir.mkdir(parents=True, exist_ok=True)
    audio_paths = []

    for i, text in enumerate(segments, 1):
        out_path = str(audio_dir / f"segment_{i:03d}.mp3")
        log(f"合成第 {i}/{len(segments)} 段音频：{text[:30]}{'...' if len(text)>30 else ''}")
        await synthesize_segment(text, out_path, strategy, lang, voice_id, edge_tts_gender)
        audio_paths.append(out_path)

    return audio_paths


# ─────────────────────────────────────────────
# 视频合成模块（纯 ffmpeg，零成本）
# ─────────────────────────────────────────────

def check_ffmpeg():
    """检查 ffmpeg 是否可用"""
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
    if result.returncode != 0:
        log("ffmpeg 未安装！请先安装 ffmpeg：", "ERR")
        log("  macOS:  brew install ffmpeg", "ERR")
        log("  Ubuntu: sudo apt install ffmpeg", "ERR")
        log("  Windows: https://ffmpeg.org/download.html", "ERR")
        sys.exit(1)


def build_segment_video(
    image_path: str,
    audio_path: str,
    output_path: str,
    resolution: Tuple[int, int] = DEFAULT_RESOLUTION
):
    """
    将单张图片 + 单段音频合成为一段视频片段。
    图片时长 = 音频时长 + SEGMENT_PADDING_SEC
    """
    w, h = resolution
    scale_filter = (
        f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
        f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black"
    )

    duration = get_audio_duration(audio_path) + SEGMENT_PADDING_SEC

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", image_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ac", "2",
        "-ar", "44100",
        "-pix_fmt", "yuv420p",
        "-t", str(duration),
        "-vf", scale_filter,
        output_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)


def reencode_video(input_path: str, output_path: str, resolution: Tuple[int, int] = DEFAULT_RESOLUTION):
    """
    将视频重新编码为目标分辨率，保持音频原有轨道。
    用于统一口播视频（如 512×640）到输出分辨率（如 1920×1080）。
    """
    w, h = resolution
    scale_filter = (
        f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
        f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black"
    )
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vf", scale_filter,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-r", "25",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ac", "2",
        "-ar", "44100",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)


def get_video_duration(video_path: str) -> float:
    """使用 ffprobe 获取视频时长（秒）"""
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ],
        capture_output=True, text=True
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0.0


def build_segment_video_with_ken_burns(
    image_path: str,
    audio_path: str,
    output_path: str,
    resolution: Tuple[int, int] = DEFAULT_RESOLUTION,
    zoom_out: bool = True,
):
    """
    将单张图片 + 单段音频合成为一段视频片段，附带 Ken Burns 镜头运动。
    zoom_out=True  ：从局部放大开始，逐渐缩小到全局（对应「放大局部慢缩到全局」）
    zoom_out=False ：从全局开始，逐渐放大到局部
    """
    w, h = resolution
    duration = get_audio_duration(audio_path) + SEGMENT_PADDING_SEC
    fps = 25
    total_frames = max(int(duration * fps), 1)

    # zoompan 表达式：
    #   zoom_out=True  → z 从 2.5 线性降至 1.0（放大局部 → 全局）
    #   zoom_out=False → z 从 1.0 线性升至 2.5（全局 → 放大局部）
    if zoom_out:
        z_expr = f"if(eq(n,0),2.5,max(1.0,{2.5} - (1.5)*n/{total_frames}))"
    else:
        z_expr = f"if(eq(n,0),1.0,min(2.5,1.0 + (1.5)*n/{total_frames}))"

    # x、y 始终居中，配合 zoom 变化实现平滑运动
    x_expr = f"(iw - iw/zoom)/2"
    y_expr = f"(ih - ih/zoom)/2"

    zoompan_filter = (
        f"zoompan=z='{z_expr}':"
        f"x='{x_expr}':"
        f"y='{y_expr}':"
        f"d={total_frames}:"
        f"s={w}x{h}:"
        f"fps={fps}"
    )
    # zoompan 输出帧后再做一次 scale+pad 确保分辨率精确
    scale_filter = (
        f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
        f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", image_path,
        "-i", audio_path,
        "-vf", f"{zoompan_filter},{scale_filter}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ac", "2",
        "-ar", "44100",
        "-pix_fmt", "yuv420p",
        "-t", str(duration),
        output_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)


def _create_blinds_transition(
    video_a: str,
    video_b: str,
    output_path: str,
    duration: float = TRANSITION_DURATION,
    resolution: Tuple[int, int] = DEFAULT_RESOLUTION,
    stripes: int = BLINDS_STRIPES,
):
    """
    自定义「百叶窗」过渡片段：
    将 video_b 切割为 stripes 条水平条纹，依次延迟出现，覆盖在 video_a 末尾。
    输出一段时长 = duration 的过渡视频，可直接插入两段视频之间。
    """
    w, h = resolution
    stripe_h = h / stripes
    delay_per = duration / stripes

    # 构建 filter_complex：
    # ① 两个输入都 trim 到 duration（过渡片段本身时长）
    # ② 将 [1:v] 切割为 stripes 条
    # ③ 用 overlay + enable='gte(t, i*delay_per)' 逐条显示
    parts = []
    # 输入标签
    parts.append(f"[0:v]trim=duration={duration},setpts=PTS-STARTPTS[a];")
    parts.append(f"[1:v]trim=duration={duration},setpts=PTS-STARTPTS[b];")

    # 切割 b 为 stripes 条
    for i in range(stripes):
        y_off = int(i * stripe_h)
        parts.append(
            f"[b]crop={w}:{int(stripe_h)}:0:{y_off},"
            f"setpts=PTS-STARTPTS[s{i}];"
        )

    # 逐条 overlay
    label = "[a]"
    for i in range(stripes):
        next_label = f"[v{i}]" if i < stripes - 1 else "[out]"
        enable_cond = f"gte(t,{i * delay_per:.3f})"
        y_pos = int(i * stripe_h)
        parts.append(
            f"{label}[s{i}]overlay=0:{y_pos}:enable='{enable_cond}'{next_label};"
        )
        label = next_label

    filter_complex = "".join(parts)

    cmd = [
        "ffmpeg", "-y",
        "-i", video_a,
        "-i", video_b,
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-t", str(duration),
        output_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)


def concatenate_videos_with_xfade(
    segment_paths: List[str],
    output_path: str,
    tmp_dir: str,
    transition_duration: float = TRANSITION_DURATION,
    resolution: Tuple[int, int] = DEFAULT_RESOLUTION,
    audio_durations: Optional[List[float]] = None,
    original_audio_paths: Optional[List[str]] = None,
):
    """
    使用 xfade 滤镜将多个视频片段拼接，片段间随机选用过渡特效。
    支持 xfade 内置特效 + 自定义 blinds 特效。

    audio_durations: 每段原始音频时长（不含 padding）。
      用于计算 xfade offset，确保 transition 在音频结束处发生。
    original_audio_paths: 每段原始音频文件路径（不含 padding）。
      若提供，音频拼接直接使用原始 mp3，避免 padding 静默导致字幕滞后。
      若未提供，降级为从视频片段提取音频（可能字幕漂移）。
    """
    n = len(segment_paths)
    if n == 1:
        shutil.copy2(segment_paths[0], output_path)
        return

    random.seed(42)
    w, h = resolution

    # ── 1. 统一转码所有片段 ──
    reenc_dir = Path(tmp_dir) / "_xfade_reenc"
    reenc_dir.mkdir(parents=True, exist_ok=True)
    reenc = []
    for i, p in enumerate(segment_paths):
        out = str(reenc_dir / f"seg_{i:03d}.mp4")
        reencode_video(p, out, resolution)
        reenc.append(out)
    segs = reenc  # 使用转码后的路径

    # ── 2. 获取每段时长 ──
    #    视频片段时长（含 padding），用于 xfade 的 offset 计算
    video_durations = [get_video_duration(p) for p in segs]

    #    xfade offset 始终用视频时长计算：
    #    offset_i = sum(video_durations[:i]) - i * transition_duration
    #             = sum(audio[:i] + padding) - i * transition_duration
    #             = sum(audio[:i]) + i*padding - i*transition_duration
    #    当 padding == transition_duration 时， = sum(audio[:i])  → 音频边界
    #    这样 transition 精准在音频边界发生，SRT 时间线与之对齐。
    durations_for_offset = video_durations
    use_audio_offset = False

    # ── 3. 为每对相邻片段分配特效 ──
    #     特效可以是 xfade 内置名称，或是 "blinds" / "zoom"
    pair_effects = []
    for i in range(n - 1):
        pair_effects.append(random.choice(TRANSITION_EFFECTS + ["blinds"]))

    # ── 4. 如果有自定义特效（blinds），先生成对应的过渡片段 ──
    #     策略：xfade 能处理的统一用 xfade 一次性做；
    #           含 blinds 的 turn 拆出来单独做过渡片段再拼接。
    #
    #     为了简化，这里采用「全 xfade」策略，blinds 用 wipeleft 近似。
    #     （若以后需要真正 blinds，可改用 _create_blinds_transition 生成过渡片段。）
    xfade_effects = []
    for ef in pair_effects:
        if ef == "blinds":
            xfade_effects.append("wipeleft")   # 用 wipeleft 近似百叶窗
        else:
            xfade_effects.append(ef)

    # ── 5. 构建 xfade filter_complex ──
    #    offset 使用视频时长（含 padding），当 padding == transition_duration 时
    #    数学上等于音频边界，确保 transition 在音频边界发生，SRT 时间线对齐。
    log(f"xfade offset 使用视频时长（padding={SEGMENT_PADDING_SEC}s = transition={transition_duration}s → 等于音频边界）", "INFO")

    filter_parts = []
    prev = "[0:v]"
    for i in range(1, n):
        offset = sum(durations_for_offset[:i]) - i * transition_duration
        out_tag = f"[v{i}]" if i < n - 1 else "[vout]"
        filter_parts.append(
            f"{prev}[{i}:v]xfade="
            f"transition={xfade_effects[i-1]}:"
            f"duration={transition_duration}:"
            f"offset={offset:.3f}"
            f"{out_tag}"
        )
        prev = out_tag

    # ── 6. 视频：xfade 合成 ──
    cmd_video = ["ffmpeg", "-y"]
    for p in segs:
        cmd_video.extend(["-i", p])
    cmd_video += [
        "-filter_complex", ";".join(filter_parts),
        "-map", "[vout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-pix_fmt", "yuv420p",
        # 不限制输出时长，让 ffmpeg 自动计算（避免截断尾部）
        "-an",
        str(Path(tmp_dir) / "_xfade_video_only.mp4")
    ]
    subprocess.run(cmd_video, capture_output=True, check=True)
    video_only = str(Path(tmp_dir) / "_xfade_video_only.mp4")

    # ── 7. 音频：拼接 ──
    #     若提供 original_audio_paths，直接使用原始音频（不含 padding），
    #     避免从视频片段提取时带入 padding 静默，导致字幕累积滞后。
    #     否则降级：从转码后的视频片段提取音轨后拼接。
    audio_segs = []

    if original_audio_paths and len(original_audio_paths) == n:
        # 使用原始音频文件（不含 padding）。
        # 经验：先把 mp3 用 -c copy 拼成单个 mp3，再统一转 aac，
        # 否则先逐段转 aac 再 concat 会丢失约 3~6 秒时长。
        log(f"音频拼接：使用原始音频文件（{n} 个，不含 padding）", "INFO")
        concat_mp3 = str(Path(tmp_dir) / "_audio_concat.mp3")
        concat_list = Path(tmp_dir) / "audio_concat_list.txt"
        with open(concat_list, "w") as f:
            for p in original_audio_paths:
                f.write(f"file '{Path(p).absolute()}'\n")

        cmd_concat_mp3 = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy",
            concat_mp3
        ]
        r = subprocess.run(cmd_concat_mp3, capture_output=True, text=True)
        if r.returncode != 0:
            log(f"mp3 concat 失败：{r.stderr[-200:]}", "WARN")
            # 降级：从视频片段提取
            audio_segs = []
            for i, seg in enumerate(segs):
                audio_out = str(Path(tmp_dir) / f"_xfade_audio_seg_{i:03d}.aac")
                cmd_extract = [
                    "ffmpeg", "-y", "-i", seg,
                    "-c:a", "aac", "-b:a", "128k",
                    "-ac", "2", "-ar", "44100", "-vn", audio_out
                ]
                subprocess.run(cmd_extract, capture_output=True, check=True)
                audio_segs.append(audio_out)
        else:
            # 将拼接后的 mp3 统一转 aac
            raw_audio = str(Path(tmp_dir) / "_xfade_audio_only.aac")
            cmd_conv = [
                "ffmpeg", "-y",
                "-i", concat_mp3,
                "-c:a", "aac", "-b:a", "128k",
                "-ac", "2", "-ar", "44100", "-vn",
                raw_audio
            ]
            subprocess.run(cmd_conv, capture_output=True, check=True)
            audio_segs = [raw_audio]
    else:
        # 降级：从转码后的视频片段提取音轨（含 padding，可能字幕滞后）
        log(f"音频拼接：从转码片段提取音轨（{len(segs)} 个，含 padding）", "WARN")
        audio_segs = []
        for i, seg in enumerate(segs):
            audio_out = str(Path(tmp_dir) / f"_xfade_audio_seg_{i:03d}.aac")
            cmd_extract = [
                "ffmpeg", "-y",
                "-i", seg,
                "-c:a", "aac", "-b:a", "128k",
                "-ac", "2", "-ar", "44100",
                "-vn",
                audio_out
            ]
            r = subprocess.run(cmd_extract, capture_output=True, text=True)
            if r.returncode != 0:
                log(f"提取第 {i} 段音轨失败：{r.stderr[-150:]}", "WARN")
            audio_segs.append(audio_out)

    # 如果已经有拼接好的 raw_audio（mp3→aac 成功），直接复用
    if 'raw_audio' not in locals() or raw_audio is None:
        audio_list = Path(tmp_dir) / "audio_concat_list.txt"
        with open(audio_list, "w") as f:
            for p in audio_segs:
                f.write(f"file '{Path(p).absolute()}'\n")
        log(f"音频拼接：从转码片段提取音轨（{len(audio_segs)} 个，含 padding）", "INFO")

        raw_audio = str(Path(tmp_dir) / "_xfade_audio_only.aac")
        cmd_audio = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(audio_list),
            "-c:a", "aac", "-b:a", "128k",
            "-ac", "2", "-ar", "44100",
            raw_audio
        ]
        subprocess.run(cmd_audio, capture_output=True, check=True)
    else:
        log(f"音频拼接完成：{raw_audio}（已跳过二次 concat）", "OK")

    # ── 8. 视频 + 音频 mux ──
    #     视频含尾部 padding（=transition_duration），比音频多约 0.6s。
    #     用 -shortest + 重编码，精确在音频结束处截断，
    #     确保最后一帧停留在图片上（非黑屏），且音频完整播放。
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", video_only,
        "-i", raw_audio,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-map", "0:v", "-map", "1:a",
        "-shortest",
        output_path
    ]
    subprocess.run(cmd_mux, capture_output=True, check=True)
    log(f"xfade 拼接完成，共 {n} 段，特效：{xfade_effects}", "OK")


def concatenate_videos(segment_paths: List[str], output_path: str, tmp_dir: str,
                      force_reencode: bool = False, use_transitions: bool = False,
                      resolution: Tuple[int, int] = DEFAULT_RESOLUTION,
                      audio_durations: Optional[List[float]] = None,
                      original_audio_paths: Optional[List[str]] = None):
    """将多个视频片段拼接为最终视频。

    force_reencode=True 时先逐段统一转码再 copy 拼接（口播+图片混合场景必须开启）。
    use_transitions=True 时启用 xfade 图片过渡特效（随机选用 TRANSITION_EFFECTS）。
    audio_durations: 每段原始音频时长，传给 xfade 用于计算正确的 offset，
                   确保 transition 在音频边界发生，避免字幕漂移。
    original_audio_paths: 每段原始音频文件路径（不含 padding），
                       传给 xfade 用于音频拼接，避免 padding 静默导致字幕滞后。
    """
    if use_transitions and len(segment_paths) > 1:
        log("── 使用 xfade 过渡特效拼接 ──", "INFO")
        concatenate_videos_with_xfade(
            segment_paths, output_path, tmp_dir,
            transition_duration=TRANSITION_DURATION,
            resolution=resolution,
            audio_durations=audio_durations,
            original_audio_paths=original_audio_paths,
        )
        return

    segment_paths_to_concat = segment_paths

    if force_reencode:
        w, h = DEFAULT_RESOLUTION
        unified_segments = []
        for i, p in enumerate(segment_paths):
            reenc = str(Path(tmp_dir) / f"_concat_reenc_{i:03d}.mp4")
            reencode_video(p, reenc, DEFAULT_RESOLUTION)
            unified_segments.append(reenc)
        segment_paths_to_concat = unified_segments

    concat_list = Path(tmp_dir) / "concat_list.txt"
    with open(concat_list, "w") as f:
        for p in segment_paths_to_concat:
            f.write(f"file '{Path(p).absolute()}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        output_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)


def embed_soft_subtitles(video_path: str, srt_path: str, output_path: str):
    """将 SRT 字幕以软字幕方式嵌入视频（可关闭）"""
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", srt_path,
        "-c", "copy",
        "-c:s", "mov_text",
        "-metadata:s:s:0", "language=chi",
        output_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)


def parse_srt(srt_path: str) -> List[Tuple[float, float, str]]:
    """解析 SRT 文件，返回 [(start_sec, end_sec, text), ...]"""
    with open(srt_path, encoding="utf-8") as f:
        content = f.read()
    blocks = re.split(r'\n\s*\n', content.strip())
    result = []
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue
        # 解析时间行
        time_line = lines[1]
        m = re.match(
            r'(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})',
            time_line
        )
        if not m:
            continue
        g = m.groups()
        start = int(g[0])*3600 + int(g[1])*60 + int(g[2]) + int(g[3])/1000
        end = int(g[4])*3600 + int(g[5])*60 + int(g[6]) + int(g[7])/1000
        text = '\n'.join(lines[2:])
        result.append((start, end, text))
    return result


def burn_hard_subtitles(video_path: str, srt_path: str, output_path: str):
    """
    将 SRT 字幕硬编码烧录进视频画面。
    优先尝试 ffmpeg subtitles 滤镜（需 libass），
    若不可用则降级到 drawtext 滤镜拼接方式。
    """
    # 尝试方法1：ffmpeg subtitles 滤镜
    import shutil
    srt_abs = str(Path(srt_path).absolute())
    tmp_srt = None
    if not srt_abs.isascii():
        tmp_srt = Path(tempfile.gettempdir()) / "ffmpeg_subtitle_tmp.srt"
        shutil.copy2(srt_abs, str(tmp_srt))
        srt_abs = str(tmp_srt)
    srt_escaped = srt_abs.replace("\\", "/").replace(":", "\\:")

    cmd_subtitles = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"subtitles={srt_escaped}:force_style='FontSize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2'",
        "-c:a", "copy",
        output_path
    ]
    result = subprocess.run(cmd_subtitles, capture_output=True)
    if tmp_srt and tmp_srt.exists():
        tmp_srt.unlink()
    if result.returncode == 0:
        return

    # subtitles 滤镜不可用，降级到方法2：逐段叠加文本
    log("ffmpeg subtitles 滤镜不可用（缺少 libass），使用 drawtext+concat 方式烧录字幕", "WARN")
    _burn_subtitles_via_drawtext(video_path, srt_path, output_path)


def _burn_subtitles_via_drawtext(video_path: str, srt_path: str, output_path: str):
    """使用 ffmpeg drawtext 滤镜逐段烧录字幕（无需 libass）"""
    # 检查 drawtext 是否可用
    check = subprocess.run(
        ["ffmpeg", "-filters"],
        capture_output=True, text=True
    )
    if "drawtext" not in check.stdout:
        # drawtext 也不可用，用纯 Python 方案
        log("ffmpeg drawtext 滤镜也不可用（缺少 freetype），使用纯 Python 方案烧录字幕", "WARN")
        _burn_subtitles_via_python(video_path, srt_path, output_path)
        return

    subs = parse_srt(srt_path)
    if not subs:
        log("SRT 字幕解析为空，跳过烧录", "WARN")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(video_path, output_path)
        return

    w, h = DEFAULT_RESOLUTION
    font_size = 28
    # 字幕位置：底部 10% 区域
    y_pos = int(h * 0.85)

    # 构建 drawtext 滤镜链（每个字幕段一条 drawtext，用 enable 控制）
    drawtext_filters = []
    for start, end, text in subs:
        # 处理多行字幕
        lines = text.split('\n')
        for li, line in enumerate(lines):
            # drawtext 不支持中文路径，文字直接传入
            # 转义特殊字符
            escaped_text = line.replace("'", "'\\''").replace(":", "\\:").replace("=", "\\=")
            line_y = y_pos + li * (font_size + 8)
            enable = f"between(t\\,{start:.3f}\\,{end:.3f})"
            drawtext_filters.append(
                f"drawtext=fontfile=/System/Library/Fonts/PingFang.ttc:"
                f"text='{escaped_text}':fontsize={font_size}:"
                f"fontcolor=white:borderw=2:bordercolor=black:"
                f"x=(w-text_w)/2:y={line_y}:enable='{enable}'"
            )

    filter_str = ",".join(drawtext_filters)

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", filter_str,
        "-c:a", "copy",
        output_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)


def _burn_subtitles_via_python(video_path: str, srt_path: str, output_path: str):
    """
    纯 Python 方案烧录字幕：调用独立脚本 scripts/burn_subtitles.py。
    该脚本使用系统 Python（Pillow 可用）逐帧烧录字幕。
    不依赖 libass/freetype，但速度较慢。
    """
    # 查找 burn_subtitles.py 脚本
    script_dir = Path(__file__).parent
    burn_script = script_dir / "burn_subtitles.py"
    if not burn_script.exists():
        log("burn_subtitles.py 脚本不存在，降级为直接复制视频（无字幕）", "WARN")
        import shutil
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(video_path, output_path)
        return

    # 优先使用系统 Python（managed Python 的 Pillow 可能因签名问题无法加载）
    system_python = "/usr/local/bin/python3"
    python_bin = system_python if Path(system_python).exists() else sys.executable

    log(f"使用 {python_bin} 执行字幕烧录脚本", "INFO")
    result = subprocess.run(
        [python_bin, str(burn_script), video_path, srt_path, output_path],
        capture_output=True, text=True
    )
    if result.stdout:
        for line in result.stdout.strip().split('\n'):
            print(f"  {line}")
    if result.returncode != 0:
        log(f"字幕烧录脚本执行失败：{result.stderr[-300:] if result.stderr else '未知错误'}", "ERR")
        import shutil
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(video_path, output_path)


# ─────────────────────────────────────────────
# 图片生成模块（wan2.7-image）
# ─────────────────────────────────────────────

async def generate_images_for_segments(segments: List[str], resolution: str, api_key: str, output_dir: Path, image_style: str = "", scene_descriptions: Optional[List[str]] = None) -> List[Path]:
    """
    依据文案段落生成统一风格的图片。通过自有平台接口: POST /api/v1/skill/image/generate

    参数:
        segments:           文案段落列表
        resolution:         图片分辨率
        api_key:            平台 API Key（用于自有平台鉴权）
        output_dir:         图片输出目录
        image_style:        图片风格提示词
        scene_descriptions: 预生成的场景描述列表（由 WorkBuddy 改写后传入）。
                           若为 None 或与 segments 条数不一致，则使用 segments 原文作为 scene_desc。
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    w, h = map(int, resolution.lower().replace("x", "x").split("x"))

    if not api_key:
        api_key = load_voice_config().get("api_key", "").strip()
    if not api_key:
        api_key = os.environ.get("DASHSCOPE_API_KEY", "").strip()
    if not api_key:
        return await _generate_images_via_pillow(segments, resolution, output_dir, "未在 voice_config.json 或环境变量中找到 API Key")

    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from dashscope_api import generate_image as api_gen_image
        import requests as _reqs
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"], check=True)
        import requests as _reqs
        sys.path.insert(0, str(Path(__file__).parent))
        from dashscope_api import generate_image as api_gen_image

    size_str = f"{w}*{h}"

    # 使用外部传入的场景描述，或退化为原始文案
    if scene_descriptions and len(scene_descriptions) == len(segments):
        log(f"使用 WorkBuddy 预生成的场景描述，共 {len(scene_descriptions)} 条", "OK")
        for i, d in enumerate(scene_descriptions, 1):
            log(f"  段落{i}：{d}")
    else:
        log("未提供场景描述，使用原始文案作为图片生成 prompt", "WARN")
        scene_descriptions = segments

    async def fetch_image(i: int, scene_desc: str) -> Path:
        img_path = output_dir / f"gen_img_{i:03d}.png"

        style_prompt = f"纯正的{image_style.strip()}风格，精美高质量画面" if image_style.strip() else "高质量摄影级，专业、沉稳风格"
        prompt = (
            f"一幅无任何文字的配图，{style_prompt}。\n"
            f"画面场景：{scene_desc}\n"
            f"强制约束：画面极简干净，绝对禁止出现任何中英文字符、数字、Logo、水印！"
        )

        negative = (
            "1. 画面中不要出现任何文字字幕，除非必要否则不要出现文字，例如如有合同、聊天记录等大量文字的图片保持虚化。\n"
            "2. 不要虚构任何公司名称、品牌Logo、版权声明或联系方式。\n"
        )

        # 调用自有平台文生图接口
        img_url = await asyncio.to_thread(
            api_gen_image,
            prompt=prompt,
            size=size_str,
            negative_prompt=negative,
            watermark=False,
        )

        # 从返回的 imageUrl 下载图片
        dl = _reqs.get(img_url, timeout=120)
        dl.raise_for_status()
        with open(img_path, "wb") as f:
            f.write(dl.content)

        log(f"段落 {i} 图片生成成功：{img_path.name}")
        return img_path

    log(f"开始使用 逐张在线生成 {len(scene_descriptions)} 张图片...")
    images = []
    for i, desc in enumerate(scene_descriptions, 1):
        try:
            img = await fetch_image(i, desc)
            images.append(img)
        except Exception as e:
            log(f"段落 {i} 在线图片生成失败（{e}），降级使用 Python Pillow 生成本地配图...", "WARN")
            return await _generate_images_via_pillow(segments, resolution, output_dir, f"段落 {i} 在线生成失败: {e}")
    return images


async def _generate_images_via_pillow(segments: List[str], resolution: str, output_dir: Path, reason: str = "") -> List[Path]:
    """Pillow 降级生成配图（深蓝底+金字法律风格）"""
    if reason:
        log(f"{reason}。使用 Python Pillow 生成本地配图...", "WARN")
    w, h = map(int, resolution.lower().replace("x", "x").split("x"))
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "Pillow", "-q"], check=True)
        from PIL import Image, ImageDraw, ImageFont

    images = []
    for i, text in enumerate(segments, 1):
        img_path = output_dir / f"gen_img_{i:03d}.png"
        if img_path.exists():
            images.append(img_path)
            continue

        # 深蓝色背景，专业法律风格
        img = Image.new('RGB', (w, h), color=(15, 32, 60))
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 60)
        except IOError:
            try:
                font = ImageFont.truetype("msyh.ttc", 60)
            except IOError:
                font = ImageFont.load_default()

        # 文字换行，避免超出边界
        max_chars_per_line = w // 65
        lines = []
        for j in range(0, len(text), max_chars_per_line):
            lines.append(text[j:j+max_chars_per_line])
        display_text = "\n".join(lines)

        # 使用 textbbox 计算边界
        bbox = draw.textbbox((0, 0), display_text, font=font, spacing=20)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (w - text_w) / 2
        y = (h - text_h) / 2

        # 画一个金色边框装饰
        margin = 80
        draw.rectangle([margin, margin, w - margin, h - margin], outline=(218, 165, 32), width=5)

        # 绘制文字（金色）
        draw.text((x, y), display_text, fill=(218, 165, 32), font=font, spacing=20, align="center")

        img.save(img_path)
        images.append(img_path)
        log(f"段落 {i} 本地配图生成成功：{img_path.name}")
    return images

# ─────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────

async def main():
    parser = argparse.ArgumentParser(description="产品介绍视频自动生成工具")
    parser.add_argument("--script", required=True, help="文案脚本文件路径（每行一段）")
    parser.add_argument("--images", default="", help="图片素材目录（非口播段落必须提供）")
    parser.add_argument("--output", default="output/product_video.mp4", help="输出视频路径")
    parser.add_argument("--voice", default="edge_tts", help="声音策略：myvoice 或 edge_tts")
    parser.add_argument("--edge-tts-gender", default="female", choices=["female", "male"],
                        help="edge-tts 声音性别：female（女声，默认）或 male（男声）")
    parser.add_argument("--lang", default="zh-CN", help="语言代码，如 zh-CN, en-US")
    parser.add_argument("--resolution", default="1920x1080", help="输出分辨率，如 1920x1080")
    parser.add_argument("--subtitle", default="soft", choices=["soft", "hard", "none"],
                        help="字幕类型：soft（软字幕，默认）、hard（硬字幕烧录）、none（无字幕）")
    parser.add_argument("--image-style", default="", 
                        help="生成图片的风格，例如：动漫、卡通、专业商务等。若为空则使用默认风格。")
    parser.add_argument("--scene-descriptions", default="",
                        help="场景描述文件路径（由 WorkBuddy 生成），每行一条场景描述，与文案段落一一对应。"
                             "若未提供则使用原始文案作为文生图 prompt")
    parser.add_argument("--clone-audio-url", default="",
                        help="使用 myvoice 时，用该公网音频URL进行声音复刻")
    parser.add_argument("--clone-audio-file", default="",
                        help="使用 myvoice 时，本地音频文件路径（自动转换为 data URI）")
    parser.add_argument("--clone-prefix", default="myvoice",
                        help="自动复刻时 create_voice 的 prefix")
    parser.add_argument("--clone-language", default="zh",
                        help="自动复刻时 language_hints，默认 zh")
    parser.add_argument("--portrait", default="",
                        help='真人口播照片路径（JPG/PNG），脚本首段含"口播："前缀时必须提供')
    parser.add_argument("--portrait-quality", default="standard", choices=["standard", "high"],
                        help="口播视频质量：standard (480P) 或 high (720P)")
    parser.add_argument("--portrait-prompt", default="人像保持 超写实，皮肤纹理清晰但平滑，零毛孔，肤色均匀，白皙透亮，无痘印雀斑，电影级布光，景深效果，8K分辨率，专业美容修图质感",
                        help="口播视频 prompt，仅 high 质量生效")
    parser.add_argument("--transitions", dest="transitions", action="store_true", default=True,
                        help="启用图片过渡特效（默认开启）")
    parser.add_argument("--no-transitions", dest="transitions", action="store_false",
                        help="禁用图片过渡特效（直接拼接）")
    args = parser.parse_args()

    # 解析场景描述文件（由 WorkBuddy 预生成）
    scene_descriptions = None
    if args.scene_descriptions:
        sd_path = Path(args.scene_descriptions)
        if sd_path.exists():
            with open(sd_path, "r", encoding="utf-8") as f:
                scene_descriptions = [line.strip() for line in f if line.strip()]
            log(f"从文件加载场景描述 {len(scene_descriptions)} 条：{args.scene_descriptions}", "OK")
        else:
            log(f"场景描述文件不存在：{args.scene_descriptions}，将使用原始文案", "WARN")

    # 解析分辨率
    w, h = map(int, args.resolution.lower().replace("x", "x").split("x"))
    resolution = (w, h)

    # 初始化输出目录（先清空旧文件，再重建）
    output_path = Path(args.output).resolve()
    output_dir = output_path.parent.resolve()

    # 安全检查：防止输出目录就是图片目录，避免误删图片
    # 注意：输出目录是图片目录的子目录（如 final/）是安全的，
    # 因为 rmtree 只清空子目录本身，不影响父目录的图片
    if args.images:
        images_dir = Path(args.images).resolve()
        if output_dir == images_dir:
            log(f"❌ 严重错误：输出目录与图片目录相同！", "ERR")
            log(f"   图片目录：{images_dir}", "ERR")
            log(f"   输出路径：{output_path}", "ERR")
            log(f"   如果继续，图片目录将被清空，所有图片会丢失！", "ERR")
            log(f"   请通过 --output 指定一个独立的输出目录，例如：", "ERR")
            log(f"     --output /path/to/output/video.mp4", "ERR")
            sys.exit(1)

    if output_dir.exists():
        import shutil
        shutil.rmtree(output_dir)
        log(f"已清空输出目录：{output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    audio_dir = output_path.parent / "audio"
    srt_path = output_path.with_suffix(".srt")

    log("═" * 50)
    log("🎬 产品介绍视频自动生成")
    log("═" * 50)

    # 1. 环境检查
    check_ffmpeg()
    log("ffmpeg 检查通过", "OK")

    # 2. 解析输入
    segments = parse_script(args.script)
    portrait_path = args.portrait.strip()
    portrait_text = detect_portrait_segment(segments[0]) if segments else None

    if portrait_text is not None:
        # ── 口播模式：首段使用真人照片 ──
        if not portrait_path:
            log('脚本第一段包含"口播："前缀，但未提供真人照片（--portrait）', "ERR")
            log("请通过 --portrait /path/to/photo.jpg 提供主持人照片后重新运行", "ERR")
            sys.exit(1)
        if not Path(portrait_path).exists():
            log(f"真人照片文件不存在：{portrait_path}", "ERR")
            sys.exit(1)
        segments[0] = portrait_text  # 去除"口播："前缀，保留纯文案
        non_portrait_segments = segments[1:]
        if non_portrait_segments:
            images = collect_images(args.images) if args.images else []
            if not images:
                log("未找到任何产品图片或未提供图片目录，将根据每段文案自动生成...")
                api_key = load_voice_config().get("api_key", "").strip() or os.environ.get("DASHSCOPE_API_KEY", "").strip()
                images = await generate_images_for_segments(
                    non_portrait_segments, args.resolution, api_key, output_path.parent / "images", args.image_style,
                    scene_descriptions=scene_descriptions
                )
            elif len(images) == len(non_portrait_segments):
                validate_inputs(non_portrait_segments, images)
            else:
                # 图片数量不匹配，尝试按文件名序号智能匹配
                log(f"图片数量（{len(images)}）与段落数量（{len(non_portrait_segments)}）不一致，尝试智能匹配...", "WARN")
                matched, matched_indices = match_images_to_segments(non_portrait_segments, images)
                if matched_indices:
                    log(f"智能匹配成功：{len(matched_indices)} 张已有图片命中，{len(non_portrait_segments) - len(matched_indices)} 张需生成")
                    api_key = load_voice_config().get("api_key", "").strip() or os.environ.get("DASHSCOPE_API_KEY", "").strip()
                    images = await fill_missing_images(
                        non_portrait_segments, matched, args.resolution, api_key,
                        output_path.parent / "images", args.image_style,
                        scene_descriptions=scene_descriptions,
                    )
                else:
                    log("无法按序号匹配任何已有图片，将根据每段文案全部自动生成...", "WARN")
                    api_key = load_voice_config().get("api_key", "").strip() or os.environ.get("DASHSCOPE_API_KEY", "").strip()
                    images = await generate_images_for_segments(
                        non_portrait_segments, args.resolution, api_key, output_path.parent / "images", args.image_style,
                        scene_descriptions=scene_descriptions
                    )
        else:
            images = []
        log(f"口播模式：第1段使用真人照片，后续 {len(non_portrait_segments)} 段使用图片", "OK")
    else:
        # ── 普通模式 ──
        images = collect_images(args.images) if args.images else []
        if not images:
            log("未找到任何产品图片或未提供图片目录，将根据每段文案自动生成...")
            api_key = load_voice_config().get("api_key", "").strip() or os.environ.get("DASHSCOPE_API_KEY", "").strip()
            images = await generate_images_for_segments(
                segments, args.resolution, api_key, output_path.parent / "images", args.image_style,
                scene_descriptions=scene_descriptions
            )
        elif len(images) == len(segments):
            validate_inputs(segments, images)
        else:
            log(f"图片数量（{len(images)}）与段落数量（{len(segments)}）不一致，尝试智能匹配...", "WARN")
            matched, matched_indices = match_images_to_segments(segments, images)
            if matched_indices:
                log(f"智能匹配成功：{len(matched_indices)} 张已有图片命中，{len(segments) - len(matched_indices)} 张需生成")
                api_key = load_voice_config().get("api_key", "").strip() or os.environ.get("DASHSCOPE_API_KEY", "").strip()
                images = await fill_missing_images(
                    segments, matched, args.resolution, api_key,
                    output_path.parent / "images", args.image_style,
                    scene_descriptions=scene_descriptions,
                )
            else:
                log("无法按序号匹配任何已有图片，将根据每段文案全部自动生成...", "WARN")
                api_key = load_voice_config().get("api_key", "").strip() or os.environ.get("DASHSCOPE_API_KEY", "").strip()
                images = await generate_images_for_segments(
                    segments, args.resolution, api_key, output_path.parent / "images", args.image_style,
                    scene_descriptions=scene_descriptions
                )
        log(f"共 {len(segments)} 段文案，{len(images)} 张图片", "OK")

    # 3. 确定 TTS 策略和 voice_id
    strategy = select_tts_strategy(args.voice)
    voice_id = ""  # 复刻声音 ID，仅在内存中使用，不写入配置文件

    requested_myvoice = bool(args.voice and "myvoice" in args.voice.lower())
    clone_audio_url = args.clone_audio_url.strip()
    if requested_myvoice and not clone_audio_url and args.clone_audio_file:
        log("检测到本地复刻音频，开始上传到平台 OSS...")
        clone_audio_url = build_audio_data_uri(args.clone_audio_file) or ""

    if requested_myvoice and clone_audio_url:
        # 有本地音频或公网URL，执行实时复刻
        log("开始自动执行声音复刻...")
        voice_id = enroll_my_voice(
            audio_url=clone_audio_url,
            prefix=args.clone_prefix,
            language=args.clone_language,
        ) or ""
        if not voice_id:
            strategy = "edge_tts"
    elif requested_myvoice:
        # 没有复刻音频，尝试从 voice_config.json 读取已保存的 voice_id
        saved_voice_id = load_voice_config().get("voice_id", "").strip()
        if saved_voice_id:
            log(f"从 voice_config.json 读取到已保存的 voice_id：{saved_voice_id}")
            voice_id = saved_voice_id
        else:
            log(
                '指定了"我的声音"，但未提供复刻音频且 voice_config.json 中无 voice_id。\n'
                '  请提供 --clone-audio-url 或 --clone-audio-file 参数来上传音频进行声音复刻，\n'
                '  或去掉 --voice myvoice 使用免费的 edge-tts 合成。',
                "WARN",
            )
            strategy = "edge_tts"

    log(f"TTS 策略：{'我的复刻声音' if strategy == 'myvoice' else 'edge-tts（免费）'}")

    # 4. 合成音频
    log("\n── 开始语音合成 ──")
    audio_paths = await synthesize_all_segments(
        segments, str(audio_dir), strategy, args.lang, voice_id, args.edge_tts_gender
    )
    log("语音合成完成", "OK")

    # 5. 获取时长，生成字幕（若需要）
    srt_content = None
    if args.subtitle != "none":
        log("\n── 生成字幕 ──")
        durations = [get_audio_duration(p) for p in audio_paths]
        srt_content = generate_srt(segments, durations, args.lang)
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_content)
        log(f"字幕文件已保存：{srt_path}", "OK")
    else:
        log("\n── 跳过字幕生成（--subtitle none）──")

    # 6. 合成视频片段
    log("\n── 合成视频片段 ──")
    with tempfile.TemporaryDirectory() as tmp_dir:
        segment_videos = []

        # ── 口播片段（首段）──
        if portrait_text is not None:
            portrait_audio = audio_paths[0]
            portrait_duration = get_audio_duration(portrait_audio)
            dashscope_key = load_voice_config().get("api_key", "").strip() or os.environ.get("DASHSCOPE_API_KEY", "").strip()
            portrait_seg_path = str(Path(tmp_dir) / "seg_001_portrait.mp4")
            portrait_done = False

            if portrait_duration > PORTRAIT_MAX_DURATION_SEC:
                log(
                    f"口播音频时长 {portrait_duration:.1f}s 超过 {PORTRAIT_MAX_DURATION_SEC}s 限制，"
                    "降级为图片视频",
                    "WARN",
                )
            elif not dashscope_key:
                log("未找到 DASHSCOPE_API_KEY，无法生成口播视频，降级为图片视频", "WARN")
            else:
                log(f"\n── 生成口播视频片段（音频时长 {portrait_duration:.1f}s）──")
                try:
                    portrait_done = await create_portrait_video(
                        portrait_path=portrait_path,
                        audio_path=portrait_audio,
                        output_path=portrait_seg_path,
                        api_key=dashscope_key,
                        quality=args.portrait_quality,
                        duration=portrait_duration,
                        prompt=args.portrait_prompt,
                    )
                except Exception as e:
                    log(f"口播视频生成失败：{e}，降级为图片视频", "WARN")

            if not portrait_done:
                log("使用真人照片合成普通图片视频（口播降级）")
                build_segment_video(portrait_path, portrait_audio, portrait_seg_path, resolution)
            else:
                # 口播视频分辨率通常与目标不一致，需重新编码统一
                reencoded = str(Path(tmp_dir) / "seg_001_reencoded.mp4")
                reencode_video(portrait_seg_path, reencoded, resolution)
                portrait_seg_path = reencoded

            segment_videos.append(portrait_seg_path)
            remaining_pairs = list(zip(images, audio_paths[1:]))
            start_idx = 2
        else:
            remaining_pairs = list(zip(images, audio_paths))
            start_idx = 1

        for i, (img, audio) in enumerate(remaining_pairs, start_idx):
            seg_out = str(Path(tmp_dir) / f"seg_{i:03d}.mp4")
            log(f"合成第 {i}/{len(segments)} 段视频片段...")
            build_segment_video(str(img), audio, seg_out, resolution)
            segment_videos.append(seg_out)

        # 7. 拼接所有片段
        log("\n── 拼接视频 ──")
        raw_video = str(Path(tmp_dir) / "raw_concat.mp4")
        # audio_durations 已在步骤5中计算（durations 变量）
        # audio_paths 是原始音频文件（不含 padding），传给 xfade 用于音频拼接
        concatenate_videos(segment_videos, raw_video, tmp_dir,
                          force_reencode=(portrait_text is not None),
                          use_transitions=args.transitions,
                          resolution=resolution,
                          audio_durations=durations,
                          original_audio_paths=audio_paths,
        )
        log("视频拼接完成", "OK")

        # 8. 嵌入字幕
        if args.subtitle == "none":
            log("\n── 无字幕模式，直接输出视频 ──")
            import shutil
            shutil.copy2(raw_video, str(output_path))
        elif args.subtitle == "hard":
            log("\n── 嵌入字幕（硬字幕烧录）──")
            burn_hard_subtitles(raw_video, str(srt_path), str(output_path))
        else:
            log("\n── 嵌入字幕（软字幕）──")
            embed_soft_subtitles(raw_video, str(srt_path), str(output_path))

    log("\n" + "═" * 50)
    log(f"🎉 视频生成完成！", "OK")
    log(f"   视频文件：{output_path}")
    log(f"   字幕文件：{srt_path}")
    log(f"   音频片段：{audio_dir}/")
    log("═" * 50)


if __name__ == "__main__":
    asyncio.run(main())
