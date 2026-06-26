#!/usr/bin/env python3
"""Helpers for public-safe SOTA-agent artifacts."""

from __future__ import annotations

import ipaddress
import ntpath
from pathlib import Path
import re
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlsplit


SENSITIVE_KEY_HINTS = (
    "KEY",
    "TOKEN",
    "SECRET",
    "PASSWORD",
    "COOKIE",
    "CREDENTIAL",
    "AUTH",
)
PRIVATE_HOST_SUFFIXES = (".local", ".internal", ".corp", ".lan")
WINDOWS_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:[\\/]")


def is_sensitive_key(key: str) -> bool:
    normalized = key.upper().replace("-", "_")
    return any(hint in normalized for hint in SENSITIVE_KEY_HINTS)


def looks_like_credential_url(value: str) -> bool:
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    if not parsed.scheme:
        return False
    if parsed.username or parsed.password:
        return True
    for key, _ in parse_qsl(parsed.query, keep_blank_values=True):
        if is_sensitive_key(key):
            return True
    if "=" in parsed.fragment:
        for key, _ in parse_qsl(parsed.fragment, keep_blank_values=True):
            if is_sensitive_key(key):
                return True
    return False


def is_absolute_like(value: str) -> bool:
    return bool(
        value.startswith("/")
        or value.startswith("~/")
        or value.startswith("\\\\")
        or WINDOWS_ABSOLUTE_RE.match(value)
    )


def is_private_host(host: str) -> bool:
    host = host.lower().strip()
    if not host:
        return False
    if host == "localhost":
        return True
    if any(host.endswith(suffix) for suffix in PRIVATE_HOST_SUFFIXES):
        return True
    if "." not in host and not any(char.isdigit() for char in host):
        return True
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return False
    return (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_unspecified
    )


def classify_target(host: str, path: str) -> str:
    host = host.lower()
    path = path.lower()
    if "colab" in host:
        return "colab"
    if "kaggle" in host:
        return "kaggle"
    if "github" in host:
        return "github"
    if "chatgpt" in host:
        return "chatgpt"
    if "gemini" in host:
        return "gemini"
    if "notebook" in host or "notebook" in path:
        return "notebook"
    if host:
        return "browser"
    return ""


def sanitize_url(raw_url: str, allow_raw: bool = False) -> dict[str, Any]:
    raw_url = raw_url.strip()
    if not raw_url:
        return {
            "url": "",
            "target_host": "",
            "target_kind": "",
            "target_label": "",
            "url_redacted": False,
        }
    try:
        parsed = urlsplit(raw_url)
    except ValueError:
        parsed = urlsplit("")
    host = parsed.hostname or parsed.netloc.split("@")[-1]
    kind = classify_target(host, parsed.path)
    private_host = is_private_host(host)
    if private_host and not allow_raw:
        label = f"private-{kind or 'browser'}-target"
        host = ""
    else:
        label = host or kind or "browser-target"
    return {
        "url": raw_url if allow_raw else "",
        "target_host": host,
        "target_kind": kind,
        "target_label": label,
        "url_redacted": not allow_raw,
    }


def sanitize_url_for_display(raw_url: str, allow_raw: bool = False) -> str:
    info = sanitize_url(raw_url, allow_raw=allow_raw)
    if allow_raw:
        return info["url"]
    parts = []
    for part in (info["target_label"], info["target_kind"]):
        if not part:
            continue
        if parts and part in parts[-1]:
            continue
        parts.append(part)
    return " ".join(parts) if parts else "<redacted-url>"


def sanitize_path(
    path: str | Path,
    *,
    alias_roots: Iterable[tuple[Path | None, str]] = (),
    allow_absolute_paths: bool = False,
) -> str:
    raw_path = str(path)
    resolved: Path | None = None
    if not (isinstance(path, str) and (WINDOWS_ABSOLUTE_RE.match(path) or path.startswith("\\\\"))):
        resolved = Path(path).expanduser().resolve()
    if allow_absolute_paths:
        return str(resolved) if resolved is not None else raw_path
    for root, alias in alias_roots:
        if root is None:
            continue
        if resolved is None:
            continue
        try:
            relative = resolved.relative_to(root.expanduser().resolve())
        except ValueError:
            continue
        rel_text = relative.as_posix()
        return alias if not rel_text or rel_text == "." else f"{alias}/{rel_text}"
    if WINDOWS_ABSOLUTE_RE.match(raw_path) or raw_path.startswith("\\\\"):
        name = ntpath.basename(raw_path.rstrip("\\/")) or "path"
    elif resolved is not None:
        name = resolved.name or "path"
    else:
        name = Path(raw_path).name or "path"
    return f"<external>/{name}"


