# Dev Update: Public Deploy + Release Docs + Product Feedback

**Date:** 2026-03-04 13:00 PST
**Agent:** CC-Mini
**Session:** Continuation of v0.5.0/v0.6.0 build session

---

## What Happened

### 1. Public Repo Deployment

Both private repos were released but the public repos were not updated. Found `deploy-public.sh` in `wip-dev-tools-private/guide/scripts/` and ran it for both:

- **Memory Crystal:** wipcomputer/memory-crystal PR #11 merged, v0.6.0 release created
- **Dream Weaver Protocol:** wipcomputer/dream-weaver-protocol PR #4 merged, v0.1.1 release created

Script handles everything: rsync (excluding ai/, .git/, .claude/, CLAUDE.md), creates PR on public repo, merges with --merge, syncs release notes from private to public.

### 2. Release Documentation Overhaul

Dream Weaver v0.1.1 release had "Release v0.1.1" as the body. Memory Crystal v0.6.0 was OK but thin. Rewrote both:

**Memory Crystal v0.6.0** ... "The Living Memory Release." Every feature documented section by section: Intelligent Install, Backfill, CE Migration, Dream Weaver integration, Crystal Core Gateway, Staging Pipeline, Commands Channel, OpenClaw Raw Data Sync, Harness-Aware Init, LDM Directory Structure. Full source file tables (new + modified). Applied to all four releases (public + private, both repos).

**Dream Weaver v0.1.1** ... full walkthrough: what the engine does, both modes (full + incremental), the pipeline (discover, extract, invoke, parse, write, watermark), prompts, parser, types, hooks interface, all exports, technical details, connection to Memory Crystal. Applied to all four releases.

### 3. External Reviews Captured

Three AIs reviewed the public releases independently:

- **GPT (ChatGPT 5.2):** Called it "personal cognition infrastructure, not a tool." Proposed Crystal Capture (auto-capture from every AI tool) as the killer adoption feature. Suggested four-layer narrative: Capture / Memory / Reflection / Communication. Two critiques: too many concepts in README, needs 1-command install path.

- **Grok 4.1:** "The closest thing I've seen to giving AI agents a real long-term memory + identity that survives context resets." Called the ===MARKER=== output format "elegant and parse-proof."

- **Claude (Desktop):** Most technically precise. Found the 200K transcript cap as a real tension for mature agents (needs chunked consolidation). Called crystal serve "the interop layer that lets this slot into workflows you didn't build." Staging pipeline is "the kind of thing that separates a tool from a system."

All three independently said the stack now reads like "an actual AI operating system."

### 4. Product Ideas Saved

Three new files in `ai/product/product-ideas/`:
- `crystal-capture-auto-capture.md` ... Crystal Capture feature (auto-capture from ChatGPT Desktop, Claude Desktop, Cursor, browsers, terminal)
- `crystal-capture-architecture-feedback.md` ... GPT's architecture analysis, CaptureEvent interface, four-layer model
- `external-reviews-v0.6.0.md` ... all three reviews synthesized with open technical questions

### 5. Plans-PRDs Reorganization

Updated both canonical docs in `ai/product/plans-prds/`:
- `roadmap.md` ... complete rewrite with three-state system (Upcoming / Done / Deprecated). 11 upcoming priorities, all shipped features grouped by version, 7 deprecated items.
- `readme-first.md` ... replaced stale 68-line version with comprehensive 423-line version, updated for v0.6.0 (What's Built, What's Missing, source files, document references).

---

## Key Decisions

1. **deploy-public.sh is in wip-dev-tools-private** (not sunsetted location). Must run after every private repo release.
2. **Release docs must be comprehensive.** Parker's direction: "explain what it does, detail by detail." Release pages are the public face.
3. **Crystal Capture is the next major feature direction.** Auto-capture from every AI surface. We already have the pipeline (cc-hook, cc-poller, agent_end). Gap is adapters.
4. **Roadmap uses three states only:** Upcoming, Done, Deprecated. Never delete. Always move.

---

## What's Next

- Run `crystal backfill` + `crystal migrate-embeddings` (the actual execution, not just the code)
- Sort plans-prds/sort/ into archive-complete/ vs current/
- Consider README simplification (30-second mental model at top)
