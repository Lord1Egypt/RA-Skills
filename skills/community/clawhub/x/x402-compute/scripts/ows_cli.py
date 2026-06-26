#!/usr/bin/env python3
"""
Thin OpenWallet / OWS CLI wrapper for x402-compute agents.

This keeps x402-compute Python-first while allowing agents to use
Open Wallet Standard commands without exposing raw keys.
"""

import argparse
import os
import shutil
import subprocess
import sys
from typing import List


OWS_PINNED_PACKAGE = "@open-wallet-standard/core@0.5.0"


def build_ows_command(args: List[str]) -> List[str]:
    explicit_bin = os.getenv("OWS_BIN", "").strip()
    if explicit_bin:
        return [explicit_bin, *args]

    local_ows = shutil.which("ows")
    if local_ows:
        return [local_ows, *args]

    raise ValueError(
        "OWS binary not found. Install it with:\n"
        f"  npm install -g {OWS_PINNED_PACKAGE}\n"
        "Then ensure `ows` is in your PATH, or set OWS_BIN to the full executable path.\n"
        "Avoid runtime npx downloads for wallet operations."
    )


def run_ows(args: List[str], timeout: int = 180) -> int:
    proc = subprocess.run(build_ows_command(args), text=True, capture_output=True, timeout=timeout)
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    return int(proc.returncode)


def require_ows_wallet(cli_wallet: str | None = None) -> str:
    wallet = (cli_wallet or os.getenv("OWS_WALLET") or "").strip()
    if not wallet:
        raise ValueError("Set OWS_WALLET or pass --wallet <wallet-name-or-id>")
    return wallet


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run OpenWallet / OWS commands from x402-compute skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ows_cli.py run wallet list
  python ows_cli.py sign-message --chain eip155:8453 --wallet compute-wallet --message "hello"
  python ows_cli.py sign-message --chain solana --wallet compute-wallet --message "hello"
  python ows_cli.py key-create --name codex-compute --wallet compute-wallet

Notes:
  - Wrapper uses OWS_BIN first, then local `ows` in PATH.
  - Install OWS with a pinned version:
      npm install -g @open-wallet-standard/core@0.5.0
  - Do NOT rely on runtime npx downloads for wallet operations.
  - OWS currently fits compute auth and management/API-key workflows best.
  - Provision and extend still use direct payment-signing keys today.
""",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="Pass OWS args directly")
    run_parser.add_argument("ows_args", nargs=argparse.REMAINDER, help="Raw OWS arguments")

    sign_parser = sub.add_parser("sign-message", help="Sign a compute auth or test message through OWS")
    sign_parser.add_argument("--chain", required=True, help="Chain (use eip155:8453 for Base, or solana)")
    sign_parser.add_argument("--wallet", help="OWS wallet name or ID (falls back to OWS_WALLET)")
    sign_parser.add_argument("--message", required=True, help="Message to sign")
    sign_parser.add_argument("--json", action="store_true", help="Emit structured JSON from OWS")

    wallet_list_parser = sub.add_parser("wallet-list", help="List saved OWS wallets")

    key_create_parser = sub.add_parser("key-create", help="Create an OWS API key for agent access")
    key_create_parser.add_argument("--name", required=True, help="Key name")
    key_create_parser.add_argument("--wallet", action="append", default=[], help="Repeatable wallet name or ID")
    key_create_parser.add_argument("--policy", action="append", default=[], help="Repeatable policy ID")
    key_create_parser.add_argument("--expires-at", help="Optional ISO-8601 expiry")

    args = parser.parse_args()

    if args.command == "run":
        raw = list(args.ows_args)
        if raw and raw[0] == "--":
            raw = raw[1:]
        if not raw:
            parser.error("run requires at least one OWS argument, e.g.: run wallet list")
        return run_ows(raw)

    if args.command == "sign-message":
        wallet = require_ows_wallet(args.wallet)
        cmd = [
            "sign",
            "message",
            "--chain",
            args.chain,
            "--wallet",
            wallet,
            "--message",
            args.message,
        ]
        if args.json:
            cmd.append("--json")
        return run_ows(cmd)

    if args.command == "wallet-list":
        return run_ows(["wallet", "list"])

    if args.command == "key-create":
        cmd = ["key", "create", "--name", args.name]
        for wallet in args.wallet:
            cmd += ["--wallet", wallet]
        for policy in args.policy:
            cmd += ["--policy", policy]
        if args.expires_at:
            cmd += ["--expires-at", args.expires_at]
        return run_ows(cmd)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
