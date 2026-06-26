from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from uuid import uuid4

logger = logging.getLogger("tianpuyue")


def log_params(event: str, **kwargs: Any) -> None:
    """Log an event with a provider prefix and JSON payload."""
    params_str = json.dumps(kwargs, ensure_ascii=False, default=str)
    logger.info("天谱乐 - %s | %s", event, params_str)


_trace_id: str = ""


def generate_trace_id() -> str:
    return uuid4().hex


def get_trace_id() -> str:
    global _trace_id
    if not _trace_id:
        _trace_id = generate_trace_id()
    return _trace_id


class _TraceIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = get_trace_id()
        return True


OUTPUT_ROOT = Path(os.environ.get("OUTPUT_ROOT", "~/")).expanduser().resolve()
BASE_URL = "https://api.tianpuyue.cn"
DEFAULT_OUTPUT_DIR = OUTPUT_ROOT / "outputs" / "tianpuyue"
LOG_DIR = OUTPUT_ROOT / "outputs" / "logs"


def setup_logging() -> None:
    if logger.handlers:
        return
    trace_filter = _TraceIdFilter()
    log_fmt = "%(asctime)s [%(trace_id)s] %(levelname)s %(message)s"
    fmt = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    file_handler = logging.FileHandler(LOG_DIR / f"{today}.log", encoding="utf-8")
    file_handler.setFormatter(fmt)
    file_handler.addFilter(trace_filter)
    logger.addHandler(file_handler)
    error_handler = logging.FileHandler(LOG_DIR / f"{today}.error.log", encoding="utf-8")
    error_handler.setFormatter(fmt)
    error_handler.addFilter(trace_filter)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)
    logger.setLevel(logging.INFO)

DUMMY_CALLBACK_URL = "https://example.com/callback"


def load_api_key() -> str:
    api_key = os.getenv("TIANPUYUE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("未设置环境变量 TIANPUYUE_API_KEY")
    return api_key


def get_callback_url() -> str:
    return os.getenv("TIANPUYUE_CALLBACK_URL", DUMMY_CALLBACK_URL).strip()


def auth_header() -> dict[str, str]:
    return {"Authorization": load_api_key()}


def ensure_output_dir() -> Path:
    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return DEFAULT_OUTPUT_DIR


def ensure_scene_output_dir(scene: str) -> Path:
    target_dir = ensure_output_dir() / scene
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def _open_request(request: Request) -> dict[str, Any]:
    try:
        with urlopen(request) as response:
            body = response.read().decode("utf-8")
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"接口请求失败: HTTP {exc.code}, body={error_body}") from exc
    return json.loads(body)


