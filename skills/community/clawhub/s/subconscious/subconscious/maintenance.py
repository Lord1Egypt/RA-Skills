"""Low-risk maintenance helpers: decay, cleanup, rotation, metrics.

No automatic promotion. No recursive self-modification.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .schema import Item, ItemLayer, ItemStatus
from .store import load, save, load_config, DEFAULT_BASE_PATH


def _utc_now() -> str:
    """Get current UTC timestamp as ISO string."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run_maintenance(base_path: Optional[Path] = None, force_decay: bool = False) -> dict:
    """Run maintenance pass.

    Args:
        base_path: Override storage path
        force_decay: Run decay even if not scheduled

    Returns:
        Metrics dict of what was done
    """
    base = base_path or DEFAULT_BASE_PATH
    config = load_config(base)
    results = {
        "decayed": 0,
        "archived": 0,
        "removed_from_pending": 0,
        "metrics_updated": False,
    }

    # Decay live items
    if force_decay:
        results["decayed"] = _decay_live_items(base, config)

    # Archive stale items
    results["archived"] = _archive_stale_items(base)

    # Cleanup old pending
    results["removed_from_pending"] = _cleanup_pending(base, max_age_days=7)

    # Update metrics
    _update_metrics(base)
    results["metrics_updated"] = True

    return results


def _decay_live_items(base: Path, config: dict) -> int:
    """Apply decay to live items based on policy."""
    decay_rates = config.get("decay", {})
    live_data = load("live", base)

    now = datetime.now(timezone.utc)
    decayed_count = 0

    updated_items = []
    for item_data in live_data:
        policy = item_data.get("decay", {}).get("policy", "medium")
        last_accessed = item_data.get("decay", {}).get("lastAccessed")

        if last_accessed:
            try:
                accessed = datetime.fromisoformat(last_accessed.replace("Z", "+00:00"))
                days_since = (now - accessed).days

                # Apply decay
                rate = decay_rates.get(policy, 0.05)
                freshness = item_data.get("freshness", 1.0)
                new_freshness = max(0.0, freshness - (rate * days_since))

                if new_freshness != freshness:
                    item_data["freshness"] = new_freshness
                    decayed_count += 1

            except (ValueError, TypeError):
                pass

        updated_items.append(item_data)

    # Save with force (live is auto-ok)
    save("live", updated_items, base, force=True)
    return decayed_count


def _archive_stale_items(base: Path, stale_threshold: float = 0.1) -> int:
    """Archive live items with very low freshness."""
    live_data = load("live", base)

    archived_count = 0
    for item_data in live_data:
        if item_data.get("freshness", 1.0) < stale_threshold:
            item_data["status"] = "archived"
            archived_count += 1

    save("live", live_data, base, force=True)
    return archived_count


def _cleanup_pending(base: Path, max_age_days: int = 7) -> int:
    """Remove old entries from pending queue."""
    pending_path = base / "pending.jsonl"
    if not pending_path.exists():
        return 0

    now = datetime.now(timezone.utc)
    kept = []
    removed = 0

    with open(pending_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                event = json.loads(line)
                ts = event.get("timestamp", "")
                if ts:
                    event_time = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    days_old = (now - event_time).days
                    if days_old <= max_age_days:
                        kept.append(line)
                    else:
                        removed += 1
                else:
                    kept.append(line)
            except (json.JSONDecodeError, ValueError):
                kept.append(line)  # Keep malformed lines

    # Rewrite pending queue
    with open(pending_path, "w", encoding="utf-8") as f:
        for line in kept:
            f.write(line + "\n")

    return removed


def _update_metrics(base: Path) -> None:
    """Update system metrics."""
    core = load("core", base)
    live = load("live", base)

    # Count pending lines
    pending_count = 0
    pending_path = base / "pending.jsonl"
    if pending_path.exists():
        with open(pending_path, "r", encoding="utf-8") as f:
            pending_count = sum(1 for _ in f if _.strip())

    metrics = {
        "timestamp": _utc_now(),
        "counts": {
            "core": len(core),
            "live": len(live),
            "pending": pending_count,
        },
        "thresholds": {
            "core_warning": 50,
            "live_warning": 100,
            "pending_warning": 150,
        },
    }

    metrics_path = base / "metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)


def get_metrics(base_path: Optional[Path] = None) -> dict:
    """Load current metrics."""
    base = base_path or DEFAULT_BASE_PATH
    metrics_path = base / "metrics.json"

    if not metrics_path.exists():
        return {"counts": {"core": 0, "live": 0, "pending": 0}}

    with open(metrics_path, "r", encoding="utf-8") as f:
        return json.load(f)
