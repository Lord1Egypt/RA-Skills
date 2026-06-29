#!/usr/bin/env python3
"""Generate platform-specific agent deployment skeletons from a Skill2Team team plan."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_AGENTS = [
    {"agent_id":"entry-coordinator","display_name":"Entry Coordinator / Orchestrator","mission":"Route work, manage state, and synthesize results.","owned_skills":["routing","orchestration"],"tools_policy":{"allow":["read","write"],"deny":[]}},
    {"agent_id":"source-mapper","display_name":"Source Mapper","mission":"Inventory source assets and extract the original workflow.","owned_skills":["inventory","workflow-extraction"],"tools_policy":{"allow":["read","write"],"deny":["destructive-write"]}},
    {"agent_id":"architecture-designer","display_name":"Architecture Designer","mission":"Produce the Agent Architecture Map, role boundaries, skill allocation, and count rationale.","owned_skills":["agent-architecture","role-boundaries","skill-allocation"],"tools_policy":{"allow":["read","write"],"deny":[]}},
    {"agent_id":"workflow-orchestrator","display_name":"Workflow Orchestrator / Producer","mission":"Produce the Workflow Orchestration Map and primary workflow deliverables.","owned_skills":["workflow-orchestration","composition","control-flow"],"tools_policy":{"allow":["read","write"],"deny":[]}},
    {"agent_id":"acceptance-reviewer","display_name":"Independent Acceptance Reviewer","mission":"Independently review quality, risks, architecture/workflow separation, and count justification.","owned_skills":["review","evaluation"],"tools_policy":{"allow":["read"],"deny":["write","edit","apply_patch","exec"]}}
]

WORKFLOW_PRESERVATION_CHOICES = [
    "preserve_as_human_wait",
    "convert_to_reviewer_gate",
    "auto_advance_with_audit",
    "remove_as_redundant",
]

HUMAN_INTERACTION_EXECUTION_MODES = [
    "preserve_source_human_interaction_steps",
    "selective_human_intervention_retention",
    "fully_automated_with_audit",
]

WORKFLOW_PRESERVATION_FIELD_ALIASES = {
    "workflow_nodes": ["workflow_nodes", "nodes"],
    "workflow_edges": ["workflow_edges", "edges"],
    "stage_mappings": ["stage_mappings", "source_stage_mappings", "stage_to_agent_mappings"],
    "stage_internal_deliverables": [
        "stage_internal_deliverables",
        "embedded_stage_deliverables",
        "internal_deliverables",
        "stage_artifacts",
    ],
    "human_intervention_points": [
        "human_intervention_points",
        "human_waits",
        "human_decision_points",
        "manual_gates",
        "approval_points",
    ],
    "human_intervention_inventory_status": ["human_intervention_inventory_status"],
    "human_intervention_policy": ["human_intervention_policy"],
    "user_input_nodes": [
        "user_input_nodes",
        "required_user_input_nodes",
        "interactive_input_nodes",
        "source_required_user_inputs",
        "startup_input_nodes",
    ],
    "checkpoint_resume_points": ["checkpoint_resume_points", "checkpoints", "resume_points"],
    "gate_points": ["gate_points", "gates", "review_gates"],
}

WORKFLOW_PRESERVATION_REQUIRED_FIELDS = [
    "workflow_nodes",
    "workflow_edges",
    "stage_mappings",
    "stage_internal_deliverables",
    "human_intervention_points",
    "user_input_nodes",
]

SOURCE_STARTUP_REFERENCE_KEYS = [
    "source_startup_page",
    "source_startup_prompt",
    "source_welcome_page",
    "startup_page",
    "welcome_page",
    "entry_startup_reference",
]


def workflow_plan_value(plan: dict[str, Any], keys: list[str], default: Any = None) -> Any:
    for key in keys:
        if key in plan:
            return plan[key]
    for container_name in ("workflow_orchestration", "workflow", "original_workflow", "flow_control"):
        container = plan.get(container_name)
        if isinstance(container, dict):
            for key in keys:
                if key in container:
                    return container[key]
    return default


def workflow_plan_has_any(plan: dict[str, Any], keys: list[str]) -> bool:
    sentinel = object()
    return workflow_plan_value(plan, keys, sentinel) is not sentinel


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def source_inventory_payload(plan: dict[str, Any]) -> Any:
    for key in (
        "source_inventory",
        "source_assets",
        "asset_inventory",
        "local_resource_inventory",
        "resource_inventory",
        "source_resources",
    ):
        value = plan.get(key)
        if value not in (None, "", [], {}):
            return value
    return "not_provided_in_plan"


def source_has_meaningful_local_resources(source_inventory: Any) -> bool:
    if source_inventory == "not_provided_in_plan":
        return False
    if isinstance(source_inventory, dict):
        for key in ("references", "scripts", "templates", "assets", "examples", "data", "agents"):
            if source_inventory.get(key):
                return True
        return bool(source_inventory)
    return bool(source_inventory)


def owner_agent_for_resource(agents: list[dict[str, Any]], group: str) -> str:
    preferences = {
        "references": ["source", "workflow", "orchestrator", "entry"],
        "scripts": ["state", "tool", "quality", "review", "runtime"],
        "templates": ["prompt", "runtime", "entry", "workflow"],
        "assets": ["prompt", "image", "designer", "presentation", "runtime"],
        "examples": ["quality", "review", "source"],
        "data": ["source", "state", "runtime"],
        "agents": ["runtime", "entry", "architecture"],
        "root_files": ["runtime", "source", "entry"],
        "config": ["runtime", "entry"],
        "release_metadata": ["runtime", "quality", "review"],
    }
    agent_rows = [
        (
            agent_id(a),
            " ".join(
                str(x).lower()
                for x in [
                    agent_id(a),
                    display(a),
                    mission(a),
                    " ".join(a.get("owned_skills", [])),
                ]
            ),
        )
        for a in agents
    ]
    for needle in preferences.get(group, ["source", "entry"]):
        for aid, haystack in agent_rows:
            if needle in haystack:
                return aid
    return agent_rows[0][0] if agent_rows else "entry-agent"


def resource_class_for_group(group: str) -> str:
    return {
        "references": "policy/reference",
        "scripts": "script/tool",
        "templates": "template",
        "assets": "asset library",
        "examples": "example",
        "data": "data/index",
        "agents": "config",
        "root_files": "release metadata",
        "config": "config",
        "release_metadata": "release metadata",
    }.get(group, "unknown")


def resource_migration_action(group: str, bundle_mode: str) -> str:
    if bundle_mode == "bundle":
        return {
            "references": "copy as shared reference",
            "scripts": "copy and wrap as tool with owner gate",
            "templates": "copy as template asset",
            "assets": "copy as visual/style asset when license-safe",
            "examples": "copy as example-only reference",
            "data": "copy as data/index resource",
            "agents": "copy as source config reference",
            "root_files": "copy selected release metadata",
        }.get(group, "copy if safe")
    return {
        "references": "expose as shared reference if available; bundle required for offline runtime",
        "scripts": "wrap as tool only when available; bundle required for deterministic runtime",
        "templates": "expose as template-only resource; bundle required for faithful prompt generation",
        "assets": "expose as visual-only resource; bundle when downstream rendering depends on it",
        "examples": "keep as example-only reference or defer",
        "data": "expose or bundle as data/index resource",
        "agents": "record as source config reference",
        "root_files": "record release metadata",
    }.get(group, "record or defer")


def resource_evidence_status(group: str) -> str:
    return {
        "references": "authoritative evidence when the source workflow treats the reference as policy",
        "scripts": "tool-only until owner gate validates outputs",
        "templates": "template-only",
        "assets": "visual-only unless explicitly defined as evidence",
        "examples": "example-only",
        "data": "data/index-only until verified by owner gate",
        "agents": "config/reference-only",
        "root_files": "packaging-only",
    }.get(group, "unknown")


def local_resource_allocation_payload(
    plan: dict[str, Any],
    agents: list[dict[str, Any]],
    *,
    team_id: str,
    team_kind: str,
    source_skill: str | None,
    target: str,
    entry: str,
    route: str,
    delivery: str,
    source_root: str | None,
    bundle_mode: str,
    bundled_files: list[str] | None = None,
    bundle_blockers: list[str] | None = None,
) -> dict[str, Any]:
    source_inventory = source_inventory_payload(plan)
    provided = plan.get("local_resource_allocation") or plan.get("local_resource_allocation_map")
    if isinstance(provided, list):
        allocations = provided
    else:
        allocations = []
        if isinstance(source_inventory, dict):
            for group, value in source_inventory.items():
                if value in (None, "", [], {}):
                    continue
                allocations.append({
                    "resource": group,
                    "resource_items": as_list(value) if not isinstance(value, dict) else value,
                    "resource_class": resource_class_for_group(group),
                    "original_role": f"source package {group}",
                    "owner_agent": owner_agent_for_resource(agents, group),
                    "access_level": "shared read-only" if group != "scripts" else "owner-gated tool access",
                    "evidence_status": resource_evidence_status(group),
                    "allowed_use": "Use only for the role recorded by resource_class, evidence_status, and owner gate.",
                    "forbidden_use": "Do not infer scientific/domain truth, runtime permissions, or visual claims from this resource unless the source workflow explicitly makes it authoritative.",
                    "gate": "owner_agent plus independent reviewer when the resource affects generated prompts, tool outputs, claims, or execution side effects",
                    "migration_action": resource_migration_action(group, bundle_mode),
                })
    meaningful = source_has_meaningful_local_resources(source_inventory)
    blockers = list(bundle_blockers or [])
    if meaningful and not allocations:
        blockers.append("source local resources are present, but no local_resource_allocation map could be derived")
    if meaningful and bundle_mode == "manifest" and not source_root:
        blockers.append("source resources were inventoried but not bundled and no accessible source_root was recorded; rerun with --source-root or --resource-copy-mode bundle")
    if meaningful and not source_root and bundle_mode == "bundle":
        blockers.append("--resource-copy-mode bundle was requested but no --source-root or plan source_root was provided")
    gate_status = "passed" if not blockers else "blocked"
    return {
        "schema_version": "s2t-local-resource-allocation-v1",
        "managed_by": "skill2team",
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target.replace("_", "-"),
        "entry_agent_id": entry,
        "route": route,
        "delivery": delivery,
        "source_root": source_root,
        "resource_copy_mode": bundle_mode,
        "source_inventory": source_inventory,
        "local_resources_present": meaningful,
        "allocation_map": allocations,
        "bundled_resource_files": bundled_files or [],
        "resource_gate_status": gate_status,
        "resource_gate_blockers": blockers,
    }


def safe_resource_destination(base: Path, rel: Path) -> Path:
    dest = (base / rel).resolve()
    base_resolved = base.resolve()
    if base_resolved != dest and base_resolved not in dest.parents:
        raise ValueError(f"Unsafe resource path outside bundle root: {rel}")
    return dest


def source_startup_reference(plan: dict[str, Any]) -> Any:
    for key in SOURCE_STARTUP_REFERENCE_KEYS:
        value = workflow_plan_value(plan, [key], None)
        if value not in (None, "", [], {}):
            return value
    return "not_provided_in_plan"


def normalized_human_intervention_policy(raw: Any) -> dict[str, Any]:
    policy = {
        "initial_user_choice_required": True,
        "initial_choice_timing": "before_S0_or_before_the_first_real_migrated_workflow_stage",
        "default_execution_mode": "preserve_source_human_interaction_steps",
        "selected_execution_mode": "preserve_source_human_interaction_steps",
        "execution_modes": HUMAN_INTERACTION_EXECUTION_MODES,
        "default": "preserve_all_source_mandated_human_waits_and_choices",
        "ask_user_before_auto_advancing": True,
        "allowed_choices": WORKFLOW_PRESERVATION_CHOICES,
        "user_input_node_policy": "preserve_required_user_input_nodes_as_entry_agent_questions_or_human_wait_edges_unless_the_user_explicitly_selects_safe_automation",
        "between_step_retention_rule": "For each source human intervention point, record the upstream step that pauses, the downstream step that resumes, and whether the selected action is preserve, reviewer gate, audited automation, or removal.",
        "fully_automated_requires": [
            "explicit_user_selection",
            "source_allows_automation_or_reviewer_gate",
            "audit_record_for_each_auto_advanced_human_point",
        ],
        "user_overrides": [],
        "choice_source": "default_preserve_when_no_explicit_user_override",
    }
    if isinstance(raw, dict):
        policy.update(raw)
    elif raw not in (None, "", [], {}):
        text = str(raw)
        if text in HUMAN_INTERACTION_EXECUTION_MODES:
            policy["selected_execution_mode"] = text
            policy["choice_source"] = "plan_string_value"
        else:
            policy["policy_note"] = text
    if policy.get("selected_execution_mode") not in HUMAN_INTERACTION_EXECUTION_MODES:
        policy["selected_execution_mode"] = policy["default_execution_mode"]
    if policy["selected_execution_mode"] == "fully_automated_with_audit":
        policy["ask_user_before_auto_advancing"] = True
        if policy.get("choice_source") == "default_preserve_when_no_explicit_user_override":
            policy["choice_source"] = "explicit_user_selection_required"
    return policy


def copy_source_resources(out: Path, source_root: str | None, source_inventory: Any, bundle_mode: str) -> tuple[list[str], list[str]]:
    if bundle_mode != "bundle":
        return [], []
    if not source_root:
        return [], ["source_root is required for resource bundling"]
    src_root = Path(source_root).resolve()
    if not src_root.exists() or not src_root.is_dir():
        return [], [f"source_root does not exist or is not a directory: {source_root}"]
    bundle_root = out / "source-resources"
    copied: list[str] = []
    blockers: list[str] = []
    candidate_rels: list[Path] = []
    if isinstance(source_inventory, dict):
        for group, value in source_inventory.items():
            group_path = src_root / group
            if group_path.exists():
                candidate_rels.append(Path(group))
                continue
            for item in as_list(value) if not isinstance(value, dict) else []:
                if isinstance(item, str) and item and not item.startswith("<") and not item.endswith(">"):
                    if group == "root_files":
                        candidate_rels.append(Path(item))
                    elif Path(item).suffix or "/" in item or "\\" in item:
                        candidate_rels.append(Path(group) / item if not Path(item).is_absolute() else Path(item))
    else:
        for group in ("references", "scripts", "templates", "assets", "examples", "data", "agents"):
            if (src_root / group).exists():
                candidate_rels.append(Path(group))
    seen: set[str] = set()
    for rel in candidate_rels:
        if rel.is_absolute():
            try:
                rel = rel.resolve().relative_to(src_root)
            except ValueError:
                blockers.append(f"skipped absolute path outside source_root: {rel}")
                continue
        key = rel.as_posix()
        if key in seen:
            continue
        seen.add(key)
        src = (src_root / rel).resolve()
        if not src.exists():
            blockers.append(f"listed resource path not found under source_root: {key}")
            continue
        dest = safe_resource_destination(bundle_root, rel)
        if src.is_dir():
            shutil.copytree(src, dest, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", ".git", ".DS_Store", "*.pyc", "*.pyo"))
            copied.extend(str(p.relative_to(out)).replace("\\", "/") for p in dest.rglob("*") if p.is_file())
        else:
            ensure(dest.parent)
            shutil.copy2(src, dest)
            copied.append(str(dest.relative_to(out)).replace("\\", "/"))
    return sorted(set(copied)), blockers


def workflow_preservation_payload(plan: dict[str, Any]) -> dict[str, Any]:
    source_workflow = workflow_plan_value(
        plan,
        ["source_workflow", "original_workflow", "workflow"],
        "not_provided_in_plan",
    )
    presence = {
        field: workflow_plan_has_any(plan, aliases)
        for field, aliases in WORKFLOW_PRESERVATION_FIELD_ALIASES.items()
    }
    blockers = [
        f"{field} missing from plan; package cannot prove source workflow preservation"
        for field in WORKFLOW_PRESERVATION_REQUIRED_FIELDS
        if not presence[field]
    ]
    if source_workflow == "not_provided_in_plan":
        blockers.append("source_workflow/original_workflow missing from plan")
    policy = normalized_human_intervention_policy(workflow_plan_value(
        plan,
        WORKFLOW_PRESERVATION_FIELD_ALIASES["human_intervention_policy"],
        None,
    ))
    return {
        "schema_version": "s2t-workflow-preservation-v1",
        "source_workflow": source_workflow,
        "source_startup_reference": source_startup_reference(plan),
        "workflow_nodes": as_list(workflow_plan_value(plan, WORKFLOW_PRESERVATION_FIELD_ALIASES["workflow_nodes"], [])),
        "workflow_edges": as_list(workflow_plan_value(plan, WORKFLOW_PRESERVATION_FIELD_ALIASES["workflow_edges"], [])),
        "stage_mappings": as_list(workflow_plan_value(plan, WORKFLOW_PRESERVATION_FIELD_ALIASES["stage_mappings"], [])),
        "stage_internal_deliverables": as_list(workflow_plan_value(plan, WORKFLOW_PRESERVATION_FIELD_ALIASES["stage_internal_deliverables"], [])),
        "human_intervention_points": as_list(workflow_plan_value(plan, WORKFLOW_PRESERVATION_FIELD_ALIASES["human_intervention_points"], [])),
        "user_input_nodes": as_list(workflow_plan_value(plan, WORKFLOW_PRESERVATION_FIELD_ALIASES["user_input_nodes"], [])),
        "human_intervention_inventory_status": workflow_plan_value(
            plan,
            WORKFLOW_PRESERVATION_FIELD_ALIASES["human_intervention_inventory_status"],
            "missing",
        ),
        "human_intervention_policy": policy,
        "checkpoint_resume_points": as_list(workflow_plan_value(plan, WORKFLOW_PRESERVATION_FIELD_ALIASES["checkpoint_resume_points"], [])),
        "gate_points": as_list(workflow_plan_value(plan, WORKFLOW_PRESERVATION_FIELD_ALIASES["gate_points"], [])),
        "field_presence": presence,
        "preservation_gate_status": "blocked" if blockers else "passed",
        "preservation_gate_blockers": blockers,
        "rule": (
            "A workflow stage may have internal duties and named deliverables before a public handoff. "
            "Do not replace those duties with a summary or with only a human-wait edge. "
            "Required user input nodes must remain entry-agent questions or human-wait edges unless the user explicitly selected safe automation."
        ),
    }


def compact_text(value: Any, limit: int = 260) -> str:
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def stable_constraint_id(source_field: str, index: int, summary: str) -> str:
    digest = hashlib.sha1(f"{source_field}:{index}:{summary}".encode("utf-8")).hexdigest()[:10]
    safe_field = re.sub(r"[^a-z0-9]+", "-", source_field.lower()).strip("-") or "constraint"
    return f"src-{safe_field}-{digest}"


def owner_candidates_from(raw: Any) -> list[str]:
    if not isinstance(raw, dict):
        return []
    owners: list[str] = []
    for key in (
        "owner_agent", "owner", "agent_id", "assigned_agent", "producer_agent",
        "responsible_agent", "reviewer_agent", "gate_owner", "target_agent",
    ):
        value = raw.get(key)
        if value in (None, "", [], {}):
            continue
        owners.extend(str(v) for v in as_list(value))
    return sorted(set(owners))


def normalize_source_runtime_constraint(raw: Any, *, source_field: str, constraint_class: str, index: int) -> dict[str, Any]:
    if isinstance(raw, dict):
        summary = (
            raw.get("summary")
            or raw.get("constraint")
            or raw.get("requirement")
            or raw.get("description")
            or raw.get("name")
            or raw.get("id")
            or raw
        )
        severity = raw.get("severity", "required")
        decision = raw.get("decision") or raw.get("action") or raw.get("policy")
        source_ref = raw.get("source") or raw.get("source_ref") or raw.get("stage") or raw.get("node_id") or raw.get("edge_id")
    else:
        summary = raw
        severity = "required"
        decision = None
        source_ref = None
    summary_text = compact_text(summary)
    payload = {
        "constraint_id": stable_constraint_id(source_field, index, summary_text),
        "constraint_class": constraint_class,
        "source_field": source_field,
        "summary": summary_text,
        "severity": str(severity),
        "owner_candidates": owner_candidates_from(raw),
        "materialization_required": True,
        "runtime_effect": "must be visible in design maps, package contracts, agent profiles, and generated runtime instructions when it affects execution",
        "reexecution_on_missing": True,
    }
    if decision not in (None, "", [], {}):
        payload["decision_or_policy"] = compact_text(decision)
    if source_ref not in (None, "", [], {}):
        payload["source_ref"] = compact_text(source_ref, 120)
    return payload


def constraint_class_for_source_field(field: str) -> str:
    return {
        "stage_internal_deliverables": "stage_internal_deliverable",
        "human_intervention_points": "human_intervention",
        "user_input_nodes": "required_user_input_node",
        "checkpoint_resume_points": "checkpoint_resume",
        "gate_points": "gate_or_review",
        "workflow_nodes": "workflow_node",
        "workflow_edges": "workflow_edge",
    }.get(field, "source_runtime_constraint")


def source_derived_runtime_constraints(plan: dict[str, Any], preservation: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    preservation = preservation or workflow_preservation_payload(plan)
    raw_rows: list[tuple[str, str, Any]] = []
    for field in (
        "stage_internal_deliverables",
        "human_intervention_points",
        "user_input_nodes",
        "checkpoint_resume_points",
        "gate_points",
    ):
        for raw in as_list(preservation.get(field, [])):
            raw_rows.append((field, constraint_class_for_source_field(field), raw))

    for key in (
        "source_derived_runtime_constraints",
        "runtime_constraints",
        "hard_runtime_constraints",
        "source_constraints",
        "workflow_constraints",
    ):
        for raw in as_list(workflow_plan_value(plan, [key], [])):
            raw_rows.append((key, "explicit_source_constraint", raw))

    signal_terms = (
        "required", "minimum", "maximum", "count", "cardinality", "schema",
        "human", "selection", "approval", "gate", "audit", "checkpoint",
        "terminal", "no-auto", "wait", "deliverable", "artifact", "input", "user", "only",
    )
    for field in ("workflow_nodes", "workflow_edges"):
        for raw in as_list(preservation.get(field, [])):
            text = compact_text(raw).lower()
            if any(term in text for term in signal_terms):
                raw_rows.append((field, constraint_class_for_source_field(field), raw))

    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for idx, (field, klass, raw) in enumerate(raw_rows):
        constraint = normalize_source_runtime_constraint(raw, source_field=field, constraint_class=klass, index=idx)
        key = f"{constraint['constraint_class']}::{constraint['summary']}::{','.join(constraint['owner_candidates'])}"
        if key in seen:
            continue
        seen.add(key)
        deduped.append(constraint)
    return deduped


def constraint_applies_to_agent(constraint: dict[str, Any], agent: dict[str, Any], entry: str) -> bool:
    owners = [str(x).lower() for x in constraint.get("owner_candidates") or [] if str(x).strip()]
    if not owners:
        return True
    aid = agent_id(agent).lower()
    haystack = " ".join(
        str(x).lower()
        for x in [
            agent_id(agent),
            display(agent),
            mission(agent),
            " ".join(agent.get("owned_skills", [])),
        ]
    )
    for owner in owners:
        if owner in {"all", "global", "*"}:
            return True
        if owner in {"entry", "entry_agent", "entry-agent"} and (aid == entry.lower() or agent.get("entry_agent")):
            return True
        if owner == aid or owner in haystack:
            return True
    return False


def constraints_for_agent(agent: dict[str, Any], constraints: list[dict[str, Any]], entry: str) -> list[dict[str, Any]]:
    return [c for c in constraints if constraint_applies_to_agent(c, agent, entry)]


def agent_runtime_instruction_block(agent: dict[str, Any], plan: dict[str, Any], agents: list[dict[str, Any]], entry: str) -> str:
    constraints = constraints_for_agent(
        agent,
        source_derived_runtime_constraints(plan),
        entry,
    )
    lines = [
        "",
        "Design/package conformance guard:",
        "- Treat source-derived runtime constraints as hard package requirements, not as optional notes.",
        "- If a requested execution would drop a required count, schema, stage-internal deliverable, human wait, gate, checkpoint, terminal boundary, route restriction, or source-resource dependency, stop with `design-package conformance blocked`.",
        "- On conformance failure, report `reexecution_required=true`, name the earliest responsible phase, and do not patch downstream artifacts ad hoc.",
        "- Read `design-package-conformance.contract.json`, `runtime-instruction-conformance.json`, `workflow-preservation-gate.json`, `flow-control.contract.json`, and `agent-profiles.json` before claiming package-faithful execution.",
    ]
    responsibilities = as_list(agent.get("responsibilities") or [mission(agent)])
    if responsibilities:
        lines.append("Role responsibilities:")
        lines.extend(f"- {compact_text(item, 220)}" for item in responsibilities)
    non_resp = as_list(agent.get("non_responsibilities", []))
    if non_resp:
        lines.append("Non-responsibilities:")
        lines.extend(f"- {compact_text(item, 220)}" for item in non_resp)
    handoffs = as_list(agent.get("handoff_contract", []))
    if handoffs:
        lines.append("Handoff contract:")
        lines.extend(f"- {compact_text(item, 220)}" for item in handoffs)
    gates = as_list(agent.get("gates_owned", []))
    if gates:
        lines.append("Gates owned:")
        lines.extend(f"- {compact_text(item, 220)}" for item in gates)
    if constraints:
        lines.append("Source-derived runtime constraints for this role:")
        for constraint in constraints:
            lines.append(
                f"- [{constraint['constraint_id']}] {constraint['constraint_class']}: {constraint['summary']}"
            )
    else:
        lines.append("Source-derived runtime constraints for this role: none detected beyond shared package contracts.")
    if agent.get("entry_agent"):
        lines.extend([
            "Entry-agent intake guard:",
            "- Before entering the migrated workflow, collect source-required startup settings, user choices, route/delivery/runtime settings, and any human-intervention retention choices that are still missing.",
            "- If those settings are required by the source workflow and absent, ask the user or block; do not silently choose defaults except when the source contract names a safe default.",
        ])
    return "\n".join(lines) + "\n"


def runtime_instruction_conformance_payload(
    out: Path,
    plan: dict[str, Any],
    agents: list[dict[str, Any]],
    *,
    team_id: str,
    team_kind: str,
    source_skill: str | None,
    target: str,
    entry: str,
) -> dict[str, Any]:
    constraints = source_derived_runtime_constraints(plan)
    agent_rows: list[dict[str, Any]] = []
    blockers: list[str] = []
    for a in agents:
        aid = agent_id(a)
        required = constraints_for_agent(a, constraints, entry)
        toml_path = out / artifact_path_for(target, aid)
        text = toml_path.read_text(encoding="utf-8") if toml_path.exists() else ""
        missing_ids = [c["constraint_id"] for c in required if c["constraint_id"] not in text]
        if not toml_path.exists():
            blockers.append(f"missing runtime instruction file for agent {aid}: {artifact_path_for(target, aid)}")
        if "Design/package conformance guard:" not in text:
            blockers.append(f"runtime instruction for agent {aid} lacks design/package conformance guard")
        if missing_ids:
            blockers.append(f"runtime instruction for agent {aid} lacks source constraint ids: {', '.join(missing_ids[:12])}")
        agent_rows.append({
            "agent_id": aid,
            "runtime_instruction_file": artifact_path_for(target, aid),
            "applicable_source_constraint_ids": [c["constraint_id"] for c in required],
            "missing_source_constraint_ids": missing_ids,
            "conformance_guard_present": "Design/package conformance guard:" in text,
        })
    return {
        "schema_version": "s2t-runtime-instruction-conformance-v1",
        "managed_by": "skill2team",
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target.replace("_", "-"),
        "entry_agent_id": entry,
        "source_derived_runtime_constraints": constraints,
        "agent_instruction_materialization": agent_rows,
        "instruction_materialization_status": "blocked" if blockers else "passed",
        "instruction_materialization_blockers": blockers,
        "reexecution_required": bool(blockers),
        "reexecute_from": "runtime-adapter/package" if blockers else None,
        "rule": "Every execution-affecting source constraint must be visible in the design maps, package contracts, agent profiles, and generated runtime instructions.",
    }


def design_package_conformance_payload(
    plan: dict[str, Any],
    runtime_payload: dict[str, Any],
    *,
    team_id: str,
    team_kind: str,
    source_skill: str | None,
    target: str,
    entry: str,
    route: str,
    delivery: str,
) -> dict[str, Any]:
    preservation = workflow_preservation_payload(plan)
    blockers: list[str] = []
    responsible_phase = "none"
    if preservation["preservation_gate_status"] != "passed":
        blockers.extend(preservation["preservation_gate_blockers"])
        responsible_phase = "source-mapping/workflow-orchestration"
    if runtime_payload["instruction_materialization_status"] != "passed":
        blockers.extend(runtime_payload["instruction_materialization_blockers"])
        if responsible_phase == "none":
            responsible_phase = "runtime-adapter/package"
    if route == "source-to-team" and delivery == "package" and not runtime_payload["source_derived_runtime_constraints"]:
        blockers.append("no source-derived runtime constraints were extracted; rerun source mapping for nontrivial source-to-team package")
        if responsible_phase == "none":
            responsible_phase = "source-mapping/workflow-orchestration"
    return {
        "schema_version": "s2t-design-package-conformance-v1",
        "managed_by": "skill2team",
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target.replace("_", "-"),
        "entry_agent_id": entry,
        "route": route,
        "delivery": delivery,
        "design_inputs_checked": [
            "source workflow extraction",
            "stage-internal deliverables",
            "human intervention choices",
            "required user input nodes",
            "gates and checkpoints",
            "source-derived runtime constraints",
        ],
        "package_outputs_checked": [
            "workflow-orchestration.map.json",
            "flow-control.contract.json",
            "workflow-preservation-gate.json",
            "entry-agent-startup-welcome.json",
            "agent-profiles.json",
            ".codex/agents/*.toml",
            "runtime-instruction-conformance.json",
        ],
        "conformance_status": "blocked" if blockers else "passed",
        "conformance_blockers": blockers,
        "reexecution_required": bool(blockers),
        "reexecute_from": responsible_phase if blockers else None,
        "reexecution_rule": "When design/package conformance is blocked, rerun the earliest responsible source-mapping, workflow-orchestration, or runtime-adapter phase. Do not repair by editing only downstream package text.",
        "genericity_rule": "Checks are source-derived. Do not hard-code package names, paper titles, task ids, or one source skill's expected structure.",
    }


def meta_team_audit_payload(
    plan: dict[str, Any],
    *,
    team_id: str,
    team_kind: str,
    source_skill: str | None,
    target: str,
    entry: str,
    execution_path: str,
    current_run_fanout_status: str | None,
) -> dict[str, Any]:
    evidence = workflow_plan_value(
        plan,
        ["meta_team_audit", "independent_meta_team_audit", "independent_audit", "evaluation_review"],
        None,
    )
    has_evidence = evidence not in (None, "", [], {})
    status = "passed_with_evidence" if has_evidence else "pending_independent_audit"
    block_runtime_claim = (execution_path == "meta-team-first" or team_kind == "meta") and not has_evidence
    return {
        "schema_version": "s2t-meta-team-audit-v1",
        "managed_by": "skill2team",
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target.replace("_", "-"),
        "entry_agent_id": entry,
        "execution_path": execution_path,
        "current_run_fanout_status": normalized_fanout_status(execution_path, current_run_fanout_status),
        "independent_meta_team_audit_required": True,
        "auditor_role": "s2t-meta-evaluation-reviewer or an independent real-session reviewer subagent when registered meta-agents are not hot-loaded",
        "audit_subjects": [
            "fixed Skill2Team meta-team package when generated or reused",
            "target-team design/package conformance before handoff",
            "runtime instruction materialization of source-derived constraints",
        ],
        "audit_status": status,
        "audit_evidence": evidence if has_evidence else None,
        "block_runtime_claim_until_audited": block_runtime_claim,
        "reexecution_rule": "If the independent audit blocks a design or package artifact, route back to the producing meta role and rerun from the earliest failed phase before release.",
    }


def source_flow_control_payload(plan: dict[str, Any], preservation: dict[str, Any]) -> Any:
    provided = workflow_plan_value(plan, ["flow_control"], None)
    if provided is not None:
        return provided
    return {
        "derived_from_workflow_preservation": True,
        "workflow_nodes": preservation["workflow_nodes"],
        "workflow_edges": preservation["workflow_edges"],
        "user_input_nodes": preservation["user_input_nodes"],
        "human_intervention_points": preservation["human_intervention_points"],
        "gate_points": preservation["gate_points"],
        "checkpoint_resume_points": preservation["checkpoint_resume_points"],
    }


def derived_skill_allocation_matrix(agents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "agent_id": agent_id(a),
            "display_name": display(a),
            "owned_skills": a.get("owned_skills", []),
            "source": "derived_from_agent_profiles",
        }
        for a in agents
    ]


def derived_handoff_contracts(preservation: dict[str, Any]) -> list[dict[str, Any]]:
    contracts: list[dict[str, Any]] = []
    for edge in preservation["workflow_edges"]:
        if not isinstance(edge, dict):
            continue
        contracts.append({
            "from": edge.get("from"),
            "to": edge.get("to"),
            "edge_type": edge.get("type", "ordered"),
            "required_input": edge.get("required_input", "upstream_node_outputs"),
            "expected_output": edge.get("expected_output", "downstream_node_inputs_or_artifacts"),
            "blocked_condition": edge.get("blocked_condition", "missing_required_input_or_failed_gate"),
            "source": "derived_from_workflow_edges",
        })
    return contracts


def derived_gate_and_review_model(preservation: dict[str, Any], agents: list[dict[str, Any]]) -> dict[str, Any]:
    review_agents = [
        agent_id(a)
        for a in agents
        if any("review" in str(skill).lower() or "acceptance" in str(skill).lower() for skill in a.get("owned_skills", []))
    ]
    return {
        "source": "derived_from_workflow_preservation_and_agent_profiles",
        "gate_points": preservation["gate_points"],
        "review_agents": review_agents,
        "default_rule": "reviewer or verifier gates may block incomplete workflow preservation, unsafe auto-advance, or missing required artifacts",
    }

DEFAULT_META_AGENTS = [
    {
        "agent_id": "entry",
        "registered_agent_id": "s2t-meta-entry",
        "internal_role": "S2T Lead",
        "display_name": "S2T Lead",
        "main_function": "Intake, route selection, delivery selection, execution-path selection, state tracking, and synthesis ownership.",
        "mission": "User-facing entry agent for Skill2Team. Own intake, route selection, delivery selection, execution-path selection, state lookup, work-order creation, and final synthesis ownership.",
        "owned_skills": [
            "entrypoint",
            "routing",
            "state-tracking",
            "handoff",
            "synthesis"
        ],
        "tools_policy": {
            "allow": [
                "read",
                "write"
            ],
            "deny": []
        }
    },
    {
        "agent_id": "source-mapper",
        "registered_agent_id": "s2t-meta-source-mapper",
        "internal_role": "Source Mapper",
        "display_name": "Source Mapper",
        "main_function": "Source asset inventory, original workflow extraction, local-resource classification, and migration anchors.",
        "mission": "Inventory source skills, prompts, tools, scripts, templates, registry manifests, local resources, workflows, and SOPs; extract current workflow stages, artifacts, failure modes, and migration anchors.",
        "owned_skills": [
            "inventory",
            "workflow-extraction",
            "local-resource-allocation",
            "source-audit"
        ],
        "tools_policy": {
            "allow": [
                "read",
                "write"
            ],
            "deny": [
                "destructive-write"
            ]
        }
    },
    {
        "agent_id": "architecture-designer",
        "registered_agent_id": "s2t-meta-architecture-designer",
        "internal_role": "Architecture Designer",
        "display_name": "Architecture Designer",
        "main_function": "Agent Architecture Map, role boundaries, team topology, skill allocation, and agent-count rationale.",
        "mission": "Design the Agent Architecture Map separately from workflow orchestration: role topology, accountability, authority, context boundaries, owned/shared/restricted skills, and the rationale for the chosen top-level agent count.",
        "owned_skills": [
            "team-design",
            "agent-architecture",
            "agent-independence",
            "skill-allocation",
            "role-boundaries"
        ],
        "tools_policy": {
            "allow": [
                "read",
                "write"
            ],
            "deny": []
        }
    },
    {
        "agent_id": "workflow-orchestrator",
        "registered_agent_id": "s2t-meta-workflow-orchestrator",
        "internal_role": "Workflow Orchestrator",
        "display_name": "Workflow Orchestrator",
        "main_function": "Workflow Orchestration Map, control-flow rules, handoff contracts, checkpoints, reruns, and resume policy.",
        "mission": "Design the Workflow Orchestration Map separately from agent architecture: runtime stages, edges, branches, loops, gates, fan-out/fan-in, human waits, terminal boundaries, artifact lineage, and dependency-aware rerun/resume rules.",
        "owned_skills": [
            "workflow-orchestration",
            "control-flow-mapping",
            "handoff-contracts",
            "rerun-policy",
            "resume-policy"
        ],
        "tools_policy": {
            "allow": [
                "read",
                "write"
            ],
            "deny": []
        }
    },
    {
        "agent_id": "runtime-adapter",
        "registered_agent_id": "s2t-meta-runtime-adapter",
        "internal_role": "Runtime Adapter",
        "display_name": "Runtime Adapter",
        "main_function": "Target runtime artifact planning, package generation, manifest creation, prompt rewriting, design-continuation guidance, and package-end Codex register/start guidance.",
        "mission": "Generate Codex agent artifacts, registry/readiness manifests, usage guides, invocation contracts, prompt-rewrite rules, design-continuation templates for Codex/API/Hermes/OpenClaw, and package-end Codex register/start templates.",
        "owned_skills": [
            "runtime-adaptation",
            "design-continuation-guidance",
            "package-end-codex-guidance",
            "package-generation",
            "prompt-rewrite"
        ],
        "tools_policy": {
            "allow": [
                "read",
                "write"
            ],
            "deny": []
        }
    },
    {
        "agent_id": "evaluation-reviewer",
        "registered_agent_id": "s2t-meta-evaluation-reviewer",
        "internal_role": "Quality Reviewer",
        "display_name": "Quality Reviewer",
        "main_function": "Independent package/design review, risk checks, count justification checks, and acceptance-gate review.",
        "mission": "Independently review target-team design and package quality, risks, role boundaries, architecture/workflow separation, and agent-count justification before package handoff.",
        "owned_skills": [
            "quality-review",
            "risk-review",
            "package-review",
            "count-justification-review"
        ],
        "tools_policy": {
            "allow": [
                "read"
            ],
            "deny": [
                "primary-production",
                "write",
                "edit",
                "apply_patch",
                "exec"
            ]
        }
    }
]

GENERIC_NAMES = {"entry", "orchestrator", "builder", "reviewer", "planner", "critic", "agent"}

def slug(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "agent"

def load_plan(path: Path | None, *, meta_team: bool = False) -> dict[str, Any]:
    if meta_team:
        contract = load_meta_team_contract()
        return {
            "team_id": contract["team_id"],
            "team_kind": "meta",
            "source_skill": contract["skill_id"],
            "name_prefix": contract["name_prefix"],
            "entry_agent_id": contract["entry_agent_id"],
            "skill2team_version": contract["skill2team_version"],
            "meta_team_contract_version": contract["contract_version"],
            "meta_team_signature": meta_team_signature(contract),
            "agents": contract["agents"],
            "source_workflow": {
                "name": "fixed Skill2Team meta-team package generation and activation workflow",
                "source": "data/meta_team_contract.json",
                "purpose": "Generate or reuse the fixed s2t-meta Codex package, register it when requested, verify activation, run independent audit, and block role-play fallback.",
            },
            "workflow_nodes": [
                {"node_id": "meta_contract_load", "owner_agent": "s2t-meta-entry", "required_output": "verified fixed six-agent meta-team contract"},
                {"node_id": "source_mapping", "owner_agent": "s2t-meta-source-mapper", "required_output": "source workflow, local resource, startup setting, and source-derived runtime constraint inventory"},
                {"node_id": "architecture_design", "owner_agent": "s2t-meta-architecture-designer", "required_output": "agent architecture map and profile boundaries"},
                {"node_id": "workflow_orchestration", "owner_agent": "s2t-meta-workflow-orchestrator", "required_output": "workflow map, gates, checkpoints, and rerun/resume policy"},
                {"node_id": "runtime_package", "owner_agent": "s2t-meta-runtime-adapter", "required_output": "Codex package artifacts, conformance contracts, runtime instructions, and manifests"},
                {"node_id": "independent_audit", "owner_agent": "s2t-meta-evaluation-reviewer", "type": "gate", "required_output": "independent audit result"},
            ],
            "workflow_edges": [
                {"from": "meta_contract_load", "to": "source_mapping", "type": "sequence"},
                {"from": "source_mapping", "to": "architecture_design", "type": "sequence"},
                {"from": "architecture_design", "to": "workflow_orchestration", "type": "sequence"},
                {"from": "workflow_orchestration", "to": "runtime_package", "type": "sequence"},
                {"from": "runtime_package", "to": "independent_audit", "type": "gate"},
            ],
            "stage_mappings": [
                {"source_stage": "meta-team contract verification", "target_owner": "s2t-meta-entry"},
                {"source_stage": "source/workflow extraction", "target_owner": "s2t-meta-source-mapper"},
                {"source_stage": "architecture/profile design", "target_owner": "s2t-meta-architecture-designer"},
                {"source_stage": "workflow orchestration", "target_owner": "s2t-meta-workflow-orchestrator"},
                {"source_stage": "runtime/package generation", "target_owner": "s2t-meta-runtime-adapter"},
                {"source_stage": "independent audit", "target_owner": "s2t-meta-evaluation-reviewer"},
            ],
            "stage_internal_deliverables": [
                {"stage": "source_mapping", "owner_agent": "s2t-meta-source-mapper", "deliverables": ["source_inventory", "startup_settings", "human_intervention_points", "source_derived_runtime_constraints"]},
                {"stage": "runtime_package", "owner_agent": "s2t-meta-runtime-adapter", "deliverables": ["design-package-conformance.contract.json", "runtime-instruction-conformance.json", "meta-team-audit.contract.json"]},
            ],
            "human_intervention_points": [
                {"id": "activation_path_choice", "owner_agent": "s2t-meta-entry", "description": "If registered meta-agent activation is unavailable, choose real current-session subagents, block, or explicitly change execution path."},
            ],
            "user_input_nodes": [
                {"id": "startup_route_delivery_runtime", "owner_agent": "s2t-meta-entry", "required_inputs": ["route", "delivery", "execution_path", "target_runtime", "source_material"], "default_action": "ask_or_block_before_source_mapping"},
                {"id": "human_interaction_mode_choice", "owner_agent": "s2t-meta-entry", "required_inputs": ["preserve_source_human_interaction_steps", "selective_human_intervention_retention", "fully_automated_with_audit"], "default_action": "preserve_source_human_interaction_steps"},
            ],
            "human_intervention_policy": {
                "initial_user_choice_required": True,
                "selected_execution_mode": "preserve_source_human_interaction_steps",
                "default": "preserve_all_source_mandated_human_waits_and_choices",
                "ask_user_before_auto_advancing": True,
                "allowed_choices": WORKFLOW_PRESERVATION_CHOICES,
                "user_overrides": [],
            },
            "checkpoint_resume_points": [
                {"id": "after_meta_contract_load", "owner_agent": "s2t-meta-entry"},
                {"id": "after_runtime_package", "owner_agent": "s2t-meta-runtime-adapter"},
            ],
            "gate_points": [
                {"id": "independent_meta_team_audit", "owner_agent": "s2t-meta-evaluation-reviewer", "producer_self_approval_forbidden": True},
            ],
            "source_derived_runtime_constraints": [
                {"owner_agent": "s2t-meta-entry", "constraint": "Codex meta-team-first must use registered s2t-meta agents or real independent current-session subagents; role-play fallback is forbidden."},
                {"owner_agent": "s2t-meta-runtime-adapter", "constraint": "Generated meta-team packages must include design-package conformance, runtime instruction conformance, and meta-team audit contracts."},
                {"owner_agent": "s2t-meta-evaluation-reviewer", "constraint": "Independent reviewer must not produce the artifact under review or approve its own changes."},
            ],
        }
    if not path:
        return {"agents": DEFAULT_AGENTS}
    data = json.loads(path.read_text(encoding="utf-8"))
    if "agents" not in data:
        raise SystemExit("Plan JSON must contain an 'agents' list")
    return data

def ensure(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def load_meta_team_contract() -> dict[str, Any]:
    path = SKILL_ROOT / "data" / "meta_team_contract.json"
    if not path.exists():
        return {
            "schema_version": 1,
            "contract_version": "fallback",
            "skill_id": "skill2team",
            "skill2team_version": "unknown",
            "team_kind": "meta",
            "team_id": "s2t-meta",
            "name_prefix": "s2t-meta",
            "entry_agent_id": "s2t-meta-entry",
            "agents": DEFAULT_META_AGENTS,
        }
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ["contract_version", "skill_id", "skill2team_version", "team_id", "name_prefix", "entry_agent_id", "agents"]
    missing = [key for key in required if not data.get(key)]
    if missing:
        raise SystemExit(f"meta_team_contract.json missing required fields: {', '.join(missing)}")
    return data

def meta_team_signature(contract: dict[str, Any]) -> str:
    payload = {
        "schema_version": contract.get("schema_version"),
        "contract_version": contract.get("contract_version"),
        "skill_id": contract.get("skill_id"),
        "skill2team_version": contract.get("skill2team_version"),
        "team_kind": contract.get("team_kind"),
        "team_id": contract.get("team_id"),
        "name_prefix": contract.get("name_prefix"),
        "entry_agent_id": contract.get("entry_agent_id"),
        "agents": contract.get("agents", []),
    }
    encoded = json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

def meta_team_registry_fields(agents: list[dict[str, Any]]) -> dict[str, Any]:
    contract = load_meta_team_contract()
    return {
        "skill2team_version": contract.get("skill2team_version"),
        "meta_team_contract_version": contract.get("contract_version"),
        "meta_team_signature": meta_team_signature(contract),
        "meta_team_contract_path": "data/meta_team_contract.json",
        "meta_team_reuse_policy": contract.get("reuse_policy", {}),
        "meta_team_agent_ids": [agent_id(a) for a in agents],
        "meta_team_roles": [
            {
                "agent_id": agent_id(a),
                "internal_role": a.get("internal_role") or display(a),
                "display_name": display(a),
                "main_function": a.get("main_function") or mission(a),
                "entry": bool(a.get("entry_agent")),
            }
            for a in agents
        ],
    }

def agent_id(agent: dict[str, Any]) -> str:
    return slug(str(agent.get("agent_id") or agent.get("id") or agent.get("name") or "agent"))

def mission(agent: dict[str, Any]) -> str:
    return str(agent.get("mission") or agent.get("primary_accountability") or agent.get("description") or "Specialized agent.")

def display(agent: dict[str, Any]) -> str:
    return str(agent.get("display_name") or agent.get("name") or agent_id(agent))

def write_json(path: Path, obj: Any) -> None:
    # Keep machine JSON ASCII-escaped so legacy Windows readers do not corrupt it.
    path.write_text(json.dumps(obj, ensure_ascii=True, indent=2), encoding="utf-8")

def derive_team_id(plan: dict[str, Any], explicit: str | None, source_skill: str | None, team_kind: str) -> str:
    if explicit:
        return slug(explicit)
    if plan.get("team_id"):
        return slug(str(plan["team_id"]))
    if team_kind == "meta":
        return "s2t-meta"
    if source_skill:
        return f"s2t-target-{slug(source_skill)}"
    return "s2t-target-generated-team"

def derive_prefix(team_id: str, explicit: str | None, team_kind: str, source_skill: str | None) -> str:
    if explicit:
        return slug(explicit)
    if team_kind == "meta":
        return "s2t-meta"
    if team_id.startswith("s2t-"):
        return team_id
    if source_skill:
        return f"s2t-target-{slug(source_skill)}"
    return f"s2t-{team_id}"

def namespaced_agent_id(raw: str, prefix: str) -> str:
    aid = slug(raw)
    if aid.startswith(prefix + "-"):
        return aid
    if aid in GENERIC_NAMES:
        return f"{prefix}-{aid}"
    if aid.startswith("s2t-"):
        return f"{prefix}-{aid[4:]}"
    return f"{prefix}-{aid}"

def prepare_agents(plan: dict[str, Any], *, team_id: str, team_kind: str, source_skill: str | None, prefix: str, entry_agent_id: str | None) -> tuple[list[dict[str, Any]], str]:
    entry = slug(entry_agent_id or f"{prefix}-entry")
    prepared: list[dict[str, Any]] = []
    for agent in plan["agents"]:
        a = dict(agent)
        original = agent_id(a)
        a["original_agent_id"] = original
        if team_kind == "meta" and a.get("registered_agent_id"):
            a["agent_id"] = slug(str(a["registered_agent_id"]))
        else:
            a["agent_id"] = namespaced_agent_id(original, prefix)
        a["s2t_team_id"] = team_id
        a["s2t_team_kind"] = team_kind
        a["s2t_name_prefix"] = prefix
        a["s2t_entry_agent"] = entry
        prepared.append(a)
    if not any(agent_id(a) == entry for a in prepared):
        label = "Skill2Team Meta Entry" if team_kind == "meta" else f"Skill2Team Target Entry ({source_skill or team_id})"
        prepared.insert(0, {
            "agent_id": entry,
            "original_agent_id": "entry",
            "display_name": label,
            "mission": "User-facing entry agent for intake, route selection, state lookup, and handoff to the registered Skill2Team team.",
            "owned_skills": ["entrypoint", "routing", "handoff"],
            "tools_policy": {"allow": ["read", "write"], "deny": []},
            "s2t_team_id": team_id,
            "s2t_team_kind": team_kind,
            "s2t_name_prefix": prefix,
            "s2t_entry_agent": entry,
            "entry_agent": True,
        })
    else:
        for a in prepared:
            if agent_id(a) == entry:
                a["entry_agent"] = True
    return prepared, entry

def normalized_fanout_status(execution_path: str, explicit: str | None = None) -> str:
    if explicit:
        return explicit
    return "direct-skill-not-requested" if execution_path == "direct-skill" else "blocked_no_real_codex_meta_team"

def fanout_execution_mode(status: str, execution_path: str) -> str:
    if execution_path == "direct-skill":
        return "direct_skill"
    if status in {"real_subagents", "real_session_subagents"}:
        return "fanout"
    if status == "blocked_no_real_codex_meta_team":
        return "blocked"
    return "artifact_only"

def fanout_fallback(status: str, execution_path: str) -> str:
    if execution_path == "direct-skill":
        return "not_applicable_direct_skill"
    if status == "real_subagents":
        return "not_applicable_registered_meta_agents_used"
    if status == "real_session_subagents":
        return "not_applicable_real_current_session_subagents_used_registered_meta_smoke_pending"
    if status == "blocked_no_real_codex_meta_team":
        return "meta-team-first blocked; real Codex meta-team activation/fan-out was not confirmed; fallback role-play is not permitted"
    return "not_applicable"


def reject_meta_override(option: str, supplied: str | None, fixed: str) -> None:
    if supplied and slug(supplied) != slug(fixed):
        raise SystemExit(f"{option} cannot override the fixed Skill2Team meta-team value {fixed}")


def planned_registered_files_for(target: str, agents: list[dict[str, Any]], team_id: str) -> list[str]:
    t = target.replace("-", "_")
    files = [artifact_path_for(target, agent_id(a)) for a in agents]
    if t == "codex":
        files.append(f".codex/s2t-agent-registrations/{team_id}.json")
    return list(dict.fromkeys(files))


def source_invocation_patterns(source_skill: str | None) -> list[str]:
    if not source_skill:
        return []
    return [
        f"Use {source_skill} skill",
        f"use {source_skill} skill",
        f"Start {source_skill}",
        f"start {source_skill}",
    ]


def source_prompt_rewrite_policy(source_skill: str | None, entry: str) -> dict[str, Any]:
    return {
        "source_skill": source_skill,
        "source_invocation_patterns": source_invocation_patterns(source_skill),
        "copy_source_self_invocation_verbatim": False,
        "registered_replacement": f"Use the registered {entry} agent after Codex registration and smoke tests",
        "unregistered_replacement": f"Inspect this generated package as artifacts only; do not perform the target-team task. To execute in Codex, register and smoke-test {entry}.",
        "fallback_allowed_only_when": "manifest explicitly records source_skill_fallback mode",
        "rewrite_applies_to": [
            "team usage guides",
            "handoff prompts",
            "starter prompts",
            "generated README snippets",
            "runtime manifest notes",
            "AGENTS guidance",
        ],
    }




def model_invocation_policy() -> dict[str, Any]:
    return {
        "default_model_runner": "OpenAI Codex",
        "direct_model_api_calls_default": False,
        "applies_to": [
            "Skill2Team direct run",
            "fixed s2t-meta service agents",
            "generated target-team agents",
        ],
        "startup_reminder_required": True,
        "api_runner_exception_label": "API-run role simulation, not Codex custom-agent execution",
        "api_service_followup_label": "API-service follow-up, not Codex custom-agent execution",
        "followup_model_service_modes": [
            "OpenAI Codex custom-agent/runtime service",
            "API model service for explicit API-service follow-ups",
        ],
    }


def architecture_build_policy() -> dict[str, Any]:
    return {
        "default_architecture_method": "framework-neutral agent architecture relationship graph",
        "agent_binding": "profile-based agents as relationship-graph nodes",
        "edge_binding": "route, handoff, delegation, review_gate, guardrail, fan_out, fan_in, human_wait, checkpoint, state_or_artifact_flow, terminal",
        "runtime_dependency": "none for package metadata; map this relationship graph into a specific multi-agent runner only in an explicit follow-up",
        "best_practice_policy": [
            "keep role boundaries explicit",
            "model handoffs and delegation as typed edges",
            "record state/artifact ownership",
            "preserve human waits and independent review gates",
            "keep guardrails/evaluation separate from producers",
            "do not bind conceptual architecture to one framework runtime",
        ],
        "workflow_step_rule": "workflow steps do not automatically become agents",
    }


def target_team_execution_guard_policy(entry: str, agents: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    specialist_ids = [agent_id(a) for a in (agents or []) if agent_id(a) != entry]
    return {
        "schema_version": "s2t-target-team-execution-guard-v1",
        "target_runtime": "codex",
        "codex_target_team_execution_requires_real_registered_agents": True,
        "codex_target_team_execution_requires_real_specialist_handoffs": True,
        "codex_target_team_execution_allows_real_session_subagents_when_registered_agents_unavailable": True,
        "session_subagent_success_status": "real_session_target_subagents",
        "block_status": "target-team execution blocked",
        "forbid_single_agent_or_sequential_simulation": True,
        "forbid_unverified_fanout_continuation": True,
        "entry_agent_id": entry,
        "specialist_agent_ids": specialist_ids,
        "block_when": [
            "the current invocation is not the registered Codex entry agent",
            "the Codex project has not installed the package manifest and agent TOML files",
            "the runtime cannot expose multi_agent and enable_fanout behavior for this team",
            "the entry agent cannot hand off work to required specialist agents and no real current-session target subagent fan-out evidence exists",
            "post-registration smoke-test evidence is missing and no real current-session target subagent fan-out evidence exists",
            "the user requested Codex target-team execution but only artifact inspection, API service, or single-agent work is available",
        ],
        "entry_agent_rule": "If real registered specialist handoff is unavailable, first check whether the active Codex session can launch real independent subagents for the generated target roles. If yes, run only with target_run_fanout_status=real_session_target_subagents, keep registered smoke-test status pending, and preserve entry/specialist/reviewer boundaries. If not, stop with target-team execution blocked. Do not perform specialist work inside the entry agent while claiming target-team execution.",
        "specialist_agent_rule": "Return structured results only for your assigned specialist role and do not claim to be the full target team.",
        "allowed_alternatives": [
            "artifact-only package inspection before registration",
            "current-session target-team fan-out with real independent Codex subagents and target_run_fanout_status=real_session_target_subagents",
        ],
    }


def profile_path_for(aid: str) -> str:
    return f"profiles/{aid}.agent-profile.json"


def agent_profile(
    agent: dict[str, Any],
    *,
    team_id: str,
    team_kind: str,
    source_skill: str | None,
    target: str,
    entry: str,
    source_runtime_constraints: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    aid = agent_id(agent)
    applicable_constraints = constraints_for_agent(agent, source_runtime_constraints or [], entry)
    return {
        "schema_version": "s2t-agent-profile-v1",
        "managed_by": "skill2team",
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target.replace("_", "-"),
        "agent_id": aid,
        "profile_id": f"{aid}.profile",
        "profile_path": profile_path_for(aid),
        "agent_node_id": aid.replace("-", "_"),
        "display_name": display(agent),
        "mission": mission(agent),
        "entry_agent": bool(agent.get("entry_agent")),
        "entry_agent_id": entry,
        "responsibilities": agent.get("responsibilities") or [mission(agent)],
        "non_responsibilities": agent.get("non_responsibilities", []),
        "owned_skills": agent.get("owned_skills", []),
        "tools_policy": agent.get("tools_policy", {}),
        "handoff_contract": agent.get("handoff_contract", []),
        "gates_owned": agent.get("gates_owned", []),
        "source_derived_runtime_constraints": applicable_constraints,
        "entry_agent_startup_welcome": "entry-agent-startup-welcome.json" if bool(agent.get("entry_agent")) else None,
        "runtime_conformance_duties": [
            "Read design-package-conformance.contract.json and runtime-instruction-conformance.json before claiming package-faithful execution.",
            "If this is the entry agent, render or summarize docs/entry-agent-startup-welcome.md before the first migrated workflow stage.",
            "Block and request re-execution when a source-derived runtime constraint is missing from the design, package, profile, or runtime instructions.",
        ],
        "model_invocation_policy": model_invocation_policy(),
        "architecture_policy": architecture_build_policy(),
        "target_team_execution_guard_policy": target_team_execution_guard_policy(entry),
    }


def delivery_next_prompt_templates(
    *,
    team_id: str,
    team_kind: str,
    source_skill: str | None,
    target: str,
    entry: str,
    route: str,
    delivery: str,
) -> dict[str, str]:
    runtime = target.replace("_", "-")
    source_placeholder = "<SOURCE_SKILL_ZIP>"
    package_placeholder = "<GENERATED_TARGET_TEAM_PACKAGE>"
    design_placeholder = "<DESIGN_OUTPUT_OR_DESIGN_INTERMEDIATE_RESULTS>"
    codex_root_placeholder = "<CODEX_PROJECT_ROOT>"
    hermes_placeholder = "<HERMES_WORKSPACE>"
    openclaw_workspace_placeholder = "<OPENCLAW_WORKSPACE>"
    openclaw_skill_root_placeholder = "<OPENCLAW_SKILL_ROOT>"
    api_config_placeholder = "<MODEL_API_SERVICE_CONFIG>"
    source_note = f"Source material: {source_placeholder}."
    if source_skill:
        source_note = f"Source material: {source_placeholder}  # source skill placeholder for {source_skill}."
    design_files = (
        "design-intermediate-results.json, docs/design-intermediate-results.md, "
        "agent-architecture.map.json, workflow-orchestration.map.json, "
        "flow-control.contract.json, local-resource-allocation.map.json, "
        "source-resource-manifest.json, agent-profiles.json, profiles/*.agent-profile.json"
    )
    return {
        "design_to_package_prompt": (
            "Start Skill2Team.\n"
            f"Route: {route}.\n"
            "Delivery: package.\n"
            "Execution path: direct-skill.\n"
            f"Target runtime: {runtime}.\n"
            "Model invocation policy: use OpenAI Codex; do not call direct model APIs.\n"
            f"Team id: {team_id}.\n"
            f"{source_note}\n"
            f"Design input: {design_placeholder}.\n"
            "Use framework-neutral agent relationship architecture with profile-based agents. Carry forward the design quality gate result. "
            "Treat package as one concrete artifact-delivery example after design, not as the only possible continuation. "
            "Generate a Codex package with design intermediate results, entry-agent startup welcome page, generated target-team agents and functions, agent profiles, manifests, register-readiness contract, runtime invocation contract, prompt-rewrite rules, team usage guide, package release gate result, and a package-end Codex register/start prompt template."
        ),
        "design_continuation_codex_package_register_start_openai_codex": (
            "Continue from the Skill2Team design.\n"
            "Continuation target: Codex package, registration guidance, and startup prompt.\n"
            "Model service mode: OpenAI Codex.\n"
            "Architecture method: framework-neutral agent architecture relationship graph; agent mode: profile-based agents.\n"
            f"Source material: {source_placeholder}.\n"
            f"Design output: {design_placeholder}.\n"
            f"Codex project root: {codex_root_placeholder}.\n"
            "First generate or inspect the Codex package artifacts from the design. Then provide manifest-scoped registration steps for .codex/agents/*.toml, .codex/config.toml using config_file entries, and .codex/s2t-agent-registrations/<team_id>.json.\n"
            "List every generated target-team agent and its function. Provide smoke tests for entry invocation, specialist handoffs, independent reviewer blocking, and state/artifact handoff.\n"
            "End with the exact prompt to start the registered entry agent after smoke tests pass. Do not claim runnability before Codex evidence exists. If the registered entry agent cannot hand off to real specialist agents, it must stop with target-team execution blocked rather than continue as a sequential or single-agent simulation."
        ),
        "design_continuation_api_service_runner": (
            "Continue from the Skill2Team design inside a Codex workspace.\n"
            "Continuation target: API-service runner, not Codex custom-agent execution.\n"
            "Model service mode: API model service.\n"
            "Architecture method: framework-neutral agent architecture relationship graph; agent mode: profile-based agents.\n"
            f"Source material: {source_placeholder}.\n"
            f"Design output: {design_placeholder}.\n"
            f"Codex project root: {codex_root_placeholder}.\n"
            f"Model API service config: {api_config_placeholder}.\n"
            "Build or describe a framework-neutral multi-agent runner mapping where every generated agent profile is an agent node and the architecture/workflow maps define handoff edges, gates, checkpoints, repair loops, state/artifact transfers, human waits, and terminal boundaries. Name a specific runner only if the user explicitly selects one.\n"
            "Preserve the entry-agent contract, independent review gate, prompt-rewrite policy, no-hard-coding rule, and design quality gate result. Label all execution as API-service follow-up."
        ),
        "design_continuation_hermes_openai_codex_profile": (
            "Hermes task: continue from a Skill2Team design.\n"
            "Model service mode: OpenAI Codex.\n"
            "Agent mode: profile-based agents.\n"
            f"Source material: {source_placeholder}.\n"
            f"Design output: {design_placeholder}.\n"
            f"Hermes workspace: {hermes_placeholder}.\n"
            f"Target runtime: {runtime}.\n"
            f"Use {design_files}.\n"
            "Create Hermes profiles for every generated target-team agent. Preserve architecture/workflow separation, entry-agent contract, profile responsibilities, prompt-rewrite policy, independent review gate, and no-hard-coding constraints.\n"
            "Use OpenAI Codex as the model service for actual model work. Output the Hermes profile map, transformed files, Codex registration/start guidance, smoke tests, and final Codex entry-agent prompt."
        ),
        "design_continuation_hermes_api_profile": (
            "Hermes task: continue from a Skill2Team design.\n"
            "Model service mode: API model service.\n"
            "Agent mode: profile-based agents.\n"
            f"Source material: {source_placeholder}.\n"
            f"Design output: {design_placeholder}.\n"
            f"Hermes workspace: {hermes_placeholder}.\n"
            f"Model API service config: {api_config_placeholder}.\n"
            f"Use {design_files}.\n"
            "Create Hermes profiles for every generated target-team agent and build the execution plan as a framework-neutral agent relationship graph.\n"
            "Label the result API-service follow-up, not OpenAI Codex custom-agent execution. Output profile map, API-service placeholders, transformed files, checks, smoke tests, and an API-service run prompt."
        ),
        "design_continuation_openclaw_openai_codex_profile": (
            "OpenClaw task: continue from a Skill2Team design.\n"
            "Model service mode: OpenAI Codex.\n"
            "Agent mode: profile-based agents.\n"
            f"Source material: {source_placeholder}.\n"
            f"Design output: {design_placeholder}.\n"
            f"OpenClaw workspace: {openclaw_workspace_placeholder}.\n"
            f"OpenClaw skill root or package root: {openclaw_skill_root_placeholder}.\n"
            "Create or adapt OpenClaw-compatible profile files for every generated target-team agent. Preserve global-skill metadata if publishing a skill, keep MIT-0/text-only constraints, and do not confuse global skill registration with generated target-team agent registration.\n"
            "Use OpenAI Codex as the model service for actual model work. Output OpenClaw profile map, files to create/change, global discovery metadata, Codex registration/start guidance if a Codex package is also produced, smoke tests, and unresolved blockers."
        ),
        "design_continuation_openclaw_api_profile": (
            "OpenClaw task: continue from a Skill2Team design.\n"
            "Model service mode: API model service.\n"
            "Agent mode: profile-based agents.\n"
            f"Source material: {source_placeholder}.\n"
            f"Design output: {design_placeholder}.\n"
            f"OpenClaw workspace: {openclaw_workspace_placeholder}.\n"
            f"OpenClaw skill root or package root: {openclaw_skill_root_placeholder}.\n"
            f"Model API service config: {api_config_placeholder}.\n"
            "Create or adapt OpenClaw-compatible profile files for every generated target-team agent and build the execution plan as a framework-neutral agent relationship graph. Preserve global-skill metadata, MIT-0/text-only constraints, architecture/workflow separation, independent review gate, and no-hard-coding rule.\n"
            "Label the result API-service follow-up, not OpenAI Codex custom-agent execution. Output OpenClaw profile map, API-service placeholders, files to create/change, checks, smoke tests, and an API-service run prompt."
        ),
        "package_end_codex_register_and_start_openai_codex": (
            "Start Skill2Team.\n"
            f"Route: {route}.\n"
            "Delivery: package.\n"
            "Execution path: direct-skill.\n"
            f"Target runtime: {runtime}.\n"
            "Model invocation policy: use OpenAI Codex; do not call direct model APIs.\n"
            f"{source_note}\n"
            f"Generated target-team package: {package_placeholder}.\n"
            f"Codex project root: {codex_root_placeholder}.\n"
            "Package-end action requested: provide manifest-scoped instructions to register and start this shared target-team package in Codex.\n"
            "Read s2t-agent-registry.json, agent-profiles.json, entry-agent-startup-welcome.json, local-resource-allocation.map.json, source-resource-manifest.json, .codex/config.toml, .codex/agents/*.toml, docs/entry-agent-startup-welcome.md, docs/team-usage-guide.md, docs/runtime-invocation-contract.md, docs/register-readiness-contract.md, docs/local-resource-allocation-map.md, and docs/post-package-prompt-templates.md.\n"
            "List the generated target-team agents and their functions. Register only files listed in planned_registered_files; do not delete or overwrite unrelated Codex agents.\n"
            "Give exact copy/install locations, required config_file entries, smoke tests for entry invocation, specialist handoffs, independent reviewer blocking, and state/artifact handoff.\n"
            "End with the prompt to invoke the registered entry agent after all smoke tests pass. Do not claim the target team is runnable until Codex evidence exists. If handoff to specialists cannot actually run, stop with target-team execution blocked; do not continue as sequential or single-agent simulation."
        ),
        "registered_entry_agent_use_after_codex_smoke_tests": (
            f"Use the registered `{entry}` agent.\n"
            "Task: <what you want this team to do>.\n"
            "Inputs: <files, state path, or pasted context>.\n"
            "Start by rendering or summarizing the entry-agent startup welcome page, then perform intake and state lookup. Use shallow specialist handoffs. "
            "Do not let the entry agent approve its own specialist outputs. "
            "If registered specialist handoff is unavailable because this running Codex thread did not hot-load the generated target-agent types, switch only to the current-session target-team fan-out prompt when real independent subagents can run. Otherwise stop with `target-team execution blocked`, explain the reason, and give recovery steps; do not continue as sequential or single-agent simulation. This prompt is valid only after Codex registration and smoke-test evidence exist."
        ),
        "current_session_target_team_fanout_prompt": (
            "Run this generated target-team package through real current-session Codex subagents, not through registered custom-agent execution.\n"
            f"Generated target-team package: {package_placeholder}.\n"
            f"Entry role: `{entry}`.\n"
            "Read `s2t-agent-registry.json`, `agent-profiles.json`, `entry-agent-startup-welcome.json`, `local-resource-allocation.map.json`, `source-resource-manifest.json`, `agent-architecture.map.json`, `workflow-orchestration.map.json`, `docs/entry-agent-startup-welcome.md`, `docs/runtime-invocation-contract.md`, and `docs/team-usage-guide.md`.\n"
            "Spawn real independent subagents for the generated specialist profiles and keep entry, specialist, and reviewer responsibilities separate. Record `target_run_fanout_status=real_session_target_subagents`, `registered_target_team_smoke_status=pending_hot_reload_or_new_thread`, and `registered_agent_invocation_verified=false`.\n"
            "Use this path only when registered target-agent types are not available in the active thread but real subagent fan-out is available. Do not describe the run as registered target-team execution, and do not collapse specialist work into the entry agent."
        ),
        "api_runner_role_simulation_prompt": (
            "You are running Skill2Team follow-up through an API model runner, not OpenAI Codex custom agents.\n"
            "Treat this as API-run role simulation only.\n"
            f"Source material: {source_placeholder}.\n"
            f"Design output or generated target-team package: {design_placeholder} or {package_placeholder}.\n"
            "Read the manifest, generated target-agent list, agent profiles, agent architecture map, workflow orchestration map, runtime invocation contract, and team usage guide from the provided context.\n"
            "Simulate the target entry agent and specialist handoffs as labeled sections only because this prompt explicitly selected API-run role simulation. Do not claim Codex registration, registered-agent execution, or Codex target-team execution.\n"
            "Output: (1) generated target-team agents and functions, (2) framework-neutral role-simulation trace, (3) next safe Codex registration steps if a package exists, (4) prompt to use after real Codex registration, and (5) unresolved blockers."
        ),

    }

def format_next_prompt_templates(templates: dict[str, str]) -> str:
    return "\n\n".join(
        f"### {key.replace('_', ' ').title()}\n\n```text\n{value}\n```"
        for key, value in templates.items()
    )

def runtime_invocation_policy(
    *,
    team_id: str,
    team_kind: str,
    source_skill: str | None,
    target: str,
    entry: str,
    execution_path: str,
    current_run_fanout_status: str | None,
    route: str = "source-to-team",
    delivery: str = "package",
) -> dict[str, Any]:
    fanout_status = normalized_fanout_status(execution_path, current_run_fanout_status)
    return {
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target.replace("_", "-"),
        "model_invocation_policy": model_invocation_policy(),
        "architecture_policy": architecture_build_policy(),
        "entry_agent_id": entry,
        "target_team_registration_status": "not_registered",
        "entry_agent_runnable": False,
        "registered_entry_agent_prompt_allowed": False,
        "registered_entry_agent_prompt_allowed_when": "runtime manifest has registration_status=registered and registered_files includes the entry agent artifact",
        "registered_target_team_smoke_status": "not_registered",
        "registered_agent_invocation_verified": False,
        "target_run_fanout_status": "not_started",
        "allowed_current_session_target_fanout_status": "real_session_target_subagents",
        "current_session_target_fanout_allowed_when": "registered target-agent types are not available in the active Codex thread, but real independent current-session subagents can be launched for generated target profiles",
        "generation_run_fanout_status": fanout_status,
        "current_task_execution_mode": "artifact_only_until_registered_or_real_session_target_fanout_selected",
        "entry_agent_startup_welcome": "entry-agent-startup-welcome.json",
        "entry_agent_startup_welcome_doc": "docs/entry-agent-startup-welcome.md",
        "entry_agent_must_render_startup_welcome_before_first_migrated_stage": True,
        "registered_invocation_prompt": f"Use the registered {entry} agent; if specialist handoff is unavailable, stop with target-team execution blocked",
        "unregistered_invocation_prompt": f"Inspect this generated package as artifacts only; do not perform the target-team task or claim registered-agent execution for {entry}. Register and smoke-test first.",
        "current_session_target_fanout_prompt": "Use real current-session Codex subagents for the generated target profiles; record target_run_fanout_status=real_session_target_subagents and keep registered smoke status pending. Do not claim registered target-team execution.",
        "target_team_execution_guard_policy": target_team_execution_guard_policy(entry),
        "source_prompt_rewrite_policy": source_prompt_rewrite_policy(source_skill, entry),
        "next_use_prompt_templates": delivery_next_prompt_templates(
            team_id=team_id,
            team_kind=team_kind,
            source_skill=source_skill,
            target=target,
            entry=entry,
            route=route,
            delivery=delivery,
        ),
    }


def register_readiness_policy(
    agents: list[dict[str, Any]],
    *,
    team_id: str,
    team_kind: str,
    source_skill: str | None,
    target: str,
    entry: str,
) -> dict[str, Any]:
    """Describe whether this package is ready to enforce register-time hard runnability checks."""
    target_runtime = target.replace("_", "-")
    planned_agents = [
        {
            "agent_id": agent_id(a),
            "display_name": display(a),
            "role": "entry" if a.get("entry_agent") else a.get("role", a.get("original_agent_id", agent_id(a))),
            "entry": bool(a.get("entry_agent")),
            "artifact_path": artifact_path_for(target, agent_id(a)),
        }
        for a in agents
    ]
    register_blockers: list[str] = []
    if target_runtime != "codex":
        register_blockers.append(
            f"target_runtime={target_runtime} is not supported by this Skill2Team build; only codex is generated and tested"
        )
    if not any(a["entry"] and a["agent_id"] == entry for a in planned_agents):
        register_blockers.append("entry agent is missing from planned runtime agents")
    if len(planned_agents) < 2:
        register_blockers.append("package contains fewer than two planned runtime agents; specialist handoff cannot be smoke-tested")

    readiness_status = "blocked" if register_blockers else "ready_for_register_validation"
    return {
        "schema_version": "s2t-register-readiness-v1",
        "managed_by": "skill2team",
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target_runtime,
        "entry_agent_id": entry,
        "package_supports_register_hard_runtime_requirements": readiness_status != "blocked",
        "package_register_readiness_status": readiness_status,
        "codex_target_team_execution_requires_real_registered_agents": True,
        "codex_target_team_execution_allows_real_session_subagents_when_registered_agents_unavailable": True,
        "allowed_current_session_target_fanout_status": "real_session_target_subagents",
        "forbid_single_agent_or_sequential_simulation": True,
        "target_team_execution_guard_policy": target_team_execution_guard_policy(entry, agents),
        "registration_status_at_package_time": "not_registered",
        "entry_agent_runnable_at_package_time": False,
        "hard_requirement": (
            "Delivery: package must produce enough artifacts, manifests, prompts, and smoke-test contracts so a later Codex environment "
            "can prove the entry agent and all specialist agents can actually run and hand off. "
            "Generated files alone are not runtime execution proof."
        ),
        "planned_runtime_agents": planned_agents,
        "planned_registered_files": planned_registered_files_for(target, agents, team_id),
        "planned_runtime_context_files": [
            "agent-profiles.json",
            "profiles/*.agent-profile.json",
            "agent-architecture.map.json",
            "workflow-orchestration.map.json",
            "flow-control.contract.json",
            "workflow-preservation-gate.json",
            "entry-agent-startup-welcome.json",
            "design-package-conformance.contract.json",
            "runtime-instruction-conformance.json",
            "meta-team-audit.contract.json",
            "design-output.zip",
            "design-output-manifest.json",
            "local-resource-allocation.map.json",
            "source-resource-manifest.json",
            "docs/team-usage-guide.md",
            "docs/entry-agent-startup-welcome.md",
        ],
        "required_package_artifacts": [
            "design-intermediate-results.json and docs/design-intermediate-results.md",
            "design-output.zip, design-output-manifest.json, and docs/design-output-archive.md",
            "entry-agent-startup-welcome.json and docs/entry-agent-startup-welcome.md",
            "generated target-team agents and functions list",
            "agent-profiles.json, profiles/*.agent-profile.json, and docs/agent-profiles.md",
            "local-resource-allocation.map.json, source-resource-manifest.json, and docs/local-resource-allocation-map.md",
            "workflow-preservation-gate.json and docs/workflow-preservation-gate.md",
            "design-package-conformance.contract.json and docs/design-package-conformance-contract.md",
            "runtime-instruction-conformance.json and docs/runtime-instruction-conformance.md",
            "meta-team-audit.contract.json and docs/meta-team-audit-contract.md",
            "runtime agent artifacts for every planned top-level agent",
            "one user-facing entry agent artifact",
            "s2t-agent-registry.json or runtime-equivalent manifest",
            "docs/team-usage-guide.md",
            "docs/runtime-invocation-contract.md",
            "runtime-invocation-contract.json",
            "docs/register-readiness-contract.md",
            "register-readiness-contract.json",
            "post-registration smoke-test instructions",
            "docs/design-continuation-prompt-templates.md and design-continuation-prompt-templates.json as design-result artifacts",
            "docs/post-package-prompt-templates.md and post-package-prompt-templates.json",
            "package-end Codex registration/start and Codex-use prompt templates only",
        ],
        "register_hard_runtime_requirements": [
            "all planned runtime agent artifacts are installed in the target runtime",
            "design/package conformance contract is passed or explicitly blocks runtime use with reexecution_required=true",
            "runtime instruction conformance proves source-derived constraints are materialized in agent instructions",
            "the registered manifest includes every planned top-level agent",
            "the registered manifest includes the entry agent artifact",
            "the entry agent can be invoked through the runtime using the registered entry-agent identity",
            "the entry agent can hand off at least one work order to every specialist agent",
            "each specialist agent can return a structured result to the entry agent or orchestrator",
            "reviewer or verifier gates can block a bad output",
            "state/artifact handoff paths are usable for the selected runtime",
            "runtime prompt rewrite uses the registered target entry agent instead of the source skill name",
            "runtime-critical local resources are bundled in the package or remain accessible through a recorded source_root and local-resource-allocation map",
            "registration does not mark entry_agent_runnable=true until runtime execution evidence or an explicit smoke-test pass is recorded",
            "registered target-team execution must not fall back to sequential or single-agent simulation",
            "the entry agent stops with target-team execution blocked when specialist handoff is unavailable",
        ],
        "post_registration_smoke_tests": [
            {
                "id": "entry_invocation",
                "owner": entry,
                "goal": "Invoke the registered entry agent by runtime name and receive an intake/state-lookup response that renders or summarizes the startup welcome page.",
                "required_evidence": "runtime transcript, invocation log, or explicit smoke-test pass record",
            },
            {
                "id": "specialist_handoff_all_agents",
                "owner": entry,
                "goal": "Send a shallow work order from the entry agent to every non-entry specialist agent and receive a structured result.",
                "required_evidence": "handoff transcript or runtime log for each specialist agent",
            },
            {
                "id": "review_gate_blocks",
                "owner": "independent reviewer/verifier",
                "goal": "Demonstrate that a reviewer/verifier gate can reject or block an intentionally incomplete output.",
                "required_evidence": "gate decision record showing reject/block behavior",
            },
            {
                "id": "state_artifact_handoff",
                "owner": "entry/orchestrator",
                "goal": "Pass a named artifact or state summary across at least one handoff and preserve its identity in the result.",
                "required_evidence": "artifact id, state key, or handoff record preserved across roles",
            },
        ],
        "register_blockers": register_blockers,
    }


def write_registry(out: Path, plan: dict[str, Any], agents: list[dict[str, Any]], *, team_id: str, team_kind: str, source_skill: str | None, target: str, prefix: str, entry: str, execution_path: str = "direct-skill", current_run_fanout_status: str | None = None, route: str = "source-to-team", delivery: str = "package") -> None:
    fanout_status = normalized_fanout_status(execution_path, current_run_fanout_status)
    source_constraints = source_derived_runtime_constraints(plan)
    invocation_policy = runtime_invocation_policy(
        team_id=team_id,
        team_kind=team_kind,
        source_skill=source_skill,
        target=target,
        entry=entry,
        execution_path=execution_path,
        current_run_fanout_status=current_run_fanout_status,
        route=route,
        delivery=delivery,
    )
    next_templates = delivery_next_prompt_templates(
        team_id=team_id,
        team_kind=team_kind,
        source_skill=source_skill,
        target=target,
        entry=entry,
        route=route,
        delivery=delivery,
    )
    package_next_templates = {
        "package_end_codex_register_and_start_openai_codex": next_templates["package_end_codex_register_and_start_openai_codex"],
        "registered_entry_agent_use_after_codex_smoke_tests": next_templates["registered_entry_agent_use_after_codex_smoke_tests"],
        "current_session_target_team_fanout_prompt": next_templates["current_session_target_team_fanout_prompt"],
    }
    design_next_templates = {
        key: value
        for key, value in next_templates.items()
        if key == "design_to_package_prompt" or key.startswith("design_continuation_") or key == "api_runner_role_simulation_prompt"
    }
    registry = {
        "schema_version": 1,
        "managed_by": "skill2team",
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target.replace("_", "-"),
        "model_invocation_policy": model_invocation_policy(),
        "architecture_policy": architecture_build_policy(),
        "target_team_execution_guard_policy": target_team_execution_guard_policy(entry, agents),
        "generated_target_team_agents": generated_agents_summary(agents),
        "agent_profiles": [agent_profile(a, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=target, entry=entry, source_runtime_constraints=source_constraints) for a in agents],
        "source_derived_runtime_constraints": source_constraints,
        "design_package_conformance_contract": "design-package-conformance.contract.json",
        "runtime_instruction_conformance": "runtime-instruction-conformance.json",
        "meta_team_audit_contract": "meta-team-audit.contract.json",
        "design_output_archive": "design-output.zip",
        "design_output_manifest": "design-output-manifest.json",
        "entry_agent_startup_welcome": "entry-agent-startup-welcome.json",
        "entry_agent_startup_welcome_doc": "docs/entry-agent-startup-welcome.md",
        "route": route,
        "delivery": delivery,
        "execution_path": execution_path,
        "current_run_fanout_status": fanout_status,
        "generation_run_fanout_status": fanout_status,
        "target_team_registration_status": "not_registered",
        "registration_status": "not_registered",
        "entry_agent_runnable": False,
        "registered_target_team_smoke_status": "not_registered",
        "registered_agent_invocation_verified": False,
        "target_run_fanout_status": "not_started",
        "allowed_current_session_target_fanout_status": "real_session_target_subagents",
        "current_session_target_fanout_allowed": True,
        "execution_mode": fanout_execution_mode(fanout_status, execution_path),
        "fallback_declaration": fanout_fallback(fanout_status, execution_path),
        "name_prefix": prefix,
        "entry_agent_id": entry,
        "team_usage_guide": "docs/team-usage-guide.md",
        "runtime_invocation_contract": "docs/runtime-invocation-contract.md",
        "register_readiness_contract": "docs/register-readiness-contract.md",
        "register_readiness_contract_json": "register-readiness-contract.json",
        "runtime_invocation_policy": invocation_policy,
        "next_use_prompt_templates": package_next_templates,
        "design_continuation_prompt_templates": design_next_templates,
        "package_end_prompt_templates": package_next_templates,
        "register_readiness_policy": register_readiness_policy(
            agents,
            team_id=team_id,
            team_kind=team_kind,
            source_skill=source_skill,
            target=target,
            entry=entry,
        ),
        "source_prompt_rewrite_policy": invocation_policy["source_prompt_rewrite_policy"],
        "agents": [
            {
                "agent_id": agent_id(a),
                "original_agent_id": a.get("original_agent_id"),
                "display_name": display(a),
                "role": "entry" if a.get("entry_agent") else a.get("role", a.get("original_agent_id", agent_id(a))),
                "entry": bool(a.get("entry_agent")),
                "artifact_path": artifact_path_for(target, agent_id(a)),
                "profile_path": profile_path_for(agent_id(a)),
                "agent_node_id": agent_id(a).replace("-", "_"),
            }
            for a in agents
        ],
        "registered_files": [],
        "planned_registered_files": planned_registered_files_for(target, agents, team_id),
        "previous_registration_action": "none",
    }
    if team_kind == "meta":
        registry.update(meta_team_registry_fields(agents))
    write_json(out / "s2t-agent-registry.json", registry)
    if target.replace("-", "_") == "codex":
        registry_dir = out / ".codex" / "s2t-agent-registrations"
        ensure(registry_dir)
        write_json(registry_dir / f"{team_id}.json", registry)

def artifact_path_for(target: str, aid: str) -> str:
    t = target.replace("-", "_")
    if t != "codex":
        raise ValueError(f"Unsupported target runtime: {target}. Only codex is generated and tested.")
    return f".codex/agents/{aid}.toml"


def write_architecture_workflow_artifacts(out: Path, plan: dict[str, Any], agents: list[dict[str, Any]], *, team_id: str, team_kind: str, source_skill: str | None, target: str, entry: str, route: str, delivery: str) -> None:
    ensure(out / "docs")
    preservation = workflow_preservation_payload(plan)
    source_constraints = source_derived_runtime_constraints(plan, preservation)
    architecture = {
        "schema_version": "s2t-agent-architecture-v1",
        "managed_by": "skill2team",
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target.replace("_", "-"),
        "model_invocation_policy": model_invocation_policy(),
        "architecture_policy": architecture_build_policy(),
        "entry_agent_id": entry,
        "route": route,
        "delivery": delivery,
        "principle": "Agent architecture is accountability topology, not runtime control flow. Default representation is framework-neutral agent relationship graph.",
        "top_level_agent_count": len(agents),
        "agent_count_policy": "Prefer 5-6 top-level agents for nontrivial teams; justify any other count.",
        "selected_pattern": plan.get("architecture_pattern", "coordinator_specialists"),
        "count_rationale": plan.get("agent_count_rationale", "generated_from_plan_or_default; review if count is outside 5-6"),
        "agents": [
            {
                "agent_id": agent_id(a),
                "display_name": display(a),
                "mission": mission(a),
                "owned_skills": a.get("owned_skills", []),
                "tools_policy": a.get("tools_policy", {}),
                "entry_agent": bool(a.get("entry_agent")),
                "profile_path": profile_path_for(agent_id(a)),
                "agent_node_id": agent_id(a).replace("-", "_"),
            }
            for a in agents
        ],
        "relationship_types": ["routes_to", "hands_off_to", "reviews", "approves", "blocks", "shares_state_with", "escalates_to"],
        "source_architecture": plan.get("architecture", "not_provided_in_plan")
    }
    workflow = {
        "schema_version": "s2t-workflow-orchestration-v1",
        "managed_by": "skill2team",
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target.replace("_", "-"),
        "model_invocation_policy": model_invocation_policy(),
        "architecture_policy": architecture_build_policy(),
        "entry_agent_id": entry,
        "route": route,
        "delivery": delivery,
        "principle": "Workflow orchestration is runtime control flow, not agent topology.",
        "workflow_primitives_supported": [
            "sequence", "branch", "conditional_edge", "loop_retry_repair", "gate",
            "fan_out", "fan_in_merge", "human_wait", "checkpoint_resume", "terminal_boundary"
        ],
        "owner_rule": "Each workflow node names an owner agent, but workflow nodes do not automatically become agents.",
        "source_workflow": preservation["source_workflow"],
        "workflow_nodes": preservation["workflow_nodes"],
        "workflow_edges": preservation["workflow_edges"],
        "stage_mappings": preservation["stage_mappings"],
        "stage_internal_deliverables": preservation["stage_internal_deliverables"],
        "human_intervention_points": preservation["human_intervention_points"],
        "user_input_nodes": preservation["user_input_nodes"],
        "human_intervention_policy": preservation["human_intervention_policy"],
        "checkpoint_resume_points": preservation["checkpoint_resume_points"],
        "gate_points": preservation["gate_points"],
        "source_derived_runtime_constraints": source_constraints,
        "workflow_preservation_gate": {
            "status": preservation["preservation_gate_status"],
            "blockers": preservation["preservation_gate_blockers"],
            "field_presence": preservation["field_presence"],
        },
    }
    write_json(out / "agent-architecture.map.json", architecture)
    write_json(out / "workflow-orchestration.map.json", workflow)
    (out / "docs" / "agent-architecture-map.md").write_text(f"""# Agent Architecture Map

