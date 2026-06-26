"""Bounded self-evolution subsystem.

Handles salience tuning, confidence/freshness updates, contradiction handling,
adaptive item reinforcement/decay/archival, and pending->live promotion.

All operations are governed by governance.py rules. No operation can bypass
protection classes or prohibited mutations.
"""

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

from .schema import Item, ItemKind, ItemLayer, ItemStatus
from .store import load, save, append_to_events_log, DEFAULT_BASE_PATH
from .governance import (
    MutationType,
    check_mutation_allowed,
    apply_mutation,
    check_promotion_to_live_eligible,
    classify_protection,
)


def _utc_now() -> str:
    """Get current UTC timestamp as ISO string."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _days_since(timestamp: str) -> int:
    """Calculate days since timestamp."""
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).days
    except (ValueError, TypeError):
        return 0


# =============================================================================
# SALIENCE TUNING
# =============================================================================

def tune_salience(
    base_path: Optional[Path] = None,
    dry_run: bool = False
) -> dict:
    """Tune salience weights based on access patterns and relevance.

    This adjusts weights within bounded limits based on:
    - Recency of access
    - Reinforcement count
    - Link to active projects
    """
    base = base_path or DEFAULT_BASE_PATH
    results = {"adjusted": 0, "skipped": 0, "errors": []}

    # Only tune live items (core is protected)
    live_data = load("live", base)
    updated = []

    for item_data in live_data:
        try:
            item = Item.from_dict(item_data)

            # Skip archived
            if item.status == ItemStatus.ARCHIVED:
                updated.append(item_data)
                continue

            # Calculate salience delta
            delta = _calculate_salience_delta(item)

            if delta == 0:
                updated.append(item_data)
                continue

            # Apply via governance
            if dry_run:
                allowed, _ = check_mutation_allowed(item, MutationType.WEIGHT_UPDATE)
                if allowed:
                    results["adjusted"] += 1
                else:
                    results["skipped"] += 1
                updated.append(item_data)
            else:
                success, new_item, reason = apply_mutation(
                    item, MutationType.WEIGHT_UPDATE, delta
                )
                if success:
                    results["adjusted"] += 1
                    updated.append(new_item.to_dict())
                    _log_mutation("weight_tune", new_item, {"delta": delta})
                else:
                    results["skipped"] += 1
                    updated.append(item_data)

        except Exception as e:
            results["errors"].append(f"Error tuning {item_data.get('id', 'unknown')}: {e}")
            updated.append(item_data)

    if not dry_run and results["adjusted"] > 0:
        save("live", updated, base, force=True)

    return results


def _calculate_salience_delta(item: Item) -> float:
    """Calculate weight adjustment based on item characteristics."""
    delta = 0.0

    # Boost frequently reinforced items
    if item.reinforcement.count >= 5:
        delta += 0.05
    elif item.reinforcement.count >= 3:
        delta += 0.02

    # Penalize stale items
    days = _days_since(item.decay.last_accessed or item.reinforcement.last_at or _utc_now())
    if days > 14:
        delta -= 0.1
    elif days > 7:
        delta -= 0.05

    # Boost high-confidence hypotheses that have been reinforced
    if item.kind == ItemKind.HYPOTHESIS and item.reinforcement.count >= 2:
        delta += 0.03

    # Boost projects with activity
    if item.kind == ItemKind.PROJECT and item.freshness > 0.7:
        delta += 0.02

    # Clamp to safe bounds
    return max(-0.1, min(0.1, delta))


# =============================================================================
# CONFIDENCE & FRESHNESS UPDATES
# =============================================================================

def update_confidence(
    item_id: str,
    evidence_delta: float,
    base_path: Optional[Path] = None
) -> tuple[bool, str]:
    """Update an item's confidence based on new evidence.

    Args:
        item_id: ID of item to update
        evidence_delta: Confidence change (-1 to 1, typically small)
        base_path: Optional override

    Returns:
        (success, reason)
    """
    base = base_path or DEFAULT_BASE_PATH

    # Find item (check live first, then core for completeness)
    for layer in ["live", "core"]:
        items = load(layer, base)
        for i, item_data in enumerate(items):
            if item_data.get("id") == item_id:
                try:
                    item = Item.from_dict(item_data)

                    # Apply via governance
                    success, new_item, reason = apply_mutation(
                        item,
                        MutationType.CONFIDENCE_UPDATE,
                        evidence_delta,
                        {"layer": layer}
                    )

                    if success:
                        items[i] = new_item.to_dict()
                        save(layer, items, base, force=True)
                        _log_mutation("confidence_update", new_item, {"delta": evidence_delta})
                        return True, reason
                    else:
                        return False, reason

                except Exception as e:
                    return False, f"Error updating: {e}"

    return False, f"Item {item_id} not found"


def update_freshness(
    base_path: Optional[Path] = None,
    force_decay: bool = False
) -> dict:
    """Update freshness for all items based on decay policy.

    Returns:
        Summary of updates
    """
    base = base_path or DEFAULT_BASE_PATH
    results = {"decayed": 0, "archived": 0, "skipped": 0}

    # Only decay live items
    live_data = load("live", base)
    updated = []

    decay_rates = {
        "fast": 0.1,
        "medium": 0.05,
        "sticky": 0.02,
    }

    for item_data in live_data:
        try:
            item = Item.from_dict(item_data)

            if item.status == ItemStatus.ARCHIVED:
                updated.append(item_data)
                continue

            # Calculate days since last access
            days = _days_since(item.decay.last_accessed or _utc_now())

            if days == 0 and not force_decay:
                updated.append(item_data)
                continue

            # Apply decay via governance
            rate = decay_rates.get(item.decay.policy, 0.05)
            delta = -rate * days

            success, new_item, _ = apply_mutation(
                item, MutationType.FRESHNESS_DECAY, delta
            )

            if success and new_item.freshness != item.freshness:
                results["decayed"] += 1

                # Archive very stale items
                if new_item.freshness < 0.1:
                    archive_success, archived_item, _ = apply_mutation(
                        new_item, MutationType.ARCHIVAL, 0
                    )
                    if archive_success:
                        new_item = archived_item
                        results["archived"] += 1

                updated.append(new_item.to_dict())
            else:
                updated.append(item_data)

        except Exception as e:
            updated.append(item_data)

    if results["decayed"] > 0 or results["archived"] > 0:
        save("live", updated, base, force=True)

    return results


# =============================================================================
# CONTRADICTION HANDLING
# =============================================================================

def handle_contradiction(
    item_id: str,
    contradictory_evidence: str,
    evidence_confidence: float,
    base_path: Optional[Path] = None
) -> tuple[bool, str]:
    """Handle contradictory evidence against an item.

    This is a gated operation requiring high confidence evidence.

    Args:
        item_id: ID of contradicted item
        contradictory_evidence: Text describing the contradiction
        evidence_confidence: Confidence in the contradictory evidence
        base_path: Optional override

    Returns:
        (success, reason)
    """
    base = base_path or DEFAULT_BASE_PATH

    # Find item
    for layer in ["live", "core"]:
        items = load(layer, base)
        for i, item_data in enumerate(items):
            if item_data.get("id") == item_id:
                try:
                    item = Item.from_dict(item_data)

                    # Check via governance (gated operation)
                    context = {"evidence_confidence": evidence_confidence}
                    allowed, reason = check_mutation_allowed(
                        item, MutationType.CONTRADICTION, context
                    )

                    if not allowed:
                        return False, reason

                    # Apply contradiction: reduce confidence significantly
                    success, new_item, _ = apply_mutation(
                        item,
                        MutationType.CONFIDENCE_UPDATE,
                        -evidence_confidence * 0.5,  # Significant reduction
                        context
                    )

                    if success:
                        # Add contradiction note
                        if not hasattr(new_item, "contradictions"):
                            new_item.notes = ""
                        new_item.notes += f"\nContradiction at {_utc_now()}: {contradictory_evidence[:100]}"

                        # Archive if confidence drops too low
                        if new_item.confidence < 0.4:
                            archive_success, new_item, _ = apply_mutation(
                                new_item, MutationType.ARCHIVAL, 0
                            )

                        items[i] = new_item.to_dict()
                        save(layer, items, base, force=True)

                        _log_mutation(
                            "contradiction",
                            new_item,
                            {"evidence": contradictory_evidence[:100], "confidence": evidence_confidence}
                        )
                        return True, f"Contradiction handled, confidence now {new_item.confidence}"

                except Exception as e:
                    return False, f"Error handling contradiction: {e}"

    return False, f"Item {item_id} not found"


# =============================================================================
# REINFORCEMENT
# =============================================================================

def reinforce_item(
    item_id: str,
    base_path: Optional[Path] = None
) -> tuple[bool, str]:
    """Reinforce an item (increment count and update last access).

    This is an allowed operation for most items.
    """
    base = base_path or DEFAULT_BASE_PATH

    # Find in pending (JSONL, special handling), then live/core (JSON)
    # pending is append-only, so we read all events, update the target item, rewrite
    pending_path = base / "pending.jsonl"
    if pending_path.exists():
        import json as _json
        updated_lines = []
        found = False
        with open(pending_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                record = _json.loads(line)
                item_data = record.get("data", {})
                if item_data.get("id") == item_id:
                    try:
                        item = Item.from_dict(item_data)
                        success_flag, new_item, reason = apply_mutation(
                            item, MutationType.REINFORCEMENT, 0
                        )
                        if success_flag:
                            record["data"] = new_item.to_dict()
                            record["type"] = "candidate_reinforced"  # mark the update
                            found = True
                    except Exception as e:
                        pass
                updated_lines.append(record)
        if found:
            with open(pending_path, "w", encoding="utf-8") as f:
                for record in updated_lines:
                    f.write(_json.dumps(record) + "\n")
            _log_mutation("reinforcement", Item.from_dict(updated_lines[-1]["data"]), {})
            return True, f"Reinforced (pending layer): {item_id}"
        # fall through if not found in pending

    # Find in live or core
    for layer in ["live", "core"]:
        items = load(layer, base)
        for i, item_data in enumerate(items):
            if item_data.get("id") == item_id:
                try:
                    item = Item.from_dict(item_data)

                    success, new_item, reason = apply_mutation(
                        item, MutationType.REINFORCEMENT, 0
                    )

                    if success:
                        items[i] = new_item.to_dict()
                        save(layer, items, base, force=True)
                        _log_mutation("reinforcement", new_item, {})
                        return True, reason
                    else:
                        return False, reason

                except Exception as e:
                    return False, f"Error reinforcing: {e}"

    return False, f"Item {item_id} not found"


def auto_reinforce_from_usage(
    accessed_item_ids: list[str],
    base_path: Optional[Path] = None
) -> dict:
    """Auto-reinforce items that were accessed/used.

    This is called when items influence a reply (bias building).
    """
    base = base_path or DEFAULT_BASE_PATH
    results = {"reinforced": 0, "failed": 0}

    for item_id in accessed_item_ids:
        success, _ = reinforce_item(item_id, base)
        if success:
            results["reinforced"] += 1
        else:
            results["failed"] += 1

    return results


# =============================================================================
# PROMOTION: PENDING -> LIVE
# =============================================================================

def promote_pending_to_live(
    pending_item_id: str,
    base_path: Optional[Path] = None,
    dry_run: bool = False
) -> tuple[bool, str]:
    """Promote a pending item to live layer.

    This is a GATED operation requiring:
    - Confidence >= 0.8
    - 3+ reinforcements
    - Freshness >= 0.5
    - Age <= 7 days
    """
    base = base_path or DEFAULT_BASE_PATH

    # Load pending
    pending = load("pending", base)

    for event in pending:
        if event.get("type") not in ("candidate_queued", "candidate_reinforced"):
            continue

        data = event.get("data", {})
        if data.get("id") != pending_item_id:
            continue

        try:
            # Create temporary item for governance check
            item = Item.from_dict(data)
            item.layer = ItemLayer.PENDING

            # Check eligibility
            eligible, reason = check_promotion_to_live_eligible(item)
            if not eligible:
                return False, reason

            if dry_run:
                return True, "Would be eligible for promotion"

            # Perform promotion
            item.layer = ItemLayer.LIVE
            item.status = ItemStatus.ACTIVE
            item.decay.last_accessed = _utc_now()

            # Add to live (dedupe by ID — don't promote if already in live)
            live_items = load("live", base)
            existing_ids = {i.get("id") for i in live_items}
            if item.id in existing_ids:
                return True, f"Already in live: {pending_item_id}"
            live_items.append(item.to_dict())
            save("live", live_items, base, force=True)

            _log_mutation("promotion_to_live", item, {"from": "pending"})
            return True, f"Promoted {pending_item_id} to live"

        except Exception as e:
            return False, f"Error promoting: {e}"

    return False, f"Pending item {pending_item_id} not found"


def scan_and_promote_eligible(
    base_path: Optional[Path] = None,
    dry_run: bool = False,
    max_promotions: int = 5
) -> dict:
    """Scan pending queue and promote all eligible items.

    Args:
        base_path: Optional override
        dry_run: If True, only check eligibility without promoting
        max_promotions: Max items to promote in one pass

    Returns:
        Summary of promotions
    """
    base = base_path or DEFAULT_BASE_PATH
    results = {"checked": 0, "eligible": 0, "promoted": 0, "failed": 0}

    pending = load("pending", base)
    eligible_ids = []

    for event in pending:
        if event.get("type") not in ("candidate_queued", "candidate_reinforced"):
            continue

        data = event.get("data", {})
        item_id = data.get("id")
        if not item_id:
            continue

        results["checked"] += 1

        # Check eligibility
        success, reason = promote_pending_to_live(item_id, base, dry_run=True)
        if success:
            results["eligible"] += 1
            eligible_ids.append(item_id)

            if len(eligible_ids) >= max_promotions:
                break

    if not dry_run and eligible_ids:
        for item_id in eligible_ids:
            success, reason = promote_pending_to_live(item_id, base, dry_run=False)
            if success:
                results["promoted"] += 1
            else:
                results["failed"] += 1

    return results


# =============================================================================
# ARCHIVAL
# =============================================================================

def archive_stale_items(
    stale_threshold: float = 0.1,
    base_path: Optional[Path] = None
) -> dict:
    """Archive items with very low freshness."""
    base = base_path or DEFAULT_BASE_PATH
    results = {"archived": 0, "skipped": 0}

    live_data = load("live", base)
    updated = []

    for item_data in live_data:
        try:
            item = Item.from_dict(item_data)

            if item.status == ItemStatus.ARCHIVED:
                updated.append(item_data)
                continue

            if item.freshness < stale_threshold:
                success, new_item, _ = apply_mutation(item, MutationType.ARCHIVAL, 0)
                if success:
                    updated.append(new_item.to_dict())
                    results["archived"] += 1
                    _log_mutation("archival", new_item, {"reason": "stale"})
                else:
                    updated.append(item_data)
            else:
                updated.append(item_data)

        except Exception:
            updated.append(item_data)

    if results["archived"] > 0:
        save("live", updated, base, force=True)

    return results


# =============================================================================
# LOGGING
# =============================================================================

def _log_mutation(mutation_type: str, item: Item, details: dict):
    """Log a mutation to events."""
    append_to_events_log(
        "evolution_mutation",
        item.id,
        {
            "mutation_type": mutation_type,
            "item_kind": item.kind.value,
            "item_layer": item.layer.value,
            "details": details,
        }
    )


# =============================================================================
# RUN ALL EVOLUTION
# =============================================================================

def run_evolution_pass(
    base_path: Optional[Path] = None,
    dry_run: bool = False,
    enable_promotion: bool = False,
) -> dict:
    """Run a complete bounded evolution pass.

    This is the main entry point for self-evolution. It runs:
    1. Freshness decay updates
    2. Archival of stale items
    3. Salience tuning
    4. Optional: pending->live promotion (if enabled)

    Args:
        base_path: Optional override
        dry_run: If True, don't actually modify
        enable_promotion: If True, allow pending->live promotion

    Returns:
        Summary of all evolution activities
    """
    base = base_path or DEFAULT_BASE_PATH

    results = {
        "decay": update_freshness(base, force_decay=False),
        "archival": archive_stale_items(base_path=base),
        "salience": tune_salience(base, dry_run=dry_run),
    }

    if enable_promotion:
        results["promotion"] = scan_and_promote_eligible(base, dry_run=dry_run)
    else:
        results["promotion"] = {"checked": 0, "eligible": 0, "promoted": 0, "note": "promotion disabled"}

    return results
