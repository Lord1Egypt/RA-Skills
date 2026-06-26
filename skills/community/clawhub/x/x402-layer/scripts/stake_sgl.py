#!/usr/bin/env python3
"""
stake_sgl.py — Agentic $SGL staking.

Stake, unstake, claim rewards, and read positions on the on-chain $SGL staking
program with only a Solana wallet keypair. No browser, no dashboard.

Ownership model: staking is an on-chain Anchor program, so mutating actions get
an UNSIGNED transaction from the API, which this script signs locally with your
keypair and submits. The signature IS the proof of ownership (the program rejects
any signer that isn't the staker). Reads are public on-chain data.

This is NOT x402 — x402 moves a token to a payee; staking locks your own tokens
in a contract only you control, which requires your signature.

Env:
  SOLANA_SECRET_KEY   base58 / JSON-array / base64 secret key (required for
                      stake/unstake/claim; and to derive your wallet for reads)
  SGL_STAKING_URL     override base URL (default https://staking.x402layer.cc)

Usage:
  python3 stake_sgl.py analytics
  python3 stake_sgl.py positions [--wallet <ADDR>]
  python3 stake_sgl.py stake --role compute --amount 50000
  python3 stake_sgl.py unstake --role compute
  python3 stake_sgl.py claim-unstake --role compute
  python3 stake_sgl.py claim [--role compute]
"""

import argparse
import base64
import json
import os
import sys

import requests

BASE = os.getenv("SGL_STAKING_URL", "https://staking.x402layer.cc").rstrip("/")
ROLES = ("compute", "validator", "yield")
TIMEOUT = 60


# ─── Solana keypair / signing (solders) ──────────────────────────────────────

def _load_keypair():
    """Load a solders Keypair from SOLANA_SECRET_KEY (base58, JSON array, or base64)."""
    try:
        from solders.keypair import Keypair  # type: ignore
    except ImportError:
        sys.exit("solders not installed. Run: pip install -r requirements.txt")

    raw = os.getenv("SOLANA_SECRET_KEY")
    if not raw:
        sys.exit("Set SOLANA_SECRET_KEY (base58 secret string or JSON byte array).")
    raw = raw.strip()
    # JSON byte array
    if raw.startswith("["):
        try:
            return Keypair.from_bytes(bytes(json.loads(raw)))
        except Exception as exc:  # noqa: BLE001
            sys.exit(f"Invalid SOLANA_SECRET_KEY JSON array: {exc}")
    # base58
    try:
        return Keypair.from_base58_string(raw)
    except Exception:  # noqa: BLE001
        pass
    # base64
    try:
        return Keypair.from_bytes(base64.b64decode(raw))
    except Exception as exc:  # noqa: BLE001
        sys.exit(f"Unsupported SOLANA_SECRET_KEY format: {exc}")


def _sign_tx_b64(keypair, tx_b64: str) -> str:
    """Sign a base64 unsigned legacy transaction and return base64 signed."""
    from solders.transaction import Transaction  # type: ignore

    raw = base64.b64decode(tx_b64)
    tx = Transaction.from_bytes(raw)
    tx.sign([keypair], tx.message.recent_blockhash)
    return base64.b64encode(bytes(tx)).decode()


# ─── API helpers ─────────────────────────────────────────────────────────────

def _get(path: str) -> dict:
    r = requests.get(f"{BASE}{path}", timeout=TIMEOUT)
    data = r.json()
    if not r.ok:
        sys.exit(f"GET {path} failed ({r.status_code}): {data.get('error', data)}")
    return data


def _post(path: str, body: dict) -> dict:
    r = requests.post(f"{BASE}{path}", json=body, timeout=TIMEOUT)
    data = r.json()
    if not r.ok:
        msg = data.get("error", data)
        if isinstance(msg, dict):
            msg = msg.get("message", msg)
        sys.exit(f"POST {path} failed ({r.status_code}): {msg}")
    return data


