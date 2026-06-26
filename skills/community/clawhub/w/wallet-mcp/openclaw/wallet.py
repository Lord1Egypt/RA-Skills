#!/usr/bin/env python3
"""
openclaw/wallet.py — Thin CLI wrapper for wallet-mcp.

Used by OpenClaw agents to call wallet-mcp functions directly
(no MCP protocol required; direct Python import).

Usage:
    python wallet.py <command> [--arg value ...]

Examples:
    python wallet.py generate_wallets --chain solana --count 10 --label airdrop1
    python wallet.py list_wallets --label airdrop1
    python wallet.py group_summary
    python wallet.py get_balance_batch --label airdrop1
    python wallet.py tag_wallets --label airdrop1 --tag funded
    python wallet.py delete_group --label airdrop1
    python wallet.py close_token_accounts --private-key 5Kd3...
    python wallet.py scan_token_accounts --address So1ana...
    python wallet.py send_native_multi --from-key 5Kd3... --label airdrop1 --amount 0.01 --chain solana
    python wallet.py sweep_wallets --to-address So1ana... --chain solana --label airdrop1
    python wallet.py scan_token_balances --chain solana --label airdrop1
    python wallet.py export_wallets --label airdrop1 --format json --path /tmp/backup.json
    python wallet.py import_wallets --path /tmp/backup.json --label airdrop2
"""
import argparse
import json
import sys
import os
import glob as _glob

# 1. Allow running from a local clone (wallet.py lives in openclaw/, wallet_mcp in ../src/)
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, ".."))
sys.path.insert(0, os.path.join(_here, "..", "src"))

# 2. Find wallet_mcp installed via `uv tool install wallet-mcp`
for _pattern in [
    os.path.expanduser("~/.local/share/uv/tools/wallet-mcp/lib/python*/site-packages"),
    "/root/.local/share/uv/tools/wallet-mcp/lib/python*/site-packages",
    "/home/*/.local/share/uv/tools/wallet-mcp/lib/python*/site-packages",
]:
    for _sp in _glob.glob(_pattern):
        if os.path.isdir(os.path.join(_sp, "wallet_mcp")):
            sys.path.insert(0, _sp)
            break

# Load .env before importing wallet_mcp
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
except ImportError:
    pass


def _out(data: dict) -> None:
    print(json.dumps(data, indent=2))


def _err(msg: str) -> None:
    print(json.dumps({"status": "error", "message": msg}))
    sys.exit(1)


# ── Commands ──────────────────────────────────────────────────────────────

def cmd_generate_wallets(args):
    from wallet_mcp.core.generator import generate_wallets
    wallets = generate_wallets(
        chain=args.chain, count=args.count,
        label=args.label, tags=args.tags or ""
    )
    _out({"status": "success", "chain": args.chain,
          "label": args.label, "generated": len(wallets),
          "wallets": [{"address": w["address"]} for w in wallets]})


def _resolve_sender_key(args):
    """Return private key: from --from-key directly, or looked up via --from-label."""
    if getattr(args, "from_key", None):
        return args.from_key
    if getattr(args, "from_label", None):
        from wallet_mcp.core.storage import filter_wallets
        wallets = filter_wallets(chain=args.chain, label=args.from_label)
        if not wallets:
            _err(f"No wallet found for from_label={args.from_label} chain={args.chain}")
        return wallets[0]["private_key"]
    _err("Provide --from-key <PRIVATE_KEY> or --from-label <LABEL>")


def cmd_send_native_multi(args):
    from wallet_mcp.core.storage import filter_wallets
    from wallet_mcp.core.distributor import send_native_multi
    sender_key = _resolve_sender_key(args)
    recipients = filter_wallets(chain=args.chain, label=args.label,
                                tag=args.tag or None)
    if not recipients:
        _err(f"No wallets found for chain={args.chain} label={args.label}")
    _out(send_native_multi(
        from_private_key=sender_key,
        recipients=recipients,
        amount=args.amount,
        chain=args.chain,
        rpc_url=args.rpc or None,
        randomize=args.randomize,
        delay_min=args.delay_min,
        delay_max=args.delay_max,
        retry_attempts=args.retries,
    ))


def cmd_add_wallet(args):
    """Import a single wallet by private key — address is derived automatically."""
    import base58
    from wallet_mcp.core.storage import load_wallets, save_wallets_batch
    from wallet_mcp.core.utils import now_iso

    chain = args.chain.lower()
    if chain == "solana":
        from solders.keypair import Keypair
        kp      = Keypair.from_bytes(base58.b58decode(args.private_key))
        address = str(kp.pubkey())
    elif chain == "evm":
        from eth_account import Account
        address = Account.from_key(args.private_key).address
    else:
        _err(f"Unsupported chain: {chain}")

    existing = {w["address"] for w in load_wallets()}
    if address in existing:
        _out({"status": "skipped", "address": address,
              "reason": "address already in storage"})
        return

    save_wallets_batch([{
        "address":     address,
        "private_key": args.private_key,
        "chain":       chain,
        "label":       args.label,
        "tags":        args.tags or "",
        "created_at":  now_iso(),
    }])
    _out({"status": "success", "address": address, "chain": chain, "label": args.label})


