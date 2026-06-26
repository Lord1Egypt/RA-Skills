from __future__ import annotations

import codecs
import json
import logging
import mimetypes
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from html import unescape
from pathlib import Path
from typing import Any

import requests


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_PATH = PROJECT_ROOT / "config.json"
WECHAT_API_BASE = "https://api.weixin.qq.com"
TOKEN_CACHE_PATH = PROJECT_ROOT / "logs" / "wechat_access_token.json"
LATEST_TASK_PATH = PROJECT_ROOT / "output" / "latest_task.json"
TASK_RESULT_FILENAME = "task_result.json"


class SkillError(Exception):
    """统一的业务异常，便于各脚本输出结构化错误。"""

    def __init__(
        self,
        stage: str,
        message: str,
        *,
        hint: str | None = None,
        details: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.stage = stage
        self.message = message
        self.hint = hint
        self.details = details

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "stage": self.stage,
            "message": self.message,
        }
        if self.hint:
            payload["hint"] = self.hint
        if self.details is not None:
            payload["details"] = self.details
        return payload


@dataclass(frozen=True)
class ComicProfile:
    canonical_name: str
    slug: str
    prompt_path: Path
    aliases: tuple[str, ...]


def ensure_directory(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return (PROJECT_ROOT / candidate).resolve()


def read_text_file(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


ESCAPED_UNICODE_PATTERN = re.compile(r"\\u[0-9a-fA-F]{4}")


def normalize_display_text(value: Any) -> str:
    """清洗展示文本，兼容意外残留的 \\uXXXX 转义字符串。"""

    text = str(value or "")
    if not text:
        return ""
    text = unescape(text)
    for _ in range(2):
        if not ESCAPED_UNICODE_PATTERN.search(text):
            break
        try:
            decoded = codecs.decode(text, "unicode_escape")
        except Exception:
            break
        if decoded == text:
            break
        text = decoded
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def read_json_file(path: str | Path) -> dict[str, Any]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SkillError("io", f"JSON 文件不存在: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SkillError("io", f"JSON 文件格式错误: {path}", details=str(exc)) from exc
    if not isinstance(payload, dict):
        raise SkillError("io", f"JSON 文件根节点必须是对象: {path}")
    return payload


def write_json_file(path: str | Path, payload: Any) -> Path:
    file_path = Path(path)
    ensure_directory(file_path.parent)
    file_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return file_path


def update_json_file(path: str | Path, updates: dict[str, Any]) -> Path:
    file_path = Path(path)
    current: dict[str, Any] = {}
    if file_path.exists():
        current = read_json_file(file_path)
    current.update(updates)
    return write_json_file(file_path, current)


def setup_logger(name: str, output_dir: str | Path) -> logging.Logger:
    """为每个任务目录绑定独立日志文件，避免复用旧 handler。"""

    output_dir = ensure_directory(output_dir)
    log_path = Path(output_dir) / "pipeline.log"
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    current_log_path = getattr(logger, "_wechat_log_path", None)
    if current_log_path == str(log_path) and logger.handlers:
        return logger

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        try:
            handler.close()
        except Exception:
            pass

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    setattr(logger, "_wechat_log_path", str(log_path))
    return logger


def get_nested_value(payload: dict[str, Any], dotted_path: str) -> Any:
    current: Any = payload
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def is_placeholder(value: Any) -> bool:
    if value is None:
        return True
    normalized = str(value).strip().lower()
    if not normalized:
        return True
    placeholder_prefixes = (
        "your_",
        "your-",
        "<",
        "example",
        "replace",
        "changeme",
        "sk-your",
        "wx-your",
    )
    return normalized.startswith(placeholder_prefixes)


def load_config(required_paths: list[str] | None = None) -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        raise SkillError(
            "config",
            f"未找到配置文件: {CONFIG_PATH}",
            hint="请先在技能根目录将 config.example.json 复制为 config.json，并填入真实模型与公众号配置。",
        )
    config = read_json_file(CONFIG_PATH)
    missing: list[str] = []
    for dotted_path in required_paths or []:
        value = get_nested_value(config, dotted_path)
        if is_placeholder(value):
            missing.append(dotted_path)
    if missing:
        raise SkillError(
            "config",
            "配置缺失或仍为占位值",
            hint="请检查 config.json 是否由 config.example.json 初始化而来，并将缺失字段替换为真实配置。",
            details={"missing": missing},
        )
    return config


def comic_profiles() -> dict[str, ComicProfile]:
    xiaolin = ComicProfile(
        canonical_name="小林漫画",
        slug="xiaolin",
        prompt_path=resolve_project_path("./prompts/xiaolin.txt"),
        aliases=("小林漫画", "小林", "xiaolin"),
    )
    parenting = ComicProfile(
        canonical_name="育儿漫画",
        slug="parenting",
        prompt_path=resolve_project_path("./prompts/parenting.txt"),
        aliases=("育儿漫画", "育儿", "parenting"),
    )
    return {
        alias.strip().lower(): profile
        for profile in (xiaolin, parenting)
        for alias in profile.aliases
    }


def normalize_comic_type(comic_type: str) -> ComicProfile:
    normalized = str(comic_type).strip().lower()
    profile = comic_profiles().get(normalized)
    if profile is None:
        raise SkillError(
            "input",
            f"不支持的漫画类型: {comic_type}",
            hint="当前仅支持：小林漫画、育儿漫画。",
        )
    if not profile.prompt_path.exists():
        raise SkillError("config", f"Prompt 模板不存在: {profile.prompt_path}")
    return profile


def build_api_url(base_url: str, path: str) -> str:
    return f"{str(base_url).rstrip('/')}/{str(path).lstrip('/')}"


def response_text_preview(response: requests.Response, limit: int = 1000) -> str:
    text = response.text
    if len(text) > limit:
        return f"{text[:limit]}...(truncated)"
    return text


def parse_json_response(response: requests.Response, stage: str) -> dict[str, Any]:
    try:
        payload = response.json()
    except ValueError as exc:
        raise SkillError(
            stage,
            "接口返回不是合法 JSON",
            details={
                "status_code": response.status_code,
                "response": response_text_preview(response),
            },
        ) from exc
    if isinstance(payload, dict) and "errcode" in payload and payload.get("errcode") not in (0, "0", None):
        raise SkillError(
            stage,
            f"接口返回业务错误: errcode={payload.get('errcode')}",
            details=payload,
        )
    return payload


def request_with_retry(
    method: str,
    url: str,
    *,
    stage: str,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    json_body: Any | None = None,
    data: Any | None = None,
    files: Any | None = None,
    timeout: int = 60,
    logger=None,
    max_retries: int = 3,
    retry_interval: int = 2,
    expected_status: tuple[int, ...] = (200,),
) -> requests.Response:
    """带重试的通用请求封装，统一输出可读错误。"""

    last_exception: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            prepared_headers = dict(headers or {})
            request_data = data
            request_json = None
            if json_body is not None:
                request_data = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
                prepared_headers.setdefault("Content-Type", "application/json; charset=utf-8")
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=prepared_headers or None,
                params=params,
                json=request_json,
                data=request_data,
                files=files,
                timeout=timeout,
            )
            if response.status_code in expected_status:
                return response

            preview = response_text_preview(response)
            retryable = response.status_code >= 500 or response.status_code in {408, 409, 425, 429}
            if logger:
                logger.warning(
                    "请求失败 stage=%s attempt=%s status=%s url=%s body=%s",
                    stage,
                    attempt,
                    response.status_code,
                    url,
                    preview,
                )
            if retryable and attempt < max_retries:
                time.sleep(retry_interval * attempt)
                continue
            raise SkillError(
                stage,
                f"HTTP 请求失败，状态码 {response.status_code}",
                details={"url": url, "response": preview},
            )
        except requests.RequestException as exc:
            last_exception = exc
            if logger:
                logger.warning("请求异常 stage=%s attempt=%s url=%s error=%s", stage, attempt, url, exc)
            if attempt < max_retries:
                time.sleep(retry_interval * attempt)
                continue
            raise SkillError(
                stage,
                f"HTTP 请求异常: {exc}",
                details={"url": url},
            ) from exc

    raise SkillError(stage, "请求重试失败", details=str(last_exception))


def extract_json_object(raw_text: str, *, stage: str) -> dict[str, Any]:
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    decoder = json.JSONDecoder()

    for start_index, char in enumerate(cleaned):
        if char not in "{[":
            continue
        try:
            payload, _ = decoder.raw_decode(cleaned[start_index:])
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload

    raise SkillError(
        stage,
        "无法从模型输出中提取合法 JSON 对象",
        details={"raw_text": cleaned[:2000]},
    )


def timestamp_label() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def now_iso() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def create_task_output_dir(comic_type: str, base_output_dir: str | Path | None = None) -> Path:
    profile = normalize_comic_type(comic_type)
    base_dir = resolve_project_path(base_output_dir or "./output")
    ensure_directory(base_dir)
    task_dir = base_dir / f"{timestamp_label()}_{profile.slug}"
    ensure_directory(task_dir)
    return task_dir


def task_result_path(output_dir: str | Path) -> Path:
    return Path(output_dir) / TASK_RESULT_FILENAME


def build_task_result(
    *,
    success: bool,
    stage: str,
    comic_type: str = "",
    topic: str = "",
    count: int | None = None,
    title: str = "",
    output_dir: str | Path = "",
    draft_status: str = "not_started",
    draft_id: str | None = None,
    created_at: str | None = None,
    error: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "success": success,
        "comic_type": comic_type,
        "topic": topic,
        "count": count,
        "title": title,
        "output_dir": str(output_dir) if output_dir else "",
        "stage": stage,
        "draft_status": draft_status,
        "draft_id": draft_id,
        "error": error,
        "created_at": created_at or now_iso(),
    }
    if extra:
        payload.update(extra)
    return payload


def save_task_result(
    output_dir: str | Path,
    payload: dict[str, Any],
    *,
    update_latest: bool = False,
) -> Path:
    output_dir = ensure_directory(output_dir)
    task_path = task_result_path(output_dir)
    merged_payload = dict(payload)
    merged_payload["output_dir"] = str(Path(output_dir).resolve())
    merged_payload["task_result_path"] = str(task_path.resolve())
    write_json_file(task_path, merged_payload)
    if update_latest:
        ensure_directory(LATEST_TASK_PATH.parent)
        write_json_file(LATEST_TASK_PATH, merged_payload)
    return task_path


def load_task_result(output_dir: str | Path) -> dict[str, Any]:
    path = task_result_path(output_dir)
    if not path.exists():
        raise SkillError(
            "task_state",
            f"任务状态文件不存在: {path}",
            hint="请先执行生成流程，确保 task_result.json 已写入。",
        )
    payload = read_json_file(path)
    payload["output_dir"] = str(Path(payload.get("output_dir") or output_dir).resolve())
    return payload


def load_latest_task() -> dict[str, Any]:
    if not LATEST_TASK_PATH.exists():
        raise SkillError(
            "task_state",
            "未找到最近任务状态",
            hint="请先执行一次生成任务，或指定 --publish_output_dir 发布已有任务。",
        )
    payload = read_json_file(LATEST_TASK_PATH)
    output_dir = payload.get("output_dir")
    if not output_dir:
        raise SkillError("task_state", "latest_task.json 缺少 output_dir")
    return load_task_result(output_dir)


def ensure_publishable_task_files(payload: dict[str, Any]) -> dict[str, Any]:
    output_dir = Path(str(payload.get("output_dir", ""))).resolve()
    required_fields = {
        "html_path": payload.get("html_path"),
        "assets_path": payload.get("assets_path"),
    }
    for field_name, field_value in required_fields.items():
        if not field_value:
            raise SkillError(
                "task_state",
                f"最近任务缺少 {field_name}",
                hint="请先执行完整生成流程，确保 HTML 与发布素材已生成。",
            )
        candidate = Path(str(field_value))
        if not candidate.is_absolute():
            candidate = output_dir / candidate
        if not candidate.exists():
            raise SkillError(
                "task_state",
                f"最近任务缺少必要文件: {candidate}",
                hint="请重新执行生成流程，确保待发布内容已完整生成。",
            )
    return payload


def load_latest_publishable_task() -> dict[str, Any]:
    payload = load_latest_task()
    draft_status = str(payload.get("draft_status", "")).strip().lower()
    if draft_status == "success":
        raise SkillError(
            "task_state",
            "最近任务已经发布成功",
            hint="如需重新发布，请显式指定 --publish_output_dir 到目标任务目录。",
            details={"draft_id": payload.get("draft_id"), "title": payload.get("title")},
        )
    if draft_status != "pending":
        raise SkillError(
            "task_state",
            "最近任务不是待发布状态",
            hint="请先执行生成流程，或指定 --publish_output_dir 发布已有任务。",
            details={"draft_status": payload.get("draft_status"), "stage": payload.get("stage")},
        )
    return ensure_publishable_task_files(payload)


def read_token_cache() -> dict[str, Any]:
    if not TOKEN_CACHE_PATH.exists():
        return {}
    try:
        return read_json_file(TOKEN_CACHE_PATH)
    except SkillError:
        return {}


def write_token_cache(payload: dict[str, Any]) -> Path:
    ensure_directory(TOKEN_CACHE_PATH.parent)
    return write_json_file(TOKEN_CACHE_PATH, payload)


def get_wechat_access_token(config: dict[str, Any], logger) -> str:
    wechat_config = config.get("wechat", {})
    appid = str(wechat_config.get("appid", "")).strip()
    appsecret = str(wechat_config.get("appsecret", "")).strip()
    cache = read_token_cache()
    now = int(time.time())
    if cache.get("access_token") and int(cache.get("expires_at", 0)) > now + 60:
        logger.info("命中本地 access_token 缓存")
        return str(cache["access_token"])

    url = build_api_url(WECHAT_API_BASE, "/cgi-bin/token")
    response = request_with_retry(
        "GET",
        url,
        stage="wechat_token",
        params={
            "grant_type": "client_credential",
            "appid": appid,
            "secret": appsecret,
        },
        timeout=60,
        logger=logger,
    )
    try:
        payload = response.json()
    except ValueError as exc:
        raise SkillError(
            "wechat_token",
            "微信 token 接口返回不是合法 JSON",
            details={
                "status_code": response.status_code,
                "response": response_text_preview(response),
            },
        ) from exc

    errcode = payload.get("errcode")
    if errcode not in (None, 0, "0"):
        hint = None
        if int(errcode) == 40164:
            hint = "请将当前出口 IP 加入微信公众号后台的接口 IP 白名单后重试。"
        raise SkillError(
            "wechat_token",
            f"微信 access_token 获取失败: errcode={errcode}",
            hint=hint,
            details=payload,
        )

    access_token = str(payload.get("access_token", "")).strip()
    expires_in = int(payload.get("expires_in", 7200))
    if not access_token:
        raise SkillError("wechat_token", "获取 access_token 失败，接口未返回 access_token", details=payload)

    cache_payload = {
        "access_token": access_token,
        "expires_in": expires_in,
        "expires_at": now + max(0, expires_in - 300),
        "updated_at": now,
    }
    write_token_cache(cache_payload)
    logger.info("微信 access_token 获取成功，已写入缓存")
    return access_token


def guess_mime_type(path: str | Path) -> str:
    mime_type, _ = mimetypes.guess_type(str(path))
    return mime_type or "application/octet-stream"


def _wechat_path(path: str) -> str:
    normalized = str(path).strip()
    if normalized.startswith("/cgi-bin/"):
        return normalized
    if normalized.startswith("/"):
        return f"/cgi-bin{normalized}"
    return f"/cgi-bin/{normalized}"


def wechat_post_json(
    access_token: str,
    path: str,
    payload: dict[str, Any],
    *,
    logger,
    timeout: int = 120,
) -> dict[str, Any]:
    url = build_api_url(WECHAT_API_BASE, _wechat_path(path))
    response = request_with_retry(
        "POST",
        url,
        stage="wechat_api",
        params={"access_token": access_token},
        headers={"Content-Type": "application/json; charset=utf-8"},
        json_body=payload,
        timeout=timeout,
        logger=logger,
    )
    return parse_json_response(response, "wechat_api")


def wechat_upload_file(
    access_token: str,
    path: str,
    file_path: str | Path,
    *,
    params: dict[str, Any] | None = None,
    logger,
    timeout: int = 120,
    max_retries: int = 3,
) -> dict[str, Any]:
    """上传素材时每次重试都重新打开文件，避免句柄失效。"""

    target_path = Path(file_path)
    if not target_path.exists():
        raise SkillError("wechat_api", f"上传文件不存在: {target_path}")

    url = build_api_url(WECHAT_API_BASE, _wechat_path(path))
    query = {"access_token": access_token}
    if params:
        query.update(params)

    last_error: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            with target_path.open("rb") as handle:
                response = requests.post(
                    url,
                    params=query,
                    files={
                        "media": (
                            target_path.name,
                            handle,
                            guess_mime_type(target_path),
                        )
                    },
                    timeout=timeout,
                )

            if response.status_code == 200:
                return parse_json_response(response, "wechat_api")

            preview = response_text_preview(response)
            retryable = response.status_code >= 500 or response.status_code in {408, 409, 425, 429}
            if logger:
                logger.warning(
                    "微信文件上传失败 attempt=%s status=%s url=%s body=%s",
                    attempt,
                    response.status_code,
                    url,
                    preview,
                )
            if retryable and attempt < max_retries:
                time.sleep(attempt * 2)
                continue
            raise SkillError(
                "wechat_api",
                f"微信文件上传失败，状态码 {response.status_code}",
                details={"url": url, "response": preview},
            )
        except requests.RequestException as exc:
            last_error = exc
            if logger:
                logger.warning("微信文件上传异常 attempt=%s url=%s error=%s", attempt, url, exc)
            if attempt < max_retries:
                time.sleep(attempt * 2)
                continue
            raise SkillError("wechat_api", f"微信文件上传异常: {exc}", details={"url": url}) from exc

    raise SkillError("wechat_api", "微信文件上传重试失败", details=str(last_error))
