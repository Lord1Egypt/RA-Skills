#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sqlite3
import subprocess
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

def _skill_ops():
    from skill_operational_memory import (
        compile_skill_lessons,
        installed_skill_records,
        refresh_skill_operational_memory,
        skill_operational_decision,
        skill_operational_memory_audit,
        skill_operational_memory_status,
        skill_operational_recall,
        skill_recall_gate,
    )
    return {
        "compile_skill_lessons": compile_skill_lessons,
        "installed_skill_records": installed_skill_records,
        "refresh_skill_operational_memory": refresh_skill_operational_memory,
        "skill_operational_decision": skill_operational_decision,
        "skill_operational_memory_audit": skill_operational_memory_audit,
        "skill_operational_memory_status": skill_operational_memory_status,
        "skill_operational_recall": skill_operational_recall,
        "skill_recall_gate": skill_recall_gate,
    }

def compile_skill_lessons():
    return _skill_ops()["compile_skill_lessons"]()


def installed_skill_records():
    return _skill_ops()["installed_skill_records"]()


def refresh_skill_operational_memory():
    return _skill_ops()["refresh_skill_operational_memory"]()


def skill_operational_decision(query: str):
    return _skill_ops()["skill_operational_decision"](query)


def skill_operational_memory_audit():
    return _skill_ops()["skill_operational_memory_audit"]()


def skill_operational_memory_status():
    return _skill_ops()["skill_operational_memory_status"]()


def skill_operational_recall(query: str, limit: int = 3):
    return _skill_ops()["skill_operational_recall"](query, limit=limit)


def skill_recall_gate(query: str):
    return _skill_ops()["skill_recall_gate"](query)

def _hygiene_ops():
    from system_hygiene_memory import (
        plan_hygiene_cleanup,
        record_hygiene_recovery,
        scan_system_hygiene,
        system_hygiene_status,
    )
    return {
        "plan_hygiene_cleanup": plan_hygiene_cleanup,
        "record_hygiene_recovery": record_hygiene_recovery,
        "scan_system_hygiene": scan_system_hygiene,
        "system_hygiene_status": system_hygiene_status,
    }


def scan_system_hygiene(*args, **kwargs):
    return _hygiene_ops()["scan_system_hygiene"](*args, **kwargs)


def plan_hygiene_cleanup(*args, **kwargs):
    return _hygiene_ops()["plan_hygiene_cleanup"](*args, **kwargs)


def record_hygiene_recovery(*args, **kwargs):
    return _hygiene_ops()["record_hygiene_recovery"](*args, **kwargs)


def system_hygiene_status(*args, **kwargs):
    return _hygiene_ops()["system_hygiene_status"](*args, **kwargs)

def _change_ops():
    from agent_change_memory import (
        audit_change_memory,
        build_change_recall_bundle,
        build_rollback_candidate,
        detect_conflict_with_prior_change,
        detect_repeat_action_risk,
        detect_unverified_change,
        query_change_history,
        query_config_history,
        query_current_known_state,
        query_package_history,
        query_service_history,
        record_agent_change,
        record_failed_change,
        record_reverted_change,
        record_hot_change_event,
        update_hot_change_event_status,
        reconcile_routine_change_history,
        query_recent_hot_changes,
        query_unverified_recent_changes,
        detect_interrupted_change_sequence,
        build_hot_recovery_bundle,
        compact_hot_buffer,
        hot_buffer_health_status,
    )
    return {
        "audit_change_memory": audit_change_memory,
        "build_change_recall_bundle": build_change_recall_bundle,
        "build_rollback_candidate": build_rollback_candidate,
        "detect_conflict_with_prior_change": detect_conflict_with_prior_change,
        "detect_repeat_action_risk": detect_repeat_action_risk,
        "detect_unverified_change": detect_unverified_change,
        "query_change_history": query_change_history,
        "query_config_history": query_config_history,
        "query_current_known_state": query_current_known_state,
        "query_package_history": query_package_history,
        "query_service_history": query_service_history,
        "record_agent_change": record_agent_change,
        "record_failed_change": record_failed_change,
        "record_reverted_change": record_reverted_change,
        "record_hot_change_event": record_hot_change_event,
        "update_hot_change_event_status": update_hot_change_event_status,
        "reconcile_routine_change_history": reconcile_routine_change_history,
        "query_recent_hot_changes": query_recent_hot_changes,
        "query_unverified_recent_changes": query_unverified_recent_changes,
        "detect_interrupted_change_sequence": detect_interrupted_change_sequence,
        "build_hot_recovery_bundle": build_hot_recovery_bundle,
        "compact_hot_buffer": compact_hot_buffer,
        "hot_buffer_health_status": hot_buffer_health_status,
    }


def record_agent_change(*args, **kwargs):
    return _change_ops()["record_agent_change"](*args, **kwargs)


def record_failed_change(*args, **kwargs):
    return _change_ops()["record_failed_change"](*args, **kwargs)


def record_reverted_change(*args, **kwargs):
    return _change_ops()["record_reverted_change"](*args, **kwargs)


def query_change_history(*args, **kwargs):
    return _change_ops()["query_change_history"](*args, **kwargs)


def query_current_known_state(*args, **kwargs):
    return _change_ops()["query_current_known_state"](*args, **kwargs)


def query_package_history(*args, **kwargs):
    return _change_ops()["query_package_history"](*args, **kwargs)


def query_service_history(*args, **kwargs):
    return _change_ops()["query_service_history"](*args, **kwargs)


def query_config_history(*args, **kwargs):
    return _change_ops()["query_config_history"](*args, **kwargs)


def build_change_recall_bundle(*args, **kwargs):
    return _change_ops()["build_change_recall_bundle"](*args, **kwargs)


def detect_conflict_with_prior_change(*args, **kwargs):
    return _change_ops()["detect_conflict_with_prior_change"](*args, **kwargs)


def detect_repeat_action_risk(*args, **kwargs):
    return _change_ops()["detect_repeat_action_risk"](*args, **kwargs)


def detect_unverified_change(*args, **kwargs):
    return _change_ops()["detect_unverified_change"](*args, **kwargs)


def build_rollback_candidate(*args, **kwargs):
    return _change_ops()["build_rollback_candidate"](*args, **kwargs)


def audit_change_memory(*args, **kwargs):
    return _change_ops()["audit_change_memory"](*args, **kwargs)


def record_hot_change_event(*args, **kwargs):
    return _change_ops()["record_hot_change_event"](*args, **kwargs)


def update_hot_change_event_status(*args, **kwargs):
    return _change_ops()["update_hot_change_event_status"](*args, **kwargs)


def reconcile_routine_change_history(*args, **kwargs):
    return _change_ops()["reconcile_routine_change_history"](*args, **kwargs)


def query_recent_hot_changes(*args, **kwargs):
    return _change_ops()["query_recent_hot_changes"](*args, **kwargs)


def query_unverified_recent_changes(*args, **kwargs):
    return _change_ops()["query_unverified_recent_changes"](*args, **kwargs)


def detect_interrupted_change_sequence(*args, **kwargs):
    return _change_ops()["detect_interrupted_change_sequence"](*args, **kwargs)


def build_hot_recovery_bundle(*args, **kwargs):
    return _change_ops()["build_hot_recovery_bundle"](*args, **kwargs)


def compact_hot_buffer(*args, **kwargs):
    return _change_ops()["compact_hot_buffer"](*args, **kwargs)


