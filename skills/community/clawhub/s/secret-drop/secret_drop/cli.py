"""CLI entry point. Successful output contains metadata only, never plaintext."""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from secret_drop import MAX_SECRET_BYTES, __version__
from secret_drop.errors import SecretDropError
from secret_drop.providers.registry import PROVIDERS, retrieve_secret
from secret_drop.providers.share import DEFAULT_PWPUSH_API_BASE, create_push
from secret_drop.redact import redact_text, sanitize_url
from secret_drop.sources import read_secret_source
from secret_drop.writers import restart_openclaw_gateway, write_secret


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="secret-drop",
        description="Silently retrieve a one-time secret and write it without printing plaintext.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="Consume one secret link and write its payload")
    ingest.add_argument("url", help="One-time secret URL (the URL itself may remain in chat history)")
    ingest.add_argument(
        "--provider", choices=("auto", *PROVIDERS), default="auto", help="Provider adapter"
    )
    ingest.add_argument("--api-base", help="Custom provider API base for a self-hosted service")
    ingest.add_argument(
        "--to",
        dest="destination",
        required=True,
        choices=("openclaw-env", "openclaw-store", "dotenv", "file"),
        help="Destination writer",
    )
    ingest.add_argument("--name", help="Environment/store entry name")
    ingest.add_argument("--path", help="Target path for dotenv or file")
    ingest.add_argument(
        "--replace", action="store_true", help="Allow replacing an existing raw file destination"
    )
    ingest.add_argument(
        "--store-kind", choices=("secret", "env"), default="secret", help="OpenClaw store kind"
    )
    ingest.add_argument(
        "--allow-host", action="append", default=[], help="Exact egress host for a protected store entry"
    )
    ingest.add_argument(
        "--config-path", help="Bind the new store entry to this OpenClaw SecretRef config path"
    )
    ingest.add_argument(
        "--reload", action="store_true", help="Run openclaw secrets reload after a store write"
    )
    ingest.add_argument(
        "--allow-private-host",
        action="store_true",
        help="Allow a self-hosted provider on a private address (explicit opt-in)",
    )
    ingest.add_argument(
        "--restart-gateway",
        action="store_true",
        help="Run 'openclaw gateway restart --safe' when the destination requires a restart",
    )
    ingest.add_argument("--json", action="store_true", help="Emit secret-free JSON status")

    share = sub.add_parser("share", help="Create a one-time link from a local secret source")
    share.add_argument(
        "--from",
        dest="source",
        required=True,
        choices=("openclaw-env", "dotenv", "file"),
        help="Local source type",
    )
    share.add_argument("--name", help="Environment entry name")
    share.add_argument("--path", help="Source path for dotenv or file")
    share.add_argument(
        "--api-base",
        default=DEFAULT_PWPUSH_API_BASE,
        help="Password Pusher service root",
    )
    share.add_argument(
        "--allow-private-host",
        action="store_true",
        help="Allow a trusted self-hosted provider on a private address",
    )
    share.add_argument("--json", action="store_true", help="Emit secret-free JSON status")

    providers = sub.add_parser("providers", help="List supported adapters")
    providers.add_argument("--json", action="store_true")
    return parser


def _safe_error(message: str, *, secret: str | None, url: str | None) -> str:
    safe = redact_text(message, secret=secret, url=url)
    if url:
        safe = redact_text(safe, url=sanitize_url(url))
    return safe


def _emit(result: dict[str, Any], *, json_mode: bool) -> None:
    if json_mode:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return
    if result.get("ok"):
        if result.get("url"):
            print(result["url"])
            return
        name = f" as {result['name']}" if result.get("name") else ""
        if result.get("gateway_restarted"):
            suffix = " Gateway restart requested."
        elif result.get("restart_required"):
            suffix = " Gateway restart required."
        else:
            suffix = ""
        print(
            f"Stored {result.get('bytes', 0)} bytes{name} via {result.get('provider')} "
            f"to {result.get('destination')}.{suffix}"
        )
    else:
        print(f"Secret Drop failed: {result.get('error', 'unknown error')}", file=sys.stderr)


def _run_ingest(args: argparse.Namespace) -> int:
    secret: str | None = None
    try:
        provider, secret = retrieve_secret(
            args.url,
            provider=args.provider,
            api_base=args.api_base,
            allow_private=args.allow_private_host,
        )
        byte_count = len(secret.encode("utf-8"))
        if byte_count == 0:
            raise SecretDropError("Provider returned an empty secret.")
        if byte_count > MAX_SECRET_BYTES:
            raise SecretDropError(f"Secret exceeds the {MAX_SECRET_BYTES}-byte limit.")
        written = write_secret(
            destination=args.destination,
            secret=secret,
            name=args.name,
            path=args.path,
            store_kind=args.store_kind,
            allowed_hosts=args.allow_host,
            config_path=args.config_path,
            reload_runtime=args.reload,
            replace=args.replace,
        )
        restarted = False
        if args.restart_gateway and written.get("restart_required"):
            try:
                restart_openclaw_gateway()
            except SecretDropError as exc:
                raise SecretDropError(
                    "Secret was stored, but OpenClaw gateway restart failed."
                ) from exc
            restarted = True
            written["restart_required"] = False
        result = {
            "ok": True,
            "provider": provider,
            "bytes": byte_count,
            "gateway_restarted": restarted,
            **written,
        }
        _emit(result, json_mode=args.json)
        return 0
    except SecretDropError as exc:
        result = {"ok": False, "error": _safe_error(str(exc), secret=secret, url=args.url)}
        _emit(result, json_mode=args.json)
        return 2
    except Exception:
        result = {"ok": False, "error": "Unexpected internal failure; no secret was printed."}
        _emit(result, json_mode=args.json)
        return 3
    finally:
        secret = None


def _run_share(args: argparse.Namespace) -> int:
    secret: str | None = None
    try:
        secret = read_secret_source(source=args.source, path=args.path, name=args.name)
        result = create_push(
            secret,
            api_base=args.api_base,
            allow_private=args.allow_private_host,
        )
        _emit(result, json_mode=args.json)
        return 0
    except SecretDropError as exc:
        result = {
            "ok": False,
            "error": _safe_error(str(exc), secret=secret, url=args.api_base),
        }
        _emit(result, json_mode=args.json)
        return 2
    except Exception:
        result = {"ok": False, "error": "Unexpected internal failure; no secret was printed."}
        _emit(result, json_mode=args.json)
        return 3
    finally:
        secret = None


def main(argv: list[str] | None = None) -> int:
    os.umask(0o077)
    parser = _parser()
    args = parser.parse_args(argv)
    if args.command == "providers":
        data = {
            "providers": [
                {"id": "pwpush", "mode": "native", "zero_knowledge": False},
                {"id": "snappwd", "mode": "native", "zero_knowledge": True},
            ]
        }
        if args.json:
            print(json.dumps(data, sort_keys=True, separators=(",", ":")))
        else:
            for item in data["providers"]:
                print(f"{item['id']}\t{item['mode']}\tzero-knowledge={str(item['zero_knowledge']).lower()}")
        return 0
    if args.command == "share":
        return _run_share(args)
    return _run_ingest(args)


if __name__ == "__main__":
    raise SystemExit(main())
