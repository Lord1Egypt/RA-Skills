from __future__ import annotations

import copy
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Set, Tuple

from .collector import collect_file_records
from .common import canonical_json, git_commit_sha, now_utc_iso
from .constants import (
    LAYER_EVASION,
    LAYER_SUPPLY,
    MAX_FILE_BYTES,
    SCAN_VERSION,
    TOOL_NAME,
    ENGINE_VERSION,
    POLICY_VERSION,
)
from .context import ContextProfile, classify_finding_surface, context_multiplier
from .finding import add_finding, initial_layer_state
from .models import Finding, ScanStats
from .repo_intel import run_github_osint_precheck
from .scanners import (
    scan_capability_contract_mismatch,
    scan_docs_command_risk,
    scan_exec_and_evasion,
    scan_prompt_semantics,
    scan_secret_exfiltration,
    scan_supply_chain,
)
from .scoring import (
    build_evidence_id,
    classify_finding_kind,
    derive_decision,
    determine_applicable_layers,
    finding_sort_key,
    overall_confidence,
    score_finding,
)


def scan_repository(
    target_repo: Path,
    max_findings: int = 120,
    context_profile: Optional[ContextProfile] = None,
    github_osint_timeout: float = 6.0,
) -> dict:
    target_repo = target_repo.resolve()
    profile = context_profile or ContextProfile()

    findings: list[Finding] = []
    dedupe: Set[Tuple[str, str, int, str]] = set()
    layer_state = initial_layer_state()

    skip_local_scan = False

    precheck = run_github_osint_precheck(target_repo=target_repo, timeout_seconds=github_osint_timeout)
    if precheck.get("decision") == "reject":
        repo_slug = str(precheck.get("repository") or "unknown")
        signals_value = precheck.get("signals")
        signals = signals_value if isinstance(signals_value, list) else []
        if not signals:
            signals = [
                {
                    "source": "github.osint",
                    "term": "high-risk signal",
                    "snippet": str(precheck.get("reason") or "GitHub OSINT precheck marked repository as high-risk."),
                }
            ]

        for idx, signal in enumerate(signals[:5], start=1):
            source = str(signal.get("source") or "github.osint")
            term = str(signal.get("term") or "high-risk signal")
            snippet = str(signal.get("snippet") or term)
            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_SUPPLY,
                rule_id="E_GITHUB_OSINT_HIGH_RISK_SIGNAL",
                category="E",
                severity="high",
                confidence="medium",
                file_path=f"github:{repo_slug}",
                line=idx,
                snippet=snippet,
                why=(
                    "GitHub OSINT precheck flagged high-risk repository signal "
                    f"({source}: {term})."
                ),
                fix=(
                    "Reject installation and require manual security review in an isolated sandbox "
                    "before any execution."
                ),
                tags=["github-osint", "precheck", "external-reputation"],
                exploitability=0.95,
                reach=0.95,
            )
        skip_local_scan = True

    if skip_local_scan:
        records = []
        stats: ScanStats = {
            "total_files_seen": 0,
            "candidate_files": 0,
            "files_scanned": 0,
            "skipped_large_files": 0,
            "skipped_unreadable_files": 0,
            "skipped_large_executable_files": 0,
            "skipped_unreadable_executable_files": 0,
        }
        file_hash_tokens: list[str] = []
    else:
        records, stats, file_hash_tokens = collect_file_records(target_repo)

        for record in records:
            if record["is_prompt_surface"]:
                scan_prompt_semantics(record, findings, dedupe, layer_state)
                scan_docs_command_risk(record, findings, dedupe, layer_state)
            if record["is_executable_surface"]:
                scan_exec_and_evasion(record, findings, dedupe, layer_state)
                scan_secret_exfiltration(record, findings, dedupe, layer_state)

        scan_supply_chain(records, findings, dedupe, layer_state)
        scan_capability_contract_mismatch(records, findings, dedupe, layer_state)

    for finding in findings:
        surface = classify_finding_surface(str(finding.get("file", "")), finding.get("tags", []))
        multiplier = context_multiplier(profile, surface)
        raw_contribution = round(score_finding(finding) * multiplier, 2)
        finding["context"] = {
            "surface": surface,
            "multiplier": multiplier,
            "profile": profile.to_dict(),
        }
        finding["finding_kind"] = classify_finding_kind(finding)
        finding["risk_contribution_raw"] = raw_contribution
        if finding["finding_kind"] == "hygiene":
            finding["risk_contribution"] = round(raw_contribution * 0.25, 2)
        else:
            finding["risk_contribution"] = raw_contribution

    findings_sorted = sorted(findings, key=finding_sort_key)
    if max_findings > 0:
        findings_sorted = findings_sorted[:max_findings]

    commit_sha = git_commit_sha(target_repo)
    for finding in findings_sorted:
        finding["evidence_id"] = build_evidence_id(commit_sha, finding)

    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for finding in findings_sorted:
        severity = str(finding.get("severity", "low"))
        if severity in severity_counts:
            severity_counts[severity] += 1

    actionable_findings = [item for item in findings_sorted if item.get("finding_kind") == "security_actionable"]
    hygiene_findings = [item for item in findings_sorted if item.get("finding_kind") == "hygiene"]

    actionable_risk_raw = sum(float(item.get("risk_contribution", 0.0)) for item in actionable_findings)
    hygiene_risk_raw = sum(float(item.get("risk_contribution", 0.0)) for item in hygiene_findings)
    hygiene_risk_capped = min(15.0, hygiene_risk_raw)
    risk_raw = actionable_risk_raw + hygiene_risk_capped
    has_obfuscation = any(
        str(item.get("category")) == "D" and item.get("finding_kind") == "security_actionable"
        for item in findings_sorted
    )
    obfuscation_bonus = 10 if has_obfuscation else 0

    applicable_layers = determine_applicable_layers(records)
    executed_required_layers = sum(1 for layer in applicable_layers if layer_state.get(layer, {}).get("executed"))
    layer_coverage_ratio = executed_required_layers / float(max(1, len(applicable_layers)))
    file_coverage_ratio = stats["files_scanned"] / float(max(1, stats["candidate_files"]))
    coverage_ratio = min(layer_coverage_ratio, file_coverage_ratio)

    coverage_penalty = 0
    coverage_notes: list[str] = []
    if stats["skipped_large_files"]:
        coverage_notes.append(f"Skipped {stats['skipped_large_files']} large file(s) over {MAX_FILE_BYTES} bytes.")
    if stats["skipped_unreadable_files"]:
        coverage_notes.append(f"Skipped {stats['skipped_unreadable_files']} unreadable/binary file(s).")
    if stats["skipped_large_executable_files"]:
        coverage_penalty += min(24, stats["skipped_large_executable_files"] * 12)
        coverage_notes.append(
            f"Skipped {stats['skipped_large_executable_files']} executable large file(s); confidence reduced."
        )
    if stats["skipped_unreadable_executable_files"]:
        coverage_penalty += min(24, stats["skipped_unreadable_executable_files"] * 12)
        coverage_notes.append(
            f"Skipped {stats['skipped_unreadable_executable_files']} executable unreadable file(s); confidence reduced."
        )

    missing_layers = [layer for layer in sorted(applicable_layers) if not layer_state.get(layer, {}).get("executed")]
    if missing_layers:
        coverage_penalty += min(30, len(missing_layers) * 15)
        coverage_notes.append("Missing required layer execution: " + ", ".join(missing_layers))

    if skip_local_scan:
        coverage_notes.append("GitHub OSINT precheck triggered hard reject; skipped local file scan.")

    if not coverage_notes:
        coverage_notes.append("Coverage complete for configured file classes and applicable layers.")

    partial_coverage = bool(stats["skipped_large_files"] or stats["skipped_unreadable_files"] or missing_layers)
    risk_score = min(100, int(round(risk_raw + obfuscation_bonus + coverage_penalty)))

    suggested_decision = derive_decision(
        risk_score=risk_score,
        actionable_findings=actionable_findings,
        hygiene_findings=hygiene_findings,
        coverage_ratio=coverage_ratio,
        partial_coverage=partial_coverage,
    )
    confidence = overall_confidence(findings_sorted, coverage_ratio)

    highlights: list[dict] = []
    for finding in findings_sorted:
        if finding.get("finding_kind") != "security_actionable":
            continue
        if finding.get("severity") not in {"medium", "high", "critical"}:
            continue
        highlights.append(
            {
                "evidence_id": finding["evidence_id"],
                "layer": finding["layer"],
                "finding_kind": finding.get("finding_kind"),
                "severity": finding["severity"],
                "category": finding["category"],
                "file": finding["file"],
                "line": finding["line"],
                "summary": (
                    f"{finding['evidence_id']} [{finding['severity']}/{finding['category']}] "
                    f"{finding['file']}:{finding['line']} - {finding['why']}"
                ),
            }
        )
    highlights = highlights[:12]

    required_highlight_refs = [
        item["evidence_id"] for item in highlights if item["severity"] in {"critical", "high"}
    ]

    file_hash_tokens_sorted = sorted(file_hash_tokens)
    repo_fingerprint = hashlib.sha256("\n".join(file_hash_tokens_sorted).encode("utf-8")).hexdigest()

    run = {
        "run_id": f"ssa-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{repo_fingerprint[:12]}",
        "engine_version": ENGINE_VERSION,
        "policy_version": POLICY_VERSION,
        "generated_at_utc": now_utc_iso(),
        "commit_sha": commit_sha,
    }

    scan_result: dict = {
        "version": SCAN_VERSION,
        "tool": TOOL_NAME,
        "target_repo": str(target_repo),
        "run": run,
        "precheck": precheck,
        "context_profile": profile.to_dict(),
        "integrity": {
            "repo_fingerprint": repo_fingerprint,
            "scan_fingerprint": "pending",
        },
        "layers": layer_state,
        "summary": {
            "total_files_seen": stats["total_files_seen"],
            "candidate_files": stats["candidate_files"],
            "files_scanned": stats["files_scanned"],
            "skipped_large_files": stats["skipped_large_files"],
            "skipped_unreadable_files": stats["skipped_unreadable_files"],
            "skipped_large_executable_files": stats["skipped_large_executable_files"],
            "skipped_unreadable_executable_files": stats["skipped_unreadable_executable_files"],
            "applicable_layers": sorted(applicable_layers),
            "coverage_ratio": round(coverage_ratio, 4),
            "partial_coverage": partial_coverage,
            "coverage_notes": coverage_notes,
            "finding_count": len(findings_sorted),
            "actionable_finding_count": len(actionable_findings),
            "hygiene_finding_count": len(hygiene_findings),
            "severity_counts": severity_counts,
        },
        "scoring": {
            "risk_raw": round(risk_raw, 2),
            "actionable_risk_raw": round(actionable_risk_raw, 2),
            "hygiene_risk_raw": round(hygiene_risk_raw, 2),
            "hygiene_risk_capped": round(hygiene_risk_capped, 2),
            "obfuscation_bonus_applied": bool(obfuscation_bonus),
            "coverage_penalty": int(coverage_penalty),
            "risk_score": risk_score,
            "confidence": confidence,
            "suggested_decision": suggested_decision,
        },
        "required_highlight_evidence_ids": required_highlight_refs,
        "highlights": highlights,
        "findings": findings_sorted,
    }

    fingerprint_payload = copy.deepcopy(scan_result)
    fingerprint_payload["integrity"]["scan_fingerprint"] = ""
    scan_result["integrity"]["scan_fingerprint"] = hashlib.sha256(
        canonical_json(fingerprint_payload).encode("utf-8")
    ).hexdigest()

    return scan_result
