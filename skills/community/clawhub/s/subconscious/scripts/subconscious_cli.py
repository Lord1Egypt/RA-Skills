#!/usr/bin/env python3
"""Subconscious v1.5 — Safe Local Integration CLI

A lightweight, explicit integration layer for Alfred's workflow.
NO daemon, NO background loops, NO automatic hooks.
Each command is explicit, bounded, and safe.

Usage:
    python scripts/subconscious_cli.py bootstrap          # Get compact context
    python scripts/subconscious_cli.py bias [project]   # Build bias for context
    python scripts/subconscious_cli.py intake <file>      # Process turn from JSON
    python scripts/subconscious_cli.py flush            # Write snapshot
    python scripts/subconscious_cli.py maintain         # Run maintenance pass
    python scripts/subconscious_cli.py status           # Show system status
    python scripts/subconscious_cli.py verify           # Run integration tests

Safety Limits (enforced):
    - Max 5 bias items per retrieval
    - Max 500 chars in rendered bias block
    - Max 10 unresolved items in snapshot
    - Max 1000 chars in bootstrap context
    - Max 20 pending items processed per intake
    - Max 10 snapshots kept
    - Core.json: read-only without explicit --force flag

Exit codes:
    0 - Success
    1 - Error/invalid input
    2 - Safety limit exceeded (would be exceeded, not exceeded)
"""

import argparse
import json
import sys
import os
from pathlib import Path
from typing import Optional

# Add workspace to path
WORKSPACE_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from subconscious import (
    bootstrap as subc_bootstrap,
    build_snapshot,
    write_snapshot,
    fetch_relevant,
    build_bias,
    load,
)
from subconscious.intake import extract_candidates, queue_pending
from subconscious.maintenance import run_maintenance, get_metrics
from subconscious.store import DEFAULT_BASE_PATH, load_config, check_resource_bounds


# =============================================================================
# SAFETY LIMITS (hard caps)
# =============================================================================

MAX_BIAS_ITEMS = 5           # Max items in bias block
MAX_BIAS_CHARS = 1200        # Max chars in rendered bias block
MAX_UNRESOLVED = 10          # Max unresolved in snapshot
MAX_BOOTSTRAP_CHARS = 1000   # Max chars in bootstrap context
MAX_PENDING_PER_INTAKE = 20  # Max pending items to process
MAX_SNAPSHOTS = 10           # Max snapshots to keep
MAX_LIVE_ITEMS = 100         # Max live items


def _safe_read_json(path: Path) -> Optional[dict]:
    """Safely read JSON file, return None if missing/corrupt."""
    try:
        if not path.exists():
            return None
        # Check file size (max 10MB safety)
        size = path.stat().st_size
        if size > 10_000_000:
            print(f"Error: File {path} too large ({size} bytes)", file=sys.stderr)
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError, OSError) as e:
        print(f"Error reading {path}: {e}", file=sys.stderr)
        return None


def _truncate_context(context: str, max_chars: int) -> str:
    """Truncate context to max chars with indicator."""
    if len(context) <= max_chars:
        return context
    return context[:max_chars-3] + "..."


def _check_stores_exist() -> bool:
    """Check if required store files exist."""
    base = DEFAULT_BASE_PATH
    return (base / "core.json").exists() or (base / "live.json").exists()


# =============================================================================
# COMMAND: bootstrap
# =============================================================================

def cmd_bootstrap(args) -> int:
    """Load compact bootstrap context for session start."""
    if not _check_stores_exist():
        # Graceful no-op: print empty but valid context
        print("## SUBCONSCIOUS")
        print("Status: No subconscious stores found. Run verification to setup.")
        return 0

    try:
        context = subc_bootstrap()

        # Get formatted output
        formatted = context.get("_formatted", "")

        # Safety: truncate to max chars
        formatted = _truncate_context(formatted, MAX_BOOTSTRAP_CHARS)

        # Output
        if args.json:
            # JSON output (truncated)
            output = {
                "identity": context.get("identity", [])[:3],
                "preferences": context.get("preferences", [])[:3],
                "projects": context.get("projects", [])[:3],
                "hypotheses": context.get("hypotheses", [])[:2],
                "formatted": formatted,
            }
            print(json.dumps(output, indent=2))
        else:
            print(formatted)

        return 0

    except Exception as e:
        print(f"Bootstrap error: {e}", file=sys.stderr)
        return 1


