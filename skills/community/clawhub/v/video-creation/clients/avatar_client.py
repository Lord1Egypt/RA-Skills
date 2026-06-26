from __future__ import annotations

import json
import os
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Optional

from clients.auth import get_token

API_BASE =  "https://open-api.chanjing.cc"

FILE_READY_STATUSES = {1}
FILE_FAILED_STATUSES = {98, 99, 100}


# =========================================================
# 通用请求层
# =========================================================
def _get_access_token() -> str:
    token, err = get_token()
    if err:
        raise RuntimeError(err)
    if not token:
        raise RuntimeError("未获取到 access_token")
    return token


def _json_request(
    url: str,
    *,
    method: str = "GET",
    data: Optional[dict[str, Any]] = None,
    headers: Optional[dict[str, str]] = None,
    timeout: int = 30,
) -> dict[str, Any]:
    req_headers = dict(headers or {})
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        req_headers.setdefault("Content-Type", "application/json")

    req = urllib.request.Request(
        url,
        data=body,
        headers=req_headers,
        method=method,
    )

    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw)


# =========================================================
# 字幕配置
# =========================================================
def validate_hex_color(value: Optional[str], arg_name: str) -> None:
    if value is None:
        return
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
        raise ValueError(f"{arg_name} 格式不正确，应为 #RRGGBB")


def get_default_subtitle_fields(
    screen_width: int = 1080,
    screen_height: int = 1920,
    resolution_rate: int = 0,
) -> dict[str, Any]:
    # 与外部 create_task.py 对齐：
    # 只有 4K 画布时才启用 4K 默认字幕参数。
    use_4k_defaults = (
        resolution_rate == 1 and screen_width >= 2160 and screen_height >= 3840
    )
    if use_4k_defaults:
        return {
            "x": 80,
            "y": 2840,
            "width": 2000,
            "height": 1000,
            "font_size": 150,
            "color": "#FFFFFF",
            "stroke_width": 7,
            "asr_type": 0,
        }

    return {
        "x": 31,
        "y": 1521,
        "width": 1000,
        "height": 200,
        "font_size": 64,
        "color": "#FFFFFF",
        "stroke_width": 7,
        "asr_type": 0,
    }


def build_subtitle_config(
    subtitle: Optional[str],
    *,
    screen_width: int = 1080,
    screen_height: int = 1920,
    resolution_rate: int = 0,
    subtitle_x: Optional[int] = None,
    subtitle_y: Optional[int] = None,
    subtitle_width: Optional[int] = None,
    subtitle_height: Optional[int] = None,
    subtitle_font_size: Optional[int] = None,
    subtitle_color: Optional[str] = None,
    subtitle_stroke_color: Optional[str] = None,
    subtitle_stroke_width: Optional[int] = None,
    subtitle_font_id: Optional[str] = None,
    subtitle_asr_type: Optional[int] = None,
) -> Optional[dict[str, Any]]:
    subtitle_fields = {
        "x": subtitle_x,
        "y": subtitle_y,
        "width": subtitle_width,
        "height": subtitle_height,
        "font_size": subtitle_font_size,
        "color": subtitle_color,
        "stroke_color": subtitle_stroke_color,
        "stroke_width": subtitle_stroke_width,
        "font_id": subtitle_font_id,
        "asr_type": subtitle_asr_type,
    }
    has_style_fields = any(v is not None for v in subtitle_fields.values())

    if subtitle is None:
        if has_style_fields:
            raise ValueError("传字幕位置或样式参数时，必须同时设置 subtitle='show'")
        return None

    if subtitle not in ("show", "hide"):
        raise ValueError("subtitle 只能是 'show' 或 'hide'")

    if subtitle == "hide":
        if has_style_fields:
            raise ValueError("subtitle='hide' 时，不能同时传字幕位置或样式参数")
        return {"show": False}

    validate_hex_color(subtitle_color, "subtitle_color")
    validate_hex_color(subtitle_stroke_color, "subtitle_stroke_color")

    config: dict[str, Any] = {"show": True}
    config.update(
        get_default_subtitle_fields(
            screen_width=screen_width,
            screen_height=screen_height,
            resolution_rate=resolution_rate,
        )
    )

    for key, value in subtitle_fields.items():
        if value is not None:
            config[key] = value

    if config["width"] > screen_width:
        raise ValueError("字幕宽度不能超过屏幕宽度")
    if config["height"] > screen_height:
        raise ValueError("字幕高度不能超过屏幕高度")
    if config["x"] + config["width"] > screen_width:
        raise ValueError("字幕区域超出屏幕宽度")
    if config["y"] + config["height"] > screen_height:
        raise ValueError("字幕区域超出屏幕高度")

    return config


