#!/usr/bin/env python3
"""Run one or more TransWeb AI Skills (apps) and return document links.

Workflow:
  1. ``list``  — POST /user/getLoginedData, show usable app IDs and metadata.
  2. choose  — the agent selects one or more IDs from the list.
  3. ``run``   — for each ID: POST /gpt/aiGatewayRequest, find the archived
                 questionData version and build the link. Records stay private
                 by default; opt in with ``--share`` to make them public.

Python's standard library is enough; HTTP uses system ``curl`` when available
and falls back to ``urllib``.

Offline entry points for marketplace sandboxes (no network, no API key):
  ``demo``  — full workflow preview with sample data.
  ``list`` / ``run`` / ``ppt`` also accept ``--dry-run`` for offline previews.

Python's standard library is enough; HTTP uses system ``curl`` when available
and falls back to ``urllib``.
"""

from __future__ import annotations

import argparse
import ast
import base64
import copy
import getpass
import http.cookiejar
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_BASE_URL = "https://transweb.cn"
DEFAULT_TIMEOUT = 360
DEFAULT_WAIT = 15
KEY_PREFIX = "ak_live_"
TABLE = "pptItem"
PPT_APP_ID = "76f7de9504bad022a8978e9fe084df0f"
DEFAULT_PROFILE = "default"
SKILL_NAME = "transweb-ai"
SKILL_VERSION = "1.2.3"
KNOWLEDGE_APP = "a973392a7f997cf42cf5b9a760e7fb3f"
CHARACTER_APP = "12a7e2f81834ac69c7bda11219570c26"
DEFAULT_AI_NAME = "深度求索"
DEFAULT_AI_MODEL = "deepseek-v4-flash"
AIGC_REQUIREMENT_APP = "d9337acc3fb525b3d2583ca18440fda0"
AIGC_CONTENT_QUALITY_APP = "e8ebeb2cc5c46549c3d30222afc2dd07"
AIGC_PAGE_TEMPLATE_APP = "91658778302410101ec9b8fc3c2ad41c"
AIGC_IMPROVE_TEMPLATE_APP = "dc6286ffb169f8b8f156ab5f87e9bf8d"
PAGE_SIZE = 100
MAX_LIST_PAGES = 50

ENV_CONFIG = "TRANSWEB_CONFIG"
ENV_KEY = "TRANSWEB_API_KEY"
ENV_BASE = "TRANSWEB_BASE_URL"
ENV_API_NAME = "TRANSWEB_API_NAME"
ENV_MODEL = "TRANSWEB_MODEL"

EXIT_CONFIG = 2
EXIT_AUTH = 3
EXIT_UPSTREAM = 4
EXIT_OUTPUT = 5
EXIT_SAVE = 6
EXIT_NETWORK = 7


class SkillError(Exception):
    def __init__(
        self,
        message: str,
        hint: str = "",
        code: str = "error",
        exit_code: int = 1,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint
        self.code = code
        self.exit_code = exit_code


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


def eprint(*args: Any, **kwargs: Any) -> None:
    print(*args, file=sys.stderr, **kwargs)


def mask_key(key: str) -> str:
    if not key:
        return ""
    if len(key) <= 16:
        return key[:4] + "***"
    return key[:12] + "…" + key[-4:]


def normalize_base_url(value: str) -> str:
    value = (value or "").strip() or DEFAULT_BASE_URL
    if not re.match(r"^https?://", value, re.I):
        raise SkillError(
            f"base URL 必须以 http(s):// 开头：{value}",
            hint="例如 --base-url https://transweb.cn",
            code="config",
            exit_code=EXIT_CONFIG,
        )
    return value.rstrip("/")


def _find_project_config(start: Path) -> Optional[Path]:
    """Find a project-local config in a client-neutral location first."""
    for base in [start, *start.parents]:
        for relative in (
            ".transweb-ai.json",
            ".transweb/transweb-ai.json",
            ".dsh/transweb-ai.json",  # legacy compatibility
        ):
            candidate = base / relative
            if candidate.exists():
                return candidate
    return None


def _legacy_project_config(start: Path) -> Optional[Path]:
    """Keep the old DSH project path working when no config exists yet."""
    for base in [start, *start.parents]:
        if (base / ".dsh").is_dir():
            return base / ".dsh" / "transweb-ai.json"
    return None


def default_config_path() -> Path:
    override = os.environ.get(ENV_CONFIG)
    if override:
        return Path(override).expanduser()

    cwd = Path.cwd()

    # User-level XDG config takes priority: it is the most trusted location,
    # and it prevents a project-local file from silently redirecting the
    # configured API key or base URL.
    xdg = Path(
        os.environ.get("XDG_CONFIG_HOME") or "~/.config"
    ).expanduser()
    xdg_config = xdg / "transweb-ai" / "config.json"
    if xdg_config.exists():
        return xdg_config

    # Legacy DSH home config, only if it already exists.
    legacy_home = (
        Path(os.environ.get("DSH_HOME") or "~/.dsh").expanduser()
        / "transweb-ai.json"
    )
    if legacy_home.exists():
        return legacy_home

    # Project-local config is a fallback for convenience; it is only used when
    # no user-level config exists, so an untrusted project directory cannot
    # override an already-configured key or endpoint.
    project_config = _find_project_config(cwd)
    if project_config is not None:
        return project_config

    # Legacy DSH project install: keep writing where existing installs expect.
    legacy_project = _legacy_project_config(cwd)
    if legacy_project is not None:
        return legacy_project

    # Platform-neutral default.
    return xdg_config


def load_config(path: Optional[str] = None) -> Tuple[Dict[str, Any], Path]:
    config_path = Path(path).expanduser() if path else default_config_path()
    if not config_path.exists():
        return {}, config_path
    try:
        raw = config_path.read_text(encoding="utf-8")
        data = json.loads(raw) if raw.strip() else {}
    except Exception as exc:  # noqa: BLE001
        raise SkillError(
            f"配置文件无法解析：{config_path}",
            hint=f"{exc}；可删除该文件后重新 configure。",
            code="config",
            exit_code=EXIT_CONFIG,
        )
    if not isinstance(data, dict):
        raise SkillError(
            f"配置文件格式不正确：{config_path}",
            hint="应为 JSON 对象，可删除后重新 configure。",
            code="config",
            exit_code=EXIT_CONFIG,
        )
    return data, config_path


def save_config(config_path: Path, data: Dict[str, Any]) -> None:
    tmp_path = config_path.with_name(config_path.name + ".tmp")
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        try:
            os.chmod(tmp_path, 0o600)
        except OSError:
            pass
        os.replace(tmp_path, config_path)
    except PermissionError:
        try:
            tmp_path.unlink()
        except OSError:
            pass
        raise SkillError(
            f"没有权限写入配置文件：{config_path}",
            hint="请改用 --config 指定工作区内的路径。",
            code="config",
            exit_code=EXIT_CONFIG,
        )


def _normalize_config(cfg: Dict[str, Any]) -> Tuple[str, Dict[str, Dict[str, Any]]]:
    """Accept both flat {apiKey,baseUrl} and {active,profiles} configs."""
    profiles = cfg.get("profiles")
    if isinstance(profiles, dict) and profiles:
        clean: Dict[str, Dict[str, Any]] = {}
        for name, value in profiles.items():
            if isinstance(value, dict):
                clean[str(name)] = dict(value)
        active = str(cfg.get("active") or DEFAULT_PROFILE)
        if not clean:
            return DEFAULT_PROFILE, {}
        if active not in clean:
            active = next(iter(clean))
        return active, clean
    flat = {
        key: value
        for key, value in cfg.items()
        if key not in ("active", "profiles")
    }
    if not flat:
        return DEFAULT_PROFILE, {}
    return DEFAULT_PROFILE, {DEFAULT_PROFILE: flat}


def _ai_config_path(explicit: Optional[str] = None) -> Path:
    return Path(explicit).expanduser() if explicit else default_config_path()


def _profile_names(profiles: Dict[str, Dict[str, Any]]) -> List[str]:
    return sorted(profiles.keys())


def resolve_settings(args: argparse.Namespace) -> Dict[str, Any]:
    cfg, config_path = load_config(getattr(args, "config", None))
    active_profile, profiles = _normalize_config(cfg)

    requested = (
        getattr(args, "profile", None)
        or os.environ.get("TRANSWEB_PROFILE")
        or active_profile
    )
    requested = str(requested or DEFAULT_PROFILE)
    profile = profiles.get(requested)
    if profile is None:
        if profiles:
            available = ", ".join(_profile_names(profiles)) or "(none)"
            raise SkillError(
                f"API Key profile 不存在：{requested}",
                hint=(
                    f"可用 profile：{available}。"
                    "用 `configure --profile <name> --api-key <key>` 新建，"
                    "或 `config use <name>` 切换。"
                ),
                code="profile",
                exit_code=EXIT_CONFIG,
            )
        profile = {}

    base_url = normalize_base_url(
        getattr(args, "base_url", None)
        or os.environ.get(ENV_BASE)
        or profile.get("baseUrl")
        or DEFAULT_BASE_URL
    )
    api_key = (
        getattr(args, "api_key", None)
        or os.environ.get(ENV_KEY)
        or profile.get("apiKey")
        or ""
    ).strip().strip('"').strip("'")
    api_name = (
        getattr(args, "api_name", None)
        or os.environ.get(ENV_API_NAME)
        or profile.get("apiName")
        or ""
    ).strip()
    model = (
        getattr(args, "model", None)
        or os.environ.get(ENV_MODEL)
        or profile.get("model")
        or ""
    ).strip()
    return {
        "base_url": base_url,
        "api_key": api_key,
        "api_name": api_name,
        "model": model,
        "profile": requested,
        "active_profile": active_profile,
        "profiles": _profile_names(profiles),
        "config_path": config_path,
        "timeout": int(getattr(args, "timeout", DEFAULT_TIMEOUT) or DEFAULT_TIMEOUT),
    }


def require_key(settings: Dict[str, Any]) -> str:
    key = settings["api_key"]
    if not key:
        raise SkillError(
            "尚未配置 transweb.cn API Key。",
            hint=(
                "运行 `python3 scripts/transweb_ai.py configure`，"
                "或设置 TRANSWEB_API_KEY。技能不会自带或读取其他技能的默认 Key。"
            ),
            code="missing_key",
            exit_code=EXIT_CONFIG,
        )
    if not key.startswith(KEY_PREFIX):
        raise SkillError(
            f"API Key 格式不正确（应以 {KEY_PREFIX} 开头）。",
            hint="请使用 transweb.cn 账号创建的 API Key。",
            code="bad_key",
            exit_code=EXIT_CONFIG,
        )
    if len(key) < 24:
        raise SkillError(
            "API Key 长度不足，可能复制不完整。",
            code="bad_key",
            exit_code=EXIT_CONFIG,
        )
    return key


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------


def _parse_body(raw: bytes) -> Dict[str, Any]:
    text = raw.decode("utf-8", errors="replace").strip()
    if not text:
        return {}
    try:
        data = json.loads(text)
    except Exception:  # noqa: BLE001
        return {"message": text[:1000], "raw": text[:4000]}
    if isinstance(data, dict):
        return data
    return {"data": data, "raw": text[:4000]}


def _http_json_curl(
    base_url: str,
    path: str,
    *,
    api_key: Optional[str] = None,
    method: str = "GET",
    body: Optional[Dict[str, Any]] = None,
    timeout: int = 60,
    cookie_file: Optional[str] = None,
) -> Tuple[int, Dict[str, Any]]:
    curl = shutil.which("curl")
    if not curl:
        raise FileNotFoundError("curl not found")
    url = base_url + path
    payload = None
    cmd = [
        curl,
        "-sS",
        "--max-time",
        str(max(1, int(timeout))),
        "-X",
        method.upper(),
        "-H",
        "Accept: application/json",
        "-H",
        "User-Agent: transweb-ai-skill/1.0",
        "-w",
        "\n%{http_code}",
    ]
    if api_key:
        cmd += ["-H", "Authorization: Bearer " + api_key]
    if cookie_file:
        cmd += ["-b", cookie_file, "-c", cookie_file]
    if body is not None:
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        cmd += [
            "-H",
            "Content-Type: application/json; charset=utf-8",
            "--data-binary",
            "@-",
        ]
    cmd.append(url)
    try:
        proc = subprocess.run(
            cmd,
            input=payload,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=max(1, int(timeout)) + 10,
        )
    except subprocess.TimeoutExpired:
        raise SkillError(
            f"请求超时（{timeout}s）：{url}",
            hint="可加 --timeout 600；重试前先确认上次是否已扣费/生成。",
            code="timeout",
            exit_code=EXIT_NETWORK,
        )

    out = proc.stdout or b""
    err = (proc.stderr or b"").decode("utf-8", errors="replace").strip()
    split = out.rfind(b"\n")
    if split == -1:
        raw, status_text = b"", out.strip()
    else:
        raw, status_text = out[:split], out[split + 1 :].strip()
    try:
        status = int(status_text.decode("ascii", errors="ignore") or "0")
    except ValueError:
        status = 0

    if proc.returncode != 0 and not raw:
        if proc.returncode == 28:
            raise SkillError(
                f"请求超时（{timeout}s）：{url}",
                hint="可加 --timeout 600；重试前先确认上次是否已扣费/生成。",
                code="timeout",
                exit_code=EXIT_NETWORK,
            )
        raise SkillError(
            f"无法连接 {url}：{err or ('curl exit ' + str(proc.returncode))}",
            hint="检查网络、base URL 和代理设置。",
            code="network",
            exit_code=EXIT_NETWORK,
        )

    parsed = _parse_body(raw)
    if status == 0:
        status = 200 if parsed else 0
    if status >= 400 and parsed.get("ret") is None and parsed.get("code") is None:
        parsed["ret"] = status
        parsed["message"] = parsed.get("message") or f"HTTP {status}"
    return status, parsed


def _http_json_urllib(
    base_url: str,
    path: str,
    *,
    api_key: Optional[str] = None,
    method: str = "GET",
    body: Optional[Dict[str, Any]] = None,
    timeout: int = 60,
    cookie_file: Optional[str] = None,
) -> Tuple[int, Dict[str, Any]]:
    url = base_url + path
    payload = None
    headers = {"Accept": "application/json", "User-Agent": "transweb-ai-skill/1.0"}
    if body is not None:
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
    if api_key:
        headers["Authorization"] = "Bearer " + api_key
    request = urllib.request.Request(url, data=payload, headers=headers, method=method)
    jar = None
    opener = urllib.request.urlopen
    if cookie_file:
        jar = http.cookiejar.MozillaCookieJar(cookie_file)
        if os.path.exists(cookie_file):
            try:
                jar.load(ignore_discard=True, ignore_expires=True)
            except Exception:  # noqa: BLE001
                pass
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(jar)
        ).open
    try:
        with opener(request, timeout=timeout) as response:
            data = _parse_body(response.read())
        if jar is not None:
            try:
                jar.save(ignore_discard=True, ignore_expires=True)
            except Exception:  # noqa: BLE001
                pass
        return response.status, data
    except urllib.error.HTTPError as exc:
        try:
            raw = exc.read()
        except Exception:  # noqa: BLE001
            raw = b""
        parsed = _parse_body(raw)
        if parsed.get("ret") is None and parsed.get("code") is None:
            parsed["ret"] = exc.code
            parsed["message"] = parsed.get("message") or f"HTTP {exc.code}"
        return exc.code, parsed
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", exc)
        if isinstance(reason, (TimeoutError, socket.timeout)):
            raise SkillError(
                f"请求超时（{timeout}s）：{url}",
                hint="可加 --timeout 600；重试前先确认上次是否已扣费/生成。",
                code="timeout",
                exit_code=EXIT_NETWORK,
            )
        raise SkillError(
            f"无法连接 {url}：{reason}",
            hint="检查网络、base URL 和代理设置。",
            code="network",
            exit_code=EXIT_NETWORK,
        )
    except (TimeoutError, socket.timeout):
        raise SkillError(
            f"请求超时（{timeout}s）：{url}",
            hint="可加 --timeout 600；重试前先确认上次是否已扣费/生成。",
            code="timeout",
            exit_code=EXIT_NETWORK,
        )


