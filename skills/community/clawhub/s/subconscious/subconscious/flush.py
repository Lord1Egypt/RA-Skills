"""Snapshot builder and loader for session continuity.

Flush = metabolism, not failure. Snapshots are compact bootstrap packs.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .schema import Item
from .store import load, DEFAULT_BASE_PATH


def _utc_now() -> str:
    """Get current UTC timestamp as ISO string."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def build_snapshot(session_context: dict, base_path: Optional[Path] = None) -> dict:
    """Build a snapshot from current state.

    Args:
        session_context: Dict with session metadata
        base_path: Override storage path

    Returns:
        Snapshot dict
    """
    base = base_path or DEFAULT_BASE_PATH

    # Load current stores
    core_items = load("core", base)
    live_items = load("live", base)

    # Compute simple hash of core for change detection
    core_hash = _hash_items(core_items)

    # Get top salient items from live
    hot_items = _get_hot_items(live_items, n=10)

    # Get flagged pending items (if any)
    pending = load("pending", base)
    unresolved = _get_flagged_pending(pending)

    snapshot = {
        "timestamp": _utc_now(),
        "version": "1.5.0",
        "core_hash": core_hash,
        "live_state": live_items,
        "hot_items": hot_items,
        "unresolved": unresolved,
        "session_meta": {
            "last_project": session_context.get("project"),
            "last_topics": session_context.get("topics", []),
            "turn_count": session_context.get("turn_count", 0),
        },
    }

    return snapshot


def write_snapshot(snapshot: dict, base_path: Optional[Path] = None) -> Path:
    """Write snapshot to disk.

    Args:
        snapshot: Snapshot dict
        base_path: Override storage path

    Returns:
        Path to written file
    """
    base = base_path or DEFAULT_BASE_PATH
    snap_dir = base / "snapshots"
    snap_dir.mkdir(parents=True, exist_ok=True)

    # Filename with timestamp
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    path = snap_dir / f"{ts}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)

    # Cleanup old snapshots (keep last 10)
    _cleanup_snapshots(snap_dir, keep=10)

    return path


def load_latest_snapshot(base_path: Optional[Path] = None) -> Optional[dict]:
    """Load the most recent snapshot.

    Args:
        base_path: Override storage path

    Returns:
        Snapshot dict or None if no snapshots
    """
    base = base_path or DEFAULT_BASE_PATH
    snap_dir = base / "snapshots"

    if not snap_dir.exists():
        return None

    # Find latest snapshot
    snapshots = sorted(snap_dir.glob("*.json"), reverse=True)
    if not snapshots:
        return None

    with open(snapshots[0], "r", encoding="utf-8") as f:
        return json.load(f)


def bootstrap(base_path: Optional[Path] = None) -> dict:
    """Bootstrap session from latest snapshot or defaults.

    Args:
        base_path: Override storage path

    Returns:
        Compact context for system prompt
    """
    base = base_path or DEFAULT_BASE_PATH

    # Core is always loaded from canonical core.json
    core = load("core", base)

    # Try to restore live from snapshot
    snapshot = load_latest_snapshot(base)
    if snapshot:
        live = snapshot.get("live_state", [])
        hot = snapshot.get("hot_items", [])
    else:
        live = []
        hot = []

    # Pending starts fresh (never bootstrapped)

    # Build compact context
    context = _build_compact_context(core, live, hot)

    return context


def _hash_items(items: list[dict]) -> str:
    """Simple hash for change detection."""
    import hashlib
    content = json.dumps(items, sort_keys=True)
    return hashlib.md5(content.encode()).hexdigest()[:16]


def _get_hot_items(live_items: list[dict], n: int = 10) -> list[dict]:
    """Get top N salient items by weight * freshness."""
    scored = []
    for item in live_items:
        weight = item.get("weight", 0.5)
        freshness = item.get("freshness", 1.0)
        score = weight * freshness
        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:n]]


def _get_flagged_pending(pending: list[dict]) -> list[dict]:
    """Get pending items flagged for attention."""
    # For now, return pending items with high confidence
    flagged = []
    for event in pending:
        if event.get("type") == "candidate_queued":
            data = event.get("data", {})
            if data.get("confidence", 0) >= 0.8:
                flagged.append(data)
    return flagged[:5]  # Cap at 5


def _build_compact_context(core: list[dict], live: list[dict], hot: list[dict]) -> dict:
    """Build compact context for system prompt."""

    def extract_by_kind(items: list[dict], kind: str) -> list[str]:
        return [i.get("text", "") for i in items if i.get("kind") == kind][:3]

    identity = extract_by_kind(core, "value")
    preferences = extract_by_kind(core, "preference")
    projects = extract_by_kind(live, "project")
    hypotheses = [i.get("text", "") for i in live if i.get("kind") == "hypothesis"][:2]

    return {
        "identity": identity,
        "preferences": preferences,
        "projects": projects,
        "hot_items": [i.get("text", "") for i in hot][:3],
        "hypotheses": hypotheses,
        "_formatted": _format_context(identity, preferences, projects, hot, hypotheses),
    }


def _format_context(identity: list, preferences: list, projects: list, hot: list, hypotheses: list) -> str:
    """Format context as markdown block."""
    lines = ["## SUBCONSCIOUS"]

    if identity:
        lines.append(f"Identity: {', '.join(identity)}")

    if preferences:
        lines.append(f"User preferences: {', '.join(preferences)}")

    active = []
    if projects:
        active.extend([f"[project: {p}]" for p in projects])
    if hypotheses:
        active.extend([f"[hypothesis: {h}]" for h in hypotheses])

    if active:
        lines.append(f"Active: {', '.join(active)}")

    if hot:
        lines.append(f"Recent: {', '.join([i.get('text', '') for i in hot][:2])}")

    return "\n".join(lines)


def _cleanup_snapshots(snap_dir: Path, keep: int = 10) -> None:
    """Remove old snapshots, keeping only the most recent N."""
    snapshots = sorted(snap_dir.glob("*.json"), reverse=True)
    for old in snapshots[keep:]:
        old.unlink()