def hot_buffer_health_status(*args, **kwargs):
    return _change_ops()["hot_buffer_health_status"](*args, **kwargs)

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", str(Path.home() / ".openclaw/workspace"))).expanduser()
SKILL_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = WORKSPACE / "memory"
LEARNINGS_DIR = WORKSPACE / ".learnings"
INDEX_STATE_DIR = MEMORY_DIR / "index-state"
QUEUE_DIR = MEMORY_DIR / "queue"
DB_PATH = INDEX_STATE_DIR / "memory.db"
STATE_JSON = INDEX_STATE_DIR / "state.json"
TELEMETRY_DB = INDEX_STATE_DIR / "telemetry.db"
QDRANT_URL = os.environ.get("SUPER_MEMORI_QDRANT_URL", "http://127.0.0.1:6333")
QDRANT_COLLECTION = os.environ.get("SUPER_MEMORI_QDRANT_COLLECTION", "super_memori")
EMBED_MODEL = os.environ.get("SUPER_MEMORI_EMBED_MODEL", "intfloat/multilingual-e5-small")
SEMANTIC_DAEMON_HOST = os.environ.get("SUPER_MEMORI_SEMANTIC_DAEMON_HOST", "127.0.0.1")
SEMANTIC_DAEMON_PORT = int(os.environ.get("SUPER_MEMORI_SEMANTIC_DAEMON_PORT", "8765"))
SEMANTIC_DAEMON_URL = f"http://{SEMANTIC_DAEMON_HOST}:{SEMANTIC_DAEMON_PORT}"
SEMANTIC_DAEMON_HEALTH_PATH = "/health"
SEMANTIC_DAEMON_EMBED_PATH = "/embed"
SEMANTIC_DAEMON_SEARCH_PATH = "/semantic-search"
HYGIENE_DIR = MEMORY_DIR / "semantic" / "system-hygiene"
HYGIENE_FINDINGS = HYGIENE_DIR / "findings.md"
HYGIENE_CLEANUP_PLANS = HYGIENE_DIR / "cleanup-plans.md"
HYGIENE_RECOVERY = HYGIENE_DIR / "recovery-lessons.md"
SYSTEM_HYGIENE_MIN_BYTES = int(os.environ.get("SUPER_MEMORI_HYGIENE_MIN_BYTES", str(10 * 1024 * 1024)))
SYSTEM_HYGIENE_SCAN_ROOTS = [str(WORKSPACE), str(Path.home() / ".cache"), str(Path.home() / ".local" / "share")]

MEMORY_TYPES = ["episodic", "semantic", "procedural", "learning", "buffer"]
VALID_LEARNING_TYPES = {"error", "correction", "lesson", "insight"}
VALID_RELATION_KEYS = ["supersedes", "refines", "confirms", "contradicts", "extends"]
CANONICAL_RELATION_TARGET_PREFIXES = ("learn:", "chunk:", "path:")
CANONICAL_DAILY_NOTE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
NONCANONICAL_SEMANTIC_SUBDIRS = {"agent-change-memory", "skill-memory", "system-hygiene"}
MAX_LEARNING_CHARS = 4000
CHUNK_TARGET_CHARS = 1200
CHUNK_OVERLAP_CHARS = 150
LEXICAL_STALE_GRACE_SECONDS = 5
SEMANTIC_STALE_GRACE_SECONDS = 5
RRF_K = 60
SEMANTIC_SCORE_THRESHOLD = float(os.environ.get("SUPER_MEMORI_SEMANTIC_MIN_SCORE", "0.35"))
SEMANTIC_TOP_K = int(os.environ.get("SUPER_MEMORI_SEMANTIC_TOP_K", "20"))
SEMANTIC_BATCH_SIZE = int(os.environ.get("SUPER_MEMORI_EMBED_BATCH_SIZE", "16"))
TEMPORAL_DECAY_DAYS = float(os.environ.get("SUPER_MEMORI_TEMPORAL_DECAY_DAYS", "180"))
SYSTEM_HYGIENE_MIN_BYTES = int(os.environ.get("SUPER_MEMORI_HYGIENE_MIN_BYTES", str(10 * 1024 * 1024)))
SYSTEM_HYGIENE_SCAN_ROOTS = [str(WORKSPACE), str(Path.home() / ".cache"), str(Path.home() / ".local" / "share")]

_EMBED_MODEL_CACHE = None

HOST_PROFILE_ENV = "SUPER_MEMORI_PROFILE"

HOST_PROFILE_STANDARD = {
    "name": "standard",
    "chunk_target_chars": 1200,
    "chunk_overlap_chars": 150,
    "retrieval": {
        "lexical_top_k": 20,
        "semantic_top_k": 20,
        "fusion_multiplier": 4,
        "rerank_limit": 10,
        "diversity_cap": 2,
    },
    "semantic_batch_size": 16,
    "audit_scroll_limit": 256,
    "queue_backlog_warn": 500,
}

HOST_PROFILE_MAX = {
    "name": "max",
    "chunk_target_chars": 900,
    "chunk_overlap_chars": 180,
    "retrieval": {
        "lexical_top_k": 50,
        "semantic_top_k": 50,
        "fusion_multiplier": 8,
        "rerank_limit": 30,
        "diversity_cap": 3,
    },
    "semantic_batch_size": 32,
    "audit_scroll_limit": 1024,
    "queue_backlog_warn": 2000,
}


def _read_int_file(path: Path) -> Optional[int]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore").strip()
    except Exception:
        return None
    if not text:
        return None
    match = re.search(r"([0-9]+)", text)
    if not match:
        return None
    value = int(match.group(1))
    lower = text.casefold()
    if "g" in lower and "b" in lower:
        return value * 1024 * 1024 * 1024
    if "m" in lower and "b" in lower:
        return value * 1024 * 1024
    if "k" in lower and "b" in lower:
        return value * 1024
    return value


def hardware_snapshot() -> dict:
    cpu_count = os.cpu_count() or 1
    mem_total_gib = 0.0
    meminfo = Path("/proc/meminfo")
    try:
        raw = meminfo.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        raw = ""
    for line in raw.splitlines():
        if line.startswith("MemTotal:"):
            try:
                mem_kib = int(line.split()[1])
                mem_total_gib = round(mem_kib / 1024 / 1024, 2)
            except Exception:
                mem_total_gib = 0.0
            break
    l3_cache_mib = None
    l3_path = Path("/sys/devices/system/cpu/cpu0/cache/index3/size")
    if l3_path.exists():
        try:
            l3_cache_mib = _read_int_file(l3_path)
            if l3_cache_mib is not None and l3_cache_mib > 1024:
                l3_cache_mib = round(l3_cache_mib / 1024 / 1024, 2)
            elif l3_cache_mib is not None and l3_cache_mib > 1024 * 1024:
                l3_cache_mib = round(l3_cache_mib / 1024 / 1024, 2)
        except Exception:
            l3_cache_mib = None
    numa_nodes = None
    numa_path = Path("/sys/devices/system/node")
    if numa_path.exists():
        try:
            numa_nodes = len([p for p in numa_path.iterdir() if p.name.startswith("node")])
        except Exception:
            numa_nodes = None
    model_name = None
    try:
        cpuinfo = Path("/proc/cpuinfo").read_text(encoding="utf-8", errors="ignore")
        for line in cpuinfo.splitlines():
            if line.lower().startswith("model name"):
                model_name = line.split(":", 1)[1].strip()
                break
    except Exception:
        model_name = None
    return {
        "cpu_count": cpu_count,
        "memory_total_gib": mem_total_gib,
        "l3_cache_mib": l3_cache_mib,
        "numa_nodes": numa_nodes,
        "model_name": model_name,
    }


def detect_host_profile(snapshot: Optional[dict] = None) -> str:
    override = os.environ.get(HOST_PROFILE_ENV, "").strip().casefold()
    if override in {"standard", "max"}:
        return override
    snapshot = snapshot or hardware_snapshot()
    cpu_count = int(snapshot.get("cpu_count") or 1)
    memory_total_gib = float(snapshot.get("memory_total_gib") or 0.0)
    if cpu_count >= 8 and memory_total_gib >= 64.0:
        return "max"
    return "standard"


def host_profile_config(snapshot: Optional[dict] = None) -> dict:
    snapshot = snapshot or hardware_snapshot()
    profile = detect_host_profile(snapshot)
    base = HOST_PROFILE_MAX if profile == "max" else HOST_PROFILE_STANDARD
    return {
        **base,
        "hardware": snapshot,
        "detected_profile": profile,
        "equipped_candidate": profile == "max",
    }


