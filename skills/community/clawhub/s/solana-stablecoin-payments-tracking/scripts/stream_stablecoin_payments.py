"""
Bitquery Solana stablecoin transfers — real-time USDC / USDT stream
==================================================================
Subscribe to Bitquery WebSocket for Solana SPL transfers where Currency.MintAddress is
USDT (Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB) or USDC
(EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v), and where the instruction program
method does not include "swap" (case-insensitive), to reduce DEX-swap noise.

Each event includes Transfer (Amount, AmountInUSD, Sender/Receiver, Currency),
Instruction.Program.Method, Block (Time, Height, Slot), and Transaction
(Signature, Signer, Fee, FeeInUSD, FeePayer).

Usage:
    python scripts/stream_stablecoin_payments.py
    python scripts/stream_stablecoin_payments.py --timeout 60

Environment:
    BITQUERY_API_KEY — Bitquery token (required). Passed as ?token= in WebSocket URL only.
    Do not print or log the full WebSocket URL.
"""

import asyncio
import os
import sys
from urllib.parse import urlencode

from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport


BITQUERY_WS_BASE = "wss://streaming.bitquery.io/graphql"

STABLECOIN_TRANSFERS_SUBSCRIPTION = gql("""
subscription StablecoinTransfers {
  Solana {
    Transfers(
      where: {
        Transfer: {
          Currency: {
            MintAddress: {
              in: [
                "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
                "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
              ]
            }
          }
        }
        Instruction: {
          Program: {
            Method: { notIncludesCaseInsensitive: "swap" }
          }
        }
      }
    ) {
      Transfer {
        Amount
        AmountInUSD
        Sender {
          Address
          Owner
        }
        Receiver {
          Address
          Owner
        }
        Currency {
          Symbol
          Name
          MintAddress
        }
      }
      Instruction {
        Program {
          Method
        }
      }
      Block {
        Time
        Height
        Slot
      }
      Transaction {
        Signature
        Signer
        Fee
        FeeInUSD
        FeePayer
      }
    }
  }
}
""")


def get_api_key() -> str:
    key = os.getenv("BITQUERY_API_KEY")
    if not key:
        raise EnvironmentError(
            "BITQUERY_API_KEY is not set. "
            "Please export your Bitquery token:\n"
            "  export BITQUERY_API_KEY=your_token_here"
        )
    return key


def _addr_short(addr: str | None, head: int = 6, tail: int = 4) -> str:
    if not addr:
        return "N/A"
    s = str(addr)
    if len(s) <= head + tail + 3:
        return s
    return f"{s[:head]}...{s[-tail:]}"


def _fmt_num(value) -> str:
    if value is None:
        return "N/A"
    try:
        f = float(value)
        if f != f:
            return str(value)
        if abs(f) >= 1e6 or (abs(f) > 0 and abs(f) < 1e-4):
            return f"{f:,.8f}".rstrip("0").rstrip(".")
        return f"{f:,.6f}".rstrip("0").rstrip(".")
    except (ValueError, TypeError):
        return str(value)


def _fmt_usd(value) -> str:
    if value is None:
        return "N/A"
    try:
        return f"${float(value):,.4f}"
    except (ValueError, TypeError):
        return str(value)


def format_transfers(data: dict) -> str:
    """Format Solana.Transfers rows for display."""
    sol = (data or {}).get("Solana") or {}
    rows = sol.get("Transfers") or []
    if not rows:
        return ""

    lines: list[str] = []
    sep = "━" * 52

    for item in rows:
        xfer = item.get("Transfer") or {}
        instr = item.get("Instruction") or {}
        block = item.get("Block") or {}
        tx = item.get("Transaction") or {}

        cur = xfer.get("Currency") or {}
        symbol = cur.get("Symbol") or "?"
        mint = cur.get("MintAddress") or "?"
        name = cur.get("Name") or ""

        sender = xfer.get("Sender") or {}
        recv = xfer.get("Receiver") or {}
        amt = xfer.get("Amount")
        usd = xfer.get("AmountInUSD")

        method = (instr.get("Program") or {}).get("Method") or "?"

        time_str = block.get("Time") or "?"
        slot = block.get("Slot")
        height = block.get("Height")

        sig = tx.get("Signature") or "?"
        fee = tx.get("Fee")
        fee_usd = tx.get("FeeInUSD")
        fee_payer = tx.get("FeePayer")
        signer = tx.get("Signer")

        slot_h = f"Slot {slot}" if slot is not None else "Slot ?"
        if height is not None:
            slot_h += f"  Height {height}"

        cur_line = f"{symbol}"
        if name:
            cur_line += f" ({name})"
        cur_line += f"  [{_addr_short(mint, 4, 4)}]"

        lines.append(sep)
        lines.append(f"Solana stablecoin  @  {time_str}  |  {slot_h}")
        lines.append(cur_line)
        lines.append(
            f"Amount: {_fmt_num(amt)}  |  USD: {_fmt_usd(usd)}"
        )
        lines.append(
            f"From: {_addr_short(sender.get('Address'))}  (owner: {_addr_short(sender.get('Owner'))})"
        )
        lines.append(
            f"To:   {_addr_short(recv.get('Address'))}  (owner: {_addr_short(recv.get('Owner'))})"
        )
        lines.append(
            f"Tx: {_addr_short(sig, 8, 8)}  |  Fee: {_fmt_num(fee)}  |  Fee USD: {_fmt_usd(fee_usd)}"
        )
        if fee_payer:
            lines.append(f"Fee payer: {_addr_short(fee_payer)}")
        if signer:
            lines.append(f"Signer: {_addr_short(signer)}")
        lines.append(f"Program method: {method}")
        lines.append(sep)
        lines.append("")

    return "\n".join(lines)


async def run_stream(timeout_seconds: int | None = None) -> None:
    api_key = get_api_key()
    url = f"{BITQUERY_WS_BASE}?{urlencode({'token': api_key})}"
    transport = WebsocketsTransport(
        url=url,
        headers={"Sec-WebSocket-Protocol": "graphql-ws"},
    )

    event_count = 0

    async with Client(transport=transport) as session:
        print(
            "Connected. Streaming Solana USDC/USDT transfers. Ctrl+C to stop.\n"
        )

        async def consume():
            nonlocal event_count
            try:
                async for result in session.subscribe(
                    STABLECOIN_TRANSFERS_SUBSCRIPTION
                ):
                    event_count += 1
                    out = format_transfers(result)
                    if out:
                        print(out)
            except asyncio.CancelledError:
                pass

        if timeout_seconds is not None:
            try:
                await asyncio.wait_for(consume(), timeout=float(timeout_seconds))
            except asyncio.TimeoutError:
                print(
                    f"\nStopped after {timeout_seconds}s ({event_count} messages)."
                )
        else:
            await consume()


def main() -> None:
    timeout: int | None = None
    if len(sys.argv) > 1 and sys.argv[1] == "--timeout" and len(sys.argv) > 2:
        try:
            timeout = int(sys.argv[2])
        except ValueError:
            print(
                "Usage: python stream_stablecoin_payments.py [--timeout SECONDS]",
                file=sys.stderr,
            )
            sys.exit(2)

    try:
        asyncio.run(run_stream(timeout_seconds=timeout))
    except EnvironmentError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStream stopped by user.")


if __name__ == "__main__":
    main()
