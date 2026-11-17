"""Seedance video generation client — 火山方舟 Ark API.

Volcengine Ark Seedance（字节豆包视频生成）：
- POST /api/v3/contents/generations/tasks  — 提交任务（异步）
- GET  /api/v3/contents/generations/tasks/{id}  — 轮询状态
- 状态：queued → running → succeeded / failed / expired / cancelled
- ⚠️ 视频 URL 24h 过期，必须立即下载

stdlib only。ARK_API_KEY 从 env / .env 三源加载（同 OFOX_API_KEY 模式）。

模型 ID 走配置：
- 默认 doubao-seedance-2-0-260128（Seedance 2.0，2026-01-28 版本，公开 API 可用）
- 可通过 ARK_VIDEO_MODEL 环境变量覆盖（如切回 1.5 Pro：doubao-seedance-1-5-pro-251215）
"""

from __future__ import annotations
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from .llm import _TOKEN_SEARCH_PATHS, _xdg_config_dir


ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DEFAULT_VIDEO_MODEL = "doubao-seedance-2-0-260128"
DEFAULT_DURATION = 5         # 单 shot 秒数
DEFAULT_RATIO = "9:16"       # XHS 竖版默认
DEFAULT_RESOLUTION = "1080p"
DEFAULT_POLL_INTERVAL = 8    # 秒
DEFAULT_POLL_TIMEOUT = 600   # 10 分钟兜底
DEFAULT_REQUEST_TIMEOUT = 30
DEFAULT_DOWNLOAD_TIMEOUT = 180

# 1.5 Pro 估价（粗略：1080p 5s 约 $0.20，按线性折算）
ESTIMATED_COST_PER_SECOND_USD = 0.04

TERMINAL_STATUSES = {"succeeded", "failed", "expired", "cancelled"}


class SeedanceError(RuntimeError):
    """Seedance API 通用错误。"""

    def __init__(self, message: str, status: int | None = None, body: str = ""):
        super().__init__(message)
        self.status = status
        self.body = body


class TaskFailed(SeedanceError):
    """任务进入 failed / expired / cancelled。"""


class TaskTimeout(SeedanceError):
    """轮询超时（任务还在 running）。"""


# ─── 凭据加载 ───

def _load_ark_key() -> str | None:
    """env > .env 文件三源（复用 llm.py 的搜索路径）。"""
    for var in ("ARK_API_KEY", "VOLCENGINE_ARK_API_KEY"):
        if v := os.environ.get(var):
            return v.strip()
    for path_fn in _TOKEN_SEARCH_PATHS:
        try:
            path = path_fn()
        except Exception:
            continue
        if not path.exists() or not path.is_file():
            continue
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                for var in ("ARK_API_KEY", "VOLCENGINE_ARK_API_KEY"):
                    if line.startswith(f"{var}="):
                        val = line.split("=", 1)[1].strip()
                        return val.strip('"').strip("'")
        except (OSError, UnicodeDecodeError):
            continue
    return None


def ark_credentials_present() -> bool:
    """preflight 用。"""
    return bool(_load_ark_key())


def help_message() -> str:
    config_dir = _xdg_config_dir()
    return (
        "ARK_API_KEY 未配置。Seedance 视频生成需要火山方舟 API key，注册：https://www.volcengine.com/product/ark\n\n"
        "  1) 环境变量：\n"
        "     export ARK_API_KEY='你的_key'\n\n"
        f"  2) 配置文件：\n"
        f"     mkdir -p {config_dir}\n"
        f"     echo 'ARK_API_KEY=你的_key' >> {config_dir}/.env"
    )


# ─── 成本估算 ───

def estimate_cost_usd(num_shots: int, duration_per_shot: int = DEFAULT_DURATION) -> float:
    """估算 N 个 shot 的总成本（USD）。仅供用户决策，非精确账单。"""
    return num_shots * duration_per_shot * ESTIMATED_COST_PER_SECOND_USD


# ─── 核心 API：submit / poll / download ───