def sanitize_env_value(key: str, value: str, allow_raw: bool = False) -> str:
    if allow_raw:
        return value
    if is_sensitive_key(key):
        return "<redacted:sensitive-key>"
    if looks_like_credential_url(value):
        return "<redacted:credential-url>"
    if is_absolute_like(value):
        return sanitize_path(value, allow_absolute_paths=False)
    return value


def sanitize_env_map(items: dict[str, str], allow_raw: bool = False) -> dict[str, str]:
    return {key: sanitize_env_value(key, value, allow_raw=allow_raw) for key, value in items.items()}


def sanitize_metadata_value(
    key: str,
    value: str,
    *,
    alias_roots: Iterable[tuple[Path | None, str]] = (),
    allow_absolute_paths: bool = False,
    allow_raw: bool = False,
) -> str:
    if allow_raw:
        return value
    if is_sensitive_key(key):
        return "<redacted:sensitive-key>"
    if looks_like_credential_url(value):
        return "<redacted:credential-url>"
    if is_absolute_like(value):
        return sanitize_path(
            value,
            alias_roots=alias_roots,
            allow_absolute_paths=allow_absolute_paths,
        )
    return value


def sanitize_metadata_map(
    items: dict[str, str],
    *,
    alias_roots: Iterable[tuple[Path | None, str]] = (),
    allow_absolute_paths: bool = False,
    allow_raw: bool = False,
) -> dict[str, str]:
    return {
        key: sanitize_metadata_value(
            key,
            value,
            alias_roots=alias_roots,
            allow_absolute_paths=allow_absolute_paths,
            allow_raw=allow_raw,
        )
        for key, value in items.items()
    }


def sanitize_alias(value: str, *, label: str, allow_raw: bool = False) -> str:
    value = value.strip()
    if not value:
        return ""
    if allow_raw:
        return value
    return f"<redacted:{label}>"


def sanitize_command_tokens(
    tokens: list[str],
    *,
    alias_roots: Iterable[tuple[Path | None, str]] = (),
    allow_absolute_paths: bool = False,
    allow_raw: bool = False,
) -> list[str]:
    if allow_raw:
        return list(tokens)

    sanitized: list[str] = []
    redact_next = False
    for token in tokens:
        if redact_next:
            sanitized.append("<redacted:sensitive-flag-value>")
            redact_next = False
            continue

        if token.startswith("--"):
            if "=" in token:
                flag, value = token.split("=", 1)
                flag_name = flag.lstrip("-")
                if is_sensitive_key(flag_name):
                    sanitized.append(f"{flag}=<redacted:sensitive-flag-value>")
                elif looks_like_credential_url(value):
                    sanitized.append(f"{flag}=<redacted:credential-url>")
                elif is_absolute_like(value):
                    sanitized.append(
                        f"{flag}={sanitize_path(value, alias_roots=alias_roots, allow_absolute_paths=allow_absolute_paths)}"
                    )
                else:
                    sanitized.append(token)
            else:
                sanitized.append(token)
                if is_sensitive_key(token.lstrip("-")):
                    redact_next = True
            continue

        if "=" in token:
            key, value = token.split("=", 1)
            if is_sensitive_key(key):
                sanitized.append(f"{key}=<redacted:sensitive-env>")
                continue
            if looks_like_credential_url(value):
                sanitized.append(f"{key}=<redacted:credential-url>")
                continue
            if is_absolute_like(value):
                sanitized.append(
                    f"{key}={sanitize_path(value, alias_roots=alias_roots, allow_absolute_paths=allow_absolute_paths)}"
                )
                continue

        if looks_like_credential_url(token):
            sanitized.append("<redacted:credential-url>")
        elif is_absolute_like(token):
            sanitized.append(sanitize_path(token, alias_roots=alias_roots, allow_absolute_paths=allow_absolute_paths))
        else:
            sanitized.append(token)
    return sanitized


def sanitize_ref(value: str, allow_raw: bool = False) -> str:
    value = value.strip()
    if not value:
        return ""
    if "://" in value:
        return sanitize_url_for_display(value, allow_raw=allow_raw)
    if is_absolute_like(value):
        return sanitize_path(value, allow_absolute_paths=allow_raw)
    return value