# =========================================================
# create_video 请求体构造
# =========================================================
def _build_person(
    person_id: str,
    *,
    person_x: int = 0,
    person_y: int = 0,
    person_width: int = 1080,
    person_height: int = 1920,
    figure_type: Optional[str] = None,
) -> dict[str, Any]:
    person: dict[str, Any] = {
        "id": person_id,
        "x": person_x,
        "y": person_y,
        "width": person_width,
        "height": person_height,
    }
    if figure_type:
        person["figure_type"] = figure_type
    return person


def _maybe_attach_bg(
    body: dict[str, Any],
    *,
    bg_file_id: Optional[str] = None,
    bg_src_url: Optional[str] = None,
    bg_x: int = 0,
    bg_y: int = 0,
    bg_width: int = 1080,
    bg_height: int = 1920,
) -> None:
    if not bg_file_id and not bg_src_url:
        return

    bg: dict[str, Any] = {
        "x": bg_x,
        "y": bg_y,
        "width": bg_width,
        "height": bg_height,
    }
    if bg_file_id:
        bg["file_id"] = bg_file_id
    if bg_src_url:
        bg["src_url"] = bg_src_url
    body["bg"] = bg


def build_audio_driven_video_body(
    person_id: str,
    *,
    audio_file_id: Optional[str] = None,
    wav_url: Optional[str] = None,
    figure_type: Optional[str] = None,
    subtitle: Optional[str] = "hide",
    subtitle_x: Optional[int] = None,
    subtitle_y: Optional[int] = None,
    subtitle_width: Optional[int] = None,
    subtitle_height: Optional[int] = None,
    subtitle_font_size: Optional[int] = None,
    subtitle_color: Optional[str] = None,
    subtitle_stroke_color: Optional[str] = None,
    subtitle_stroke_width: Optional[int] = None,
    subtitle_font_id: Optional[str] = None,
    subtitle_asr_type: Optional[int] = None,
    person_x: int = 0,
    person_y: int = 0,
    person_width: int = 1080,
    person_height: int = 1920,
    screen_width: int = 1080,
    screen_height: int = 1920,
    model: int = 0,
    resolution_rate: int = 0,
    bg_color: str = "#EDEDED",
    bg_file_id: Optional[str] = None,
    bg_src_url: Optional[str] = None,
    bg_x: int = 0,
    bg_y: int = 0,
    bg_width: int = 1080,
    bg_height: int = 1920,
    volume: int = 100,
    language: str = "cn",
    backway: int = 1,
    drive_mode: Optional[str] = None,
    callback: Optional[str] = None,
    rgba_mode: bool = False,
    add_compliance_watermark: bool = False,
    compliance_watermark_position: int = 0,
) -> dict[str, Any]:
    if audio_file_id and wav_url:
        raise ValueError("audio_file_id 和 wav_url 只能二选一")
    if not audio_file_id and not wav_url:
        raise ValueError("音频驱动必须提供 audio_file_id 或 wav_url")

    person = _build_person(
        person_id,
        person_x=person_x,
        person_y=person_y,
        person_width=person_width,
        person_height=person_height,
        figure_type=figure_type,
    )

    audio: dict[str, Any] = {
        "type": "audio",
        "volume": volume,
        "language": language,
    }
    if audio_file_id:
        audio["file_id"] = audio_file_id
    if wav_url:
        audio["wav_url"] = wav_url

    body: dict[str, Any] = {
        "person": person,
        "audio": audio,
        "bg_color": bg_color,
        "screen_width": screen_width,
        "screen_height": screen_height,
        "model": model,
        "backway": backway,
        "add_compliance_watermark": add_compliance_watermark,
        "compliance_watermark_position": compliance_watermark_position,
        "resolution_rate": resolution_rate,
    }

    if drive_mode:
        body["drive_mode"] = drive_mode
    if callback:
        body["callback"] = callback
    if rgba_mode:
        body["is_rgba_mode"] = True

    subtitle_config = build_subtitle_config(
        subtitle,
        screen_width=screen_width,
        screen_height=screen_height,
        resolution_rate=resolution_rate,
        subtitle_x=subtitle_x,
        subtitle_y=subtitle_y,
        subtitle_width=subtitle_width,
        subtitle_height=subtitle_height,
        subtitle_font_size=subtitle_font_size,
        subtitle_color=subtitle_color,
        subtitle_stroke_color=subtitle_stroke_color,
        subtitle_stroke_width=subtitle_stroke_width,
        subtitle_font_id=subtitle_font_id,
        subtitle_asr_type=subtitle_asr_type,
    )
    if subtitle_config is not None:
        body["subtitle_config"] = subtitle_config

    _maybe_attach_bg(
        body,
        bg_file_id=bg_file_id,
        bg_src_url=bg_src_url,
        bg_x=bg_x,
        bg_y=bg_y,
        bg_width=bg_width,
        bg_height=bg_height,
    )

    return body


