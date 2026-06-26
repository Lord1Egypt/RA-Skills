from __future__ import annotations

import ipaddress
import logging
import os
import socket
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

SQLITE_MAX_VARIABLES = 999

# Domains allowed even if they resolve to private IPs (configurable via env)
_SSRF_ALLOWLIST: list[str] = [
    d.strip()
    for d in os.environ.get("AGENT_MEMORY_SSRF_ALLOWLIST", "").split(",")
    if d.strip()
]


def _validate_url(url: str, allow_private: bool | None = None) -> str:
    """Validate URL to prevent SSRF attacks.

    - Only allows http:// and https:// schemes
    - Blocks private/internal IP ranges unless explicitly allowed
    - Validates that the hostname resolves to a public IP
    - Supports a configurable domain allowlist via AGENT_MEMORY_SSRF_ALLOWLIST env var
    - Can be bypassed for dev/testing via AGENT_MEMORY_ALLOW_PRIVATE_URLS=true env var
    """
    if allow_private is None:
        allow_private = os.environ.get("AGENT_MEMORY_ALLOW_PRIVATE_URLS", "").lower() == "true"

    parsed = urlparse(url)

    # Only allow http/https
    if parsed.scheme not in ("http", "https"):
        logger.warning("SSRF blocked: URL scheme '%s' not allowed (only http/https): %s", parsed.scheme, url)
        raise ValueError(f"URL scheme '{parsed.scheme}' not allowed. Only http/https permitted.")

    hostname = parsed.hostname
    if not hostname:
        logger.warning("SSRF blocked: URL has no hostname: %s", url)
        raise ValueError("URL has no hostname")

    if allow_private:
        return url

    # Check domain allowlist
    if hostname in _SSRF_ALLOWLIST:
        return url

    # Resolve hostname and check IP
    try:
        addrs = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        logger.warning("SSRF blocked: cannot resolve hostname '%s'", hostname)
        raise ValueError(f"Cannot resolve hostname '{hostname}'")

    for family, _, _, _, sockaddr in addrs:
        ip = ipaddress.ip_address(sockaddr[0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            logger.warning(
                "SSRF blocked: hostname '%s' resolves to private/reserved IP %s. "
                "Set AGENT_MEMORY_ALLOW_PRIVATE_URLS=true to allow.",
                hostname,
                ip,
            )
            raise ValueError(
                f"URL hostname '{hostname}' resolves to private/reserved IP {ip}. "
                "Set AGENT_MEMORY_ALLOW_PRIVATE_URLS=true to allow."
            )

    return url


def _validate_path(path: str, allowed_dirs: list = None) -> str:
    """Validate file path to prevent path traversal.

    Args:
        path: The file path to validate.
        allowed_dirs: Optional list of allowed directory prefixes.
            If provided, the resolved path must be under one of these directories.

    Returns:
        The resolved absolute path.

    Raises:
        ValueError: If the path is outside allowed directories or contains traversal.
    """
    resolved = os.path.realpath(path)
    # Block path traversal: if the original path contains ".." and resolves
    # outside the expected location, reject it
    if ".." in path:
        abs_path = os.path.abspath(path)
        if resolved != abs_path:
            raise ValueError(f"Path traversal detected: '{path}' resolves to '{resolved}'")
    if allowed_dirs:
        allowed = any(resolved.startswith(os.path.realpath(d)) for d in allowed_dirs)
        if not allowed:
            raise ValueError(f"Path '{path}' outside allowed directories")
    return resolved


def _chunked_placeholders(ids: list, chunk_size: int = SQLITE_MAX_VARIABLES) -> list[tuple[str, list]]:
    chunks = []
    for i in range(0, len(ids), chunk_size):
        chunk = ids[i:i + chunk_size]
        placeholders = ",".join("?" * len(chunk))
        chunks.append((placeholders, chunk))
    return chunks

def content_hash(text: str) -> str:
    import hashlib
    return hashlib.sha256(text.encode()).hexdigest()

def short_id(text: str, length: int = 12) -> str:
    import hashlib
    return hashlib.sha256(text.encode()).hexdigest()[:length]
