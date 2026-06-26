from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from json import JSONDecodeError
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from wiznote_helper import LoginResult, note_list_path


@dataclass(frozen=True)
class Credentials:
    base_url: str
    user: str
    password: str


@dataclass(frozen=True)
class RequestSpec:
    url: str
    headers: dict[str, str]
    data: bytes | None = None
    method: str = "GET"


DEFAULT_TIMEOUT_SECONDS = 10


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wiznote-cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_notes = subparsers.add_parser("list-notes")
    list_notes.add_argument("--category-root", required=True)
    list_notes.add_argument("--category", required=True)

    return parser


def load_credentials(*, base_url: str | None = None, user: str | None = None, password: str | None = None) -> Credentials:
    resolved_base_url = base_url if base_url is not None else os.getenv("WIZNOTE_BASE_URL")
    resolved_user = user if user is not None else os.getenv("WIZNOTE_USER")
    resolved_password = password if password is not None else os.getenv("WIZNOTE_PASSWORD")

    missing = []
    if not resolved_base_url:
        missing.append("WIZNOTE_BASE_URL")
    if not resolved_user:
        missing.append("WIZNOTE_USER")
    if not resolved_password:
        missing.append("WIZNOTE_PASSWORD")
    if missing:
        raise ValueError(f"Missing WizNote credentials: {', '.join(missing)}")

    assert resolved_base_url is not None
    assert resolved_user is not None
    assert resolved_password is not None

    return Credentials(
        base_url=resolved_base_url.rstrip("/"),
        user=resolved_user,
        password=resolved_password,
    )


def login_request_payload(credentials: Credentials) -> dict[str, str | bool]:
    return {
        "userId": credentials.user,
        "password": credentials.password,
        "autoLogin": True,
        "clientType": "web",
        "clientVersion": "4.0",
        "lang": "zh-cn",
    }


def note_list_request(
    *,
    base_url: str,
    kb_guid: str,
    token: str,
    category: str,
    start: int = 0,
    count: int = 100,
) -> RequestSpec:
    return RequestSpec(
        url=f"{base_url.rstrip('/')}{note_list_path(kb_guid, category, start=start, count=count)}",
        headers={"X-Wiz-Token": token},
    )


def note_create_request(
    *,
    base_url: str,
    kb_guid: str,
    token: str,
    title: str,
    category: str,
    html: str,
) -> RequestSpec:
    payload = {
        "kbGuid": kb_guid,
        "title": title,
        "category": category,
        "html": html,
    }
    return RequestSpec(
        url=f"{base_url.rstrip('/')}/ks/note/create/{kb_guid}",
        headers={"X-Wiz-Token": token, "Content-type": "application/json"},
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
    )


def note_html_path(kb_guid: str, doc_guid: str) -> str:
    return f"/ks/note/download/{kb_guid}/{doc_guid}"


def fetch_note_html(*, base_url: str, kb_guid: str, doc_guid: str, token: str) -> str:
    request = Request(
        f"{base_url.rstrip('/')}{note_html_path(kb_guid, doc_guid)}",
        headers={"X-Wiz-Token": token},
        method="GET",
    )
    try:
        with urlopen(request, timeout=DEFAULT_TIMEOUT_SECONDS) as response:
            return response.read().decode("utf-8")
    except (HTTPError, URLError) as exc:
        raise ValueError(f"WizNote note download request failed: {exc}") from exc


def create_note(
    *,
    base_url: str,
    kb_guid: str,
    token: str,
    title: str,
    category: str,
    html: str,
) -> dict[str, object]:
    request_spec = note_create_request(
        base_url=base_url,
        kb_guid=kb_guid,
        token=token,
        title=title,
        category=category,
        html=html,
    )
    request = Request(
        request_spec.url,
        data=request_spec.data,
        headers=request_spec.headers,
        method=request_spec.method,
    )
    try:
        with urlopen(request, timeout=DEFAULT_TIMEOUT_SECONDS) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError) as exc:
        raise ValueError(f"WizNote note create request failed: {exc}") from exc
    except JSONDecodeError as exc:
        raise ValueError("WizNote note create returned invalid JSON") from exc


def save_note(
    *,
    base_url: str,
    kb_guid: str,
    doc_guid: str,
    token: str,
    title: str,
    category: str,
    html: str,
) -> dict[str, object]:
    payload = {
        "kbGuid": kb_guid,
        "docGuid": doc_guid,
        "title": title,
        "category": category,
        "html": html,
    }
    request = Request(
        f"{base_url.rstrip('/')}/ks/note/save/{kb_guid}/{doc_guid}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"X-Wiz-Token": token, "Content-type": "application/json"},
        method="PUT",
    )
    try:
        with urlopen(request, timeout=DEFAULT_TIMEOUT_SECONDS) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError) as exc:
        raise ValueError(f"WizNote note save request failed: {exc}") from exc
    except JSONDecodeError as exc:
        raise ValueError("WizNote note save returned invalid JSON") from exc


def login(credentials: Credentials) -> LoginResult:
    payload = login_request_payload(credentials)
    request = Request(
        url=(
            f"{credentials.base_url.rstrip('/')}"
            "/as/user/login?clientType=web&clientVersion=4.0&lang=zh-cn"
        ),
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=DEFAULT_TIMEOUT_SECONDS) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError) as exc:
        raise ValueError(f"WizNote login request failed: {exc}") from exc
    except JSONDecodeError as exc:
        raise ValueError("WizNote login returned invalid JSON") from exc
    from wiznote_helper import parse_login_result

    return parse_login_result(response_payload)


def fetch_note_list(
    *,
    base_url: str,
    kb_guid: str,
    token: str,
    category: str,
    start: int = 0,
    count: int = 100,
) -> dict:
    request_spec = note_list_request(
        base_url=base_url,
        kb_guid=kb_guid,
        token=token,
        category=category,
        start=start,
        count=count,
    )
    request = Request(request_spec.url, headers=request_spec.headers, method="GET")
    try:
        with urlopen(request, timeout=DEFAULT_TIMEOUT_SECONDS) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError) as exc:
        raise ValueError(f"WizNote note list request failed: {exc}") from exc
    except JSONDecodeError as exc:
        raise ValueError("WizNote note list returned invalid JSON") from exc
