#!/usr/bin/env python3
"""Safety helpers for WordPress API Pro scripts.

These helpers intentionally avoid third-party dependencies so the skill remains
portable inside OpenClaw agent environments.
"""

from __future__ import annotations

import ipaddress
import os
import socket
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Iterable

DEFAULT_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
TEXT_MAX_BYTES = 2 * 1024 * 1024  # 2 MB


class SafetyError(ValueError):
    """Raised when an input crosses the skill's safety boundaries."""


def _split_roots(raw: str | None) -> list[Path]:
    if not raw:
        return [Path.cwd().resolve()]
    roots: list[Path] = []
    for item in raw.split(os.pathsep):
        item = item.strip()
        if item:
            roots.append(Path(item).expanduser().resolve())
    return roots or [Path.cwd().resolve()]


def allowed_roots() -> list[Path]:
    """Return local filesystem roots this skill may read from.

    Defaults to the current working directory. Override with
    WP_ALLOWED_FILE_ROOTS using os.pathsep-separated paths.
    """

    return _split_roots(os.getenv("WP_ALLOWED_FILE_ROOTS"))


def validate_local_file(path_value: str, *, purpose: str = "file", max_bytes: int = DEFAULT_MAX_BYTES) -> Path:
    """Validate and resolve a local file path before reading it."""

    if not path_value:
        raise SafetyError(f"Missing {purpose} path")

    path = Path(path_value).expanduser().resolve()
    roots = allowed_roots()

    if not path.exists():
        raise SafetyError(f"{purpose} not found: {path}")
    if not path.is_file():
        raise SafetyError(f"{purpose} is not a regular file: {path}")
    if not any(path == root or root in path.parents for root in roots):
        roots_text = ", ".join(str(root) for root in roots)
        raise SafetyError(
            f"Refusing to read {path}. Allowed roots: {roots_text}. "
            "Set WP_ALLOWED_FILE_ROOTS to opt in to another directory."
        )
    size = path.stat().st_size
    if size > max_bytes:
        raise SafetyError(f"{purpose} is too large: {size} bytes > {max_bytes} bytes")
    return path


def _hostname_addresses(hostname: str) -> Iterable[ipaddress._BaseAddress]:
    for family, _, _, _, sockaddr in socket.getaddrinfo(hostname, None):
        if family in (socket.AF_INET, socket.AF_INET6):
            yield ipaddress.ip_address(sockaddr[0])


def validate_remote_url(url: str) -> str:
    """Validate a remote URL before fetching it.

    Only HTTPS URLs are allowed. Hostnames resolving to private, loopback,
    link-local, multicast, unspecified, or reserved addresses are blocked to
    reduce SSRF/exfiltration risk in agentic contexts.
    """

    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        raise SafetyError("Remote media URLs must use https://")
    if not parsed.hostname:
        raise SafetyError("Remote URL must include a hostname")

    hostname = parsed.hostname
    try:
        addresses = list(_hostname_addresses(hostname))
    except socket.gaierror as exc:
        raise SafetyError(f"Could not resolve remote URL host {hostname!r}: {exc}") from exc

    if not addresses:
        raise SafetyError(f"Remote URL host {hostname!r} resolved to no addresses")

    for address in addresses:
        if any(
            [
                address.is_private,
                address.is_loopback,
                address.is_link_local,
                address.is_multicast,
                address.is_reserved,
                address.is_unspecified,
            ]
        ):
            raise SafetyError(f"Refusing remote URL host {hostname!r}; resolved to unsafe address {address}")

    return url


def read_limited_response(response, *, max_bytes: int = DEFAULT_MAX_BYTES) -> bytes:
    """Read a response body with a strict size limit."""

    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(min(65536, max_bytes + 1 - total))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > max_bytes:
            raise SafetyError(f"Remote response is too large: > {max_bytes} bytes")
    return b"".join(chunks)


def fetch_https_media(url: str, *, timeout: int = 20, max_bytes: int = DEFAULT_MAX_BYTES):
    """Fetch a validated HTTPS URL and return (response, body)."""

    validate_remote_url(url)
    request = urllib.request.Request(url, headers={"User-Agent": "wordpress-api-pro/3.4.0"})
    response = urllib.request.urlopen(request, timeout=timeout)
    body = read_limited_response(response, max_bytes=max_bytes)
    return response, body


def warn_insecure_wp_url(url, env=None):
    """Warn when a WordPress API URL is plaintext http:// on a non-local host.
    Basic-Auth credentials would travel unencrypted. Localhost/dev hosts are exempt.
    With WP_REQUIRE_HTTPS=1 this raises SafetyError instead of warning.
    Returns the url unchanged (never mutates it)."""
    env = env if env is not None else os.environ
    parsed = urllib.parse.urlparse(url if "://" in str(url) else "https://" + str(url))
    host = (parsed.hostname or "").lower()
    is_local = (
        host in ("localhost", "127.0.0.1", "0.0.0.0", "::1")
        or host.endswith(".local")
        or host.endswith(".test")
        or host.endswith(".localhost")
    )
    if parsed.scheme == "http" and not is_local:
        msg = (
            "SECURITY WARNING: WordPress URL '%s' uses plaintext http:// — "
            "Basic-Auth credentials will be sent unencrypted. Use https:// in production." % url
        )
        if env.get("WP_REQUIRE_HTTPS") == "1":
            raise SafetyError(msg + " (WP_REQUIRE_HTTPS=1 set — refusing.)")
        print(msg, file=sys.stderr)
    return url


def should_confirm_publish(status, assume_yes, is_tty):
    """True only when we should interactively prompt before a live publish:
    going to 'publish', not pre-approved with --yes, and attached to a TTY.
    Non-interactive (agent/CI) contexts return False -> behavior unchanged."""
    return status == "publish" and not assume_yes and bool(is_tty)


def die_safety(error: Exception) -> None:
    print(f"Safety error: {error}", file=sys.stderr)
    sys.exit(2)
