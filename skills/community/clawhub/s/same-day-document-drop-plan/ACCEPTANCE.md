# Acceptance Criteria - Same-Day Document Drop Plan

## Gate Checks

- [x] `SKILL.md` exists and contains a prompt-only workflow.
- [x] `skill.json` is valid JSON and declares `version=1.0.0`, `license=MIT-0`, `language=en`, and `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] Public-facing documentation is English only.
- [x] No executable code, scripts, package files, network calls, APIs, credentials, secrets, or private data are included.
- [x] Trigger scenario, concrete deliverable, workflow, output format, and safety boundary are explicit.
- [x] The workflow is limited to logistics, document handling, proof, and fallback planning.
- [x] The workflow requires recipient, hours, cutoff, intake method, and original-document requirements to be verified.
- [x] The output includes a drop mission snapshot, recipient verification, document inventory, packet prep checklist, route plan, proof checklist, fallback plan, post-drop log, and open questions.
- [x] The safety boundary handles originals and identity documents carefully and avoids legal sufficiency or official acceptance claims.
- [x] No CJK characters are present.

## Scope

- Prompt-only MVP.
- Local implementation only.
- Not published to ClawHub in this phase.

## Clean Scan Evidence

- [x] Secrets scan: no API keys, tokens, passwords, or credentials found.
- [x] Executable scan: no scripts, binaries, or executable code present.
- [x] Network scan: no outbound calls, fetch, or API endpoints.
- [x] File audit: only SKILL.md, skill.json, and ACCEPTANCE.md; no temp, logs, or build artifacts.
- [x] Language audit: English only; no CJK or mixed-script content.
- [x] Claims audit: all gate check claims verifiable against file contents.

## Install-First Success Path

- **Input:** User says "I need to drop off paperwork at a government office by 4pm today."
- **Steps:**
  1. Agent reads SKILL.md and asks for recipient address, hours, deadline, document list, originals vs. copies, and transportation.
  2. Agent inventories documents, verifies recipient details, prepares the packet checklist, and builds a time-blocked route with a latest-leave time.
  3. Agent assembles the full drop plan with proof-of-delivery checklist, fallback steps, and post-drop log.
- **Output:** A complete Same-Day Document Drop Plan with drop mission snapshot, recipient verification, document inventory, packet prep checklist, time-blocked route, proof checklist, fallback plan, and post-drop log — all without legal advice or official acceptance guarantees.

## Review Status

- Implemented by: Golden Bean / coder
- Date: 2026-05-11
- Status: Ready for cross-review and test.
