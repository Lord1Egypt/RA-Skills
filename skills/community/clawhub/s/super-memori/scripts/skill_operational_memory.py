#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from typing import Optional

from super_memori_common import LEARNINGS_DIR, WORKSPACE, now_iso, normalize_compare_text, read_state, write_state

SKILL_MEMORY_DIR = WORKSPACE / "memory" / "semantic" / "skill-memory"
REGISTRY_PATH = SKILL_MEMORY_DIR / "registry.md"
LESSONS_PATH = SKILL_MEMORY_DIR / "lessons.md"


def _frontmatter(raw: str) -> dict[str, str]:
    if not raw.startswith("---"):
        return {}
    lines = raw.splitlines()
    meta: dict[str, str] = {}
    key = None
    collecting = False
    buf: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if collecting and line.startswith(" "):
            buf.append(line.strip())
            continue
        if collecting and buf:
            meta[key] = " ".join(buf).strip()
            buf = []
            collecting = False
        if ":" in line:
            k, v = line.split(":", 1)
            key = k.strip().casefold()
            v = v.strip()
            if v in {"|", ">"}:
                collecting = True
                buf = []
            else:
                meta[key] = v
    if collecting and buf:
        meta[key] = " ".join(buf).strip()
    return meta


def _sections(raw: str) -> dict[str, str]:
    out: dict[str, list[str]] = {}
    current = None
    for line in raw.splitlines():
        if line.startswith("## "):
            current = line[3:].strip().casefold()
            out.setdefault(current, [])
            continue
        if current is not None:
            out[current].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def _pick_section(sections: dict[str, str], needles: list[str]) -> str:
    for key, value in sections.items():
        if value and any(needle in key for needle in needles):
            return value
    return ""


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _skill_name_from_path(skill_md: Path) -> str:
    return skill_md.parent.name


def _related_skill_ids(blob_map: dict[str, str], self_id: str) -> list[str]:
    related: list[str] = []
    self_blob = blob_map[self_id]
    for other_id, blob in blob_map.items():
        if other_id == self_id:
            continue
        if other_id.casefold() in self_blob or self_id.casefold() in blob:
            related.append(other_id)
    return sorted(set(related))


def skill_memory_root() -> Path:
    return SKILL_MEMORY_DIR


def registry_path() -> Path:
    return REGISTRY_PATH


def lessons_path() -> Path:
    return LESSONS_PATH


def installed_skill_records() -> list[dict]:
    skills_root = WORKSPACE / "skills"
    records: list[dict] = []
    if not skills_root.exists():
        return records

    blob_map: dict[str, str] = {}
    raw_map: dict[str, str] = {}
    skill_paths = sorted(skills_root.glob("*/SKILL.md"))
    for skill_md in skill_paths:
        try:
            raw = skill_md.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        skill_id = _skill_name_from_path(skill_md)
        raw_map[skill_id] = raw
        blob_map[skill_id] = normalize_compare_text(raw)

    for skill_md in skill_paths:
        try:
            raw = skill_md.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        skill_id = _skill_name_from_path(skill_md)
        front = _frontmatter(raw)
        sections = _sections(raw)
        title = front.get("name") or skill_id
        description = (front.get("description") or "").replace("\n", " ").strip()
        trigger_text = _pick_section(sections, ["when to use", "required modes", "minimal decision rules", "quick start", "instructions"])
        avoid_text = _pick_section(sections, ["what not to do", "known limitations", "anti-patterns", "failure recovery", "what not to"])
        core_text = _pick_section(sections, ["execution", "runtime", "how to use", "quick start", "usage"])
        diagnostics_text = _pick_section(sections, ["health check", "troubleshooting", "failure recovery", "debug", "known limitations", "health & safety"])
        related = _related_skill_ids(blob_map, skill_id)
        records.append({
            "skill_id": skill_id,
            "status": "installed",
            "title": title,
            "path": str(skill_md),
            "source_hash": _hash_text(raw),
            "source_mtime": skill_md.stat().st_mtime,
            "purpose": description or raw.splitlines()[0].lstrip("# ").strip(),
            "best_for": trigger_text[:1500],
            "avoid_when": avoid_text[:1500],
            "trigger_signals": trigger_text[:1500],
            "task_patterns": trigger_text[:1500],
            "core_algorithm": core_text[:1500],
            "expected_inputs": "skill docs, user task text, examples, diagnostics",
            "touched_artifacts": str(skill_md),
            "typical_failures": diagnostics_text[:1500],
            "failure_signatures": avoid_text[:1500],
            "diagnostics": diagnostics_text[:1500],
            "recovery_steps": diagnostics_text[:1500],
            "successful_usage_examples": [],
            "failed_usage_examples": [],
            "reusable_lessons": [],
            "anti_patterns": avoid_text[:1500],
            "confidence_state": "installed",
            "freshness_state": "current",
            "validation_state": "source-scanned",
            "last_verified": now_iso(),
            "related_skills": related,
        })
    return records


