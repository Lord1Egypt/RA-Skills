"""Bridge: Self-improving agent .learnings/ → subconscious intake.

Reads entries from the self-improving-agent skill's .learnings/ files and feeds
them into the subconscious system's queue_pending pipeline as Item objects.

Idempotent: each entry is processed exactly once (tracked by entry ID + timestamp).
"""

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .schema import Item, ItemKind, ItemLayer, ItemSource, ItemLinks, ItemReinforcement
from .store import append_event, DEFAULT_BASE_PATH


import os as _os
_WS_ENV = _os.environ.get("SUBCONSCIOUS_WORKSPACE", "").strip()
if _WS_ENV:
    _WORKSPACE = Path(_WS_ENV)
else:
    # Walk up to find workspace: subconscious/ -> skills/ -> ~/.openclaw/ -> any workspace dir
    _skill_parent = Path(__file__).resolve().parent.parent.parent  # ~/.openclaw/
    _candidates = [_c for _c in _skill_parent.iterdir()
                   if _c.is_dir() and (_c / "memory").is_dir()]
    _WORKSPACE = next(
        (_c for _c in _candidates if _c.name == "workspace-alfred"),
        _candidates[0] if _candidates else _skill_parent / "workspace-alfred"
    )
LEARNINGS_DIR = _WORKSPACE / ".learnings"
TRACKER_FILE = DEFAULT_BASE_PATH / "learnings_bridge_last_seen.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# ─── Category mapping ─────────────────────────────────────────────────────────

CATEGORY_KIND_MAP = {
    # LEARNINGS.md categories
    "correction":     ItemKind.LESSON,
    "insight":        ItemKind.VALUE,
    "knowledge_gap":  ItemKind.FACT,
    "best_practice":  ItemKind.LESSON,
    # ERRORS.md — all treated as FACT
    "error":          ItemKind.FACT,
    # FEATURE_REQUESTS.md
    "feature":        ItemKind.VALUE,
    "request":        ItemKind.VALUE,
}


# ─── Parser ──────────────────────────────────────────────────────────────────

# Skill canonical format: ## [LRN-20260329-001] correction
ENTRY_START_RE = re.compile(r"^## \[([A-Z]+-\d{8}-[A-Z0-9]+)\] (\S+)")
# Legacy/other format: ## 2026-03-08 — Title  (date-stamped, no ID)
ENTRY_DATE_RE  = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*[-—]\s*(.+)")
PRIORITY_RE    = re.compile(r"^\*\*Priority\*\*:\s*(\S+)", re.IGNORECASE)
STATUS_RE      = re.compile(r"^\*\*Status\*\*:\s*(\S+)",   re.IGNORECASE)
AREA_RE        = re.compile(r"^\*\*Area\*\*:\s*(\S+)",    re.IGNORECASE)
SUMMARY_RE     = re.compile(r"^### Summary\s*\n(.+?)(?=\n###|\n---|\n\*\*|$)", re.IGNORECASE | re.DOTALL)
METADATA_KEY_RE = re.compile(r"^- \*\*(\w[\w ]+?)\*\*:\s*(.+)")


def _parse_body(body: str) -> dict:
    """Extract structured fields from entry body. Returns dict of extras."""
    extras = {}
    for line in body.splitlines():
        m = METADATA_KEY_RE.match(line.strip())
        if m:
            extras[m.group(1).lower().replace(" ", "_")] = m.group(2).strip()
    # Summary (may contain multiple lines)
    sm = SUMMARY_RE.search(body)
    if sm:
        extras["summary"] = sm.group(1).strip()
    return extras


