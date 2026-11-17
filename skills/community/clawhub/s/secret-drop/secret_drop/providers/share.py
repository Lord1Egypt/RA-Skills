"""Outbound Password Pusher creation without exposing plaintext to chat or logs."""

from __future__ import annotations

import json
import re
from urllib.parse import urlsplit

from secret_drop.errors import SecretDropError
from secret_drop.net import request_json

DEFAULT_PWPUSH_API_BASE = "https://eu.pwpush.com"
_TOKEN_RE = re.compile(r"^[A-Za-z0-9_-]{4,256}$")


def _api_url(api_base: str) -> str:
    base = (api_base or DEFAULT_PWPUSH_API_BASE).rstrip("/")
    parts = urlsplit(base)
    if (
        parts.scheme != "https"
        or not parts.hostname
        or parts.username
        or parts.password
        or parts.query
        or parts.fragment
    ):
        raise SecretDropError("Only plain https provider roots are allowed.")
    netloc = parts.netloc
    path = f"{parts.path.rstrip('/')}/p.json" if parts.path else "/p.json"
    return f"https://{netloc}{path}"


def _assert_share_url(link: str, *, api_url: str, url_token: str) -> None:
    parts = urlsplit(link)
    api_parts = urlsplit(api_url)
    segments = [segment for segment in parts.path.split("/") if segment]
    try:
        push_index = segments.index("p")
    except ValueError as exc:
        raise SecretDropError("Provider returned an invalid retrieval-step URL.") from exc
    host_allowed = (
        (parts.hostname or "").lower() == (api_parts.hostname or "").lower()
        and parts.port == api_parts.port
    )
    if (
        parts.scheme != "https"
        or not parts.hostname
        or not host_allowed
        or parts.username
        or parts.password
        or parts.query
        or parts.fragment
        or segments[push_index + 1 : push_index + 3] != [url_token, "r"]
        or len(segments) != push_index + 3
    ):
        raise SecretDropError("Provider returned an invalid retrieval-step URL.")


def create_push(
    secret: str,
    *,
    api_base: str | None = None,
    allow_private: bool = False,
) -> dict[str, str | int | bool]:
    if not secret:
        raise SecretDropError("Secret payload is empty.")

    url = _api_url(api_base or DEFAULT_PWPUSH_API_BASE)
    payload_data = {
        "password": {
            "payload": secret,
            "expire_after_views": 1,
            "expire_after_days": 1,
            "retrieval_step": True,
            "deletable_by_viewer": True,
        }
    }
    encoded = json.dumps(payload_data).encode("utf-8")
    status, response_json, _ = request_json(
        url,
        method="POST",
        data=encoded,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        allow_private=allow_private,
        allow_redirects=False,
    )
    if status not in {200, 201} or not response_json:
        raise SecretDropError("Failed to create secret link with provider.")

    url_token = response_json.get("url_token")
    if not isinstance(url_token, str) or not _TOKEN_RE.fullmatch(url_token):
        raise SecretDropError("Provider did not return a valid secret token.")
    if response_json.get("expire_after_views") != 1:
        raise SecretDropError("Provider did not create a one-view push.")
    if response_json.get("retrieval_step") is not True:
        raise SecretDropError("Provider did not enable the retrieval step.")
    expire_days = response_json.get("expire_after_days")
    expire_duration = response_json.get("expire_after_duration")
    if expire_days != 1 and expire_duration != 6:
        raise SecretDropError("Provider did not create a one-day push.")

    html_url = response_json.get("html_url")
    if not isinstance(html_url, str) or not html_url.strip():
        raise SecretDropError("Provider did not return a retrieval-step URL.")
    link = html_url.strip()
    _assert_share_url(link, api_url=url, url_token=url_token)
    return {
        "ok": True,
        "url": link,
        "provider": "pwpush",
        "expire_views": 1,
        "expire_days": 1,
        "retrieval_step": True,
    }
