# Startup Page

A bare startup request such as `Start Skill2Team.` shows the startup page only.

The startup page is not conversion. It must not inspect uploaded files, read `SKILL.md`, ask guided intake questions, generate a team, generate runtime artifacts, register agents, compare outputs, or call helper scripts.

## Required startup contents

1. What Skill2Team does.
2. **OpenAI Codex model invocation reminder**: Skill2Team itself, `s2t-meta-*` service agents, and generated target-team agents default to OpenAI Codex runtime/custom-agent invocation, not direct model API calls.
3. **framework-neutral agent relationship architecture reminder**: package design defaults to profile-based agents as graph nodes and explicit handoff/review/checkpoint edges.
4. Reminder that source material is required before conversion starts.
5. Fixed six-agent S2T service team.
6. Execution path selector.
7. Route selector.
8. Delivery selector: `design` or `package`.
9. Codex-only runtime selector when deployable artifacts are needed.
10. Human-interaction preservation selector for conversion: preserve source human-interaction steps by default, selectively preserve/convert steps, or fully automate with audit only by explicit choice.
11. Package output reminder: design intermediate results, entry-agent startup welcome page, generated target-team agents/functions, agent profiles, Codex artifacts, design-output archive, and Codex-only package-end prompt templates.
12. Agent-count note: prefer 5-6 top-level agents; justify other counts.
13. Architecture/workflow note: Agent Architecture Map and Workflow Orchestration Map are separate outputs.

## Fixed S2T service team

| Registered agent id | Internal role | Future responsibility |
|---|---|---|
| `s2t-meta-entry` | **S2T Lead** | Intake, route/delivery/execution-path selection, state tracking, synthesis ownership |
| `s2t-meta-source-mapper` | **Source Mapper** | Source inventory, workflow extraction, local-resource classification |
| `s2t-meta-architecture-designer` | **Architecture Designer** | Agent Architecture Map, role boundaries, skill allocation, count rationale |
| `s2t-meta-workflow-orchestrator` | **Workflow Orchestrator** | Workflow Orchestration Map, control-flow, handoffs, checkpoints, reruns, resume |
| `s2t-meta-runtime-adapter` | **Runtime Adapter** | Codex package artifacts, profile artifacts, manifests, prompt rewriting, design-output archive and Codex-only package-end templates |
| `s2t-meta-evaluation-reviewer` | **Quality Reviewer** | Independent design/package review, risk checks, count justification, acceptance-gate checks |

This service team is a planning/routing structure during bare startup. If `meta-team-first` is explicitly selected with `Target runtime: codex`, Skill2Team must generate/reuse/register the fixed six-agent `s2t-meta` Codex team, then separately verify whether the active Codex session can invoke the registered custom agents. Some Codex desktop sessions do not hot-load agent types written to `.codex/config.toml` during the same thread. In that case, Skill2Team may continue only if real current-session subagents execute the fixed S2T work orders and the run records `current_run_fanout_status=real_session_subagents`; otherwise it must stop. Fallback role-play is not allowed in Codex `meta-team-first`. Real model work should be run through OpenAI Codex unless the user explicitly chooses a labeled API-service follow-up.

## Execution paths

| Execution path | Meaning |
|---|---|
| `direct-skill` | Default. Use Skill2Team directly without generating or activating the S2T meta-team first. |
| `meta-team-first` | First generate/reuse/register the fixed six-agent S2T meta-team in Codex, then either activate registered `s2t-meta-*` agents or use real current-session subagents for fixed S2T work orders. No fallback role-play is allowed in Codex `meta-team-first`. |

If `meta-team-first` cannot confirm registered Codex meta-agent activation or real current-session subagent handoff, stop with `meta-team-first blocked`, give the concrete reason, and provide recovery steps. Do not continue with a fallback run.

## Routes

| Route | Meaning |
|---|---|
| `source-to-team` | Convert or restructure existing source material. |
| `brief-to-team` | Turn a brief or rough workflow description into a first team draft/package. |
| `guided-to-team` | Ask guided questions before design/package. |

## Delivery modes

| Delivery | Meaning |
|---|---|
| `design` | Inventory, diagnosis, architecture map, workflow map, contracts, role cards, skill allocation, gates, migration plan, and design quality gate. |
| `package` | Generate Codex package artifacts and manifests without installing; include design intermediate results, `design-output.zip`, entry-agent startup welcome page, target-agent list, profile files, usage guide, package release gate, and Codex-only package-end prompt templates. |

Skill2Team 1.9.2 exposes only `design` and `package`. Package is a concrete continuation after design; other continuations are guided by prompt templates.

## Default prompt

```text
Start Skill2Team.
Route: source-to-team
Delivery: package
Execution path: direct-skill
Target runtime: codex
Model invocation policy: use OpenAI Codex; do not call direct model APIs.
Source material: <SOURCE_SKILL_ZIP / path-to-source-skill / generated-team-package / registry-manifest / pasted workflow description>
Use framework-neutral agent relationship architecture with profile-based agents.
Separate Agent Architecture Map from Workflow Orchestration Map. Prefer 5-6 top-level agents and justify any other count.
Package output must include design intermediate results, `design-output.zip`, generated target-team agents and functions, agent profiles, Codex artifacts, usage guide, package release gate, and Codex-only package-end prompt templates.
Human-interaction mode: preserve source human-interaction steps by default; ask before converting selected steps to reviewer gates or audited automation.
```
