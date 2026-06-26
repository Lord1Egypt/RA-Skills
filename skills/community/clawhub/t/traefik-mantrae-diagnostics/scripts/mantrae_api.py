#!/usr/bin/env python3
"""Read Mantrae Traefik dynamic configuration via its Connect RPC API."""

from __future__ import annotations

import argparse
import getpass
import json
import os
import ssl
import sys
import urllib.parse
import urllib.error
import urllib.request


DEFAULT_BASE_URL = "http://localhost:3000"

METHODS = {
    "version": "/mantrae.v1.UtilService/GetVersion",
    "dynamic-config": "/mantrae.v1.UtilService/GetDynamicConfig",
    "routers": "/mantrae.v1.RouterService/ListRouters",
    "services": "/mantrae.v1.ServiceService/ListServices",
    "middlewares": "/mantrae.v1.MiddlewareService/ListMiddlewares",
    "entrypoints": "/mantrae.v1.EntryPointService/ListEntryPoints",
    "transports": "/mantrae.v1.ServersTransportService/ListServersTransports",
    "profiles": "/mantrae.v1.ProfileService/ListProfiles",
    "agents": "/mantrae.v1.AgentService/ListAgents",
    "dns-providers": "/mantrae.v1.DNSProviderService/ListDNSProviders",
    "backups": "/mantrae.v1.BackupService/ListBackups",
    "audit-logs": "/mantrae.v1.AuditLogService/ListAuditLogs",
    "settings": "/mantrae.v1.SettingService/ListSettings",
}


def request_json(
    base_url: str,
    path: str,
    payload: dict,
    timeout: float,
    token: str | None = None,
    insecure: bool = False,
    connect_ip: str | None = None,
) -> dict:
    parsed = urllib.parse.urlparse(base_url)
    url_base = base_url.rstrip("/")
    host_header = None
    if connect_ip:
        netloc = connect_ip
        if parsed.port:
            netloc = f"{connect_ip}:{parsed.port}"
        url_base = urllib.parse.urlunparse(
            (parsed.scheme, netloc, parsed.path.rstrip("/"), "", "", "")
        )
        host_header = parsed.netloc
    url = url_base + path
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Connect-Protocol-Version": "1",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if host_header:
        headers["Host"] = host_header
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    context = ssl._create_unverified_context() if insecure else None
    with urllib.request.urlopen(req, timeout=timeout, context=context) as response:
        return json.loads(response.read())


def login(
    base_url: str,
    username: str | None,
    email: str | None,
    password: str,
    timeout: float,
    insecure: bool,
    connect_ip: str | None,
) -> str:
    payload = {"password": password}
    if email:
        payload["email"] = email
    elif username:
        payload["username"] = username
    else:
        raise ValueError("provide --username, --email, MANTRAE_USERNAME, or MANTRAE_EMAIL")
    data = request_json(
        base_url,
        "/mantrae.v1.UserService/LoginUser",
        payload,
        timeout,
        insecure=insecure,
        connect_ip=connect_ip,
    )
    token = data.get("token")
    if not token:
        raise RuntimeError("login succeeded but response did not include a token")
    return token


def pretty_print(data: dict, compact: bool) -> None:
    if compact:
        print(json.dumps(data, separators=(",", ":")))
    else:
        print(json.dumps(data, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Query Mantrae's Connect RPC API")
    parser.add_argument(
        "method",
        nargs="?",
        default="routers",
        help=f"Method alias. Aliases: {', '.join(sorted(METHODS))}",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("MANTRAE_BASE_URL", DEFAULT_BASE_URL),
        help=f"Mantrae base URL (default: {DEFAULT_BASE_URL}, env: MANTRAE_BASE_URL)",
    )
    parser.add_argument("--username", default=os.environ.get("MANTRAE_USERNAME"))
    parser.add_argument("--email", default=os.environ.get("MANTRAE_EMAIL"))
    parser.add_argument("--password", default=os.environ.get("MANTRAE_PASSWORD"))
    parser.add_argument("--token", default=os.environ.get("MANTRAE_TOKEN"))
    parser.add_argument("--timeout", type=float, default=8.0)
    parser.add_argument(
        "--profile-id",
        default=os.environ.get("MANTRAE_PROFILE_ID", "1"),
        help="Mantrae profile id for list/config methods (default: 1, env: MANTRAE_PROFILE_ID)",
    )
    parser.add_argument("--insecure", action="store_true", help="Skip TLS verification")
    parser.add_argument(
        "--connect-ip",
        default=os.environ.get("MANTRAE_CONNECT_IP"),
        help="Connect to this IP while preserving the base URL Host header",
    )
    parser.add_argument("--compact", action="store_true", help="Do not pretty-print JSON")
    parser.add_argument(
        "--message",
        default="{}",
        help="JSON request body for list/get methods (default: {})",
    )
    args = parser.parse_args()

    path = METHODS.get(args.method, args.method)
    if not path.startswith("/"):
        path = "/" + path

    token = args.token
    if not token:
        password = args.password
        if not password and (args.username or args.email):
            password = getpass.getpass("Mantrae password: ")
        if not password:
            print(
                "Missing auth: set MANTRAE_TOKEN or provide MANTRAE_USERNAME/MANTRAE_EMAIL + MANTRAE_PASSWORD",
                file=sys.stderr,
            )
            return 2
        try:
            token = login(
                args.base_url,
                args.username,
                args.email,
                password,
                args.timeout,
                args.insecure,
                args.connect_ip,
            )
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError, RuntimeError) as exc:
            print(f"Login failed: {exc}", file=sys.stderr)
            return 1

    try:
        payload = json.loads(args.message)
    except json.JSONDecodeError as exc:
        print(f"Invalid --message JSON: {exc}", file=sys.stderr)
        return 2
    if (
        "profileId" not in payload
        and args.method
        in {
            "dynamic-config",
            "routers",
            "services",
            "middlewares",
            "entrypoints",
            "transports",
        }
    ):
        payload["profileId"] = int(args.profile_id)
    if "limit" not in payload and args.method in {"routers", "services", "middlewares"}:
        payload["limit"] = -1

    try:
        data = request_json(
            args.base_url,
            path,
            payload,
            args.timeout,
            token,
            args.insecure,
            args.connect_ip,
        )
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace").strip()
        print(f"HTTP {exc.code} from {args.base_url.rstrip('/') + path}: {exc.reason}", file=sys.stderr)
        if detail:
            print(detail, file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Cannot reach {args.base_url.rstrip('/') + path}: {exc.reason}", file=sys.stderr)
        return 1
    except TimeoutError:
        print(f"Timed out reaching {args.base_url.rstrip('/') + path}", file=sys.stderr)
        return 1

    pretty_print(data, args.compact)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
