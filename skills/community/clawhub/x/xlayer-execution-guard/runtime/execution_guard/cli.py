"""CLI for Execution Guard."""
import asyncio
import argparse
import json
import os
import sys

from .guard import ExecutionGuard
from .models import GuardIntent


async def main():
    parser = argparse.ArgumentParser(description="X Layer Execution Guard CLI")
    parser.add_argument("--agent", default="flasharb", help="Agent name")
    parser.add_argument("--intent-id", default="cli-demo", help="Intent ID")
    parser.add_argument("--from", dest="from_token", default="USDC", help="From token")
    parser.add_argument("--to", dest="to_token", default="OKB", help="To token")
    parser.add_argument("--amount", default="25", help="Amount")
    parser.add_argument(
        "--amount-mode",
        choices=["readable", "raw"],
        default=os.getenv("EXECUTION_GUARD_AMOUNT_MODE", "readable"),
        help="Use readable token units or raw base units for --amount",
    )
    parser.add_argument("--slippage", default="0.5", help="Slippage percent")
    parser.add_argument("--max-impact", default="1.20", help="Max price impact percent")
    parser.add_argument("--no-execute", action="store_true", help="Skip execution after verdict")
    parser.add_argument(
        "--execution-mode",
        choices=["proof", "agentic-wallet"],
        default=os.getenv("EXECUTION_GUARD_EXECUTION_MODE", "proof"),
        help="proof records a simulated evidence result; agentic-wallet uses onchainos swap execute",
    )
    parser.add_argument("--live", action="store_true", help="Alias for --execution-mode agentic-wallet")
    parser.add_argument("--wallet", default=os.getenv("EXECUTION_GUARD_WALLET", "default"), help="onchainos wallet name or address")
    parser.add_argument("--chain", default=os.getenv("ONCHAINOS_CHAIN_INDEX", "196"), help="Chain index/name for onchainos")
    parser.add_argument("--reason", help="Human-readable reason for the requested action")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()
    execution_mode = "agentic-wallet" if args.live else args.execution_mode

    guard = ExecutionGuard()

    intent = GuardIntent(
        agent_name=args.agent,
        intent_id=args.intent_id,
        from_token=args.from_token,
        to_token=args.to_token,
        amount=args.amount,
        slippage_percent=args.slippage,
        reason=args.reason or f"CLI request: {args.from_token} -> {args.to_token}",
        max_price_impact_percent=args.max_impact,
        execute_after_verdict=not args.no_execute,
        amount_mode=args.amount_mode,
        execution_mode=execution_mode,
        wallet=args.wallet,
        chain=args.chain,
    )

    result = await guard.run(intent)

    output = result.to_dict()

    if args.output:
        with open(args.output, "w") as f:
            json.dump(output, f, indent=2)
        print(f"Output written to {args.output}")
    else:
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
