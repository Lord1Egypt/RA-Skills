# Acceptance Checklist

- [x] SKILL.md has valid YAML frontmatter.
- [x] skill.json is present and valid JSON.
- [x] Version is 1.0.0 and license is MIT-0.
- [x] Language is English only.
- [x] Prompt-only metadata is present: promptOnly true, hasExecutableCode false, requires_api false, no_code_execution true, execution noExec.
- [x] No executable code, scripts, package files, automation hooks, API requirements, credential needs, or network requirements.
- [x] Directory contains exactly SKILL.md, skill.json, and ACCEPTANCE.md.
- [x] Boundary reminds users to remove personal data while avoiding credential handling, private file review, unlock bypassing, and account recovery.
- [x] Boundary avoids data-recovery promises, certified destruction claims, secure-erasure guarantees, repair diagnostics, resale valuation, and recycler acceptance promises.
- [x] Deliverable is a sort list plus wipe/remove/accessory/battery/packing checklist.
- [x] Workflow covers inventory, data-bearing device separation, data-removal reminders, battery and hazard sorting, accessory matching, destination rule checks, and final packing.
- [x] Slug matches the accepted design: small-electronics-recycling-prep.

## Clean Scan Evidence

- [x] Secrets scan: no API keys, tokens, passwords, or credentials found.
- [x] Executable scan: no scripts, binaries, or executable code present.
- [x] Network scan: no outbound calls, fetch, or API endpoints.
- [x] File audit: only SKILL.md, skill.json, and ACCEPTANCE.md; no temp, logs, or build artifacts.
- [x] Language audit: English only; no CJK or mixed-script content.
- [x] Claims audit: all gate check claims verifiable against file contents.

## Install-First Success Path

- **Input:** User says "Sort this drawer of old phones, cables, and remotes into a recycling prep list."
- **Steps:**
  1. Agent reads SKILL.md, asks for device types, counts, whether items may contain personal data, battery types, accessories, and intended destination.
  2. Agent inventories the pile, separates data-bearing devices, creates data-removal reminders, sorts batteries and hazards, matches accessories, and checks destination rules.
  3. Agent produces the Pile Snapshot, Sort List, Data Removal Reminders, Battery and Safety Check, Accessory Match, Pack Map, Confirm Before Drop-Off list, and Carry-Out Checklist.
- **Output:** A one-page electronics recycling prep card with a sort list separating data-bearing, battery-sensitive, and ready-to-recycle items — plus data-wipe reminders, accessory matching, pack-by-bag labels, and a carry-out checklist — all without asking for passwords or promising secure erasure.
