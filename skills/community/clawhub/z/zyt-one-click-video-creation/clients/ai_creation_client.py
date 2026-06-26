from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Optional

from clients.auth import clear_cached_token, get_token, is_token_invalid

API_BASE = os.environ.get("CHANJING_API_BASE", "https://open-api.chanjing.cc")

RUNNING_STATUSES = {"Queued", "Ready", "Generating"}
SUCCESS_STATUSES = {"Success"}
FAILED_STATUSES = {"Error", "Fail"}


def _get_access_token() -> str:
    token, err = get_token()
    if err:
        raise RuntimeError(err)
    if not token:
        raise RuntimeError("未获取到 access_token")
    return token


def _json_get(
    path: str,
    *,
    query: Optional[dict[str, Any]] = None,
    timeout: int = 30,
) -> dict[str, Any]:
    suffix = ""
    if query:
        suffix = "?" + urllib.parse.urlencode(query, doseq=True)
    token = _get_access_token()

    def _once(current_token: str) -> dict[str, Any]:
        req = urllib.request.Request(
            f"{API_BASE}{path}{suffix}",
            headers={"access_token": current_token},
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    body = _once(token)
    if is_token_invalid(body):
        clear_cached_token()
        refreshed, err = get_token(force_refresh=True)
        if err or not refreshed:
            raise RuntimeError(err or "刷新 access_token 失败")
        body = _once(str(refreshed))

    if body.get("code") != 0:
        raise RuntimeError(body.get("msg", body))

    data = body.get("data")
    if data is None:
        raise RuntimeError("响应缺少 data")
    return data


def _json_post(
    path: str,
    payload: dict[str, Any],
    *,
    timeout: int = 30,
) -> dict[str, Any] | str:
    token = _get_access_token()

    def _once(current_token: str) -> dict[str, Any]:
        req = urllib.request.Request(
            f"{API_BASE}{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"access_token": current_token, "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    body = _once(token)
    if is_token_invalid(body):
        clear_cached_token()
        refreshed, err = get_token(force_refresh=True)
        if err or not refreshed:
            raise RuntimeError(err or "刷新 access_token 失败")
        body = _once(str(refreshed))

    if body.get("code") != 0:
        raise RuntimeError(body.get("msg", body))

    return body.get("data")


def first_output_url(data: dict[str, Any]) -> Optional[str]:
    urls = (data or {}).get("output_url") or []
    if isinstance(urls, list) and urls:
        return str(urls[0])
    return None


def submit_ai_creation_task(body: dict[str, Any]) -> str:
    data = _json_post("/open/v1/ai_creation/task/submit", body)
    if not data:
        raise RuntimeError("响应无任务 unique_id")
    return str(data)


def build_video_generation_body(
    *,
    model_code: str,
    prompt: str,
    aspect_ratio: Optional[str] = None,
    clarity: Optional[int] = None,
    video_duration: Optional[int] = None,
    style: Optional[str] = None,
    callback: Optional[str] = None,
    ref_img_url: Optional[list[str]] = None,
    quality_mode: Optional[str] = None,
) -> dict[str, Any]:
    if not model_code:
        raise ValueError("缺少 model_code")
    if not prompt:
        raise ValueError("缺少 prompt")

    body: dict[str, Any] = {
        "creation_type": 4,
        "model_code": model_code,
        "ref_prompt": prompt,
    }

    if aspect_ratio:
        body["aspect_ratio"] = aspect_ratio
    if clarity is not None:
        body["clarity"] = clarity
    if video_duration is not None:
        body["video_duration"] = video_duration
    if style:
        body["style"] = style
    if callback:
        body["callback"] = callback
    if quality_mode:
        body["quality_mode"] = quality_mode
    if ref_img_url:
        body["ref_img_url"] = ref_img_url

    return body


def submit_video_generation_task(
    *,
    model_code: str,
    prompt: str,
    aspect_ratio: Optional[str] = None,
    clarity: Optional[int] = None,
    video_duration: Optional[int] = None,
    style: Optional[str] = None,
    callback: Optional[str] = None,
    ref_img_url: Optional[list[str]] = None,
    quality_mode: Optional[str] = None,
) -> str:
    body = build_video_generation_body(
        model_code=model_code,
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        clarity=clarity,
        video_duration=video_duration,
        style=style,
        callback=callback,
        ref_img_url=ref_img_url,
        quality_mode=quality_mode,
    )
    return submit_ai_creation_task(body)


def get_ai_creation_task(unique_id: str) -> dict[str, Any]:
    return _json_get(
        "/open/v1/ai_creation/task",
        query={"unique_id": unique_id},
        timeout=30,
    )


def poll_ai_creation_task(
    unique_id: str,
    *,
    interval: int = 10,
    timeout: int = 1800,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        data = get_ai_creation_task(unique_id)
        status = data.get("progress_desc")

        if status in SUCCESS_STATUSES:
            return data

        if status in FAILED_STATUSES:
            raise RuntimeError(f"任务失败: {data.get('err_msg') or status}")

        if status not in RUNNING_STATUSES:
            raise RuntimeError(f"未知任务状态: {status}")

        time.sleep(interval)

    raise TimeoutError("轮询超时")


def poll_ai_creation_task_url(
    unique_id: str,
    *,
    interval: int = 10,
    timeout: int = 1800,
) -> str:
    data = poll_ai_creation_task(unique_id, interval=interval, timeout=timeout)
    url = first_output_url(data)
    if not url:
        raise RuntimeError("任务成功但无 output_url")
    return url


def download_ai_creation_result(url: str, output_path: str) -> str:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "chanjing-ai-creation-client"},
        method="GET",
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        with open(output, "wb") as handle:
            handle.write(resp.read())

    if not output.exists() or output.stat().st_size == 0:
        raise RuntimeError("下载失败: 输出文件为空")

    return str(output)