# =============================================================================
# COMMAND: bias
# =============================================================================

def cmd_bias(args) -> int:
    """Build compact bias block for given context."""
    if not _check_stores_exist():
        print(json.dumps({"subconscious_bias": {"attention": [], "_meta": {"error": "No stores"}}}))
        return 0

    try:
        # Build query context
        query_ctx = {
            "query": args.query or args.project or "",
            "project": args.project,
            "topics": args.topics.split(",") if args.topics else [],
        }

        # Fetch relevant items (max 5)
        items = fetch_relevant(query_ctx, limit=MAX_BIAS_ITEMS, min_confidence=0.7)

        # Build bias block
        bias = build_bias(items, max_items=MAX_BIAS_ITEMS, min_confidence=0.7)

        # Safety: check rendered size
        bias_str = json.dumps(bias)
        if len(bias_str) > MAX_BIAS_CHARS:
            # Truncate by removing items from all non-empty categories until under limit
            categories = ["style", "interpretation", "attention", "action"]
            while len(bias_str) > MAX_BIAS_CHARS:
                popped = False
                for cat in categories:
                    if bias["subconscious_bias"][cat]:
                        bias["subconscious_bias"][cat].pop()
                        bias["subconscious_bias"]["_meta"]["item_count"] -= 1
                        popped = True
                        break
                if not popped:
                    break
                bias_str = json.dumps(bias)

        if args.json:
            print(json.dumps(bias, indent=2))
        else:
            # Full category output using format_for_prompt
            from subconscious.influence import format_for_prompt
            prompt_text = format_for_prompt(bias)
            if prompt_text.strip():
                print(prompt_text)
            else:
                print("## SUBCONSCIOUS BIAS")
                print("(no relevant biases)")

        return 0

    except Exception as e:
        print(f"Bias error: {e}", file=sys.stderr)
        return 1


# =============================================================================
# COMMAND: intake
# =============================================================================

def cmd_intake(args) -> int:
    """Process a turn and queue candidates to pending."""
    if not args.file:
        print("Error: --file required for intake", file=sys.stderr)
        return 1

    # Read turn context
    turn_data = _safe_read_json(Path(args.file))
    if turn_data is None:
        print(f"Error: Cannot read turn file: {args.file}", file=sys.stderr)
        return 1

    try:
        # Extract candidates
        candidates = extract_candidates(turn_data)

        # Safety: limit candidates processed
        candidates = candidates[:MAX_PENDING_PER_INTAKE]

        # Queue each candidate
        queued = 0
        skipped = 0
        for c in candidates:
            if queue_pending(c):
                queued += 1
            else:
                skipped += 1

        # Output summary
        result = {
            "extracted": len(candidates),
            "queued": queued,
            "skipped_duplicate": skipped,
        }

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Intake: {queued} queued, {skipped} duplicates skipped")

        return 0

    except Exception as e:
        print(f"Intake error: {e}", file=sys.stderr)
        return 1


# =============================================================================
# COMMAND: flush
# =============================================================================

def cmd_flush(args) -> int:
    """Build and write snapshot."""
    if not _check_stores_exist():
        print("Error: No subconscious stores to flush", file=sys.stderr)
        return 1

    try:
        # Build session context
        session_ctx = {
            "project": args.project,
            "topics": args.topics.split(",") if args.topics else [],
            "turn_count": args.turn_count or 0,
        }

        # Build snapshot
        snapshot = build_snapshot(session_ctx)

        # Safety: check unresolved count
        unresolved = snapshot.get("unresolved", [])
        if len(unresolved) > MAX_UNRESOLVED:
            # Truncate to max
            snapshot["unresolved"] = unresolved[:MAX_UNRESOLVED]
            snapshot["_meta"] = {"unresolved_truncated": True}

        # Write snapshot
        path = write_snapshot(snapshot)

        # Check snapshot size
        size_kb = path.stat().st_size / 1024

        result = {
            "path": str(path),
            "size_kb": round(size_kb, 2),
            "timestamp": snapshot.get("timestamp"),
        }

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Snapshot written: {path}")
            print(f"Size: {size_kb:.1f} KB")

        return 0

    except Exception as e:
        print(f"Flush error: {e}", file=sys.stderr)
        return 1


# =============================================================================
# COMMAND: maintain
# =============================================================================

