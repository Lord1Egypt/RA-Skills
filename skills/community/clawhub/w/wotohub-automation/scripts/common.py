#!/usr/bin/env python3
from typing import Optional
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from config import BASE_URL, DEFAULT_SOURCEAPP, DEFAULT_API_KEY

try:
    import ssl
except Exception:  # pragma: no cover - environment-specific import guard
    ssl = None  # type: ignore[assignment]


def _build_ssl_context():
    if ssl is None:
        return None
    verify_tls = os.environ.get("WOTOHUB_VERIFY_TLS", "1").strip().lower() not in {"0", "false", "no"}
    if verify_tls:
        return ssl.create_default_context()
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context


_SSL_CONTEXT = _build_ssl_context()

_STATE_DIR = Path(os.environ.get("WOTOHUB_STATE_DIR", Path.home() / ".config" / "wotohub"))
_SETTINGS_PATH = _STATE_DIR / "settings.json"
_LOGS_DIR = _STATE_DIR / "logs"


def ensure_state_dir() -> Path:
    _STATE_DIR.mkdir(parents=True, exist_ok=True)
    _LOGS_DIR.mkdir(parents=True, exist_ok=True)
    return _STATE_DIR


def state_file(name: str) -> Path:
    ensure_state_dir()
    return _STATE_DIR / name


def log_file(name: str) -> Path:
    ensure_state_dir()
    return _LOGS_DIR / name


def _load_settings() -> dict:
    try:
        if _SETTINGS_PATH.exists():
            return json.loads(_SETTINGS_PATH.read_text())
    except Exception:
        pass
    return {}


def get_saved_token() -> Optional[str]:
    settings = _load_settings()
    token = (settings.get("apiKey") or settings.get("api_key") or "").strip()
    return token or None


def save_token(token: str) -> str:
    token = (token or "").strip()
    if not token:
        raise ValueError("api-key is empty")
    ensure_state_dir()
    settings = _load_settings()
    settings["apiKey"] = token
    _SETTINGS_PATH.write_text(json.dumps(settings, ensure_ascii=False, indent=2))
    return token


def _missing_token_message(feature: Optional[str] = None) -> str:
    feature_map = {
        "preflight": "鉴权预检",
        "inbox_list": "收件箱列表查询",
        "inbox_detail": "邮件详情查看",
        "inbox_dialogue": "对话详情查看",
        "send_email": "邮件发送",
        "reply_email": "邮件回复",
        "reply_assist": "reply assist / 收件箱监控",
        "reply_preview": "回复预览生成",
        "conversation_analysis": "对话分析输入构建",
        "conversation_context": "对话上下文构建",
    }
    feature_label = feature_map.get(feature) or "当前操作"
    return (
        f"This action requires a WotoHub api-key because it is a user-state operation ({feature_label}). "
        "Please provide it in one of these ways: \n"
        "1. Pass --token YOUR_API_KEY\n"
        "2. Set env WOTOHUB_API_KEY\n"
        "3. Save it into ~/.config/wotohub/settings.json\n"
        "Tip: search/product-analysis/recommend can run without api-key, but send/inbox/reply cannot."
    )



def get_token(cli_token: Optional[str]= None, required: bool = True, feature: Optional[str] = None) -> Optional[str]:
    token = cli_token or os.environ.get("WOTOHUB_API_KEY") or get_saved_token() or DEFAULT_API_KEY
    if cli_token:
        try:
            save_token(cli_token)
        except Exception:
            pass
    if required and not token:
        raise SystemExit(_missing_token_message(feature))
    return token


def build_headers(token: Optional[str]= None, json_body: bool = False) -> dict:
    headers = {
        "Sourceapp": DEFAULT_SOURCEAPP,
    }
    if token:
        headers["api-key"] = token
    if json_body:
        headers["Content-Type"] = "application/json"
    return headers


def request_json(method: str, path: str, token: Optional[str]= None, payload: Optional[dict]= None, timeout: int = 20, path_params: Optional[dict]= None) -> dict:
    url = BASE_URL.rstrip("/") + path
    if path_params:
        for key, val in path_params.items():
            url = url.replace(f"{{{key}}}", str(val))
    if url.startswith("https://") and ssl is None:
        raise RuntimeError(
            "HTTPS request requires Python ssl support, but ssl could not be imported. "
            "Fix the Python/OpenSSL installation in the runtime environment before calling WotoHub APIs."
        )
    data = None
    headers = build_headers(token, json_body=payload is not None)
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CONTEXT) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
    return json.loads(raw)


def is_success_response(resp: Optional[dict]) -> bool:
    if not isinstance(resp, dict):
        return False
    if resp.get("success") is True:
        return True
    code = resp.get("code")
    return code in {0, "0", 200, "200"}


def print_json(obj: dict):
    print(json.dumps(obj, ensure_ascii=False, indent=2))
