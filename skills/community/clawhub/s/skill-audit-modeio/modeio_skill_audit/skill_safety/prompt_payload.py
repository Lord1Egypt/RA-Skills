from __future__ import annotations

import json
from typing import Any, Dict, Optional


def build_prompt_payload(
    scan_result: Dict[str, Any],
    target_repo: str,
    context: Optional[str],
    focus: Optional[str],
    include_full_findings: bool,
) -> str:
    highlights = scan_result.get("highlights", [])
    required_refs = scan_result.get("required_highlight_evidence_ids", [])

    payload: Dict[str, Any] = {
        "target_repo": target_repo,
        "context": context or "",
        "focus": focus or "",
        "scan_version": scan_result.get("version"),
        "run": scan_result.get("run", {}),
        "context_profile": scan_result.get("context_profile", {}),
        "script_scan_summary": scan_result.get("summary", {}),
        "script_scan_scoring": scan_result.get("scoring", {}),
        "script_scan_precheck": scan_result.get("precheck", {}),
        "script_scan_integrity": scan_result.get("integrity", {}),
        "script_scan_layers": scan_result.get("layers", {}),
        "required_highlight_evidence_ids": required_refs,
        "script_scan_highlights": highlights,
    }
    if include_full_findings:
        payload["script_scan_findings"] = scan_result.get("findings", [])

    lines: list[str] = []
    lines.append("Skill Safety Assessment prompt input")
    lines.append("Use contract: skill-audit/references/prompt-contract.md")
    lines.append("")
    lines.append("SCRIPT_SCAN_HIGHLIGHTS")
    if highlights:
        for item in highlights:
            lines.append(f"- {item.get('summary')}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("SCRIPT_SCAN_JSON")
    lines.append("```json")
    lines.append(json.dumps(payload, ensure_ascii=False, indent=2))
    lines.append("```")
    return "\n".join(lines)