def post_json(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    headers = auth_header()
    headers["Content-Type"] = "application/json"
    request = Request(
        f"{BASE_URL}{path}",
        data=data,
        headers=headers,
        method="POST",
    )
    return _open_request(request)


def ensure_success(response: dict[str, Any], context: str) -> dict[str, Any]:
    code = response.get("status")
    if code != 200000:
        raise RuntimeError(f"{context}失败: {json.dumps(response, ensure_ascii=False)}")
    return response


# --- 纯音乐 ---

def create_music_task(*, prompt: str, model: str) -> dict[str, Any]:
    payload = {
        "prompt": prompt,
        "model": model,
        "callback_url": get_callback_url(),
    }
    resp = ensure_success(post_json("/open-apis/v1/instrumental/generate", payload), "纯音乐生成")
    item_ids = resp.get("data", {}).get("item_ids", [])
    if not item_ids:
        raise RuntimeError(f"纯音乐生成未返回 item_id: {json.dumps(resp, ensure_ascii=False)}")
    return resp


def query_music_task(item_id: str) -> dict[str, Any]:
    payload = {"item_ids": [item_id]}
    resp = ensure_success(post_json("/open-apis/v1/instrumental/query", payload), "纯音乐状态查询")
    instrumentals = resp.get("data", {}).get("instrumentals", [])
    if not instrumentals:
        raise RuntimeError(f"纯音乐查询未返回结果: {json.dumps(resp, ensure_ascii=False)}")
    return instrumentals[0]


def wait_for_music_task(
    item_id: str,
    *,
    poll_interval: int = 15,
    timeout: int = 900,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    last_status: str | None = None

    while time.monotonic() < deadline:
        item = query_music_task(item_id)
        status = str(item.get("status", ""))

        if status != last_status:
            print(f"纯音乐任务状态: {status}")
            log_params("纯音乐任务状态", item_id=item_id, status=status)
            last_status = status

        if status in ("succeeded", "main_succeeded", "part_failed"):
            return item
        if status == "failed":
            raise RuntimeError(f"纯音乐任务失败: {json.dumps(item, ensure_ascii=False)}")

        time.sleep(poll_interval)

    raise TimeoutError(f"纯音乐任务超时，item_id={item_id}")


# --- 歌曲 ---

def create_song_task(
    *,
    prompt: str,
    model: str,
    lyrics: str | None = None,
    voice_id: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "prompt": prompt,
        "model": model,
        "callback_url": get_callback_url(),
    }
    if lyrics is not None:
        payload["lyrics"] = lyrics
    if voice_id is not None:
        payload["voice_id"] = voice_id
    resp = ensure_success(post_json("/open-apis/v1/song/generate", payload), "歌曲生成")
    item_ids = resp.get("data", {}).get("item_ids", [])
    if not item_ids:
        raise RuntimeError(f"歌曲生成未返回 item_id: {json.dumps(resp, ensure_ascii=False)}")
    return resp


def query_song_task(item_id: str) -> dict[str, Any]:
    payload = {"item_ids": [item_id]}
    resp = ensure_success(post_json("/open-apis/v1/song/query", payload), "歌曲状态查询")
    songs = resp.get("data", {}).get("songs", [])
    if not songs:
        raise RuntimeError(f"歌曲查询未返回结果: {json.dumps(resp, ensure_ascii=False)}")
    return songs[0]


def wait_for_song_task(
    item_id: str,
    *,
    poll_interval: int = 15,
    timeout: int = 900,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    last_status: str | None = None

    while time.monotonic() < deadline:
        item = query_song_task(item_id)
        status = str(item.get("status", ""))

        if status != last_status:
            print(f"歌曲任务状态: {status}")
            log_params("歌曲任务状态", item_id=item_id, status=status)
            last_status = status

        if status in ("succeeded", "main_succeeded", "part_failed"):
            return item
        if status == "failed":
            raise RuntimeError(f"歌曲任务失败: {json.dumps(item, ensure_ascii=False)}")

        time.sleep(poll_interval)

    raise TimeoutError(f"歌曲任务超时，item_id={item_id}")


# --- 歌词 ---

def create_lyrics_task(*, prompt: str, song_model: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "prompt": prompt,
        "callback_url": get_callback_url(),
    }
    if song_model is not None:
        payload["song_model"] = song_model
    resp = ensure_success(post_json("/open-apis/v1/lyrics/generate", payload), "歌词生成")
    item_ids = resp.get("data", {}).get("item_ids", [])
    if not item_ids:
        raise RuntimeError(f"歌词生成未返回 item_id: {json.dumps(resp, ensure_ascii=False)}")
    return resp


def query_lyrics_task(item_id: str) -> dict[str, Any]:
    payload = {"item_ids": [item_id]}
    resp = ensure_success(post_json("/open-apis/v1/lyrics/query", payload), "歌词状态查询")
    lyrics_list = resp.get("data", {}).get("lyrics", [])
    if not lyrics_list:
        raise RuntimeError(f"歌词查询未返回结果: {json.dumps(resp, ensure_ascii=False)}")
    return lyrics_list[0]


def wait_for_lyrics_task(
    item_id: str,
    *,
    poll_interval: int = 10,
    timeout: int = 300,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    last_status: str | None = None

    while time.monotonic() < deadline:
        item = query_lyrics_task(item_id)
        status = str(item.get("status", ""))

        if status != last_status:
            print(f"歌词任务状态: {status}")
            log_params("歌词任务状态", item_id=item_id, status=status)
            last_status = status

        if status == "succeeded":
            return item
        if status == "failed":
            raise RuntimeError(f"歌词任务失败: {json.dumps(item, ensure_ascii=False)}")

        time.sleep(poll_interval)

    raise TimeoutError(f"歌词任务超时，item_id={item_id}")


# --- 通用工具 ---

def extract_audio_url(item: dict[str, Any]) -> str:
    url = str(item.get("audio_url", "")).strip()
    if not url:
        raise RuntimeError(f"结果中缺少 audio_url: {json.dumps(item, ensure_ascii=False)}")
    return url


def download_file(url: str, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    log_params("文件下载开始", url=url, output_path=str(output_path.name))
    request = Request(url, method="GET")
    with urlopen(request) as response:
        output_path.write_bytes(response.read())
    size = output_path.stat().st_size
    log_params("文件下载完成", url=url, output_path=str(output_path.name), size=size)
    return output_path


def default_output_path(scene: str, item_id: str, suffix: str, name: str = "") -> Path:
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    stem = f"{name}_{timestamp}" if name else f"{item_id}_{timestamp}"
    return ensure_scene_output_dir(scene) / f"{stem}{suffix}"


def pretty_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)
