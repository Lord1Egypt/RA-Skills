"""Minimal stdlib HTTP client for the reCamera API (raw token auth, self-signed HTTPS OK)."""

from __future__ import annotations

import http.client
import json
import socket
import ssl
import urllib.parse
from typing import Any, Mapping, Optional, Tuple

from ._config import DeviceRecord
from ._errors import RecameraError

DEFAULT_TIMEOUT = 10.0

_INSECURE_SSL = ssl.create_default_context()
_INSECURE_SSL.check_hostname = False
_INSECURE_SSL.verify_mode = ssl.CERT_NONE


def base_url(device: DeviceRecord) -> str:
    protocol = device.get("protocol", "http")
    host = device["host"].strip()
    # Bracket IPv6 literals.
    try:
        socket.inet_pton(socket.AF_INET6, host)
        host = f"[{host}]"
    except OSError:
        pass
    port = device.get("port")
    if port:
        return f"{protocol}://{host}:{int(port)}"
    return f"{protocol}://{host}"


def api_url(
    device: DeviceRecord, endpoint: str, params: Optional[Mapping[str, Any]] = None
) -> str:
    url = base_url(device) + endpoint
    if params:
        cleaned = [(k, str(v)) for k, v in params.items() if v is not None]
        if cleaned:
            url = f"{url}?{urllib.parse.urlencode(cleaned)}"
    return url


def _auth_headers(device: DeviceRecord) -> dict[str, str]:
    return {"Authorization": device["token"]}


def _ssl_context(device: DeviceRecord):
    if device.get("protocol") == "https" and device.get("allow_unsecured", False):
        return _INSECURE_SSL
    return None


def _device_origin(device: DeviceRecord) -> Tuple[str, str, int]:
    """Return the (scheme, lowercase host, port) tuple of the registered device.

    Used to enforce same-origin redirects so we never send the bearer token to
    a host we didn't register.
    """
    scheme = (device.get("protocol") or "http").lower()
    host = (device.get("host") or "").strip().lower()
    try:
        socket.inet_pton(socket.AF_INET6, host)
    except OSError:
        # Already a hostname / IPv4 literal; leave as-is.
        pass
    port = device.get("port")
    if not port:
        port = 443 if scheme == "https" else 80
    return scheme, host, int(port)


def _raise_for_http(
    status: int, reason: str, body: bytes, what: str
) -> "RecameraError":
    body_text = body.decode("utf-8", errors="replace") if body else ""
    detail = f": {body_text.strip()}" if body_text.strip() else ""
    return RecameraError(
        f"{what} failed: HTTP {status} {reason}{detail}",
        status=status,
        body=body_text,
    )


def _connect(
    scheme: str, host: str, port: int, timeout: float, ctx
) -> http.client.HTTPConnection:
    if scheme == "https":
        return http.client.HTTPSConnection(host, port, timeout=timeout, context=ctx)
    return http.client.HTTPConnection(host, port, timeout=timeout)


def _split(url: str) -> Tuple[str, str, int, str]:
    u = urllib.parse.urlsplit(url)
    scheme = u.scheme or "http"
    host = u.hostname or ""
    default_port = 443 if scheme == "https" else 80
    port = u.port or default_port
    path = u.path or "/"
    if u.query:
        path = f"{path}?{u.query}"
    return scheme, host, port, path


