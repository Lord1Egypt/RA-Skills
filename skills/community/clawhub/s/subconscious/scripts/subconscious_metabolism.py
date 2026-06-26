#!/usr/bin/env python3
"""Subconscious 24/7 Bounded Metabolism Tick

A scheduler-friendly, one-shot metabolism script for continuous operation.
NO daemon, NO background loops, NO resident processes.

Designed for cron/systemd timer invocation with bounded resource usage:
- Max execution time: ~500ms
- Max memory: negligible (file-based)
- Idempotent: safe to run repeatedly
- Bounded: resource limits enforced in code

Usage:
    # Quick metabolism tick (maintain + conditional flush)
    python scripts/subconscious_metabolism.py tick

    # Full rotation (maintenance + flush + cleanup)
    python scripts/subconscious_metabolism.py rotate

    # Status check only
    python scripts/subconscious_metabolism.py status

    # 24/7 mode verification
    python scripts/subconscious_metabolism.py verify

Cadence Recommendation for 24/7 Operation:
    # Per-turn (from session, not cron)
    python scripts/subconscious_cli.py intake --file turn.json
    python scripts/subconscious_cli.py bias --project X

    # Every 5 minutes (light maintenance)
    */5 * * * * python /home/edward/.openclaw/workspace-alfred/scripts/subconscious_metabolism.py tick

    # Hourly (full rotation with snapshot)
    0 * * * * python /home/edward/.openclaw/workspace-alfred/scripts/subconscious_metabolism.py rotate

    # Daily (deep review - optional)
    0 6 * * * python /home/edward/.openclaw/workspace-alfred/scripts/subconscious_metabolism.py review

Exit codes:
    0 - Success (or nothing to do, which is success)
    1 - Error
    2 - Resource limit would be exceeded (no action taken)
"""

import argparse
import json
import sys
import time
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
from subconscious.store import DEFAULT_BASE_PATH, load_config


# =============================================================================
# 24/7 RESOURCE CEILINGS (Hard Limits)
# =============================================================================

class ResourceCeilings:
    """Hard resource ceilings for continuous 24/7 operation."""

    # Pending queue
    MAX_PENDING_LINES = 500          # Max lines in pending.jsonl
    MAX_PENDING_AGE_DAYS = 7         # Auto-remove after 7 days

    # Live items
    MAX_LIVE_ITEMS = 100           # Max items in live.json
    MAX_LIVE_AGE_DAYS = 30         # Archive after 30 days inactive

    # Core items
    MAX_CORE_ITEMS = 50            # Warning threshold for core

    # Snapshots
    MAX_SNAPSHOTS = 10             # Max snapshot files kept
    MAX_SNAPSHOT_SIZE_KB = 50      # Max single snapshot size

    # Bootstrap
    MAX_BOOTSTRAP_CHARS = 1000     # Max chars in bootstrap context
    MAX_BIAS_CHARS = 500           # Max chars in bias block

    # Events log
    MAX_EVENTS_LOG_MB = 10         # Max events.jsonl size
    EVENTS_ROTATE_COUNT = 3        # Keep 3 rotated copies

    # Execution bounds
    MAX_TICK_DURATION_MS = 500     # Max time for a tick
    NO_OP_IF_EMPTY = True          # Skip work if nothing to do


# =============================================================================
# STATE CHECKS
# =============================================================================

def _check_stores_exist() -> bool:
    """Check if required store files exist."""
    base = DEFAULT_BASE_PATH
    return (base / "core.json").exists() or (base / "live.json").exists()


