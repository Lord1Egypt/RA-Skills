"""File storage layer with atomic writes and simple locking."""

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def _utc_now() -> str:
    """Get current UTC timestamp as ISO string."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# Default paths relative to workspace (auto-detect install location)
# Skill lives at: ~/.openclaw/skills/subconscious/subconscious/
# Workspace: detected from env var SUBCONSCIOUS_WORKSPACE or by finding the parent openclaw workspace
# Prefers workspace-alfred if multiple workspaces exist

_SKILL_DIR = Path(__file__).parent.resolve()
_WS_ENV = os.environ.get("SUBCONSCIOUS_WORKSPACE", "").strip()

if _WS_ENV:
    # Explicit override
    _WORKSPACE = Path(_WS_ENV)
else:
    # Walk up from skill: subconscious/ -> skills/ -> ~/.openclaw/ -> find "memory" sibling
    _parent = _SKILL_DIR.parent.parent.parent  # ~/.openclaw/
    # Find all workspaces: dirs that have memory/ subdir (openclaw workspace convention)
    _candidates = [_c for _c in _parent.iterdir()
                  if _c.is_dir() and (_c / "memory").is_dir()]
    # Prefer workspace-alfred if it exists, otherwise first alphabetically
    _WORKSPACE = next(
        (_c for _c in _candidates if _c.name == "workspace-alfred"),
        _candidates[0] if _candidates else _parent / "workspace-alfred"
    )

DEFAULT_BASE_PATH = _WORKSPACE / "memory" / "subconscious"


def _ensure_dir(path: Path) -> None:
    """Ensure directory exists."""
    path.parent.mkdir(parents=True, exist_ok=True)


def load(layer: str, base_path: Optional[Path] = None) -> list[dict]:
    """Load items from a layer store.

    Args:
        layer: One of 'core', 'live', 'pending'
        base_path: Override base storage path

    Returns:
        List of item dicts
    """
    base = base_path or DEFAULT_BASE_PATH

    if layer == "pending":
        # pending is a JSONL file
        path = base / "pending.jsonl"
        if not path.exists():
            return []
        items = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    items.append(json.loads(line))
        return items
    else:
        # core and live are JSON files
        path = base / f"{layer}.json"
        if not path.exists():
            return []
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("items", [])


def save(layer: str, items: list[dict], base_path: Optional[Path] = None, force: bool = False) -> None:
    """Save items to a layer store with atomic write.

    Args:
        layer: One of 'core', 'live', 'pending'
        items: List of item dicts to save
        base_path: Override base storage path
        force: Required for 'core' layer saves

    Raises:
        RuntimeError: If saving to core without force=True
    """
    base = base_path or DEFAULT_BASE_PATH

    # Core protection: require explicit force flag
    if layer == "core" and not force:
        raise RuntimeError(
            "Cannot save to core without force=True. "
            "Core modifications must be explicit and user-confirmed."
        )

    if layer == "pending":
        raise RuntimeError(
            "Use append_event for pending queue. "
            "Pending is append-only JSONL, not overwrite."
        )

    path = base / f"{layer}.json"
    _ensure_dir(path)

    # Atomic write: write to temp, then rename
    temp_fd, temp_path = tempfile.mkstemp(dir=base, suffix=".tmp")
    try:
        with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
            json.dump({"items": items, "meta": {"saved_at": _utc_now()}}, f, indent=2)
        os.replace(temp_path, path)
    except Exception:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise


def append_event(event_type: str, data: dict, base_path: Optional[Path] = None) -> None:
    """Append an event to the pending queue or events log.

    Args:
        event_type: Type of event (created, reinforced, decayed, etc.)
        data: Event data dict
        base_path: Override base storage path
    """
    base = base_path or DEFAULT_BASE_PATH
    path = base / "pending.jsonl"
    _ensure_dir(path)

    event = {
        "type": event_type,
        "timestamp": _utc_now(),
        "data": data,
    }

    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, separators=(",", ":")) + "\n")


def append_to_events_log(event_type: str, item_id: str, details: Optional[dict] = None, base_path: Optional[Path] = None) -> None:
    """Append to the audit events log.

    Args:
        event_type: Type of event
        item_id: ID of affected item
        details: Optional additional details
        base_path: Override base storage path
    """
    base = base_path or DEFAULT_BASE_PATH
    path = base / "events.jsonl"
    _ensure_dir(path)

    event = {
        "type": event_type,
        "item_id": item_id,
        "timestamp": _utc_now(),
        "details": details or {},
    }

    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, separators=(",", ":")) + "\n")


def load_config(base_path: Optional[Path] = None) -> dict:
    """Load config file."""
    base = base_path or DEFAULT_BASE_PATH
    path = base / "config.json"

    if not path.exists():
        return _default_config()

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# 24/7 Bounded Operation Ceilings (Hard Limits)
RESOURCE_CEILINGS = {
    "max_pending_lines": 500,       # Max lines in pending.jsonl
    "max_live_items": 100,          # Max items in live.json
    "max_core_items": 50,           # Warning threshold for core
    "max_snapshots": 10,            # Max snapshot files kept
    "max_snapshot_size_kb": 50,     # Max single snapshot size
    "max_bootstrap_chars": 1000,    # Max chars in bootstrap context
    "max_bias_chars": 500,          # Max chars in bias block
    "max_events_log_mb": 10,        # Max events.jsonl size before rotation
    "events_rotate_count": 3,       # Keep 3 rotated event logs
    "max_tick_duration_ms": 500,    # Max time for metabolism tick
    "no_op_if_empty": True,         # Skip work if nothing to do
}


def _default_config() -> dict:
    """Default configuration with 24/7 bounded operation settings."""
    return {
        "version": "1.5.0",
        "thresholds": {
            "min_confidence_surface": 0.7,
            "min_confidence_live": 0.6,
            "min_confidence_core": 0.95,
            "max_bias_items": 5,
            "max_live_items": 100,
            "max_pending_items": 200,
            "max_snapshot_size_kb": 50,
        },
        "decay": {
            "fast": 0.2,
            "medium": 0.05,
            "sticky": 0.01,
        },
        "ceilings": RESOURCE_CEILINGS,  # 24/7 hard limits
        "operation_mode": "bounded",  # "bounded" | "unbounded" (for 24/7 safety)
    }


def check_resource_bounds(base_path: Optional[Path] = None) -> tuple[bool, dict, list[str]]:
    """Check if resource usage is within 24/7 ceilings.

    Returns:
        (ok, usage_dict, warnings) - ok=True if all limits respected
    """
    base = base_path or DEFAULT_BASE_PATH
    ceilings = RESOURCE_CEILINGS
    usage = {
        "core_count": 0,
        "live_count": 0,
        "pending_lines": 0,
        "snapshot_count": 0,
        "events_size_mb": 0,
    }
    warnings = []

    # Count items
    core_path = base / "core.json"
    if core_path.exists():
        try:
            with open(core_path, "r") as f:
                data = json.load(f)
                usage["core_count"] = len(data.get("items", []))
        except (json.JSONDecodeError, IOError):
            pass

    live_path = base / "live.json"
    if live_path.exists():
        try:
            with open(live_path, "r") as f:
                data = json.load(f)
                usage["live_count"] = len(data.get("items", []))
        except (json.JSONDecodeError, IOError):
            pass

    # Count pending lines
    pending_path = base / "pending.jsonl"
    if pending_path.exists():
        try:
            with open(pending_path, "r") as f:
                usage["pending_lines"] = sum(1 for _ in f if _.strip())
        except IOError:
            pass

    # Count snapshots
    snap_dir = base / "snapshots"
    if snap_dir.exists():
        usage["snapshot_count"] = len(list(snap_dir.glob("*.json")))

    # Events log size
    events_path = base / "events.jsonl"
    if events_path.exists():
        usage["events_size_mb"] = events_path.stat().st_size / (1024 * 1024)

    # Check limits
    if usage["pending_lines"] > ceilings["max_pending_lines"]:
        warnings.append(f"Pending lines ({usage['pending_lines']}) exceeds max ({ceilings['max_pending_lines']})")

    if usage["live_count"] > ceilings["max_live_items"]:
        warnings.append(f"Live items ({usage['live_count']}) exceeds max ({ceilings['max_live_items']})")

    if usage["core_count"] > ceilings["max_core_items"]:
        warnings.append(f"Core items ({usage['core_count']}) exceeds warning ({ceilings['max_core_items']})")

    if usage["snapshot_count"] > ceilings["max_snapshots"]:
        warnings.append(f"Snapshots ({usage['snapshot_count']}) exceeds max ({ceilings['max_snapshots']})")

    if usage["events_size_mb"] > ceilings["max_events_log_mb"]:
        warnings.append(f"Events log ({usage['events_size_mb']:.1f}MB) exceeds max ({ceilings['max_events_log_mb']}MB)")

    return len(warnings) == 0, usage, warnings