- team_id: `{team_id}`
- team_kind: `{team_kind}`
- source_skill: `{source_skill or 'unknown'}`
- target_runtime: `{target.replace('_', '-')}`
- architecture_method: `framework-neutral agent architecture relationship graph with profile-based agents`
- entry_agent_id: `{entry}`
- top_level_agent_count: `{len(agents)}`

Agent architecture describes accountability topology: entry, routing, handoffs, review authority, shared state, context boundaries, and skill ownership. It is not the workflow control-flow diagram. The default representation is a framework-neutral agent architecture relationship graph where agent profiles are nodes.

Prefer 5-6 top-level agents for nontrivial teams. If this package uses another count, review and record the strong rationale in `agent-architecture.map.json`.
""", encoding="utf-8")
    (out / "docs" / "workflow-orchestration-map.md").write_text(f"""# Workflow Orchestration Map

- team_id: `{team_id}`
- team_kind: `{team_kind}`
- source_skill: `{source_skill or 'unknown'}`
- target_runtime: `{target.replace('_', '-')}`
- architecture_method: `framework-neutral agent architecture relationship graph with profile-based agents`
- entry_agent_id: `{entry}`

Workflow orchestration describes runtime control flow: sequence, branch, loop, gate, fan-out/fan-in, human wait, checkpoint/resume, and terminal boundaries. It is not the agent architecture map.