def _registry_markdown(records: list[dict]) -> str:
    lines = ["# Skill Operational Registry", "#tags: skills, workflow, memory, habits", ""]
    for record in records:
        lines.extend([
            f"## {record['skill_id']}",
            f"- skill_id: {record['skill_id']}",
            f"- status: {record['status']}",
            f"- title: {record['title']}",
            f"- path: {record['path']}",
            f"- source_hash: {record['source_hash']}",
            f"- source_mtime: {record['source_mtime']}",
            f"- purpose: {record['purpose']}",
            f"- best_for: {record['best_for']}",
            f"- avoid_when: {record['avoid_when']}",
            f"- trigger_signals: {record['trigger_signals']}",
            f"- task_patterns: {record['task_patterns']}",
            f"- core_algorithm: {record['core_algorithm']}",
            f"- expected_inputs: {record['expected_inputs']}",
            f"- touched_artifacts: {record['touched_artifacts']}",
            f"- typical_failures: {record['typical_failures']}",
            f"- failure_signatures: {record['failure_signatures']}",
            f"- diagnostics: {record['diagnostics']}",
            f"- recovery_steps: {record['recovery_steps']}",
            f"- successful_usage_examples: none",
            f"- failed_usage_examples: none",
            f"- reusable_lessons: none",
            f"- anti_patterns: {record['anti_patterns']}",
            f"- confidence_state: {record['confidence_state']}",
            f"- freshness_state: {record['freshness_state']}",
            f"- validation_state: {record['validation_state']}",
            f"- last_verified: {record['last_verified']}",
            f"- related_skills: {', '.join(record['related_skills']) if record['related_skills'] else 'none'}",
            "",
        ])
    return "\n".join(lines)


def _learning_blocks() -> list[tuple[dict, str]]:
    blocks: list[tuple[dict, str]] = []
    if not LEARNINGS_DIR.exists():
        return blocks
    for path in sorted(LEARNINGS_DIR.rglob("*.md")):
        try:
            raw = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        current = None
        buf: list[str] = []
        meta: dict[str, str] = {}
        for line in raw.splitlines():
            if line.startswith("## "):
                if current and buf:
                    blocks.append((meta | {"path": str(path), "title": current}, "\n".join(buf).strip()))
                current = line[3:].strip()
                buf = []
                meta = {}
                continue
            if current is None:
                continue
            low = line.strip().lower()
            if low.startswith("- source:"):
                meta["source"] = line.split(":", 1)[1].strip()
            elif low.startswith("- signature:"):
                meta["signature"] = line.split(":", 1)[1].strip()
            elif low.startswith("- status:"):
                meta["status"] = line.split(":", 1)[1].strip()
            elif low.startswith("- tags:"):
                meta["tags"] = line.split(":", 1)[1].strip()
            else:
                buf.append(line)
        if current and buf:
            blocks.append((meta | {"path": str(path), "title": current}, "\n".join(buf).strip()))
    return blocks


def _skill_detection_quality(text: str) -> str:
    low = text.casefold()
    if any(term in low for term in ["validated", "confirmed", "reviewed"]):
        return "validated"
    if any(term in low for term in ["observed", "worked", "helped", "useful"]):
        return "observed"
    if any(term in low for term in ["stale", "outdated", "needs review"]):
        return "stale"
    return "inferred"