def build_text_driven_video_body(
    person_id: str,
    *,
    text: str,
    audio_man: str,
    speed: float = 1.0,
    pitch: float = 1.0,
    figure_type: Optional[str] = None,
    subtitle: Optional[str] = "hide",
    subtitle_x: Optional[int] = None,
    subtitle_y: Optional[int] = None,
    subtitle_width: Optional[int] = None,
    subtitle_height: Optional[int] = None,
    subtitle_font_size: Optional[int] = None,
    subtitle_color: Optional[str] = None,
    subtitle_stroke_color: Optional[str] = None,
    subtitle_stroke_width: Optional[int] = None,
    subtitle_font_id: Optional[str] = None,
    subtitle_asr_type: Optional[int] = None,
    person_x: int = 0,
    person_y: int = 0,
    person_width: int = 1080,
    person_height: int = 1920,
    screen_width: int = 1080,
    screen_height: int = 1920,
    model: int = 0,
    resolution_rate: int = 0,
    bg_color: str = "#EDEDED",
    bg_file_id: Optional[str] = None,
    bg_src_url: Optional[str] = None,
    bg_x: int = 0,
    bg_y: int = 0,
    bg_width: int = 1080,
    bg_height: int = 1920,
    volume: int = 100,
    language: str = "cn",
    backway: int = 1,
    drive_mode: Optional[str] = None,
    callback: Optional[str] = None,
    rgba_mode: bool = False,
    add_compliance_watermark: bool = False,
    compliance_watermark_position: int = 0,
) -> dict[str, Any]:
    if not text:
        raise ValueError("文本驱动必须提供 text")
    if not audio_man:
        raise ValueError("文本驱动必须提供 audio_man")
    if len(text) > 4000:
        raise ValueError("文本长度不能超过 4000 字符")

    person = _build_person(
        person_id,
        person_x=person_x,
        person_y=person_y,
        person_width=person_width,
        person_height=person_height,
        figure_type=figure_type,
    )

    audio: dict[str, Any] = {
        "type": "tts",
        "volume": volume,
        "language": language,
        "tts": {
            "text": [text],
            "speed": speed,
            "audio_man": audio_man,
            "pitch": pitch,
        },
    }

    body: dict[str, Any] = {
        "person": person,
        "audio": audio,
        "bg_color": bg_color,
        "screen_width": screen_width,
        "screen_height": screen_height,
        "model": model,
        "backway": backway,
        "add_compliance_watermark": add_compliance_watermark,
        "compliance_watermark_position": compliance_watermark_position,
        "resolution_rate": resolution_rate,
    }

    if drive_mode:
        body["drive_mode"] = drive_mode
    if callback:
        body["callback"] = callback
    if rgba_mode:
        body["is_rgba_mode"] = True

    subtitle_config = build_subtitle_config(
        subtitle,
        screen_width=screen_width,
        screen_height=screen_height,
        resolution_rate=resolution_rate,
        subtitle_x=subtitle_x,
        subtitle_y=subtitle_y,
        subtitle_width=subtitle_width,
        subtitle_height=subtitle_height,
        subtitle_font_size=subtitle_font_size,
        subtitle_color=subtitle_color,
        subtitle_stroke_color=subtitle_stroke_color,
        subtitle_stroke_width=subtitle_stroke_width,
        subtitle_font_id=subtitle_font_id,
        subtitle_asr_type=subtitle_asr_type,
    )
    if subtitle_config is not None:
        body["subtitle_config"] = subtitle_config

    _maybe_attach_bg(
        body,
        bg_file_id=bg_file_id,
        bg_src_url=bg_src_url,
        bg_x=bg_x,
        bg_y=bg_y,
        bg_width=bg_width,
        bg_height=bg_height,
    )

    return body


