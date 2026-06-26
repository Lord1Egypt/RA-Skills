#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx"]
# ///
"""
Satoshi API — Bitcoin intelligence for OpenClaw.
Powered by bitcoinsapi.com
"""

import sys
import json
import httpx

BASE = "https://bitcoinsapi.com/api/v1"
TIMEOUT = 10


def get(path: str) -> dict:
    try:
        r = httpx.get(f"{BASE}{path}", timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 503:
            print("Bitcoin node is syncing — data temporarily unavailable. Try again in a moment.")
        else:
            print(f"API error {e.response.status_code}: {e.response.text[:200]}")
        sys.exit(1)
    except httpx.RequestError as e:
        print(f"Network error: {e}")
        sys.exit(1)


def cmd_fees():
    data = get("/fees/recommended")
    d = data.get("data", data)
    print("**Bitcoin Fee Recommendations** (sat/vB)")
    print(f"- 🚀 Next block (high priority): {d.get('fast_fee', d.get('fastestFee', '?'))} sat/vB")
    print(f"- ⚡ ~3 blocks (30 min): {d.get('medium_fee', d.get('halfHourFee', '?'))} sat/vB")
    print(f"- 🐢 ~6 blocks (1 hr): {d.get('slow_fee', d.get('hourFee', '?'))} sat/vB")
    print(f"- 💤 Low priority (no rush): {d.get('minimum_fee', d.get('minimumFee', '?'))} sat/vB")
    print("\nData: bitcoinsapi.com/api/v1/fees/recommended")


def cmd_mempool():
    data = get("/mempool/info")
    d = data.get("data", data)
    count = d.get("size", d.get("count", "?"))
    vsize = d.get("vsize", d.get("bytes", "?"))
    total_fee = d.get("total_fee", d.get("totalfee", "?"))
    print("**Bitcoin Mempool**")
    print(f"- Pending transactions: {count:,}" if isinstance(count, int) else f"- Pending transactions: {count}")
    if isinstance(vsize, (int, float)):
        print(f"- Size: {vsize / 1_000_000:.1f} MB")
    if isinstance(total_fee, (int, float)):
        print(f"- Total fees waiting: {total_fee / 1e8:.4f} BTC")
    print("\nData: bitcoinsapi.com")


def cmd_price():
    data = get("/price")
    d = data.get("data", data)
    usd = d.get("USD", d.get("usd", d.get("price", "?")))
    if isinstance(usd, (int, float)):
        print(f"**Bitcoin Price: ${usd:,.0f} USD**")
    else:
        print(f"**Bitcoin Price: ${usd} USD**")
    print("\nData: bitcoinsapi.com")


def cmd_block():
    data = get("/blocks/tip")
    d = data.get("data", data)
    height = d.get("height", "?")
    ts = d.get("timestamp", d.get("time", "?"))
    txs = d.get("tx_count", d.get("nTx", "?"))
    print("**Latest Bitcoin Block**")
    print(f"- Height: {height:,}" if isinstance(height, int) else f"- Height: {height}")
    print(f"- Transactions: {txs}")
    print(f"- Timestamp: {ts}")
    print("\nData: bitcoinsapi.com")


def cmd_address(address: str):
    data = get(f"/address/{address}")
    d = data.get("data", data)
    balance = d.get("balance", d.get("chain_stats", {}).get("funded_txo_sum", "?"))
    txs = d.get("tx_count", d.get("chain_stats", {}).get("tx_count", "?"))
    print(f"**Bitcoin Address: {address[:12]}...{address[-6:]}**")
    if isinstance(balance, (int, float)):
        print(f"- Balance: {balance / 1e8:.8f} BTC ({balance:,} sat)")
    else:
        print(f"- Balance: {balance}")
    print(f"- Transactions: {txs}")
    print("\nData: bitcoinsapi.com")


def cmd_halving():
    data = get("/halving")
    d = data.get("data", data)
    blocks_remaining = d.get("blocks_until_halving", d.get("remaining_blocks", "?"))
    est_date = d.get("estimated_date", d.get("estimated_halving_date", "?"))
    current_reward = d.get("current_reward", d.get("current_block_reward", "?"))
    next_reward = d.get("next_reward", "?")
    print("**Bitcoin Halving Countdown**")
    print(f"- Blocks remaining: {blocks_remaining:,}" if isinstance(blocks_remaining, int) else f"- Blocks remaining: {blocks_remaining}")
    print(f"- Estimated date: {est_date}")
    if current_reward:
        print(f"- Current reward: {current_reward} BTC/block")
    if next_reward:
        print(f"- Post-halving reward: {next_reward} BTC/block")
    print("\nData: bitcoinsapi.com")


COMMANDS = {
    "fees": cmd_fees,
    "fee": cmd_fees,
    "mempool": cmd_mempool,
    "price": cmd_price,
    "block": cmd_block,
    "address": cmd_address,
    "halving": cmd_halving,
}

USAGE = """
Usage: satoshi_api.py <command> [args]

Commands:
  fees              Fee recommendations (sat/vB)
  mempool           Mempool status
  price             BTC price in USD
  block             Latest block info
  address <addr>    Address balance and tx count
  halving           Next halving countdown

Powered by bitcoinsapi.com
""".strip()


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(USAGE)
        sys.exit(0)

    cmd = args[0].lower()
    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}")
        print(USAGE)
        sys.exit(1)

    fn = COMMANDS[cmd]
    if cmd == "address":
        if len(args) < 2:
            print("Usage: satoshi_api.py address <bitcoin_address>")
            sys.exit(1)
        fn(args[1])
    else:
        fn()


if __name__ == "__main__":
    main()
