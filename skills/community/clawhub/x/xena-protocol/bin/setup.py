"""Setup orchestrator CLI. Subcommands called by SKILL.md's wizard flow.

The LLM-driven wizard talks to the user (e.g. 'paste your gmail account') and
invokes this script for each deterministic step. Each subcommand prints a
single JSON line to stdout for the LLM to parse.

Usage:
    python -m bin.setup check-config
    python -m bin.setup verify-gog-auth --account you@gmail.com
    python -m bin.setup generate-wallet
    python -m bin.setup wait-balance --address 0x... --min-wei 200000000000000
    python -m bin.setup stake --recipient 0x... --amount-wei 100000000000000 --private-key 0x...
    python -m bin.setup save-mode --mode reporter
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import subprocess

from bin.gog_client import is_gog_installed, verify_auth
from bin.registry_client import RegistryClient, generate_wallet

CONFIG_DIR = Path.home() / ".openclaw" / "phishing-detection"
CONFIG_FILE = CONFIG_DIR / "config.json"
AGENT_ROOT = Path(__file__).resolve().parent.parent
# Bundled with the skill (primary)
_BUNDLED_DEPLOYED = AGENT_ROOT / "data" / "deployed.json"
# Monorepo sibling (dev-time fallback — works when running from the repo checkout)
_SIBLING_DEPLOYED = AGENT_ROOT.parent / "contracts" / "deployed.json"
DEFAULT_DEPLOYED = _BUNDLED_DEPLOYED if _BUNDLED_DEPLOYED.exists() else _SIBLING_DEPLOYED


def _emit(payload: dict) -> None:
    print(json.dumps(payload))


def _load_config() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    return json.loads(CONFIG_FILE.read_text())


def _save_config(cfg: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2) + "\n")


def cmd_check_config(_args) -> int:
    cfg = _load_config()
    status = {
        "has_config": bool(cfg),
        "has_mode": bool(cfg.get("mode")),
        "has_gmail_account": bool(cfg.get("gmail_account")),
        "has_wallet": bool(cfg.get("wallet_address")),
        "mode": cfg.get("mode"),
        "setup_required": not (cfg.get("mode") and cfg.get("gmail_account")),
    }
    if cfg.get("mode") == "reporter":
        status["setup_required"] = status["setup_required"] or not cfg.get("wallet_address")
    status["gog_installed"] = is_gog_installed()
    _emit(status)
    return 0


def _gog_has_credentials() -> bool:
    """Check whether `gog auth credentials` has been configured at all."""
    try:
        result = subprocess.run(
            ["gog", "auth", "list", "--json"],
            capture_output=True, text=True, check=False, timeout=5,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
    if result.returncode == 0:
        return True
    err = (result.stderr or "").lower() + (result.stdout or "").lower()
    # gog prints specific errors when creds are missing vs when just empty
    return "credentials" not in err and "not configured" not in err


def _python_deps_ok() -> bool:
    try:
        import web3  # noqa: F401
        import bs4  # noqa: F401
        import dns  # noqa: F401
    except ImportError:
        return False
    return True


def cmd_doctor(args) -> int:
    """Full environment check. Reports which prerequisites are satisfied
    and gives the exact command to run for each missing one. The LLM in
    SKILL.md reads this and walks the user through gaps.
    """
    cfg = _load_config()

    # Collect facts
    gog_installed = is_gog_installed()
    gog_has_creds = _gog_has_credentials() if gog_installed else False
    gmail_account = args.account or cfg.get("gmail_account")
    gog_authed = (
        verify_auth(gmail_account) if gog_installed and gog_has_creds and gmail_account else False
    )
    deps_ok = _python_deps_ok()
    sepolia_rpc_set = bool(os.environ.get("SEPOLIA_RPC"))
    anthropic_set = bool(os.environ.get("ANTHROPIC_API_KEY"))

    checks = []

    checks.append({
        "name": "python_deps",
        "ok": deps_ok,
        "fix": (
            None if deps_ok else
            "pip install -r ~/.openclaw/skills/phishing-detection/requirements.txt"
        ),
        "detail": "Python packages (web3, beautifulsoup4, dnspython) available to this interpreter",
    })

    checks.append({
        "name": "anthropic_api_key",
        "ok": anthropic_set,
        "fix": (
            None if anthropic_set else
            "Add to ~/.zshrc:  export ANTHROPIC_API_KEY=sk-ant-...  then run `source ~/.zshrc`"
        ),
        "detail": "ANTHROPIC_API_KEY env var required for the LLM to classify ambiguous emails",
    })

    checks.append({
        "name": "gog_installed",
        "ok": gog_installed,
        "fix": None if gog_installed else "brew install steipete/tap/gogcli",
        "detail": "gog is OpenClaw's Google Workspace CLI (provides Gmail OAuth access)",
    })

    checks.append({
        "name": "gog_credentials",
        "ok": gog_has_creds,
        "fix": (
            None if gog_has_creds else (
                "You need a Google Cloud OAuth 'Desktop app' client. One-time steps:\n"
                "  1. Open https://console.cloud.google.com/apis/credentials in a browser.\n"
                "  2. Create a new project (e.g. 'OpenClaw Personal').\n"
                "  3. Enable the Gmail API: https://console.cloud.google.com/apis/library/gmail.googleapis.com\n"
                "  4. Configure the OAuth consent screen: User Type = External; "
                "add your own email as a Test User (keeps the app in Testing mode, no Google verification needed).\n"
                "  5. Create OAuth client ID: Application type = Desktop app. Name it 'OpenClaw'.\n"
                "  6. Click Download JSON. Save it somewhere like ~/Downloads.\n"
                "  7. Run: gog auth credentials ~/Downloads/client_secret_<long-string>.json\n"
                "     (path is the file you just downloaded)"
            )
        ),
        "detail": "gog needs a Google OAuth client credentials file to initiate user OAuth flows",
    })

    checks.append({
        "name": "gog_account_authed",
        "ok": gog_authed,
        "fix": (
            None if gog_authed else (
                f"Run: gog auth add {gmail_account or 'you@gmail.com'} --services gmail\n"
                "  (this opens a browser, asks you to grant Gmail read/modify access, "
                "then returns a green 'authenticated' in the terminal)"
            )
        ),
        "detail": f"{gmail_account or '(account unknown)'} must be listed in `gog auth list`",
    })

    checks.append({
        "name": "sepolia_rpc",
        "ok": sepolia_rpc_set,
        "fix": (
            None if sepolia_rpc_set else (
                "Reporter mode only (Watchers can skip). Get an Alchemy API key at https://alchemy.com\n"
                "  then add to ~/.zshrc:\n"
                "    export SEPOLIA_RPC=https://eth-sepolia.g.alchemy.com/v2/<YOUR_KEY>"
            )
        ),
        "detail": "SEPOLIA_RPC needed only for on-chain reads/writes (Reporter tier)",
    })

    all_required_ok = all(
        c["ok"] for c in checks if c["name"] in {
            "python_deps", "anthropic_api_key", "gog_installed",
            "gog_credentials", "gog_account_authed",
        }
    )

    _emit({
        "ok": all_required_ok,
        "gmail_account": gmail_account,
        "checks": checks,
    })
    return 0 if all_required_ok else 1


def cmd_verify_gog_auth(args) -> int:
    ok = verify_auth(args.account)
    _emit({"account": args.account, "authenticated": ok})
    return 0 if ok else 1


def cmd_generate_wallet(_args) -> int:
    address, pk = generate_wallet()
    cfg = _load_config()
    cfg["wallet_address"] = address
    cfg["wallet_private_key"] = pk  # in production: vault; here config
    _save_config(cfg)
    _emit({"address": address, "saved_to": str(CONFIG_FILE)})
    return 0


def cmd_wait_balance(args) -> int:
    rpc = os.environ.get("SEPOLIA_RPC")
    if not rpc:
        _emit({"error": "SEPOLIA_RPC not set"})
        return 2
    deployed = args.deployed or DEFAULT_DEPLOYED
    client = RegistryClient(rpc_url=rpc, deployed_json=deployed)

    deadline = time.time() + args.timeout
    while time.time() < deadline:
        balance = client.get_balance(args.address)
        if balance >= args.min_wei:
            _emit({"address": args.address, "balance": balance, "funded": True})
            return 0
        time.sleep(5)

    _emit({"address": args.address, "balance": balance, "funded": False, "timed_out": True})
    return 1


def cmd_stake(args) -> int:
    rpc = os.environ.get("SEPOLIA_RPC")
    if not rpc:
        _emit({"error": "SEPOLIA_RPC not set"})
        return 2
    deployed = args.deployed or DEFAULT_DEPLOYED
    client = RegistryClient(rpc_url=rpc, deployed_json=deployed)
    tx = client.stake(
        recipient=args.recipient,
        value_wei=args.amount_wei,
        private_key=args.private_key,
    )
    _emit({"tx": tx, "recipient": args.recipient, "amount_wei": args.amount_wei})
    return 0


def cmd_save_mode(args) -> int:
    if args.mode not in ("watcher", "reporter"):
        _emit({"error": "mode must be watcher or reporter"})
        return 2
    cfg = _load_config()
    cfg["mode"] = args.mode
    if args.gmail_account:
        cfg["gmail_account"] = args.gmail_account
    _save_config(cfg)
    _emit({"mode": args.mode, "saved_to": str(CONFIG_FILE)})
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check-config").set_defaults(func=cmd_check_config)

    p = sub.add_parser("doctor")
    p.add_argument("--account", help="Gmail account to verify (overrides saved config)")
    p.set_defaults(func=cmd_doctor)

    p = sub.add_parser("verify-gog-auth")
    p.add_argument("--account", required=True)
    p.set_defaults(func=cmd_verify_gog_auth)

    sub.add_parser("generate-wallet").set_defaults(func=cmd_generate_wallet)

    p = sub.add_parser("wait-balance")
    p.add_argument("--address", required=True)
    p.add_argument("--min-wei", type=int, required=True)
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--deployed", type=Path)
    p.set_defaults(func=cmd_wait_balance)

    p = sub.add_parser("stake")
    p.add_argument("--recipient", required=True)
    p.add_argument("--amount-wei", type=int, required=True)
    p.add_argument("--private-key", required=True)
    p.add_argument("--deployed", type=Path)
    p.set_defaults(func=cmd_stake)

    p = sub.add_parser("save-mode")
    p.add_argument("--mode", required=True)
    p.add_argument("--gmail-account")
    p.set_defaults(func=cmd_save_mode)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