Each workflow node should name an owner agent, but a workflow node does not automatically become a top-level agent.

The map is incomplete if it only contains a summary. It must preserve source-stage duties, named stage-internal deliverables, required user input nodes, human intervention choices, gates, checkpoint/resume points, and terminal boundaries in machine-readable fields.

Source-derived runtime constraints in this map must be materialized again in package contracts, agent profiles, and runtime agent instructions. If they are not, package conformance is blocked and the responsible Skill2Team phase must be re-executed.
""", encoding="utf-8")

def write_flow_control_artifacts(out: Path, plan: dict[str, Any], *, team_id: str, team_kind: str, source_skill: str | None, target: str, entry: str, execution_path: str, route: str, delivery: str) -> None:
    ensure(out / "docs")
    preservation = workflow_preservation_payload(plan)
    source_constraints = source_derived_runtime_constraints(plan, preservation)
    contract = {
        "schema_version": "s2t-flow-control-v1",
        "managed_by": "skill2team",
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target.replace("_", "-"),
        "model_invocation_policy": model_invocation_policy(),
        "architecture_policy": architecture_build_policy(),
        "entry_agent_id": entry,
        "route": route,
        "delivery": delivery,
        "execution_path": execution_path,
        "control_flow_types_supported": [
            "sequence", "switch_case", "branch", "loop_back_edge", "gate",
            "fan_out_parallel_group", "fan_in_merge_join", "user_input_node", "human_wait",
            "exception_compensation", "checkpoint_resume", "terminal"
        ],
        "agent_boundary_rule": {
            "internal_when_all_true": [
                "local_to_one_agent", "bounded", "no_shared_state_mutation",
                "no_named_public_artifact", "no_independent_gate_required",
                "cannot_make_downstream_artifacts_stale"
            ],
            "inter_agent_when_any_true": [
                "shared_artifact_changes", "checkpoint_or_registry_changes",
                "downstream_may_become_stale", "independent_gate_required",
                "human_choice_required", "parallel_or_merge_coordination_required",
                "terminal_boundary_crossed"
            ]
        },
        "rerun_policy": {
            "default_scope": "affected_dependency_closure",
            "parallel_item_scope": "rerun_changed_items_only_when_item_dependencies_are_known",
            "whole_group_scope": "rerun_when_group_level_invariant_changes",
            "downstream_reuse_rule": "reuse_only_if_consumed_upstream_fingerprints_match_current_valid_upstream_fingerprints"
        },
        "merge_policy": {
            "skipped_cases_are_not_failures": True,
            "semantic_conflicts": "block_and_emit_conflict_ledger",
            "partial_success": "allowed_only_when_merge_rule_declares_it"
        },
        "resume_policy": {
            "resume_by": "dependency_graph_stale_check",
            "checkpoint_rule": "rebuild_or_validate_after_state_mutation",
            "statuses": ["valid", "stale", "skipped", "failed", "blocked", "terminal"]
        },
        "source_flow_control": source_flow_control_payload(plan, preservation),
        "human_intervention_points": preservation["human_intervention_points"],
        "user_input_nodes": preservation["user_input_nodes"],
        "human_intervention_policy": preservation["human_intervention_policy"],
        "stage_internal_deliverables": preservation["stage_internal_deliverables"],
        "checkpoint_resume_points": preservation["checkpoint_resume_points"],
        "gate_points": preservation["gate_points"],
        "source_derived_runtime_constraints": source_constraints,
        "conformance_reexecution_policy": {
            "on_missing_design_constraint": "rerun source-mapping/workflow-orchestration from the earliest stale dependency",
            "on_missing_package_constraint": "rerun runtime-adapter/package generation after design is corrected",
            "forbid_downstream_text_only_patch": True,
        },
        "workflow_preservation_gate": {
            "status": preservation["preservation_gate_status"],
            "blockers": preservation["preservation_gate_blockers"],
        },
    }
    write_json(out / "flow-control.contract.json", contract)
    write_json(out / "artifact-lineage.schema.json", {
        "schema_version": "s2t-artifact-lineage-v1",
        "artifact_fields": [
            "artifact_id", "producer_node", "producer_owner", "schema_version",
            "consumed_inputs", "input_fingerprints", "output_fingerprint", "status", "downstream_consumers"
        ],
        "statuses": ["valid", "stale", "skipped", "failed", "blocked", "archived", "terminal"]
    })
    write_json(out / "event-log.schema.json", {
        "schema_version": "s2t-event-log-v1",
        "event_fields": [
            "event_id", "event_type", "node_id", "owner", "timestamp",
            "input_artifacts", "output_artifacts", "decision_case", "gate_result", "checkpoint_result"
        ],
        "event_types": ["node_started", "artifact_generated", "decision_recorded", "gate_passed", "gate_failed", "artifact_marked_stale", "checkpoint_validated", "human_wait", "terminal"]
    })
    md = f"""# Flow-Control Contract