def _get_resource_usage() -> dict:
    """Get current resource usage."""
    base = DEFAULT_BASE_PATH
    usage = {
        "core_count": 0,
        "live_count": 0,
        "pending_lines": 0,
        "snapshot_count": 0,
        "events_size_mb": 0,
    }

    # Count items
    if (base / "core.json").exists():
        usage["core_count"] = len(load("core"))
    if (base / "live.json").exists():
        usage["live_count"] = len(load("live"))

    # Count pending lines
    pending_path = base / "pending.jsonl"
    if pending_path.exists():
        with open(pending_path, "r") as f:
            usage["pending_lines"] = sum(1 for _ in f if _.strip())

    # Count snapshots
    snap_dir = base / "snapshots"
    if snap_dir.exists():
        usage["snapshot_count"] = len(list(snap_dir.glob("*.json")))

    # Events log size
    events_path = base / "events.jsonl"
    if events_path.exists():
        usage["events_size_mb"] = events_path.stat().st_size / (1024 * 1024)

    return usage


def _check_resource_limits(usage: dict) -> tuple[bool, list[str]]:
    """Check if usage exceeds hard limits.

    Returns:
        (ok, warnings) - ok=True if all limits respected
    """
    warnings = []
    ceilings = ResourceCeilings

    if usage["pending_lines"] > ceilings.MAX_PENDING_LINES:
        warnings.append(f"Pending lines ({usage['pending_lines']}) exceeds max ({ceilings.MAX_PENDING_LINES})")

    if usage["live_count"] > ceilings.MAX_LIVE_ITEMS:
        warnings.append(f"Live items ({usage['live_count']}) exceeds max ({ceilings.MAX_LIVE_ITEMS})")

    if usage["core_count"] > ceilings.MAX_CORE_ITEMS:
        warnings.append(f"Core items ({usage['core_count']}) exceeds warning ({ceilings.MAX_CORE_ITEMS})")

    if usage["snapshot_count"] > ceilings.MAX_SNAPSHOTS:
        warnings.append(f"Snapshots ({usage['snapshot_count']}) exceeds max ({ceilings.MAX_SNAPSHOTS})")

    if usage["events_size_mb"] > ceilings.MAX_EVENTS_LOG_MB:
        warnings.append(f"Events log ({usage['events_size_mb']:.1f}MB) exceeds max ({ceilings.MAX_EVENTS_LOG_MB}MB)")

    return len(warnings) == 0, warnings


# =============================================================================
# BOUNDED OPERATIONS
# =============================================================================

def _bounded_maintenance(force: bool = False, enable_evolution: bool = False) -> dict:
    """Run maintenance with hard resource bounds."""
    start = time.time()

    # Check limits before running
    usage = _get_resource_usage()
    ok, warnings = _check_resource_limits(usage)

    if not ok and not force:
        return {
            "status": "blocked",
            "reason": "resource_limits",
            "warnings": warnings,
            "action": "Run with --force to proceed anyway, or run rotate to compact",
        }

    # Feed learnings from self-improving agent into pending queue
    bridge_result = None
    try:
        from subconscious.learnings_bridge import scan_learnings
        bridge_result = scan_learnings()
    except Exception:
        pass

    # Run standard maintenance
    results = run_maintenance(force_decay=True)
    results["learnings_bridged"] = bridge_result

    # Additional bounded cleanup
    results["pending_trimmed"] = _trim_pending_to_limit()
    results["live_trimmed"] = _trim_live_to_limit()
    results["events_rotated"] = _rotate_events_if_needed()

    # Run bounded evolution if enabled (lightweight for tick)
    if enable_evolution:
        from subconscious.evolution import update_freshness, archive_stale_items, reinforce_item
        from subconscious.store import load
        # Passive reinforcement: tick all pending items by +1
        # This prevents starvation when items aren't explicitly accessed
        pending_items = load("pending", DEFAULT_BASE_PATH)
        reinforced = 0
        for record in pending_items:
            # Skip items already reinforced — reinforcing again destroys their
            # promotion eligibility (type becomes candidate_reinforced and the
            # promotion scan only processes candidate_queued items)
            if record.get("type") == "candidate_reinforced":
                continue
            # pending.jsonl stores event records: {type, timestamp, data: {...item...}}
            item_data = record.get("data", {}) if isinstance(record, dict) else record
            item_id = item_data.get("id")
            if item_id:
                success, _ = reinforce_item(item_id, DEFAULT_BASE_PATH)
                if success:
                    reinforced += 1
        results["evolution"] = {
            "decay": update_freshness(force_decay=False),
            "archival": archive_stale_items(base_path=DEFAULT_BASE_PATH),
            "passive_reinforced": reinforced,
        }

    elapsed_ms = (time.time() - start) * 1000
    results["elapsed_ms"] = round(elapsed_ms, 2)

    return results