# =========================================================
# 1️⃣ 创建视频任务（底层）
# =========================================================
def create_video_task(body: dict[str, Any]) -> str:
    token = _get_access_token()

    url = f"{API_BASE}/open/v1/create_video"
    res = _json_request(
        url,
        method="POST",
        data=body,
        headers={"access_token": token},
        timeout=30,
    )

    if res.get("code") != 0:
        raise RuntimeError(res.get("msg", res))

    video_id = res.get("data")
    if not video_id:
        raise RuntimeError("响应无 video_id")

    return str(video_id)


# =========================================================
# 2️⃣ 上层创建封装
# =========================================================
def create_audio_driven_video_task(
    person_id: str,
    *,
    audio_file_id: Optional[str] = None,
    wav_url: Optional[str] = None,
    figure_type: Optional[str] = None,
    subtitle: Optional[str] = "hide",
    subtitle_x: Optional[int] = None,
    subtitle_y: Optional[int] = None,
    subtitle_width: Optional[int] = None,
    subtitle_height: Optional[int] = None,
    subtitle_font_size: Optional[int] = None,
    subtitle_color: Optional[str] = None,
    subtitle_stroke_color: Optional[str] = None,
    subtitle_stroke_width: Optional[int] = None,
    subtitle_font_id: Optional[str] = None,
    subtitle_asr_type: Optional[int] = None,
    person_x: int = 0,
    person_y: int = 0,
    person_width: int = 1080,
    person_height: int = 1920,
    screen_width: int = 1080,
    screen_height: int = 1920,
    model: int = 0,
    resolution_rate: int = 0,
    bg_color: str = "#EDEDED",
    bg_file_id: Optional[str] = None,
    bg_src_url: Optional[str] = None,
    bg_x: int = 0,
    bg_y: int = 0,
    bg_width: int = 1080,
    bg_height: int = 1920,
    volume: int = 100,
    language: str = "cn",
    backway: int = 1,
    drive_mode: Optional[str] = None,
    callback: Optional[str] = None,
    rgba_mode: bool = False,
    add_compliance_watermark: bool = False,
    compliance_watermark_position: int = 0,
) -> str:
    body = build_audio_driven_video_body(
        person_id=person_id,
        audio_file_id=audio_file_id,
        wav_url=wav_url,
        figure_type=figure_type,
        subtitle=subtitle,
        subtitle_x=subtitle_x,
        subtitle_y=subtitle_y,
        subtitle_width=subtitle_width,
        subtitle_height=subtitle_height,
        subtitle_font_size=subtitle_font_size,
        subtitle_color=subtitle_color,
        subtitle_stroke_color=subtitle_stroke_color,
        subtitle_stroke_width=subtitle_stroke_width,
        subtitle_font_id=subtitle_font_id,
        subtitle_asr_type=subtitle_asr_type,
        person_x=person_x,
        person_y=person_y,
        person_width=person_width,
        person_height=person_height,
        screen_width=screen_width,
        screen_height=screen_height,
        model=model,
        resolution_rate=resolution_rate,
        bg_color=bg_color,
        bg_file_id=bg_file_id,
        bg_src_url=bg_src_url,
        bg_x=bg_x,
        bg_y=bg_y,
        bg_width=bg_width,
        bg_height=bg_height,
        volume=volume,
        language=language,
        backway=backway,
        drive_mode=drive_mode,
        callback=callback,
        rgba_mode=rgba_mode,
        add_compliance_watermark=add_compliance_watermark,
        compliance_watermark_position=compliance_watermark_position,
    )
    return create_video_task(body)