def host_profile_status(snapshot: Optional[dict] = None) -> dict:
    config = host_profile_config(snapshot)
    hardware = config["hardware"]
    return {
        "detected_profile": config["detected_profile"],
        "equipped_candidate": config["equipped_candidate"],
        "cpu_count": hardware.get("cpu_count"),
        "memory_total_gib": hardware.get("memory_total_gib"),
        "l3_cache_mib": hardware.get("l3_cache_mib"),
        "numa_nodes": hardware.get("numa_nodes"),
        "model_name": hardware.get("model_name"),
        "chunk_target_chars": config["chunk_target_chars"],
        "chunk_overlap_chars": config["chunk_overlap_chars"],
        "retrieval": config["retrieval"],
        "semantic_batch_size": config["semantic_batch_size"],
        "audit_scroll_limit": config["audit_scroll_limit"],
        "queue_backlog_warn": config["queue_backlog_warn"],
    }


def pattern_mining_status() -> dict:
    report_path = SKILL_DIR / "reports" / "pattern-report.json"
    report_exists = report_path.exists()
    latest_learning = None
    if LEARNINGS_DIR.exists():
        for path in sorted(LEARNINGS_DIR.rglob("*.md")):
            try:
                mtime = path.stat().st_mtime
            except Exception:
                continue
            latest_learning = mtime if latest_learning is None else max(latest_learning, mtime)
    report_fresh = None
    if report_exists and latest_learning is not None:
        try:
            report_fresh = report_path.stat().st_mtime >= latest_learning
        except Exception:
            report_fresh = None
    return {
        "report_path": str(report_path),
        "report_exists": report_exists,
        "report_fresh": report_fresh,
        "latest_learning_mtime": latest_learning,
    }


def ensure_dirs() -> None:
    INDEX_STATE_DIR.mkdir(parents=True, exist_ok=True)
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    (QUEUE_DIR / "processed").mkdir(parents=True, exist_ok=True)
    LEARNINGS_DIR.mkdir(parents=True, exist_ok=True)
    HYGIENE_DIR.mkdir(parents=True, exist_ok=True)
    HYGIENE_DIR.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def system_hygiene_status() -> dict:
    state = read_state()
    hygiene_dir = MEMORY_DIR / "semantic" / "system-hygiene"
    findings = hygiene_dir / "findings.md"
    cleanup = hygiene_dir / "cleanup-plans.md"
    recovery = hygiene_dir / "recovery-lessons.md"
    return {
        "findings_exists": findings.exists(),
        "cleanup_plans_exists": cleanup.exists(),
        "recovery_exists": recovery.exists(),
        "last_scanned_at": state.get("system_hygiene_last_scanned_at"),
        "findings_count": int(state.get("system_hygiene_findings_count", 0) or 0),
        "scan_roots": state.get("system_hygiene_scan_roots", SYSTEM_HYGIENE_SCAN_ROOTS),
        "fresh": findings.exists() and bool(state.get("system_hygiene_last_scanned_at")),
        "validation_state": "current" if findings.exists() else "stale",
    }