def cmd_list_wallets(args):
    from wallet_mcp.core.manager import list_wallets
    wallets = list_wallets(chain=args.chain or None, label=args.label or None,
                           tag=args.tag or None, show_keys=args.show_keys)
    _out({"status": "success", "count": len(wallets), "wallets": wallets})


def cmd_close_token_accounts(args):
    from wallet_mcp.core.solana import close_token_accounts
    result = close_token_accounts(private_key_b58=args.private_key,
                                  rpc_url=args.rpc or None,
                                  close_non_empty=args.close_non_empty)
    _out({"status": "success", **result})


def cmd_scan_token_accounts(args):
    from wallet_mcp.core.solana import get_token_accounts, DEFAULT_RPC
    accounts = get_token_accounts(args.address, args.rpc or DEFAULT_RPC)
    empty = [a for a in accounts if a["amount"] == 0]
    _out({"status": "success", "total": len(accounts),
          "empty": len(empty), "non_empty": len(accounts) - len(empty),
          "accounts": accounts})


def cmd_get_balance_batch(args):
    from wallet_mcp.core.manager import get_balance_batch
    result = get_balance_batch(chain=args.chain or None, label=args.label or None,
                               tag=args.tag or None, rpc_url=args.rpc or None)
    _out({"status": "success", **result})


def cmd_tag_wallets(args):
    from wallet_mcp.core.manager import tag_label
    _out({"status": "success", **tag_label(label=args.label, tag=args.tag)})


def cmd_group_summary(_args):
    from wallet_mcp.core.manager import group_summary
    _out({"status": "success", "groups": group_summary()})


def cmd_delete_group(args):
    from wallet_mcp.core.manager import delete_group
    _out({"status": "success", **delete_group(label=args.label)})


def cmd_sweep_wallets(args):
    from wallet_mcp.core.storage import filter_wallets
    from wallet_mcp.core.distributor import sweep_native_multi

    # Resolve destination: --to-address or --to-label
    to_address = args.to_address
    if not to_address and args.to_label:
        dest_wallets = filter_wallets(chain=args.chain, label=args.to_label)
        if not dest_wallets:
            _err(f"No wallet found for to_label={args.to_label} chain={args.chain}")
        to_address = dest_wallets[0]["address"]
    if not to_address:
        _err("Provide --to-address <ADDRESS> or --to-label <LABEL>")

    wallets = filter_wallets(chain=args.chain, label=args.label or None,
                             tag=args.tag or None)
    if not wallets:
        _err(f"No wallets found for chain={args.chain} label={args.label}")
    _out(sweep_native_multi(
        wallets=wallets,
        to_address=to_address,
        chain=args.chain,
        rpc_url=args.rpc or None,
        leave_lamports=args.leave_lamports,
        delay_min=args.delay_min,
        delay_max=args.delay_max,
        retry_attempts=args.retries,
    ))


def cmd_scan_token_balances(args):
    from wallet_mcp.core.manager import scan_token_balances
    result = scan_token_balances(
        chain=args.chain,
        label=args.label or None,
        tag=args.tag or None,
        token=args.token or None,
        rpc_url=args.rpc or None,
    )
    _out({"status": "success", **result})


def cmd_export_wallets(args):
    from wallet_mcp.core.storage import filter_wallets
    from wallet_mcp.core.exporter import export_wallets
    wallets = filter_wallets(chain=args.chain or None, label=args.label or None,
                             tag=args.tag or None)
    if not wallets:
        _err("No wallets match the given filters.")
    result = export_wallets(wallets=wallets, fmt=args.format,
                            output_path=args.path or None,
                            include_keys=args.include_keys)
    _out({"status": "success", **result})


def cmd_import_wallets(args):
    from wallet_mcp.core.importer import import_wallets
    result = import_wallets(file_path=args.path, fmt=args.format,
                            label=args.label or None, tags=args.tags or "")
    _out({"status": "success", **result})


# ── Parser ────────────────────────────────────────────────────────────────