def create_text_driven_video_task(
    person_id: str,
    *,
    text: str,
    audio_man: str,
    speed: float = 1.0,
    pitch: float = 1.0,
    figure_type: Optional[str] = None,
    subtitle: Optional[str] = "hide",
    subtitle_x: Optional[int] = None,
    subtitle_y: Optional[int] = None,
    subtitle_width: Optional[int] = None,
    subtitle_height: Optional[int] = None,
    subtitle_font_size: Optional[int] = None,
    subtitle_color: Optional[str] = None,
    subtitle_stroke_color: Optional[str] = None,
    subtitle_stroke_width: Optional[int] = None,
    subtitle_font_id: Optional[str] = None,
    subtitle_asr_type: Optional[int] = None,
    person_x: int = 0,
    person_y: int = 0,
    person_width: int = 1080,
    person_height: int = 1920,
    screen_width: int = 1080,
    screen_height: int = 1920,
    model: int = 0,
    resolution_rate: int = 0,
    bg_color: str = "#EDEDED",
    bg_file_id: Optional[str] = None,
    bg_src_url: Optional[str] = None,
    bg_x: int = 0,
    bg_y: int = 0,
    bg_width: int = 1080,
    bg_height: int = 1920,
    volume: int = 100,
    language: str = "cn",
    backway: int = 1,
    drive_mode: Optional[str] = None,
    callback: Optional[str] = None,
    rgba_mode: bool = False,
    add_compliance_watermark: bool = False,
    compliance_watermark_position: int = 0,
) -> str:
    body = build_text_driven_video_body(
        person_id=person_id,
        text=text,
        audio_man=audio_man,
        speed=speed,
        pitch=pitch,
        figure_type=figure_type,
        subtitle=subtitle,
        subtitle_x=subtitle_x,
        subtitle_y=subtitle_y,
        subtitle_width=subtitle_width,
        subtitle_height=subtitle_height,
        subtitle_font_size=subtitle_font_size,
        subtitle_color=subtitle_color,
        subtitle_stroke_color=subtitle_stroke_color,
        subtitle_stroke_width=subtitle_stroke_width,
        subtitle_font_id=subtitle_font_id,
        subtitle_asr_type=subtitle_asr_type,
        person_x=person_x,
        person_y=person_y,
        person_width=person_width,
        person_height=person_height,
        screen_width=screen_width,
        screen_height=screen_height,
        model=model,
        resolution_rate=resolution_rate,
        bg_color=bg_color,
        bg_file_id=bg_file_id,
        bg_src_url=bg_src_url,
        bg_x=bg_x,
        bg_y=bg_y,
        bg_width=bg_width,
        bg_height=bg_height,
        volume=volume,
        language=language,
        backway=backway,
        drive_mode=drive_mode,
        callback=callback,
        rgba_mode=rgba_mode,
        add_compliance_watermark=add_compliance_watermark,
        compliance_watermark_position=compliance_watermark_position,
    )
    return create_video_task(body)


# =========================================================
# 3️⃣ 轮询视频任务
# =========================================================
def get_video_task_detail(video_id: str) -> dict[str, Any]:
    token = _get_access_token()
    url = f"{API_BASE}/open/v1/video?id={urllib.parse.quote(video_id)}"

    body = _json_request(
        url,
        method="GET",
        headers={"access_token": token},
        timeout=30,
    )

    if body.get("code") != 0:
        raise RuntimeError(body.get("msg", body))

    data = body.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("video 查询响应缺少 data")
    return data


def poll_video_task(video_id: str, interval: int = 10, timeout: int = 1800) -> dict[str, Any]:
    start = time.monotonic()

    while True:
        if time.monotonic() - start > timeout:
            raise TimeoutError("视频任务超时")

        data = get_video_task_detail(video_id)
        status = data.get("status")

        if status == 30:
            return data

        if isinstance(status, int) and status >= 40:
            raise RuntimeError(data.get("msg") or f"status={status}")

        time.sleep(interval)


def poll_video_task_url(video_id: str, interval: int = 10, timeout: int = 1800) -> str:
    data = poll_video_task(video_id, interval=interval, timeout=timeout)
    video_url = data.get("video_url")
    if not video_url:
        raise RuntimeError("任务成功但无 video_url")
    return str(video_url)


# =========================================================
# 4️⃣ 上传文件
# =========================================================
def create_upload_url(service: str, filename: str) -> dict[str, Any]:
    token = _get_access_token()

    qs = urllib.parse.urlencode(
        {
            "service": service,
            "name": filename,
        }
    )
    url = f"{API_BASE}/open/v1/common/create_upload_url?{qs}"

    body = _json_request(
        url,
        method="GET",
        headers={"access_token": token},
        timeout=30,
    )

    if body.get("code") != 0:
        raise RuntimeError(body.get("msg", body))

    data = body.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("create_upload_url 响应缺少 data")
    return data


