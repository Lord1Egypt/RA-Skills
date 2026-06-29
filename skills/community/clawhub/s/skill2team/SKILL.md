---
name: skill2team
description: "Design profile-based agent teams from skills, workflows, prompts, tools, or briefs."
metadata:
  display_name: Skill2Team
  version: 1.9.2
  user_invocable: true
  visibility: global
  global_skill: true
  discoverable: true
  openclaw:
    emoji: "🧩"
    scope: global
    discoverable: true
    global_skill: true
    registry_name: skill2team
  search:
    aliases:
      - skill2team
      - Skill2Team
      - s2t
      - skill to team
      - skills to agents
      - agent team designer
    keywords:
      - agent team
      - skill conversion
      - codex agent package
      - openai codex
      - multi-agent architecture
      - profile agents
      - clawhub
      - skill creator
      - mit-0
      - on-demand context
---

# Skill2Team

Use Skill2Team to convert source material into a compact, accountable, profile-based agent team design and, when requested, a concrete Codex package.

Source material can be a skill zip/folder, `SKILL.md`, existing agents, generated team package, prompts, tools, scripts, docs, SOPs, manual workflows, or a natural-language brief.

## Startup reminder

At startup, tell the user:

> Skill2Team 1.9.2 defaults model execution to **OpenAI Codex**. Running Skill2Team, running the fixed `s2t-meta-*` agents, and running generated target-team agents should use Codex custom-agent/runtime invocation, not direct model API calls.

If the user explicitly chooses API model service, label it as **API-service follow-up** or **API-run role simulation**. Do not describe API runs as Codex custom-agent execution.

## Context loading policy

Keep the entry skill lean. Load supporting files only when needed.

| Need | Load on demand |
|---|---|
| Bare startup | `references/startup-page.md`, `references/startup-routing.md` |
| Design | `references/design-workflow.md`, `references/multi-agent-architecture-best-practices.md`, `references/workflow-aligned-orchestration.md`, `references/agent-architecture-and-workflow-method.md`, `references/orchestration-design.md`, `references/flow-control-and-resume.md`, `references/design-package-conformance-and-reexecution.md`, `references/output-contracts.md`, `references/local-resource-allocation.md` |
| Package | `references/package-workflow.md`, `references/package-to-register-readiness.md`, `references/agent-registration-and-entrypoints.md`, `references/runtime-invocation-and-prompt-rewrite.md`, `references/target-team-execution-guard.md`, `references/team-usage-guide.md`, `references/design-package-conformance-and-reexecution.md`, `references/local-resource-allocation.md`, `assets/prompt-templates/` |
| Meta-team-first | `data/meta_team_contract.json`, `references/meta-team-execution.md`, `references/design-package-conformance-and-reexecution.md` |
| ClawHub / Skill Creator / MIT-0 | `references/skill-creator-packaging.md`, `references/mit0-openclaw-clawhub-compliance.md`, `references/clawhub-publish-checklist.md` |
| Deterministic helpers | only the specific script in `scripts/` needed for the requested operation |

For the detailed policy, read `references/context-loading-policy.md` only when context-loading or packaging compliance is in scope.

Do not preload all references. Do not copy long reference text into the answer unless the user asks for it.

## Routes

| Route | Use when |
|---|---|
| `source-to-team` | Convert or restructure existing source material into a cleaner target team. Old-team-to-new-team restructuring belongs here. |
| `brief-to-team` | Turn a natural-language brief, rough prompt, or SOP summary into a first team design. |
| `guided-to-team` | Ask focused questions before design/package when the source or risks are unclear. |

## Delivery modes

Skill2Team exposes only:

```text
design -> package
```

| Delivery | Meaning |
|---|---|
| `design` | Inventory, diagnosis, Agent Architecture Map, Workflow Orchestration Map, Control-Flow & Resume Contract, profile-based agent roster, skill allocation, gates, migration plan, design quality gate, and design-continuation prompts. |
| `package` | A concrete Codex artifact continuation after design. Generate target-agent TOML, profiles, manifests, usage guide, design intermediate results, `design-output.zip`, entry-agent startup welcome page, package release gate, and package-end Codex register/start/use prompts. |