def submit_task(
    prompt: str,
    *,
    model: str | None = None,
    duration: int = DEFAULT_DURATION,
    ratio: str = DEFAULT_RATIO,
    resolution: str = DEFAULT_RESOLUTION,
    watermark: bool = False,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: int = DEFAULT_REQUEST_TIMEOUT,
) -> str:
    """提交一个文生视频任务，返回 task_id。

    Raises:
        SeedanceError: HTTP 错误或响应缺 id 字段
    """
    api_key = api_key or _load_ark_key()
    if not api_key:
        raise SeedanceError("ARK_API_KEY 未配置")

    base_url = (base_url or os.environ.get("ARK_BASE_URL") or ARK_BASE_URL).rstrip("/")
    model = model or os.environ.get("ARK_VIDEO_MODEL") or DEFAULT_VIDEO_MODEL

    payload = json.dumps({
        "model": model,
        "content": [{"type": "text", "text": prompt}],
        "duration": duration,
        "ratio": ratio,
        "resolution": resolution,
        "watermark": watermark,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url}/contents/generations/tasks",
        data=payload,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        raise SeedanceError(
            f"HTTP {e.code} from Ark submit: {body}", status=e.code, body=body,
        ) from e
    except urllib.error.URLError as e:
        raise SeedanceError(f"Network error reaching Ark: {e.reason}") from e

    task_id = data.get("id")
    if not task_id:
        raise SeedanceError(f"Ark response missing 'id' field: {str(data)[:200]}")
    return task_id


def query_task(
    task_id: str,
    *,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: int = DEFAULT_REQUEST_TIMEOUT,
) -> dict:
    """单次查询任务状态，返回完整 JSON。"""
    api_key = api_key or _load_ark_key()
    if not api_key:
        raise SeedanceError("ARK_API_KEY 未配置")

    base_url = (base_url or os.environ.get("ARK_BASE_URL") or ARK_BASE_URL).rstrip("/")

    req = urllib.request.Request(
        f"{base_url}/contents/generations/tasks/{task_id}",
        headers={"Authorization": f"Bearer {api_key}"},
        method="GET",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        raise SeedanceError(
            f"HTTP {e.code} from Ark query: {body}", status=e.code, body=body,
        ) from e
    except urllib.error.URLError as e:
        raise SeedanceError(f"Network error reaching Ark: {e.reason}") from e


def poll_task(
    task_id: str,
    *,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: int = DEFAULT_POLL_TIMEOUT,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
    on_progress=None,  # callable(status: str, elapsed: int)
) -> dict:
    """阻塞轮询直到 task 进入终态。

    Returns:
        最终状态的完整 JSON（含 content.video_url 如果成功）

    Raises:
        TaskTimeout: 超过 timeout 还在 queued/running
        TaskFailed: 进入 failed / expired / cancelled
    """
    started = time.time()
    while True:
        result = query_task(task_id, api_key=api_key, base_url=base_url)
        status = result.get("status", "unknown")
        elapsed = int(time.time() - started)

        if on_progress:
            on_progress(status, elapsed)

        if status == "succeeded":
            return result
        if status in ("failed", "expired", "cancelled"):
            err = result.get("error", {}) or {}
            msg = err.get("message") or result.get("message") or "(no detail)"
            raise TaskFailed(f"Task {task_id} {status}: {msg}")

        if elapsed >= timeout:
            raise TaskTimeout(
                f"Task {task_id} still {status} after {elapsed}s (timeout={timeout}s)",
            )
        time.sleep(poll_interval)


def download_video(url: str, out_path: Path, timeout: int = DEFAULT_DOWNLOAD_TIMEOUT) -> Path:
    """下载视频文件到本地。

    Ark 返回的 URL 24h 后过期，须立即下载。
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8.7.1"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            out_path.write_bytes(resp.read())
    except urllib.error.HTTPError as e:
        raise SeedanceError(f"HTTP {e.code} downloading video from {url[:80]}") from e
    except urllib.error.URLError as e:
        raise SeedanceError(f"Network error downloading video: {e.reason}") from e
    return out_path


# ─── 阻塞模式入口：submit + poll + download 一条龙 ───

def submit_and_wait(
    prompt: str,
    out_path: Path,
    *,
    model: str | None = None,
    duration: int = DEFAULT_DURATION,
    ratio: str = DEFAULT_RATIO,
    resolution: str = DEFAULT_RESOLUTION,
    watermark: bool = False,
    api_key: str | None = None,
    base_url: str | None = None,
    poll_timeout: int = DEFAULT_POLL_TIMEOUT,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
    on_progress=None,
) -> tuple[Path, str]:
    """提交 + 阻塞轮询 + 下载，返回 (本地视频路径, task_id)。

    on_progress(status, elapsed) 可选，用于打印进度行。

    Raises:
        SeedanceError / TaskFailed / TaskTimeout
    """
    task_id = submit_task(
        prompt,
        model=model, duration=duration, ratio=ratio, resolution=resolution,
        watermark=watermark, api_key=api_key, base_url=base_url,
    )
    if on_progress:
        on_progress("submitted", 0)

    result = poll_task(
        task_id,
        api_key=api_key, base_url=base_url,
        timeout=poll_timeout, poll_interval=poll_interval,
        on_progress=on_progress,
    )

    content = result.get("content") or {}
    video_url = content.get("video_url")
    if not video_url:
        raise SeedanceError(f"Task {task_id} succeeded but no video_url in response")

    download_video(video_url, out_path)
    return out_path, task_id


def extract_video_url(query_response: dict) -> str | None:
    """从 query_task 响应里提取 video_url（兼容字段名变化）。"""
    content = query_response.get("content") or {}
    return content.get("video_url") or query_response.get("video_url")