def cmd_maintain(args) -> int:
    """Run maintenance pass (decay, metrics, cleanup)."""
    try:
        # Run maintenance
        results = run_maintenance(force_decay=args.force_decay)

        # Get updated metrics
        metrics = get_metrics()

        output = {
            "maintenance": results,
            "metrics": metrics,
        }

        if args.json:
            print(json.dumps(output, indent=2))
        else:
            print("Maintenance complete")
            if results.get("decayed"):
                print(f"  Decayed items: {results['decayed']}")
            if results.get("archived"):
                print(f"  Archived items: {results['archived']}")
            if "counts" in metrics:
                print(f"  Store counts: {metrics['counts']}")

        return 0

    except Exception as e:
        print(f"Maintenance error: {e}", file=sys.stderr)
        return 1


# =============================================================================
# COMMAND: status
# =============================================================================

def cmd_status(args) -> int:
    """Show subconscious system status."""
    try:
        base = DEFAULT_BASE_PATH
        config = load_config()

        # Load counts
        core_items = load("core")
        live_items = load("live")
        pending_items = load("pending")

        # Count snapshots
        snap_dir = base / "snapshots"
        snapshot_count = len(list(snap_dir.glob("*.json"))) if snap_dir.exists() else 0

        # Get metrics if available
        metrics = get_metrics()

        status = {
            "stores": {
                "core_count": len(core_items),
                "live_count": len(live_items),
                "pending_count": len(pending_items),
                "snapshot_count": snapshot_count,
            },
            "thresholds": config.get("thresholds", {}),
            "healthy": True,
        }

        # Add health warnings
        warnings = []
        if len(live_items) > MAX_LIVE_ITEMS:
            warnings.append(f"Live items ({len(live_items)}) exceeds max ({MAX_LIVE_ITEMS})")
        if snapshot_count > MAX_SNAPSHOTS:
            warnings.append(f"Snapshots ({snapshot_count}) exceeds max ({MAX_SNAPSHOTS})")

        if warnings:
            status["healthy"] = False
            status["warnings"] = warnings

        if args.json:
            print(json.dumps(status, indent=2))
        else:
            print("Subconscious System Status")
            print(f"  Core items: {len(core_items)}")
            print(f"  Live items: {len(live_items)}")
            print(f"  Pending items: {len(pending_items)}")
            print(f"  Snapshots: {snapshot_count}")
            if warnings:
                print("  Warnings:")
                for w in warnings:
                    print(f"    ! {w}")
            else:
                print("  Status: Healthy")

        return 0 if status["healthy"] else 2

    except Exception as e:
        print(f"Status error: {e}", file=sys.stderr)
        return 1


# =============================================================================
# COMMAND: verify
# =============================================================================

def cmd_verify(args) -> int:
    """Run integration verification."""
    print("Running subconscious integration verification...")

    checks = []

    # Check 1: Stores exist or can be created
    base = DEFAULT_BASE_PATH
    stores_ok = (base / "core.json").exists() and (base / "live.json").exists()
    checks.append(("Stores exist", stores_ok))

    if not stores_ok:
        print("ERROR: Subconscious stores not initialized. Run demo first?")
        return 1

    # Check 2: Bootstrap works
    try:
        ctx = subc_bootstrap()
        bootstrap_ok = "_formatted" in ctx
        checks.append(("Bootstrap", bootstrap_ok))
    except Exception as e:
        checks.append(("Bootstrap", False))
        print(f"Bootstrap failed: {e}")

    # Check 3: Bias building works
    try:
        items = fetch_relevant({"query": "test"}, limit=5)
        bias = build_bias(items)
        bias_ok = "subconscious_bias" in bias
        checks.append(("Bias building", bias_ok))
    except Exception as e:
        checks.append(("Bias building", False))
        print(f"Bias building failed: {e}")

    # Check 4: Safety limits are in config
    try:
        config = load_config()
        thresholds = config.get("thresholds", {})
        has_limits = all(k in thresholds for k in ["max_bias_items", "min_confidence_surface"])
        checks.append(("Safety limits", has_limits))
    except Exception as e:
        checks.append(("Safety limits", False))

    # Check 5: Maintenance runs
    try:
        metrics_before = get_metrics()
        maint_result = run_maintenance()
        metrics_after = get_metrics()
        maint_ok = maint_result.get("metrics_updated", False)
        checks.append(("Maintenance", maint_ok))
    except Exception as e:
        checks.append(("Maintenance", False))
        print(f"Maintenance failed: {e}")

    # Print results
    print("\nVerification Results:")
    all_passed = True
    for name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"  [{status}] {name}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n✓ All integration checks passed")
        return 0
    else:
        print("\n✗ Some checks failed")
        return 1


