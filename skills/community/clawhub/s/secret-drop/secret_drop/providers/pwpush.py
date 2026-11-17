"""Password Pusher JSON API adapter (hosted or self-hosted)."""

from __future__ import annotations

import re
from urllib.parse import urlsplit, urlunsplit

from secret_drop.errors import SecretDropError
from secret_drop.net import request_json

_TOKEN_RE = re.compile(r"^[A-Za-z0-9_-]{4,256}$")


def matches(url: str) -> bool:
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    # Unknown/self-hosted domains require an explicit --provider pwpush choice.
    return host == "pwpush.com" or host.endswith(".pwpush.com")


def _token_from_path(path: str) -> str:
    segments = [segment for segment in path.split("/") if segment]
    try:
        idx = segments.index("p")
        token = segments[idx + 1]
    except (ValueError, IndexError) as exc:
        raise SecretDropError("Password Pusher URL does not contain a push token.") from exc
    if token.endswith(".json"):
        token = token[:-5]
    if not _TOKEN_RE.fullmatch(token):
        raise SecretDropError("Password Pusher token has an invalid shape.")
    return token


def _endpoint(url: str, token: str, suffix: str, *, api_base: str | None) -> str:
    if api_base:
        base = urlsplit(api_base.rstrip("/"))
        path = f"{base.path.rstrip('/')}/p/{token}{suffix}"
        return urlunsplit((base.scheme, base.netloc, path, "", ""))
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, f"/p/{token}{suffix}", "", ""))


def retrieve(url: str, *, allow_private: bool = False, api_base: str | None = None) -> str:
    parts = urlsplit(url)
    if parts.query:
        raise SecretDropError("Password Pusher links with query parameters are not accepted.")
    token = _token_from_path(parts.path)
    json_url = _endpoint(url, token, ".json", api_base=api_base)
    _, payload, _ = request_json(json_url, allow_private=allow_private)
    if payload and payload.get("retrieval_step") and not isinstance(payload.get("payload"), str):
        preview_url = _endpoint(url, token, "/preview.json", api_base=api_base)
        request_json(preview_url, allow_private=allow_private)
        _, payload, _ = request_json(json_url, allow_private=allow_private)
    if not payload or not isinstance(payload.get("payload"), str):
        if payload and (payload.get("expired") or payload.get("deleted")):
            raise SecretDropError("Password Pusher link is expired or deleted.")
        if payload and payload.get("retrieval_step"):
            raise SecretDropError(
                "Password Pusher still requires a retrieval step. Open the link once in a browser, then retry, or disable the extra click for agent ingest."
            )
        raise SecretDropError("Password Pusher returned no text payload.")
    return payload["payload"]
