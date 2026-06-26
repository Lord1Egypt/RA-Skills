from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import mimetypes
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen
from uuid import uuid4

logger = logging.getLogger("qiniu")


def _get_output_root() -> Path:
    return Path(os.environ.get("OUTPUT_ROOT", "~/")).expanduser().resolve()


def log_params(event: str, **kwargs: Any) -> None:
    """Log an event with a provider prefix and JSON payload."""
    params_str = json.dumps(kwargs, ensure_ascii=False, default=str)
    logger.info("七牛 - %s | %s", event, params_str)


_trace_id: str = ""


def get_trace_id() -> str:
    global _trace_id
    if not _trace_id:
        _trace_id = uuid4().hex
    return _trace_id


class _TraceIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = get_trace_id()
        return True


def _ensure_logging() -> None:
    """Lazy init logging on first use."""
    if logger.handlers:
        return
    log_dir = _get_output_root() / "outputs" / "logs"
    trace_filter = _TraceIdFilter()
    log_fmt = "%(asctime)s [%(trace_id)s] %(levelname)s %(message)s"
    fmt = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
    log_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    file_handler = logging.FileHandler(log_dir / f"{today}.log", encoding="utf-8")
    file_handler.setFormatter(fmt)
    file_handler.addFilter(trace_filter)
    logger.addHandler(file_handler)
    error_handler = logging.FileHandler(log_dir / f"{today}.error.log", encoding="utf-8")
    error_handler.setFormatter(fmt)
    error_handler.addFilter(trace_filter)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)
    logger.setLevel(logging.INFO)


DEFAULT_UPLOAD_DOMAIN = "https://upload-z2.qiniup.com"

ENV_FIELD_MAP = {
    "access_key": "QINIU_ACCESS_KEY",
    "secret_key": "QINIU_SECRET_KEY",
    "bucket": "QINIU_BUCKET",
    "public_domain": "QINIU_PUBLIC_DOMAIN",
}
OPTIONAL_ENV_FIELD_MAP = {
    "is_private": "QINIU_IS_PRIVATE",
}


def parse_bool(value: Any, *, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if not normalized:
            return default
        if normalized in {"1", "true", "yes", "y", "on"}:
            return True
        if normalized in {"0", "false", "no", "n", "off"}:
            return False
    raise RuntimeError("七牛配置字段 is_private 只能是布尔值或可识别的 true/false 字符串")


def load_config() -> dict[str, Any]:
    config: dict[str, Any] = {}
    missing: list[str] = []
    for field, env_name in ENV_FIELD_MAP.items():
        value = os.getenv(env_name, "").strip()
        if value:
            config[field] = value
        else:
            missing.append(env_name)

    if missing:
        raise RuntimeError(
            f"缺少必要的环境变量: {', '.join(missing)}"
        )

    config["public_domain"] = normalize_domain(config["public_domain"])
    is_private_env = os.getenv(OPTIONAL_ENV_FIELD_MAP["is_private"])
    config["is_private"] = parse_bool(is_private_env, default=False)
    _ensure_logging()
    log_params("配置加载完成", bucket=config["bucket"], is_private=config["is_private"])
    return config


def urlsafe_base64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8")


def normalize_domain(domain: str) -> str:
    return domain.rstrip("/")


def build_public_url(domain: str, object_key: str) -> str:
    return f"{normalize_domain(domain)}/{quote(object_key)}"


def build_private_download_url(
    *,
    access_key: str,
    secret_key: str,
    base_url: str,
    expires_in: int = 600,
) -> str:
    deadline = int(time.time()) + expires_in
    separator = "&" if "?" in base_url else "?"
    signing_url = f"{base_url}{separator}e={deadline}"

    digest = hmac.new(
        secret_key.encode("utf-8"),
        signing_url.encode("utf-8"),
        hashlib.sha1,
    ).digest()
    encoded_sign = urlsafe_base64_encode(digest)
    token = f"{access_key}:{encoded_sign}"
    _ensure_logging()
    log_params("生成签名链接", base_url=base_url, expires_in=expires_in)
    return f"{signing_url}&token={token}"


def resolve_access_mode(
    *,
    is_private_bucket: bool,
    prefer_private: bool = False,
    prefer_public: bool = False,
) -> str:
    if prefer_private and prefer_public:
        raise ValueError("--private-url 和 --public-url 不能同时使用")
    if prefer_private:
        return "private"
    if prefer_public:
        return "public"
    return "private" if is_private_bucket else "public"


def build_upload_token(
    *,
    access_key: str,
    secret_key: str,
    bucket: str,
    object_key: str,
    expires_in: int = 3600,
) -> str:
    deadline = int(time.time()) + expires_in
    policy = {
        "scope": f"{bucket}:{object_key}",
        "deadline": deadline,
    }
    encoded_policy = urlsafe_base64_encode(
        json.dumps(policy, separators=(",", ":")).encode("utf-8")
    )
    digest = hmac.new(
        secret_key.encode("utf-8"),
        encoded_policy.encode("utf-8"),
        hashlib.sha1,
    ).digest()
    encoded_sign = urlsafe_base64_encode(digest)
    return f"{access_key}:{encoded_sign}:{encoded_policy}"


def encode_multipart_form(
    *,
    fields: list[tuple[str, str]],
    file_field: str,
    file_path: Path,
) -> tuple[bytes, str]:
    boundary = "----CodexQiniuFormBoundary7MA4YWxkTrZu0gW"
    chunks: list[bytes] = []

    for key, value in fields:
        chunks.append(f"--{boundary}\r\n".encode("utf-8"))
        chunks.append(
            f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8")
        )
        chunks.append(value.encode("utf-8"))
        chunks.append(b"\r\n")

    mime_type, _ = mimetypes.guess_type(file_path.name)
    if mime_type is None:
        mime_type = "application/octet-stream"

    chunks.append(f"--{boundary}\r\n".encode("utf-8"))
    chunks.append(
        (
            f'Content-Disposition: form-data; name="{file_field}"; '
            f'filename="{file_path.name}"\r\n'
        ).encode("utf-8")
    )
    chunks.append(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    chunks.append(file_path.read_bytes())
    chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks), boundary


def upload_file(
    *,
    file_path: Path,
    object_key: str,
    config: dict[str, Any],
    upload_domain: str | None = None,
    token_expires_in: int = 3600,
) -> dict[str, str]:
    _ensure_logging()
    file_size = file_path.stat().st_size
    log_params("文件上传开始", file=str(file_path.name), key=object_key, size=file_size)
    token = build_upload_token(
        access_key=config["access_key"],
        secret_key=config["secret_key"],
        bucket=config["bucket"],
        object_key=object_key,
        expires_in=token_expires_in,
    )
    body, boundary = encode_multipart_form(
        fields=[("token", token), ("key", object_key)],
        file_field="file",
        file_path=file_path,
    )
    request = Request(
        upload_domain or DEFAULT_UPLOAD_DOMAIN,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))
    log_params("文件上传完成", key=object_key, size=file_size)
    return result
