#!/usr/bin/env python3
"""Watch a Solana address for new inbound SOL transfers."""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

try:
    import httpx
except ImportError:
    import urllib.error
    import urllib.request

    class _Resp:
        def __init__(self, data: bytes, status: int = 200):
            self._data = data
            self.status_code = status

        def json(self) -> Any:
            return json.loads(self._data.decode())

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise RuntimeError(f"HTTP {self.status_code}")

    class httpx:  # type: ignore
        @staticmethod
        def post(url: str, json: dict | None = None, timeout: float = 30.0, headers: dict | None = None):
            data = None if json is None else __import__("json").dumps(json).encode()
            req = urllib.request.Request(
                url,
                data=data,
                headers={**(headers or {}), "Content-Type": "application/json"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    return _Resp(r.read(), getattr(r, "status", 200))
            except urllib.error.HTTPError as e:
                return _Resp(e.read() or b"{}", e.code)


RPC_DEFAULT = "https://api.mainnet-beta.solana.com"


def rpc(url: str, method: str, params: list[Any]) -> Any:
    r = httpx.post(url, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, timeout=30.0)
    r.raise_for_status()
    body = r.json()
    if body.get("error"):
        raise RuntimeError(body["error"])
    return body.get("result")


def load_state(path: Path) -> set[str]:
    if not path.exists():
        return set()
    try:
        data = json.loads(path.read_text())
        return set(data.get("seen") or [])
    except Exception:
        return set()


def save_state(path: Path, seen: set[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # keep last 500 sigs
    ordered = list(seen)[-500:]
    path.write_text(json.dumps({"seen": ordered}, indent=2))


def inbound_events(rpc_url: str, address: str, limit: int = 20) -> list[dict[str, Any]]:
    sigs = rpc(rpc_url, "getSignaturesForAddress", [address, {"limit": limit}]) or []
    out: list[dict[str, Any]] = []
    for item in sigs:
        sig = item.get("signature")
        if not sig or item.get("err"):
            continue
        tx = rpc(
            rpc_url,
            "getTransaction",
            [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}],
        )
        if not tx:
            continue
        meta = tx.get("meta") or {}
        if meta.get("err"):
            continue
        message = (tx.get("transaction") or {}).get("message") or {}
        account_keys = message.get("accountKeys") or []
        # normalize account keys
        keys: list[str] = []
        for k in account_keys:
            if isinstance(k, str):
                keys.append(k)
            elif isinstance(k, dict):
                keys.append(k.get("pubkey") or "")
        if address not in keys:
            continue
        idx = keys.index(address)
        pre = (meta.get("preBalances") or [0]) 
        post = (meta.get("postBalances") or [0])
        if idx >= len(pre) or idx >= len(post):
            continue
        delta = int(post[idx]) - int(pre[idx])
        if delta <= 0:
            continue
        # rough counterparties: accounts that lost lamports
        senders = []
        for i, key in enumerate(keys):
            if i == idx or not key:
                continue
            if i < len(pre) and i < len(post) and int(post[i]) < int(pre[i]):
                senders.append(key)
        out.append(
            {
                "signature": sig,
                "slot": tx.get("slot"),
                "lamports": delta,
                "sol": delta / 1_000_000_000,
                "from": senders,
                "to": address,
                "blockTime": tx.get("blockTime") or item.get("blockTime"),
            }
        )
    return out


def emit(event: dict[str, Any], webhook: str | None) -> None:
    line = json.dumps(event, separators=(",", ":"))
    print(line, flush=True)
    if webhook:
        try:
            httpx.post(webhook, json=event, timeout=15.0)
        except Exception as e:
            print(json.dumps({"warning": "webhook_failed", "error": str(e)}), file=sys.stderr)


def once(args: argparse.Namespace, seen: set[str]) -> set[str]:
    events = inbound_events(args.rpc, args.address, limit=args.limit)
    min_lamports = int(args.min_sol * 1_000_000_000)
    for ev in reversed(events):  # oldest first among batch
        sig = ev["signature"]
        if sig in seen:
            continue
        if ev["lamports"] < min_lamports:
            seen.add(sig)
            continue
        emit(ev, args.webhook)
        seen.add(sig)
    return seen


def main() -> int:
    p = argparse.ArgumentParser(description="Watch Solana address for inbound SOL")
    p.add_argument("--address", required=True, help="Solana address to watch")
    p.add_argument("--rpc", default=RPC_DEFAULT)
    p.add_argument("--min-sol", type=float, default=0.001)
    p.add_argument("--state", type=Path, default=Path("/tmp/sol-inbound-state.json"))
    p.add_argument("--webhook", default=None)
    p.add_argument("--loop", type=int, default=0, help="Seconds between polls; 0 = once")
    p.add_argument("--limit", type=int, default=25)
    args = p.parse_args()

    seen = load_state(args.state)
    if args.loop and args.loop > 0:
        while True:
            try:
                seen = once(args, seen)
                save_state(args.state, seen)
            except Exception as e:
                print(json.dumps({"error": str(e)}), file=sys.stderr)
            time.sleep(args.loop)
    else:
        seen = once(args, seen)
        save_state(args.state, seen)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
