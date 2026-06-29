#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

KEYWORDS = {
    "Source / Data Mapper": ["search", "collect", "source", "web", "database", "pdf", "extract"],
    "Evidence Verifier": ["verify", "fact", "evidence", "official", "citation", "audit"],
    "Domain Producer / Analyst": ["analyze", "compare", "rank", "recommend", "risk", "strategy", "write", "document"],
    "Workflow Orchestrator": ["workflow", "branch", "loop", "rerun", "approval", "process"],
    "Independent Acceptance Reviewer": ["review", "qa", "accept", "approval", "reject"],
    "Runtime Adapter": ["deploy", "package", "codex", "manifest", "prompt template"]
}

def score_roles(text: str) -> dict[str, int]:
    low = text.lower()
    return {r: sum(1 for w in ws if w.lower() in low) for r, ws in KEYWORDS.items()}

def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def main() -> int:
    parser = argparse.ArgumentParser(description="Draft a starter Skill2Team team from a plain-language brief.")
    parser.add_argument("source", help="Text file containing the skill or workflow description.")
    parser.add_argument("--execution-path", choices=["direct-skill", "meta-team-first"], default="direct-skill")
    parser.add_argument("--target-runtime", choices=["codex"], default="codex")
    args = parser.parse_args()

    text = Path(args.source).read_text(encoding="utf-8")
    scores = score_roles(text)
    selected = [
        "Entry Coordinator / Orchestrator",
        "Source Mapper",
        "Architecture Designer",
        "Workflow Orchestrator / Producer",
        "Independent Acceptance Reviewer",
    ]
    if args.target_runtime == "codex" or scores.get("Runtime Adapter", 0) > 0:
        selected.append("Runtime Adapter")
    elif scores.get("Evidence Verifier", 0) > 0:
        selected.insert(3, "Evidence Verifier")

    # Keep starter draft compact. Stronger evidence can expand later with explicit rationale.
    selected = selected[:6]
    team = []
    for role in dict.fromkeys(selected):
        team.append({
            "agent_id": slug(role),
            "display_name": role,
            "mission": f"Own {role.lower()} responsibilities extracted from the brief.",
            "responsibilities": [f"Handle {role.lower()} tasks"],
            "non_responsibilities": ["Do not take over adjacent work without a handoff contract"],
            "authority": ["May request missing inputs", "May escalate blocked decisions"],
            "owned_skills": [],
            "shared_skills": [],
            "allowed_tools": [],
            "denied_tools": [],
            "risk_level": "medium"
        })

    work_orders = [
        {"owner_role": "S2T Lead", "task": "Integrate route outputs and own final synthesis.", "expected_output": "synthesis_notes", "gate": "all required route outputs present"},
        {"owner_role": "Source Mapper", "task": "Inventory the provided description and extract workflow anchors.", "expected_output": "source_inventory_and_workflow_anchors", "gate": "source status recorded"},
        {"owner_role": "Architecture Designer", "task": "Draft Agent Architecture Map and count rationale.", "expected_output": "agent_architecture_map", "gate": "architecture is not confused with workflow"},
        {"owner_role": "Workflow Orchestrator", "task": "Draft Workflow Orchestration Map and rerun/resume notes.", "expected_output": "workflow_orchestration_map", "gate": "workflow nodes do not automatically become agents"},
        {"owner_role": "Quality Reviewer", "task": "Flag risks, missing gates, and whether the count is justified.", "expected_output": "risk_and_count_review", "gate": "producer does not self-approve"},
    ]
    meta_first = args.execution_path == "meta-team-first"
    execution_path_log = {
        "selected_route": "brief-to-team",
        "delivery": "design",
        "model_invocation_policy": "OpenAI Codex default; direct model API calls only as labeled API-run role simulation",
        "execution_path": args.execution_path,
        "meta_team_first_done": meta_first,
        "source_status": "present",
        "target_runtime": args.target_runtime,
        "current_run_fanout_status": "blocked_no_real_codex_meta_team" if meta_first else "direct-skill-not-requested",
        "target_subagent_fanout_supported": "runtime-dependent",
        "execution_mode": "blocked" if meta_first else "direct_skill",
        "fallback_declaration": "meta-team-first blocked; real Codex meta-team activation/fan-out was not confirmed; fallback role-play is not permitted" if meta_first else "not_applicable_direct_skill",
        "synthesis_owner": "S2T Lead" if meta_first else "Skill2Team direct skill"
    }
    out = {
        "mode": "brief_to_team",
        "warning": "Starter draft. Confirm workflow, risks, runtime, and agent-count rationale before deployment.",
        "execution_path_log": execution_path_log,
        "detected_role_scores": scores,
        "agent_count_policy": "Prefer 5-6 top-level agents for nontrivial teams; justify fewer or more.",
        "architecture_map": {
            "selected_pattern": "coordinator_specialists",
            "top_level_agent_count": len(team),
            "count_rationale": "starter draft aims for 5-6 top-level agents unless the brief is simple"
        },
        "workflow_orchestration_map": {
            "note": "Draft runtime flow separately from agent architecture: sequence, branch, loop, gate, human wait, checkpoint/resume, and terminal boundaries."
        },
        "suggested_team": team,
        "next_questions": [
            "Please provide or confirm the source SKILL.md / team / workflow brief that should be converted.",
            "Confirm that the target runtime is Codex and that model execution defaults to OpenAI Codex rather than direct API calls.",
            "Which responsibilities must remain independently reviewed or approved?",
            "Can the final team fit in 5-6 top-level agents? If not, what strong requirement justifies another count?"
        ]
    }
    if meta_first:
        out["meta_team_execution"] = {
            **execution_path_log,
            "assigned_roles": [w["owner_role"] for w in work_orders],
            "work_orders": work_orders,
            "local_resource_allocation_status": "not_needed_for_plain_description",
            "synthesis_owner": "S2T Lead"
        }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
