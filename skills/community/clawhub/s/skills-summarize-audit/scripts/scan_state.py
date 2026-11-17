"""Explicit, read-only baseline reuse; discovery and source hashes are always refreshed."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

IGNORED = {".git", ".archived", "__pycache__", ".pytest_cache", ".data", ".audit-snapshots", "node_modules", ".venv"}


def digest_paths(paths):
    result = {}
    for path in sorted(set(Path(p).resolve() for p in paths)):
        try:
            result[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            result[str(path)] = "unavailable"
    return result


def fingerprint(item):
    paths = [Path(p) for p in item.get("source_paths", [])]
    reference_targets = {}
    for source in list(paths):
        if source.name == "SKILL.md" and source.parent.exists():
            paths += [p for p in source.parent.rglob("*") if p.is_file() and not set(p.relative_to(source.parent).parts) & IGNORED]
            try:
                refs = re.findall(r"(?:references|scripts|agents)/[A-Za-z0-9_.\-/]+", source.read_text(encoding="utf-8-sig", errors="replace"))
                for ref in refs:
                    for parent in [source.parent, *list(source.parents)[1:5]]:
                        target = parent / ref.rstrip(".,;:)")
                        reference_targets[str(target.resolve())] = "present" if target.exists() else "missing"
                        if target.is_file():
                            paths.append(target)
            except OSError:
                reference_targets[str(source)] = "unavailable"
    return {"files": digest_paths(paths), "reference_targets": reference_targets,
            "metadata": hashlib.sha256(json.dumps(item, sort_keys=True, ensure_ascii=False).encode()).hexdigest()}


def plan_scan(items, context, baseline=None, mode="auto", now=None):
    now = now or datetime.now(timezone.utc)
    fingerprints = {item["id"]: fingerprint(item) for item in items}
    supplied = baseline is not None
    baseline = baseline if isinstance(baseline, dict) else {"invalid": True}
    valid = baseline.get("schema_version") == 1 and baseline.get("context") == context and isinstance(baseline.get("fingerprints"), dict)
    try:
        age = (now - datetime.fromisoformat(baseline["created_at"])).total_seconds() / 86400
        valid = valid and 0 <= age <= 30 and isinstance(baseline.get("findings"), dict)
    except (KeyError, TypeError, ValueError):
        valid = False
    actual = "incremental" if valid and mode != "full" else "full"
    previous = baseline.get("fingerprints", {}) if valid else {}
    changed = [key for key, value in fingerprints.items() if value != previous.get(key)]
    removed = sorted(set(previous) - set(fingerprints))
    reusable = {}
    if actual == "incremental":
        for key, fp in fingerprints.items():
            findings = baseline["findings"].get(key)
            if key not in changed and isinstance(findings, list) and not findings and "unavailable" not in fp["files"].values():
                reusable[key] = findings
    reasons = []
    if supplied and not valid:
        reasons.append("基线过期、格式或扫描边界不匹配，已重新全景扫描")
    if valid and (len(changed) + len(removed)) / max(len(previous), 1) >= 0.25:
        reasons.append("资产变化至少 25%")
    return {"mode": actual, "changed": changed, "removed": removed, "checked": len(items) - len(reusable),
            "reused": len(reusable), "reasons": reasons, "suggest_full_scan": False}, reusable, {
                "schema_version": 1, "created_at": baseline["created_at"] if actual == "incremental" else now.isoformat(), "checked_at": now.isoformat(), "context": context,
                "fingerprints": fingerprints, "findings": {}}


def finish_scan(scan, snapshot, issues, evidence_coverage=None):
    for key in snapshot["fingerprints"]:
        snapshot["findings"][key] = [i for i in issues if i["id"] == key]
    actionable = [i for i in issues if i["severity"] in {"warning", "critical"}]
    if scan["mode"] == "incremental":
        if any(i["severity"] == "critical" for i in issues):
            scan["reasons"].append("发现 critical")
        if len(actionable) >= 5:
            scan["reasons"].append("阻断或修复问题至少 5 项")
        if evidence_coverage and evidence_coverage["total"] and evidence_coverage["available"] / evidence_coverage["total"] < 0.75:
            scan["reasons"].append("证据覆盖不足 75%")
        scan["reasons"] = list(dict.fromkeys(scan["reasons"]))
        scan["suggest_full_scan"] = bool(scan["reasons"])