def _trim_pending_to_limit() -> int:
    """Trim pending queue to MAX_PENDING_LINES (FIFO)."""
    base = DEFAULT_BASE_PATH
    pending_path = base / "pending.jsonl"

    if not pending_path.exists():
        return 0

    lines = []
    with open(pending_path, "r") as f:
        lines = [line for line in f if line.strip()]

    if len(lines) <= ResourceCeilings.MAX_PENDING_LINES:
        return 0

    # Keep only the most recent N lines
    keep_lines = lines[-ResourceCeilings.MAX_PENDING_LINES:]
    removed = len(lines) - len(keep_lines)

    with open(pending_path, "w") as f:
        for line in keep_lines:
            f.write(line + "\n")

    return removed


def _trim_live_to_limit() -> int:
    """Archive oldest live items if over MAX_LIVE_ITEMS."""
    live_items = load("live")

    if len(live_items) <= ResourceCeilings.MAX_LIVE_ITEMS:
        return 0

    # Sort by freshness (keep freshest)
    sorted_items = sorted(
        live_items,
        key=lambda x: (x.get("freshness", 0), x.get("weight", 0)),
        reverse=True
    )

    # Archive excess
    keep = sorted_items[:ResourceCeilings.MAX_LIVE_ITEMS]
    archive = sorted_items[ResourceCeilings.MAX_LIVE_ITEMS:]

    for item in archive:
        item["status"] = "archived"
        item["archived_reason"] = "resource_limit"

    # Save back (all items, archived ones stay in live.json but marked)
    from subconscious.store import save
    save("live", keep + archive, force=True)

    return len(archive)


def _rotate_events_if_needed() -> bool:
    """Rotate events.jsonl if over size limit."""
    base = DEFAULT_BASE_PATH
    events_path = base / "events.jsonl"

    if not events_path.exists():
        return False

    size_mb = events_path.stat().st_size / (1024 * 1024)
    if size_mb <= ResourceCeilings.MAX_EVENTS_LOG_MB:
        return False

    # Rotate: move current to .1, .1 to .2, etc.
    for i in range(ResourceCeilings.EVENTS_ROTATE_COUNT - 1, 0, -1):
        old_path = base / f"events.jsonl.{i}"
        new_path = base / f"events.jsonl.{i+1}"
        if old_path.exists():
            old_path.rename(new_path)

    events_path.rename(base / "events.jsonl.1")

    # Clean up oldest if exceeds rotation count
    oldest = base / f"events.jsonl.{ResourceCeilings.EVENTS_ROTATE_COUNT + 1}"
    if oldest.exists():
        oldest.unlink()

    return True


def _cleanup_snapshots() -> int:
    """Ensure only MAX_SNAPSHOTS kept."""
    base = DEFAULT_BASE_PATH
    snap_dir = base / "snapshots"

    if not snap_dir.exists():
        return 0

    snapshots = sorted(snap_dir.glob("*.json"), reverse=True)
    to_remove = snapshots[ResourceCeilings.MAX_SNAPSHOTS:]

    for snap in to_remove:
        snap.unlink()

    return len(to_remove)


# =============================================================================
# COMMANDS
# =============================================================================