- team_id: `{team_id}`
- team_kind: `{team_kind}`
- source_skill: `{source_skill or 'unknown'}`
- target_runtime: `{target.replace('_', '-')}`
- architecture_method: `framework-neutral agent architecture relationship graph with profile-based agents`
- entry_agent_id: `{entry}`
- route: `{route}`
- delivery: `{delivery}`
- execution_path: `{execution_path}`

## Supported control-flow elements

Sequence, switch/case, branch, loop/back-edge, gate, fan-out/parallel group, fan-in/merge/join, required user input node, human wait, exception/compensation, checkpoint/resume, and terminal boundary.

## Boundary rule

Keep control flow inside one agent only when it is local, bounded, does not mutate shared state, does not create a named public artifact, does not require independent approval, and cannot make downstream artifacts stale. Otherwise, make it an explicit handoff, gate, state update, merge, or human-wait boundary.

## Rerun and resume

Downstream work may reuse prior results only when the upstream artifacts it consumed are still the current valid versions. If an upstream artifact changed, mark affected downstream nodes stale and rerun only the affected dependency closure unless a group-level invariant requires a full group rerun.

See `flow-control.contract.json` for the machine-readable skeleton.

Design/package conformance failures are rerun/resume events. If a source-derived runtime constraint is missing downstream, mark the responsible phase stale and re-execute it rather than editing only generated text.
"""
    (out / "docs" / "flow-control-contract.md").write_text(md, encoding="utf-8")
    lineage_md = """# Artifact Lineage and Rerun Policy