def http_json(
    base_url: str,
    path: str,
    *,
    api_key: Optional[str] = None,
    method: str = "GET",
    body: Optional[Dict[str, Any]] = None,
    timeout: int = 60,
    cookie_file: Optional[str] = None,
) -> Tuple[int, Dict[str, Any]]:
    if shutil.which("curl"):
        try:
            return _http_json_curl(
                base_url,
                path,
                api_key=api_key,
                method=method,
                body=body,
                timeout=timeout,
                cookie_file=cookie_file,
            )
        except FileNotFoundError:
            pass
    return _http_json_urllib(
        base_url,
        path,
        api_key=api_key,
        method=method,
        body=body,
        timeout=timeout,
        cookie_file=cookie_file,
    )


def _message(payload: Dict[str, Any]) -> str:
    return str(payload.get("message") or payload.get("error") or "").strip()


def api_error(payload: Dict[str, Any], status: int = 0) -> SkillError:
    ret = payload.get("ret")
    code = payload.get("code")
    message = _message(payload) or (f"HTTP {status}" if status else "接口返回未知错误")
    lower = message.lower()

    if ret == 3 or code == 3 or "scope" in lower or "权限" in message:
        return SkillError(
            message,
            hint="API Key 缺少所需 scope；list 需要 doc:read，run 需要 ai:chat。",
            code="scope",
            exit_code=EXIT_AUTH,
        )
    if (
        ret == 1
        or code == 1
        or "登录" in message
        or "未登录" in message
        or "api key" in lower
    ):
        return SkillError(
            message,
            hint="API Key 可能无效、已过期或被撤销；请重新创建后 configure。",
            code="auth",
            exit_code=EXIT_AUTH,
        )
    if ret == 2 or "积分" in message or "余额" in message or "充值" in message:
        return SkillError(
            message,
            hint="账号积分不足；请先在 transweb.cn 充值。",
            code="points",
            exit_code=EXIT_UPSTREAM,
        )
    if status == 404:
        return SkillError(
            message,
            hint="接口不存在：确认 --base-url 是 https://transweb.cn。",
            code="not_found",
            exit_code=EXIT_UPSTREAM,
        )
    return SkillError(message, code="upstream", exit_code=EXIT_UPSTREAM)


def check_api(payload: Dict[str, Any], status: int) -> Dict[str, Any]:
    if status >= 500:
        raise api_error(payload, status)
    ret = payload.get("ret")
    code = payload.get("code")
    if ret is not None and ret != 0:
        raise api_error(payload, status)
    if code is not None and code != 0:
        raise api_error(payload, status)
    if ret is None and code is None and status >= 400:
        raise api_error(payload, status)
    return payload


# ---------------------------------------------------------------------------
# Content helpers
# ---------------------------------------------------------------------------


def extract_generated_text(payload: Dict[str, Any]) -> str:
    usage = payload.get("usage")
    containers = [payload]
    if isinstance(usage, dict):
        containers.append(usage)
    data = payload.get("data")
    if isinstance(data, str) and data.strip():
        return data
    if isinstance(data, dict):
        containers.append(data)
    for container in containers:
        for key in ("result", "content", "text"):
            value = container.get(key)
            if isinstance(value, str) and value.strip():
                return value
            if isinstance(value, dict) and value:
                try:
                    return json.dumps(value, ensure_ascii=False)
                except Exception:  # noqa: BLE001
                    pass
    return ""


def _strip_trailing_commas(text: str) -> str:
    out = []
    in_string = False
    escaped = False
    for index, char in enumerate(text):
        if in_string:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
            out.append(char)
            continue
        if char == ",":
            lookahead = index + 1
            while lookahead < len(text) and text[lookahead] in " \t\r\n":
                lookahead += 1
            if lookahead < len(text) and text[lookahead] in "}]":
                continue
        out.append(char)
    return "".join(out)


def extract_json_object(text: str) -> Tuple[str, Dict[str, Any]]:
    body = text.strip().lstrip("\ufeff")
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", body, re.I)
    if fence:
        body = fence.group(1).strip()
    try:
        parsed = json.loads(_strip_trailing_commas(body))
        if isinstance(parsed, dict):
            return json.dumps(parsed, ensure_ascii=False, separators=(",", ":")), parsed
    except Exception:  # noqa: BLE001
        pass

    best: Optional[Tuple[str, Dict[str, Any]]] = None
    start = body.find("{")
    while start != -1:
        depth = 0
        in_string = False
        escaped = False
        for index in range(start, len(body)):
            char = body[index]
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                continue
            if char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    candidate = body[start : index + 1]
                    try:
                        parsed = json.loads(_strip_trailing_commas(candidate))
                    except Exception:  # noqa: BLE001
                        break
                    if isinstance(parsed, dict):
                        rendered = json.dumps(parsed, ensure_ascii=False, separators=(",", ":"))
                        if "slides" in parsed:
                            return rendered, parsed
                        if best is None:
                            best = (rendered, parsed)
                    break
        start = body.find("{", start + 1)
    if best is not None:
        return best
    raise SkillError(
        "模型输出不是 JSON。",
        hint=f"原始输出开头：{body[:300]}",
        code="invalid_output",
        exit_code=EXIT_OUTPUT,
    )


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


# ---------------------------------------------------------------------------
# Archive / access
# ---------------------------------------------------------------------------


def fetch_account(base_url: str, api_key: str) -> Optional[Dict[str, Any]]:
    try:
        status, payload = http_json(
            base_url, "/user/getUserData?lang=zh", api_key=api_key, timeout=30
        )
    except SkillError:
        return None
    if status >= 400:
        return None
    try:
        check_api(payload, status)
    except SkillError:
        return None
    data = payload.get("data")
    return data if isinstance(data, dict) else None


def fetch_document_type(
    base_url: str,
    api_key: str,
    app_id: str,
    *,
    timeout: int = 30,
    cache: Optional[Dict[str, str]] = None,
) -> str:
    """Return "agent"/"skill" from getDocumentData; unknown falls back to "skill"."""
    if cache is not None and app_id in cache:
        return cache[app_id]
    query = urllib.parse.urlencode(
        {"table": TABLE, "key": "documentId", "documentId": app_id}
    )
    try:
        status, payload = http_json(
            base_url,
            "/user/getDocumentData?" + query,
            api_key=api_key,
            timeout=timeout,
        )
        if status >= 400 or payload.get("ret") not in (0, "0", None):
            return ""
        rows = payload.get("data")
        if not isinstance(rows, list) or not rows or not isinstance(rows[0], dict):
            return ""
        value = str(rows[0].get("documentType") or "").strip().lower()
        if value in ("agent", "skill"):
            if cache is not None:
                cache[app_id] = value
            return value
    except SkillError:
        return ""
    return ""


def _query_question_rows(
    base_url: str,
    api_key: str,
    app_id: str,
    *,
    page_no: int,
    page_size: int,
    folder_name: Optional[str] = None,
    timeout: int = 60,
) -> Tuple[int, Dict[str, Any]]:
    condition: Dict[str, Any] = {"documentId": app_id}
    if folder_name:
        values: list = [str(folder_name)]
        try:
            number = int(folder_name)
            if str(number) == str(folder_name):
                values.append(number)
        except (TypeError, ValueError):
            pass
        condition["folderName"] = {"$in": values}
    query = urllib.parse.urlencode(
        {
            "table": "questionData",
            "condition": json.dumps(condition, ensure_ascii=False),
            "sort": json.dumps({"_time": -1}),
            "pageNo": page_no,
            "pageSize": page_size,
        }
    )
    return http_json(
        base_url,
        "/user/queryQuestionData?" + query,
        api_key=api_key,
        timeout=timeout,
    )


