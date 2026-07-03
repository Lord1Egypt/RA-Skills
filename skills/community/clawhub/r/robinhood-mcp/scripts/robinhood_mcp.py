#!/usr/bin/env python3
"""Robinhood Trading MCP client with persistent OAuth.

Connects to Robinhood's remote MCP server (Streamable HTTP) on behalf of the
user. OAuth credentials (the dynamically-registered client and the
access/refresh tokens) are persisted to a directory *outside* the agent
session so that future sessions re-authenticate silently via the refresh
token, with no user interaction.

Subcommands
-----------
  login [--manual]   One-time interactive OAuth. Opens the Robinhood consent
                     page in a browser (or prints the URL with --manual for
                     headless/remote use) and stores the resulting tokens.
  status             Verify stored credentials by silently connecting. Never
                     prompts; exits non-zero (reauth_required) if a fresh
                     login is needed.
  logout             Delete the stored credentials and client registration.
  tools              List the tools the Robinhood MCP server exposes.
  call <tool> [json] Call a tool. Arguments are a JSON object passed as the
                     2nd arg or on stdin.

All commands except `login` are fully non-interactive: they rely on the
stored refresh token and fail with a clear message if re-auth is needed.

Environment
-----------
  ROBINHOOD_MCP_HOME          Persistent dir for credentials.
                              Default: $XDG_CONFIG_HOME/robinhood-mcp
                              or ~/.config/robinhood-mcp
  ROBINHOOD_MCP_URL           Override the MCP server URL.
                              Default: https://agent.robinhood.com/mcp/trading
  ROBINHOOD_MCP_SCOPE         Optional OAuth scope string.
  ROBINHOOD_MCP_REDIRECT_URI  Override the loopback redirect URI.
                              Default: http://localhost:8765/callback
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import anyio

from mcp import ClientSession
from mcp.client.auth import OAuthClientProvider, TokenStorage
from mcp.client.streamable_http import streamablehttp_client
from mcp.shared.auth import (
    OAuthClientInformationFull,
    OAuthClientMetadata,
    OAuthToken,
)

DEFAULT_SERVER_URL = "https://agent.robinhood.com/mcp/trading"
DEFAULT_REDIRECT_URI = "http://localhost:8765/callback"
CLIENT_NAME = "OpenClaw Robinhood Skill"
EXPIRY_SKEW_SECONDS = 60  # refresh slightly before the server-side expiry


class ReauthRequired(Exception):
    """Raised when a silent flow would otherwise require user interaction."""


# --------------------------------------------------------------------------- #
# Persistence
# --------------------------------------------------------------------------- #
def creds_home() -> Path:
    env = os.environ.get("ROBINHOOD_MCP_HOME")
    if env:
        return Path(env).expanduser()
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg).expanduser() if xdg else Path.home() / ".config"
    return base / "robinhood-mcp"


class FileTokenStorage(TokenStorage):
    """Persists OAuth tokens + the registered client to disk.

    The MCP SDK loads tokens on startup but does not restore the access
    token's expiry across processes, so it would trust a stale token and 401
    into an interactive re-auth. We persist an absolute expiry and blank the
    access token once it is (nearly) expired, which steers the SDK into its
    silent refresh-token path instead.
    """

    def __init__(self, home: Path):
        self.home = home
        self.tokens_path = home / "credentials.json"
        self.client_path = home / "client.json"

    def _ensure_home(self) -> None:
        self.home.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(self.home, 0o700)
        except OSError:
            pass

    @staticmethod
    def _write_private(path: Path, text: str) -> None:
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(text)
        try:
            os.chmod(tmp, 0o600)
        except OSError:
            pass
        os.replace(tmp, path)

    async def get_tokens(self) -> OAuthToken | None:
        if not self.tokens_path.exists():
            return None
        data = json.loads(self.tokens_path.read_text())
        expires_at = data.pop("_expires_at", None)
        token = OAuthToken.model_validate(data)
        if (
            expires_at is not None
            and token.refresh_token
            and time.time() >= (expires_at - EXPIRY_SKEW_SECONDS)
        ):
            # Force the SDK to refresh rather than trust the stale token.
            token.access_token = ""
        return token

    async def set_tokens(self, tokens: OAuthToken) -> None:
        self._ensure_home()
        # Some servers omit refresh_token on refresh responses; keep the old one.
        if not tokens.refresh_token and self.tokens_path.exists():
            try:
                prev = json.loads(self.tokens_path.read_text())
                if prev.get("refresh_token"):
                    tokens.refresh_token = prev["refresh_token"]
            except (OSError, json.JSONDecodeError):
                pass
        data = tokens.model_dump(exclude_none=True)
        if tokens.expires_in:
            data["_expires_at"] = time.time() + tokens.expires_in
        self._write_private(self.tokens_path, json.dumps(data, indent=2))

    async def get_client_info(self) -> OAuthClientInformationFull | None:
        if not self.client_path.exists():
            return None
        return OAuthClientInformationFull.model_validate_json(
            self.client_path.read_text()
        )

    async def set_client_info(self, client_info: OAuthClientInformationFull) -> None:
        self._ensure_home()
        self._write_private(self.client_path, client_info.model_dump_json(indent=2))


# --------------------------------------------------------------------------- #
# OAuth handlers
# --------------------------------------------------------------------------- #
def _redirect_uri() -> str:
    return os.environ.get("ROBINHOOD_MCP_REDIRECT_URI", DEFAULT_REDIRECT_URI)


def _parse_callback(raw: str) -> tuple[str, str | None]:
    raw = raw.strip()
    query = urlparse(raw).query if "?" in raw or raw.startswith("http") else raw
    params = parse_qs(query)
    if params.get("error"):
        raise ReauthRequired(
            f"Authorization denied: {params['error'][0]} "
            f"{params.get('error_description', [''])[0]}".strip()
        )
    code = params.get("code", [None])[0]
    if not code:
        raise ReauthRequired("No authorization code found in the pasted redirect URL.")
    return code, params.get("state", [None])[0]


def _loopback_callback(redirect_uri: str):
    """Return an async callback handler backed by a one-shot loopback server."""
    from http.server import BaseHTTPRequestHandler, HTTPServer

    parsed = urlparse(redirect_uri)
    host = parsed.hostname or "localhost"
    port = parsed.port or 80
    captured: dict[str, str | None] = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            q = parse_qs(urlparse(self.path).query)
            captured["code"] = q.get("code", [None])[0]
            captured["state"] = q.get("state", [None])[0]
            captured["error"] = q.get("error", [None])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                b"<html><body style='font-family:sans-serif'>"
                b"<h2>Robinhood authorization complete.</h2>"
                b"<p>You can close this tab and return to the terminal.</p>"
                b"</body></html>"
            )

        def log_message(self, *args):  # silence
            pass

    async def handler() -> tuple[str, str | None]:
        def serve() -> None:
            server = HTTPServer((host, port), Handler)
            server.timeout = 300
            server.handle_request()
            server.server_close()

        await anyio.to_thread.run_sync(serve)
        if captured.get("error"):
            raise ReauthRequired(f"Authorization denied: {captured['error']}")
        if not captured.get("code"):
            raise ReauthRequired("Timed out waiting for the authorization redirect.")
        return captured["code"], captured.get("state")

    return handler


def _manual_callback():
    async def handler() -> tuple[str, str | None]:
        print(
            "\nAfter approving in Robinhood (including the mobile-app "
            "verification), your browser is redirected to a localhost URL that "
            "will not load. Copy that full URL from the address bar and paste "
            "it here:",
            file=sys.stderr,
        )
        raw = await anyio.to_thread.run_sync(lambda: sys.stdin.readline())
        if not raw:
            raise ReauthRequired("No redirect URL provided on stdin.")
        return _parse_callback(raw)

    return handler


def _interactive_redirect(manual: bool):
    async def handler(authorization_url: str) -> None:
        print("\n" + "=" * 72, file=sys.stderr)
        print("Open this URL on a desktop browser to authorize Robinhood:", file=sys.stderr)
        print("\n  " + authorization_url + "\n", file=sys.stderr)
        print("=" * 72, file=sys.stderr)
        if not manual:
            try:
                import webbrowser

                webbrowser.open(authorization_url)
            except Exception:
                pass

    return handler


async def _non_interactive_redirect(authorization_url: str) -> None:
    raise ReauthRequired(
        "Stored Robinhood credentials are missing or expired. "
        "Run `robinhood_mcp.py login` to re-authenticate."
    )


async def _non_interactive_callback() -> tuple[str, str | None]:
    raise ReauthRequired(
        "Stored Robinhood credentials are missing or expired. "
        "Run `robinhood_mcp.py login` to re-authenticate."
    )


# --------------------------------------------------------------------------- #
# Provider construction
# --------------------------------------------------------------------------- #
def build_provider(*, interactive: bool, manual: bool = False) -> OAuthClientProvider:
    redirect_uri = _redirect_uri()
    scope = os.environ.get("ROBINHOOD_MCP_SCOPE")
    metadata = OAuthClientMetadata(
        client_name=CLIENT_NAME,
        redirect_uris=[redirect_uri],
        grant_types=["authorization_code", "refresh_token"],
        response_types=["code"],
        token_endpoint_auth_method="none",
        scope=scope,
    )
    if interactive:
        redirect_handler = _interactive_redirect(manual)
        callback_handler = (
            _manual_callback() if manual else _loopback_callback(redirect_uri)
        )
    else:
        redirect_handler = _non_interactive_redirect
        callback_handler = _non_interactive_callback

    return OAuthClientProvider(
        server_url=server_url(),
        client_metadata=metadata,
        storage=FileTokenStorage(creds_home()),
        redirect_handler=redirect_handler,
        callback_handler=callback_handler,
    )


def server_url() -> str:
    return os.environ.get("ROBINHOOD_MCP_URL", DEFAULT_SERVER_URL)


# --------------------------------------------------------------------------- #
# Session helpers
# --------------------------------------------------------------------------- #
def _unwrap(exc: BaseException) -> BaseException:
    """Drill into anyio/ExceptionGroup wrappers to the most useful cause."""
    seen = set()
    while True:
        if id(exc) in seen:
            return exc
        seen.add(id(exc))
        inner = getattr(exc, "exceptions", None)
        if inner:
            # Prefer a ReauthRequired anywhere in the group, else the first leaf.
            reauth = next((e for e in inner if isinstance(e, ReauthRequired)), None)
            exc = reauth or inner[0]
            continue
        return exc


async def _with_session(provider: OAuthClientProvider, fn):
    async with streamablehttp_client(server_url(), auth=provider) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            return await fn(session)


async def run_session(provider: OAuthClientProvider, fn):
    """Run `fn(session)`, normalizing transport/auth failures into clean errors.

    Raises ReauthRequired for interaction-needed cases; otherwise raises a
    RuntimeError carrying a human-readable message.
    """
    try:
        return await _with_session(provider, fn)
    except ReauthRequired:
        raise
    except BaseException as exc:  # noqa: BLE001 - normalize everything else
        cause = _unwrap(exc)
        if isinstance(cause, ReauthRequired):
            raise cause
        raise RuntimeError(f"{type(cause).__name__}: {cause}") from cause


def _fail(error: str, message: str, code: int = 1) -> int:
    json.dump({"error": error, "message": message}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return code


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
async def cmd_login(args) -> int:
    provider = build_provider(interactive=True, manual=args.manual)

    async def fn(session):
        return await session.list_tools()

    try:
        tools = await run_session(provider, fn)
    except ReauthRequired as e:
        return _fail("auth_failed", str(e))
    except RuntimeError as e:
        return _fail("connection_error", str(e))
    home = creds_home()
    print(
        json.dumps(
            {
                "status": "authenticated",
                "credentials_path": str(home / "credentials.json"),
                "server_url": server_url(),
                "tools_available": len(tools.tools),
            },
            indent=2,
        )
    )
    print(
        "\nCredentials stored. Future sessions will refresh silently as long as "
        f"{home} is persisted across sessions.",
        file=sys.stderr,
    )
    return 0


async def cmd_status(args) -> int:
    home = creds_home()
    creds = home / "credentials.json"
    if not creds.exists():
        return _fail(
            "not_authenticated",
            f"No stored credentials at {creds}. Run `login` first.",
            code=2,
        )
    provider = build_provider(interactive=False)

    async def fn(session):
        return await session.list_tools()

    try:
        tools = await run_session(provider, fn)
    except ReauthRequired as e:
        return _fail("reauth_required", str(e), code=2)
    except RuntimeError as e:
        return _fail("connection_error", str(e))
    print(
        json.dumps(
            {
                "status": "authenticated",
                "credentials_path": str(creds),
                "server_url": server_url(),
                "tools_available": len(tools.tools),
            },
            indent=2,
        )
    )
    return 0


async def cmd_logout(args) -> int:
    home = creds_home()
    removed = []
    for name in ("credentials.json", "client.json"):
        p = home / name
        if p.exists():
            p.unlink()
            removed.append(str(p))
    print(json.dumps({"status": "logged_out", "removed": removed}, indent=2))
    return 0


async def cmd_tools(args) -> int:
    provider = build_provider(interactive=False)

    async def fn(session):
        return await session.list_tools()

    try:
        result = await run_session(provider, fn)
    except ReauthRequired as e:
        return _fail("reauth_required", str(e), code=2)
    except RuntimeError as e:
        return _fail("connection_error", str(e))
    tools = [
        {
            "name": t.name,
            "description": t.description,
            "inputSchema": t.inputSchema,
        }
        for t in result.tools
    ]
    print(json.dumps({"tools": tools}, indent=2))
    return 0


async def cmd_call(args) -> int:
    if args.json_args is not None:
        raw = args.json_args
    elif not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
    else:
        raw = ""
    raw = raw or "{}"
    try:
        arguments = json.loads(raw)
    except json.JSONDecodeError as e:
        return _fail("invalid_arguments", f"Tool arguments must be valid JSON: {e}")
    if not isinstance(arguments, dict):
        return _fail("invalid_arguments", "Tool arguments must be a JSON object.")

    provider = build_provider(interactive=False)

    async def fn(session):
        return await session.call_tool(args.tool, arguments)

    try:
        result = await run_session(provider, fn)
    except ReauthRequired as e:
        return _fail("reauth_required", str(e), code=2)
    except RuntimeError as e:
        return _fail("connection_error", str(e))

    payload = result.model_dump(mode="json", exclude_none=True)
    print(json.dumps(payload, indent=2))
    return 1 if result.isError else 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Robinhood Trading MCP client.")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("login", help="One-time interactive OAuth login.")
    sp.add_argument(
        "--manual",
        action="store_true",
        help="Headless mode: print the auth URL and read the redirect URL from stdin "
        "(use when no local browser/loopback is reachable, e.g. remote sessions).",
    )
    sp.set_defaults(func=cmd_login)

    sp = sub.add_parser("status", help="Verify stored credentials (silent).")
    sp.set_defaults(func=cmd_status)

    sp = sub.add_parser("logout", help="Delete stored credentials.")
    sp.set_defaults(func=cmd_logout)

    sp = sub.add_parser("tools", help="List Robinhood MCP tools.")
    sp.set_defaults(func=cmd_tools)

    sp = sub.add_parser("call", help="Call a Robinhood MCP tool.")
    sp.add_argument("tool", help="Tool name (see `tools`).")
    sp.add_argument(
        "json_args",
        nargs="?",
        default=None,
        help="JSON object of arguments. Omit to read from stdin.",
    )
    sp.set_defaults(func=cmd_call)
    return p


def main() -> int:
    args = build_parser().parse_args()
    try:
        return anyio.run(lambda: args.func(args))
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
