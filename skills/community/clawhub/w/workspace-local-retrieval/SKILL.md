---
name: workspace-local-retrieval
description: Build a local-first retrieval architecture for an OpenClaw workspace with explicit corpus boundaries, deny-by-default agent access, separate personal-memory vs workspace-knowledge layers, stable agent-facing search interfaces, and maintenance-aware refresh workflows. Use when a user wants to: (1) add local RAG without indexing everything, (2) separate personal memory from reusable workspace retrieval, (3) define agent-scoped access to different corpora, (4) package a retrieval system as a reusable skill rather than private glue code, (5) add explainable status / refresh workflows, or (6) turn a one-off local search setup into a safer multi-agent retrieval pattern.
---

# Workspace Local Retrieval

Package retrieval as architecture, not ad-hoc glue.

This skill exists for a common failure mode in local RAG systems: indexing grows faster than boundary discipline. The result is usually a system that can sometimes retrieve relevant text, but cannot clearly answer:
- what should be searchable
- which agent should see which corpus
- what belongs in personal memory versus workspace knowledge
- how freshness should be maintained over time

Prefer this skill when the goal is **workspace knowledge retrieval**, not personal memory recall. Keep those layers separate.

## Single-command npm install

This skill also ships as an npm-friendly CLI. Install it with one line (`npm install -g workspace-local-retrieval`) or run it on-demand via `npx workspace-local-retrieval install`. The CLI wraps the existing Python helpers (`scripts/check_retrieval_prereqs.py` + `scripts/bootstrap_workspace_retrieval.py`), so the `install` command performs a safety check, writes the `retrieval/config` templates, and hints at the next refresh/index steps. Run `workspace-local-retrieval check` anytime for a standalone prerequisite report.

## Core workflow

0. **Run a preflight gate before any retrieval work**
   - Run `scripts/check_retrieval_prereqs.py` before bootstrap, indexing, embedding refresh, or search.
   - Classify findings into:
     - **required**: must exist before execution
     - **recommended**: may proceed with warning
     - **optional**: capability upgrade only
   - Treat missing required prerequisites as a hard stop.
   - Do not continue into retrieval execution when the environment is not ready.
   - Read `references/dependencies-and-platforms.md` when deciding what is required on the current OS.

1. **Decide the boundary model first**
   - Use built-in memory tools for personal continuity (`MEMORY.md`, `memory/*.md`).
   - Use this skill's retrieval pattern for workspace knowledge, docs, skills, plans, schemas, and agent-specific materials.
   - Do not merge personal notes into a general retrieval corpus unless the user explicitly wants that and understands the privacy tradeoff.

2. **Design corpora before indexing**
   - Split knowledge into small allowlisted corpora.
   - Prefer domain or workspace boundaries over one giant corpus.
   - Exclude runtime state, secrets, private notes, vector DB artifacts, build outputs, and caches.
   - Read `references/privacy-and-boundaries.md` before writing config.

3. **Define agent access explicitly**
   - Use deny-by-default agent retrieval policy.
   - Allow each agent to see only the corpora it needs.
   - Use separate memory-boundary rules for personal memory vs domain memory.
   - Read `references/agent-scoping.md` when creating agent rules.

4. **Bootstrap templates safely**
   - Run `scripts/bootstrap_workspace_retrieval.py --dest <dir>` to generate sanitized starter templates.
   - The script creates template config files only. It does not read external services, call the network, or ingest private data.
   - Read `references/runtime-layout.md` and `references/dependencies-and-platforms.md` before claiming the setup is runnable.
   - Run `scripts/check_retrieval_prereqs.py` before wiring indexing or embedding backends.

5. **Implement retrieval entrypoints**
   - Keep one stable wrapper for agent-facing search.
   - Make the wrapper responsible for corpus allowlist checks.
   - Keep indexing / embeddings / scoring internals behind the wrapper.
   - Read `references/interface-contract.md` for a recommended contract.