def _request(
    device: DeviceRecord,
    endpoint: str,
    *,
    method: str,
    params: Optional[Mapping[str, Any]] = None,
    body: Optional[bytes] = None,
    content_type: Optional[str] = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> Tuple[bytes, str]:
    """One HTTP round-trip. Follows 3xx up to 5 hops **only** when each redirect
    target stays on the same (scheme, host, port) as the registered device.

    Cross-origin redirects are refused to prevent leaking the bearer token or
    turning the SDK into an SSRF gadget; urllib also won't forward 307 POSTs,
    which is why we handle redirects explicitly.
    """
    url = api_url(device, endpoint, params)
    headers = dict(_auth_headers(device))
    if content_type is not None:
        headers["Content-Type"] = content_type
    cur_method = method
    cur_body = body
    ctx = _ssl_context(device)
    insecure_ctx_fallback = None
    if ctx is None and device.get("allow_unsecured", False):
        insecure_ctx_fallback = _INSECURE_SSL
    origin = _device_origin(device)

    max_hops = 5
    for hop in range(max_hops + 1):
        scheme, host, port, path = _split(url)
        use_ctx = ctx if scheme == "https" else None
        if scheme == "https" and use_ctx is None and insecure_ctx_fallback is not None:
            use_ctx = insecure_ctx_fallback
        conn = _connect(scheme, host, port, timeout, use_ctx)
        try:
            send_headers = dict(headers)
            if cur_body is not None:
                send_headers.setdefault("Content-Length", str(len(cur_body)))
            conn.request(cur_method, path, body=cur_body, headers=send_headers)
            resp = conn.getresponse()
            status = resp.status
            reason = resp.reason
            if status in (301, 302, 303, 307, 308) and hop < max_hops:
                location = resp.getheader("Location")
                resp.read()
                if not location:
                    raise RecameraError(
                        f"{method} {endpoint} redirect missing Location header"
                    )
                url = urllib.parse.urljoin(url, location)
                # Refuse to follow the redirect if it points at a different
                # (scheme, host, port). Forwarding the Authorization header to
                # an unexpected origin would leak the long-lived bearer token.
                next_scheme, next_host, next_port, _ = _split(url)
                next_origin = (next_scheme.lower(), next_host.lower(), int(next_port))
                if next_origin != origin:
                    raise RecameraError(
                        f"{method} {endpoint} refused cross-origin redirect to "
                        f"{next_origin[0]}://{next_origin[1]}:{next_origin[2]} "
                        f"(registered device is {origin[0]}://{origin[1]}:{origin[2]})."
                    )
                if status == 303:
                    cur_method = "GET"
                    cur_body = None
                    headers.pop("Content-Type", None)
                continue
            data = resp.read()
            ct = resp.getheader("Content-Type", "") or ""
            if 200 <= status < 300:
                return data, ct
            raise _raise_for_http(status, reason, data, f"{method} {endpoint}")
        except (socket.timeout, TimeoutError) as exc:
            raise RecameraError(
                f"{method} {endpoint} timed out after {timeout:.0f}s"
            ) from exc
        except OSError as exc:
            raise RecameraError(f"{method} {endpoint} failed: {exc}") from exc
        finally:
            conn.close()
    raise RecameraError(f"{method} {endpoint} exceeded redirect limit ({max_hops})")


def get_json(
    device: DeviceRecord,
    endpoint: str,
    params: Optional[Mapping[str, Any]] = None,
    *,
    timeout: float = DEFAULT_TIMEOUT,
) -> Any:
    data, _ = _request(device, endpoint, method="GET", params=params, timeout=timeout)
    return _parse_json(data, f"GET {endpoint}")


def get_bytes(
    device: DeviceRecord,
    endpoint: str,
    params: Optional[Mapping[str, Any]] = None,
    *,
    timeout: float = DEFAULT_TIMEOUT,
) -> Tuple[bytes, str]:
    """Binary GET; returns ``(body, content_type)``."""
    return _request(device, endpoint, method="GET", params=params, timeout=timeout)


def post_json(
    device: DeviceRecord,
    endpoint: str,
    params: Optional[Mapping[str, Any]] = None,
    payload: Any = None,
    *,
    timeout: float = DEFAULT_TIMEOUT,
) -> Any:
    body = None
    ct = None
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        ct = "application/json"
    data, _ = _request(
        device,
        endpoint,
        method="POST",
        params=params,
        body=body,
        content_type=ct,
        timeout=timeout,
    )
    if not data:
        return {}
    return _parse_json(data, f"POST {endpoint}")


def post_text(
    device: DeviceRecord,
    endpoint: str,
    body: str,
    *,
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    _request(
        device,
        endpoint,
        method="POST",
        body=body.encode("utf-8"),
        content_type="text/plain",
        timeout=timeout,
    )


def delete(
    device: DeviceRecord,
    endpoint: str,
    params: Optional[Mapping[str, Any]] = None,
    *,
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    _request(device, endpoint, method="DELETE", params=params, timeout=timeout)


def expect_ok(resp: Any, context: str) -> None:
    """Enforce the ``code == 0`` contract for Record API POSTs."""
    if not isinstance(resp, dict):
        return
    code = resp.get("code")
    if code in (None, 0):
        return
    msg = resp.get("message") or "Unknown error"
    raise RecameraError(f"{context} failed (code={code}): {msg}", code=int(code))


def _parse_json(data: bytes, ctx: str) -> Any:
    if not data:
        return None
    try:
        return json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RecameraError(f"{ctx}: invalid JSON response") from exc