def build_parser():
    p = argparse.ArgumentParser(prog="wallet.py",
                                description="wallet-mcp CLI wrapper for OpenClaw")
    sub = p.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    # generate_wallets
    g = sub.add_parser("generate_wallets")
    g.add_argument("--chain",  required=True, choices=["solana", "evm"])
    g.add_argument("--count",  required=True, type=int)
    g.add_argument("--label",  required=True)
    g.add_argument("--tags",   default="")

    # send_native_multi
    s = sub.add_parser("send_native_multi")
    key_group = s.add_mutually_exclusive_group(required=True)
    key_group.add_argument("--from-key",   dest="from_key",   default=None,
                           help="sender private key (base58/hex)")
    key_group.add_argument("--from-label", dest="from_label", default=None,
                           help="label of a stored sender wallet (no key in chat)")
    s.add_argument("--label",     required=True)
    s.add_argument("--amount",    required=True, type=float)
    s.add_argument("--chain",     required=True, choices=["solana", "evm"])
    s.add_argument("--rpc",       default=None)
    s.add_argument("--tag",       default=None)
    s.add_argument("--randomize", action="store_true")
    s.add_argument("--delay-min", type=int, default=1,  dest="delay_min")
    s.add_argument("--delay-max", type=int, default=30, dest="delay_max")
    s.add_argument("--retries",   type=int, default=3)

    # list_wallets
    lw = sub.add_parser("list_wallets")
    lw.add_argument("--chain",     default=None)
    lw.add_argument("--label",     default=None)
    lw.add_argument("--tag",       default=None)
    lw.add_argument("--show-keys", action="store_true", dest="show_keys")

    # close_token_accounts
    c = sub.add_parser("close_token_accounts")
    c.add_argument("--private-key",     required=True, dest="private_key")
    c.add_argument("--rpc",             default=None)
    c.add_argument("--close-non-empty", action="store_true", dest="close_non_empty")

    # scan_token_accounts
    sc = sub.add_parser("scan_token_accounts")
    sc.add_argument("--address", required=True)
    sc.add_argument("--rpc",     default=None)

    # get_balance_batch
    b = sub.add_parser("get_balance_batch")
    b.add_argument("--chain",  default=None)
    b.add_argument("--label",  default=None)
    b.add_argument("--tag",    default=None)
    b.add_argument("--rpc",    default=None)

    # tag_wallets
    t = sub.add_parser("tag_wallets")
    t.add_argument("--label", required=True)
    t.add_argument("--tag",   required=True)

    # group_summary
    sub.add_parser("group_summary")

    # delete_group
    d = sub.add_parser("delete_group")
    d.add_argument("--label", required=True)

    # sweep_wallets
    sw = sub.add_parser("sweep_wallets")
    to_group = sw.add_mutually_exclusive_group(required=True)
    to_group.add_argument("--to-address", dest="to_address", default=None,
                          help="destination public address")
    to_group.add_argument("--to-label",   dest="to_label",   default=None,
                          help="label of a stored destination wallet")
    sw.add_argument("--chain",          required=True, choices=["solana", "evm"])
    sw.add_argument("--label",          default=None)
    sw.add_argument("--tag",            default=None)
    sw.add_argument("--rpc",            default=None)
    sw.add_argument("--leave-lamports", type=int, default=5000, dest="leave_lamports")
    sw.add_argument("--delay-min",      type=int, default=1,    dest="delay_min")
    sw.add_argument("--delay-max",      type=int, default=10,   dest="delay_max")
    sw.add_argument("--retries",        type=int, default=3)

    # scan_token_balances
    stb = sub.add_parser("scan_token_balances")
    stb.add_argument("--chain",  required=True, choices=["solana", "evm"])
    stb.add_argument("--label",  default=None)
    stb.add_argument("--tag",    default=None)
    stb.add_argument("--token",  default=None,
                     help="SPL mint (Solana) or ERC-20 contract address (EVM, required)")
    stb.add_argument("--rpc",    default=None)

    # export_wallets
    ew = sub.add_parser("export_wallets")
    ew.add_argument("--chain",        default=None)
    ew.add_argument("--label",        default=None)
    ew.add_argument("--tag",          default=None)
    ew.add_argument("--format",       default="json", choices=["json", "csv"])
    ew.add_argument("--path",         default=None)
    ew.add_argument("--include-keys", action="store_true", dest="include_keys")

    # import_wallets
    iw = sub.add_parser("import_wallets")
    iw.add_argument("--path",   required=True)
    iw.add_argument("--format", default="auto", choices=["auto", "json", "csv"])
    iw.add_argument("--label",  default=None)
    iw.add_argument("--tags",   default="")

    # add_wallet
    aw = sub.add_parser("add_wallet",
                        help="Import a single wallet by private key (address auto-derived)")
    aw.add_argument("--private-key", required=True, dest="private_key")
    aw.add_argument("--chain",       required=True, choices=["solana", "evm"])
    aw.add_argument("--label",       required=True)
    aw.add_argument("--tags",        default="")

    return p


DISPATCH = {
    "generate_wallets":     cmd_generate_wallets,
    "send_native_multi":    cmd_send_native_multi,
    "list_wallets":         cmd_list_wallets,
    "close_token_accounts": cmd_close_token_accounts,
    "scan_token_accounts":  cmd_scan_token_accounts,
    "get_balance_batch":    cmd_get_balance_batch,
    "tag_wallets":          cmd_tag_wallets,
    "group_summary":        cmd_group_summary,
    "delete_group":         cmd_delete_group,
    "sweep_wallets":        cmd_sweep_wallets,
    "scan_token_balances":  cmd_scan_token_balances,
    "export_wallets":       cmd_export_wallets,
    "import_wallets":       cmd_import_wallets,
    "add_wallet":           cmd_add_wallet,
}


def main():
    args = build_parser().parse_args()
    handler = DISPATCH.get(args.command)
    if not handler:
        _err(f"Unknown command: {args.command}")
    try:
        handler(args)
    except Exception as e:
        _err(str(e))


if __name__ == "__main__":
    main()