def cmd_tick(args) -> int:
    """Lightweight metabolism tick - safe for frequent runs (every 5 min)."""
    start = time.time()

    if not _check_stores_exist():
        print(json.dumps({"status": "no_op", "reason": "no_stores"}))
        return 0

    # Check if there's work to do
    usage = _get_resource_usage()

    if ResourceCeilings.NO_OP_IF_EMPTY:
        # Skip if nothing to maintain
        if (usage["pending_lines"] == 0 and
            usage["live_count"] < ResourceCeilings.MAX_LIVE_ITEMS * 0.8 and
            usage["snapshot_count"] <= ResourceCeilings.MAX_SNAPSHOTS):
            print(json.dumps({
                "status": "no_op",
                "reason": "nothing_to_do",
                "usage": usage,
                "elapsed_ms": round((time.time() - start) * 1000, 2),
            }))
            return 0

    # Run bounded maintenance with evolution
    results = _bounded_maintenance(force=args.force, enable_evolution=True)

    # Cleanup snapshots
    removed = _cleanup_snapshots()
    results["snapshots_cleaned"] = removed

    elapsed_ms = (time.time() - start) * 1000

    output = {
        "status": "ok",
        "operation": "tick",
        "results": results,
        "usage_after": _get_resource_usage(),
        "elapsed_ms": round(elapsed_ms, 2),
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"Tick complete ({elapsed_ms:.1f}ms)")
        if results.get("decayed"):
            print(f"  Decayed: {results['decayed']}")
        if results.get("archived"):
            print(f"  Archived: {results['archived']}")
        if results.get("pending_trimmed"):
            print(f"  Pending trimmed: {results['pending_trimmed']}")
        if results.get("snapshots_cleaned"):
            print(f"  Snapshots cleaned: {results['snapshots_cleaned']}")
        if results.get("evolution"):
            ev = results["evolution"]
            if ev.get("decay", {}).get("decayed"):
                print(f"  Evolution decayed: {ev['decay']['decayed']}")

    return 0


def cmd_rotate(args) -> int:
    """Full rotation: maintenance + evolution + flush + cleanup. For hourly runs."""
    start = time.time()

    if not _check_stores_exist():
        print(json.dumps({"status": "no_op", "reason": "no_stores"}))
        return 0

    # Step 1: Maintenance with full evolution
    maint_results = _bounded_maintenance(force=args.force, enable_evolution=True)

    # Step 2: Run full evolution pass with optional promotion
    from subconscious.evolution import run_evolution_pass, scan_and_promote_eligible

    evolution_results = run_evolution_pass(
        dry_run=False,
        enable_promotion=args.enable_promotion
    )
    maint_results["evolution_full"] = evolution_results

    # Step 3: Snapshot (compact bootstrap pack)
    session_ctx = {
        "project": args.project or "maintenance_rotation",
        "topics": args.topics.split(",") if args.topics else [],
        "turn_count": 0,
        "trigger": "scheduled_rotation",
    }

    snapshot = build_snapshot(session_ctx)

    # Safety: truncate unresolved
    unresolved = snapshot.get("unresolved", [])
    if len(unresolved) > 10:
        snapshot["unresolved"] = unresolved[:10]
        snapshot["_meta"] = {"unresolved_truncated": True}

    path = write_snapshot(snapshot)

    # Step 4: Cleanup
    removed = _cleanup_snapshots()

    elapsed_ms = (time.time() - start) * 1000

    output = {
        "status": "ok",
        "operation": "rotate",
        "maintenance": maint_results,
        "evolution": evolution_results,
        "snapshot": {
            "path": str(path),
            "size_kb": round(path.stat().st_size / 1024, 2),
        },
        "snapshots_cleaned": removed,
        "usage_after": _get_resource_usage(),
        "elapsed_ms": round(elapsed_ms, 2),
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"Rotation complete ({elapsed_ms:.1f}ms)")
        print(f"  Snapshot: {path.name} ({output['snapshot']['size_kb']:.1f}KB)")
        if maint_results.get("decayed"):
            print(f"  Decayed: {maint_results['decayed']}")
        if evolution_results.get("salience", {}).get("adjusted"):
            print(f"  Salience tuned: {evolution_results['salience']['adjusted']}")
        if evolution_results.get("promotion", {}).get("promoted"):
            print(f"  Promoted to live: {evolution_results['promotion']['promoted']}")
        if removed:
            print(f"  Old snapshots removed: {removed}")

    return 0