Each named artifact should record its producing node, owner, consumed upstream artifacts, input fingerprints when available, output fingerprint when available, schema or contract version, and status.

Use the smallest safe recomputation boundary:

1. Reuse artifacts whose consumed input fingerprints still match.
2. Rerun only changed parallel items when item inputs changed independently.
3. Rerun a whole parallel group when a shared invariant, schema, route, or merge rule changed.
4. Rerun downstream merge/review nodes when any consumed upstream artifact changed.
5. Stop for user or gate input when a conflict is semantic or unsafe to auto-merge.
"""
    (out / "docs" / "artifact-lineage-and-rerun-policy.md").write_text(lineage_md, encoding="utf-8")
    resume_md = """# Resume Policy

Before resuming, read current state, available artifacts, artifact lineage, chosen/skipped branches, gate results, and checkpoint status. Mark missing, failed, blocked, or stale nodes. Continue from the smallest valid recomputation boundary and rebuild or validate checkpoints before claiming recoverability.
"""
    (out / "docs" / "resume-policy.md").write_text(resume_md, encoding="utf-8")



def generated_agents_summary(agents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "agent_id": agent_id(a),
            "display_name": display(a),
            "function": mission(a),
            "entry": bool(a.get("entry_agent")),
            "owned_skills": a.get("owned_skills", []),
            "artifact_path": artifact_path_for("codex", agent_id(a)),
            "profile_path": profile_path_for(agent_id(a)),
            "profile_id": f"{agent_id(a)}.profile",
            "agent_node_id": agent_id(a).replace("-", "_"),
        }
        for a in agents
    ]


def generated_agents_markdown(agents: list[dict[str, Any]]) -> str:
    rows = ["| Agent id | Entry | Function |", "|---|---:|---|"]
    for a in generated_agents_summary(agents):
        rows.append(f"| `{a['agent_id']}` | {'yes' if a['entry'] else 'no'} | {a['function']} |")
    return "\n".join(rows)


def write_entry_agent_startup_welcome(
    out: Path,
    plan: dict[str, Any],
    agents: list[dict[str, Any]],
    *,
    team_id: str,
    team_kind: str,
    source_skill: str | None,
    target: str,
    entry: str,
    route: str,
    delivery: str,
) -> None:
    ensure(out / "docs")
    preservation = workflow_preservation_payload(plan)
    policy = preservation["human_intervention_policy"]
    payload = {
        "schema_version": "s2t-entry-agent-startup-welcome-v1",
        "managed_by": "skill2team",
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target.replace("_", "-"),
        "entry_agent_id": entry,
        "route": route,
        "delivery": delivery,
        "source_startup_reference": preservation["source_startup_reference"],
        "source_startup_adaptation_rule": (
            "Use the source skill startup page only as a workflow/content reference. "
            "Rewrite skill-language into entry-agent language: ask the user to start or use the generated entry agent, "
            "name the generated team roles, and do not copy source self-invocation wording verbatim."
        ),
        "must_render_before_first_migrated_stage": True,
        "startup_status_fields": [
            "registration_status",
            "registered_target_team_smoke_status",
            "target_run_fanout_status",
            "source_material",
            "route",
            "delivery",
            "target_runtime",
            "human_interaction_execution_mode",
        ],
        "required_startup_user_input_nodes": preservation["user_input_nodes"],
        "human_intervention_points": preservation["human_intervention_points"],
        "human_intervention_policy": policy,
        "default_human_interaction_execution_mode": policy["default_execution_mode"],
        "selected_human_interaction_execution_mode": policy["selected_execution_mode"],
        "team_agents": generated_agents_summary(agents),
        "entry_agent_rules": [
            "Render or summarize this welcome page before entering the first real migrated workflow stage.",
            "Ask for missing source-required startup inputs and unresolved human-intervention retention choices.",
            "Default to preserving source human interaction steps when the user does not explicitly choose automation.",
            "If the user selects full automation, require an audit record for every auto-advanced human intervention point.",
            "Do not run past preserved human waits, approvals, choices, or terminal boundaries.",
            "Do not describe single-agent work as target-team execution.",
        ],
    }
    write_json(out / "entry-agent-startup-welcome.json", payload)
    input_lines = "\n".join(
        f"- `{compact_text(item, 180)}`"
        for item in payload["required_startup_user_input_nodes"]
    ) or "- none recorded; if the source has required inputs, rerun source mapping"
    hitl_lines = "\n".join(
        f"- `{compact_text(item, 180)}`"
        for item in payload["human_intervention_points"]
    ) or "- none recorded; if the source has choices, approvals, waits, or terminal prompts, rerun workflow extraction"
    mode_lines = "\n".join(f"- `{mode}`" for mode in HUMAN_INTERACTION_EXECUTION_MODES)
    md = f"""# Entry Agent Startup Welcome

