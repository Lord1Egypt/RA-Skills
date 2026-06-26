import json
import os
import time
import urllib.parse
import urllib.request
from typing import Any

from clients.auth import get_token

API_BASE =  "https://open-api.chanjing.cc"


def create_tts_task(
    text: str,
    audio_man: str,
    speed: float = 1,
    pitch: float = 1,
    aigc_watermark: bool = False,
) -> str:
    if len(text) > 4000:
        raise ValueError("文本长度不能超过 4000 字符")

    body = {
        "audio_man": audio_man.strip(),
        "speed": speed,
        "pitch": pitch,
        "text": {"text": text},
        "aigc_watermark": aigc_watermark,
    }

    token, err = get_token()
    if err:
        raise RuntimeError(err)

    url = f"{API_BASE}/open/v1/create_audio_task"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "access_token": token,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode("utf-8"))

    if res.get("code") != 0:
        raise RuntimeError(res.get("msg", res))

    data = res.get("data") or {}
    task_id = data.get("task_id")
    if not task_id:
        raise RuntimeError("响应无 task_id")

    return str(task_id)


def poll_tts_task_full(task_id: str, interval: int = 3, timeout: int = 300) -> dict[str, Any]:
    url = f"{API_BASE}/open/v1/audio_task_state"
    body = json.dumps({"task_id": task_id}).encode("utf-8")
    start = time.monotonic()

    while True:
        if time.monotonic() - start > timeout:
            raise TimeoutError("TTS任务超时")

        token, err = get_token()
        if err:
            raise RuntimeError(err)

        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "access_token": token,
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            res = json.loads(resp.read().decode("utf-8"))

        if res.get("code") != 0:
            raise RuntimeError(res.get("msg", res))

        data = res.get("data") or {}
        status = data.get("status")

        if status == 9:
            return data

        if status not in (1, None):
            err_msg = data.get("errMsg") or data.get("errReason") or f"status={status}"
            raise RuntimeError(f"TTS任务失败: {err_msg}")

        time.sleep(interval)


def generate_audio_with_meta(text: str, audio_man: str) -> dict[str, Any]:
    task_id = create_tts_task(text, audio_man)
    return poll_tts_task_full(task_id)


def list_voices(page: int = 1, size: int = 100) -> dict[str, Any]:
    token, err = get_token()
    if err:
        raise RuntimeError(err)

    qs = urllib.parse.urlencode({"page": page, "size": size})
    url = f"{API_BASE}/open/v1/list_common_audio?{qs}"
    req = urllib.request.Request(
        url,
        headers={"access_token": token},
        method="GET",
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode("utf-8"))

    if body.get("code") != 0:
        raise RuntimeError(body.get("msg", body))

    data = body.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("list_voices 响应缺少 data")
    return data


def first_voice_id(data: dict[str, Any]) -> str:
    for v in data.get("list") or []:
        vid = str(v.get("id", "")).strip()
        if vid:
            return vid
    raise RuntimeError("list_voices 返回列表为空或无 id")