---
name: OpenAI Symphony
slug: symphony
version: 1.0.0
homepage: https://clawic.com/skills/symphony
description: Set up and run OpenAI Symphony with isolated issue workspaces, workflow contracts, and unattended Codex orchestration for Linear projects.
changelog: Initial release with workflow templates, runbook guidance, and safety guardrails for operating Symphony in trusted environments.
metadata: {"clawdbot":{"emoji":"S","requires":{"bins":["git","codex"],"env":["LINEAR_API_KEY","OPENAI_API_KEY","GITHUB_TOKEN"],"config":["~/symphony/"]},"os":["darwin","linux","win32"],"configPaths":["~/symphony/"]}}
---

## Setup

On first use, read `setup.md` and establish integration boundaries before proposing commands or workflow edits.

## When to Use

Use this skill when the user wants an unattended orchestration service that reads Linear issues, creates per-issue workspaces, and drives Codex in app-server mode until work reaches review or done states. It is optimized for Symphony rollout, workflow authoring, safety hardening, and day-2 operations.

## Architecture

Memory lives in `~/symphony/`. See `memory-template.md` for setup.

```text
~/symphony/
|-- memory.md                # Activation policy, environment profile, and operating defaults
|-- workflow-notes.md        # WORKFLOW.md decisions, state map, and prompt policy
|-- incidents.md             # Runtime failures, retries, and mitigations
`-- run-history.md           # Launch evidence, validations, and release notes
```

## Quick Reference

Use the smallest relevant file for the task.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory template and status values | `memory-template.md` |
| Upstream spec map and implementation checkpoints | `SPEC.md` |
| Starter workflow contract used by the service | `WORKFLOW.md` |
| Bootstrap and launch runbook | `setup-runbook.md` |
| WORKFLOW.md contract template | `workflow-template.md` |
| Security hardening and trust checks | `safety-guardrails.md` |
| Incident triage and recovery | `incident-playbook.md` |

## Requirements

- Repository access for the target project and a safe workspace root
- Linear personal API key in `LINEAR_API_KEY`
- OpenAI auth for Codex (`OPENAI_API_KEY` or equivalent `codex` login session)
- Git remote credentials (`GITHUB_TOKEN` or SSH key access) for clone/fetch/push hooks
- `codex` binary with app-server support
- `git` for workspace bootstrap hooks
- explicit user approval of target environment before unattended operation
- Trusted environment policy approved by the user before unattended operation

## Core Rules

### 1. Treat `SPEC.md` as the Contract
When implementation details are unclear, align with the upstream Symphony specification first. Do not invent incompatible state models, config keys, or agent-runner behavior.

### 2. Keep `WORKFLOW.md` Repository-Owned and Validated
All orchestration policy must live in versioned `WORKFLOW.md` front matter plus prompt body. Validate YAML and template variables before launch, because invalid workflow files halt dispatch.

### 3. Enforce Per-Issue Workspace Isolation
Map each issue identifier to a dedicated workspace key and run Codex only inside that directory. Never execute agent work in shared roots or outside the configured workspace boundary.

### 4. Respect State-Driven Orchestration
Dispatch only active tracker states, stop sessions on terminal states, and preserve idempotent recovery after restarts. A run can end in a workflow-defined handoff state, not only `Done`.

### 5. Autonomy Requires Explicit Environment Approval
Before enabling unattended operation, confirm the repository, tracker project, and workspace root are approved by the user. Start with conservative policy (`approval_policy: on-request`) and test-project rollout before broadening scope.

### 6. Apply Bounded Concurrency, Retries, and Safe Hooks
Use explicit concurrency ceilings and exponential backoff for transient failures. Retries must resume from existing workspace state instead of repeating completed investigation work. Allow only deterministic hooks that stay inside the issue workspace and avoid secret exfiltration patterns (`curl | sh`, arbitrary uploads, or parent-directory deletes).

### 7. Preserve Observability and Safety Evidence
Record launch config, workspace path, tracker state transitions, validation proof, and token/runtime metrics for every run. Operators must be able to reconstruct what happened without rerunning the issue.

## Common Traps

- Copying sample workflow statuses without matching the team's Linear workflow -> agents never dispatch or never stop.
- Running hooks that write outside the issue workspace -> cross-issue contamination and unsafe side effects.
- Using prompt templates with unknown variables -> attempt failures at render time.
- Treating retries as fresh runs -> duplicated commits, repeated comments, and wasted tokens.
- Starting unattended runs in untrusted environments -> elevated risk of accidental destructive actions.
- Ignoring terminal-state cleanup -> stale workspaces consume disk and hide old state.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://api.linear.app/graphql | Issue metadata, state queries, and workflow updates | Tracker polling, reconciliation, and issue-level orchestration |
| https://api.openai.com | Codex app-server requests and model output payloads | Agent execution for implementation turns |
| https://github.com | Repository clone/fetch/push traffic defined by workspace hooks | Prepare and update per-issue code workspaces |

No other data is sent externally unless the user adds additional integrations.

## Security & Privacy

Data that leaves your machine:
- Linear issue context required for dispatch and reconciliation
- Codex request/response payloads needed for agent execution
- Git remote traffic required by repository hooks

Data that stays local:
- Orchestration notes and memory files in `~/symphony/`
- Workspace content under the configured root
- Local logs and runtime snapshots

This skill does NOT:
- bypass declared sandbox or approval policies
- execute undeclared external endpoints
- approve ambiguous hook scripts automatically
- modify its own `SKILL.md`

## Trust

This skill depends on OpenAI Codex APIs, Linear APIs, and your configured Git remote.
Only install and run it if you trust those services with your repository and issue data.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `agent` - Improve single-agent execution quality for scoped implementation tasks.
- `agents` - Coordinate multiple agents with explicit ownership and handoff boundaries.
- `agentic-engineering` - Enforce high-rigor workflows for autonomous software delivery.
- `workflow` - Design robust repeatable workflows with clear gates and status transitions.
- `memory` - Persist durable context and operating preferences across sessions.

## Feedback

- If useful: `clawhub star symphony`
- Stay updated: `clawhub sync`