def _parse_file(path: Path, seen_ids: set[str]) -> list[Item]:
    """Parse one .learnings file, yielding Items for never-before-seen entries."""
    if not path.exists():
        return []

    items = []
    content = path.read_text()
    current_id: Optional[str] = None
    current_category = "insight"
    current_body_lines: list[str] = []
    in_body = False

    def _flush():
        nonlocal current_id, current_category, current_body_lines
        if not current_id or current_id in seen_ids:
            current_id = None
            current_body_lines = []
            return
        body = "\n".join(current_body_lines)
        extras = _parse_body(body)
        kind = CATEGORY_KIND_MAP.get(current_category, ItemKind.VALUE)
        # Priority from entry → confidence override
        # If the entry has an explicit priority, use it; otherwise use category-based default
        priority_override = extras.get("priority", "").lower()
        if priority_override in {"critical", "high", "medium", "low"}:
            confidence_map = {"critical": 0.95, "high": 0.85, "medium": 0.7, "low": 0.5}
            confidence = confidence_map[priority_override]
        else:
            # Category-based default for entries without explicit priority
            category_default = {"correction": 0.85, "insight": 0.8, "knowledge_gap": 0.85,
                               "best_practice": 0.8, "error": 0.9, "feature": 0.7, "request": 0.7}
            confidence = category_default.get(current_category, 0.7)
        item_id = f"subc_{current_id.lower().replace('-', '_')}"
        text = extras.get("summary", body[:200].strip())
        if not text:
            text = f"[{current_id}] {current_category}"
        links = ItemLinks()
        if "area" in extras:
            links.topics.append(extras["area"])
        if "related_files" in extras:
            for f in extras["related_files"].split(","):
                f = f.strip().strip("`")
                if f:
                    links.values.append(f)
        source = ItemSource(type="learnings_bridge", timestamp=_utc_now())
        reinforcement = ItemReinforcement(
            count=1,
            first_at=_utc_now(),
            last_at=_utc_now(),
        )
        item = Item(
            id=item_id,
            layer=ItemLayer.PENDING,
            kind=kind,
            text=text[:1500],
            weight=0.5,
            confidence=confidence,
            freshness=1.0,
            source=source,
            links=links,
            reinforcement=reinforcement,
            notes=body[:1000] if body else "",
        )
        items.append(item)
        current_id = None
        current_body_lines = []

    entry_counter = 0

    for line in content.splitlines():
        m = ENTRY_START_RE.match(line)
        date_m = ENTRY_DATE_RE.match(line)
        if m:
            _flush()
            current_id = m.group(1)   # e.g. "LRN-20260329-001"
            current_category = m.group(2).lower()
            in_body = True
            current_body_lines = []
        elif date_m:
            _flush()
            # Generate a stable ID from date + title hash
            date_part = date_m.group(1).replace("-", "")  # "20260308"
            title_slug = re.sub(r'[^a-z0-9]', '', date_m.group(2).lower())[:20]
            entry_counter += 1
            current_id = f"LRN-{date_part}-{entry_counter:03d}"
            current_category = "insight"
            in_body = True
            current_body_lines = []
        elif in_body and line.strip() == "---":
            _flush()
            in_body = False
        elif in_body:
            current_body_lines.append(line)

    _flush()
    return items


def _load_tracker() -> dict:
    if TRACKER_FILE.exists():
        import json
        return json.loads(TRACKER_FILE.read_text())
    return {}


def _save_tracker(tracker: dict) -> None:
    import json
    TRACKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    TRACKER_FILE.write_text(json.dumps(tracker, indent=2))


# ─── Public API ───────────────────────────────────────────────────────────────

def scan_learnings(base_path: Optional[Path] = None) -> dict:
    """Scan .learnings/ files and queue new entries to subconscious.

    Idempotent — each entry is processed exactly once.

    Returns:
        dict with keys: scanned (files checked), queued (items added), skipped (already seen)
    """
    base = base_path or DEFAULT_BASE_PATH
    tracker = _load_tracker()
    seen_ids: set[str] = set(tracker.get("seen_ids", []))
    last_mtimes: dict = tracker.get("last_mtimes", {})

    files = {
        "learnings":  LEARNINGS_DIR / "LEARNINGS.md",
        "errors":     LEARNINGS_DIR / "ERRORS.md",
        "features":   LEARNINGS_DIR / "FEATURE_REQUESTS.md",
    }

    result = {"scanned": list(files.keys()), "queued": 0, "skipped": 0, "errors": []}

    for name, path in files.items():
        if not path.exists():
            continue

        current_mtime = str(path.stat().st_mtime)
        last_mtime = last_mtimes.get(name, "0")

        # Skip if file hasn't changed since last scan
        if current_mtime == last_mtime:
            continue

        try:
            items = _parse_file(path, seen_ids)
        except Exception as e:
            result["errors"].append(f"{name}: {e}")
            continue

        for item in items:
            from .intake import queue_pending
            ok = queue_pending(item, base_path=base)
            if ok:
                # Store raw ID without prefix (e.g. "LRN-20260308-001")
                raw_id = item.id.replace("subc_", "").upper()
                seen_ids.add(raw_id)
                result["queued"] += 1
            else:
                result["skipped"] += 1

        # Update tracker
        last_mtimes[name] = current_mtime
        tracker["last_mtimes"] = last_mtimes
        tracker["seen_ids"] = list(seen_ids)
        _save_tracker(tracker)

    result["errors"] = result["errors"] or None
    return result
