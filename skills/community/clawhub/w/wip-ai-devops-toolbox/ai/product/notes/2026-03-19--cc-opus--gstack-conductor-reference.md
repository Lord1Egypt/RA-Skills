# Reference: gstack Conductor / Multi-Session Orchestration

**Date:** 2026-03-19
**Author:** cc-opus
**Status:** Reference doc (not active work)
**Related to:** LDM OS / Memory Crystal agent coordination

## What it is

gstack's `conductor.json` defines how to orchestrate multiple parallel Claude Code sessions. The idea: run 10-15 concurrent sprints, each handling a different feature/bug/task, with a coordinator managing the workflow.

## How gstack does it

Their `conductor.json` is currently minimal (just setup/teardown scripts), but the concept is described in their docs:

- Each session gets a role (plan, build, review, QA, ship)
- Sessions run in parallel on the same codebase
- A conductor coordinates: assigns tasks, collects results, resolves conflicts
- Sprint structure: Think → Plan → Build → Review → Test → Ship → Reflect

## Why this matters for LDM OS / Memory Crystal

Multi-session orchestration is fundamentally an **agent coordination problem**:
- Multiple Claude Code sessions working on different repos simultaneously
- Cross-repo operations (license checks across 10 repos, bulk releases)
- Agent-to-agent handoffs (Claude Code → Lesa, or vice versa)
- Parallel devops pipelines (test all repos, update all manifests)

This overlaps with whatever LDM OS / Memory Crystal is building for agent orchestration. The tooling should live where the coordination layer lives — not necessarily in WIP Code.

## What to capture for later

When we're ready to build this:

1. **Study gstack's full conductor vision** — their docs describe the parallel sprint model
2. **Identify what's WIP Code vs LDM OS** — task distribution is LDM OS; task execution is WIP Code
3. **Define the interface** — how does a conductor tell wip-release to run across 5 repos?
4. **Consider `wip-repos` as the foundation** — we already have a manifest reconciler that knows about all repos

## Source files

- `ai/repos/gstack-private/conductor.json` — their config (minimal)
- `ai/repos/gstack-private/ARCHITECTURE.md` — their architecture docs
- `ai/repos/gstack-private/CLAUDE.md` — describes the parallel sprint workflow