def _prepare_sign_submit(prepare_path: str, body: dict) -> None:
    """POST a prepare endpoint, sign each returned tx, submit it."""
    keypair = _load_keypair()
    # Explicit warning before signing/submitting an on-chain transaction that
    # moves $SGL / changes your stake. Review the action before running.
    print(
        f"⚠️  This will SIGN and SUBMIT an on-chain Solana transaction "
        f"({prepare_path.rsplit('/', 1)[-1]}) from wallet {keypair.pubkey()}. "
        f"It moves $SGL / changes your stake and cannot be undone. "
        f"Set SGL_STAKING_URL only to a trusted host.",
        file=sys.stderr,
    )
    prep = _post(prepare_path, body)
    txs = prep.get("transactions", [])
    if not txs:
        sys.exit(f"No transactions returned: {json.dumps(prep)}")
    for t in txs:
        signed = _sign_tx_b64(keypair, t["transaction"])
        res = _post("/api/agent/submit", {"transaction": signed})
        print(f"✅ {t.get('description', prepare_path)}")
        print(f"   signature: {res.get('signature')}")
        if res.get("explorer"):
            print(f"   {res['explorer']}")


def _wallet_from_args(args) -> str:
    if getattr(args, "wallet", None):
        return args.wallet
    return str(_load_keypair().pubkey())


# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_analytics(_args):
    print(json.dumps(_get("/api/agent/analytics"), indent=2))


def cmd_positions(args):
    wallet = _wallet_from_args(args)
    print(json.dumps(_get(f"/api/agent/positions?wallet={wallet}"), indent=2))


def cmd_stake(args):
    wallet = str(_load_keypair().pubkey())
    _prepare_sign_submit("/api/agent/stake", {"wallet": wallet, "role": args.role, "amount": args.amount})


def cmd_unstake(args):
    wallet = str(_load_keypair().pubkey())
    _prepare_sign_submit("/api/agent/unstake", {"wallet": wallet, "role": args.role})


def cmd_claim_unstake(args):
    wallet = str(_load_keypair().pubkey())
    _prepare_sign_submit("/api/agent/claim-unstake", {"wallet": wallet, "role": args.role})


def cmd_claim(args):
    wallet = str(_load_keypair().pubkey())
    body = {"wallet": wallet}
    if args.role:
        body["role"] = args.role
    _prepare_sign_submit("/api/agent/claim", body)


def main():
    p = argparse.ArgumentParser(description="Agentic $SGL staking (stake / unstake / claim / read).")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("analytics", help="Global staking analytics (no auth).")

    sp = sub.add_parser("positions", help="A wallet's stake positions (no auth).")
    sp.add_argument("--wallet", help="Wallet address (defaults to your SOLANA_SECRET_KEY wallet).")

    sp = sub.add_parser("stake", help="Stake $SGL (signs + submits).")
    sp.add_argument("--role", required=True, choices=ROLES)
    sp.add_argument("--amount", required=True, type=float, help="$SGL to stake (min 50000).")

    sp = sub.add_parser("unstake", help="Begin unstake cooldown (signs + submits).")
    sp.add_argument("--role", required=True, choices=ROLES)

    sp = sub.add_parser("claim-unstake", help="Withdraw after cooldown (signs + submits).")
    sp.add_argument("--role", required=True, choices=ROLES)

    sp = sub.add_parser("claim", help="Claim USDC + $SGL rewards (signs + submits).")
    sp.add_argument("--role", choices=ROLES, help="Omit to claim every position with rewards.")

    args = p.parse_args()
    handlers = {
        "analytics": cmd_analytics,
        "positions": cmd_positions,
        "stake": cmd_stake,
        "unstake": cmd_unstake,
        "claim-unstake": cmd_claim_unstake,
        "claim": cmd_claim,
    }
    handlers[args.command](args)


if __name__ == "__main__":
    main()