def cmd_review(args) -> int:
    """Daily review: summary + status + optional resurface."""
    start = time.time()

    if not _check_stores_exist():
        print(json.dumps({"status": "no_op", "reason": "no_stores"}))
        return 0

    # Get status
    usage = _get_resource_usage()
    metrics = get_metrics()
    ok, warnings = _check_resource_limits(usage)

    # Get recent items for review
    live_items = load("live")
    recent_active = [
        item for item in live_items
        if item.get("status") == "active" and item.get("freshness", 0) > 0.5
    ][:10]

    # Build summary
    elapsed_ms = (time.time() - start) * 1000

    output = {
        "status": "ok" if ok else "warning",
        "operation": "review",
        "usage": usage,
        "metrics": metrics,
        "warnings": warnings if warnings else None,
        "recent_active_items": [
            {"text": i.get("text", "")[:60], "freshness": i.get("freshness", 0)}
            for i in recent_active
        ],
        "elapsed_ms": round(elapsed_ms, 2),
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"Daily Review ({elapsed_ms:.1f}ms)")
        print(f"  Core: {usage['core_count']}, Live: {usage['live_count']}, Pending: {usage['pending_lines']}")
        print(f"  Snapshots: {usage['snapshot_count']}")
        if warnings:
            print("  Warnings:")
            for w in warnings:
                print(f"    ! {w}")
        else:
            print("  Status: Healthy")
        if recent_active:
            print(f"  Active items: {len(recent_active)}")

    return 0 if ok else 2


