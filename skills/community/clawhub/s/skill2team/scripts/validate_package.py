#!/usr/bin/env python3
"""Validate Skill2Team package structure, global-skill metadata, and MIT-0 packaging."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

REQUIRED = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "license.txt",
    ".clawhubignore",
    "references/startup-page.md",
    "references/startup-routing.md",
    "references/meta-team-execution.md",
    "references/guided-intake.md",
    "references/decomposition-lenses.md",
    "references/skill-use-taxonomy.md",
    "references/restructuring-method.md",
    "references/workflow-aligned-orchestration.md",
    "references/flow-control-and-resume.md",
    "references/design-package-conformance-and-reexecution.md",
    "references/multi-agent-architecture-best-practices.md",
    "references/local-resource-allocation.md",
    "references/agent-architecture-and-workflow-method.md",
    "references/agent-independence-model.md",
    "references/agent-registration-and-entrypoints.md",
    "references/team-usage-guide.md",
    "references/runtime-invocation-and-prompt-rewrite.md",
    "references/package-to-register-readiness.md",
    "references/target-team-execution-guard.md",
    "references/platform-adapters.md",
    "references/orchestration-design.md",
    "references/baseline-vs-team-evaluation.md",
    "references/continuous-improvement-loop.md",
    "references/scoring-and-decision-rules.md",
    "references/output-contracts.md",
    "references/migration-playbook.md",
    "references/risk-governance.md",
    "references/mit0-openclaw-clawhub-compliance.md",
    "references/clawhub-publish-checklist.md",
    "references/clawhub-submission-info.md",
    "references/global-skill-discovery.md",
    "references/context-loading-policy.md",
    "references/skill-creator-packaging.md",
    "references/design-workflow.md",
    "references/package-workflow.md",
    "assets/runtime-templates/codex-custom-agent/agent-toml-template.md",
    "assets/runtime-templates/generic-agent-spec/AGENT-SPEC-json-template.md",
    "assets/prompt-templates/design-continuation.md",
    "assets/prompt-templates/package-end-codex-register-start.md",
    "assets/prompt-templates/api-service-runner.md",
    "assets/prompt-templates/target-team-execution-guard.md",
    "agents/s2t-meta-agent-profiles.json",
    "prompts/startup-page-prompt.md",
    "prompts/startup-team-prompt.md",
    "prompts/interview-flow.md",
    "prompts/asset-inventory-prompt.md",
    "prompts/workflow-extraction-prompt.md",
    "prompts/brief-to-team-prompt.md",
    "prompts/final-report-template.md",
    "data/question_bank.json",
    "data/skill_taxonomy.json",
    "data/decomposition_lenses.json",
    "data/agent_archetypes.json",
    "data/orchestration_patterns.json",
    "data/architecture_patterns.json",
    "data/evaluation_metrics.json",
    "data/platform_adapters.json",
    "data/global_skill_manifest.json",
    "data/meta_team_contract.json",
    "scripts/score_questionnaire.py",
    "scripts/generate_restructure_plan.py",
    "scripts/brief_to_team.py",
    "scripts/generate_deployment_package.py",
    "scripts/ensure_codex_meta_team.py",
    "scripts/register_codex_agents.py",
    "scripts/compare_runs.py",
    "examples/sample_answers.json",
    "examples/sample_run_comparison.json",
    "examples/sample_team_plan.json",
    "examples/sample_skill_description.txt",
]

TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".jsonl", ".py", ".yaml", ".yml", ".toml", ".svg",
    ".gitignore", ".clawhubignore",
}
TEXT_NAMES = {"LICENSE", "SKILL.md", "README.md", ".clawhubignore", ".gitignore"}
ARCHIVE_EXTENSIONS = {".zip", ".tar", ".gz", ".tgz", ".bz2", ".7z", ".rar"}
BINARY_MEDIA_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".mp4", ".mov", ".mp3", ".wav", ".wasm", ".bin", ".sqlite", ".db"}
MAX_BUNDLE_BYTES = 50 * 1024 * 1024
SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",
    r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |)PRIVATE KEY-----",
    r"sk-[A-Za-z0-9_-]{20,}",
    r"ghp_[A-Za-z0-9]{20,}",
]

MIT0_REQUIRED_SNIPPETS = [
    "MIT No Attribution",
    "Permission is hereby granted, free of charge",
    "without restriction",
    "THE SOFTWARE IS PROVIDED \"AS IS\"",
]


def parse_frontmatter(skill_md: str) -> dict[str, str]:
    if not skill_md.startswith("---\n"):
        return {}
    end = skill_md.find("\n---", 4)
    if end == -1:
        return {}
    block = skill_md[4:end]
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.startswith(" ") or line.startswith("\t"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def validate(root: Path) -> int:
    errors: list[str] = []
    root = root.resolve()

    for rel in REQUIRED:
        if not (root / rel).exists():
            errors.append(f"Missing required file: {rel}")

    # ClawHub/global-skill package shape checks.
    skill_path = root / "SKILL.md"
    if skill_path.exists():
        text = skill_path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        name = fm.get("name", "")
        desc = fm.get("description", "")
        frontmatter_text = text.split("---", 2)[1] if text.startswith("---") else ""
        version = fm.get("version", "")
        if not version:
            match = re.search(r"(?m)^\s+version:\s*([0-9A-Za-z.+-]+)\s*$", frontmatter_text)
            version = match.group(1) if match else ""
        if not name:
            errors.append("SKILL.md frontmatter must include name")
        if not desc:
            errors.append("SKILL.md frontmatter must include description")
        if not version:
            errors.append("SKILL.md frontmatter should include semver version for ClawHub publishing")
        if name and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append(f"Skill name must be lowercase npm-safe slug with hyphens only: {name}")
        if name and root.name != name:
            errors.append(f"Folder name should match frontmatter name: folder={root.name}, name={name}")
        if desc and ("\n" in desc or len(desc) > 160):
            errors.append("Description should be one line and <= 160 characters")
        if version and not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
            errors.append(f"Version should be semver-like: {version}")
        required_nested = [
            "display_name: Skill2Team",
            "version: 1.9.2",
            "user_invocable: true",
            "visibility: global",
            "global_skill: true",
            "scope: global",
            "discoverable: true",
            "global_skill: true",
            "registry_name: skill2team",
        ]
        for needle in required_nested:
            if needle not in frontmatter_text:
                errors.append(f"SKILL.md frontmatter missing global discovery metadata: {needle}")
        if 'emoji: "S2T"' in frontmatter_text or "emoji: 'S2T'" in frontmatter_text:
            errors.append("metadata.openclaw.emoji should be a real emoji, not the text label S2T")
        if len(text.splitlines()) > 180:
            errors.append("SKILL.md should stay lean for Skill Creator style packaging; move long guidance to references/")
        if "references/context-loading-policy.md" not in text or "assets/prompt-templates/" not in text:
            errors.append("SKILL.md should declare on-demand context loading and asset prompt templates")
        for needle in [
            "Every `design` reply must end with paste-ready follow-up prompts",
            "Every `package` reply must end only with Codex package-use prompts",
            "local resource allocation map",
            "source-resource manifest",
            "source_derived_runtime_constraints",
            "design-package-conformance.contract.json",
            "runtime-instruction-conformance.json",
            "meta-team-audit.contract.json",
            "design-output.zip",
            "entry-agent-startup-welcome.json",
            "preserve_source_human_interaction_steps",
            "framework-neutral agent architecture relationship graph",
        ]:
            if needle not in text:
                errors.append(f"SKILL.md missing 1.9.2 output/follow-up requirement: {needle}")
        forbidden_meta = ["license:", "pricing:", "price:", "paywall:", "revenue"]
        for bad in forbidden_meta:
            if bad in frontmatter_text.lower():
                errors.append(f"Do not include unsupported/conflicting ClawHub metadata in SKILL.md: {bad}")

    # MIT-0 license checks.
    license_path = root / "LICENSE"
    if license_path.exists():
        license_text = license_path.read_text(encoding="utf-8")
        for snippet in MIT0_REQUIRED_SNIPPETS:
            if snippet not in license_text:
                errors.append(f"LICENSE does not look like MIT-0; missing snippet: {snippet}")
    if (root / "license.txt").exists():
        lt = (root / "license.txt").read_text(encoding="utf-8")
        if "MIT-0" not in lt:
            errors.append("license.txt should state MIT-0")

    # JSON validation.
    for jf in list((root / "data").glob("*.json")) + list((root / "examples").glob("*.json")):
        try:
            json.loads(jf.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"Invalid JSON in {jf.relative_to(root)}: {exc}")

    # Global discovery manifest checks.
    global_manifest = root / "data" / "global_skill_manifest.json"
    if global_manifest.exists():
        try:
            gm = json.loads(global_manifest.read_text(encoding="utf-8"))
            if gm.get("skill_id") != "skill2team":
                errors.append("global_skill_manifest.json skill_id must be skill2team")
            if gm.get("registry_scope") != "global":
                errors.append("global_skill_manifest.json registry_scope must be global")
            if gm.get("entry_file") != "SKILL.md":
                errors.append("global_skill_manifest.json entry_file must be SKILL.md")
            if gm.get("user_invocable") is not True:
                errors.append("global_skill_manifest.json user_invocable must be true")
            if gm.get("discoverable") is not True:
                errors.append("global_skill_manifest.json discoverable must be true")
            aliases = set(gm.get("aliases", []))
            for alias in {"skill2team", "Skill2Team", "s2t"}:
                if alias not in aliases:
                    errors.append(f"global_skill_manifest.json aliases should include {alias}")
            if gm.get("delivery_modes") != ["design", "package"]:
                errors.append("global_skill_manifest.json delivery_modes must be exactly ['design', 'package']")
            style = gm.get("package_style") or {}
            if style.get("license") != "MIT-0" or style.get("skill_creator_layout") is not True or style.get("on_demand_context") is not True:
                errors.append("global_skill_manifest.json package_style must record Skill Creator layout, on-demand context, and MIT-0")
            keywords = set(gm.get("keywords", []))
            for kw in {"framework-neutral architecture", "profile-based agents", "internal quality gates", "Skill Creator", "MIT-0", "on-demand context"}:
                if kw not in keywords:
                    errors.append(f"global_skill_manifest.json keywords should include {kw}")
        except Exception as exc:
            errors.append(f"Could not validate global_skill_manifest.json: {exc}")

    meta_contract = root / "data" / "meta_team_contract.json"
    if meta_contract.exists():
        try:
            mt = json.loads(meta_contract.read_text(encoding="utf-8"))
            allowed = (mt.get("delivery_policy") or {}).get("allowed_delivery_modes")
            if allowed != ["design", "package"]:
                errors.append("meta_team_contract.json allowed_delivery_modes must be exactly ['design', 'package']")
            if not (mt.get("agent_profile_policy") or {}).get("profile_mode_default"):
                errors.append("meta_team_contract.json must set agent_profile_policy.profile_mode_default=true")
            arch_text = json.dumps(mt.get("architecture_default", {}), ensure_ascii=False)
            if "framework-neutral" not in arch_text or "relationship" not in arch_text:
                errors.append("meta_team_contract.json architecture_default must record framework-neutral agent relationship architecture")
        except Exception as exc:
            errors.append(f"Could not validate meta_team_contract.json: {exc}")

    for rel_name in ["README.md", "SKILL.md", "prompts/startup-team-prompt.md", "references/startup-page.md"]:
        path = root / rel_name
        if path.exists():
            txt = path.read_text(encoding="utf-8")
            for forbidden in ["design -> " + "validate -> package", "Delivery modes: `design`, `" + "`validate`, `package`", "| `validate` | Check coherence"]:
                if forbidden in txt:
                    errors.append(f"{rel_name} still exposes validate as a delivery: {forbidden}")


    # Codex meta-team-first hard rule: no fallback role-play or legacy fan-out-unavailable path.
    hard_rule_files = [
        "SKILL.md",
        "references/meta-team-execution.md",
        "references/startup-page.md",
        "prompts/startup-team-prompt.md",
        "scripts/ensure_codex_meta_team.py",
        "scripts/generate_deployment_package.py",
    ]
    for rel_name in hard_rule_files:
        path = root / rel_name
        if path.exists():
            txt = path.read_text(encoding="utf-8")
            if "meta-team-first blocked" not in txt and "blocked_no_real_codex_meta_team" not in txt:
                errors.append(f"{rel_name} must include the Codex meta-team-first blocker rule")
    forbidden_meta_first_fallbacks = [
        "runtime fan-out " + "unavailable",
        "single_agent" + "_simulation",
        "simulate roles " + "sequentially",
        "simulate the fixed " + "S2T meta-team",
        "simulated " + "meta-team run",
    ]
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        try:
            txt = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for bad in forbidden_meta_first_fallbacks:
            if bad in txt:
                errors.append(f"Legacy Codex meta-team-first fallback phrase found in {p.relative_to(root)}: {bad}")


    # Generated target-team Codex execution must not silently degrade into simulation.
    target_guard_files = [
        "SKILL.md",
        "references/target-team-execution-guard.md",
        "references/runtime-invocation-and-prompt-rewrite.md",
        "references/package-to-register-readiness.md",
        "scripts/generate_deployment_package.py",
        "scripts/register_codex_agents.py",
    ]
    for rel_name in target_guard_files:
        path = root / rel_name
        if path.exists():
            txt = path.read_text(encoding="utf-8")
            if "target-team execution blocked" not in txt:
                errors.append(f"{rel_name} must include the generated target-team execution blocker rule")
    generated_script = root / "scripts" / "generate_deployment_package.py"
    if generated_script.exists():
        txt = generated_script.read_text(encoding="utf-8")
        for needle in [
            "codex_target_team_execution_requires_real_registered_agents",
            "codex_target_team_execution_allows_real_session_subagents_when_registered_agents_unavailable",
            "real_session_target_subagents",
            "forbid_single_agent_or_sequential_simulation",
        ]:
            if needle not in txt:
                errors.append(f"generate_deployment_package.py missing target-team no-simulation guard field: {needle}")

    # Workflow preservation hard rule: generated target teams must not collapse source workflow into a summary.
    preservation_files = [
        "SKILL.md",
        "references/design-workflow.md",
        "references/workflow-aligned-orchestration.md",
        "references/orchestration-design.md",
        "references/flow-control-and-resume.md",
        "references/output-contracts.md",
        "references/package-workflow.md",
        "prompts/workflow-extraction-prompt.md",
        "scripts/generate_deployment_package.py",
    ]
    for rel_name in preservation_files:
        path = root / rel_name
        if path.exists():
            txt = path.read_text(encoding="utf-8").lower()
            for alternatives in [
                ["stage-internal deliverables", "stage-internal deliverable"],
                ["user_input_nodes", "required user input"],
                ["human intervention"],
                ["workflow preservation", "workflow-preservation"],
            ]:
                if not any(needle in txt for needle in alternatives):
                    errors.append(f"{rel_name} missing workflow-preservation rule text: {' or '.join(alternatives)}")
    if generated_script.exists():
        txt = generated_script.read_text(encoding="utf-8")
        for needle in [
            "workflow_preservation_payload",
            "source_flow_control_payload",
            "derived_skill_allocation_matrix",
            "derived_handoff_contracts",
            "derived_gate_and_review_model",
            "workflow-preservation-gate.json",
            "stage_internal_deliverables",
            "user_input_nodes",
            "human_intervention_points",
            "preserve_source_human_interaction_steps",
            "preserve_all_source_mandated_human_waits_and_choices",
        ]:
            if needle not in txt:
                errors.append(f"generate_deployment_package.py missing workflow-preservation implementation field: {needle}")

    # 1.9.2 design/package conformance and independent audit hardening.
    conformance_files = [
        "SKILL.md",
        "references/design-package-conformance-and-reexecution.md",
        "references/design-workflow.md",
        "references/workflow-aligned-orchestration.md",
        "references/flow-control-and-resume.md",
        "references/output-contracts.md",
        "references/package-workflow.md",
        "references/meta-team-execution.md",
        "scripts/generate_deployment_package.py",
    ]
    for rel_name in conformance_files:
        path = root / rel_name
        if path.exists():
            txt = path.read_text(encoding="utf-8")
            for needle in [
                "source_derived_runtime_constraints",
                "design-package-conformance.contract.json",
                "runtime-instruction-conformance.json",
                "reexecution_required",
                "reexecute_from",
            ]:
                if needle not in txt:
                    errors.append(f"{rel_name} missing 1.9.2 conformance rule/artifact: {needle}")
    if generated_script.exists():
        txt = generated_script.read_text(encoding="utf-8")
        for needle in [
            "source_derived_runtime_constraints",
            "agent_runtime_instruction_block",
            "runtime_instruction_conformance_payload",
            "design_package_conformance_payload",
            "write_design_package_conformance_artifacts",
            "write_meta_team_audit_contract",
            "meta_team_audit_payload",
            "design-package-conformance.contract.json",
            "runtime-instruction-conformance.json",
            "meta-team-audit.contract.json",
            "design-output.zip",
            "write_design_output_archive",
            "entry-agent-startup-welcome.json",
            "write_entry_agent_startup_welcome",
            "Design/package conformance guard:",
            "reexecution_required",
            "reexecute_from",
        ]:
            if needle not in txt:
                errors.append(f"generate_deployment_package.py missing 1.9.2 conformance implementation field: {needle}")
    meta_contract = root / "data/meta_team_contract.json"
    if meta_contract.exists():
        txt = meta_contract.read_text(encoding="utf-8")
        for needle in [
            "independent_meta_team_audit_policy",
            "s2t-meta-evaluation-reviewer",
            "design-package-conformance.contract.json",
            "runtime-instruction-conformance.json",
            "meta-team-audit.contract.json",
            "reexecution_required",
        ]:
            if needle not in txt:
                errors.append(f"data/meta_team_contract.json missing 1.9.2 independent audit contract: {needle}")

    # 1.9.2 local-resource and follow-up prompt hardening.
    local_resource_files = [
        "SKILL.md",
        "references/output-contracts.md",
        "references/package-workflow.md",
        "references/local-resource-allocation.md",
        "prompts/final-report-template.md",
        "prompts/startup-team-prompt.md",
        "scripts/generate_deployment_package.py",
    ]
    for rel_name in local_resource_files:
        path = root / rel_name
        if path.exists():
            txt = path.read_text(encoding="utf-8")
            for needle in [
                "local-resource-allocation.map.json",
                "source-resource-manifest.json",
            ]:
                if needle not in txt:
                    errors.append(f"{rel_name} missing 1.9.2 local-resource package artifact: {needle}")
    followup_files = [
        "SKILL.md",
        "references/output-contracts.md",
        "prompts/final-report-template.md",
        "prompts/startup-team-prompt.md",
    ]
    for rel_name in followup_files:
        path = root / rel_name
        if path.exists():
            txt = path.read_text(encoding="utf-8").lower()
            for needle in [
                "every",
                "design",
                "package",
                "follow-up prompts",
                "further analysis",
            ]:
                if needle not in txt:
                    errors.append(f"{rel_name} missing final follow-up prompt requirement term: {needle}")
    if generated_script.exists():
        txt = generated_script.read_text(encoding="utf-8")
        for needle in [
            "source_inventory_payload",
            "source_assets",
            "local_resource_allocation_payload",
            "copy_source_resources",
            "--source-root",
            "--resource-copy-mode",
            "write_local_resource_allocation_artifacts",
        ]:
            if needle not in txt:
                errors.append(f"generate_deployment_package.py missing 1.9.2 local-resource implementation field: {needle}")

    # Clean build must not carry stale release strings.
    for p in root.rglob("*"):
        if p.is_file():
            try:
                txt = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            stale_versions = [
                "1" + "." + "3" + "." + "0",
                "1" + "." + "4" + "." + "0",
                "1" + "." + "4" + "." + "1",
                "1" + "." + "6" + "." + "0",
                "1" + "." + "7" + "." + "0",
                "1" + "." + "8" + "." + "0",
                "1" + "." + "9" + "." + "0",
                "1" + "." + "9" + "." + "1",
            ]
            for stale in stale_versions:
                if stale in txt:
                    errors.append(f"Stale version string {stale} found in {p.relative_to(root)}")
            forbidden_arch_defaults = [
                "api-" + "lang" + "graph-runner.md",
                "design_continuation_codex_" + "lang" + "graph_api_service",
                "Codex/API+" + "Lang" + "Graph",
                "Lang" + "Graph " + "construction",
                "Lang" + "Graph " + "project root",
                "Lang" + "Graph " + "runner",
            ]
            for bad in forbidden_arch_defaults:
                if bad in txt:
                    errors.append(f"Framework-specific default artifact/text found in {p.relative_to(root)}: {bad}")

    # Text-only, no archives/caches/generated artifacts.
    total = 0
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if p.is_dir():
            if p.name in {"__pycache__", ".clawhub", ".clawdhub", ".cache", "dist", "build", "out", "outputs"}:
                errors.append(f"Unexpected generated/local directory in package: {rel}")
            if rel.parts == ("templates",) or (len(rel.parts) > 1 and rel.parts[0] == "templates"):
                errors.append("Use assets/ for templates in the clean Skill Creator layout; top-level templates/ is not allowed")
            continue
        total += p.stat().st_size
        if p.suffix in ARCHIVE_EXTENSIONS:
            errors.append(f"Archive files should not be bundled inside ClawHub skill package: {rel}")
        if p.suffix.lower() in BINARY_MEDIA_EXTENSIONS:
            errors.append(f"Binary/media artifacts should not be bundled in this text-only skill: {rel}")
        if p.is_symlink():
            errors.append(f"Symlinks should not be bundled: {rel}")
        if p.name.endswith((".pyc", ".pyo")):
            errors.append(f"Unexpected Python cache artifact: {rel}")
        if p.name not in TEXT_NAMES and p.suffix not in TEXT_EXTENSIONS:
            errors.append(f"File may not be accepted as text-based ClawHub content: {rel}")
        try:
            txt = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"Non-UTF-8 or binary file detected: {rel}")
            continue
        for pattern in SECRET_PATTERNS:
            if re.search(pattern, txt):
                errors.append(f"Possible secret or private key pattern detected in {rel}")
    if total > MAX_BUNDLE_BYTES:
        errors.append(f"Bundle size exceeds 50MB ClawHub limit: {total} bytes")

    if errors:
        print("Skill2Team package validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print(f"Skill2Team package validation passed: {root}")
    print(f"Bundle size: {total} bytes")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    raise SystemExit(validate(Path(args.root)))
