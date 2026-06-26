#!/usr/bin/env python3
"""
sigui-security/evaluate.py — Sigui Protocol transaction security evaluator for OpenClaw

SECURITY POLICY:
  This script is FAIL-CLOSED by default. If the Sigui SDK or a real API endpoint
  is not available, the script exits with code 3 (error) and does NOT simulate results.

  Mock/demo mode must be explicitly enabled with the --demo flag and is NEVER used
  to authorize real transactions.

Usage:
    python evaluate.py --amount <usdc> --destination <address> [options]

Exit codes:
    0 = ALLOW / ALLOW_WITH_CAP  (only if --confirmed)
    1 = BLOCK
    2 = ESCALATE (deep analysis required)
    3 = Error / SDK unavailable / No confirmation

Options:
    --amount        Required. Transaction amount in USDC
    --destination   Required. Destination wallet or contract address
    --agent         Agent ID (default: OPENCLAW_AGENT_ID env var)
    --action        Action type: transfer|approve|swap|bridge|mint|contract_call
    --chain         Chain: arc|ethereum|starknet|aptos|solana (default: arc)
    --api-url       Sigui API URL (required unless --demo is set)
    --escalate      Auto-run deep analysis if verdict is ESCALATE
    --confirmed     Required to proceed after an ALLOW verdict
    --demo          Enable local mock mode (FOR TESTING ONLY, never for real funds)
    --json          Output raw JSON
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
from typing import Any, Dict, Optional

# ── Auto-install Sigui SDK if missing ─────────────────────────────────────────

def _auto_install_sdk() -> bool:
    """
    Attempt to install sigui-sdk automatically if not found.
    Returns True if SDK is available after the attempt.
    """
    try:
        from sigui import SiguiClient  # noqa: F401
        return True
    except ImportError:
        pass

    print("📦 sigui-sdk not found. Installing automatically...", file=sys.stderr)
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "sigui-sdk>=0.3.1", "--quiet"],
            timeout=120,
        )
        # Verify import works after install
        result = subprocess.run(
            [sys.executable, "-c", "from sigui import SiguiClient; print('ok')"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            print("✅ sigui-sdk installed successfully.", file=sys.stderr)
            return True
        else:
            print(f"❌ sigui-sdk installed but import failed: {result.stderr}", file=sys.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("❌ Auto-install timed out. Run: pip install sigui-sdk>=0.3.1", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Auto-install failed: {e}", file=sys.stderr)
        print("   Run manually: pip install sigui-sdk>=0.3.1", file=sys.stderr)
        return False


SIGUI_AVAILABLE = _auto_install_sdk()

# ── Optional: rich for formatted output ───────────────────────────────────────

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    console = Console(stderr=False)
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = None

# ── Import SDK after auto-install attempt ─────────────────────────────────────

if SIGUI_AVAILABLE:
    try:
        from sigui import SiguiClient
        from sigui.models import Verdict
    except ImportError:
        SIGUI_AVAILABLE = False


# ── Output helpers ─────────────────────────────────────────────────────────────

def _err(msg: str) -> None:
    if RICH_AVAILABLE:
        console.print(f"[bold red]❌[/bold red] {msg}")
    else:
        print(f"❌ {msg}", file=sys.stderr)


def _warn(msg: str) -> None:
    if RICH_AVAILABLE:
        console.print(f"[bold yellow]⚠️[/bold yellow]  {msg}")
    else:
        print(f"⚠️  {msg}", file=sys.stderr)


def _info(msg: str) -> None:
    if RICH_AVAILABLE:
        console.print(f"[cyan]{msg}[/cyan]")
    else:
        print(msg, file=sys.stderr)


# ── Core evaluation ────────────────────────────────────────────────────────────

async def _evaluate_real(args: argparse.Namespace) -> Dict[str, Any]:
    """Call the real Sigui API. Fails closed if unavailable."""
    api_url = args.api_url or os.environ.get("SIGUI_API_URL", "")

    if not api_url:
        _err(
            "No Sigui API URL configured.\n"
            "  Set SIGUI_API_URL environment variable or use --api-url.\n"
            "  For testing only, use --demo flag to run in local mock mode."
        )
        sys.exit(3)

    client = SiguiClient(api_url=api_url)
    _info(f"🔗 Connecting to Sigui node: {api_url}")

    result = await client.evaluate(
        agent_id=args.agent,
        amount=args.amount,
        destination=args.destination,
        action_type=args.action,
        chain=args.chain,
    )

    verdict = result.verdict.value
    data: Dict[str, Any] = {
        "verdict": verdict,
        "risk_score": result.risk_score,
        "confidence": result.confidence,
        "reason": result.reason,
        "action_hash": result.action_hash,
        "arc_tx_log": result.arc_tx_log,
        "arcwarden_mode": result.arcwarden_mode,
        "synthetic_score": result.synthetic_score,
        "chain": result.chain,
        "onchain_proof": result.onchain_proof,
        "demo": False,
    }

    # Deep escalation if requested
    if args.escalate and verdict == "ESCALATE":
        _warn("ESCALATE verdict received. Requesting deep analysis (may cost ~$0.003 USDC)...")
        try:
            esc = await client.escalate(
                agent_id=args.agent,
                amount=args.amount,
                destination=args.destination,
                action_type=args.action,
                original_verdict=result,
            )
            data["escalation"] = {
                "verdict": esc.verdict.value,
                "analysis": esc.analysis,
                "cap_amount_usdc": esc.cap_amount_usdc,
                "inference_engine": esc.inference_engine,
            }
            data["verdict"] = esc.verdict.value
        except Exception as e:
            _err(f"Deep escalation failed: {e}")

    return data


async def _evaluate_demo(args: argparse.Namespace) -> Dict[str, Any]:
    """
    Demo/mock mode — FOR TESTING ONLY.
    Always prints a prominent warning. Never use for real fund authorization.
    """
    import hashlib
    import random

    _warn("=" * 60)
    _warn("DEMO MODE — Results are SIMULATED heuristics.")
    _warn("DO NOT use these verdicts to authorize real transactions.")
    _warn("=" * 60)

    dest = args.destination.lower().strip()
    amount = args.amount

    # Simple heuristic
    _KNOWN_BAD = {"0x000000000000000000000000000000000000dead",
                  "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"}

    if dest in _KNOWN_BAD:
        risk = 0.97
    elif amount > 10_000:
        risk = min(0.85 + random.gauss(0, 0.03), 0.99)
    elif amount > 1_000:
        risk = min(0.45 + random.gauss(0, 0.05), 0.99)
    else:
        risk = max(0.05 + random.gauss(0, 0.03), 0.01)

    verdict = "ALLOW" if risk < 0.35 else ("ESCALATE" if risk < 0.80 else "BLOCK")
    h = hashlib.sha256(f"{dest}{amount}".encode()).hexdigest()

    return {
        "verdict": verdict,
        "risk_score": round(risk, 4),
        "confidence": round(0.60 + random.gauss(0, 0.05), 4),
        "reason": f"[DEMO] Simulated heuristic result (score={risk:.3f}). NOT oracle-backed.",
        "action_hash": f"0xDEMO_{h[:32]}",
        "arc_tx_log": "",
        "arcwarden_mode": "DEMO",
        "synthetic_score": int((1.0 - risk) * 1000),
        "chain": args.chain,
        "onchain_proof": None,
        "demo": True,
    }


# ── Display ────────────────────────────────────────────────────────────────────

def _pretty_print(r: Dict[str, Any], args: argparse.Namespace) -> None:
    verdict = r["verdict"]
    risk = r["risk_score"]
    score = r.get("synthetic_score", int((1 - risk) * 1000))
    demo_tag = "  ⚠️  DEMO MODE — NOT REAL" if r.get("demo") else ""

    if not RICH_AVAILABLE:
        print(f"\n--- SIGUI EVALUATION{demo_tag} ---")
        print(f"Verdict      : {verdict}")
        print(f"Risk Score   : {risk:.4f}")
        print(f"Safety Score : {score}/1000")
        print(f"Confidence   : {r.get('confidence', 0):.1%}")
        print(f"Reason       : {r['reason']}")
        if r.get("onchain_proof"):
            print(f"Proof        : {r['onchain_proof']}")
        if r.get("escalation"):
            e = r["escalation"]
            print(f"\n--- DEEP ANALYSIS ---")
            print(f"Deep Verdict : {e['verdict']}")
            print(f"Analysis     : {e['analysis']}")
        print("-" * 50)
        return

    color = "green" if verdict in ("ALLOW", "ALLOW_WITH_CAP") else "yellow" if verdict == "ESCALATE" else "red"
    icon  = {"ALLOW": "✅", "ALLOW_WITH_CAP": "⚠️", "ESCALATE": "🔍", "BLOCK": "🚫"}.get(verdict, "❓")

    t = Table(show_header=False, box=None, padding=(0, 2))
    t.add_column("Field", style="bold cyan", justify="right")
    t.add_column("Value")

    t.add_row("Verdict",      f"[{color} bold]{icon} {verdict}[/]")
    rc = "green" if risk < 0.35 else "yellow" if risk < 0.80 else "red"
    t.add_row("Risk Score",   f"[{rc}]{risk:.4f}[/] (0=safe, 1=critical)")
    t.add_row("Safety Score", f"{score}/1000")
    t.add_row("Confidence",   f"{r.get('confidence', 0):.1%}")
    t.add_row("Reason",       f"[italic]{r['reason']}[/]")
    t.add_row("Chain",        args.chain.upper())
    if r.get("onchain_proof"):
        t.add_row("Proof", f"[link={r['onchain_proof']}]{r['onchain_proof']}[/link]")
    if r.get("demo"):
        t.add_row("Mode", "[bold red]⚠️  DEMO (heuristic only, NOT oracle)[/bold red]")

    title = f"[bold]Sigui Evaluation — {args.amount} USDC → {args.destination[:12]}...[/bold]"
    console.print(Panel(t, title=title, border_style=color, expand=False))

    if r.get("escalation"):
        e = r["escalation"]
        ec = "green" if e["verdict"] in ("ALLOW", "ALLOW_WITH_CAP") else "red"
        et = Table(show_header=False, box=None, padding=(0, 2))
        et.add_column("Field", style="bold magenta", justify="right")
        et.add_column("Value")
        et.add_row("Verdict",      f"[{ec} bold]{e['verdict']}[/]")
        et.add_row("Spending Cap", f"${e['cap_amount_usdc']:.2f} USDC")
        et.add_row("Engine",       e["inference_engine"])
        et.add_row("Analysis",     e["analysis"])
        console.print(Panel(et, title="[bold magenta]🔍 Deep Analysis[/bold magenta]",
                            border_style="magenta", expand=False))


# ── Main ───────────────────────────────────────────────────────────────────────

async def _run(args: argparse.Namespace) -> int:
    # 1. SDK must be available (auto-installed above)
    if not SIGUI_AVAILABLE:
        _err("sigui-sdk is unavailable and could not be installed automatically.")
        _err("Please install manually: pip install sigui-sdk>=0.3.1")
        return 3

    # 2. Evaluate
    try:
        if args.demo:
            result = await _evaluate_demo(args)
        else:
            result = await _evaluate_real(args)
    except SystemExit:
        raise
    except Exception as exc:
        _err(f"Evaluation failed: {exc}")
        return 3

    # 3. Output
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        _pretty_print(result, args)

    verdict = result["verdict"]

    # 4. ALLOW requires explicit --confirmed flag
    if verdict in ("ALLOW", "ALLOW_WITH_CAP") and not args.confirmed:
        _warn(
            "Transaction received an ALLOW verdict.\n"
            "  ⚠️  USER CONFIRMATION REQUIRED before proceeding.\n"
            "  Re-run with --confirmed only after the user explicitly approves."
        )
        if not args.json:
            print("\n  Please confirm with the user: 'Do you want to proceed with this transaction?'")
        return 3  # Block until confirmed

    # 5. Exit codes
    if verdict == "BLOCK":
        return 1
    if verdict == "ESCALATE":
        return 2
    return 0  # ALLOW + confirmed


def main() -> None:
    p = argparse.ArgumentParser(
        description="Sigui Protocol — Blockchain AI Security Oracle for OpenClaw agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--amount",      required=True, type=float,
                   help="Transaction amount in USDC equivalent")
    p.add_argument("--destination", required=True,
                   help="Destination wallet, contract, or ENS/domain address")
    p.add_argument("--agent",       default=os.environ.get("OPENCLAW_AGENT_ID", "openclaw"),
                   help="Calling agent ID (default: OPENCLAW_AGENT_ID env var)")
    p.add_argument("--action",      default="transfer",
                   choices=["transfer", "approve", "swap", "bridge", "mint", "contract_call"],
                   help="Transaction action type (default: transfer)")
    p.add_argument("--chain",       default=os.environ.get("SIGUI_CHAIN", "arc"),
                   choices=["arc", "ethereum", "starknet", "aptos", "solana"],
                   help="Target blockchain (default: arc or SIGUI_CHAIN env var)")
    p.add_argument("--api-url",     default=None,
                   help="Sigui API URL (or set SIGUI_API_URL env var)")
    p.add_argument("--escalate",    action="store_true",
                   help="Auto-run deep analysis if verdict is ESCALATE")
    p.add_argument("--confirmed",   action="store_true",
                   help="Indicate user has explicitly confirmed an ALLOW verdict")
    p.add_argument("--demo",        action="store_true",
                   help="⚠️  DEMO/TEST MODE: heuristic mock only. Never use for real funds.")
    p.add_argument("--json",        action="store_true",
                   help="Output raw JSON")

    args = p.parse_args()
    sys.exit(asyncio.run(_run(args)))


if __name__ == "__main__":
    main()
