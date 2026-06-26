#!/usr/bin/env python3
"""WordPress.com OAuth helper for OpenClaw workspace skills.

Commands:
- begin-oauth
- exchange-token
- token-info
- publish-post
"""

from __future__ import annotations

import argparse
import json
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

AUTHORIZE_ENDPOINT = "https://public-api.wordpress.com/oauth2/authorize"
TOKEN_ENDPOINT = "https://public-api.wordpress.com/oauth2/token"
TOKEN_INFO_ENDPOINT = "https://public-api.wordpress.com/oauth2/token-info"
PUBLISH_ENDPOINT_TEMPLATE = "https://public-api.wordpress.com/rest/v1.1/sites/{site}/posts/new"

BASE_DIR = Path(__file__).resolve().parent
STATE_PATH = BASE_DIR / "oauth_state.json"
CREDS_PATH = BASE_DIR / "credentials.json"


class SkillError(Exception):
    """User-facing operational error."""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def mask_token(token: str) -> str:
    if len(token) <= 10:
        return "***"
    return f"{token[:6]}...{token[-4:]}"


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SkillError(f"Required file not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SkillError(f"Invalid JSON in {path}: {exc}") from exc


def request_json(
    method: str,
    url: str,
    form_data: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    payload: bytes | None = None
    request_headers = {"Accept": "application/json"}
    if headers:
        request_headers.update(headers)

    if form_data is not None:
        payload = urlencode(form_data).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/x-www-form-urlencoded")

    req = Request(url=url, data=payload, method=method.upper(), headers=request_headers)

    try:
        with urlopen(req, timeout=30) as response:
            body = response.read().decode("utf-8")
            if not body.strip():
                return {}
            return json.loads(body)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        detail = body.strip() or str(exc)
        raise SkillError(f"HTTP {exc.code} for {url}: {detail}") from exc
    except URLError as exc:
        raise SkillError(f"Network error for {url}: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise SkillError(f"Non-JSON response from {url}: {exc}") from exc


def get_required(value: str | None, env_name: str, flag_name: str) -> str:
    if value:
        return value
    raise SkillError(
        f"Missing required value. Provide {flag_name} or set {env_name}."
    )


def begin_oauth(args: argparse.Namespace) -> dict[str, Any]:
    client_id = get_required(args.client_id, "WPCOM_CLIENT_ID", "--client-id")
    redirect_uri = get_required(
        args.redirect_uri, "WPCOM_REDIRECT_URI", "--redirect-uri"
    )
    state = secrets.token_urlsafe(24)

    params: dict[str, str] = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": args.scope,
        "state": state,
    }
    if args.blog:
        params["blog"] = args.blog

    auth_url = f"{AUTHORIZE_ENDPOINT}?{urlencode(params)}"

    state_data = {
        "state": state,
        "created_at_utc": utc_now_iso(),
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": args.scope,
        "blog": args.blog,
    }
    write_json(STATE_PATH, state_data)

    return {
        "auth_url": auth_url,
        "generated_state": state,
        "state_file": str(STATE_PATH),
    }


def parse_callback(callback_url: str) -> tuple[str | None, str | None, str | None]:
    parsed = urlparse(callback_url)
    params = parse_qs(parsed.query)

    code = params.get("code", [None])[0]
    state = params.get("state", [None])[0]
    oauth_error = params.get("error", [None])[0]

    return code, state, oauth_error


def exchange_token(args: argparse.Namespace) -> dict[str, Any]:
    client_id = get_required(args.client_id, "WPCOM_CLIENT_ID", "--client-id")
    client_secret = get_required(
        args.client_secret, "WPCOM_CLIENT_SECRET", "--client-secret"
    )
    redirect_uri = get_required(
        args.redirect_uri, "WPCOM_REDIRECT_URI", "--redirect-uri"
    )

    code = args.code
    callback_state = args.state
    if args.callback_url:
        parsed_code, parsed_state, oauth_error = parse_callback(args.callback_url)
        if oauth_error:
            raise SkillError(f"OAuth callback returned error: {oauth_error}")
        code = code or parsed_code
        callback_state = callback_state or parsed_state

    if not code:
        raise SkillError(
            "Missing OAuth code. Provide --callback-url with code=... or --code directly."
        )

    stored_state = read_json(STATE_PATH)
    expected_state = stored_state.get("state")
    if not expected_state:
        raise SkillError(f"State value missing from {STATE_PATH}.")
    if callback_state != expected_state:
        raise SkillError("State mismatch. Run begin-oauth again and retry exchange.")

    token_response = request_json(
        "POST",
        TOKEN_ENDPOINT,
        form_data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        },
    )

    access_token = token_response.get("access_token")
    if not access_token:
        raise SkillError(f"Token endpoint did not return access_token: {token_response}")

    credentials = {
        "access_token": access_token,
        "token_type": token_response.get("token_type", "bearer"),
        "blog_id": token_response.get("blog_id"),
        "blog_url": token_response.get("blog_url"),
        "scope": token_response.get("scope"),
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "obtained_at_utc": utc_now_iso(),
    }
    write_json(CREDS_PATH, credentials)

    return {
        "access_token_masked": mask_token(access_token),
        "blog_id": credentials.get("blog_id"),
        "blog_url": credentials.get("blog_url"),
        "scope": credentials.get("scope"),
        "credentials_file": str(CREDS_PATH),
    }


def token_info(args: argparse.Namespace) -> dict[str, Any]:
    credentials = read_json(CREDS_PATH)
    access_token = credentials.get("access_token")
    if not access_token:
        raise SkillError(f"No access_token in {CREDS_PATH}.")

    client_id = args.client_id or credentials.get("client_id")
    if not client_id:
        raise SkillError("Client ID is required. Provide --client-id.")

    query = urlencode({"client_id": client_id, "token": access_token})
    info = request_json("GET", f"{TOKEN_INFO_ENDPOINT}?{query}")

    return {
        "access_token_masked": mask_token(access_token),
        "token_info": info,
    }


def publish_post(args: argparse.Namespace) -> dict[str, Any]:
    credentials = read_json(CREDS_PATH)
    access_token = credentials.get("access_token")
    if not access_token:
        raise SkillError(f"No access_token in {CREDS_PATH}.")

    site = get_required(args.site, "WPCOM_SITE", "--site")

    payload: dict[str, str] = {
        "title": args.title,
        "content": args.content,
        "status": args.status,
    }
    if args.tags:
        payload["tags"] = args.tags
    if args.categories:
        payload["categories"] = args.categories

    endpoint = PUBLISH_ENDPOINT_TEMPLATE.format(site=site)
    response = request_json(
        "POST",
        endpoint,
        form_data=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    return {
        "site": site,
        "post_id": response.get("ID") or response.get("id"),
        "post_url": response.get("URL") or response.get("url"),
        "status": response.get("status"),
        "response": response,
    }


def print_json(data: dict[str, Any]) -> None:
    print(json.dumps(data, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="WordPress.com OAuth skill helper for OpenClaw workspace skill directory."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_begin = subparsers.add_parser("begin-oauth", help="Generate OAuth authorize URL.")
    p_begin.add_argument("--client-id", default=None)
    p_begin.add_argument("--redirect-uri", default=None)
    p_begin.add_argument("--scope", default="posts")
    p_begin.add_argument("--blog", default=None)
    p_begin.set_defaults(func=begin_oauth)

    p_exchange = subparsers.add_parser(
        "exchange-token", help="Exchange OAuth code for access token."
    )
    p_exchange.add_argument("--client-id", default=None)
    p_exchange.add_argument("--client-secret", default=None)
    p_exchange.add_argument("--redirect-uri", default=None)
    p_exchange.add_argument("--callback-url", default=None)
    p_exchange.add_argument("--code", default=None)
    p_exchange.add_argument("--state", default=None)
    p_exchange.set_defaults(func=exchange_token)

    p_token = subparsers.add_parser("token-info", help="Validate stored token.")
    p_token.add_argument("--client-id", default=None)
    p_token.set_defaults(func=token_info)

    p_publish = subparsers.add_parser("publish-post", help="Publish a post using stored token.")
    p_publish.add_argument("--site", default=None)
    p_publish.add_argument("--title", required=True)
    p_publish.add_argument("--content", required=True)
    p_publish.add_argument(
        "--status",
        default="draft",
        choices=["publish", "draft", "future", "private", "pending"],
    )
    p_publish.add_argument("--tags", default=None)
    p_publish.add_argument("--categories", default=None)
    p_publish.set_defaults(func=publish_post)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = args.func(args)
        print_json(result)
        return 0
    except SkillError as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
