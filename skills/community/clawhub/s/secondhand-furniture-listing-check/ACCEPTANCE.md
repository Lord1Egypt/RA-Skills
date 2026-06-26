# Acceptance Criteria - Secondhand Furniture Listing Check

## Gate Checks

- [x] `SKILL.md` exists and contains a prompt-only workflow.
- [x] `skill.json` is valid JSON and declares `version=1.0.0`, `license=MIT-0`, `language=en`, and `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] Public-facing documentation is English only.
- [x] No executable code, scripts, package files, network calls, APIs, credentials, secrets, or private data are included.
- [x] Trigger scenario, concrete deliverable, workflow, output format, and safety boundary are explicit.
- [x] The workflow produces a seller question script, photo checklist, measurement box, risk flags, pickup readiness card, and open questions.
- [x] The skill warns about pests, unsafe meetups, recalls, and hygiene concerns.
- [x] The skill avoids legal advice, valuation claims, authentication claims, guarantees, and accusations against sellers.
- [x] No CJK characters are present.

## Clean Scan Evidence

Verify the skill directory contains exactly these files with no unexpected artifacts:

| File | Expected | Check |
|---|---|---|
| SKILL.md | Present, English, YAML frontmatter with name/description | ✅ |
| skill.json | Valid JSON, version 1.0.0, license MIT-0, language en, hasExecutableCode false | ✅ |
| ACCEPTANCE.md | Present, English, gate checks documented | ✅ |
| Extras | No executable scripts, package files, .env, credentials, logs, temp files, or network configs | ✅ |

Scan command: `find . -type f | sort` → exactly 3 files.

## Install-First Success Path

1. **Input:** User says "I found a used couch online. What should I ask before pickup?"
2. **Steps:** The skill guides the assistant to: (a) capture listing basics (item type, location, price, condition), (b) check fit against doorways/stairs/vehicle, (c) request better evidence with a photo checklist, (d) build seller questions (age, repairs, odors, pests), (e) flag hygiene and pest risks for upholstered items, (f) plan pickup safely (daylight, bring help, share plan), (g) prepare transport tools and supplies, (h) create a go/no-go card.
3. **Output:** A readiness sheet with listing snapshot, seller script, photo checklist, fit and transport box, risk flags, pickup readiness card, and open questions. The user can immediately message the seller and plan a safe pickup.

Expected first-run outcome: The user has a complete checklist to evaluate the couch before committing to pickup, with safety and hygiene risks clearly flagged.

## Scope

- Prompt-only MVP.
- Local implementation only.
- Not published to ClawHub in this phase.

## Review Status

- Implemented by: Golden Bean / coder
- Date: 2026-05-11
- Status: Ready for cross-review and test.