def upload_to_oss(sign_url: str, file_path: Path, mime_type: str) -> None:
    with open(file_path, "rb") as f:
        content = f.read()

    req = urllib.request.Request(
        sign_url,
        data=content,
        headers={"Content-Type": mime_type},
        method="PUT",
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        if resp.status not in (200, 204):
            raise RuntimeError(f"上传失败 status={resp.status}")


def get_file_detail(file_id: str) -> dict[str, Any]:
    token = _get_access_token()
    url = f"{API_BASE}/open/v1/common/file_detail?id={urllib.parse.quote(file_id)}"

    body = _json_request(
        url,
        method="GET",
        headers={"access_token": token},
        timeout=30,
    )

    if body.get("code") != 0:
        raise RuntimeError(body.get("msg", body))

    data = body.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("file_detail 响应缺少 data")
    return data


def poll_file_ready(file_id: str, interval: int = 5, timeout: int = 300) -> bool:
    start = time.monotonic()

    while time.monotonic() - start < timeout:
        data = get_file_detail(file_id)
        status = data.get("status")

        if status in FILE_READY_STATUSES:
            return True

        if status in FILE_FAILED_STATUSES:
            raise RuntimeError(data.get("msg") or f"文件处理失败 status={status}")

        time.sleep(interval)

    raise TimeoutError("文件处理超时")


def upload_file(file_path: str, service: str) -> str:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(file_path)

    data = create_upload_url(service, path.name)

    sign_url = data.get("sign_url")
    file_id = data.get("file_id")
    mime_type = data.get("mime_type", "application/octet-stream")

    if not sign_url or not file_id:
        raise RuntimeError("响应缺少 sign_url 或 file_id")

    upload_to_oss(str(sign_url), path, str(mime_type))
    poll_file_ready(str(file_id))

    return str(file_id)


# =========================================================
# 5️⃣ 下载视频
# =========================================================
def download_video(url: str, output_path: str) -> str:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "chanjing-video-compose-client"},
        method="GET",
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        with open(output, "wb") as f:
            f.write(resp.read())

    if not output.exists() or output.stat().st_size == 0:
        raise RuntimeError("下载失败：文件为空")

    return str(output)

def list_figures(
    source: str = "customised",
    page: int = 1,
    page_size: int = 20,
) -> dict[str, Any]:
    token = _get_access_token()

    if source == "customised":
        req = urllib.request.Request(
            f"{API_BASE}/open/v1/list_customised_person",
            data=json.dumps({"page": page, "page_size": page_size}).encode("utf-8"),
            headers={
                "access_token": token,
                "Content-Type": "application/json",
            },
            method="POST",
        )
    elif source == "common":
        params = urllib.parse.urlencode({"page": page, "size": page_size})
        req = urllib.request.Request(
            f"{API_BASE}/open/v1/list_common_dp?{params}",
            headers={
                "access_token": token,
                "Content-Type": "application/json",
            },
            method="GET",
        )
    else:
        raise ValueError("source 只能是 'customised' 或 'common'")

    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode("utf-8"))

    if body.get("code") != 0:
        raise RuntimeError(body.get("msg", body))

    data = body.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("list_figures 响应缺少 data")

    return {
        "source": source,
        "data": data,
    }


def build_figure_rows(source: str, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    if source == "customised":
        for item in items:
            width = item.get("width")
            height = item.get("height")
            size = f"{width}x{height}" if width and height else "-"
            rows.append(
                {
                    "source": "customised",
                    "person_id": item.get("id", ""),
                    "name": item.get("name", ""),
                    "figure_type": "-",
                    "size": size,
                    "audio_man_id": item.get("audio_man_id", ""),
                    "note": f"support_4k={item.get('support_4k', '')}",
                    "preview_url": item.get("preview_url", ""),
                }
            )
        return rows

    for item in items:
        for figure in item.get("figures", []):
            rows.append(
                {
                    "source": "common",
                    "person_id": item.get("id", ""),
                    "name": item.get("name", ""),
                    "figure_type": figure.get("type", ""),
                    "size": f"{figure.get('width', '')}x{figure.get('height', '')}",
                    "audio_man_id": item.get("audio_man_id", ""),
                    "note": f"audio_name={item.get('audio_name', '')}",
                    "preview_url": figure.get("preview_video_url", ""),
                }
            )
    return rows


def first_common_person_figure(payload: dict[str, Any]) -> tuple[str, str]:
    data = payload.get("data") or {}
    items = data.get("list") or []
    for item in items:
        pid = str(item.get("id", "")).strip()
        figures = item.get("figures") or []
        for fig in figures:
            ft = str(fig.get("type", "")).strip()
            if pid and ft:
                return pid, ft
        if pid and figures:
            ft0 = str(figures[0].get("type", "") or "sit_body").strip()
            return pid, ft0 or "sit_body"
    raise RuntimeError("list_figures(source='common') 返回列表为空")