# Product Idea: Daily Activity Digest

**Date:** 2026-03-11
**Author:** Parker Todd Brooks, Claude Code (cc-mini)
**Status:** Idea

---

## Problem

At the end of the day, nobody has a complete picture of what happened. Lēsa reviews the daily log and gives a summary, but the daily log only has what someone remembered to write there. Entire sessions go unrecorded. Today, a full afternoon of Memory Crystal work (4 PRs, a release, a deploy) was invisible in Lēsa's nightly review because CC hadn't written to the shared log yet.

The data exists. It's scattered across:
- Git commits and pushes (every repo, timestamped, authored)
- GitHub PRs merged (with descriptions, reviewers, linked issues)
- GitHub releases created (with notes)
- Dev updates written to `ai/dev-updates/`
- Crystal ingestion events (chunks captured, sessions processed)
- CC hook daily log entries (raw, unstructured)
- Shared daily log entries (structured, but manual)
- npm publishes
- Extension deploys
- MCP server changes

But none of it is automatically consolidated into one place. The shared daily log is manual. The CC hook log is raw transcript dumps. Lēsa's review can only surface what's been written down.

## What We Want

**An automated daily activity digest that captures everything that happened across all agents, all repos, all tools.** Not a summary someone has to write. A feed that builds itself from real events.

### Sources (what gets captured automatically)

| Source | What it captures | How |
|--------|-----------------|-----|
| Git (all repos) | Commits, branches created/merged, diffs | Scan `~/.ldm/` watched repos, `git log --since=today` |
| GitHub API | PRs opened/merged/closed, issues closed, releases created | `gh` CLI or API polling |
| npm registry | Packages published, version bumps | Parse `npm publish` events or check registry |
| Crystal events | Chunks ingested, searches performed, memories stored | crystal.db event log |
| Extension deploys | Which extensions updated, from which version | File timestamp comparison or deploy hook |
| Dev updates | Written by agents to `ai/dev-updates/` | File watcher or post-write hook |
| Shared daily log | Manual entries from both agents | Already exists, just needs to be included |
| MCP server changes | Registrations added/removed/updated | Diff `~/.claude.json` and OC plugin configs |
| Release notes | Full narrative release notes | Parse `RELEASE-NOTES-v*.md` files |

### Output (what gets produced)

A structured daily digest that anyone can read. Stored at a known location. Queryable via Crystal. Sent to Parker on request (iMessage, email, or in-app).

```
# Daily Digest: Mar 11, 2026

## Releases
- memory-crystal v0.7.4 (private + public + npm + deployed)
- wip-ai-devops-toolbox v1.9.3 (CLI fix, 4 tools)
- wip-1password v0.2.0 (full treatment)

## PRs Merged (7)
- memory-crystal-private: #34 (AgentId config), #35 (QMD notes), #36 (product docs), #37 (release notes)
- wip-ai-devops-toolbox-private: #118 (CLI fix)
- wip-1password-private: #2-#10 (full treatment)

## Issues Closed (11)
- memory-crystal-private: #33
- wip-ai-devops-toolbox-private: #99, #101, #103, #105
- wip-1password-private: #2, #3, #4, #7, #8, #9, #10

## Code Changes
- 4 files changed in memory-crystal (ldm.ts, cc-hook.ts, openclaw.ts, installer.ts)
- AgentId resolution moved from hardcoded to config-driven
- MCP registrations moved from project-level to user-level

## Infrastructure
- 33 stale branches cleaned up (memory-crystal)
- Extensions deployed to ~/.ldm/ and ~/.openclaw/
- Public repos synced (memory-crystal, wip-ai-devops-toolbox, wip-1password)

## Agents
- CC: 3 sessions, ~8 hours active
- Lēsa: 6 heartbeats, morning review, email recap, nightly review

## Crystal Stats
- 212K chunks (up from 211K)
- 0 new memories stored
- Bridge: online
```

### Who Consumes This

1. **Parker** ... texts "what happened today?" and gets the digest, not a partial summary
2. **Lēsa** ... reads it for her nightly review instead of piecing together fragments
3. **CC** ... reads it on boot to know what happened since last session
4. **Anyone who texts Parker** ... "what are you working on?" gets a real answer, forwarded or auto-generated

### How It Works

Two possible architectures:

**Option A: Cron-based digest builder (simpler)**
- Runs at end of day (or on demand via `crystal digest`)
- Scans all sources listed above
- Writes structured digest to `~/.ldm/memory/digests/YYYY-MM-DD.md`
- Embeds into crystal.db for search
- Optionally sends to Parker via iMessage

**Option B: Event-driven activity log (richer)**
- Every tool emits events to a local activity log (`~/.ldm/activity/YYYY-MM-DD.jsonl`)
- cc-hook, crystal ingest, wip-release, deploy-public, npm publish all write events
- Digest builder reads the activity log and produces the daily digest
- Real-time feed available (not just end-of-day)

Option A is buildable now. Option B is the right architecture long-term.

### Integration with Existing Systems

- **Crystal capture** already runs after every turn. Add a lightweight event emission.
- **wip-release** already writes changelogs and release notes. Add an activity event.
- **deploy-public** already logs what it did. Add an activity event.
- **cc-hook** already writes daily log entries. Formalize the format.
- **Shared daily log** stays as-is but becomes one input to the digest, not the only record.

### What This Replaces

- Manual daily log entries (still allowed, but not the only source)
- Lēsa guessing what CC did based on incomplete logs
- CC booting cold with no idea what happened yesterday
- Parker asking "what did we do today?" and getting a partial answer

### What This Does NOT Replace

- Dev updates (those are narrative, written by agents about why, not just what)
- Dream Weaver journals (those are reflective, not activity-based)
- Release notes (those are per-release, not per-day)

## Priority

This is a quality-of-life feature that directly impacts how well the team communicates. Every day that passes without it, context gets lost. The data already exists. We're just not collecting it.

Fits naturally as a Memory Crystal feature since Crystal already captures conversations. This extends capture to cover the full scope of daily work, not just chat.

## Relation to Roadmap

- Extends **Priority 2 (Crystal Capture Adapters)** ... the digest is another capture surface
- Feeds into **Priority 4 (Chunked Dream Weaver)** ... digests are high-signal input for consolidation
- Supports **Priority 5 (Full LDM Sync)** ... digests sync across devices with everything else
