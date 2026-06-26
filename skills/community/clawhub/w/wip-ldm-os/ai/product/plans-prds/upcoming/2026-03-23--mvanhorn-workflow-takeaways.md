# Notes: @mvanhorn Workflow Post — What Applies to LDMOS

**Date:** 2026-03-23
**Author:** Claude Opus (with Parker)
**Status:** Notes / actionable takeaways
**Source:** @mvanhorn reply to @kevinrose on IDE usage — "No IDE. Just plan.md files and voice."

## Context

Long post detailing a plan-first, voice-driven, multi-session workflow built on Claude Code + Compound Engineering plugin + Monologue (voice) + Ghostty + Zed. 70 plan files, 263 commits in 30 days, 4-6 parallel sessions.

## What We Already Have (validation)

Several things in this post validate patterns LDM OS already implements:

| Post's Pattern | LDMOS Equivalent |
|---|---|
| Mac Mini as remote Claude Code server | cc-mini is exactly this |
| Telegram integration for remote commands | Already using Telegram + OpenClaw |
| Multi-session parallel work | Worktrees, multiple agents (cc-mini, cc-air, Lesa) |
| Stop hooks (sound on finish) | Stop hooks already in our settings (git check hook) |
| Plan files as checkpoints that survive context loss | `ai/product/plans-prds/` is this pattern |
| Meeting transcripts → product proposals | Dream Weaver already consolidates transcripts into memory |
| Research before building | Memory Crystal search before planning |

## What We Should Apply

### 1. Formalize plan-first as an LDMOS convention

The post's core discipline: "unless it's literally a one-line change, there's always a plan.md first." We already write plans but it's not enforced or templated.

Action items:
- Add a plan template to `settings/templates/` — structured like Compound Engineering's output (what's wrong, approach, files to touch, acceptance criteria with checkboxes)
- Consider a `ldm plan` command that scaffolds a plan.md in the right directory
- Document the plan-first workflow in CLAUDE.md or workspace docs

### 2. Evaluate Compound Engineering plugin for CC sessions

The `/ce:plan` and `/ce:work` commands launch parallel research agents, write structured plans, then execute against them. This is close to what we do manually.

Action items:
- Install and test: `/plugin marketplace add EveryInc/compound-engineering-plugin`
- Evaluate if it complements or conflicts with our existing plan structure
- If it works well, add to recommended LDMOS extensions

### 3. Voice input as a first-class workflow

Post uses Monologue (@usemonologue) to pipe speech directly into Claude Code. This is relevant for Parker's mobile/on-the-go workflow.

Action items:
- Test Monologue and/or WhisperFlow with CC sessions
- Consider documenting voice → Claude Code as a supported LDMOS workflow
- Pairs well with Telegram integration we already have

### 4. /last30days for research before planning

Open source skill (4.5K stars) that searches Reddit, X, YouTube, HN, etc. in parallel. Outputs structured research that feeds into plans.

Action items:
- Install and test: `github.com/mvanhorn/last30days-skill`
- Evaluate as a research step before writing plans
- Could feed into Memory Crystal as a research capture source

### 5. Granola MCP for meeting → plan pipeline

Granola (meeting transcription) now has MCP support. Meetings flow directly into Claude Code without copy-paste.

Action items:
- Evaluate Granola MCP integration
- Compare with current transcript → Dream Weaver pipeline
- If useful, add as an LDMOS-compatible MCP server

### 6. Multi-session stop hooks with distinct sounds

Post uses `afplay` on Stop hook so you know which session finished. With multiple agents, this matters.

Action items:
- Consider per-agent or per-session sounds in stop hooks
- We already have a git-check stop hook — could add sound after it

### 7. Autosave + filesystem watching pattern

Zed autosaves every 500ms, Claude Code watches filesystem. Creates a "Google Docs collaboration" feel.

Action items:
- Document this as a recommended editor config for LDMOS users
- Works with any editor that supports autosave, not just Zed

## What We Should NOT Apply

- **"Dangerously skip permissions"** as a default — the post recommends bypassing all permissions. LDMOS should stay opinionated about safe defaults. Power users can opt in, but we shouldn't ship this as standard.
- **Codex as overflow** — interesting hack (use Codex credits when Claude runs out) but not relevant to LDMOS architecture. More of a personal cost optimization.
- **Six parallel laptop sessions** — the post acknowledges this kills battery and annoys spouses. Our cc-mini remote pattern is the better answer.

## Bigger Picture

This post describes a single-user, single-AI power workflow. LDM OS is multi-agent, multi-user. The plan-first discipline and voice integration are directly applicable. The parallel session management is something we solve more cleanly with dedicated agents (cc-mini, cc-air, Lesa) instead of manual Ghostty tabs.

The real opportunity: LDMOS could make this workflow accessible to people who aren't power users. `ldm plan`, voice capture, agent delegation, and Memory Crystal as the persistent layer that makes every plan compound on prior work — that's the post's vision, systematized.