def _row_matches(
    row: Dict[str, Any],
    raw_content: str,
    json_text: str,
    parsed: Optional[Dict[str, Any]],
) -> Optional[str]:
    row_id = row.get("_id")
    if not row_id:
        return None
    for key in ("result", "data"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            if raw_content and value == raw_content:
                return str(row_id)
            if json_text and value.strip() == json_text:
                return str(row_id)
            if raw_content and normalize_text(value) == normalize_text(raw_content):
                return str(row_id)
            if parsed is not None:
                try:
                    _, row_parsed = extract_json_object(value)
                except SkillError:
                    continue
                if row_parsed == parsed:
                    return str(row_id)
        elif isinstance(value, dict) and parsed is not None and value == parsed:
            return str(row_id)
    return None


def find_archived_data_id(
    base_url: str,
    api_key: str,
    app_id: str,
    raw_content: str,
    json_text: str,
    parsed: Optional[Dict[str, Any]],
    *,
    folder_name: Optional[str] = None,
    wait_seconds: int = DEFAULT_WAIT,
    timeout: int = 60,
) -> Optional[str]:
    deadline = time.time() + max(0, wait_seconds)
    while True:
        status, payload = _query_question_rows(
            base_url,
            api_key,
            app_id,
            page_no=1,
            page_size=50,
            folder_name=folder_name,
            timeout=timeout,
        )
        if status < 500:
            try:
                check_api(payload, status)
            except SkillError as exc:
                if exc.code == "scope":
                    raise
            else:
                rows = payload.get("data")
                if isinstance(rows, list):
                    for row in rows:
                        if isinstance(row, dict):
                            found = _row_matches(row, raw_content, json_text, parsed)
                            if found:
                                return found
        if time.time() >= deadline:
            break
        time.sleep(1)

    page_no = 1
    page_size = 100
    while page_no <= 10:
        status, payload = _query_question_rows(
            base_url,
            api_key,
            app_id,
            page_no=page_no,
            page_size=page_size,
            folder_name=folder_name,
            timeout=timeout,
        )
        if status >= 500:
            break
        try:
            check_api(payload, status)
        except SkillError as exc:
            if exc.code == "scope":
                raise
            break
        rows = payload.get("data")
        if not isinstance(rows, list) or not rows:
            break
        for row in rows:
            if isinstance(row, dict):
                found = _row_matches(row, raw_content, json_text, parsed)
                if found:
                    return found
        total = payload.get("total") or payload.get("pagination", {}).get("total")
        if isinstance(total, int) and page_no * page_size >= total:
            break
        if len(rows) < page_size:
            break
        page_no += 1
    return None


def _set_is_share(
    base_url: str, api_key: str, data_id: str, *, timeout: int = 30
) -> Tuple[bool, str]:
    body = {
        "table": "questionData",
        "cKey": "_id",
        "_id": data_id,
        "key": "isShare",
        "value": "true",
    }
    status, payload = http_json(
        base_url,
        "/user/setDocumentStatus",
        api_key=api_key,
        method="POST",
        body=body,
        timeout=timeout,
    )
    if status >= 400:
        return False, _message(payload) or f"HTTP {status}"
    try:
        check_api(payload, status)
    except SkillError as exc:
        return False, exc.message
    return True, ""


def _is_public(base_url: str, data_id: str, *, timeout: int = 30) -> bool:
    query = urllib.parse.urlencode(
        {
            "table": "questionData",
            "condition": json.dumps({"_id": data_id}, ensure_ascii=False),
            "pageNo": 1,
            "pageSize": 1,
        }
    )
    try:
        status, payload = http_json(
            base_url, "/user/queryQuestionData?" + query, timeout=timeout
        )
        check_api(payload, status)
    except SkillError:
        return False
    rows = payload.get("data")
    if not isinstance(rows, list) or not rows:
        return False
    return str(rows[0].get("isShare")) == "true"


def make_record_accessible(
    base_url: str, api_key: str, data_id: str, *, timeout: int = 30
) -> Tuple[bool, str]:
    last_error = ""
    for attempt in range(2):
        ok, error = _set_is_share(base_url, api_key, data_id, timeout=timeout)
        if ok and _is_public(base_url, data_id, timeout=timeout):
            return True, ""
        last_error = error or "更新后仍未验证到公开访问"
        if attempt == 0:
            time.sleep(1)
    return False, last_error


# ---------------------------------------------------------------------------
# App list
# ---------------------------------------------------------------------------


def _parse_tags(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str):
        raw = value.strip()
        if not raw:
            return []
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return [str(item) for item in parsed if str(item).strip()]
        except Exception:  # noqa: BLE001
            pass
        return [raw]
    return []


def _compact_app(row: Dict[str, Any], source: str = "mine") -> Dict[str, Any]:
    app_id = str(row.get("documentId") or "").strip()
    title = str(row.get("title") or row.get("name") or "").strip()
    description = str(row.get("description") or row.get("introduce") or "").strip()
    if len(description) > 500:
        description = description[:500] + "…"
    return {
        "id": app_id,
        "title": title,
        "description": description,
        "type": str(row.get("type") or "").strip(),
        "tags": _parse_tags(row.get("tags")),
        "category": str(row.get("category") or "").strip(),
        "appLabel": str(row.get("appLabel") or "").strip(),
        "publishStatus": row.get("publishStatus"),
        "source": source,
        "owner": str(row.get("appOwner") or row.get("creator") or "").strip(),
        "folderName": str(row.get("folderName") or "").strip(),
        "usageCount": row.get("usageCount"),
    }


def fetch_apps(
    base_url: str, api_key: str, *, include_all: bool, timeout: int = 60
) -> List[Dict[str, Any]]:
    condition = {} if include_all else {"publishStatus": "true"}
    apps: List[Dict[str, Any]] = []
    seen = set()
    page_no = 1
    total = None
    while page_no <= MAX_LIST_PAGES:
        body = {
            "table": TABLE,
            "pageSize": PAGE_SIZE,
            "pageNo": page_no,
            "condition": condition,
        }
        status, payload = http_json(
            base_url,
            "/user/getLoginedData",
            api_key=api_key,
            method="POST",
            body=body,
            timeout=timeout,
        )
        if status >= 400:
            raise api_error(payload, status)
        check_api(payload, status)
        rows = payload.get("data")
        if not isinstance(rows, list) or not rows:
            break
        for row in rows:
            if not isinstance(row, dict):
                continue
            app = _compact_app(row, "mine")
            if not app["id"] or app["id"] in seen:
                continue
            seen.add(app["id"])
            apps.append(app)
        pagination = payload.get("pagination") or {}
        if total is None and isinstance(pagination.get("total"), int):
            total = pagination["total"]
        if payload.get("isEnd"):
            break
        if isinstance(total, int) and page_no * PAGE_SIZE >= total:
            break
        if len(rows) < PAGE_SIZE:
            break
        page_no += 1
    return apps


def fetch_published_apps(
    base_url: str,
    api_key: str,
    *,
    timeout: int = 60,
    max_pages: int = MAX_LIST_PAGES,
) -> List[Dict[str, Any]]:
    """GET /user/getPublishedList — 公开市场里已发布的应用。"""
    apps: List[Dict[str, Any]] = []
    seen = set()
    page_no = 1
    total = None
    while page_no <= max_pages:
        query = urllib.parse.urlencode(
            {"pageSize": PAGE_SIZE, "pageNo": page_no, "sort": -1}
        )
        status, payload = http_json(
            base_url,
            "/user/getPublishedList?" + query,
            api_key=api_key,
            timeout=timeout,
        )
        if status >= 400:
            raise api_error(payload, status)
        check_api(payload, status)
        rows = payload.get("data")
        if not isinstance(rows, list) or not rows:
            break
        for row in rows:
            if not isinstance(row, dict):
                continue
            app = _compact_app(row, "published")
            if not app["id"] or app["id"] in seen:
                continue
            seen.add(app["id"])
            apps.append(app)
        if total is None and isinstance(payload.get("total"), int):
            total = payload["total"]
        if payload.get("isEnd"):
            break
        if isinstance(total, int) and page_no * PAGE_SIZE >= total:
            break
        if len(rows) < PAGE_SIZE:
            break
        page_no += 1
    return apps


def _merge_apps(
    primary: List[Dict[str, Any]], secondary: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    seen = set()
    merged: List[Dict[str, Any]] = []
    for app in primary + secondary:
        if app["id"] in seen:
            continue
        seen.add(app["id"])
        merged.append(app)
    return merged


def _score_app(app: Dict[str, Any], query: str) -> int:
    q = query.lower()
    title = app["title"].lower()
    tags = " ".join(app["tags"]).lower()
    type_name = app["type"].lower()
    description = app["description"].lower()
    score = 0
    if q in title:
        score += 10
    if q in tags:
        score += 6
    if q in type_name:
        score += 4
    if q in description:
        score += 2
    if score == 0:
        # 逐词匹配，支持中文空格分词
        for word in re.split(r"[\s,，、/]+", q):
            if len(word) < 2:
                continue
            if word in title:
                score += 3
            elif word in tags or word in type_name:
                score += 2
            elif word in description:
                score += 1
    return score


def search_apps(
    apps: List[Dict[str, Any]], query: str, limit: int
) -> List[Dict[str, Any]]:
    scored = []
    for app in apps:
        score = _score_app(app, query)
        if score > 0:
            scored.append((app, score))
    scored.sort(key=lambda item: (-item[1], item[0]["title"]))
    return [app for app, _ in scored[:limit]]


# ---------------------------------------------------------------------------
# Agent / Skill creation
# ---------------------------------------------------------------------------


def get_publish_info(base_url: str, *, timeout: int = 30) -> Dict[str, Any]:
    text = http_text(base_url + "/admin/getAppConfig?callback=cb", timeout=timeout)
    match = re.search(r"cb\((.*)\);?\s*$", text, re.S)
    if not match:
        match = re.search(r"\(\s*(\{.*\})\s*\)", text, re.S)
    if not match:
        raise SkillError(
            "无法解析 admin/getAppConfig 返回。",
            hint="检查平台是否可访问 /admin/getAppConfig。",
            code="config",
            exit_code=EXIT_UPSTREAM,
        )
    try:
        config = json.loads(match.group(1))
    except Exception as exc:  # noqa: BLE001
        raise SkillError(
            f"admin/getAppConfig JSON 解析失败：{exc}",
            code="config",
            exit_code=EXIT_UPSTREAM,
        )
    publish_info = config.get("publishInfo")
    if not isinstance(publish_info, dict) or not publish_info.get("folderName"):
        raise SkillError(
            "admin/getAppConfig 缺少 publishInfo.folderName。",
            code="config",
            exit_code=EXIT_UPSTREAM,
        )
    if not publish_info.get("appName"):
        raise SkillError(
            "admin/getAppConfig 缺少 publishInfo.appName。",
            code="config",
            exit_code=EXIT_UPSTREAM,
        )
    return publish_info


def _normalize_surrogates(text: str) -> str:
    try:
        return text.encode("utf-16", "surrogatepass").decode("utf-16")
    except Exception:  # noqa: BLE001
        return text.encode("utf-8", "replace").decode("utf-8")


def _decode_template(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _decode_template(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_decode_template(item) for item in value]
    if not isinstance(value, str):
        return value
    text = re.sub(
        r"%u([0-9a-fA-F]{4})",
        lambda match: chr(int(match.group(1), 16)),
        value,
    )
    try:
        text = urllib.parse.unquote(text)
    except Exception:  # noqa: BLE001
        pass
    text = _normalize_surrogates(text)
    stripped = text.strip()
    if stripped.startswith("{") or stripped.startswith("["):
        try:
            return _decode_template(ast.literal_eval(stripped))
        except Exception:  # noqa: BLE001
            pass
    return text


def _template_meta(template: Dict[str, Any]) -> Dict[str, Any]:
    meta = template.get("meta")
    if isinstance(meta, dict):
        return meta
    if isinstance(meta, str):
        decoded = _decode_template(meta)
        if isinstance(decoded, dict):
            return decoded
    return {}


def get_agent_template(
    base_url: str,
    api_key: str,
    publish_info: Dict[str, Any],
    cookie_file: str,
    *,
    timeout: int = 60,
    template_name: Optional[str] = None,
) -> Dict[str, Any]:
    folder = str(publish_info.get("folderName") or "")
    app_name = str(template_name or publish_info.get("appName") or "")
    query = urllib.parse.urlencode({"agent": folder, "lang": "zh"})
    status, payload = http_json(
        base_url,
        "/user/getAgentData?" + query,
        api_key=api_key,
        timeout=timeout,
        cookie_file=cookie_file,
    )
    check_api(payload, status)
    data = payload.get("data")
    if not isinstance(data, dict):
        raise SkillError(
            "getAgentData 返回数据为空。",
            code="template",
            exit_code=EXIT_UPSTREAM,
        )
    raw = data.get("agentList_zh") or data.get("agentList")
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except Exception as exc:  # noqa: BLE001
            raise SkillError(
                f"agentList_zh JSON 解析失败：{exc}",
                code="template",
                exit_code=EXIT_UPSTREAM,
            )
    if isinstance(raw, dict):
        items = list(raw.values())
    elif isinstance(raw, list):
        items = raw
    else:
        items = []

    def as_template(item: Any) -> Optional[Dict[str, Any]]:
        # agentList_zh 可能是对象数组，也可能是「每个元素是 JSON 字符串」的数组
        if isinstance(item, str):
            try:
                item = json.loads(item)
            except Exception:  # noqa: BLE001
                return None
        if not isinstance(item, dict):
            return None
        return _decode_template(item)

    templates = [tpl for tpl in (as_template(item) for item in items) if tpl]
    if not templates:
        raise SkillError(
            "agentList_zh 中没有可用模板。",
            code="template",
            exit_code=EXIT_UPSTREAM,
        )
    matches = [
        item for item in templates if str(item.get("name") or "") == app_name
    ]
    if not matches:
        available = ", ".join(str(item.get("name")) for item in templates)
        raise SkillError(
            f"agentList_zh 中找不到 publishInfo.appName={app_name} 的模板。",
            hint=f"可用模板：{available}",
            code="template",
            exit_code=EXIT_UPSTREAM,
        )
    template = matches[0]
    template["publishInfo"] = publish_info
    return template


def http_text(url: str, *, timeout: int = 60) -> str:
    curl = shutil.which("curl")
    if curl:
        proc = subprocess.run(
            [curl, "-sS", "--max-time", str(max(1, int(timeout))), url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=max(1, int(timeout)) + 10,
        )
        if proc.returncode != 0:
            raise SkillError(
                f"下载模板失败：{proc.stderr.decode('utf-8', errors='replace').strip()}",
                code="network",
                exit_code=EXIT_NETWORK,
            )
        return (proc.stdout or b"").decode("utf-8", errors="replace")
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        raise SkillError(
            f"下载模板失败：{exc}",
            code="network",
            exit_code=EXIT_NETWORK,
        )


def get_folder_name(
    base_url: str, api_key: str, cookie_file: str, *, timeout: int = 60
) -> str:
    status, payload = http_json(
        base_url,
        "/user/getLoginedData",
        api_key=api_key,
        method="POST",
        body={"table": TABLE, "pageSize": 1, "pageNo": 1},
        timeout=timeout,
        cookie_file=cookie_file,
    )
    check_api(payload, status)
    rows = payload.get("data")
    if isinstance(rows, list) and rows and isinstance(rows[0], dict):
        folder = str(rows[0].get("folderName") or "")
        if folder:
            return folder
    status, payload = http_json(
        base_url,
        "/user/getUserData?lang=zh",
        api_key=api_key,
        timeout=timeout,
        cookie_file=cookie_file,
    )
    check_api(payload, status)
    data = payload.get("data")
    if isinstance(data, dict):
        folder = str(data.get("folderName") or "")
        if folder:
            return folder
    raise SkillError(
        "无法确定当前账号的 folderName。",
        hint="需要 doc:read scope，且账号下至少有一个应用。",
        code="folder",
        exit_code=EXIT_AUTH,
    )


def get_account_name(
    base_url: str,
    api_key: str,
    folder_name: str,
    cookie_file: str,
    *,
    timeout: int = 30,
) -> str:
    """Return the API key owner's display name (agent account ``name_zh``)."""
    query = urllib.parse.urlencode({"agent": folder_name, "lang": "zh"})
    try:
        status, payload = http_json(
            base_url,
            "/user/getAgentData?" + query,
            api_key=api_key,
            timeout=timeout,
            cookie_file=cookie_file,
        )
        check_api(payload, status)
    except SkillError:
        return ""
    data = payload.get("data")
    if not isinstance(data, dict):
        return ""
    for key in ("name_zh", "name", "account"):
        value = str(data.get(key) or "").strip()
        if value:
            return value
    return ""


def upload_document(
    base_url: str,
    api_key: str,
    folder_name: str,
    document_id: str,
    content: str,
    cookie_file: str,
    *,
    timeout: int = 90,
) -> None:
    curl = shutil.which("curl")
    if not curl:
        raise SkillError(
            "创建 Agent/Skill 需要系统 curl 上传文档。",
            hint="安装 curl 后重试；list/run/ppt 不依赖 curl 上传。",
            code="missing_bin",
            exit_code=EXIT_CONFIG,
        )
    fd, path = tempfile.mkstemp(prefix="transweb-doc-", suffix=".txt")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
        url = (
            f"{base_url}/bucket/personal/"
            f"{urllib.parse.quote(folder_name)}/document/"
            f"{urllib.parse.quote(document_id)}"
        )
        proc = subprocess.run(
            [
                curl,
                "-sS",
                "--max-time",
                str(max(1, int(timeout))),
                "-X",
                "PUT",
                "-H",
                "Authorization: Bearer " + api_key,
                "-b",
                cookie_file,
                "-c",
                cookie_file,
                "-F",
                f"file=@{path}",
                url,
                "-w",
                "\n%{http_code}",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=max(1, int(timeout)) + 10,
        )
        out = proc.stdout or b""
        err = (proc.stderr or b"").decode("utf-8", errors="replace").strip()
        split = out.rfind(b"\n")
        raw = out[:split] if split != -1 else out
        status_text = out[split + 1 :].strip() if split != -1 else b"0"
        try:
            status = int(status_text.decode("ascii", errors="ignore") or "0")
        except ValueError:
            status = 0
        payload = _parse_body(raw)
        if proc.returncode != 0 or status < 200 or status >= 300:
            raise SkillError(
                f"上传文档失败：{payload.get('message') or err or 'HTTP ' + str(status)}",
                code="upload",
                exit_code=EXIT_SAVE,
            )
        if payload.get("code") not in (None, 0) and payload.get("ret") not in (None, 0):
            raise SkillError(
                f"上传文档失败：{payload.get('message') or '未知错误'}",
                code="upload",
                exit_code=EXIT_SAVE,
            )
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def call_ai_app(
    base_url: str,
    api_key: str,
    document_id: str,
    context: str,
    *,
    timeout: int = 360,
) -> Tuple[str, Optional[float]]:
    body = {
        "documentId": document_id,
        "context": context,
        "apiName": DEFAULT_AI_NAME,
        "model": DEFAULT_AI_MODEL,
    }
    status, payload = http_json(
        base_url,
        "/gpt/aiGatewayRequest",
        api_key=api_key,
        method="POST",
        body=body,
        timeout=timeout,
    )
    check_api(payload, status)
    content = extract_generated_text(payload)
    usage = payload.get("usage") if isinstance(payload.get("usage"), dict) else {}
    return content, usage.get("pointsCost")


def _safe_json(text: str) -> Optional[Dict[str, Any]]:
    try:
        _, parsed = extract_json_object(text)
        return parsed
    except SkillError:
        return None


def generate_agent_profile(
    base_url: str,
    api_key: str,
    material: str,
    *,
    timeout: int = 360,
) -> Dict[str, Any]:
    knowledge_text, points1 = call_ai_app(
        base_url, api_key, KNOWLEDGE_APP, material, timeout=timeout
    )
    knowledge = _safe_json(knowledge_text) or {}
    character_text, points2 = call_ai_app(
        base_url,
        api_key,
        CHARACTER_APP,
        json.dumps(knowledge, ensure_ascii=False) if knowledge else knowledge_text,
        timeout=timeout,
    )
    profile = _safe_json(character_text) or {}
    role = profile.get("roleProfile") if isinstance(profile.get("roleProfile"), dict) else {}
    prompt = role.get("soulMd") or character_text
    if isinstance(prompt, (dict, list)):
        prompt = _object_to_markdown(prompt)
    prompt = str(prompt).strip()
    if not prompt:
        prompt = "# Role\n专业助手\n\n# Knowledge\n" + material[:6000]
    title = str(role.get("name") or knowledge.get("title") or "AI 助手").strip()
    subtitle = str(role.get("identity") or "智能助手").strip()
    examples = []
    faq = knowledge.get("faq")
    if isinstance(faq, list):
        for item in faq[:3]:
            if isinstance(item, dict):
                tags = item.get("tags") if isinstance(item.get("tags"), list) else []
                fallback_title = (",".join(str(tag) for tag in tags) + "方面问题") if tags else "示例"
                examples.append(
                    {
                        "title": str(item.get("name") or fallback_title)[:60],
                        "desc": str(item.get("question") or item.get("name") or "")[:160],
                    }
                )
    points = sum(
        value for value in (points1, points2) if isinstance(value, (int, float))
    )
    return {
        "title": title,
        "description": subtitle,
        "introduce": str(role.get("mission") or subtitle).strip(),
        "prompt": prompt,
        "examples": examples,
        "knowledge": knowledge,
        "knowledgeRaw": knowledge_text,
        "pointsCost": points or None,
    }


def _object_to_markdown(value: Any, level: int = 2) -> str:
    if not isinstance(value, (dict, list)):
        return "" if value is None else str(value)
    if isinstance(value, list):
        return "\n".join(f"- {item}" for item in value if item is not None)
    lines: List[str] = []
    for key, item in value.items():
        name = str(key).strip()
        if not name or item is None:
            continue
        heading = "#" * min(max(level, 1), 6)
        if isinstance(item, dict):
            lines.append(f"{heading} {name}\n{_object_to_markdown(item, level + 1)}")
        elif isinstance(item, list):
            lines.append(f"{heading} {name}\n{_object_to_markdown(item, level + 1)}")
        else:
            lines.append(f"{heading} {name}\n{item}")
    return "\n\n".join(lines)


def _data_url(text: str) -> str:
    encoded = base64.b64encode(text.encode("utf-8")).decode("ascii")
    return "data:text/plain;charset=utf-8;base64," + encoded


def _bind_data(code: str, params: Dict[str, Any]) -> str:
    def repl(match: re.Match) -> str:
        key = match.group(1)
        if key not in params:
            return match.group(0)
        value = params[key]
        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False)
        return str(value)

    return re.sub(r"{{\s*([^}\s]+)\s*}}", repl, code)


def _json_block(text: str, label: str) -> Dict[str, Any]:
    try:
        _, parsed = extract_json_object(text)
    except SkillError:
        raise SkillError(
            f"{label} 返回的不是有效 JSON。",
            hint=f"原始输出开头：{text[:300]}",
            code="invalid_output",
            exit_code=EXIT_OUTPUT,
        )
    return parsed


def generate_skill_app(
    base_url: str,
    api_key: str,
    requirement: str,
    *,
    timeout: int = 360,
) -> Dict[str, Any]:
    """Reproduce aigcPlugin.createAigcApp's four-step workflow."""
    step0_text, points0 = call_ai_app(
        base_url, api_key, AIGC_REQUIREMENT_APP, requirement, timeout=timeout
    )
    j0 = _json_block(step0_text, "需求分析")
    step1_text, points1 = call_ai_app(
        base_url,
        api_key,
        AIGC_CONTENT_QUALITY_APP,
        json.dumps({"需求分析": step0_text}, ensure_ascii=False),
        timeout=timeout,
    )
    j1 = _json_block(step1_text, "质量约束")

    example = j0.get("example")
    page_input = (
        json.dumps(example, ensure_ascii=False)
        if isinstance(example, (dict, list))
        else str(example or "")
    )
    step2_text, points2 = call_ai_app(
        base_url,
        api_key,
        AIGC_PAGE_TEMPLATE_APP,
        page_input,
        timeout=timeout,
    )
    step3_text, points3 = call_ai_app(
        base_url,
        api_key,
        AIGC_IMPROVE_TEMPLATE_APP,
        json.dumps(
            {"模板生成": step2_text, "质量约束": step1_text},
            ensure_ascii=False,
        ),
        timeout=timeout,
    )
    j3 = _json_block(step3_text, "模板润色")
    html = str(j3.get("html") or "").strip()
    css = str(j3.get("css") or "").strip()
    if not html:
        raise SkillError(
            "模板润色结果缺少 html。",
            code="invalid_output",
            exit_code=EXIT_OUTPUT,
        )

    example_for_code = (
        json.dumps(example, ensure_ascii=False)
        if isinstance(example, (dict, list))
        else str(example or "{}")
    )
    prompt = f"""# Role
{j1.get("role", "")}

# Objective
{j0.get("description", "")}

# JSON Output Enforcement（JSON输出强约束）

请严格按照以下要求生成输出：

你必须只输出一个合法的 JSON 对象，不得包含任何额外内容。

1. 输出唯一性要求
仅允许输出 一个 JSON 对象
禁止输出任何解释、说明、思考过程或多余文本
禁止使用 Markdown、代码块标记（如 ```）
2. JSON 格式强约束
输出必须为标准 JSON，可被 JSON.parse() 直接解析
所有 key 必须使用 双引号
所有 string 类型 value 必须使用 双引号
禁止使用单引号
3. 语法零容忍规则（必须满足）

以下情况一律禁止：

❌ 尾随逗号（trailing comma）
❌ 注释（// 或 /* */）
❌ 多余非 JSON 文本
❌ 未闭合的括号或引号
❌ 换行中夹杂非 JSON 字符
4. 输出结构要求
必须是一个完整 JSON 对象 {{ ... }}
不能是数组、字符串或其他数据类型
所有字段必须合法 JSON 类型（string / number / boolean / object / array / null）
5. 强制约束（关键）

如果无法生成合法 JSON：
→ 仍必须输出一个最小合法 JSON，例如：{{}}

在生成 JSON 前，请在内部验证其可解析性，但不要输出验证过程。

# Constraints
{json.dumps(j1.get("constraints", {}), ensure_ascii=False)}

# Requirements
{json.dumps(j1.get("requirements", {}), ensure_ascii=False)}

# Output Schema
{json.dumps(j0.get("struct"), ensure_ascii=False) if isinstance(j0.get("struct"), (dict, list)) else j0.get("struct", "")}

# Output Example
{example_for_code}
"""
    custom_code = f"""<template>
  <div class="rootContainerItem tw-w-full tw-h-full tw-p-4 tw-overflow-auto">
  {html}
  </div>
</template>
<script>
export default {{
  "name": "-",
  "data": function() {{
    return {{
      accountData: {example_for_code}
    }}
  }}
}}
</script>
<style>
{css}
</style>
"""
    points = sum(
        value for value in (points0, points1, points2, points3)
        if isinstance(value, (int, float))
    )
    return {
        "title": str(j0.get("title") or requirement[:30] or "AI Skill").strip(),
        "description": str(j0.get("description") or "").strip(),
        "introduce": str(j0.get("introduce") or j0.get("description") or "").strip(),
        "type": str(j0.get("type") or "创意写作类"),
        "category": str(j0.get("category") or "未定义"),
        "grades": str(j0.get("grades") or "[]"),
        "tags": str(j0.get("tags") or "[]"),
        "icon": str(j0.get("icon") or "🧩"),
        "prompt": prompt,
        "customCode": custom_code,
        "input": str(j1.get("input") or "请输入你的需求…"),
        "inputExamples": j1.get("inputExamples") or [],
        "role": str(j1.get("role") or ""),
        "pointsCost": points or None,
    }


def _escape_js(value: str) -> str:
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
    )


def _replace_once(text: str, old: str, new: str) -> Tuple[str, bool]:
    if old not in text:
        return text, False
    return text.replace(old, new, 1), True


def _js_escape(value: str) -> str:
    r"""Match JavaScript ``escape()`` for every string written into the wrapper.

    ``extractContentInBrackets`` uses ``/\(([^)]*)\)/``. Any literal ``)`` inside
    a JSON string truncates the match and breaks ``eval``. JS ``escape()`` turns
    ``)`` into ``%29`` (and also ``(``, spaces, Chinese, etc.), so the wrapper
    body contains no ``)`` until its final closing bracket.
    """
    safe = set(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@*_+-./"
    )
    out: List[str] = []
    for char in value:
        if char in safe:
            out.append(char)
            continue
        code = ord(char)
        if code <= 0xFF:
            out.append(f"%{code:02X}")
        elif code <= 0xFFFF:
            out.append(f"%u{code:04X}")
        else:
            code -= 0x10000
            high = 0xD800 + (code >> 10)
            low = 0xDC00 + (code & 0x3FF)
            out.append(f"%u{high:04X}%u{low:04X}")
    return "".join(out)


def _encode_wrapper_strings(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _encode_wrapper_strings(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_encode_wrapper_strings(item) for item in value]
    if isinstance(value, str):
        return _js_escape(value)
    return value


def _build_wrapper(
    document_id: str,
    title: str,
    description: str,
    code: str,
    folder_name: str,
    app_template: Dict[str, Any],
    publish_info: Dict[str, Any],
) -> str:
    app = copy.deepcopy(app_template)
    app["publishInfo"] = publish_info
    if not app.get("name"):
        app["name"] = publish_info.get("appName") or "appGenerator"
    payload = {
        "content": [
            {
                "content": {
                    "title": title,
                    "description": description,
                    "code": code,
                }
            }
        ],
        "app": app,
        "documentMeta": {
            "documentId": document_id,
            "folderName": folder_name,
            "title": title,
            "description": description,
            "appName": app.get("name"),
            "versionArray": [],
        },
    }
    body = json.dumps(_encode_wrapper_strings(payload), ensure_ascii=False)
    if ")" in body:
        raise SkillError(
            "生成的文档包装仍包含未转义的 ')'，会被 extractContentInBrackets 截断。",
            code="serialize",
            exit_code=EXIT_SAVE,
        )
    return f"transweb_{document_id}({body});"


def _build_skill_code(
    template: str,
    generated: Dict[str, Any],
    document_id: str,
) -> str:
    custom_code = str(generated.get("customCode") or "").strip()
    if not custom_code:
        raise SkillError(
            "Skill 工作流没有生成自定义页面代码。",
            code="invalid_output",
            exit_code=EXIT_OUTPUT,
        )
    params = {
        "content": _data_url(custom_code),
        "title": generated.get("title") or "",
        "introduce": generated.get("introduce") or generated.get("description") or "",
        "icon": generated.get("icon") or "🧩",
    }
    code = _bind_data(template, params)
    code, ok_title = _replace_once(
        code, 'title: "...",', f'title: "{_escape_js(str(params["title"]))}",'
    )
    code, ok_intro = _replace_once(
        code,
        'introduce: "...",',
        f'introduce: "{_escape_js(str(params["introduce"]))}",',
    )
    code, ok_icon = _replace_once(
        code, 'icon: "...",', f'icon: "{_escape_js(str(params["icon"]))}",'
    )
    encoded_prompt = urllib.parse.quote(str(generated.get("prompt") or ""), safe="")
    code, ok_prompt = _replace_once(
        code, 'defaultTemplate: "",', f'defaultTemplate: "{encoded_prompt}",'
    )
    code, _ = _replace_once(
        code,
        'inputPlaceholder: "...",',
        f'inputPlaceholder: "{_escape_js(str(generated.get("input") or "请输入你的需求…"))}",',
    )
    examples = json.dumps(generated.get("inputExamples") or [], ensure_ascii=False)
    code, count = re.subn(
        r"exampleList:\s*\[[\s\S]*?\n(\s*)\],",
        f"exampleList: {examples},",
        code,
        count=1,
    )
    # 兼容旧版本替换产生的多余 "],"，避免 data() 语法错误
    code, _ = re.subn(
        r"(exampleList:\s*\[[\s\S]*?\]),\s*\n\s*\],\s*\n(\s*loadingProgressApp:)",
        r"\1,\n\2",
        code,
        count=1,
    )
    code, ok_query = _replace_once(
        code,
        'documentId: "7d866c16505b8c1f60e731835fa287e8"',
        f'documentId: "{document_id}"',
    )
    if not (ok_title and ok_intro and ok_icon and ok_prompt and ok_query and count):
        raise SkillError(
            "Skill 模板结构不匹配，无法写入页面或数据字段。",
            hint="模板可能已更新；请检查 /transweb/appTemplate.vue。",
            code="template",
            exit_code=EXIT_UPSTREAM,
        )
    return code


def publish_created_item(
    base_url: str,
    api_key: str,
    cookie_file: str,
    document_id: str,
    document_path: str,
    title: str,
    description: str,
    prompt: str,
    folder_name: str,
    *,
    kind: str,
    app_name: str,
    app_label: str,
    app_agent: str,
    app_owner: str,
    avatar: str,
    item_type: str = "",
    item_category: str = "",
    item_grades: str = "",
    item_tags: str = "",
    item_icon: str = "",
    item_introduce: str = "",
    creator: str = "",
    publish: bool = False,
) -> None:
    body = {
        "id": document_id,
        "document": document_path,
        "name": title,
        "title": title,
        "description": description,
        "introduce": item_introduce or description,
        "type": item_type or ("创意写作类" if kind == "skill" else "社交"),
        "category": item_category or "未定义",
        "grades": item_grades or "[]",
        "tags": item_tags or "[]",
        "icon": item_icon or "🧩",
        "prompt": prompt,
        "appName": app_name,
        "appLabel": app_label,
        "appAgent": app_agent,
        "appOwner": app_owner,
        "avatar": avatar,
        "folderName": folder_name,
        "creator": creator or "TransWeb",
        "rootFlag": 1,
        "root": "",
        "rootAccount": folder_name,
        "table": TABLE,
        "apiName": DEFAULT_AI_NAME,
        "model": DEFAULT_AI_MODEL,
    }
    status, payload = http_json(
        base_url,
        "/user/publishPptItem",
        api_key=api_key,
        method="POST",
        body=body,
        timeout=60,
        cookie_file=cookie_file,
    )
    check_api(payload, status)
    # 默认不发布到全局市场；只有显式 --publish 才公开
    set_body = {
        "table": TABLE,
        "cKey": "documentId",
        "documentId": document_id,
        "key": "publishStatus",
        "value": "true" if publish else "false",
    }
    http_json(
        base_url,
        "/user/setDocumentStatus",
        api_key=api_key,
        method="POST",
        body=set_body,
        timeout=30,
        cookie_file=cookie_file,
    )


def _create_record(
    args: argparse.Namespace,
    *,
    kind: str,
    text: str,
) -> Dict[str, Any]:
    settings = resolve_settings(args)
    key = require_key(settings)
    base_url = settings["base_url"]
    tmpdir = tempfile.mkdtemp(prefix="transweb-create-")
    cookie_file = os.path.join(tmpdir, "cookies.txt")
    try:
        if not args.quiet:
            eprint("⏳ 准备账号会话 ...")
        folder_name = get_folder_name(base_url, key, cookie_file, timeout=60)
        publish_info = get_publish_info(base_url, timeout=30)
        template_name = "agentGenerator" if kind == "agent" else "appGenerator"
        template_app = get_agent_template(
            base_url,
            key,
            publish_info,
            cookie_file,
            timeout=60,
            template_name=template_name,
        )
        meta = _template_meta(template_app)
        app_name = str(template_app.get("name") or template_name)
        app_label = str(meta.get("label") or "轻应用")
        app_agent = str(publish_info.get("folderName") or "")
        app_owner = str(publish_info.get("user") or "")
        avatar = str(publish_info.get("avatar") or "")
        creator_name = get_account_name(
            base_url, key, folder_name, cookie_file, timeout=30
        ) or "TransWeb"
        if not args.quiet:
            eprint(
                f"   folderName={folder_name} creator={creator_name} "
                f"publishFolder={app_agent} appName={app_name} label={app_label}"
            )

        if kind == "agent":
            if not args.quiet:
                eprint("⏳ 正在从资料生成 Agent 人设 ...")
            generated = generate_agent_profile(
                base_url, key, text, timeout=settings["timeout"]
            )
            if args.title:
                generated["title"] = args.title
            if args.description:
                generated["description"] = args.description
            template_url = base_url + "/transweb/agentTemplate.vue"
            template = http_text(template_url, timeout=60)
            doc_id = uuid.uuid4().hex
            code, _ = _replace_once(
                template,
                'title: "同行助手",',
                f'title: "{_escape_js(generated["title"])}",',
            )
            code, _ = _replace_once(
                code,
                'subtitle: "与你同行，在真理与恩典中寻找答案。",',
                f'subtitle: "{_escape_js(generated["description"])}",',
            )
            code, _ = _replace_once(
                code,
                'introduce: "求真而不妄断，求善而不说教，求美而不矫饰。",',
                f'introduce: "{_escape_js(generated.get("introduce") or "")}",',
            )
            examples = json.dumps(generated.get("examples") or [], ensure_ascii=False)
            code, example_count = re.subn(
                r"exampleList:\s*\[[\s\S]*?\n(\s*)\],",
                f"exampleList: {examples},",
                code,
                count=1,
            )
            if not example_count:
                if not args.quiet:
                    eprint("   ⚠️  Agent 模板 exampleList 未替换，使用模板默认示例")
            code, _ = re.subn(
                r"(exampleList:\s*\[[\s\S]*?\]),\s*\n\s*\],\s*\n(\s*query:)",
                r"\1,\n\2",
                code,
                count=1,
            )
            code, _ = _replace_once(
                code,
                '"documentId": "49f774c4c3ccbf42d7dac0f89fe412c4"',
                f'"documentId": "{doc_id}"',
            )
        else:
            if not args.quiet:
                eprint("⏳ 正在执行 Skill 四步工作流 ...")
            generated = generate_skill_app(
                base_url, key, text, timeout=settings["timeout"]
            )
            if args.title:
                generated["title"] = args.title
            if args.description:
                generated["description"] = args.description
                generated["introduce"] = args.description
            template_url = base_url + "/transweb/appTemplate.vue"
            template = http_text(template_url, timeout=60)
            doc_id = uuid.uuid4().hex
            code = _build_skill_code(template, generated, doc_id)

        title = str(generated["title"]).strip() or ("AI Agent" if kind == "agent" else "AI Skill")
        description = str(generated["description"]).strip()
        prompt = str(generated["prompt"]).strip()
        if not prompt:
            raise SkillError(
                "生成结果缺少 prompt。",
                code="invalid_output",
                exit_code=EXIT_OUTPUT,
            )

        wrapper = _build_wrapper(
            doc_id,
            title,
            description,
            code,
            folder_name,
            template_app,
            publish_info,
        )
        document_path = f"/bucket/personal/{folder_name}/document/{doc_id}"
        if not args.quiet:
            eprint("⏳ 正在上传应用代码 ...")
        upload_document(
            base_url,
            key,
            folder_name,
            doc_id,
            wrapper,
            cookie_file,
            timeout=90,
        )
        if not args.quiet:
            eprint("⏳ 正在创建应用记录 ...")
        publish_created_item(
            base_url,
            key,
            cookie_file,
            doc_id,
            document_path,
            title,
            description,
            prompt,
            folder_name,
            kind=kind,
            app_name=app_name,
            app_label=app_label,
            app_agent=app_agent,
            app_owner=app_owner,
            avatar=avatar,
            item_type=str(generated.get("type") or ""),
            item_category=str(generated.get("category") or ""),
            item_grades=str(generated.get("grades") or ""),
            item_tags=str(generated.get("tags") or ""),
            item_icon=str(generated.get("icon") or ""),
            item_introduce=str(generated.get("introduce") or ""),
            creator=creator_name,
            publish=bool(args.publish),
        )
        if kind == "agent" and generated.get("knowledgeRaw"):
            knowledge_raw = str(generated.get("knowledgeRaw") or "")
            knowledge = generated.get("knowledge") if isinstance(generated.get("knowledge"), dict) else {}
            try:
                k_json_text, k_parsed = extract_json_object(knowledge_raw)
            except SkillError:
                k_json_text, k_parsed = "", knowledge
            if not args.quiet:
                eprint("⏳ 正在关联知识库存档 ...")
            k_id = find_archived_data_id(
                base_url,
                key,
                KNOWLEDGE_APP,
                knowledge_raw,
                k_json_text,
                k_parsed or None,
                folder_name=folder_name,
                wait_seconds=10,
                timeout=60,
            )
            if k_id:
                attr = {
                    "table": TABLE,
                    "cKey": "documentId",
                    "documentId": doc_id,
                    "key": "knowledges",
                    "value": [
                        {
                            "id": k_id,
                            "name": str(knowledge.get("title") or title),
                        }
                    ],
                }
                http_json(
                    base_url,
                    "/user/setDocumentStatus",
                    api_key=key,
                    method="POST",
                    body=attr,
                    timeout=30,
                    cookie_file=cookie_file,
                )
        link = f"{base_url}/{'agent' if kind == 'agent' else 'skill'}.html?id={doc_id}"
        return {
            "ok": True,
            "link": link,
            "id": doc_id,
            "type": kind,
            "title": title,
            "description": description,
            "promptChars": len(prompt),
            "pointsCost": generated.get("pointsCost"),
            "published": bool(args.publish),
        }
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def cmd_agent(args: argparse.Namespace) -> int:
    text = _read_input_text(args, "资料")
    result = _create_record(args, kind="agent", text=text)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
        return 0
    print(f"✅ 已创建 Agent：{result['title']}")
    print(f"🔗 链接：{result['link']}")
    if result.get("pointsCost") is not None:
        print(f"⚡ 消耗：{result['pointsCost']} 积分")
    return 0


def cmd_skill(args: argparse.Namespace) -> int:
    text = _read_input_text(args, "需求描述")
    result = _create_record(args, kind="skill", text=text)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
        return 0
    print(f"✅ 已创建 Skill：{result['title']}")
    print(f"🔗 链接：{result['link']}")
    if result.get("pointsCost") is not None:
        print(f"⚡ 消耗：{result['pointsCost']} 积分")
    return 0


def _read_file_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader  # type: ignore
        except Exception:  # noqa: BLE001
            try:
                from PyPDF2 import PdfReader  # type: ignore
            except Exception:  # noqa: BLE001
                raise SkillError(
                    "读取 PDF 需要 pypdf 或 PyPDF2。",
                    hint="pip install pypdf，或先把 PDF 转成 txt。",
                    code="missing_dep",
                    exit_code=EXIT_CONFIG,
                )
        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    if suffix == ".docx":
        try:
            import docx  # type: ignore
        except Exception:  # noqa: BLE001
            raise SkillError(
                "读取 Word 需要 python-docx。",
                hint="pip install python-docx，或先把文档转成 txt。",
                code="missing_dep",
                exit_code=EXIT_CONFIG,
            )
        document = docx.Document(str(path))
        return "\n".join(p.text for p in document.paragraphs)
    if suffix == ".doc":
        raise SkillError(
            "暂不支持旧版 .doc，请先另存为 .docx 或 .txt。",
            code="bad_input",
            exit_code=EXIT_CONFIG,
        )
    return path.read_text(encoding="utf-8", errors="replace")


def _read_input_text(args: argparse.Namespace, label: str) -> str:
    if args.input is not None:
        text = args.input
    elif args.file:
        path = Path(args.file).expanduser()
        if not path.exists():
            raise SkillError(
                f"输入文件不存在：{path}", code="bad_input", exit_code=EXIT_CONFIG
            )
        text = _read_file_text(path)
    elif args.stdin:
        text = sys.stdin.read()
    else:
        raise SkillError(
            f"缺少{label}。",
            hint="使用 --input、--file 或 --stdin 传入。",
            code="bad_input",
            exit_code=EXIT_CONFIG,
        )
    text = text.strip()
    if not text:
        raise SkillError(f"{label}为空。", code="bad_input", exit_code=EXIT_CONFIG)
    return text


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_configure(args: argparse.Namespace) -> int:
    # 读取当前 transweb-ai 配置，再写入（不会读取其他技能的 Key）
    cfg, _ = load_config(args.config)
    active_profile, profiles = _normalize_config(cfg)
    target_path = _ai_config_path(args.config)
    profile_name = (
        getattr(args, "profile", None)
        or (active_profile if profiles else DEFAULT_PROFILE)
        or DEFAULT_PROFILE
    )
    profile_name = str(profile_name)
    existing = dict(profiles.get(profile_name) or {})

    api_key = (args.api_key or "").strip().strip('"').strip("'")
    if args.api_key_stdin:
        api_key = sys.stdin.read().strip().strip('"').strip("'")
    if not api_key:
        api_key = str(existing.get("apiKey") or "").strip()
    if not api_key:
        try:
            api_key = getpass.getpass(
                f"transweb.cn API Key ({KEY_PREFIX}...) [{profile_name}]: "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            raise SkillError("已取消配置。", code="cancelled", exit_code=EXIT_CONFIG)
    if not api_key:
        raise SkillError("API Key 不能为空。", code="bad_key", exit_code=EXIT_CONFIG)
    if not api_key.startswith(KEY_PREFIX):
        raise SkillError(
            f"API Key 应以 {KEY_PREFIX} 开头。",
            hint="这是 transweb.cn 账号的 API Key，不是模型厂商 Key。",
            code="bad_key",
            exit_code=EXIT_CONFIG,
        )
    if len(api_key) < 24:
        raise SkillError(
            "API Key 长度不足，可能复制不完整。",
            code="bad_key",
            exit_code=EXIT_CONFIG,
        )

    profile = dict(existing)
    profile["apiKey"] = api_key
    if args.base_url:
        profile["baseUrl"] = normalize_base_url(args.base_url)
    if args.api_name:
        profile["apiName"] = args.api_name.strip()
    if args.model:
        profile["model"] = args.model.strip()
    profiles[profile_name] = profile
    save_config(
        target_path,
        {"active": profile_name, "profiles": profiles},
    )
    print(f"✅ 已保存配置：{target_path}")
    print(f"   Profile：{profile_name}（已设为当前）")
    print(f"   Key：{mask_key(api_key)}")
    print(f"   Base URL：{profile.get('baseUrl') or DEFAULT_BASE_URL}")

    if args.verify:
        settings = {
            "base_url": normalize_base_url(profile.get("baseUrl") or DEFAULT_BASE_URL),
            "api_key": api_key,
        }
        try:
            whoami(settings, json_mode=False)
        except SkillError as exc:
            eprint(f"⚠️  保存成功，但验证未通过：{exc.message}")
            if exc.hint:
                eprint(f"   {exc.hint}")
    return 0


def cmd_config_show(args: argparse.Namespace) -> int:
    cfg, config_path = load_config(args.config)
    active_profile, profiles = _normalize_config(cfg)
    action = getattr(args, "action", "show")
    name = getattr(args, "name", None)

    if action == "path":
        print(str(config_path))
        return 0

    if action == "base":
        profile_name = active_profile or DEFAULT_PROFILE
        profile = dict(profiles.get(profile_name) or {})
        if not name:
            print(profile.get("baseUrl") or DEFAULT_BASE_URL)
            return 0
        base_url = normalize_base_url(str(name))
        profile["baseUrl"] = base_url
        profiles[profile_name] = profile
        save_config(
            _ai_config_path(args.config),
            {"active": profile_name, "profiles": profiles},
        )
        print(f"✅ 已切换服务地址：{base_url}")
        print(f"   Profile：{profile_name}")
        return 0

    def profile_rows() -> List[Dict[str, Any]]:
        rows = []
        for profile_name in _profile_names(profiles):
            data = profiles.get(profile_name) or {}
            key = str(data.get("apiKey") or "")
            rows.append(
                {
                    "name": profile_name,
                    "active": profile_name == active_profile,
                    "configured": bool(key),
                    "apiKey": mask_key(key) if key else "",
                    "baseUrl": data.get("baseUrl") or DEFAULT_BASE_URL,
                    "apiName": data.get("apiName") or "",
                    "model": data.get("model") or "",
                }
            )
        return rows

    if action == "list":
        print(
            json.dumps(
                {
                    "configPath": str(config_path),
                    "activeProfile": active_profile,
                    "profiles": profile_rows(),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if action in ("use", "remove"):
        if not name:
            raise SkillError(
                f"config {action} 需要 profile 名称。",
                hint="例如：config use work / config remove work",
                code="profile",
                exit_code=EXIT_CONFIG,
            )
        if name not in profiles:
            raise SkillError(
                f"profile 不存在：{name}",
                hint="可用 profile：" + (", ".join(_profile_names(profiles)) or "(none)"),
                code="profile",
                exit_code=EXIT_CONFIG,
            )
        if action == "use":
            active_profile = name
            print(f"✅ 已切换 profile：{name}")
        else:
            if name == active_profile:
                raise SkillError(
                    "不能删除当前 active profile。",
                    hint="先用 `config use <其他 profile>` 切换，再删除。",
                    code="profile",
                    exit_code=EXIT_CONFIG,
                )
            profiles.pop(name, None)
            print(f"✅ 已删除 profile：{name}")
        save_config(
            _ai_config_path(args.config),
            {"active": active_profile, "profiles": profiles},
        )
        return 0

    # show
    requested = str(getattr(args, "profile", None) or active_profile or DEFAULT_PROFILE)
    data = profiles.get(requested)
    if data is None and profiles:
        raise SkillError(
            f"profile 不存在：{requested}",
            hint="可用 profile：" + (", ".join(_profile_names(profiles)) or "(none)"),
            code="profile",
            exit_code=EXIT_CONFIG,
        )
    data = data or {}
    key = str(data.get("apiKey") or "")
    print(
        json.dumps(
            {
                "configPath": str(config_path),
                "activeProfile": active_profile,
                "profile": requested,
                "configured": bool(key),
                "apiKey": mask_key(key) if key else "",
                "baseUrl": data.get("baseUrl") or DEFAULT_BASE_URL,
                "apiName": data.get("apiName") or "",
                "model": data.get("model") or "",
                "profiles": profile_rows(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def whoami(settings: Dict[str, Any], json_mode: bool) -> Dict[str, Any]:
    key = require_key(settings)
    status, payload = http_json(
        settings["base_url"], "/user/getUserData?lang=zh", api_key=key, timeout=30
    )
    if status >= 400:
        raise api_error(payload, status)
    check_api(payload, status)
    data = payload.get("data") or {}
    if not isinstance(data, dict):
        data = {}
    info = {
        "ok": True,
        "account": data.get("account") or data.get("name_zh") or "",
        "folderName": str(data.get("folderName") or ""),
        "tokenUsed": data.get("tokenUsed"),
        "tokenLimit": data.get("tokenLimit"),
        "baseUrl": settings["base_url"],
    }
    if json_mode:
        print(json.dumps(info, ensure_ascii=False))
    else:
        print("✅ API Key 有效")
        print(f"   账号：{info['account'] or '-'}")
        print(f"   folderName：{info['folderName'] or '-'}")
        if info.get("tokenLimit") is not None or info.get("tokenUsed") is not None:
            print(f"   积分：已用 {info.get('tokenUsed')} / 上限 {info.get('tokenLimit')}")
    return info


def cmd_whoami(args: argparse.Namespace) -> int:
    settings = resolve_settings(args)
    whoami(settings, json_mode=args.json)
    return 0


# ---------------------------------------------------------------------------
# Offline preview: works in marketplace sandboxes (no network, no API key)
# ---------------------------------------------------------------------------

SAMPLE_APPS = [
    {
        "id": "11111111111111111111111111111111",
        "title": "季度汇报大纲助手",
        "type": "agent",
        "documentType": "agent",
        "description": "把季度数据整理成分点汇报大纲（示例数据，非真实应用）",
    },
    {
        "id": "22222222222222222222222222222222",
        "title": "演示文稿生成器",
        "type": "skill",
        "documentType": "skill",
        "description": "根据大纲生成可打开的演示文稿（示例数据，非真实应用）",
    },
]

DEMO_INPUT = "把本季度三条业务线的关键数据整理成一份 8 页汇报，并生成可打开的 PPT 链接。"


def _preview_input(args: Optional[argparse.Namespace], label: str) -> str:
    if args is None:
        return DEMO_INPUT
    if getattr(args, "input", None):
        return str(args.input).strip() or DEMO_INPUT
    if getattr(args, "file", None):
        path = Path(str(args.file)).expanduser()
        if not path.exists():
            raise SkillError(f"输入文件不存在：{path}", code="bad_input", exit_code=EXIT_CONFIG)
        return path.read_text(encoding="utf-8", errors="replace").strip() or DEMO_INPUT
    if getattr(args, "stdin", False):
        return sys.stdin.read().strip() or DEMO_INPUT
    return DEMO_INPUT


def _offline_preview(kind: str, args: Optional[argparse.Namespace] = None) -> Dict[str, Any]:
    """Build a truthful offline preview. Contains sample data only, no network I/O."""
    result: Dict[str, Any] = {
        "ok": True,
        "mode": "dry-run",
        "network": False,
        "created": False,
        "sample": True,
        "note": "离线预览：使用示例数据，未联网、未读取账号、未消耗积分、未创建任何文档。配置 API Key 后去掉 --dry-run 即为真实执行。",
        "next": "python3 scripts/transweb_ai.py configure --verify",
    }
    if kind == "list":
        result.update({
            "command": "list",
            "count": len(SAMPLE_APPS),
            "apps": SAMPLE_APPS,
            "preview": {
                "steps": [
                    "POST /user/getLoginedData 读取账号下可用应用（离线时用示例清单代替）",
                    "按 --query / --source / --limit 过滤并排序",
                    "输出应用 ID、标题、类型（agent/skill）与描述",
                    "把选中的 ID 传给 run，或用 ppt 走固定演示文稿应用",
                ],
                "filters": {
                    "query": getattr(args, "query", None) if args else None,
                    "source": getattr(args, "source", "auto") if args else "auto",
                    "limit": getattr(args, "limit", 100) if args else 100,
                },
            },
        })
    elif kind == "run":
        ids = []
        for raw in (getattr(args, "ids", None) or ["11111111111111111111111111111111"]) if args else ["11111111111111111111111111111111"]:
            for item in str(raw).split(","):
                if item.strip():
                    ids.append(item.strip())
        text = _preview_input(args, "需求描述")
        chain = getattr(args, "chain_mode", "result") if args else "result"
        result.update({
            "command": "run",
            "ids": ids,
            "inputChars": len(text),
            "chainMode": chain,
            "preview": {
                "steps": [
                    f"第 1 步：调用应用 {ids[0] if ids else '（示例 ID）'}，传入需求描述",
                    "第 2 步：把上一步结果作为下一步输入（chainMode=" + chain + "）",
                    "逐步归档得到每个应用的文档 ID（默认保持私有，--share 才公开）",
                    "Agent 类型输出文本结果；Skill 类型输出可打开的应用链接",
                ],
                "outputs": [
                    {"id": ids[0] if ids else "示例", "type": "agent", "output": "文本结果（示例）"},
                    {"id": ids[1] if len(ids) > 1 else "22222222222222222222222222222222", "type": "skill", "output": None},
                ],
                "links": [],
            },
        })
    elif kind == "ppt":
        text = _preview_input(args, "PPT 需求")
        result.update({
            "command": "ppt",
            "inputChars": len(text),
            "appId": getattr(args, "app_id", PPT_APP_ID) if args else PPT_APP_ID,
            "preview": {
                "title": "季度业务汇报（示例）",
                "slideOutline": [
                    "封面：汇报主题与时间范围",
                    "业务总览：三条业务线的关键指标",
                    "线一：进展、问题与下阶段动作",
                    "线二：进展、问题与下阶段动作",
                    "线三：进展、问题与下阶段动作",
                    "横向对比与资源诉求",
                    "风险与应对",
                    "结论与下一步计划",
                ],
                "steps": [
                    "识别为 PPT 需求，固定映射到演示文稿应用",
                    "把大纲整理成结构化提示词并提交生成",
                    "等待存档、设置分享权限，写入 documentType",
                    "返回演示文稿标题、页大纲与可打开链接",
                ],
                "link": None,
            },
        })
    else:
        result.update({
            "command": "demo",
            "preview": {
                "workflow": [
                    {"step": 1, "command": "list", "output": "可用应用清单（示例）"},
                    {"step": 2, "command": "run", "output": "串联执行结果 / 应用链接"},
                    {"step": 3, "command": "ppt", "output": "演示文稿页大纲 + 链接"},
                ],
                "list": _offline_preview("list")["apps"],
                "run": _offline_preview("run")["preview"],
                "ppt": _offline_preview("ppt")["preview"],
            },
        })
    return result


def _brief(item: Any) -> str:
    if isinstance(item, dict):
        return ", ".join(f"{k}={v}" for k, v in list(item.items())[:3])
    return str(item)


def _print_preview(result: Dict[str, Any], json_mode: bool) -> int:
    if json_mode:
        print(json.dumps(result, ensure_ascii=False))
        return 0
    print(f"🔍 离线预览（示例数据，未真实执行）：{result.get('command', 'demo')}")
    preview = result.get("preview", {})
    if isinstance(preview, dict):
        for key, value in preview.items():
            print(f"   {key}:")
            if isinstance(value, list):
                for item in value[:8]:
                    print(f"     - {_brief(item)}")
            elif isinstance(value, dict):
                for k, v in list(value.items())[:6]:
                    print(f"     - {k}: {_brief(v)}")
            else:
                print(f"     {value}")
    elif isinstance(preview, list):
        for item in preview[:8]:
            print(f"     - {_brief(item)}")
    print(f"   {result['note']}")
    print(f"   下一步：{result['next']}")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    """Offline demo entry point: no key, no network, always produces a preview."""
    return _print_preview(
        _offline_preview(getattr(args, "kind", "workflow"), args),
        bool(getattr(args, "json", False)),
    )


def cmd_list(args: argparse.Namespace) -> int:
    if getattr(args, "dry_run", False):
        return _print_preview(_offline_preview("list", args), args.json)
    settings = resolve_settings(args)
    key = require_key(settings)
    base_url = settings["base_url"]
    limit = max(1, min(int(args.limit or 100), 500))
    query = (args.query or "").strip()
    source_arg = args.source

    own: List[Dict[str, Any]] = []
    published: List[Dict[str, Any]] = []
    own_error: Optional[SkillError] = None

    if source_arg in ("auto", "mine", "both"):
        try:
            own = fetch_apps(
                base_url,
                key,
                include_all=args.all,
                timeout=args.timeout,
            )
        except SkillError as exc:
            # 只有缺 doc:read 时才允许用公开市场兜底；Key 无效/过期应直接报错，
            # 否则用户会误以为新 Key 已经生效。
            if source_arg == "mine" or exc.code != "scope":
                raise
            own_error = exc
            own = []

    def own_matches() -> List[Dict[str, Any]]:
        if query:
            return search_apps(own, query, limit)
        return own[:limit]

    def published_matches() -> List[Dict[str, Any]]:
        if query:
            return search_apps(published, query, limit)
        return published[:limit]

    fallback = False
    selected_source = source_arg

    if source_arg == "mine":
        selected = own_matches()
        selected_source = "mine"
    elif source_arg == "published":
        published = fetch_published_apps(
            base_url, key, timeout=args.timeout
        )
        selected = published_matches()
        selected_source = "published"
    elif source_arg == "both":
        published = fetch_published_apps(
            base_url, key, timeout=args.timeout
        )
        selected = _merge_apps(own_matches(), published_matches())
        selected = selected[:limit]
        selected_source = "both"
    else:  # auto
        selected = own_matches()
        if selected:
            selected_source = "mine"
        else:
            published = fetch_published_apps(
                base_url, key, timeout=args.timeout
            )
            selected = published_matches()
            selected_source = "published"
            fallback = True

    total = len(selected)
    if len(selected) > limit:
        selected = selected[:limit]

    if getattr(args, "with_document_type", False):
        type_cache: Dict[str, str] = {}
        for app in selected:
            app_id = str(app.get("id") or "")
            if app_id:
                app["documentType"] = (
                    fetch_document_type(
                        base_url, key, app_id, timeout=30, cache=type_cache
                    )
                    or "skill"
                )

    result: Dict[str, Any] = {
        "ok": True,
        "source": source_arg,
        "selectedSource": selected_source,
        "fallback": fallback,
        "ownTotal": len(own),
        "publishedTotal": len(published) if published else None,
        "total": total,
        "returned": len(selected),
        "publishedOnly": not args.all,
        "query": query,
        "apps": selected,
    }

    notes: List[str] = []
    if own_error is not None:
        notes.append(
            f"读取自建应用失败（{own_error.message}），已改用公开市场应用。"
        )
    if fallback:
        notes.append(
            "自建应用（getLoginedData）中没有匹配，已回退到公开市场"
            "（getPublishedList）。"
        )
    if total > len(selected):
        notes.append(
            f"共匹配 {total} 个应用，仅返回 {len(selected)} 个；"
            "可用 --limit 调整。"
        )
    if (
        source_arg == "auto"
        and selected_source == "mine"
        and not query
    ):
        notes.append(
            "默认优先返回自建应用；需要公开市场时用 --source published/both，"
            "或加 --query 让 auto 自动判断并回退。"
        )
    if notes:
        result["note"] = " ".join(notes)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _chain_input(
    mode: str, original: str, content: str
) -> str:
    if mode == "requirement":
        return original
    if mode == "both":
        return f"{original}\n\n---\n上一步输出：\n{content}"
    return content


def cmd_ppt(args: argparse.Namespace) -> int:
    """PPT 专用入口：固定演示文稿应用，输出 title/slides 和链接。"""
    if getattr(args, "dry_run", False):
        return _print_preview(_offline_preview("ppt", args), args.json)
    settings = resolve_settings(args)
    key = require_key(settings)
    base_url = settings["base_url"]
    timeout = settings["timeout"]
    app_id = args.app_id or PPT_APP_ID

    if args.input is not None:
        original = args.input
    elif args.file:
        path = Path(args.file).expanduser()
        if not path.exists():
            raise SkillError(
                f"输入文件不存在：{path}", code="bad_input", exit_code=EXIT_CONFIG
            )
        original = path.read_text(encoding="utf-8", errors="replace")
    elif args.stdin:
        original = sys.stdin.read()
    else:
        raise SkillError(
            "缺少 PPT 大纲或需求描述。",
            hint="使用 --input、--file 或 --stdin 传入。",
            code="bad_input",
            exit_code=EXIT_CONFIG,
        )
    original = original.strip()
    if not original:
        raise SkillError(
            "PPT 大纲或需求描述为空。", code="bad_input", exit_code=EXIT_CONFIG
        )

    if not args.quiet:
        eprint(f"⏳ 正在用「演示文稿」应用生成 PPT（{app_id}）...")

    body: Dict[str, Any] = {"documentId": app_id, "context": original}
    if settings["api_name"]:
        body["apiName"] = settings["api_name"]
    if settings["model"]:
        body["model"] = settings["model"]

    started = time.time()
    status, payload = http_json(
        base_url,
        "/gpt/aiGatewayRequest",
        api_key=key,
        method="POST",
        body=body,
        timeout=timeout,
    )
    if status >= 400:
        raise api_error(payload, status)
    check_api(payload, status)

    content = extract_generated_text(payload)
    if not content.strip():
        raise SkillError(
            "接口返回成功，但内容为空。",
            hint="可能是上游模型异常；请重试。",
            code="invalid_output",
            exit_code=EXIT_OUTPUT,
        )
    try:
        json_text, deck = extract_json_object(content)
    except SkillError:
        raise SkillError(
            "PPT 应用没有返回有效的 JSON 演示文稿。",
            hint=f"原始输出开头：{content[:300]}",
            code="invalid_output",
            exit_code=EXIT_OUTPUT,
        )
    slides = deck.get("slides")
    if not isinstance(slides, list) or not slides:
        raise SkillError(
            "PPT 输出缺少非空的 slides 数组。",
            hint="请把大纲写得更具体（主题、章节、每页要点）后重试。",
            code="invalid_output",
            exit_code=EXIT_OUTPUT,
        )
    title = str(deck.get("title") or "").strip()

    account = fetch_account(base_url, key)
    folder_name = None
    if account:
        folder_name = str(account.get("folderName") or "") or None

    if not args.quiet:
        eprint("⏳ 生成完成，正在查询文档存档 ...")
    data_id = find_archived_data_id(
        base_url,
        key,
        app_id,
        content,
        json_text,
        deck,
        folder_name=folder_name,
        wait_seconds=args.wait,
        timeout=60,
    )
    if not data_id:
        fallback = settings["config_path"].parent / "transweb-ppt-last-deck.json"
        try:
            save_config(fallback, deck)
            fallback_hint = f"生成结果已保存到 {fallback}。"
        except Exception:  # noqa: BLE001
            fallback_hint = "生成结果未能保存到本地。"
        raise SkillError(
            "PPT 已生成，但在文档存档中没有找到对应版本。",
            hint=(
                f"{fallback_hint} 请确认生成已正常计费/记录，"
                "或稍后用 --wait 30 重试。"
            ),
            code="archive_not_found",
            exit_code=EXIT_SAVE,
        )

    accessible = False
    access_error = ""
    if args.share:
        accessible, access_error = make_record_accessible(
            base_url, key, str(data_id), timeout=30
        )
        if not accessible and not args.quiet:
            eprint(f"⚠️  访问权限设置失败：{access_error}")

    link = (
        f"{base_url}/?solo=true&dataView=true&dataId="
        f"{urllib.parse.quote(str(data_id))}&id={app_id}"
    )
    usage = payload.get("usage") if isinstance(payload.get("usage"), dict) else {}
    result: Dict[str, Any] = {
        "ok": True,
        "link": link,
        "dataId": str(data_id),
        "documentId": app_id,
        "title": title,
        "slides": len(slides),
        "pointsCost": usage.get("pointsCost"),
        "archived": True,
        "accessible": accessible,
        "elapsedMs": int((time.time() - started) * 1000),
    }
    if not accessible and access_error:
        result["accessError"] = access_error

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
        return 0

    print(f"✅ 已生成：{title or '未命名演示文稿'}")
    print(f"🔗 链接：{link}")
    print(f"📄 页数：{len(slides)}")
    if args.share:
        if accessible:
            print("🔓 访问权限：已设为公开可访问（--share）")
        else:
            print(f"🔓 访问权限：设置失败：{access_error}")
    else:
        print("🔒 访问权限：保持私有（默认，未分享）")
    if result["pointsCost"] is not None:
        print(f"⚡ 本次消耗：{result['pointsCost']} 积分")
    print(f"⏱  耗时：{result['elapsedMs'] / 1000:.1f}s")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    if getattr(args, "dry_run", False):
        return _print_preview(_offline_preview("run", args), args.json)
    settings = resolve_settings(args)
    key = require_key(settings)
    base_url = settings["base_url"]
    timeout = settings["timeout"]

    ids: List[str] = []
    for raw in args.ids or []:
        for item in str(raw).split(","):
            item = item.strip()
            if item:
                ids.append(item)
    if not ids:
        raise SkillError(
            "缺少应用 ID。",
            hint="先运行 list 获取 ID，再用 --ids id1,id2 传入。",
            code="bad_input",
            exit_code=EXIT_CONFIG,
        )
    for app_id in ids:
        if not re.fullmatch(r"[0-9a-fA-F]{32}", app_id):
            raise SkillError(
                f"应用 ID 格式不正确：{app_id}",
                hint="transweb 应用 ID 是 32 位十六进制字符串。",
                code="bad_input",
                exit_code=EXIT_CONFIG,
            )

    if args.input is not None:
        original = args.input
    elif args.file:
        path = Path(args.file).expanduser()
        if not path.exists():
            raise SkillError(
                f"输入文件不存在：{path}",
                code="bad_input",
                exit_code=EXIT_CONFIG,
            )
        original = path.read_text(encoding="utf-8", errors="replace")
    elif args.stdin:
        original = sys.stdin.read()
    else:
        raise SkillError(
            "缺少需求描述。",
            hint="使用 --input、--file 或 --stdin 传入。",
            code="bad_input",
            exit_code=EXIT_CONFIG,
        )
    original = original.strip()
    if not original:
        raise SkillError("需求描述为空。", code="bad_input", exit_code=EXIT_CONFIG)

    if not args.quiet:
        eprint(f"⏳ 准备串行执行 {len(ids)} 个应用 ...")

    account = fetch_account(base_url, key)
    folder_name = None
    if account:
        folder_name = str(account.get("folderName") or "") or None

    current_input = original
    steps: List[Dict[str, Any]] = []
    total_started = time.time()
    type_cache: Dict[str, str] = {}

    def print_step(step: Dict[str, Any]) -> None:
        if step.get("documentType") == "agent":
            print(f"✅ [{step['index']}] {step['appId']} (agent)")
            print(step.get("result", ""))
        else:
            print(f"✅ [{step['index']}] {step['appId']} -> {step.get('link', '')}")

    for index, app_id in enumerate(ids, 1):
        document_type = fetch_document_type(
            base_url, key, app_id, timeout=30, cache=type_cache
        ) or "skill"
        if not args.quiet:
            eprint(
                f"▶️  [{index}/{len(ids)}] 调用 {app_id} "
                f"({document_type}) ..."
            )
        step_started = time.time()
        body: Dict[str, Any] = {"documentId": app_id, "context": current_input}
        if settings["api_name"]:
            body["apiName"] = settings["api_name"]
        if settings["model"]:
            body["model"] = settings["model"]
        try:
            status, payload = http_json(
                base_url,
                "/gpt/aiGatewayRequest",
                api_key=key,
                method="POST",
                body=body,
                timeout=timeout,
            )
            if status >= 400:
                raise api_error(payload, status)
            check_api(payload, status)

            content = extract_generated_text(payload)
            if not content.strip():
                raise SkillError(
                    "接口返回成功，但内容为空。",
                    hint="可能是上游模型异常；可换一个应用或重试。",
                    code="invalid_output",
                    exit_code=EXIT_OUTPUT,
                )
            usage = payload.get("usage") if isinstance(payload.get("usage"), dict) else {}

            if document_type == "agent":
                # Agent 应用只输出字符串结果，不生成 dataId/链接。
                step = {
                    "index": index,
                    "appId": app_id,
                    "documentType": "agent",
                    "result": content,
                    "chars": len(content),
                    "pointsCost": usage.get("pointsCost"),
                    "elapsedMs": int((time.time() - step_started) * 1000),
                }
                steps.append(step)
                if not args.quiet:
                    preview = content[:120].replace("\n", " ")
                    eprint(f"   ✅ agent 结果：{preview}")
            else:
                parsed = None
                json_text = ""
                try:
                    json_text, parsed = extract_json_object(content)
                except SkillError:
                    pass

                if not args.quiet:
                    eprint(f"   ↳ 已生成 {len(content)} 字符，查询存档 ...")
                data_id = find_archived_data_id(
                    base_url,
                    key,
                    app_id,
                    content,
                    json_text,
                    parsed,
                    folder_name=folder_name,
                    wait_seconds=args.wait,
                    timeout=60,
                )
                if not data_id:
                    raise SkillError(
                        "生成成功，但文档存档中没有找到对应版本。",
                        hint="加 --wait 30 重试；确认该应用已正常计费/记录。",
                        code="archive_not_found",
                        exit_code=EXIT_SAVE,
                    )

                accessible = False
                access_error = ""
                if args.share:
                    accessible, access_error = make_record_accessible(
                        base_url, key, str(data_id), timeout=30
                    )
                    if not accessible and not args.quiet:
                        eprint(f"   ⚠️  访问权限设置失败：{access_error}")

                link = (
                    f"{base_url}/?solo=true&dataView=true&dataId="
                    f"{urllib.parse.quote(str(data_id))}&id={app_id}"
                )
                step = {
                    "index": index,
                    "appId": app_id,
                    "documentType": "skill",
                    "link": link,
                    "dataId": str(data_id),
                    "accessible": accessible,
                    "chars": len(content),
                    "pointsCost": usage.get("pointsCost"),
                    "elapsedMs": int((time.time() - step_started) * 1000),
                }
                if not accessible and access_error:
                    step["accessError"] = access_error
                steps.append(step)
                if not args.quiet:
                    eprint(f"   ✅ {link}")

            if index < len(ids):
                current_input = _chain_input(args.chain_mode, original, content)
        except SkillError as exc:
            result = {
                "ok": False,
                "error": exc.message,
                "hint": exc.hint,
                "code": exc.code,
                "completed": steps,
                "failedAppId": app_id,
                "failedIndex": index,
                "elapsedMs": int((time.time() - total_started) * 1000),
            }
            if args.json:
                print(json.dumps(result, ensure_ascii=False))
            else:
                for step in steps:
                    print_step(step)
                eprint(f"❌ 第 {index} 步失败（{app_id}）：{exc.message}")
                if exc.hint:
                    eprint(f"   {exc.hint}")
            return exc.exit_code

    points = [step["pointsCost"] for step in steps if isinstance(step["pointsCost"], (int, float))]
    last = steps[-1]
    result: Dict[str, Any] = {
        "ok": True,
        "finalAppId": last["appId"],
        "documentType": last.get("documentType", "skill"),
        "steps": steps,
        "pointsCost": sum(points) if points else None,
        "elapsedMs": int((time.time() - total_started) * 1000),
    }
    if last.get("documentType") == "agent":
        result["result"] = last.get("result", "")
    else:
        result["link"] = last.get("link", "")
        result["dataId"] = last.get("dataId", "")

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
        return 0

    for step in steps:
        print(f"步骤 {step['index']}：{step['appId']} ({step.get('documentType', 'skill')})")
        if step.get("documentType") == "agent":
            print(step.get("result", ""))
        else:
            print(f"  链接：{step.get('link', '')}")
        if step.get("pointsCost") is not None:
            print(f"  消耗：{step['pointsCost']} 积分")
    if result.get("documentType") == "agent":
        print("🏁 最终结果：")
        print(result.get("result", ""))
    else:
        print(f"🏁 最终链接：{result.get('link', '')}")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def cmd_selftest(args: argparse.Namespace) -> int:
    """Offline package check for marketplace sandboxes (no network, no key)."""
    root = Path(__file__).resolve().parents[1]
    checks = []

    def add(name: str, ok: bool, detail: str = "", required: bool = True) -> None:
        checks.append({"name": name, "ok": bool(ok), "detail": detail, "required": required})

    add("python", sys.version_info >= (3, 9), sys.version.split()[0])
    for rel in ("SKILL.md", "README.md", "references/api.md", "scripts/transweb_ai.py", "tests/test_cli.py"):
        path = root / rel
        add("file:" + rel, path.exists(), str(path) if path.exists() else "missing")

    frontmatter = ""
    try:
        text = (root / "SKILL.md").read_text(encoding="utf-8", errors="replace")
        match = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
        frontmatter = match.group(1) if match else ""
    except OSError:
        frontmatter = ""
    for field in (
        "name",
        "description",
        "display_name",
        "display_name_en",
        "description_zh",
        "description_en",
        "version",
        "author",
        "examples_zh",
        "examples_en",
    ):
        found = bool(re.search(r"^" + re.escape(field) + r":\s*\S", frontmatter, re.M))
        add("frontmatter:" + field, found, "present" if found else "missing")
    add(
        "frontmatter:name-value",
        bool(re.search(r"^name:\s*" + re.escape(SKILL_NAME) + r"\s*$", frontmatter, re.M)),
        SKILL_NAME,
    )
    ver_match = re.search(r"^version:\s*(\S+)", frontmatter, re.M)
    add(
        "version-match",
        bool(ver_match and ver_match.group(1).strip("\"'") == SKILL_VERSION),
        f"SKILL.md={ver_match.group(1) if ver_match else 'missing'} / script={SKILL_VERSION}",
    )
    preview = _offline_preview("demo")
    pv = preview.get("preview", {})
    add(
        "offline-preview",
        preview.get("ok") is True
        and preview.get("created") is False
        and preview.get("network") is False
        and len(pv.get("workflow", [])) >= 3,
        "full workflow preview generated with no network call",
    )

    add("bin:python3", bool(shutil.which("python3")), shutil.which("python3") or "missing")
    add(
        "bin:curl",
        bool(shutil.which("curl")),
        shutil.which("curl") or "missing (required only for upload)",
        required=False,
    )

    key_pattern = re.compile(r"ak_live_[A-Za-z0-9]{20,}")
    hits = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".py", ".md", ".json", ".txt", ".yaml", ".yml"}:
            continue
        try:
            if path.stat().st_size > 2 * 1024 * 1024:
                continue
            if key_pattern.search(path.read_text(encoding="utf-8", errors="replace")):
                hits.append(str(path.relative_to(root)))
        except OSError:
            pass
    add("no-api-key", not hits, ", ".join(hits) if hits else "none")

    config_path = default_config_path()
    add(
        "config",
        True,
        f"{config_path} ({'exists' if config_path.exists() else 'not configured; run configure'})",
        required=False,
    )
    add("network", True, "no network calls (by design)", required=False)

    ok = all(item["ok"] for item in checks if item["required"])
    result = {"ok": ok, "skill": SKILL_NAME, "version": SKILL_VERSION, "checks": checks}
    if getattr(args, "json", False):
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"{'✅' if ok else '❌'} selftest {SKILL_NAME} {SKILL_VERSION}")
        for item in checks:
            mark = "✅" if item["ok"] else ("⚠️" if not item["required"] else "❌")
            print(f"  {mark} {item['name']}: {item['detail']}")
        print("  ✅ no network calls were made")
    return 0 if ok else EXIT_CONFIG


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--config",
        help="配置文件路径（默认搜索 .transweb-ai.json / .dsh/transweb-ai.json / XDG；不读取其他技能的 Key）",
    )
    common.add_argument("--base-url", help=f"服务地址（默认 {DEFAULT_BASE_URL}）")
    common.add_argument("--api-key", help="API Key（建议用 configure 或环境变量）")
    common.add_argument("--profile", help="使用指定 API Key profile（默认 active）")
    common.add_argument("--api-name", help="覆盖模型供应方 apiName")
    common.add_argument("--model", help="覆盖模型")

    parser = argparse.ArgumentParser(
        prog="transweb_ai.py",
        description="列出并执行 transweb.cn 账号下的 AI 应用：Agent 输出字符串，Skill 输出链接。",
    )
    parser.add_argument("--version", action="version", version="%(prog)s " + SKILL_VERSION)
    sub = parser.add_subparsers(dest="command", required=True)

    p_selftest = sub.add_parser("selftest", help="离线自检：不联网、不需要 API Key")
    p_selftest.add_argument("--json", action="store_true", help="输出 JSON")

    p_demo = sub.add_parser("demo", help="离线演示：不联网、不需要 Key，输出工作流预览")
    p_demo.add_argument("kind", nargs="?", choices=["workflow", "list", "run", "ppt"],
                        default="workflow", help="预览范围，默认 workflow（完整工作流）")
    p_demo.add_argument("--json", action="store_true", help="输出 JSON")

    p_conf = sub.add_parser("configure", help="保存 transweb.cn API Key 配置")
    p_conf.add_argument("--api-key-stdin", action="store_true", help="从 stdin 读取 Key")
    p_conf.add_argument("--verify", action="store_true", help="保存后调用 whoami 验证")
    p_conf.add_argument("--config", help="配置文件路径")
    p_conf.add_argument("--base-url", help=f"服务地址（默认 {DEFAULT_BASE_URL}）")
    p_conf.add_argument("--api-key", help="API Key（会进入 shell 历史）")
    p_conf.add_argument("--profile", help="profile 名称（默认当前 active；新名称会创建并切换）")
    p_conf.add_argument("--api-name", help="默认模型供应方 apiName")
    p_conf.add_argument("--model", help="默认模型")

    p_show = sub.add_parser("config", help="查看/切换 API Key profile（Key 脱敏）")
    p_show.add_argument(
        "action",
        nargs="?",
        choices=["show", "path", "list", "use", "remove", "base"],
        default="show",
        help="show（默认）/ path / list / use / remove / base",
    )
    p_show.add_argument(
        "name",
        nargs="?",
        help="use/remove 的 profile 名称；base 时为服务地址，如 http://localhost",
    )
    p_show.add_argument("--profile", help="show 指定 profile（默认 active）")
    p_show.add_argument("--config", help="配置文件路径")

    p_who = sub.add_parser("whoami", help="校验 API Key", parents=[common])
    p_who.add_argument("--json", action="store_true", help="输出 JSON")

    p_list = sub.add_parser("list", help="列出账号下可用的 AI Skill ID", parents=[common])
    p_list.add_argument(
        "--source",
        choices=["auto", "mine", "published", "both"],
        default="auto",
        help="auto=优先自建、无匹配回退公开市场（默认）；mine=仅自建；published=仅公开市场；both=两者",
    )
    p_list.add_argument("--all", action="store_true", help="包含未发布的自建应用（可能很多）")
    p_list.add_argument("--query", help="按标题/描述/标签/类型关键词过滤")
    p_list.add_argument("--limit", type=int, default=100, help="最多返回数量（默认 100）")
    p_list.add_argument("--timeout", type=int, default=60, help="列表请求超时秒数")
    p_list.add_argument("--dry-run", action="store_true",
                         help="离线预览：不联网、不需要 Key，只输出应用清单示例")
    p_list.add_argument("--json", action="store_true", help="输出 JSON（list 默认就是 JSON）")
    p_list.add_argument(
        "--with-document-type",
        action="store_true",
        help="逐个查询 documentType（agent/skill），会增加请求次数",
    )

    p_ppt = sub.add_parser(
        "ppt",
        help="PPT 专用：识别做 PPT 的需求，固定用演示文稿应用生成",
        parents=[common],
    )
    ppt_source = p_ppt.add_mutually_exclusive_group(required=True)
    ppt_source.add_argument("--input", help="PPT 大纲或需求描述")
    ppt_source.add_argument("--file", help="从文件读取大纲")
    ppt_source.add_argument("--stdin", action="store_true", help="从 stdin 读取大纲")
    p_ppt.add_argument("--app-id", default=PPT_APP_ID, help="覆盖演示文稿应用 ID")
    p_ppt.add_argument("--share", action="store_true", help="显式将生成结果设为公开可访问（默认私有）")
    p_ppt.add_argument("--wait", type=int, default=DEFAULT_WAIT, help="等待存档秒数")
    p_ppt.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="生成超时")
    p_ppt.add_argument("--dry-run", action="store_true",
                         help="离线预览：不联网、不需要 Key，只输出 PPT 结构草案")
    p_ppt.add_argument("--json", action="store_true", help="输出 JSON")
    p_ppt.add_argument("--quiet", action="store_true", help="不输出进度")

    p_run = sub.add_parser("run", help="串行执行一个或多个 AI Skill", parents=[common])
    p_run.add_argument(
        "--ids",
        action="append",
        required=True,
        help="应用 ID，逗号分隔或重复传 --ids",
    )
    source = p_run.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", help="需求描述")
    source.add_argument("--file", help="从文件读取需求")
    source.add_argument("--stdin", action="store_true", help="从 stdin 读取需求")
    p_run.add_argument(
        "--chain-mode",
        choices=["result", "requirement", "both"],
        default="result",
        help="多步时下一步的输入：上一步结果（默认）/ 原始需求 / 两者",
    )
    p_run.add_argument("--share", action="store_true", help="显式将每步结果设为公开可访问（默认私有）")
    p_run.add_argument("--wait", type=int, default=DEFAULT_WAIT, help="等待存档秒数")
    p_run.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="单步生成超时")
    p_run.add_argument("--dry-run", action="store_true",
                         help="离线预览：不联网、不需要 Key，只输出串联步骤")
    p_run.add_argument("--json", action="store_true", help="输出 JSON")
    p_run.add_argument("--quiet", action="store_true", help="不输出进度")

    return parser


def main(argv: Optional[list] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    json_mode = bool(getattr(args, "json", False))

    try:
        if args.command == "selftest":
            return cmd_selftest(args)
        if args.command == "demo":
            return cmd_demo(args)
        if args.command == "configure":
            return cmd_configure(args)
        if args.command == "config":
            return cmd_config_show(args)
        if args.command == "whoami":
            return cmd_whoami(args)
        if args.command == "list":
            return cmd_list(args)
        if args.command == "ppt":
            return cmd_ppt(args)
        if args.command == "run":
            return cmd_run(args)
        parser.error("未知命令")
        return 1
    except SkillError as exc:
        if json_mode:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": exc.message,
                        "hint": exc.hint,
                        "code": exc.code,
                    },
                    ensure_ascii=False,
                )
            )
        else:
            eprint(f"❌ {exc.message}")
            if exc.hint:
                eprint(f"   {exc.hint}")
        return exc.exit_code
    except KeyboardInterrupt:
        eprint("❌ 已中断")
        return 1
    except Exception as exc:  # noqa: BLE001
        if json_mode:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": str(exc),
                        "hint": "",
                        "code": "unexpected",
                    },
                    ensure_ascii=False,
                )
            )
        else:
            eprint(f"❌ 未预期的错误：{exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