def scan_system_hygiene(*, roots: Optional[list[str]] = None, min_bytes: int = SYSTEM_HYGIENE_MIN_BYTES) -> dict:
    ensure_dirs()
    hygiene_dir = MEMORY_DIR / "semantic" / "system-hygiene"
    hygiene_dir.mkdir(parents=True, exist_ok=True)
    findings_path = hygiene_dir / "findings.md"
    cleanup_path = hygiene_dir / "cleanup-plans.md"
    recovery_path = hygiene_dir / "recovery-lessons.md"
    scan_roots = [Path(r) for r in roots] if roots else [Path(r) for r in SYSTEM_HYGIENE_SCAN_ROOTS]
    findings: list[dict] = []
    for root in scan_roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            try:
                if path.is_dir():
                    continue
                if len(path.relative_to(root).parts) > 6:
                    continue
                stat = path.stat()
                size = stat.st_size
                age_days = round(max(0.0, time.time() - stat.st_mtime) / 86400.0, 2)
                category = "disk-bloat"
                low = path.name.casefold()
                full = str(path).casefold()
                if any(low.endswith(ext) for ext in [".log", ".out", ".err"]) or "/log" in full:
                    category = "stale-log"
                elif any(token in low for token in ["backup", ".bak", ".old", ".orig", ".copy"]) or "/backup" in full:
                    category = "stale-backup"
                elif any(token in full for token in ["cache", ".cache", "tmp", "temp", "/tmp/"]):
                    category = "cache-or-temp"
                elif any(token in full for token in ["index-state", "memory.db", "telemetry.db"]):
                    category = "memory-index-health"
                elif any(token in full for token in [".learnings", "semantic/skill-memory"]):
                    category = "openclaw-runtime-health"
                if size < min_bytes and category not in {"memory-index-health", "openclaw-runtime-health"}:
                    continue
                if category == "stale-log" and age_days < 7:
                    continue
                if category == "stale-backup" and age_days < 14:
                    continue
                findings.append({
                    "finding_id": _hash_text(f"{path}:{stat.st_mtime}:{size}")[:16],
                    "category": category,
                    "path": str(path),
                    "size": size,
                    "age": age_days,
                    "owner": "openclaw" if "openclaw" in full else ("log" if "log" in full else ("backup" if "backup" in full else "unknown")),
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
    state = read_state()
    state["system_hygiene_last_scanned_at"] = now_iso()
    state["system_hygiene_findings_count"] = len(findings)
    state["system_hygiene_scan_roots"] = [str(r) for r in scan_roots]
    write_state(state)
    try:
        from system_hygiene_memory import scan_system_hygiene, plan_hygiene_cleanup, record_hygiene_recovery, system_hygiene_status  # noqa: F401
    except Exception:
        pass


def read_state() -> dict:
    ensure_dirs()
    if STATE_JSON.exists():
        try:
            return json.loads(STATE_JSON.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def write_state(state: dict) -> None:
    ensure_dirs()
    tmp = STATE_JSON.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(STATE_JSON)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _is_canonical_daily_note(path: Path) -> bool:
    return path.parent == MEMORY_DIR and bool(CANONICAL_DAILY_NOTE_RE.match(path.name))



def _is_noncanonical_semantic_path(path: Path) -> bool:
    try:
        rel = path.relative_to(MEMORY_DIR / "semantic")
    except Exception:
        return False
    return bool(rel.parts) and rel.parts[0] in NONCANONICAL_SEMANTIC_SUBDIRS



def canonical_memory_files() -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    if MEMORY_DIR.exists():
        for path in sorted(MEMORY_DIR.glob("*.md")):
            if _is_canonical_daily_note(path):
                files.append(("episodic", path))
        for mem_type in ["episodic", "semantic", "procedural"]:
            d = MEMORY_DIR / mem_type
            if d.exists():
                for path in sorted(d.rglob("*.md")):
                    if mem_type == "semantic" and _is_noncanonical_semantic_path(path):
                        continue
                    files.append((mem_type, path))
        buffer = MEMORY_DIR / "working-buffer.md"
        if buffer.exists():
            files.append(("buffer", buffer))
    if LEARNINGS_DIR.exists():
        for path in sorted(LEARNINGS_DIR.rglob("*.md")):
            files.append(("learning", path))
    memory_md = WORKSPACE / "MEMORY.md"
    if memory_md.exists():
        files.append(("semantic", memory_md))
    return files


def parse_iso_timestamp(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(value, fmt).timestamp()
        except Exception:
            continue
    return None


def newest_canonical_mtime() -> Optional[float]:
    newest: Optional[float] = None
    for _, path in canonical_memory_files():
        try:
            mtime = path.stat().st_mtime
        except Exception:
            continue
        newest = mtime if newest is None else max(newest, mtime)
    return newest


def lexical_index_stale(state: Optional[dict] = None) -> bool:
    state = state or read_state()
    indexed_at = parse_iso_timestamp(state.get("lexical_last_indexed_at"))
    if indexed_at is None:
        return True
    newest = newest_canonical_mtime()
    if newest is None:
        return False
    return newest > indexed_at + LEXICAL_STALE_GRACE_SECONDS


def semantic_index_stale(state: Optional[dict] = None) -> bool:
    state = state or read_state()
    indexed_at = parse_iso_timestamp(state.get("semantic_last_indexed_at"))
    if indexed_at is None:
        return True
    newest = newest_canonical_mtime()
    if newest is None:
        return False
    return newest > indexed_at + SEMANTIC_STALE_GRACE_SECONDS


def learning_text_exists(text: str, signature: str = "") -> Optional[Path]:
    needle = normalize_compare_text(text)
    sig = signature.strip().casefold()
    if not needle and not sig:
        return None
    if not LEARNINGS_DIR.exists():
        return None
    for path in sorted(LEARNINGS_DIR.rglob("*.md")):
        try:
            existing = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        existing_lc = existing.casefold()
        if needle and needle in normalize_compare_text(existing):
            return path
        if sig and f"- signature: {sig}" in existing_lc:
            return path
    return None


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip("\n")
    return text


def normalize_compare_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).casefold()


QUERY_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "did", "do", "does", "for", "from", "how", "i", "in", "is", "it",
    "last", "mention", "mentioned", "month", "now", "of", "on", "or", "the", "to", "was", "what", "when", "where",
    "who", "why", "with", "you", "your",
}


def informative_query_tokens(query: str) -> list[str]:
    tokens = re.findall(r"[\w-]+", (query or "").casefold())
    seen: set[str] = set()
    informative: list[str] = []
    for token in tokens:
        if len(token) < 3 or token in QUERY_STOPWORDS or token.isdigit():
            continue
        if token in seen:
            continue
        seen.add(token)
        informative.append(token)
    return informative


def semantic_path_penalty(source_path: str) -> float:
    lowered = (source_path or "").casefold()
    if "bootstrap" in lowered:
        return 0.85
    return 1.0


def query_anchor_multiplier(item: dict, *, query: str) -> float:
    tokens = informative_query_tokens(query)
    if not tokens:
        return 1.0
    blob = " ".join([
        str(item.get("source_path") or ""),
        str(item.get("snippet") or ""),
    ]).casefold()
    hits = sum(1 for token in tokens if token in blob)
    if hits <= 0:
        return 0.94
    coverage = hits / max(len(tokens), 1)
    return min(1.24, 1.0 + 0.16 * coverage + 0.04 * max(0, hits - 1))


def infer_memory_type(path: Path) -> str:
    try:
        resolved = path.resolve()
    except Exception:
        resolved = path
    try:
        if LEARNINGS_DIR in resolved.parents:
            return "learning"
    except Exception:
        pass
    parts = resolved.parts
    if "episodic" in parts:
        return "episodic"
    if "procedural" in parts:
        return "procedural"
    if resolved.name == "working-buffer.md":
        return "buffer"
    return "semantic"


def chunk_text(text: str, chunk_size: Optional[int] = None, overlap: Optional[int] = None) -> list[str]:
    chunk_size = int(chunk_size or effective_chunk_params()[0])
    overlap = int(overlap or effective_chunk_params()[1])
    text = text.strip()
    if not text:
        return []
    if overlap >= chunk_size:
        overlap = max(0, chunk_size // 4)
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = end - overlap
        if start >= end:
            break
    return chunks


def ensure_column(conn: sqlite3.Connection, table: str, column: str, sql_type: str, default_sql: str) -> None:
    existing = {row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
    if column not in existing:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {sql_type} DEFAULT {default_sql}")


def ensure_telemetry_db() -> sqlite3.Connection:
    ensure_dirs()
    conn = sqlite3.connect(TELEMETRY_DB)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS retrieval_events (
          event_id INTEGER PRIMARY KEY AUTOINCREMENT,
          created_at TEXT NOT NULL,
          event_type TEXT NOT NULL,
          query_text TEXT,
          mode_requested TEXT,
          mode_used TEXT,
          degraded INTEGER NOT NULL DEFAULT 0,
          payload_json TEXT NOT NULL DEFAULT '{}'
        )
        """
    )
    conn.commit()
    return conn


def log_retrieval_event(event_type: str, *, query_text: str, mode_requested: str, mode_used: str, degraded: bool, payload: Optional[dict] = None) -> None:
    conn = ensure_telemetry_db()
    conn.execute(
        "INSERT INTO retrieval_events(created_at, event_type, query_text, mode_requested, mode_used, degraded, payload_json) VALUES(?, ?, ?, ?, ?, ?, ?)",
        (now_iso(), event_type, query_text, mode_requested, mode_used, 1 if degraded else 0, json.dumps(payload or {}, ensure_ascii=False)),
    )
    conn.commit()


def list_promotion_candidates(limit: int = 10) -> list[dict]:
    conn = ensure_telemetry_db()
    rows = conn.execute(
        """
        SELECT event_type, COUNT(*) AS freq, MAX(created_at) AS last_seen
        FROM retrieval_events
        WHERE event_type IN ('retrieval_miss', 'stale_success', 'relation_traversal_hit')
        GROUP BY event_type
        ORDER BY freq DESC, last_seen DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    return [dict(row) for row in rows]


def effective_chunk_params() -> tuple[int, int]:
    profile = host_profile_config()
    return int(profile["chunk_target_chars"]), int(profile["chunk_overlap_chars"])


def chunk_text(text: str, chunk_size: Optional[int] = None, overlap: Optional[int] = None) -> list[str]:
    chunk_size = int(chunk_size or effective_chunk_params()[0])
    overlap = int(overlap or effective_chunk_params()[1])
    text = text.strip()
    if not text:
        return []
    if overlap >= chunk_size:
        overlap = max(0, chunk_size // 4)
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = end - overlap
        if start >= end:
            break
    return chunks


def ensure_db() -> sqlite3.Connection:
    ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS entries (
          entry_id TEXT PRIMARY KEY,
          source_path TEXT NOT NULL UNIQUE,
          memory_type TEXT NOT NULL,
          content_hash TEXT NOT NULL,
          tags_json TEXT NOT NULL DEFAULT '[]',
          created_at TEXT,
          updated_at TEXT,
          indexed_at TEXT NOT NULL,
          reviewed INTEGER NOT NULL DEFAULT 1,
          importance INTEGER NOT NULL DEFAULT 3,
          namespace TEXT NOT NULL DEFAULT 'default'
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS chunks (
          chunk_id TEXT PRIMARY KEY,
          entry_id TEXT NOT NULL,
          chunk_index INTEGER NOT NULL,
          text TEXT NOT NULL,
          token_estimate INTEGER NOT NULL,
          char_count INTEGER NOT NULL,
          FOREIGN KEY(entry_id) REFERENCES entries(entry_id) ON DELETE CASCADE
        )
        """
    )
    ensure_column(conn, "entries", "relation_json", "TEXT", "'{}'")
    ensure_column(conn, "entries", "conflict_status", "TEXT", "'none'")
    ensure_column(conn, "entries", "source_confidence", "REAL", "0.5")
    fts_sql = conn.execute("SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'chunks_fts'").fetchone()
    if fts_sql and fts_sql[0] and "content=''" in fts_sql[0]:
        conn.execute("DROP TABLE IF EXISTS chunks_fts")
    conn.execute(
        """
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
          chunk_id UNINDEXED,
          text
        )
        """
    )
    conn.commit()
    return conn


def extract_tags(text: str) -> list[str]:
    for line in text.splitlines()[:5]:
        if line.lower().startswith("#tags:"):
            tags = line.split(":", 1)[1]
            return [t.strip() for t in tags.split(",") if t.strip()]
    return []


def parse_relation_values(value: str) -> list[str]:
    return [item.strip() for item in re.split(r"[,;|]", value) if item.strip()]


def validate_relation_target(rel_type: str, target: str) -> tuple[bool, str]:
    if rel_type not in VALID_RELATION_KEYS:
        return False, f"non-canonical relation type: {rel_type}"
    cleaned = (target or "").strip()
    if not cleaned:
        return False, "empty relation target"
    if not cleaned.startswith(CANONICAL_RELATION_TARGET_PREFIXES):
        allowed = ", ".join(CANONICAL_RELATION_TARGET_PREFIXES)
        return False, f"relation target must start with one of: {allowed}"
    if cleaned.startswith("learn:") and len(cleaned) <= len("learn:"):
        return False, "learn: target requires a signature"
    if cleaned.startswith("chunk:") and len(cleaned) <= len("chunk:"):
        return False, "chunk: target requires a chunk id"
    if cleaned.startswith("path:") and len(cleaned) <= len("path:"):
        return False, "path: target requires a canonical source path"
    return True, "ok"


def known_learning_signatures() -> set[str]:
    signatures: set[str] = set()
    if not LEARNINGS_DIR.exists():
        return signatures
    for path in sorted(LEARNINGS_DIR.rglob("*.md")):
        try:
            raw = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for line in raw.splitlines():
            if line.lower().startswith("- signature:"):
                value = line.split(":", 1)[1].strip()
                if value and value.lower() != "none":
                    signatures.add(value)
                    signatures.add(value.casefold())
    return signatures


def derive_source_confidence(memory_type: str, reviewed: bool) -> float:
    base = {
        "procedural": 0.88,
        "semantic": 0.84,
        "episodic": 0.72,
        "learning": 0.58 if reviewed else 0.42,
        "buffer": 0.35,
    }.get(memory_type, 0.5)
    return round(base, 2)


def parse_memory_metadata(raw: str, path: Path, memory_type: str) -> dict:
    relation_json = {key: [] for key in VALID_RELATION_KEYS}
    conflict_status = "none"
    source_confidence: Optional[float] = None
    reviewed = not (memory_type == "learning" and "- status: pending" in raw.casefold())
    for line in raw.splitlines()[:50]:
        low = line.strip().lower()
        if low.startswith("- source_confidence:") or low.startswith("source_confidence:"):
            _, value = line.split(":", 1)
            try:
                source_confidence = max(0.0, min(1.0, float(value.strip())))
            except Exception:
                pass
        elif low.startswith("- conflict_status:") or low.startswith("conflict_status:"):
            _, value = line.split(":", 1)
            cleaned = value.strip().casefold()
            if cleaned in {"none", "active", "superseded", "contradicted", "stale"}:
                conflict_status = cleaned
        else:
            for key in VALID_RELATION_KEYS:
                if low.startswith(f"- {key}:") or low.startswith(f"{key}:"):
                    _, value = line.split(":", 1)
                    relation_json[key] = parse_relation_values(value)
    if source_confidence is None:
        source_confidence = derive_source_confidence(memory_type, reviewed)
    relation_json = {key: values for key, values in relation_json.items() if values}
    return {
        "relation_json": relation_json,
        "conflict_status": conflict_status,
        "source_confidence": source_confidence,
        "reviewed": reviewed,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(path.stat().st_ctime)),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(path.stat().st_mtime)),
    }


def rebuild_lexical_index(full: bool = False) -> dict:
    conn = ensure_db()
    changed = 0
    seen_paths = set()
    for mem_type, path in canonical_memory_files():
        seen_paths.add(str(path))
        raw = path.read_text(encoding="utf-8", errors="ignore")
        text = strip_frontmatter(raw)
        content_hash = sha256_text(text)
        metadata = parse_memory_metadata(raw, path, mem_type)
        row = conn.execute("SELECT entry_id, content_hash FROM entries WHERE source_path = ?", (str(path),)).fetchone()
        if row and row["content_hash"] == content_hash and not full:
            continue
        entry_id = row["entry_id"] if row else sha256_text(str(path))
        conn.execute("DELETE FROM chunks_fts WHERE chunk_id IN (SELECT chunk_id FROM chunks WHERE entry_id = ?)", (entry_id,))
        conn.execute("DELETE FROM chunks WHERE entry_id = ?", (entry_id,))
        conn.execute(
            """
            INSERT INTO entries(entry_id, source_path, memory_type, content_hash, tags_json, created_at, updated_at, indexed_at, reviewed, importance, namespace, relation_json, conflict_status, source_confidence)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(entry_id) DO UPDATE SET
              source_path=excluded.source_path,
              memory_type=excluded.memory_type,
              content_hash=excluded.content_hash,
              tags_json=excluded.tags_json,
              created_at=excluded.created_at,
              updated_at=excluded.updated_at,
              indexed_at=excluded.indexed_at,
              reviewed=excluded.reviewed,
              relation_json=excluded.relation_json,
              conflict_status=excluded.conflict_status,
              source_confidence=excluded.source_confidence
            """,
            (
                entry_id,
                str(path),
                mem_type,
                content_hash,
                json.dumps(extract_tags(raw), ensure_ascii=False),
                metadata["created_at"],
                metadata["updated_at"],
                now_iso(),
                1 if metadata["reviewed"] else 0,
                3,
                "default",
                json.dumps(metadata["relation_json"], ensure_ascii=False),
                metadata["conflict_status"],
                metadata["source_confidence"],
            ),
        )
        chunks = chunk_text(text)
        for idx, chunk in enumerate(chunks):
            chunk_id = sha256_text(f"{entry_id}:{idx}:{chunk[:80]}")
            conn.execute(
                "INSERT INTO chunks(chunk_id, entry_id, chunk_index, text, token_estimate, char_count) VALUES(?, ?, ?, ?, ?, ?)",
                (chunk_id, entry_id, idx, chunk, max(1, len(chunk) // 4), len(chunk)),
            )
            conn.execute("INSERT INTO chunks_fts(chunk_id, text) VALUES(?, ?)", (chunk_id, chunk))
        changed += 1
    missing = conn.execute("SELECT source_path, entry_id FROM entries").fetchall()
    for row in missing:
        if row["source_path"] not in seen_paths:
            conn.execute("DELETE FROM chunks_fts WHERE chunk_id IN (SELECT chunk_id FROM chunks WHERE entry_id = ?)", (row["entry_id"],))
            conn.execute("DELETE FROM chunks WHERE entry_id = ?", (row["entry_id"],))
            conn.execute("DELETE FROM entries WHERE entry_id = ?", (row["entry_id"],))
    conn.commit()
    state = read_state()
    profile = host_profile_status()
    state["lexical_last_indexed_at"] = now_iso()
    state["lexical_entries"] = conn.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
    state["lexical_chunks"] = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    state["canonical_files_count"] = len(canonical_memory_files())
    state["host_profile"] = profile
    write_state(state)
    return {
        "changed_entries": changed,
        "entries": state["lexical_entries"],
        "chunks": state["lexical_chunks"],
        "indexed_at": state["lexical_last_indexed_at"],
    }


def qdrant_request(path: str, *, method: str = "GET", payload: Optional[dict] = None, timeout: int = 10) -> dict:
    url = f"{QDRANT_URL}{path}"
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode("utf-8", "ignore")
        return json.loads(raw) if raw else {}


def qdrant_ok() -> bool:
    try:
        with urllib.request.urlopen(f"{QDRANT_URL}/collections", timeout=3) as r:
            return r.status == 200
    except Exception:
        return False


def semantic_daemon_request(path: str, *, payload: Optional[dict] = None, timeout: int = 10) -> dict:
    url = f"{SEMANTIC_DAEMON_URL}{path}"
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    method = "POST" if payload is not None else "GET"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode("utf-8", "ignore")
        return json.loads(raw) if raw else {}


def semantic_daemon_ok() -> bool:
    try:
        with urllib.request.urlopen(f"{SEMANTIC_DAEMON_URL}{SEMANTIC_DAEMON_HEALTH_PATH}", timeout=1.5) as r:
            return r.status == 200
    except Exception:
        return False


def ensure_semantic_daemon(timeout: float = 12.0) -> tuple[bool, Optional[str]]:
    if semantic_daemon_ok():
        return True, None
    daemon_script = SKILL_DIR / "scripts" / "semantic_daemon.py"
    if not daemon_script.exists():
        return False, f"semantic daemon script missing: {daemon_script}"
    proc = None
    try:
        proc = subprocess.Popen(
            ["python3", str(daemon_script)],
            cwd=str(WORKSPACE),
            env=os.environ.copy(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except Exception as exc:
        return False, str(exc)
    deadline = time.time() + timeout
    last_error = None
    while time.time() < deadline:
        if semantic_daemon_ok():
            return True, None
        if proc is not None and proc.poll() is not None:
            if semantic_daemon_ok():
                return True, None
            last_error = f"semantic daemon exited with code {proc.returncode}"
            break
        time.sleep(0.2)
    if semantic_daemon_ok():
        return True, None
    return False, last_error or "semantic daemon failed to start"


def qdrant_collection_info() -> Optional[dict]:
    try:
        data = qdrant_request(f"/collections/{QDRANT_COLLECTION}", timeout=3)
        return data.get("result")
    except Exception:
        return None


def qdrant_scroll(limit: int = 256) -> list[dict]:
    if not qdrant_ok():
        return []
    points: list[dict] = []
    offset = None
    while True:
        payload = {"limit": limit, "with_payload": True, "with_vectors": False}
        if offset is not None:
            payload["offset"] = offset
        try:
            data = qdrant_request(f"/collections/{QDRANT_COLLECTION}/points/scroll", method="POST", payload=payload, timeout=30)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return []
            raise
        result = data.get("result") or {}
        batch = result.get("points") or []
        points.extend(batch)
        offset = result.get("next_page_offset")
        if not offset or not batch:
            break
    return points


def semantic_dependencies_available() -> dict:
    import importlib.util
    return {
        "sentence_transformers": bool(importlib.util.find_spec("sentence_transformers")),
        "numpy": bool(importlib.util.find_spec("numpy")),
    }


def get_embedding_model():
    global _EMBED_MODEL_CACHE
    if _EMBED_MODEL_CACHE is not None:
        return _EMBED_MODEL_CACHE
    from sentence_transformers import SentenceTransformer
    _EMBED_MODEL_CACHE = SentenceTransformer(EMBED_MODEL, device="cpu", local_files_only=True)
    return _EMBED_MODEL_CACHE


def local_embedding_model_available() -> tuple[bool, Optional[str]]:
    deps = semantic_dependencies_available()
    if not all(deps.values()):
        return False, "embedding dependencies missing"
    ready, error = ensure_semantic_daemon()
    if ready:
        return True, None
    return False, error or "semantic daemon unavailable"


def semantic_runtime_status(state: Optional[dict] = None) -> dict:
    state = state or read_state()
    deps = semantic_dependencies_available()
    qdrant_ready = qdrant_ok()
    info = qdrant_collection_info() if qdrant_ready else None
    model_ok, model_error = local_embedding_model_available()
    vectors = int((info or {}).get("indexed_vectors_count") or (info or {}).get("points_count") or 0)
    return {
        "deps": deps,
        "qdrant": qdrant_ready,
        "collection_present": bool(info),
        "collection_info": info,
        "model_ready": model_ok,
        "model_error": model_error,
        "indexed_vectors": vectors,
        "semantic_fresh": bool(state.get("semantic_last_indexed_at")) and not semantic_index_stale(state),
        "semantic_last_indexed_at": state.get("semantic_last_indexed_at"),
        "semantic_ready": qdrant_ready and model_ok and bool(info) and vectors > 0 and not semantic_index_stale(state),
        "host_profile": host_profile_status(),
    }


def ensure_qdrant_collection(vector_size: int, recreate: bool = False) -> None:
    if recreate:
        try:
            qdrant_request(f"/collections/{QDRANT_COLLECTION}", method="DELETE", timeout=10)
        except Exception:
            pass
    payload = {
        "vectors": {"size": vector_size, "distance": "Cosine"},
        "optimizers_config": {"memmap_threshold": 50000},
    }
    try:
        qdrant_request(f"/collections/{QDRANT_COLLECTION}", method="PUT", payload=payload, timeout=20)
    except urllib.error.HTTPError as exc:
        if exc.code != 409:
            raise


def chunk_point_id(chunk_id: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"super-memori:{chunk_id}"))


def embed_texts(texts: list[str], *, prefix: str) -> list[list[float]]:
    if not texts:
        return []
    ready, error = ensure_semantic_daemon()
    if not ready:
        raise RuntimeError(f"semantic daemon unavailable: {error}")
    data = semantic_daemon_request(
        SEMANTIC_DAEMON_EMBED_PATH,
        payload={"texts": texts, "prefix": prefix},
        timeout=max(30, len(texts) * 5),
    )
    vectors = data.get("vectors") or []
    return [list(vector) for vector in vectors]


def rebuild_semantic_index(*, recreate: bool = True, limit: Optional[int] = None) -> dict:
    if not qdrant_ok():
        raise RuntimeError("qdrant unavailable")
    model_ok, model_error = local_embedding_model_available()
    if not model_ok:
        raise RuntimeError(f"local embedding model unavailable: {model_error}")

    conn = ensure_db()
    rows = conn.execute(
        """
        SELECT c.chunk_id, c.text, e.source_path, e.memory_type, e.updated_at, e.reviewed,
               c.chunk_index, e.entry_id, e.relation_json, e.conflict_status, e.source_confidence
        FROM chunks c
        JOIN entries e ON e.entry_id = c.entry_id
        ORDER BY e.source_path, c.chunk_index
        """
    ).fetchall()
    if limit is not None:
        rows = rows[:limit]
    if not rows:
        state = read_state()
        state["semantic_last_indexed_at"] = now_iso()
        state["semantic_indexed_vectors"] = 0
        write_state(state)
        return {"indexed_vectors": 0, "indexed_at": state["semantic_last_indexed_at"], "collection": QDRANT_COLLECTION}

    sample_vector = embed_texts([rows[0]["text"]], prefix="passage")[0]
    ensure_qdrant_collection(len(sample_vector), recreate=recreate)

    indexed = 0
    for start in range(0, len(rows), SEMANTIC_BATCH_SIZE):
        batch = rows[start:start + SEMANTIC_BATCH_SIZE]
        vectors = embed_texts([row["text"] for row in batch], prefix="passage")
        points = []
        for row, vector in zip(batch, vectors):
            snippet = (row["text"] or "").strip().replace("\n", " ")
            payload = {
                "chunk_id": row["chunk_id"],
                "entry_id": row["entry_id"],
                "source_path": row["source_path"],
                "memory_type": row["memory_type"],
                "updated_at": row["updated_at"],
                "reviewed": int(row["reviewed"]),
                "chunk_index": int(row["chunk_index"]),
                "text": row["text"],
                "snippet": snippet[:400],
                "relation_json": json.loads(row["relation_json"] or "{}"),
                "conflict_status": row["conflict_status"] or "none",
                "source_confidence": float(row["source_confidence"] or 0.5),
            }
            points.append({"id": chunk_point_id(row["chunk_id"]), "vector": vector, "payload": payload})
        qdrant_request(f"/collections/{QDRANT_COLLECTION}/points?wait=true", method="PUT", payload={"points": points}, timeout=120)
        indexed += len(points)

    info = qdrant_collection_info() or {}
    state = read_state()
    state["semantic_last_indexed_at"] = now_iso()
    state["semantic_indexed_vectors"] = int(info.get("indexed_vectors_count") or info.get("points_count") or indexed)
    state["semantic_collection"] = QDRANT_COLLECTION
    write_state(state)
    return {
        "indexed_vectors": state["semantic_indexed_vectors"],
        "indexed_at": state["semantic_last_indexed_at"],
        "collection": QDRANT_COLLECTION,
    }


def lexical_search(query: str, memory_type: str = "all", limit: int = 5, reviewed_only: bool = False) -> list[dict]:
    conn = ensure_db()
    terms = [t.strip() for t in query.replace('"', ' ').split() if t.strip()]
    if not terms:
        return []
    fts_query = " OR ".join(f'"{term}"' for term in terms)
    params: list[object] = []
    sql = """
    SELECT e.source_path, e.memory_type, e.updated_at, c.chunk_id, c.text AS snippet,
           e.reviewed, e.relation_json, e.conflict_status, e.source_confidence,
           bm25(chunks_fts) AS rank
    FROM chunks_fts
    JOIN chunks c ON c.rowid = chunks_fts.rowid
    JOIN entries e ON e.entry_id = c.entry_id
    WHERE chunks_fts MATCH ?
    """
    params.append(fts_query)
    if memory_type != "all":
        sql += " AND e.memory_type = ?"
        params.append(memory_type)
    if reviewed_only:
        sql += " AND e.reviewed = 1"
    sql += " ORDER BY rank LIMIT ?"
    params.append(limit)
    rows = conn.execute(sql, tuple(params)).fetchall()
    results = []
    for row in rows:
        item = dict(row)
        snippet = (item.get("snippet") or "").strip().replace("\n", " ")
        item["snippet"] = snippet[:280] + ("..." if len(snippet) > 280 else "")
        item["relation_json"] = json.loads(item.get("relation_json") or "{}")
        item["source_confidence"] = float(item.get("source_confidence") or 0.5)
        results.append(item)
    return results


def semantic_search(query: str, *, memory_type: str = "all", limit: int = 5, reviewed_only: bool = False) -> list[dict]:
    ready, error = ensure_semantic_daemon()
    if not ready:
        raise RuntimeError(f"semantic daemon unavailable: {error}")
    data = semantic_daemon_request(
        SEMANTIC_DAEMON_SEARCH_PATH,
        payload={
            "query": query,
            "memory_type": memory_type,
            "limit": max(limit, 1),
            "reviewed_only": reviewed_only,
        },
        timeout=30,
    )
    return data.get("results") or []


def reciprocal_rank_fuse(lexical_results: list[dict], semantic_results: list[dict], *, limit: int = 5) -> list[dict]:
    combined: dict[str, dict] = {}
    order_lists = [("lexical", lexical_results), ("semantic", semantic_results)]
    for source_name, rows in order_lists:
        for idx, row in enumerate(rows, start=1):
            chunk_id = row.get("chunk_id") or f"{source_name}:{idx}:{row.get('source_path','?')}"
            entry = combined.setdefault(chunk_id, dict(row))
            entry.setdefault("fusion_sources", [])
            if source_name not in entry["fusion_sources"]:
                entry["fusion_sources"].append(source_name)
            entry["fusion_score"] = entry.get("fusion_score", 0.0) + 1.0 / (RRF_K + idx)
            if source_name == "semantic":
                entry["semantic_score"] = row.get("semantic_score")
            if source_name == "lexical":
                entry["lexical_rank"] = row.get("rank")
    fused = sorted(combined.values(), key=lambda item: item.get("fusion_score", 0.0), reverse=True)
    return fused[:limit]


def result_identifiers(item: dict) -> set[str]:
    identifiers = set()
    for key in ("chunk_id", "source_path"):
        value = item.get(key)
        if value:
            identifiers.add(str(value))
            identifiers.add(str(value).casefold())
    source_path = item.get("source_path")
    if source_path:
        identifiers.add(Path(str(source_path)).name.casefold())
    return identifiers


def freshness_days(updated_at: Optional[str]) -> Optional[float]:
    ts = parse_iso_timestamp(updated_at)
    if ts is None:
        return None
    return max(0.0, (time.time() - ts) / 86400.0)


def temporal_relational_rerank(results: list[dict], *, query: str = "", limit: int = 5) -> list[dict]:
    if not results:
        return []
    rescored: list[dict] = []
    identifier_map: dict[str, int] = {}
    for idx, item in enumerate(results):
        for ident in result_identifiers(item):
            identifier_map[ident] = idx

    base_scores = []
    for idx, item in enumerate(results, start=1):
        base = float(item.get("fusion_score") or item.get("semantic_score") or (1.0 / (RRF_K + idx)))
        age_days = freshness_days(item.get("updated_at"))
        freshness_multiplier = 1.0 if age_days is None else (0.55 + 0.45 * math.exp(-age_days / TEMPORAL_DECAY_DAYS))
        confidence_multiplier = 0.7 + 0.6 * float(item.get("source_confidence") or 0.5)
        reviewed_multiplier = 1.03 if int(item.get("reviewed") or 0) else 0.97
        conflict_status = (item.get("conflict_status") or "none").casefold()
        conflict_multiplier = {
            "none": 1.0,
            "active": 1.0,
            "stale": 0.88,
            "superseded": 0.72,
            "contradicted": 0.65,
        }.get(conflict_status, 1.0)
        path_multiplier = semantic_path_penalty(str(item.get("source_path") or ""))
        anchor_multiplier = query_anchor_multiplier(item, query=query)
        score = base * freshness_multiplier * confidence_multiplier * reviewed_multiplier * conflict_multiplier * path_multiplier * anchor_multiplier
        rescored.append(dict(item))
        rescored[-1]["freshness_days"] = age_days
        rescored[-1]["relation_hits"] = []
        rescored[-1]["query_anchor_multiplier"] = round(anchor_multiplier, 4)
        rescored[-1]["path_penalty_multiplier"] = round(path_multiplier, 4)
        base_scores.append(score)

    scores = list(base_scores)
    for idx, item in enumerate(rescored):
        relations = item.get("relation_json") or {}
        source_conf = float(item.get("source_confidence") or 0.5)
        for rel_key, bonus, target_multiplier in [
            ("supersedes", 0.10, 0.74),
            ("refines", 0.05, 0.96),
            ("confirms", 0.04, 1.02),
            ("extends", 0.03, 0.99),
        ]:
            for target in relations.get(rel_key, []) or []:
                target_idx = identifier_map.get(str(target)) or identifier_map.get(str(target).casefold())
                if target_idx is None:
                    continue
                scores[idx] *= 1.0 + bonus
                scores[target_idx] *= target_multiplier
                rescored[idx]["relation_hits"].append(f"{rel_key}:{target}")
        for target in relations.get("contradicts", []) or []:
            target_idx = identifier_map.get(str(target)) or identifier_map.get(str(target).casefold())
            if target_idx is None:
                continue
            target_conf = float(rescored[target_idx].get("source_confidence") or 0.5)
            if source_conf >= target_conf:
                scores[target_idx] *= 0.68
                scores[idx] *= 1.05
            else:
                scores[idx] *= 0.9
            rescored[idx]["relation_hits"].append(f"contradicts:{target}")

    for idx, item in enumerate(rescored):
        item["temporal_relational_score"] = scores[idx]
        item["rerank_applied"] = True
    rescored.sort(key=lambda entry: entry.get("temporal_relational_score", 0.0), reverse=True)
    return rescored[:limit]


def diversify_results(results: list[dict], *, limit: int = 5, per_source_cap: int = 2) -> list[dict]:
    diversified: list[dict] = []
    per_source: dict[str, int] = {}
    for item in results:
        source = item.get("source_path", "?")
        if per_source.get(source, 0) >= per_source_cap:
            continue
        diversified.append(item)
        per_source[source] = per_source.get(source, 0) + 1
        if len(diversified) >= limit:
            break
    return diversified


def _query_has_exact_indicator(query: str) -> bool:
    lowered = (query or "").casefold()
    return any(token in lowered for token in ["/", ".md", ".py", ".sh", ".json", "#tags", "path:", "chunk:", "learn:"])


def classify_result_authority(item: dict, *, query: str, mode_used: str) -> str:
    chunk_id = str(item.get("chunk_id") or "")
    if chunk_id.startswith("grep:"):
        return "fallback"

    fusion_sources = {str(source).casefold() for source in (item.get("fusion_sources") or [])}
    source_path = str(item.get("source_path") or "")
    snippet = str(item.get("snippet") or "")
    query_lc = (query or "").strip().casefold()

    exact_query_match = bool(query_lc) and (query_lc in source_path.casefold() or query_lc in snippet.casefold())
    exact_indicator = exact_query_match or _query_has_exact_indicator(query)
    lexical_signal = bool(fusion_sources & {"lexical"}) or item.get("rank") is not None or item.get("lexical_rank") is not None
    semantic_signal = bool(fusion_sources & {"semantic"}) or item.get("semantic_score") is not None

    if mode_used == "hybrid" and lexical_signal and semantic_signal:
        return "hybrid"
    if mode_used == "semantic" and semantic_signal and not lexical_signal:
        return "semantic"
    if exact_indicator and lexical_signal:
        return "exact"
    if semantic_signal:
        return "semantic"
    if lexical_signal:
        return "exact" if mode_used in {"exact", "recent", "learning"} else "fallback"
    return "fallback"


def summarize_authority_surface(results: list[dict], *, query: str, mode_used: str, degraded: bool) -> dict:
    classified = []
    for item in results:
        enriched = dict(item)
        enriched["match_authority"] = classify_result_authority(enriched, query=query, mode_used=mode_used)
        classified.append(enriched)
    authoritative_result_present = any(item.get("match_authority") in {"exact", "hybrid"} for item in classified)
    low_authority_only = bool(classified) and not authoritative_result_present
    return {
        "results": classified,
        "authoritative_result_present": authoritative_result_present,
        "low_authority_only": low_authority_only,
        "requires_low_authority_warning": bool(degraded and low_authority_only),
    }


def grep_fallback(query: str, memory_type: str = "all", limit: int = 5, reviewed_only: bool = False) -> list[dict]:
    search_paths: list[Path] = []
    if memory_type == "all":
        search_paths = [MEMORY_DIR / "episodic", MEMORY_DIR / "semantic", MEMORY_DIR / "procedural", LEARNINGS_DIR]
        if (MEMORY_DIR / "working-buffer.md").exists():
            search_paths.append(MEMORY_DIR / "working-buffer.md")
        if (WORKSPACE / "MEMORY.md").exists():
            search_paths.append(WORKSPACE / "MEMORY.md")
    elif memory_type == "learning":
        search_paths = [LEARNINGS_DIR]
    elif memory_type == "buffer":
        search_paths = [MEMORY_DIR / "working-buffer.md"]
    else:
        search_paths = [MEMORY_DIR / memory_type]

    results = []
    query_lc = query.casefold()
    for path in search_paths:
        if not path.exists():
            continue
        file_iter = [path] if path.is_file() else sorted(path.rglob("*.md"))
        for file_path in file_iter:
            actual_type = infer_memory_type(file_path)
            if memory_type != "all" and actual_type != memory_type:
                continue
            try:
                raw = file_path.read_text(encoding="utf-8", errors="ignore")
                lines = raw.splitlines()
                metadata = parse_memory_metadata(raw, file_path, actual_type)
            except Exception:
                continue

            current_learning_reviewed = True
            current_learning_header = 1
            matched = False
            for lineno, line in enumerate(lines, 1):
                if actual_type == "learning" and line.startswith("## "):
                    current_learning_header = lineno
                    current_learning_reviewed = True
                elif actual_type == "learning" and line.lower().startswith("- status:"):
                    status_value = line.split(":", 1)[1].strip().casefold() if ":" in line else ""
                    current_learning_reviewed = status_value != "pending"

                if query_lc in line.casefold():
                    if reviewed_only and actual_type == "learning" and not current_learning_reviewed:
                        continue
                    results.append({
                        "source_path": str(file_path),
                        "memory_type": actual_type,
                        "chunk_id": f"grep:{file_path}:{current_learning_header if actual_type == 'learning' else lineno}",
                        "snippet": line.strip(),
                        "updated_at": metadata["updated_at"],
                        "rank": None,
                        "reviewed": 1 if metadata["reviewed"] else 0,
                        "relation_json": metadata["relation_json"],
                        "conflict_status": metadata["conflict_status"],
                        "source_confidence": metadata["source_confidence"],
                    })
                    matched = True
                    break
            if matched and len(results) >= limit:
                return results
    return results


def audit_memory_integrity() -> dict:
    conn = ensure_db()
    lexical_chunks = conn.execute("SELECT chunk_id, source_path FROM chunks JOIN entries USING(entry_id)").fetchall()
    lexical_ids = {row["chunk_id"] for row in lexical_chunks}
    lexical_sources = {row["source_path"] for row in lexical_chunks}

    orphan_chunk_rows = conn.execute(
        "SELECT c.chunk_id FROM chunks c LEFT JOIN entries e ON e.entry_id = c.entry_id WHERE e.entry_id IS NULL"
    ).fetchall()
    orphan_fts_rows = conn.execute(
        "SELECT c.chunk_id FROM chunks c LEFT JOIN chunks_fts f ON f.chunk_id = c.chunk_id WHERE f.chunk_id IS NULL"
    ).fetchall()
    entry_rows = conn.execute("SELECT source_path, relation_json FROM entries").fetchall()
    broken_relations = []
    known_relation_targets = lexical_ids | lexical_sources | {Path(path).name.casefold() for path in lexical_sources}
    learning_signatures = known_learning_signatures()
    for row in entry_rows:
        try:
            relations = json.loads(row["relation_json"] or "{}")
        except Exception:
            relations = {}
        for rel_key, targets in relations.items():
            for target in targets or []:
                valid, reason = validate_relation_target(rel_key, str(target))
                if not valid:
                    broken_relations.append({"source_path": row["source_path"], "relation": rel_key, "target": target, "reason": reason})
                    continue
                target_value = str(target)
                if target_value.startswith("chunk:"):
                    chunk_id = target_value[len("chunk:"):]
                    if chunk_id not in lexical_ids:
                        broken_relations.append({"source_path": row["source_path"], "relation": rel_key, "target": target, "reason": "chunk target not found"})
                elif target_value.startswith("path:"):
                    source_path = target_value[len("path:"):]
                    source_norm = source_path.casefold()
                    if source_path not in known_relation_targets and source_norm not in known_relation_targets:
                        broken_relations.append({"source_path": row["source_path"], "relation": rel_key, "target": target, "reason": "path target not found"})
                elif target_value.startswith("learn:"):
                    signature = target_value[len("learn:"):].strip()
                    if signature not in learning_signatures and signature.casefold() not in learning_signatures:
                        broken_relations.append({"source_path": row["source_path"], "relation": rel_key, "target": target, "reason": "learning signature target not found"})

    profile = host_profile_status()
    vector_points = qdrant_scroll(limit=int(profile.get("audit_scroll_limit") or 256)) if qdrant_ok() else []
    vector_chunk_ids = {(point.get("payload") or {}).get("chunk_id") for point in vector_points if (point.get("payload") or {}).get("chunk_id")}
    orphan_vectors = sorted(chunk_id for chunk_id in vector_chunk_ids if chunk_id not in lexical_ids)
    missing_vectors = sorted(chunk_id for chunk_id in lexical_ids if chunk_id not in vector_chunk_ids)

    vector_state = "ok"
    if not lexical_ids and not vector_chunk_ids:
        vector_state = "semantic-unbuilt"
    elif missing_vectors and not vector_chunk_ids:
        vector_state = "semantic-unbuilt"
    elif missing_vectors:
        vector_state = "stale-vectors"
    elif orphan_vectors:
        vector_state = "orphan-vectors"

    has_drift = bool(orphan_chunk_rows or orphan_fts_rows or orphan_vectors or broken_relations or (missing_vectors and vector_state != "semantic-unbuilt"))
    return {
        "status": "ok" if not has_drift else "warn",
        "lexical_chunk_count": len(lexical_ids),
        "vector_point_count": len(vector_chunk_ids),
        "vector_state": vector_state,
        "orphan_chunks": [row["chunk_id"] for row in orphan_chunk_rows],
        "orphan_fts_chunks": [row["chunk_id"] for row in orphan_fts_rows],
        "orphan_vectors": orphan_vectors,
        "missing_vectors": missing_vectors,
        "broken_relations": broken_relations,
        "host_profile": profile,
        "lexical_fresh": bool(read_state().get("lexical_last_indexed_at")) and not lexical_index_stale(read_state()),
        "semantic_fresh": bool(read_state().get("semantic_last_indexed_at")) and not semantic_index_stale(read_state()),
    }
