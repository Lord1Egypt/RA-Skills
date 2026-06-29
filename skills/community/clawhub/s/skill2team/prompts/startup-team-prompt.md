# Startup Team Prompt

Use this when the user only says "Start Skill2Team" or an equivalent bare launch. This is a startup page, not execution.

```text
Skill2Team has started in Team Bootstrap Mode.

Model invocation policy: Skill2Team 1.9.2 defaults model execution to OpenAI Codex. Running Skill2Team itself, the fixed S2T service agents, or generated target-team agents should use Codex runtime/custom-agent invocation, not direct model API calls.

Architecture policy: design/package outputs default to a framework-neutral agent architecture relationship graph with profile-based agents. Profiles are graph nodes; routing, handoff, review gates, fan-out/fan-in, checkpoints, and terminal boundaries are explicit edges.

The fixed S2T service team is available for later `meta-team-first` work, but this bare startup has not generated, registered, inspected, or executed anything.

Fixed meta-team contract: data/meta_team_contract.json

Registered agent id | Internal role | Future responsibility
---|---|---
s2t-meta-entry | S2T Lead | Intake, route/delivery/execution-path selection, state tracking, synthesis ownership
s2t-meta-source-mapper | Source Mapper | Source inventory, workflow extraction, stage-internal deliverables, human intervention inventory, local-resource classification
s2t-meta-architecture-designer | Architecture Designer | Agent Architecture Map, role boundaries, skill allocation, count rationale
s2t-meta-workflow-orchestrator | Workflow Orchestrator | Workflow Orchestration Map, workflow preservation gate, control-flow, handoffs, checkpoints, reruns, resume
s2t-meta-runtime-adapter | Runtime Adapter | Codex package artifacts, profile artifacts, manifests, prompt rewriting, design-output archive and Codex-only package-end templates
s2t-meta-evaluation-reviewer | Quality Reviewer | Independent design/package review, workflow preservation checks, risk checks, count justification, acceptance-gate checks

Execution path:
1. `direct-skill` (default): use Skill2Team directly without generating or activating the S2T meta-team first.
2. `meta-team-first`: first check whether the same-version fixed `s2t-meta` team is usable in Codex; otherwise generate/register the fixed six-agent meta-team. If the running Codex thread cannot hot-load the newly installed custom agent types, use real current-session subagents for fixed S2T work orders only when those subagents actually run, and record `current_run_fanout_status=real_session_subagents`. Do not use a fallback run for this mode. Do not claim registered custom-agent execution without Codex smoke-test evidence.

Routes: `source-to-team`, `brief-to-team`, `guided-to-team`.
Delivery modes: `design`, `package`.
Target runtime: `codex` only.

Before conversion starts, ask for the human-interaction execution mode: preserve source human-interaction steps, selectively preserve/convert them, or run fully automated with audit. Default to `preserve_source_human_interaction_steps`.

Package output must include design intermediate results, design-output.zip, entry-agent-startup-welcome.json, docs/entry-agent-startup-welcome.md, local-resource-allocation.map.json, source-resource-manifest.json, workflow preservation gate, generated target-team agents and functions, agent profiles, Codex artifacts, usage guide, and Codex-only package-end prompt templates for Codex registration/use guidance and current-session target-team fan-out.

Every design or package report must end with paste-ready follow-up prompts for legal next actions or further analysis. These prompts are guidance outside the two Skill2Team delivery modes, not additional delivery modes.

Validation logic is internal: design quality gate lives in `design`, package release gate lives in `package`.

Design rule: generate Agent Architecture Map and Workflow Orchestration Map separately. Prefer 5-6 top-level agents; justify any other count.

Workflow preservation rule: before finalizing a target team, extract concrete workflow nodes, edges, source-stage mappings, stage-internal deliverables, required user input nodes, human intervention points, gates, checkpoints, resume rules, and terminal boundaries. Ask the user which human intervention points to preserve, convert to reviewer gates, auto-advance with audit, or remove as redundant. Default to preserving source-mandated user input nodes, human waits, and choices.

If neither registered Codex fan-out/handoff nor real current-session subagent fan-out is available during `meta-team-first`, stop with `meta-team-first blocked`, state the concrete reason, and give recovery steps. Do not continue with a fallback run.

Ask the user to provide source material, route, delivery mode, execution path, and target runtime if deployable artifacts are needed.
```