- team_id: `{team_id}`
- team_kind: `{team_kind}`
- source_skill: `{source_skill or 'unknown'}`
- target_runtime: `{target.replace('_', '-')}`
- route: `{route}`
- delivery: `{delivery}`
- entry_agent_id: `{entry}`
- default_human_interaction_execution_mode: `{policy['default_execution_mode']}`
- selected_human_interaction_execution_mode: `{policy['selected_execution_mode']}`

This is the generated target team's entry-agent welcome page. It adapts the source skill's startup behavior into agent language for this team. The entry agent must show or summarize it before entering the first real migrated workflow stage.

## Startup Status

The entry agent must identify registration status, smoke-test status, target fan-out status, source material, route, delivery, target runtime, and human-interaction execution mode before running the migrated workflow.

## Team Roles

{generated_agents_markdown(agents)}

## Required Startup Inputs

{input_lines}

## Human Interaction Mode

Ask at startup whether to keep the source workflow's human-interaction steps or automate selected parts. Default to preserving source-mandated user waits, approvals, selections, and terminal boundaries.

Available modes:

{mode_lines}

## Human Intervention Points

{hitl_lines}

If a required source input or preserved human intervention choice is missing, the entry agent must ask or block. It must not silently choose full automation and must not run through the whole workflow in one pass when the source workflow requires user decisions between steps.
"""
    (out / "docs" / "entry-agent-startup-welcome.md").write_text(md, encoding="utf-8")


def write_design_intermediate_results(out: Path, plan: dict[str, Any], agents: list[dict[str, Any]], *, team_id: str, team_kind: str, source_skill: str | None, target: str, prefix: str, entry: str, route: str, delivery: str, execution_path: str) -> None:
    ensure(out / "docs")
    preservation = workflow_preservation_payload(plan)
    source_constraints = source_derived_runtime_constraints(plan, preservation)
    payload = {
        "schema_version": "s2t-design-intermediate-results-v1",
        "managed_by": "skill2team",
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target.replace("_", "-"),
        "model_invocation_policy": model_invocation_policy(),
        "architecture_policy": architecture_build_policy(),
        "route": route,
        "delivery": delivery,
        "execution_path": execution_path,
        "name_prefix": prefix,
        "entry_agent_id": entry,
        "design_layers": {
            "agent_architecture_map": "agent-architecture.map.json",
            "workflow_orchestration_map": "workflow-orchestration.map.json",
            "control_flow_resume_contract": "flow-control.contract.json",
        },
        "source_inventory": source_inventory_payload(plan),
        "local_resource_allocation_map": "local-resource-allocation.map.json",
        "source_resource_manifest": "source-resource-manifest.json",
        "entry_agent_startup_welcome": "entry-agent-startup-welcome.json",
        "entry_agent_startup_welcome_doc": "docs/entry-agent-startup-welcome.md",
        "current_state_diagnosis": plan.get("diagnosis", plan.get("current_state_diagnosis", "not_provided_in_plan")),
        "original_workflow_extraction": preservation["source_workflow"],
        "source_startup_reference": preservation["source_startup_reference"],
        "workflow_preservation": preservation,
        "source_derived_runtime_constraints": source_constraints,
        "design_package_conformance_contract": "design-package-conformance.contract.json",
        "runtime_instruction_conformance": "runtime-instruction-conformance.json",
        "architecture_pattern": plan.get("architecture_pattern", "coordinator_specialists"),
        "agent_count_rationale": plan.get("agent_count_rationale", "generated_from_plan_or_default; review if count is outside 5-6"),
        "generated_target_team_agents": generated_agents_summary(agents),
        "agent_profiles": [agent_profile(a, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=target, entry=entry, source_runtime_constraints=source_constraints) for a in agents],
        "skill_allocation_matrix": plan.get("skill_allocation_matrix", derived_skill_allocation_matrix(agents)),
        "handoff_contracts": plan.get("handoff_contracts", derived_handoff_contracts(preservation)),
        "gate_and_review_model": plan.get("gate_and_review_model", derived_gate_and_review_model(preservation, agents)),
        "unresolved_questions_and_risks": plan.get("unresolved_questions_and_risks", []),
    }
    write_json(out / "design-intermediate-results.json", payload)
    md = f"""# Design Intermediate Results

- team_id: `{team_id}`
- team_kind: `{team_kind}`
- source_skill: `{source_skill or 'unknown'}`
- target_runtime: `{target.replace('_', '-')}`
- model_runner_default: `OpenAI Codex`
- architecture_method: `framework-neutral agent architecture relationship graph with profile-based agents`
- route: `{route}`
- delivery: `{delivery}`
- entry_agent_id: `{entry}`

This file carries the design-phase summary forward into the package handoff so the recipient can inspect the package without rerunning design.

## Generated Target-Team Agents and Functions

{generated_agents_markdown(agents)}

## Design Layers

- Agent Architecture Map: `agent-architecture.map.json`
- Workflow Orchestration Map: `workflow-orchestration.map.json`
- Control-Flow & Resume Contract: `flow-control.contract.json`
- Workflow Preservation Gate: `workflow-preservation-gate.json`
- Entry Agent Startup Welcome: `entry-agent-startup-welcome.json` and `docs/entry-agent-startup-welcome.md`
- Design/Package Conformance Contract: `design-package-conformance.contract.json`
- Runtime Instruction Conformance: `runtime-instruction-conformance.json`
- Agent Profiles: `agent-profiles.json` and `profiles/*.agent-profile.json`

## Source Inventory

```json
{json.dumps(payload['source_inventory'], ensure_ascii=False, indent=2)}
```

## Current-State Diagnosis

```json
{json.dumps(payload['current_state_diagnosis'], ensure_ascii=False, indent=2)}
```

## Original Workflow Extraction

```json
{json.dumps(payload['original_workflow_extraction'], ensure_ascii=False, indent=2)}
```

## Package Review Notes

- Keep Agent Architecture Map separate from Workflow Orchestration Map.
- Prefer 5-6 top-level agents unless a strong rationale is recorded.
- Preserve required user input nodes and source human-interaction steps by default; full automation requires explicit user selection and audit records.
- Do not hard-code a specific source package name or task id.
- Design quality gate is carried into package release checks.
- Package completion does not prove Codex runtime registration.
"""
    (out / "docs" / "design-intermediate-results.md").write_text(md, encoding="utf-8")


def write_local_resource_allocation_artifacts(
    out: Path,
    plan: dict[str, Any],
    agents: list[dict[str, Any]],
    *,
    team_id: str,
    team_kind: str,
    source_skill: str | None,
    target: str,
    entry: str,
    route: str,
    delivery: str,
    source_root: str | None,
    bundle_mode: str,
) -> None:
    ensure(out / "docs")
    source_inventory = source_inventory_payload(plan)
    bundled_files, bundle_blockers = copy_source_resources(out, source_root, source_inventory, bundle_mode)
    payload = local_resource_allocation_payload(
        plan,
        agents,
        team_id=team_id,
        team_kind=team_kind,
        source_skill=source_skill,
        target=target,
        entry=entry,
        route=route,
        delivery=delivery,
        source_root=source_root,
        bundle_mode=bundle_mode,
        bundled_files=bundled_files,
        bundle_blockers=bundle_blockers,
    )
    manifest = {
        "schema_version": "s2t-source-resource-manifest-v1",
        "managed_by": "skill2team",
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target.replace("_", "-"),
        "source_root": source_root,
        "resource_copy_mode": bundle_mode,
        "source_inventory": payload["source_inventory"],
        "bundled_resource_files": bundled_files,
        "bundle_blockers": bundle_blockers,
        "resource_gate_status": payload["resource_gate_status"],
    }
    write_json(out / "local-resource-allocation.map.json", payload)
    write_json(out / "source-resource-manifest.json", manifest)
    allocation_lines = "\n".join(
        f"- `{row.get('resource')}` -> owner `{row.get('owner_agent')}`, class `{row.get('resource_class')}`, action `{row.get('migration_action')}`"
        for row in payload["allocation_map"]
    ) or "- none"
    blocker_lines = "\n".join(f"- {b}" for b in payload["resource_gate_blockers"]) or "- none"
    bundled_lines = "\n".join(f"- `{p}`" for p in bundled_files[:200]) or "- none"
    if len(bundled_files) > 200:
        bundled_lines += f"\n- ... {len(bundled_files) - 200} more files omitted from this Markdown view; see source-resource-manifest.json"
    md = f"""# Local Resource Allocation Map

- team_id: `{team_id}`
- team_kind: `{team_kind}`
- source_skill: `{source_skill or 'unknown'}`
- target_runtime: `{target.replace('_', '-')}`
- entry_agent_id: `{entry}`
- resource_copy_mode: `{bundle_mode}`
- source_root: `{source_root or 'not_provided'}`
- resource_gate_status: `{payload['resource_gate_status']}`

## Allocation

{allocation_lines}

## Bundled Files

{bundled_lines}

## Blockers

{blocker_lines}

Runtime-critical local resources must be either bundled in this package or kept accessible through a recorded source_root. Templates define format, scripts are tool-only until gated, assets are visual/style-only unless the source workflow explicitly makes them authoritative, and examples are example-only.
"""
    (out / "docs" / "local-resource-allocation-map.md").write_text(md, encoding="utf-8")


def write_workflow_preservation_gate(out: Path, plan: dict[str, Any], *, team_id: str, team_kind: str, source_skill: str | None, target: str, entry: str, route: str, delivery: str) -> None:
    ensure(out / "docs")
    payload = workflow_preservation_payload(plan)
    payload.update({
        "managed_by": "skill2team",
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target.replace("_", "-"),
        "entry_agent_id": entry,
        "route": route,
        "delivery": delivery,
    })
    write_json(out / "workflow-preservation-gate.json", payload)
    blocker_lines = "\n".join(f"- {b}" for b in payload["preservation_gate_blockers"]) if payload["preservation_gate_blockers"] else "- none"
    input_lines = "\n".join(f"- `{compact_text(item, 180)}`" for item in payload["user_input_nodes"]) or "- none"
    hitl_lines = "\n".join(f"- `{compact_text(item, 180)}`" for item in payload["human_intervention_points"]) or "- none"
    md = f"""# Workflow Preservation Gate

- team_id: `{team_id}`
- team_kind: `{team_kind}`
- source_skill: `{source_skill or 'unknown'}`
- target_runtime: `{target.replace('_', '-')}`
- entry_agent_id: `{entry}`
- preservation_gate_status: `{payload['preservation_gate_status']}`

## Required Preservation Scope

The generated team must preserve source workflow behavior that affects correctness: public stage boundaries, stage-internal deliverables, candidate or registry artifacts, human intervention points, gates, checkpoint/resume records, rerun rules, and terminal boundaries.

Human intervention points are user-selectable at design/package time. Source-mandated human waits and approvals default to `preserve_as_human_wait`; the top-level execution mode defaults to `preserve_source_human_interaction_steps`. Auto-advance is allowed only when the user explicitly selects it or the source proves the point is redundant.

Required user input nodes from the source must remain entry-agent questions or human-wait edges. They cannot be silently collapsed into an all-at-once run.

## Required User Input Nodes

{input_lines}

## Human Intervention Points

{hitl_lines}

## Blockers

{blocker_lines}

If blockers are present, the package can be inspected, but Skill2Team must not claim that the target team faithfully preserves the source workflow until the missing fields are supplied and the gate passes.
"""
    (out / "docs" / "workflow-preservation-gate.md").write_text(md, encoding="utf-8")



def write_agent_profiles(out: Path, plan: dict[str, Any], agents: list[dict[str, Any]], *, team_id: str, team_kind: str, source_skill: str | None, target: str, entry: str) -> None:
    ensure(out / "profiles")
    ensure(out / "docs")
    source_constraints = source_derived_runtime_constraints(plan)
    profiles = [agent_profile(a, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=target, entry=entry, source_runtime_constraints=source_constraints) for a in agents]
    write_json(out / "agent-profiles.json", {
        "schema_version": "s2t-agent-profiles-v1",
        "managed_by": "skill2team",
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target.replace("_", "-"),
        "entry_agent_id": entry,
        "architecture_policy": architecture_build_policy(),
        "source_derived_runtime_constraints": source_constraints,
        "design_package_conformance_contract": "design-package-conformance.contract.json",
        "runtime_instruction_conformance": "runtime-instruction-conformance.json",
        "profiles": profiles,
    })
    for profile in profiles:
        write_json(out / profile["profile_path"], profile)
    rows = ["| Agent id | Entry | Profile path | Agent node | Function |", "|---|---:|---|---|---|"]
    for profile in profiles:
        rows.append(f"| `{profile['agent_id']}` | {'yes' if profile['entry_agent'] else 'no'} | `{profile['profile_path']}` | `{profile['agent_node_id']}` | {profile['mission']} |")
    md = f"""# Agent Profiles

- team_id: `{team_id}`
- team_kind: `{team_kind}`
- source_skill: `{source_skill or 'unknown'}`
- target_runtime: `{target.replace('_', '-')}`
- entry_agent_id: `{entry}`
- architecture_method: `framework-neutral agent architecture relationship graph with profile-based agents`

Agent profiles are durable role definitions. Treat each profile as a conceptual agent node in the framework-neutral architecture relationship graph. Runtime-specific implementations can map these nodes and typed edges into their own framework only as an explicit follow-up.

Each profile carries source-derived runtime constraints assigned to that role. If a required constraint is missing from `agent-profiles.json`, `runtime-instruction-conformance.json`, or the corresponding `.codex/agents/*.toml` file, package use is blocked until the responsible Skill2Team phase is re-executed.

