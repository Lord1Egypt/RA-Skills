from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from lib.discovery import ensure_directory


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_skill_report(
    target,
    stage: str,
    static_result: dict[str, Any],
    ai_result: dict[str, Any],
    policy_result: dict[str, Any],
    policy: dict[str, Any],
) -> dict[str, Any]:
    finding_count = len(static_result.get("findings", []))
    summary = build_summary(target, stage, policy_result, ai_result, finding_count, policy)
    risk_signature = build_risk_signature(target, stage, static_result, ai_result, policy_result)
    return {
        "generated_at": utc_now_iso(),
        "stage": stage,
        "skill": {
            "name": target.name,
            "path": str(target.path),
            "source_kind": target.source_kind,
            "declared_purpose": target.declared_purpose,
            "metadata": target.metadata,
            "provenance": target.provenance,
        },
        "inventory": {
            "file_count": len(target.files),
            "files": [
                {
                    "path": file_info.relative_path,
                    "size": file_info.size,
                    "sha256": file_info.sha256,
                    "is_text": file_info.is_text,
                    "is_symlink": file_info.is_symlink,
                    "content_truncated": file_info.content_truncated,
                }
                for file_info in target.files
            ],
        },
        "static_analysis": static_result,
        "ai_audit": ai_result,
        "decision": policy_result,
        "summary": summary,
        "risk_signature": risk_signature,
    }


def build_bundle(stage: str, reports: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "generated_at": utc_now_iso(),
        "stage": stage,
        "skills": reports,
    }


def write_json_report(bundle: dict[str, Any], reports_dir: Path, filename_prefix: str) -> Path:
    ensure_directory(reports_dir)
    filename = f"{filename_prefix}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    path = reports_dir / filename
    with path.open("w", encoding="utf-8") as handle:
        json.dump(bundle, handle, indent=2, ensure_ascii=False)
    return path


def print_text_summary(bundle: dict[str, Any]) -> None:
    stage = bundle["stage"]
    reports = bundle["skills"]
    print("=" * 72)
    print(f"SkillGuard report | stage={stage} | targets={len(reports)}")
    print("=" * 72)
    for report in reports:
        decision = report["decision"]
        ai_result = report["ai_audit"]
        static_findings = report["static_analysis"].get("findings", [])
        icon = {
            "PASS": "PASS",
            "WARN": "WARN",
            "BLOCK": "BLOCK",
            "QUARANTINE": "QUARANTINE",
        }[decision["recommendation"]]
        print(
            f"[{icon}] {report['skill']['name']} | risk={decision['risk_score']} "
            f"| static={decision['static_score']} | ai={decision['ai_score']}"
        )
        print(f"  headline: {report['summary']['headline']}")
        print(f"  purpose: {report['skill']['declared_purpose']}")
        print(f"  path: {report['skill']['path']}")
        if static_findings:
            for finding in static_findings[:6]:
                evidence = "; ".join(finding.get("evidence", [])[:2])
                print(f"  - {finding['title']} @ {finding['file']} :: {evidence}")
        else:
            print("  - no static findings")
        if ai_result.get("summary"):
            print(f"  ai: {ai_result['summary']}")
        if decision.get("reasons"):
            print(f"  reasons: {', '.join(decision['reasons'][:4])}")
        print(f"  signature: {report['risk_signature']}")
        print("-" * 72)


def build_summary(target, stage: str, policy_result: dict[str, Any], ai_result: dict[str, Any], finding_count: int, policy: dict[str, Any]) -> dict[str, Any]:
    templates = policy.get("report_templates", {})
    context = {
        "skill_name": target.name,
        "stage": stage,
        "recommendation": policy_result["recommendation"],
        "risk_score": policy_result["risk_score"],
        "declared_purpose": target.declared_purpose,
        "finding_count": finding_count,
    }
    headline = templates.get("headline", "{recommendation} {skill_name} risk={risk_score}").format(**context)
    summary = templates.get("summary", "{skill_name} has {finding_count} finding(s).").format(**context)
    operator_note = templates.get("operator_note", "")
    return {
        "headline": headline,
        "summary": summary,
        "operator_note": operator_note,
        "ai_summary": ai_result.get("summary"),
    }


def build_risk_signature(target, stage: str, static_result: dict[str, Any], ai_result: dict[str, Any], policy_result: dict[str, Any]) -> str:
    normalized = {
        "skill": target.name,
        "stage": stage,
        "static_rule_ids": sorted(finding.get("rule_id", "") for finding in static_result.get("findings", [])),
        "ai_recommendation": ai_result.get("recommendation"),
        "ai_threats": ai_result.get("threats", []),
        "decision": policy_result.get("recommendation"),
        "risk_score": policy_result.get("risk_score"),
        "critical_rules": policy_result.get("critical_rules", []),
    }
    payload = json.dumps(normalized, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]
