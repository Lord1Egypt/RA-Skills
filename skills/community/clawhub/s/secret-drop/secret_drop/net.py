"""HTTPS-only fetches with private-target rejection and pinned DNS resolution."""

from __future__ import annotations

import ipaddress
import json
import socket
import ssl
from http.client import HTTPSConnection
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, HTTPSHandler, Request, build_opener

from secret_drop.errors import SecretDropError
from secret_drop.redact import host_of, sanitize_url

USER_AGENT = "openclaw-secret-drop/0.1"
DEFAULT_TIMEOUT = 20
MAX_BODY_BYTES = 2_000_000
MAX_REDIRECTS = 3


def _is_private_ip(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return True
    if hasattr(addr, "ipv4_mapped") and addr.ipv4_mapped:
        addr = addr.ipv4_mapped
    return not addr.is_global


def parse_https_url(url: str) -> tuple[str, int, str]:
    try:
        parts = urlsplit(url)
    except Exception as exc:
        raise SecretDropError("URL is not valid.") from exc
    if parts.scheme != "https":
        raise SecretDropError("Only https URLs are allowed.")
    host = parts.hostname
    if not host:
        raise SecretDropError("URL is missing a hostname.")
    if parts.username or parts.password:
        raise SecretDropError("URLs with embedded credentials are not allowed.")
    port = parts.port or 443
    path = parts.path or "/"
    if parts.query:
        path = f"{path}?{parts.query}"
    return host, port, path


def resolve_public_https(url: str, *, allow_private: bool = False) -> tuple[str, int, str, str]:
    """Return hostname, port, path, and a pinned connect target."""
    host, port, path = parse_https_url(url)
    if allow_private:
        return host, port, path, host
    if host.lower() in {"localhost", "localhost.localdomain"}:
        raise SecretDropError("Refusing to fetch localhost.")
    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except OSError as exc:
        raise SecretDropError(f"Could not resolve host {host}.") from exc
    if not infos:
        raise SecretDropError(f"Could not resolve host {host}.")
    resolved_ips = [info[4][0] for info in infos]
    # Validate every A/AAAA result before selecting the pinned connection target.
    # A single private or scoped result makes a mixed DNS answer unsafe.
    if any(_is_private_ip(ip) for ip in resolved_ips):
        raise SecretDropError(f"Refusing to fetch private or local address for {host}.")
    return host, port, path, resolved_ips[0]


def assert_public_https(url: str, *, allow_private: bool = False) -> None:
    resolve_public_https(url, allow_private=allow_private)


class _PinnedHTTPSConnection(HTTPSConnection):
    def __init__(self, host: str, port: int | None = None, *, connect_ip: str, **kwargs: Any) -> None:
        super().__init__(host, port, **kwargs)
        self._connect_ip = connect_ip

    def connect(self) -> None:
        self.sock = socket.create_connection((self._connect_ip, self.port), self.timeout)
        if self._tunnel_host:
            self._tunnel()
        # SNI hostname must not include a port
        sni_host = self.host.split(":")[0] if self.host else None
        self.sock = self._context.wrap_socket(self.sock, server_hostname=sni_host)


class _PinnedHTTPSHandler(HTTPSHandler):
    def __init__(self, context: ssl.SSLContext, *, allow_private: bool) -> None:
        super().__init__(context=context)
        self.allow_private = allow_private
        self.redirects = 0

    def https_open(self, req: Request):  # type: ignore[no-untyped-def]
        host, _port, _path, connect_ip = resolve_public_https(
            req.full_url, allow_private=self.allow_private
        )

        def http_class(*args: Any, **kwargs: Any) -> _PinnedHTTPSConnection:
            return _PinnedHTTPSConnection(*args, connect_ip=connect_ip, **kwargs)

        return self.do_open(http_class, req)


class _SafeRedirect(HTTPRedirectHandler):
    """Bound redirects and reject redirects to local or private destinations."""

    max_repeats = MAX_REDIRECTS
    max_redirections = MAX_REDIRECTS

    def __init__(self, *, allow_private: bool, allow_redirects: bool = True) -> None:
        super().__init__()
        self.allow_private = allow_private
        self.allow_redirects = allow_redirects

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        if not self.allow_redirects:
            raise SecretDropError("Provider redirects are not allowed for this operation.")
        resolve_public_https(newurl, allow_private=self.allow_private)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def request_json(
    url: str,
    *,
    method: str = "GET",
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    allow_private: bool = False,
    allow_redirects: bool = True,
) -> tuple[int, dict[str, Any] | None, bytes]:
    resolve_public_https(url, allow_private=allow_private)
    hdrs = {"User-Agent": USER_AGENT, "Accept": "application/json", **(headers or {})}
    req = Request(url, data=data, headers=hdrs, method=method)
    context = ssl.create_default_context()
    opener = build_opener(
        _SafeRedirect(allow_private=allow_private, allow_redirects=allow_redirects),
        _PinnedHTTPSHandler(context, allow_private=allow_private),
    )
    try:
        with opener.open(req, timeout=timeout) as resp:
            status = getattr(resp, "status", 200)
            raw = resp.read(MAX_BODY_BYTES + 1)
            if resp.geturl() and resp.geturl() != url:
                resolve_public_https(resp.geturl(), allow_private=allow_private)
    except HTTPError as exc:
        raw = exc.read(MAX_BODY_BYTES + 1) if exc.fp else b""
        if len(raw) > MAX_BODY_BYTES:
            raise SecretDropError("Provider response was too large.") from exc
        raise SecretDropError(
            f"Provider HTTP {exc.code} from {host_of(url) or sanitize_url(url)}."
        ) from exc
    except URLError as exc:
        raise SecretDropError(f"Network error fetching {host_of(url) or 'provider'}.") from exc
    except TimeoutError as exc:
        raise SecretDropError("Provider request timed out.") from exc
    if len(raw) > MAX_BODY_BYTES:
        raise SecretDropError("Provider response was too large.")
    return status, _try_json(raw), raw


def _try_json(raw: bytes) -> dict[str, Any] | None:
    if not raw:
        return None
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None