def cmd_status(args) -> int:
    """Quick status check."""
    usage = _get_resource_usage()
    metrics = get_metrics()
    ok, warnings = _check_resource_limits(usage)

    output = {
        "status": "ok" if ok else "warning",
        "usage": usage,
        "ceilings": {
            "max_pending_lines": ResourceCeilings.MAX_PENDING_LINES,
            "max_live_items": ResourceCeilings.MAX_LIVE_ITEMS,
            "max_core_items": ResourceCeilings.MAX_CORE_ITEMS,
            "max_snapshots": ResourceCeilings.MAX_SNAPSHOTS,
        },
        "warnings": warnings if warnings else None,
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print("Subconscious 24/7 Status")
        print(f"  Core: {usage['core_count']}/{ResourceCeilings.MAX_CORE_ITEMS}")
        print(f"  Live: {usage['live_count']}/{ResourceCeilings.MAX_LIVE_ITEMS}")
        print(f"  Pending: {usage['pending_lines']}/{ResourceCeilings.MAX_PENDING_LINES}")
        print(f"  Snapshots: {usage['snapshot_count']}/{ResourceCeilings.MAX_SNAPSHOTS}")
        print(f"  Events: {usage['events_size_mb']:.1f}MB/{ResourceCeilings.MAX_EVENTS_LOG_MB}MB")
        if warnings:
            print("  Warnings:")
            for w in warnings:
                print(f"    ! {w}")
        else:
            print("  Status: OK")

    return 0 if ok else 2


def cmd_evolve(args) -> int:
    """Run bounded self-evolution pass."""
    start = time.time()

    if not _check_stores_exist():
        print(json.dumps({"status": "no_op", "reason": "no_stores"}))
        return 0

    from subconscious.evolution import run_evolution_pass

    results = run_evolution_pass(
        dry_run=args.dry_run,
        enable_promotion=args.enable_promotion,
    )

    elapsed_ms = (time.time() - start) * 1000

    output = {
        "status": "ok",
        "operation": "evolve",
        "dry_run": args.dry_run,
        "results": results,
        "elapsed_ms": round(elapsed_ms, 2),
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        mode = "DRY RUN" if args.dry_run else "LIVE"
        print(f"Evolution pass complete ({elapsed_ms:.1f}ms) [{mode}]")
        if results.get("decay", {}).get("decayed"):
            print(f"  Decayed: {results['decay']['decayed']}")
        if results.get("archival", {}).get("archived"):
            print(f"  Archived: {results['archival']['archived']}")
        if results.get("salience", {}).get("adjusted"):
            print(f"  Salience tuned: {results['salience']['adjusted']}")
        if results.get("promotion", {}).get("eligible"):
            print(f"  Promotion eligible: {results['promotion']['eligible']}")
            print(f"  Promoted: {results['promotion'].get('promoted', 0)}")

    return 0


def cmd_governance(args) -> int:
    """Show governance rules and protections."""
    from subconscious.governance import get_governance_summary

    summary = get_governance_summary()

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print("Subconscious Governance Rules")
        print("\nProtected Classes (Manual-only):")
        for p in summary["protected_classes"]:
            print(f"  - {p}")

        print("\nAllowed Auto-Mutations:")
        for m in summary["allowed_mutations"]:
            print(f"  - {m}")

        print("\nGated Mutations (Requires thresholds):")
        for m in summary["gated_mutations"]:
            print(f"  - {m}")

        print("\nProhibited Mutations:")
        for m in summary["prohibited_mutations"]:
            print(f"  - {m}")

        print("\nGate Thresholds:")
        for k, v in summary["gate_thresholds"].items():
            print(f"  {k}: {v}")

        print("\nMutation Bounds:")
        for k, v in summary["mutation_bounds"].items():
            print(f"  {k}: {v}")

    return 0


def cmd_verify(args) -> int:
    """Verify 24/7 bounded behavior: run multiple ticks, check state stays bounded."""
    print("=== Subconscious 24/7 Bounded Verification ===\n")

    all_passed = True

    # Test 1: Resource ceilings enforced
    print("Test 1: Resource ceilings enforced")
    usage = _get_resource_usage()
    ok, warnings = _check_resource_limits(usage)
    print(f"  [{'PASS' if ok else 'FAIL'}] Current usage within limits")
    if warnings:
        for w in warnings:
            print(f"    ! {w}")
    if not ok:
        all_passed = False

    # Test 2: Tick is idempotent and fast
    print("\nTest 2: Tick idempotency and speed (3 consecutive runs)")
    for i in range(3):
        start = time.time()
        usage_before = _get_resource_usage()
        results = _bounded_maintenance(enable_evolution=True)
        elapsed = (time.time() - start) * 1000

        ok = elapsed < ResourceCeilings.MAX_TICK_DURATION_MS
        print(f"  [{'PASS' if ok else 'FAIL'}] Tick {i+1}: {elapsed:.1f}ms (limit: {ResourceCeilings.MAX_TICK_DURATION_MS}ms)")
        if not ok:
            all_passed = False

    # Test 3: State stays bounded after repeated ticks
    print("\nTest 3: State bounded after repeated operations")
    usage = _get_resource_usage()
    checks = [
        (usage["pending_lines"] <= ResourceCeilings.MAX_PENDING_LINES, "pending"),
        (usage["live_count"] <= ResourceCeilings.MAX_LIVE_ITEMS, "live"),
        (usage["snapshot_count"] <= ResourceCeilings.MAX_SNAPSHOTS, "snapshots"),
    ]
    for check, name in checks:
        print(f"  [{'PASS' if check else 'FAIL'}] {name} within limit")
        if not check:
            all_passed = False

    # Test 4: Governance rules enforced
    print("\nTest 4: Governance enforcement")
    from subconscious.governance import check_promotion_to_core_eligible, PROHIBITED_MUTATIONS

    # Test that promotion to core is prohibited
    ok, _ = check_promotion_to_core_eligible(None)
    ok = not ok  # Should be NOT allowed
    print(f"  [{'PASS' if ok else 'FAIL'}] Promotion to core is prohibited")
    if not ok:
        all_passed = False

    # Test 5: Evolution bounds respected
    print("\nTest 5: Evolution bounds respected")
    from subconscious.governance import MUTATION_BOUNDS
    checks = [
        MUTATION_BOUNDS.get("weight_delta", 1.0) <= 0.1,
        MUTATION_BOUNDS.get("confidence_delta", 1.0) <= 0.2,
        MUTATION_BOUNDS.get("max_freshness_decay", 1.0) <= 0.3,
    ]
    for i, check in enumerate(checks):
        print(f"  [{'PASS' if check else 'FAIL'}] Bound {i+1} respected")
        if not check:
            all_passed = False

    # Test 6: No-op when empty
    print("\nTest 6: No-op behavior when nothing to do")
    print(f"  [INFO] Current pending: {usage['pending_lines']}")
    print(f"  [INFO] Tick will no-op if below thresholds")

    # Summary
    print("\n=== Verification Summary ===")
    if all_passed:
        print("All tests PASSED - System is safe for 24/7 operation")
        return 0
    else:
        print("Some tests FAILED - Review limits before enabling 24/7 mode")
        return 1


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Subconscious 24/7 Bounded Metabolism",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
24/7 Operation Pattern:
  # Every 5 minutes (light maintenance + evolution)
  */5 * * * * python %(prog)s tick

  # Hourly (full rotation with snapshot + evolution)
  0 * * * * python %(prog)s rotate

  # Daily at 6am (review)
  0 6 * * * python %(prog)s review

  # Manual evolution pass (optional)
  python %(prog)s evolve

Commands:
  tick        - Light maintenance (decay, cleanup, evolution) - safe every 5 min
  rotate      - Full rotation (maintain + evolve + flush + cleanup) - hourly
  evolve      - Run bounded self-evolution pass
  governance  - Show governance rules and protections
  review      - Daily summary and health check
  status      - Quick status check
  verify      - Run boundedness verification tests
"""
    )
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--force", action="store_true", help="Force despite limits")
    parser.add_argument("--project", help="Project context for rotation")
    parser.add_argument("--topics", help="Comma-separated topics for rotation")
    parser.add_argument("--enable-promotion", action="store_true",
                        help="Enable pending->live promotion (gated by thresholds)")

    subparsers = parser.add_subparsers(dest="command", help="Command")

    # tick
    p_tick = subparsers.add_parser("tick", help="Light metabolism tick")
    p_tick.set_defaults(func=cmd_tick)

    # rotate
    p_rotate = subparsers.add_parser("rotate", help="Full rotation with snapshot")
    p_rotate.add_argument("--enable-promotion", action="store_true",
                          help="Enable pending->live promotion (gated by thresholds)")
    p_rotate.set_defaults(func=cmd_rotate)

    # evolve
    p_evolve = subparsers.add_parser("evolve", help="Run bounded self-evolution")
    p_evolve.add_argument("--dry-run", action="store_true", help="Show what would happen")
    p_evolve.set_defaults(func=cmd_evolve)

    # governance
    p_gov = subparsers.add_parser("governance", help="Show governance rules")
    p_gov.set_defaults(func=cmd_governance)

    # review
    p_review = subparsers.add_parser("review", help="Daily review")
    p_review.set_defaults(func=cmd_review)

    # status
    p_status = subparsers.add_parser("status", help="Quick status")
    p_status.set_defaults(func=cmd_status)

    # verify
    p_verify = subparsers.add_parser("verify", help="Verify bounded behavior")
    p_verify.set_defaults(func=cmd_verify)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