`package` is a built-in concrete continuation after `design` for Codex artifact delivery. Design-continuation prompts may target Codex, API runners, Hermes, OpenClaw, or other frameworks, but package-end prompts must only explain how to use the converted target team in Codex.

`validate` is not a user-facing delivery. Validation logic is split into the `design` quality gate and the `package` release gate. `scripts/validate_package.py` is a local QA helper only.

## Design rules

- Keep **Agent Architecture Map** separate from **Workflow Orchestration Map**.
- Use a **framework-neutral agent architecture relationship graph** by default: profile agents are nodes; delegation, handoffs, routing, state/artifact flow, guardrails, human waits, fan-out/fan-in, review gates, checkpoints, and terminal boundaries are typed edges. Do not describe the default design as tied to any one runtime framework.
- Preserve source workflow control as an explicit migration object. A target team is incomplete if the workflow map only summarizes stages and omits concrete nodes, edges, stage mappings, stage-internal deliverables, required user input nodes, human intervention points, gates, checkpoints, resume rules, or terminal boundaries.
- Stage-internal duties are not optional. If a source stage generates named artifacts, candidate sets, prompt packages, registries, matrices, checkpoints, or closing handoff prompts before the next public step, the target workflow must preserve those deliverables or record a deliberate, reviewed rewrite.
- At the start of source conversion, ask whether to preserve the source workflow's original human-interaction steps, preserve only selected steps, or run fully automated with audit. The default is `preserve_source_human_interaction_steps`.
- Before finalizing a generated target team, inventory human intervention points and ask the user which ones to preserve, convert to reviewer gates, auto-advance with audit, or remove as redundant. If the user does not explicitly choose automation, preserve all source-mandated user input nodes, human waits, approvals, no-auto-continue boundaries, and terminal boundaries.
- Before entering the migrated workflow's first real stage, collect source-required startup settings, user choices, runtime settings, route/delivery constraints, and unresolved human-intervention retention choices. If a required setting is absent and the source does not name a safe default, ask the user or block.
- For `package`, generate an entry-agent startup welcome page (`entry-agent-startup-welcome.json` and `docs/entry-agent-startup-welcome.md`) adapted from the source skill's startup behavior into target-team entry-agent language. The entry agent must render or summarize it before the first real migrated workflow stage.
- Extract `source_derived_runtime_constraints` from the source workflow and materialize them in design maps, package contracts, agent profiles, generated runtime instructions, usage guidance, and manifests.
- Verify design/package conformance before package handoff. If a generated team does not conform to the design or package contract, set `reexecution_required=true`, name `reexecute_from`, and rerun the earliest responsible Skill2Team phase instead of patching downstream package text.
- Prefer **5-6 top-level agents** for nontrivial target teams. Fewer or more requires a strong rationale.
- Do not turn every workflow step, prompt, tool, or skill into an agent.
- Include an entry agent, clear accountability boundaries, independent review where quality risk exists, and explicit state/artifact ownership.
- Stay source-agnostic. Do not hard-code identifiers, prompts, agent ids, package names, or rewrite rules from one specific source.

## Fixed S2T meta-team

The internal Skill2Team service team is fixed by `data/meta_team_contract.json` and uses the same profile/framework-neutral convention as target-team packages.

| Registered agent id | Role |
|---|---|
| `s2t-meta-entry` | Intake, routing, delivery selection, state tracking, synthesis |
| `s2t-meta-source-mapper` | Source inventory and original workflow extraction |
| `s2t-meta-architecture-designer` | Agent Architecture Map and role boundaries |
| `s2t-meta-workflow-orchestrator` | Workflow Orchestration Map, handoffs, checkpoint/resume |
| `s2t-meta-runtime-adapter` | Codex package/profile artifacts and prompt templates |
| `s2t-meta-evaluation-reviewer` | Independent design/package conformance, runtime-instruction, and package-quality audit |