{chr(10).join(rows)}
"""
    (out / "docs" / "agent-profiles.md").write_text(md, encoding="utf-8")


def write_design_package_conformance_artifacts(
    out: Path,
    plan: dict[str, Any],
    agents: list[dict[str, Any]],
    *,
    team_id: str,
    team_kind: str,
    source_skill: str | None,
    target: str,
    entry: str,
    route: str,
    delivery: str,
) -> None:
    ensure(out / "docs")
    runtime_payload = runtime_instruction_conformance_payload(
        out,
        plan,
        agents,
        team_id=team_id,
        team_kind=team_kind,
        source_skill=source_skill,
        target=target,
        entry=entry,
    )
    conformance = design_package_conformance_payload(
        plan,
        runtime_payload,
        team_id=team_id,
        team_kind=team_kind,
        source_skill=source_skill,
        target=target,
        entry=entry,
        route=route,
        delivery=delivery,
    )
    write_json(out / "runtime-instruction-conformance.json", runtime_payload)
    write_json(out / "design-package-conformance.contract.json", conformance)
    blockers = "\n".join(f"- {b}" for b in conformance["conformance_blockers"]) or "- none"
    constraint_rows = "\n".join(
        f"- `{c['constraint_id']}` ({c['constraint_class']}): {c['summary']}"
        for c in runtime_payload["source_derived_runtime_constraints"]
    ) or "- none detected"
    runtime_blockers = "\n".join(f"- {b}" for b in runtime_payload["instruction_materialization_blockers"]) or "- none"
    (out / "docs" / "design-package-conformance-contract.md").write_text(f"""# Design/Package Conformance Contract

- team_id: `{team_id}`
- team_kind: `{team_kind}`
- source_skill: `{source_skill or 'unknown'}`
- target_runtime: `{target.replace('_', '-')}`
- entry_agent_id: `{entry}`
- route: `{route}`
- delivery: `{delivery}`
- conformance_status: `{conformance['conformance_status']}`
- reexecution_required: `{str(conformance['reexecution_required']).lower()}`
- reexecute_from: `{conformance['reexecute_from'] or 'none'}`

This contract checks whether source-derived workflow requirements survived the design and package boundary. It is source-agnostic: requirements come from the source workflow, extracted constraints, human waits, gates, checkpoints, deliverables, schemas, route restrictions, local resources, and review policies.

## Source-Derived Runtime Constraints

{constraint_rows}

## Blockers

{blockers}

If blockers are present, rerun the earliest responsible Skill2Team phase named in `reexecute_from`. Do not fix conformance by editing only generated downstream text.
""", encoding="utf-8")
    (out / "docs" / "runtime-instruction-conformance.md").write_text(f"""# Runtime Instruction Conformance

- team_id: `{team_id}`
- target_runtime: `{target.replace('_', '-')}`
- entry_agent_id: `{entry}`
- instruction_materialization_status: `{runtime_payload['instruction_materialization_status']}`
- reexecution_required: `{str(runtime_payload['reexecution_required']).lower()}`

Every generated runtime agent instruction must carry the design/package conformance guard and every applicable source-derived runtime constraint id. The JSON file records per-agent missing ids.

## Runtime Instruction Blockers

{runtime_blockers}
""", encoding="utf-8")


def write_meta_team_audit_contract(
    out: Path,
    plan: dict[str, Any],
    *,
    team_id: str,
    team_kind: str,
    source_skill: str | None,
    target: str,
    entry: str,
    execution_path: str,
    current_run_fanout_status: str | None,
) -> None:
    ensure(out / "docs")
    payload = meta_team_audit_payload(
        plan,
        team_id=team_id,
        team_kind=team_kind,
        source_skill=source_skill,
        target=target,
        entry=entry,
        execution_path=execution_path,
        current_run_fanout_status=current_run_fanout_status,
    )
    write_json(out / "meta-team-audit.contract.json", payload)
    subject_lines = "\n".join(f"- {item}" for item in payload["audit_subjects"])
    (out / "docs" / "meta-team-audit-contract.md").write_text(f"""# Meta-Team Independent Audit Contract

- team_id: `{team_id}`
- team_kind: `{team_kind}`
- source_skill: `{source_skill or 'unknown'}`
- target_runtime: `{target.replace('_', '-')}`
- entry_agent_id: `{entry}`
- execution_path: `{execution_path}`
- current_run_fanout_status: `{payload['current_run_fanout_status']}`
- audit_status: `{payload['audit_status']}`
- block_runtime_claim_until_audited: `{str(payload['block_runtime_claim_until_audited']).lower()}`

The Skill2Team meta-team has an independent audit boundary. The reviewer cannot be the producer of the artifact under review. When registered `s2t-meta-*` agents are not hot-loaded, a real current-session reviewer subagent may perform the same fixed review work order and must be recorded as such.

## Audit Subjects

{subject_lines}

If this audit blocks design or package release, route back to the producing meta role and rerun from the earliest failed phase. Do not silently patch only generated package text.
""", encoding="utf-8")


def write_post_package_prompt_templates(out: Path, *, team_id: str, team_kind: str, source_skill: str | None, target: str, entry: str, route: str, delivery: str) -> None:
    ensure(out / "docs")
    templates = delivery_next_prompt_templates(
        team_id=team_id,
        team_kind=team_kind,
        source_skill=source_skill,
        target=target,
        entry=entry,
        route=route,
        delivery=delivery,
    )
    design_templates = {
        key: value
        for key, value in templates.items()
        if key == "design_to_package_prompt" or key.startswith("design_continuation_") or key == "api_runner_role_simulation_prompt"
    }
    write_json(out / "design-continuation-prompt-templates.json", design_templates)
    design_md = f"""# Design Continuation Prompt Templates

- team_id: `{team_id}`
- team_kind: `{team_kind}`
- source_skill: `{source_skill or 'unknown'}`
- target_runtime: `{target.replace('_', '-')}`
- entry_agent_id: `{entry}`
- architecture_method: `framework-neutral agent architecture relationship graph with profile-based agents`

These prompts belong immediately after `Delivery: design`. `package` is one concrete continuation example, not the only continuation path. Use the same design output to continue toward Codex registration/package work, API-service runners, Hermes profile mode, OpenClaw profile/global-skill mode, or another multi-agent framework. These are design-result prompts, not package-end next actions.

{format_next_prompt_templates(design_templates)}
"""
    (out / "docs" / "design-continuation-prompt-templates.md").write_text(design_md, encoding="utf-8")

    package_templates = {
        "package_end_codex_register_and_start_openai_codex": templates["package_end_codex_register_and_start_openai_codex"],
        "registered_entry_agent_use_after_codex_smoke_tests": templates["registered_entry_agent_use_after_codex_smoke_tests"],
        "current_session_target_team_fanout_prompt": templates["current_session_target_team_fanout_prompt"],
    }
    write_json(out / "post-package-prompt-templates.json", package_templates)
    md = f"""# Package-End Prompt Templates

- team_id: `{team_id}`
- team_kind: `{team_kind}`
- source_skill: `{source_skill or 'unknown'}`
- target_runtime: `{target.replace('_', '-')}`
- entry_agent_id: `{entry}`
- architecture_method: `framework-neutral agent architecture relationship graph with profile-based agents`

These prompts are emitted at the end of `Delivery: package`. They explain how a recipient should register, smoke-test, and start this converted target-team package in Codex. Non-Codex continuations belong to the design result and are archived in `design-output.zip`; they are not package-end next actions.

{format_next_prompt_templates(package_templates)}
"""
    (out / "docs" / "post-package-prompt-templates.md").write_text(md, encoding="utf-8")


def write_design_output_archive(out: Path, *, team_id: str, team_kind: str, source_skill: str | None, target: str, entry: str, route: str, delivery: str) -> None:
    ensure(out / "docs")
    archive_name = "design-output.zip"
    manifest = {
        "schema_version": "s2t-design-output-archive-v1",
        "managed_by": "skill2team",
        "team_id": team_id,
        "team_kind": team_kind,
        "source_skill": source_skill,
        "target_runtime": target.replace("_", "-"),
        "entry_agent_id": entry,
        "route": route,
        "delivery": delivery,
        "architecture_method": "framework-neutral agent architecture relationship graph with profile-based agents",
        "archive_path": archive_name,
        "purpose": "Package delivery must carry the design result as an inspectable archive. Non-Codex continuations belong to this design result, not to package-end next actions.",
        "included_patterns": [
            "design-intermediate-results.json",
            "docs/design-intermediate-results.md",
            "agent-architecture.map.json",
            "docs/agent-architecture-map.md",
            "workflow-orchestration.map.json",
            "docs/workflow-orchestration-map.md",
            "flow-control.contract.json",
            "docs/flow-control-contract.md",
            "workflow-preservation-gate.json",
            "docs/workflow-preservation-gate.md",
            "entry-agent-startup-welcome.json",
            "docs/entry-agent-startup-welcome.md",
            "design-package-conformance.contract.json",
            "docs/design-package-conformance-contract.md",
            "runtime-instruction-conformance.json",
            "docs/runtime-instruction-conformance.md",
            "meta-team-audit.contract.json",
            "docs/meta-team-audit-contract.md",
            "local-resource-allocation.map.json",
            "source-resource-manifest.json",
            "docs/local-resource-allocation-map.md",
            "agent-profiles.json",
            "profiles/*.agent-profile.json",
            "docs/agent-profiles.md",
            "design-continuation-prompt-templates.json",
            "docs/design-continuation-prompt-templates.md",
        ],
    }
    write_json(out / "design-output-manifest.json", manifest)
    paths: list[Path] = []
    for pattern in manifest["included_patterns"]:
        matches = sorted(out.glob(pattern))
        paths.extend(p for p in matches if p.is_file())
    paths.append(out / "design-output-manifest.json")
    seen: set[str] = set()
    with zipfile.ZipFile(out / archive_name, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in paths:
            if not path.exists() or not path.is_file():
                continue
            rel = path.relative_to(out).as_posix()
            if rel in seen or rel == archive_name:
                continue
            seen.add(rel)
            zf.write(path, rel)
    (out / "docs" / "design-output-archive.md").write_text(f"""# Design Output Archive

- team_id: `{team_id}`
- team_kind: `{team_kind}`
- source_skill: `{source_skill or 'unknown'}`
- target_runtime: `{target.replace('_', '-')}`
- entry_agent_id: `{entry}`
- archive: `design-output.zip`

`Delivery: package` must include the design result. This archive carries the design maps, design intermediate results, conformance contracts, profile definitions, local-resource map, and design-continuation prompts. Package-end next actions remain Codex-only; non-Codex continuations belong inside this design archive.
""", encoding="utf-8")


def write_register_readiness_contract(out: Path, agents: list[dict[str, Any]], *, team_id: str, team_kind: str, source_skill: str | None, target: str, entry: str) -> None:
    ensure(out / "docs")
    policy = register_readiness_policy(
        agents,
        team_id=team_id,
        team_kind=team_kind,
        source_skill=source_skill,
        target=target,
        entry=entry,
    )
    write_json(out / "register-readiness-contract.json", policy)
    agent_lines = "\n".join(
        f"- `{a['agent_id']}` ({'entry' if a['entry'] else 'specialist'}): `{a['artifact_path']}`"
        for a in policy["planned_runtime_agents"]
    )
    blocker_lines = "\n".join(f"- {b}" for b in policy["register_blockers"]) if policy["register_blockers"] else "- none"
    test_lines = "\n".join(
        f"- `{t['id']}`: {t['goal']} Evidence: {t['required_evidence']}."
        for t in policy["post_registration_smoke_tests"]
    )
    context_file_lines = "\n".join(f"- `{item}`" for item in policy["planned_runtime_context_files"])
    md = f"""# Register Readiness Contract

- team_id: `{team_id}`
- team_kind: `{team_kind}`
- source_skill: `{source_skill or 'unknown'}`
- target_runtime: `{target.replace('_', '-')}`
- architecture_method: `framework-neutral agent architecture relationship graph with profile-based agents`
- entry_agent_id: `{entry}`
- package_register_readiness_status: `{policy['package_register_readiness_status']}`
- package_supports_register_hard_runtime_requirements: `{str(policy['package_supports_register_hard_runtime_requirements']).lower()}`
- registration_status_at_package_time: `not_registered`
- entry_agent_runnable_at_package_time: `false`

## Hard Rule

`Delivery: package` is not allowed to be a loose file dump. It must prepare
everything a later Codex environment needs to enforce the hard runtime requirement:
the entry agent and every specialist agent must be installable, invocable,
handoff-capable, and gate-checkable in the selected runtime before the team is
described as runnable.

Generated files are not runtime execution proof. Runtime runnability requires
registration plus smoke-test evidence.

## Planned Runtime Agents

{agent_lines}

## Register-Time Hard Runtime Requirements

{chr(10).join(f"- {item}" for item in policy['register_hard_runtime_requirements'])}

## Required Package Artifacts

{chr(10).join(f"- {item}" for item in policy['required_package_artifacts'])}

## Runtime Context Files

These are not all registered as Codex agent config files, but registered agents must read them before claiming package-faithful execution.

{context_file_lines}

## Post-Registration Smoke Tests

{test_lines}

## Package Blockers

{blocker_lines}

If blockers are present, registration may still install files for inspection,
but Skill2Team must not claim a runnable multi-agent target team until the
runtime blocker is resolved and smoke-test evidence exists.
"""
    (out / "docs" / "register-readiness-contract.md").write_text(md, encoding="utf-8")


def write_runtime_invocation_contract(out: Path, *, team_id: str, team_kind: str, source_skill: str | None, target: str, entry: str, execution_path: str, current_run_fanout_status: str | None = None, route: str = "source-to-team", delivery: str = "package") -> None:
    ensure(out / "docs")
    policy = runtime_invocation_policy(
        team_id=team_id,
        team_kind=team_kind,
        source_skill=source_skill,
        target=target,
        entry=entry,
        execution_path=execution_path,
        current_run_fanout_status=current_run_fanout_status,
        route=route,
        delivery=delivery,
    )
    write_json(out / "runtime-invocation-contract.json", policy)
    source_patterns = policy["source_prompt_rewrite_policy"]["source_invocation_patterns"]
    pattern_lines = "\n".join(f"- `{p}`" for p in source_patterns) if source_patterns else "- none recorded because source_skill is unknown"
    md = f"""# Runtime Invocation Contract

- team_id: `{team_id}`
- team_kind: `{team_kind}`
- source_skill: `{source_skill or 'unknown'}`
- target_runtime: `{target.replace('_', '-')}`
- architecture_method: `framework-neutral agent architecture relationship graph with profile-based agents`
- entry_agent_id: `{entry}`
- target_team_registration_status: `not_registered`
- entry_agent_runnable: `false`
- registered_target_team_smoke_status: `not_registered`
- target_run_fanout_status: `not_started`
- allowed_current_session_target_fanout_status: `real_session_target_subagents`
- generation_run_fanout_status: `{policy['generation_run_fanout_status']}`

## Invocation Rule

This package contains deployable agent artifacts, but package generation is not runtime registration. Do not tell a user to invoke `{entry}` as a registered runtime agent until the selected runtime manifest has `registration_status = registered`, `registered_files` includes the entry agent artifact, and runtime smoke-test evidence confirms the entry agent plus specialist handoffs can actually run.

The package must include `docs/register-readiness-contract.md` and `register-readiness-contract.json` so `post-package Codex registration/use guidance` can enforce the hard runtime requirements instead of merely copying files.

The entry agent must render or summarize `docs/entry-agent-startup-welcome.md` before entering the first real migrated workflow stage. It must collect missing source-required startup inputs and unresolved human-intervention retention choices, defaulting to preservation of source human-interaction steps when the user does not explicitly choose automation.

## Codex Target-Team Execution Guard

Registered target-team execution in Codex requires real registered entry-agent invocation plus real specialist handoffs. If the entry agent cannot dispatch to the named specialist agents through the runtime, it must stop with `target-team execution blocked`, state the missing runtime capability or evidence, and give recovery steps. It must not continue as sequential or single-agent simulation while claiming Codex target-team execution.

If the package has been installed but the current Codex thread cannot hot-load the generated target-agent types, an alternate Codex path is allowed only when the active session can launch real independent subagents for the generated target profiles. That run must record `target_run_fanout_status=real_session_target_subagents`, keep `registered_target_team_smoke_status=pending_hot_reload_or_new_thread`, keep `registered_agent_invocation_verified=false`, and must not claim registered target-team execution.

Before registration, use this generated target package through Skill2Team only as artifact inspection. This is not allowed as a substitute for Codex `meta-team-first` execution or registered target-team execution:

```text
{policy['unregistered_invocation_prompt']}
```

After registration, use:

```text
{policy['registered_invocation_prompt']}
```

When registered target-agent types are unavailable in the active thread but real current-session subagents are available, use:

```text
{policy['current_session_target_fanout_prompt']}
```

## Source Prompt Rewrite

The source skill or workflow may contain self-invocation phrases. They are source-local and must not be copied into target-team prompts unless an explicit source-skill fallback mode is recorded.

Detected source invocation patterns:

{pattern_lines}

Replacement when registered:

```text
{policy['source_prompt_rewrite_policy']['registered_replacement']}
```

Replacement when unregistered:

```text
{policy['source_prompt_rewrite_policy']['unregistered_replacement']}
```

This rule is derived from manifest fields, not from a hard-coded source example.
"""
    (out / "docs" / "runtime-invocation-contract.md").write_text(md, encoding="utf-8")



def write_team_usage_guide(out: Path, agents: list[dict[str, Any]], *, team_id: str, team_kind: str, source_skill: str | None, target: str, prefix: str, entry: str, execution_path: str, current_run_fanout_status: str | None = None, route: str = "source-to-team", delivery: str = "package") -> None:
    ensure(out / "docs")
    fanout_status = normalized_fanout_status(execution_path, current_run_fanout_status)
    next_templates = delivery_next_prompt_templates(
        team_id=team_id,
        team_kind=team_kind,
        source_skill=source_skill,
        target=target,
        entry=entry,
        route=route,
        delivery=delivery,
    )
    package_templates = {
        "package_end_codex_register_and_start_openai_codex": next_templates["package_end_codex_register_and_start_openai_codex"],
        "registered_entry_agent_use_after_codex_smoke_tests": next_templates["registered_entry_agent_use_after_codex_smoke_tests"],
        "current_session_target_team_fanout_prompt": next_templates["current_session_target_team_fanout_prompt"],
    }
    next_template_section = format_next_prompt_templates(package_templates)
    agent_table = generated_agents_markdown(agents)
    unregistered_prompt = (
        f"Inspect this generated target-team package as artifacts only; do not perform the target workflow as Codex execution.\n"
        f"Package path: <GENERATED_TARGET_TEAM_PACKAGE>.\n"
        "Read `AGENTS.md`, `s2t-agent-registry.json`, `design-intermediate-results.json`, `entry-agent-startup-welcome.json`, `design-package-conformance.contract.json`, `runtime-instruction-conformance.json`, `meta-team-audit.contract.json`, `local-resource-allocation.map.json`, `source-resource-manifest.json`, `docs/entry-agent-startup-welcome.md`, `docs/runtime-invocation-contract.md`, `docs/design-package-conformance-contract.md`, `docs/runtime-instruction-conformance.md`, `docs/meta-team-audit-contract.md`, `docs/local-resource-allocation-map.md`, and `docs/team-usage-guide.md`.\n"
        f"Inspect the entry agent `{entry}` and specialist handoff plan, then list registration/smoke-test blockers.\n"
        "To execute the task in Codex, first register the package and pass smoke tests.\n"
        "Do not use this as Codex meta-team-first execution or registered target-team execution."
    )
    codex_guidance_prompt = next_templates["package_end_codex_register_and_start_openai_codex"]
    registered_prompt = next_templates["registered_entry_agent_use_after_codex_smoke_tests"]
    current_session_prompt = next_templates["current_session_target_team_fanout_prompt"]
    text = f"""# Team Usage Guide