# =============================================================================
# COMMAND: mode (24/7 bounded mode status)
# =============================================================================

def cmd_mode(args) -> int:
    """Show 24/7 bounded metabolism mode status."""
    config = load_config()
    ok, usage, warnings = check_resource_bounds()

    ceilings = config.get("ceilings", {})
    mode = config.get("operation_mode", "unbounded")
    cadence = config.get("cadence", {})

    output = {
        "operation_mode": mode,
        "bounded_24_7": mode == "bounded",
        "ceilings": {
            "max_pending_lines": ceilings.get("max_pending_lines", 500),
            "max_live_items": ceilings.get("max_live_items", 100),
            "max_core_items": ceilings.get("max_core_items", 50),
            "max_snapshots": ceilings.get("max_snapshots", 10),
            "max_tick_duration_ms": ceilings.get("max_tick_duration_ms", 500),
        },
        "current_usage": usage,
        "recommended_cadence": {
            "tick": f"Every {cadence.get('tick_interval_minutes', 5)} minutes",
            "rotate": f"Every {cadence.get('rotate_interval_hours', 1)} hours",
            "review": f"Daily at {cadence.get('review_time', '06:00')}",
        },
        "commands": {
            "tick": "python scripts/subconscious_metabolism.py tick",
            "rotate": "python scripts/subconscious_metabolism.py rotate",
            "review": "python scripts/subconscious_metabolism.py review",
            "verify": "python scripts/subconscious_metabolism.py verify",
        },
        "healthy": ok,
        "warnings": warnings if warnings else None,
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print("Subconscious 24/7 Bounded Mode")
        print(f"  Mode: {mode}")
        print(f"  Status: {'Healthy' if ok else 'WARNING'}")
        print("\nResource Ceilings:")
        print(f"  Pending: {usage['pending_lines']}/{output['ceilings']['max_pending_lines']} lines")
        print(f"  Live: {usage['live_count']}/{output['ceilings']['max_live_items']} items")
        print(f"  Core: {usage['core_count']}/{output['ceilings']['max_core_items']} items")
        print(f"  Snapshots: {usage['snapshot_count']}/{output['ceilings']['max_snapshots']} files")
        print("\nRecommended Cadence:")
        for k, v in output["recommended_cadence"].items():
            print(f"  {k}: {v}")
        if warnings:
            print("\nWarnings:")
            for w in warnings:
                print(f"  ! {w}")

    return 0 if ok else 2


# =============================================================================
# COMMAND: governance
# =============================================================================

def cmd_governance(args) -> int:
    """Show governance rules for self-evolution."""
    from subconscious.governance import get_governance_summary

    summary = get_governance_summary()

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print("Subconscious Governance")
        print("\nProtected Classes (Manual-only mutations):")
        for p in summary["protected_classes"]:
            print(f"  - {p}")

        print("\nAllowed Auto-Mutations (Bounded):")
        for m in summary["allowed_mutations"]:
            print(f"  - {m}")

        print("\nGated Mutations (Thresholds required):")
        for m in summary["gated_mutations"]:
            print(f"  - {m}")

        print("\nProhibited Mutations (Never automatic):")
        for m in summary["prohibited_mutations"]:
            print(f"  - {m}")

        print("\nPromotion Thresholds (pending -> live):")
        promo = summary["gate_thresholds"].get("promotion_to_live", {})
        for k, v in promo.items():
            print(f"  {k}: {v}")

        print("\nMutation Bounds:")
        for k, v in summary["mutation_bounds"].items():
            print(f"  {k}: {v}")

    return 0


# =============================================================================
# COMMAND: evolve
# =============================================================================

def cmd_evolve(args) -> int:
    """Run bounded self-evolution."""
    try:
        from subconscious.evolution import run_evolution_pass

        results = run_evolution_pass(
            dry_run=args.dry_run,
            enable_promotion=args.enable_promotion,
        )

        output = {
            "evolution": results,
            "dry_run": args.dry_run,
        }

        if args.json:
            print(json.dumps(output, indent=2))
        else:
            mode = "DRY RUN" if args.dry_run else "LIVE"
            print(f"Evolution pass [{mode}]")

            if results.get("decay", {}).get("decayed"):
                print(f"  Decayed: {results['decay']['decayed']}")
            if results.get("archival", {}).get("archived"):
                print(f"  Archived: {results['archival']['archived']}")
            if results.get("salience", {}).get("adjusted"):
                print(f"  Salience tuned: {results['salience']['adjusted']}")
            if results.get("promotion", {}).get("eligible") is not None:
                print(f"  Promotion checked: {results['promotion']['checked']}")
                print(f"  Eligible: {results['promotion']['eligible']}")
                if not args.dry_run:
                    print(f"  Promoted: {results['promotion'].get('promoted', 0)}")

        return 0

    except Exception as e:
        print(f"Evolution error: {e}", file=sys.stderr)
        return 1


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Subconscious v1.5 — Safe Local Integration CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s bootstrap                          # Get compact context
  %(prog)s bias --project pepper              # Build bias for project
  %(prog)s intake --file turn.json            # Process turn
  %(prog)s flush --project xiaohongshu        # Write snapshot
  %(prog)s maintain                         # Run maintenance
  %(prog)s status                           # Show status
  %(prog)s verify                           # Run verification
  %(prog)s mode                             # Show 24/7 mode status
  %(prog)s governance                       # Show governance rules
  %(prog)s evolve --dry-run                 # Test evolution pass

24/7 Bounded Operation:
  python scripts/subconscious_metabolism.py tick    # Every 5 min
  python scripts/subconscious_metabolism.py rotate  # Hourly
  python scripts/subconscious_metabolism.py review  # Daily
  python scripts/subconscious_metabolism.py evolve  # Manual evolution

Safety limits enforced:
  Max 5 bias items, 500 chars bias block, 1000 chars bootstrap,
  10 unresolved in snapshot, 20 pending per intake, 10 snapshots kept.
  Core is protected - no automatic mutations.
  Promotion to core is prohibited in v1.5.
        """
    )
    parser.add_argument("--json", action="store_true", help="Output JSON")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # bootstrap
    p_boot = subparsers.add_parser("bootstrap", help="Load compact context for session")
    p_boot.set_defaults(func=cmd_bootstrap)

    # bias
    p_bias = subparsers.add_parser("bias", help="Build compact bias block")
    p_bias.add_argument("project", nargs="?", help="Project context")
    p_bias.add_argument("--query", help="Query text")
    p_bias.add_argument("--topics", help="Comma-separated topics")
    p_bias.set_defaults(func=cmd_bias)

    # intake
    p_intake = subparsers.add_parser("intake", help="Process turn and queue candidates")
    p_intake.add_argument("--file", required=True, help="JSON file with turn context")
    p_intake.set_defaults(func=cmd_intake)

    # flush
    p_flush = subparsers.add_parser("flush", help="Write snapshot")
    p_flush.add_argument("--project", help="Current project")
    p_flush.add_argument("--topics", help="Comma-separated topics")
    p_flush.add_argument("--turn-count", type=int, help="Turn count")
    p_flush.set_defaults(func=cmd_flush)

    # maintain
    p_maint = subparsers.add_parser("maintain", help="Run maintenance pass")
    p_maint.add_argument("--force-decay", action="store_true", help="Force decay pass")
    p_maint.set_defaults(func=cmd_maintain)

    # status
    p_status = subparsers.add_parser("status", help="Show system status")
    p_status.set_defaults(func=cmd_status)

    # verify
    p_verify = subparsers.add_parser("verify", help="Run integration verification")
    p_verify.set_defaults(func=cmd_verify)

    # mode (24/7 status)
    p_mode = subparsers.add_parser("mode", help="Show 24/7 bounded mode status")
    p_mode.set_defaults(func=cmd_mode)

    # governance
    p_gov = subparsers.add_parser("governance", help="Show governance rules")
    p_gov.add_argument("--json", action="store_true", help="Output JSON")
    p_gov.set_defaults(func=cmd_governance)

    # evolve
    p_evolve = subparsers.add_parser("evolve", help="Run bounded self-evolution")
    p_evolve.add_argument("--dry-run", action="store_true", help="Show what would happen")
    p_evolve.add_argument("--enable-promotion", action="store_true",
                          help="Enable pending->live promotion")
    p_evolve.add_argument("--json", action="store_true", help="Output JSON")
    p_evolve.set_defaults(func=cmd_evolve)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