def _distinct_field_text(lines: list[str], labels: list[str], fallback: str = "") -> str:
    for line in lines:
        low = line.casefold()
        if any(low.startswith(label) for label in labels):
            return line.split(":", 1)[1].strip() if ":" in line else line.strip()
    return fallback


def _short_token_set(text: str) -> set[str]:
    return {tok for tok in re.findall(r"[a-z0-9_:-]+", text.casefold()) if len(tok) >= 4}


def _field_overlap_ratio(*fields: str) -> float:
    tokens = [_short_token_set(f) for f in fields if f]
    if len(tokens) < 2:
        return 0.0
    union = set().union(*tokens)
    if not union:
        return 0.0
    shared = set.intersection(*tokens)
    return len(shared) / max(1, len(union))


def _extract_why_better(lines: list[str], text: str) -> str:
    for label in ["- why", "- why_this_skill_helped:", "- why chosen:", "- why this skill helped:"]:
        for line in lines:
            if line.casefold().startswith(label):
                return line.split(":", 1)[1].strip() if ":" in line else line.strip()
    if "because" in text.casefold():
        return text[:260]
    return "selected because the example matched a repeatable operational pattern"


def _extract_preconditions(lines: list[str], text: str) -> str:
    for label in ["- preconditions:", "- prerequisites:", "- before:"]:
        for line in lines:
            if line.casefold().startswith(label):
                return line.split(":", 1)[1].strip() if ":" in line else line.strip()
    return "have the skill installed and the task pattern present"


def _extract_expected_outcome(lines: list[str], text: str) -> str:
    for label in ["- expected outcome:", "- outcome:", "- result quality:"]:
        for line in lines:
            if line.casefold().startswith(label):
                return line.split(":", 1)[1].strip() if ":" in line else line.strip()
    return "reusable operational improvement"


def _extract_antipattern(lines: list[str], text: str) -> str:
    for label in ["- anti-pattern:", "- anti patterns:", "- if misused:", "- known failure if omitted:"]:
        for line in lines:
            if line.casefold().startswith(label):
                return line.split(":", 1)[1].strip() if ":" in line else line.strip()
    return "using the skill without relevance checking"


def _lesson_confidence(text: str) -> float:
    quality = _skill_detection_quality(text)
    richness_bonus = 0.0
    if len(_short_token_set(text)) >= 24:
        richness_bonus += 0.08
    if any(marker in text.casefold() for marker in ["preconditions:", "expected outcome:", "anti-pattern:", "why this skill helped:"]):
        richness_bonus += 0.07
    if quality == "validated":
        return min(0.97, 0.9 + richness_bonus)
    if quality == "observed":
        return min(0.85, 0.7 + richness_bonus)
    if quality == "stale":
        return 0.35
    return min(0.72, 0.55 + richness_bonus)


