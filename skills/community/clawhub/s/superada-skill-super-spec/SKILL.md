---
name: super-spec
description: Create product, technical, PRD, RFC, agent-build, and handoff specs from rough context.
---

# Super Spec

Super Spec turns rough operator context into an executable spec that a builder, reviewer, or agent fleet can act on after context compaction.

Use it when a task needs more than a plan: product requirements, technical design, proof gates, rollout, rollback, builder prompt, and reviewer prompt in one durable artifact.

## What it produces

- Source map: evidence, constraints, assumptions, ignored context, and open questions.
- Goals and non-goals strong enough to stop scope creep.
- Requirements with acceptance criteria and validation method.
- Technical design, data/API surfaces, permissions, dependencies, and failure modes.
- Tests, evals, proof requirements, production QA gate, rollout, observability, and rollback.
- Traceability matrix from requirement to proof.
- Atomic build plan.
- Builder prompt and reviewer prompt.
- Route receipt showing whether the run used Pro or an explicit fallback.

## Why it exists

Agent work often fails because the handoff is mushy: unclear requirements, hidden assumptions, no proof gate, and no way for another agent to resume after context compaction. Super Spec is the antidote. It compiles messy context into a document that can be built, reviewed, and audited.

## Runner behavior

The included runner prefers a Pro/Oracle route when configured. It is fail-closed by default: if Pro is expected and the Pro route fails, it stops instead of silently writing a fallback spec. Use `--no-pro` for an intentional non-Pro run, or set `SUPER_SPEC_ALLOW_CODEX_FALLBACK=on` only when a fallback spec is acceptable.

For long Pro jobs, use background Responses mode and enough time:

```bash
export SUPER_SPEC_ORACLE_BACKGROUND_MODE=on
export SUPER_SPEC_PRO_TIMEOUT=3600
export SUPER_SPEC_PRO_HTTP_TIMEOUT=60m
export SUPER_SPEC_ORACLE_WALL_TIMEOUT=3700s
```

## Install

```bash
curl -sSf https://superada.ai/install/super-spec | sh
```

## Run

```bash
super-spec --title "Enterprise Local Model Orchestrator" --input context.md
```

Or directly:

```bash
skills/super-spec/scripts/run-super-spec.sh --title "<title>" --input <context-file>
```

## Configuration

Set these when using a Pro route:

```bash
export SUPER_SPEC_PRO_MODEL=gpt-5.4-pro
export SUPER_SPEC_PRO_BASE_URL=http://127.0.0.1:4000/v1
export SUPER_SPEC_PRO_API_KEY=...
```

For Azure Responses via Oracle, set your own deployment values:

```bash
export SUPER_SPEC_AZURE_ENDPOINT=https://your-resource.openai.azure.com
export SUPER_SPEC_AZURE_DEPLOYMENT=gpt-5.4-pro
export SUPER_SPEC_AZURE_API_VERSION=2025-04-01-preview
```

Do not paste API keys into specs, prompts, or public docs.

## Quality bar

- The spec must reduce degrees of freedom for the builder.
- Requirements must be testable or explicitly unresolved.
- Non-goals must block obvious scope creep.
- Every risky assumption needs a validation path.
- Tasks must be small enough for review and proof.
- The final spec must be resumable by another agent after context compaction.