6. **Add freshness + maintenance**
   - Track corpus fingerprints or file signatures.
   - Prefer selective refresh when only a small set of files changed.
   - Fall back to full rebuild only when needed.
   - Read `references/maintenance-patterns.md` for a production-friendly approach.

7. **Validate with smoke tests**
   - Test at least:
     - one broad query
     - one corpus-specific query
     - one agent allowlist denial
     - one changed-file refresh path
   - Do not claim retrieval is ready because indexing succeeded once.

8. **Handle missing prerequisites explicitly**
   - If a required prerequisite is missing and the user has **not** authorized installation or environment changes:
     - stop
     - say the skill is currently unavailable
     - list the missing prerequisites
     - tell the user what must be installed or configured first
   - If a required prerequisite is missing and the user **does** want the environment prepared:
     - create a task plan first
     - make the plan OS-specific when needed
     - install or configure dependencies
     - update config and documentation to reflect the chosen backend and runtime
     - rerun `scripts/check_retrieval_prereqs.py`
     - continue only after the required checks pass
   - Use this rule consistently for macOS, Linux, and Windows. Do not pretend portability removes the need for explicit checks.

## Recommended file layout

Use this skill as a pattern, not a rigid requirement.

```text
retrieval/
  config/
    corpora.json
    agent_corpora.json
    agent_memory.json
    backend.json
  scripts/
    workspace_search.mjs
    build_index.py
    build_embeddings.mjs
    retrieval_status.py
    refresh_incremental.py
  indexes/
    workspace_retrieval.sqlite
```

If the workspace already has a retrieval system, adapt the layout instead of forcing a rewrite.

## Defaults worth keeping

- local-first storage
- allowlisted corpora
- deny-by-default agent access
- personal memory separate from workspace retrieval
- minimal indexed file extensions
- explicit exclude globs
- incremental refresh before full rebuild
- one stable wrapper for agent-facing search

## When to read references

- Read `references/privacy-and-boundaries.md` for safe corpus design and exclusions.
- Read `references/agent-scoping.md` when mapping corpora and memory roots to agents.
- Read `references/interface-contract.md` when building or reviewing the agent-facing search wrapper.
- Read `references/maintenance-patterns.md` when adding status checks, selective refresh, and smoke tests.
- Read `references/example-templates.md` when you need sanitized starter JSON examples.
- Read `references/dependencies-and-platforms.md` when the user wants concrete runtime dependencies, embedding backend choices, or cross-platform guidance.
- Read `references/preflight-and-install-policy.md` when deciding whether the skill is runnable now, blocked, or should first produce an installation task plan.
- Read `references/runtime-layout.md` when the user wants a more runnable implementation footprint.
- Read `references/design-rationale.md` when the user needs the architectural thesis, tradeoffs, or public-facing positioning.
- Read `references/sanitized-demo.md` when the user wants a safe walkthrough or publishable example.
- Read `references/publish-readiness-checklist.md` before packaging or publicly promoting the skill.

## Practical guidance

- Prefer fewer, clearer corpora over many overlapping ones.
- Avoid indexing secrets, credentials, private journals, logs, and generated artifacts.
- If two agents need different trust levels, separate their corpora even if the docs overlap.
- If retrieval results look noisy, improve corpus design before tuning ranking weights.
- If privacy matters, treat boundary design as a first-class feature, not cleanup later.
- Treat prerequisite checks as part of the runtime contract, not as optional setup advice.
- The npm-friendly CLI is the simplest user entry point: `workspace-local-retrieval install` bootstraps the templates, `workspace-local-retrieval check` reports missing requirements, and both commands accept `--dest`, `--workspace-root`, and `--force` switches for customization.
- No required prerequisites, no execution.
- If installation is needed, prefer a short task plan over ad-hoc shell improvisation.
- After installation or config changes, rerun preflight checks before claiming the skill is ready.

## Output expectations

When using this skill for a user request, produce some or all of the following depending on scope:
- sanitized corpus config
- agent allowlist config
- memory-boundary config
- search wrapper contract
- maintenance workflow
- smoke-test checklist
- packaging-ready skill contents when the user wants distribution