def _distinctive_lesson_parts(text: str) -> tuple[str, str, str, str, str, str, str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    headline = lines[0] if lines else text[:160]
    task_shape = _distinct_field_text(lines, ["- task pattern:", "- task shape:", "- task_pattern:"] , headline)
    exact_usage = _distinct_field_text(lines, ["- exact usage pattern:", "- usage pattern:", "- exact_usage_pattern:"] , text[:320])
    reusable_rule = _distinct_field_text(lines, ["- reusable rule:", "- reusable_rule:"] , headline)
    why_better = _extract_why_better(lines, text)
    preconditions = _extract_preconditions(lines, text)
    expected_outcome = _extract_expected_outcome(lines, text)
    anti_pattern = _extract_antipattern(lines, text)
    return task_shape, exact_usage, reusable_rule, why_better, preconditions, expected_outcome, anti_pattern

def _compile_lesson(skill_id: str, lesson_text: str, source_path: str, confidence: float, validation_source: str) -> dict:
    task_shape, exact_usage, reusable_rule, why_better, preconditions, expected_outcome, anti_pattern = _distinctive_lesson_parts(lesson_text)
    raw_lines = [line.strip() for line in lesson_text.splitlines() if line.strip()]
    headline = raw_lines[0] if raw_lines else lesson_text[:180]
    quality = _skill_detection_quality(lesson_text)
    overlap = _field_overlap_ratio(task_shape, exact_usage, reusable_rule, why_better, preconditions, expected_outcome, anti_pattern)
    if len(_short_token_set(lesson_text)) < 8 or overlap > 0.42:
        return {}
    if not any(marker in lesson_text.casefold() for marker in ["preconditions:", "why", "expected outcome:", "anti-pattern:", "validation_source"]):
        confidence = min(confidence, 0.55)
    return {
        "skill_id": skill_id,
        "task_pattern": task_shape[:260],
        "task_shape": task_shape[:260],
        "user_intent": headline[:220],
        "why_this_skill_helped": why_better[:320],
        "exact_workflow_pattern": exact_usage[:700],
        "exact_usage_pattern": exact_usage[:700],
        "expected_outcome": expected_outcome[:220],
        "result_quality": expected_outcome[:220],
        "reusable_rule": reusable_rule[:260],
        "failure_if_omitted": anti_pattern[:220],
        "known_failure_if_omitted": anti_pattern[:220],
        "misuse_risk": anti_pattern[:220],
        "preconditions": preconditions[:220],
        "confidence": round(confidence, 2),
        "confidence_state": quality,
        "freshness": "current" if quality != "stale" else "stale",
        "validation_source": validation_source,
        "validation_state": quality,
        "evidence_basis": validation_source,
        "source_path": source_path,
        "timestamp": now_iso(),
        "anti_pattern": anti_pattern[:220],
    }


def compile_skill_lessons() -> list[dict]:
    records = installed_skill_records()
    lessons: list[dict] = []
    if not records:
        return lessons
    by_id = {record["skill_id"].casefold(): record for record in records}
    by_title = {record["title"].casefold(): record for record in records}
    for meta, body in _learning_blocks():
        blob = normalize_compare_text(body)
        matched = None
        for key, record in by_id.items():
            if key in blob or record["title"].casefold() in blob or f"skill:{key}" in blob:
                matched = record
                break
        if not matched:
            for key, record in by_title.items():
                if key in blob:
                    matched = record
                    break
        if not matched:
            continue
        confidence = _lesson_confidence(body)
        if _skill_detection_quality(body) == "stale":
            continue
        compiled = _compile_lesson(matched["skill_id"], body, meta["path"], confidence, meta.get("source", meta["path"]))
        if not compiled:
            continue
        lessons.append(compiled)
    return lessons


def refresh_skill_operational_memory() -> dict:
    SKILL_MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    registry = installed_skill_records()
    lessons = compile_skill_lessons()
    REGISTRY_PATH.write_text(_registry_markdown(registry), encoding="utf-8")
    lessons_lines = ["# Skill Operational Lessons", "#tags: skills, lessons, workflow, memory", ""]
    for lesson in lessons:
        lessons_lines.extend([
            f"## lesson — {lesson['timestamp']}",
            f"- skill_id: {lesson['skill_id']}",
            f"- task_pattern: {lesson['task_pattern']}",
            f"- task_shape: {lesson['task_shape']}",
            f"- user_intent: {lesson['user_intent']}",
            f"- why_this_skill_helped: {lesson['why_this_skill_helped']}",
            f"- preconditions: {lesson['preconditions']}",
            f"- exact_workflow_pattern: {lesson['exact_workflow_pattern']}",
            f"- expected_outcome: {lesson['expected_outcome']}",
            f"- result_quality: {lesson['result_quality']}",
            f"- reusable_rule: {lesson['reusable_rule']}",
            f"- failure_if_omitted: {lesson['failure_if_omitted']}",
            f"- misuse_risk: {lesson['misuse_risk']}",
            f"- anti_pattern: {lesson['anti_pattern']}",
            f"- confidence: {lesson['confidence']:.2f}",
            f"- confidence_state: {lesson['confidence_state']}",
            f"- freshness: {lesson['freshness']}",
            f"- validation_state: {lesson['validation_state']}",
            f"- evidence_basis: {lesson['evidence_basis']}",
            f"- validation_source: {lesson['validation_source']}",
            "",
        ])
    LESSONS_PATH.write_text("\n".join(lessons_lines), encoding="utf-8")
    state = read_state()
    state["skill_memory_last_refreshed_at"] = now_iso()
    state["skill_memory_registry_count"] = len(registry)
    state["skill_memory_lesson_count"] = len(lessons)
    state["skill_memory_registry_path"] = str(REGISTRY_PATH)
    state["skill_memory_lessons_path"] = str(LESSONS_PATH)
    write_state(state)
    return {
        "registry_count": len(registry),
        "lesson_count": len(lessons),
        "registry_path": str(REGISTRY_PATH),
        "lessons_path": str(LESSONS_PATH),
    }


def skill_operational_memory_status() -> dict:
    state = read_state()
    registry_exists = REGISTRY_PATH.exists()
    lessons_exists = LESSONS_PATH.exists()
    return {
        "registry_exists": registry_exists,
        "lessons_exists": lessons_exists,
        "registry_count": int(state.get("skill_memory_registry_count", 0) or 0),
        "lesson_count": int(state.get("skill_memory_lesson_count", 0) or 0),
        "last_refreshed_at": state.get("skill_memory_last_refreshed_at"),
        "registry_path": state.get("skill_memory_registry_path", str(REGISTRY_PATH)),
        "lessons_path": state.get("skill_memory_lessons_path", str(LESSONS_PATH)),
        "fresh": registry_exists and lessons_exists and bool(state.get("skill_memory_registry_count")),
        "validation_state": "current" if registry_exists and lessons_exists else "stale",
    }


def _score_query_against_record(query: str, record: dict) -> float:
    q = normalize_compare_text(query)
    blob = normalize_compare_text(" ".join([
        record.get("skill_id", ""),
        record.get("title", ""),
        record.get("purpose", ""),
        record.get("best_for", ""),
        record.get("avoid_when", ""),
        record.get("trigger_signals", ""),
        record.get("core_algorithm", ""),
        record.get("typical_failures", ""),
        record.get("recovery_steps", ""),
    ]))
    score = 0.0
    if record["skill_id"].casefold() in q:
        score += 4.0
    if record["title"].casefold() in q:
        score += 2.5
    for token in set(re.findall(r"[a-z0-9_:-]+", q)):
        if len(token) >= 3 and token in blob:
            score += 1.0
    for token in set(re.findall(r"[a-z0-9_:-]+", record.get("trigger_signals", "").casefold())):
        if len(token) >= 3 and token in q:
            score += 0.8
    return score


def skill_operational_recall(query: str, limit: int = 3) -> list[dict]:
    records = installed_skill_records()
    lessons = compile_skill_lessons()
    output = []
    for record in records:
        score = _score_query_against_record(query, record)
        if score <= 0:
            continue
        related_lessons = [lesson for lesson in lessons if lesson["skill_id"] == record["skill_id"]][:3]
        output.append({
            "skill_id": record["skill_id"],
            "title": record["title"],
            "status": record["status"],
            "purpose": record["purpose"],
            "best_for": record["best_for"][:400],
            "avoid_when": record["avoid_when"][:400],
            "trigger_signals": record["trigger_signals"][:400],
            "task_patterns": record["task_patterns"][:400],
            "core_algorithm": record["core_algorithm"][:400],
            "typical_failures": record["typical_failures"][:400],
            "failure_signatures": record["failure_signatures"][:400],
            "diagnostics": record["diagnostics"][:400],
            "recovery_steps": record["recovery_steps"][:400],
            "confidence_state": record["confidence_state"],
            "freshness_state": record["freshness_state"],
            "validation_state": record["validation_state"],
            "last_verified": record["last_verified"],
            "related_skills": record["related_skills"],
            "lessons": related_lessons,
            "score": round(score, 2),
            "evidence_basis": [record["path"]] + [lesson["validation_source"] for lesson in related_lessons],
        })
    output.sort(key=lambda item: item["score"], reverse=True)
    return output[:limit]


def skill_recall_gate(query: str) -> dict:
    candidates = skill_operational_recall(query, limit=5)
    best = candidates[0] if candidates else None
    stale_penalty = 0.0
    if best and best.get("freshness_state") == "stale":
        stale_penalty += 1.1
    if best and best.get("validation_state") in {"inferred", "observed"}:
        stale_penalty += 0.2
    adjusted = (best["score"] - stale_penalty) if best else 0.0
    should_recall = bool(best and adjusted >= 2.2)
    no_skill_reason = None if should_recall else "no strong skill match"
    return {
        "should_recall": should_recall,
        "decision": "recall" if should_recall else "no-skill",
        "confidence": round(adjusted, 2) if best else 0.0,
        "best_candidate": best,
        "candidates": candidates,
        "no_skill_reason": no_skill_reason,
        "adjusted_confidence": round(adjusted, 2) if best else 0.0,
        "stale_penalty": round(stale_penalty, 2),
        "evidence_dominance": "registry" if candidates and not candidates[0].get("lessons") else "lessons",
    }


def skill_operational_decision(query: str) -> dict:
    gate = skill_recall_gate(query)
    candidates = gate["candidates"]
    decision = {
        "current_task": query,
        "candidate_skills": [
            {
                "skill_id": c["skill_id"],
                "title": c["title"],
                "why_may_help": c["purpose"][:180],
                "why_may_not_help": c["avoid_when"][:180],
                "expected_gain": round(c["score"], 2),
                "known_risks": c["typical_failures"][:180],
                "confidence": c["score"],
                "evidence_basis": c.get("evidence_basis", []),
                "best_lesson": c.get("lessons", [])[:1],
            }
            for c in candidates
        ],
        "best_candidate": gate["best_candidate"],
        "no_skill_outcome": gate["no_skill_reason"],
        "decision": gate["decision"],
        "confidence": gate["confidence"],
        "adjusted_confidence": gate.get("adjusted_confidence", gate["confidence"]),
        "stale_penalty": gate.get("stale_penalty", 0.0),
        "evidence_dominance": gate.get("evidence_dominance"),
    }
    return decision


def skill_operational_memory_audit() -> dict:
    status = skill_operational_memory_status()
    registry = installed_skill_records()
    current = {record["skill_id"]: record for record in registry}
    stale = []
    removed = []
    changed = []
    if REGISTRY_PATH.exists():
        raw = REGISTRY_PATH.read_text(encoding="utf-8", errors="ignore")
        for block in raw.split("\n## "):
            if not block.strip() or block.startswith("# "):
                continue
            lines = [line.strip() for line in block.splitlines() if line.strip()]
            skill_id = lines[0].lstrip("# ").strip().splitlines()[0]
            path = None
            source_hash = None
            last_verified = None
            for line in lines[1:]:
                low = line.casefold()
                if low.startswith("- path:"):
                    path = line.split(":", 1)[1].strip()
                elif low.startswith("- source_hash:"):
                    source_hash = line.split(":", 1)[1].strip()
                elif low.startswith("- last_verified:"):
                    last_verified = line.split(":", 1)[1].strip()
            if skill_id not in current:
                removed.append(skill_id)
                continue
            current_record = current[skill_id]
            actual_path = Path(path or current_record["path"])
            if not actual_path.exists():
                removed.append(skill_id)
                continue
            actual_hash = _hash_text(actual_path.read_text(encoding="utf-8", errors="ignore"))
            if source_hash and source_hash != actual_hash:
                changed.append(skill_id)
            if last_verified and actual_path.stat().st_mtime > time.mktime(time.strptime(last_verified[:19], "%Y-%m-%dT%H:%M:%S")):
                stale.append(skill_id)
    return {
        "status": "ok" if not stale and not removed and not changed and status["fresh"] else "warn",
        "stale_skills": stale,
        "removed_skills": removed,
        "changed_skills": changed,
        "registry_count": len(registry),
        "lesson_count": status["lesson_count"],
        "fresh": status["fresh"],
        "status_surface": status,
    }