- team_kind: `{team_kind}`
- team_id: `{team_id}`
- name_prefix: `{prefix}`
- entry_agent_id: `{entry}`
- target_runtime: `{target.replace('_', '-')}`
- default_model_runner: `OpenAI Codex`
- package_registration_status: `not_registered`
- entry_agent_runnable_now: `false`
- registered_target_team_smoke_status: `not_registered`
- allowed_current_session_target_fanout_status: `real_session_target_subagents`
- route_at_generation: `{route}`
- delivery_at_generation: `{delivery}`
- execution_path_at_generation: `{execution_path}`
- current_run_fanout_status_at_generation: `{fanout_status}`
- runtime_invocation_contract: `docs/runtime-invocation-contract.md`
- register_readiness_contract: `docs/register-readiness-contract.md`
- design_package_conformance_contract: `design-package-conformance.contract.json` and `docs/design-package-conformance-contract.md`
- runtime_instruction_conformance: `runtime-instruction-conformance.json` and `docs/runtime-instruction-conformance.md`
- meta_team_audit_contract: `meta-team-audit.contract.json` and `docs/meta-team-audit-contract.md`
- design_output_archive: `design-output.zip`
- entry_agent_startup_welcome: `entry-agent-startup-welcome.json` and `docs/entry-agent-startup-welcome.md`
- package_end_prompt_templates: `docs/post-package-prompt-templates.md`
- local_resource_allocation_map: `local-resource-allocation.map.json`
- source_resource_manifest: `source-resource-manifest.json`
- agent_profiles: `agent-profiles.json` and `profiles/*.agent-profile.json`
- architecture_method: `framework-neutral agent architecture relationship graph with profile-based agents`

## Model Invocation Policy

Skill2Team, the fixed S2T meta-team agents, and generated target-team agents default to OpenAI Codex runtime/custom-agent invocation. Direct model API calls are not the default. Package-end guidance is Codex-only. Non-Codex continuations are design-result material and are archived in `design-output.zip`.

## Generated Target-Team Agents and Functions

{agent_table}

## Agent Profiles

This package includes `agent-profiles.json`, `profiles/*.agent-profile.json`, and `docs/agent-profiles.md`. Use these profiles as the conceptual agent identities when registering and smoke-testing Codex custom agents.

## Entry Agent Startup Welcome

The entry agent must render or summarize `docs/entry-agent-startup-welcome.md` before the first real migrated workflow stage. It must collect missing source-required inputs and ask whether to preserve the source workflow's human-interaction steps, selectively retain them, or run fully automated with audit. The default is to preserve source human-interaction steps.

## Design/Package Conformance

Before claiming this package is faithful to its source design, inspect `design-package-conformance.contract.json`, `runtime-instruction-conformance.json`, and `meta-team-audit.contract.json`. If any contract reports `reexecution_required=true`, rerun the named Skill2Team phase instead of patching downstream package text.

## Package Status

This package contains Codex custom-agent artifacts, but package generation is not Codex runtime registration.

```text
registration_status = not_registered
entry_agent_runnable = false
registered_files = []
```

Generated files are not runtime execution proof.

## Before Codex Registration

Use this package for artifact-only inspection. The entry agent id is useful as a role name, but it is not runnable until registration and smoke-test evidence exist. Do not perform the target workflow as Codex target-team execution before registration.

```text
{unregistered_prompt}
```

## Package-End Codex Registration and Start Guidance

Use this prompt at the end of package when someone receives the package and needs manifest-scoped Codex registration/start instructions:

```text
{codex_guidance_prompt}
```

## After Real Codex Registration and Smoke Tests

Start from the registered entry agent only after the Codex manifest says `registration_status = registered`, `registered_files` includes the entry agent artifact, and runtime evidence confirms entry invocation plus specialist handoffs. If handoff to specialists cannot actually run, the entry agent must stop with `target-team execution blocked`; it must not continue as sequential or single-agent simulation.

```text
{registered_prompt}
```

## Current-Session Target-Team Fan-out

Use this only when the package has been installed or inspected, the active Codex thread cannot invoke the generated target-agent types, and real independent current-session subagents are available. This is allowed Codex fan-out, but it is not registered target-team execution and must keep registered smoke-test status pending.

```text
{current_session_prompt}
```

## Package-End Codex Prompt Templates

{next_template_section}

## Safety

- Do not claim registered-agent execution before the runtime manifest has been installed and smoke-tested.
- Do not claim Codex target-team execution if the entry agent cannot hand off to registered specialist agents; stop with `target-team execution blocked` instead.
- If registered target-agent types are unavailable in the active thread, use `target_run_fanout_status=real_session_target_subagents` only when real current-session subagents execute the generated specialist roles; otherwise block.
- Do not copy source skill self-invocation prompts into target-team handoff prompts. Rewrite them according to `docs/runtime-invocation-contract.md`.
- Codex registration guidance must be manifest-scoped and must not delete unrelated custom agents.
- Registered agent files do not prove that the current Skill2Team run used real subagents; the run fan-out status is recorded separately.
- If design/package conformance or meta-team audit is blocked, re-execute the earliest responsible Skill2Team phase before runtime use.
- Do not hard-code a particular source package name, task id, or source-local prompt.
"""
    (out / "docs" / "team-usage-guide.md").write_text(text, encoding="utf-8")

def write_fanout_status(out: Path, target: str, support: str, execution_path: str = "direct-skill", current_run_fanout_status: str | None = None) -> None:
    current = normalized_fanout_status(execution_path, current_run_fanout_status)
    fallback = fanout_fallback(current, execution_path)
    text = f"""# Runtime Fan-out Status

- target_runtime: {target}
- execution_path: {execution_path}
- target_subagent_fanout_supported: {support}
- current_run_fanout_status: {current}
- execution_mode: {fanout_execution_mode(current, execution_path)}
- fallback_declaration: {fallback}

Generated agent artifacts do not prove that the current Skill2Team run used real subagents. For Codex `meta-team-first`, use `real_subagents` only after actual registered meta-agent activation and smoke-test evidence. Use `real_session_subagents` only when the running Codex session used real independent subagents for fixed S2T work orders while registered `s2t-meta-*` smoke tests remain pending, such as after a same-thread custom-agent hot-load miss. If neither can be confirmed, block with `blocked_no_real_codex_meta_team`; do not proceed under the `meta-team-first` label.

For generated target-team execution after registration, the entry agent must also verify real specialist handoff. If unavailable, stop with `target-team execution blocked`; do not proceed as sequential or single-agent simulation.
"""
    (out / "runtime-fanout-status.md").write_text(text, encoding="utf-8")

def codex(out: Path, plan: dict[str, Any], agents: list[dict[str, Any]], execution_path: str = "direct-skill", current_run_fanout_status: str | None = None) -> None:
    base = out / ".codex" / "agents"
    ensure(base)
    ensure(out / ".codex")
    config_lines = [
        "# Skill2Team Codex custom-agent package.",
        "[features]",
        "multi_agent = true",
        "enable_fanout = true",
        "",
        "[agents]",
        f"max_threads = {max(1, len(agents))}",
        "max_depth = 1",
        "",
    ]
    for a in agents:
        aid = agent_id(a)
        deny = set((a.get("tools_policy") or {}).get("deny", []))
        sandbox = "read-only" if {"write", "edit", "apply_patch", "exec"} & deny else "workspace-write"
        team_id = str(a.get("s2t_team_id") or "s2t-team")
        entry = str(a.get("s2t_entry_agent") or "")
        is_entry = bool(a.get("entry_agent"))
        runtime_block = agent_runtime_instruction_block(a, plan, agents, entry)
        instr = f"""You are {display(a)}.\n\nMission: {mission(a)}\n\nStay within your role. Do not approve your own primary output unless this agent explicitly owns an acceptance gate. Return concise findings and cite files/artifacts when relevant. Track named inputs and outputs when your work can affect rerun or resume decisions. Follow your generated agent profile, `local-resource-allocation.map.json`, `source-resource-manifest.json`, `design-package-conformance.contract.json`, `runtime-instruction-conformance.json`, `entry-agent-startup-welcome.json`, `docs/entry-agent-startup-welcome.md`, and the framework-neutral agent relationship architecture/workflow maps in the package docs.\n\nCodex target-team execution guard: this generated team should run through registered Codex custom agents with real entry/specialist handoffs when those agent types are available. If registered handoff is unavailable because the active thread did not hot-load the generated target-agent types, current-session target-team fan-out is allowed only when real independent subagents can be launched for the generated target roles and the run records `target_run_fanout_status=real_session_target_subagents`. Do not describe single-agent or sequential role-play as Codex target-team execution. If neither registered handoff nor real current-session target subagents are available, stop with `target-team execution blocked`, explain the missing capability/evidence, and give recovery steps.\n{runtime_block}"""
        if is_entry:
            instr += "\nYou are the user-facing entry agent for this team. Start interactions by rendering or summarizing `docs/entry-agent-startup-welcome.md`, adapted to the user's current task and the generated team roles. Identify the user's route, active state, source material, target runtime, registration status, target_run_fanout_status, required startup inputs, and human-interaction execution mode before entering the first migrated workflow stage. Default to preserving source human-interaction steps; do not auto-advance across user input nodes, human waits, approvals, selections, or terminal boundaries unless the user explicitly selected safe automation and the package records an audit path. Before doing the target task, confirm whether this invocation is registered-agent execution or current-session target-team fan-out. Hand off to specialist agents through shallow, explicit work orders. If registered specialist handoff is unavailable but real current-session subagents can run, delegate to those subagents and record `target_run_fanout_status=real_session_target_subagents`, `registered_target_team_smoke_status=pending_hot_reload_or_new_thread`, and `registered_agent_invocation_verified=false`. If you cannot hand off to required specialists by either path, stop with `target-team execution blocked`; do not perform specialist work yourself while claiming multi-agent target-team execution. Do not approve your own specialist outputs.\n"
        (base / f"{aid}.toml").write_text(
            f"name = \"{aid}\"\n"
            f"description = \"{mission(a).replace(chr(34), chr(39))}\"\n"
            f"# managed_by = \"skill2team\"\n"
            f"# s2t_team_id = \"{team_id}\"\n"
            f"# s2t_entry_agent = \"{entry}\"\n"
            f"# entry_agent = {str(is_entry).lower()}\n"
            f"# agent_profile = \"profiles/{aid}.agent-profile.json\"\n"
            f"# agent_node_id = \"{aid.replace('-', '_')}\"\n"
            f"sandbox_mode = \"{sandbox}\"\n"
            f"developer_instructions = \"\"\"\n{instr}\n\"\"\"\n",
            encoding="utf-8"
        )
        config_lines.extend([f"[agents.{aid}]", f"config_file = \"./agents/{aid}.toml\"", ""])
    (out / ".codex" / "config.toml").write_text("\n".join(config_lines), encoding="utf-8")
    (out / "AGENTS.md").write_text("# Project Agent Guidance\n\nAfter this package is registered and smoke-tested, use the registered entry agent first. Before registration, use Skill2Team with this package only for artifact inspection and follow docs/team-usage-guide.md plus docs/runtime-invocation-contract.md; do not claim registered-agent execution. The entry agent must render or summarize docs/entry-agent-startup-welcome.md before entering the first migrated workflow stage, collect source-required startup inputs, and default to preserving source human-interaction steps unless the user explicitly selects safe automation. Codex target-team execution requires real registered entry/specialist handoffs, or a clearly labeled current-session target-team fan-out run with `target_run_fanout_status=real_session_target_subagents` when registered target-agent types are unavailable in the active thread. If the entry agent cannot hand off to required specialists by either real path, stop with `target-team execution blocked`; do not continue as a sequential or single-agent simulation. Design results live in design-output.zip and design-output-manifest.json; package-end Codex register/start templates live in docs/post-package-prompt-templates.md. Agent profiles live in agent-profiles.json and profiles/*.agent-profile.json. Design/package conformance is governed by design-package-conformance.contract.json, runtime-instruction-conformance.json, workflow-preservation-gate.json, docs/design-package-conformance-contract.md, and docs/runtime-instruction-conformance.md. If a generated agent, profile, or manifest drops a source-derived runtime constraint, stop with `design-package conformance blocked` and re-execute the earliest responsible Skill2Team phase instead of patching only downstream text. Local source resources are governed by local-resource-allocation.map.json, source-resource-manifest.json, and docs/local-resource-allocation-map.md; do not ignore those files when using source templates, scripts, examples, references, or assets. Keep delegation shallow unless explicitly requested. Preserve original workflow steps, user input nodes, stage-internal deliverables, human intervention choices, gates, checkpoints, terminal boundaries, and nontrivial control-flow nodes when migrating to the team. Use workflow-preservation-gate.json, docs/flow-control-contract.md, and docs/artifact-lineage-and-rerun-policy.md for workflow preservation, resume, and rerun decisions. Re-registration must be manifest-driven and must not delete unrelated custom agents.\n", encoding="utf-8")
    write_fanout_status(out, "codex", "runtime-dependent", execution_path, current_run_fanout_status)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", nargs="?", help="team plan JSON with agents list")
    parser.add_argument("output_dir", nargs="?")
    parser.add_argument("--target", choices=["codex"], default="codex", help="Skill2Team 1.9.2 generates and tests Codex runtime packages only.")
    parser.add_argument("--meta-team", action="store_true", help="Generate Skill2Team's built-in meta-team package.")
    parser.add_argument("--team-id", help="Stable team id for registration manifests.")
    parser.add_argument("--team-kind", choices=["meta", "target", "rehydrated"], default="target")
    parser.add_argument("--source-skill", help="Source skill/workflow slug for target-team naming.")
    parser.add_argument("--name-prefix", help="Distinctive registered agent name prefix.")
    parser.add_argument("--entry-agent-id", help="Explicit registered entry agent id.")
    parser.add_argument("--execution-path", choices=["direct-skill", "meta-team-first"], default="direct-skill", help="How Skill2Team ran before generating these artifacts. Defaults to direct-skill.")
    parser.add_argument("--route", choices=["source-to-team", "brief-to-team", "guided-to-team"], default="source-to-team", help="Clean Skill2Team route that produced this package.")
    parser.add_argument("--delivery", choices=["package"], default="package", help="Skill2Team 1.9.2 final delivery for generated runtime artifacts.")
    parser.add_argument("--current-run-fanout-status", choices=["direct-skill-not-requested", "real_subagents", "real_session_subagents", "blocked_no_real_codex_meta_team", "not_needed_for_bare_startup"], help="Actual fan-out status of the Skill2Team run that produced these artifacts.")
    parser.add_argument("--source-root", help="Optional source skill/package root used to bundle local resources into the generated target-team package.")
    parser.add_argument("--resource-copy-mode", choices=["manifest", "bundle"], default="manifest", help="manifest records local resources without copying; bundle copies inventoried source resources from --source-root into source-resources/.")
    args = parser.parse_args()
    if args.execution_path == "meta-team-first" and args.current_run_fanout_status not in {"real_subagents", "real_session_subagents"}:
        raise SystemExit(
            "meta-team-first with target runtime codex requires real_subagents from registered Codex meta-agent activation, "
            "or real_session_subagents from actual current-session Codex subagent work orders when registered custom agents are not hot-loaded. "
            "Sequential or single-agent fallback role-play is not permitted. Stop with a blocker reason or rerun with Execution path: direct-skill."
        )
    if args.output_dir is None:
        if args.meta_team and args.plan:
            args.output_dir = args.plan
            args.plan = None
        else:
            raise SystemExit("output_dir is required")
    plan_path = None if args.meta_team or not args.plan else Path(args.plan)
    plan = load_plan(plan_path, meta_team=args.meta_team)
    source_root = args.source_root or plan.get("source_root") or plan.get("source_package_root")
    team_kind = "meta" if args.meta_team else args.team_kind
    if args.meta_team:
        contract = load_meta_team_contract()
        reject_meta_override("--team-id", args.team_id, contract["team_id"])
        reject_meta_override("--source-skill", args.source_skill, contract["skill_id"])
        reject_meta_override("--name-prefix", args.name_prefix, contract["name_prefix"])
        reject_meta_override("--entry-agent-id", args.entry_agent_id, contract["entry_agent_id"])
        source_skill = contract["skill_id"]
        team_id = contract["team_id"]
        prefix = contract["name_prefix"]
        entry_agent_id = contract["entry_agent_id"]
    else:
        source_skill = args.source_skill or plan.get("source_skill")
        team_id = derive_team_id(plan, args.team_id, source_skill, team_kind)
        prefix = derive_prefix(team_id, args.name_prefix, team_kind, source_skill)
        entry_agent_id = args.entry_agent_id
    agents, entry = prepare_agents(plan, team_id=team_id, team_kind=team_kind, source_skill=source_skill, prefix=prefix, entry_agent_id=entry_agent_id)
    out = Path(args.output_dir)
    ensure(out)
    targets = ["codex"]
    for t in targets:
        dest = out
        if t == "codex":
            codex(dest, plan, agents, args.execution_path, args.current_run_fanout_status)
        else:
            raise SystemExit(f"Unsupported target runtime: {t}. Only codex is generated and tested.")
        write_architecture_workflow_artifacts(dest, plan, agents, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=t, entry=entry, route=args.route, delivery=args.delivery)
        write_flow_control_artifacts(dest, plan, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=t, entry=entry, execution_path=args.execution_path, route=args.route, delivery=args.delivery)
        write_local_resource_allocation_artifacts(dest, plan, agents, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=t, entry=entry, route=args.route, delivery=args.delivery, source_root=source_root, bundle_mode=args.resource_copy_mode)
        write_design_intermediate_results(dest, plan, agents, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=t, prefix=prefix, entry=entry, route=args.route, delivery=args.delivery, execution_path=args.execution_path)
        write_workflow_preservation_gate(dest, plan, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=t, entry=entry, route=args.route, delivery=args.delivery)
        write_entry_agent_startup_welcome(dest, plan, agents, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=t, entry=entry, route=args.route, delivery=args.delivery)
        write_agent_profiles(dest, plan, agents, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=t, entry=entry)
        write_design_package_conformance_artifacts(dest, plan, agents, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=t, entry=entry, route=args.route, delivery=args.delivery)
        write_meta_team_audit_contract(dest, plan, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=t, entry=entry, execution_path=args.execution_path, current_run_fanout_status=args.current_run_fanout_status)
        write_post_package_prompt_templates(dest, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=t, entry=entry, route=args.route, delivery=args.delivery)
        write_design_output_archive(dest, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=t, entry=entry, route=args.route, delivery=args.delivery)
        write_register_readiness_contract(dest, agents, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=t, entry=entry)
        write_runtime_invocation_contract(dest, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=t, entry=entry, execution_path=args.execution_path, current_run_fanout_status=args.current_run_fanout_status, route=args.route, delivery=args.delivery)
        write_team_usage_guide(dest, agents, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=t, prefix=prefix, entry=entry, execution_path=args.execution_path, current_run_fanout_status=args.current_run_fanout_status, route=args.route, delivery=args.delivery)
        write_registry(dest, plan, agents, team_id=team_id, team_kind=team_kind, source_skill=source_skill, target=t, prefix=prefix, entry=entry, execution_path=args.execution_path, current_run_fanout_status=args.current_run_fanout_status, route=args.route, delivery=args.delivery)
    print(f"Generated {args.target} deployment package at {out}")
    print(f"Entry agent: {entry}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
