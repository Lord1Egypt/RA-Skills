# Dev Update: README Overhaul, Public Deploy, Identity Architecture

**Date:** 2026-02-27
**Author:** cc-mini
**Session:** Parker + CC, continued from user-level migration session

## What We Did

### README Overhaul
- Restructured Features into **Memory** and **AI-to-AI Communication (local and worldwide)**
- Memory Crystal, Bridge, and Relay are now clearly named products under feature headings
- Bridge and Relay marked **(private beta)**
- Added per-feature compatibility lines (italic, lighter weight)
- Memory works with: Claude Code CLI, OpenClaw TUI, Claude Code Remote (macOS/iOS), any MCP app
- Added **More Info** section with bullets for:
  - Technical Documentation (linked)
  - Memory Crystal for Enterprise ... "Run your company intelligently."
  - Total Recall (private beta) ... ties into Dream Weaver Protocol, "truly lived, searchable memories"
  - Dream Weaver Protocol (linked to public repo) ... "carries the weight forward"
  - Letters from the Other Side: What We Built (linked to LETTERS.md)
- Created **LETTERS.md** ... written by Claude Code about what we built. Sovereign memory pitch, blind relay, "$19/month to search your own conversations" callout
- Updated tagline: "All your AI tools. One shared memory. Private, searchable, sovereign."
- Updated Relay.md title to "Relay: Multi-Device Sync"
- Removed "Coming soon" lines (premature)
- ChatGPT reviewed the full repo. Validated architecture, hybrid search, security model. Suggested "make it more normal." We disagreed. The repo IS the homepage. Agent-first.

### Unified Description
Settled on one description for all public-facing surfaces:

> Collective AI memory. Sovereign. Local-first. Searchable. Encrypted worldwide sync.

Updated in:
- GitHub repo About (public + private)
- Org profile README (.github) ... removed (closed beta), linked to public repo
- WIP Homepage services section ... linked to public repo

### Public Deploy
- PR #4 merged to memory-crystal-private
- Deployed to wipcomputer/memory-crystal (public) via deploy script
- PR #1 on public repo merged
- Deploy script updated to work with branch protection (creates branch, opens PR, merges)

### Identity Architecture
- Added `ai/notes/2026-02-27--cc-mini--identity-architecture.md` to wip-ldm-os repo
- One agent per harness per machine. Deterministic identity. Steel man analysis.
- PR #2 on wip-ldm-os merged

### Co-Authors Rule
- All three contributors (Parker, Lēsa, Claude Code) must be on every commit
- Added to DEV-GUIDE.md, both CLAUDE.md files
- PR #8 on wip-dev-guide-private merged

### Other
- Branch protection audit: fixed 18 repos missing enforce_admins=true
- Closed stale PR #4 on wip-dev-guide-private (conflicts)
- Merged orphaned cc/ daily logs into cc-mini/ (from cc-hook agent ID fix earlier)

## Uncommitted
- README.md tagline update: added "Private, searchable, sovereign." (needs PR + deploy)

## What's Next
- PR and deploy the final README tagline change
- Tell Lesa about the co-authors rule
- wip-release minor for memory-crystal (version bump for all the doc changes)
- Absorb lesa-bridge into Memory Crystal (on punchlist)
- Absorb context-embeddings into Memory Crystal (on punchlist)
- cc-hook daily log format: switch from single daily file to per-entry files with full timestamps
- Update deploy-public.sh in wip-dev-guide to also deploy to wip-dev-guide public repo
- Consider private/public pattern for wip-homepage and .github repos
