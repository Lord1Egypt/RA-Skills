#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Optional

from super_memori_common import MEMORY_DIR, WORKSPACE, now_iso, read_state, write_state, sha256_text

HYGIENE_DIR = MEMORY_DIR / "semantic" / "system-hygiene"
HYGIENE_FINDINGS = HYGIENE_DIR / "findings.md"
HYGIENE_CLEANUP_PLANS = HYGIENE_DIR / "cleanup-plans.md"
HYGIENE_RECOVERY = HYGIENE_DIR / "recovery-lessons.md"
SYSTEM_HYGIENE_MIN_BYTES = int(os.environ.get("SUPER_MEMORI_HYGIENE_MIN_BYTES", str(10 * 1024 * 1024)))
SYSTEM_HYGIENE_SCAN_ROOTS = [str(WORKSPACE), str(Path.home() / ".cache"), str(Path.home() / ".local" / "share")]


def _human_size(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024.0 or unit == units[-1]:
            return f"{size:.1f}{unit}" if unit != "B" else f"{int(size)}B"
        size /= 1024.0
    return f"{int(size)}B"


def _path_owner_guess(path: Path) -> str:
    low = str(path).casefold()
    if "openclaw" in low:
        return "openclaw"
    if "cache" in low:
        return "cache"
    if "log" in low:
        return "log"
    if "backup" in low or "bak" in low:
        return "backup"
    return "unknown"


def _candidate_category(path: Path) -> str:
    low = path.name.casefold()
    full = str(path).casefold()
    if any(low.endswith(ext) for ext in [".log", ".out", ".err"]) or "/log" in full:
        return "stale-log"
    if any(token in low for token in ["backup", ".bak", ".old", ".orig", ".copy"]) or "/backup" in full:
        return "stale-backup"
    if any(token in full for token in ["cache", ".cache", "tmp", "temp", "/tmp/"]):
        return "cache-or-temp"
    if any(token in full for token in ["index-state", "memory.db", "telemetry.db"]):
        return "memory-index-health"
    if any(token in full for token in [".learnings", "semantic/skill-memory"]):
        return "openclaw-runtime-health"
    return "disk-bloat"


def system_hygiene_status() -> dict:
    state = read_state()
    return {
        "findings_exists": HYGIENE_FINDINGS.exists(),
        "cleanup_plans_exists": HYGIENE_CLEANUP_PLANS.exists(),
        "recovery_exists": HYGIENE_RECOVERY.exists(),
        "last_scanned_at": state.get("system_hygiene_last_scanned_at"),
        "findings_count": int(state.get("system_hygiene_findings_count", 0) or 0),
        "scan_roots": state.get("system_hygiene_scan_roots", SYSTEM_HYGIENE_SCAN_ROOTS),
        "fresh": HYGIENE_FINDINGS.exists() and bool(state.get("system_hygiene_last_scanned_at")),
        "validation_state": "current" if HYGIENE_FINDINGS.exists() else "stale",
    }


def _scan_tree(root: Path, *, min_bytes: int) -> list[dict]:
    findings: list[dict] = []
    if not root.exists():
        return findings
    for path in sorted(root.rglob("*")):
        try:
            if path.is_dir():
                continue
            if len(path.relative_to(root).parts) > 6:
                continue
            stat = path.stat()
            size = stat.st_size
            age_days = round(max(0.0, time.time() - stat.st_mtime) / 86400.0, 2)
            category = _candidate_category(path)
            if size < min_bytes and category not in {"memory-index-health", "openclaw-runtime-health"}:
                continue
            if category == "stale-log" and age_days < 7:
                continue
            if category == "stale-backup" and age_days < 14:
                continue
            full = str(path).casefold()
            findings.append({
                "finding_id": sha256_text(f"{path}:{stat.st_mtime}:{size}")[:16],
                "category": category,
                "path": str(path),
                "size": size,
                "size_human": _human_size(size),
                "age": age_days,
                "owner": _path_owner_guess(path),
                "source": str(root),
                "why_it_matters": f"{category} may consume disk space or confuse OpenClaw hygiene checks",
                "affects_openclaw": any(tok in full for tok in ["openclaw", "memory", ".learnings", "skills"]),
                "affects_os": category in {"stale-log", "stale-backup", "cache-or-temp", "disk-bloat"},
                "safe_action": "run index-memory.sh / refresh index state" if category == "memory-index-health" else ("rotate or archive after review" if category == "stale-log" else ("review duplicate backup before deletion" if category == "stale-backup" else "cleanup only if confirmed disposable")),
                "dangerous_action": "delete without confirmation" if category in {"stale-backup", "stale-log", "cache-or-temp"} else "touch without audit",
                "review_required": category != "memory-index-health",
                "confidence": 0.72 if category != "disk-bloat" else 0.56,
                "freshness": "current",
                "validation_state": "discovered",
                "last_seen": now_iso(),
                "recovery_if_removed_wrongly": f"restore from backup if {category} was deleted incorrectly",
            })
        except Exception:
            continue
    return findings


def scan_system_hygiene(*, roots: Optional[list[str]] = None, min_bytes: int = SYSTEM_HYGIENE_MIN_BYTES) -> dict:
    HYGIENE_DIR.mkdir(parents=True, exist_ok=True)
    scan_roots = [Path(r) for r in roots] if roots else [Path(r) for r in SYSTEM_HYGIENE_SCAN_ROOTS]
    findings: list[dict] = []
    for root in scan_roots:
        findings.extend(_scan_tree(root, min_bytes=min_bytes))
    findings.sort(key=lambda item: (item["category"], -(item["size"] or 0), item["path"]))
    state = read_state()
    state["system_hygiene_last_scanned_at"] = now_iso()
    state["system_hygiene_findings_count"] = len(findings)
    state["system_hygiene_scan_roots"] = [str(r) for r in scan_roots]
    write_state(state)
    HYGIENE_FINDINGS.write_text("# System Hygiene Findings\n#tags: system-hygiene, disk-bloat, stale-backups, stale-logs\n\n" + "\n".join(json.dumps(item, ensure_ascii=False) for item in findings), encoding="utf-8")
    return {
        "status": "ok",
        "findings_count": len(findings),
        "findings": findings[:200],
        "scan_roots": [str(r) for r in scan_roots],
        "last_scanned_at": state["system_hygiene_last_scanned_at"],
        "paths": {"findings": str(HYGIENE_FINDINGS), "cleanup": str(HYGIENE_CLEANUP_PLANS), "recovery": str(HYGIENE_RECOVERY)},
    }


def plan_hygiene_cleanup(*, allow_destructive: bool = False) -> dict:
    status = system_hygiene_status()
    findings = []
    if HYGIENE_FINDINGS.exists():
        for line in HYGIENE_FINDINGS.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("{"):
                try:
                    findings.append(json.loads(line))
                except Exception:
                    continue
    plans = []
    for finding in findings[:100]:
        plans.append({
            "plan_id": sha256_text(finding.get("finding_id", finding.get("path", "")))[:16],
            "finding_id": finding.get("finding_id"),
            "category": finding.get("category"),
            "path": finding.get("path"),
            "risk_level": "high" if finding.get("review_required") else "low",
            "safe_action": finding.get("safe_action", "review"),
            "dangerous_action": finding.get("dangerous_action", "touch without audit"),
            "auto_fix": bool(allow_destructive and not finding.get("review_required")),
            "requires_confirmation": not allow_destructive or bool(finding.get("review_required")),
            "recovery_if_removed_wrongly": finding.get("recovery_if_removed_wrongly"),
            "validation_state": finding.get("validation_state", "discovered"),
            "freshness": finding.get("freshness", "current"),
        })
    HYGIENE_CLEANUP_PLANS.write_text("# System Hygiene Cleanup Plans\n#tags: system-hygiene, cleanup, recovery\n\n" + "\n".join(json.dumps(item, ensure_ascii=False) for item in plans), encoding="utf-8")
    return {"status": "ok", "plans": plans, "requires_confirmation": any(p["requires_confirmation"] for p in plans), "scan_status": status}


def record_hygiene_recovery(note: str) -> dict:
    HYGIENE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = now_iso()
    entry = {"timestamp": timestamp, "note": note}
    existing = HYGIENE_RECOVERY.read_text(encoding="utf-8", errors="ignore") if HYGIENE_RECOVERY.exists() else "# System Hygiene Recovery Lessons\n#tags: system-hygiene, recovery, lessons\n\n"
    HYGIENE_RECOVERY.write_text(existing + json.dumps(entry, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"status": "ok", "last_recorded_at": timestamp, "path": str(HYGIENE_RECOVERY)}