When `Execution path: meta-team-first` is requested with `Target runtime: codex`, first generate/reuse/register the fixed six-agent `s2t-meta` Codex meta-team. Then check the active Codex session separately: newly written `.codex/config.toml` entries may require a new thread or workspace reload before `spawn_agent` can invoke those custom agent types. If registered `s2t-meta-*` activation is unavailable but the active session can still spawn real independent Codex subagents, you may continue only as `current_run_fanout_status=real_session_subagents`, record that registered `s2t-meta-*` smoke tests remain pending, and route fixed-role work orders through real subagents. Fallback role-play is not allowed in Codex `meta-team-first`. If neither registered activation nor real session subagents can be confirmed, stop with `meta-team-first blocked`, explain the concrete reason, and give recovery steps; do not continue under the `meta-team-first` label.

Generated meta-team packages and meta-team-first target packages require independent audit by `s2t-meta-evaluation-reviewer` or an equivalent real independent reviewer subagent. The reviewer must inspect source extraction, design/package conformance, runtime instruction materialization, local-resource allocation, human-intervention choices, and package integrity. If the audit blocks, rerun the producing meta role from the earliest failed phase before package handoff.

## Required outputs

For `design`, include the design result plus continuation prompts for package, Codex/OpenAI, framework-neutral API-service runners, Hermes profile conversion, OpenClaw profile conversion, and other explicitly selected frameworks.

For `package`, include generated target-team agents and functions, profiles, manifests, design intermediate results, `design-output.zip`, `design-output-manifest.json`, `entry-agent-startup-welcome.json`, `docs/entry-agent-startup-welcome.md`, `local-resource-allocation.map.json`, `source-resource-manifest.json`, workflow preservation gate, `design-package-conformance.contract.json`, `runtime-instruction-conformance.json`, `meta-team-audit.contract.json`, package release gate, target-team execution guard, and package-end Codex registration/start/use prompt templates. The local resource allocation map and source-resource manifest are required for source packages with bundled local files.

Every `design` reply must end with paste-ready follow-up prompts for legal next actions or further analysis, including package generation, further design/resource-gate analysis, Codex/OpenAI registration guidance, API-runner construction, API-run role simulation, Hermes profile conversion, and OpenClaw profile conversion prompts. Every `package` reply must end only with Codex package-use prompts: artifact inspection, package release/resource-gate analysis, Codex registration/use after smoke tests, and current-session target-team fan-out when registered target-agent types are unavailable. These prompts are not additional Skill2Team delivery modes.

Direct-skill and meta-team-first must produce target-team packages with the same artifact contract, design archive, conformance gates, Codex package-end prompts, and target-team execution guard. The only allowed difference is the recorded Skill2Team run fan-out status and meta-team activation evidence.

Generated target-team execution in Codex must not degrade into sequential or single-agent simulation. A registered target-team entry agent should hand off to real registered specialist agents. If newly registered target-agent types are unavailable in the active thread but real independent current-session Codex subagents can run, the target run may continue only with `target_run_fanout_status=real_session_target_subagents`, `registered_target_team_smoke_status=pending_hot_reload_or_new_thread`, and explicit entry/specialist/reviewer boundaries. If neither registered handoff nor real current-session target subagents are available, it must stop with `target-team execution blocked`, a concrete reason, and recovery steps.

Use the user's language unless they request otherwise. Keep file names, ids, and placeholders unchanged.

## Helper scripts

Use deterministic helpers only when useful for the requested task:

```bash
python scripts/ensure_codex_meta_team.py --codex-root <CODEX_PROJECT_ROOT> --register
python scripts/generate_deployment_package.py examples/sample_team_plan.json /tmp/s2t_deploy --target codex --delivery package
python scripts/validate_package.py .
```

Helper scripts do not create additional Skill2Team delivery modes.
