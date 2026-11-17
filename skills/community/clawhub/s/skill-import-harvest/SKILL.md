---
name: skill-import-harvest
description: "Use when needed functionality may already exist online: search, quality-check, harvest data."
version: 1.1.0
author: Maxwell McClure
license: MIT-0
metadata:
  hermes:
    tags: [clawhub, skills, import, harvest, search, quality, workflow]
    related_skills: [skill-import-audit, skill-export-audit]
---

When the user needs functionality or domain knowledge, harvest what already exists in the community registry BEFORE building. Quality-check every candidate with the same discipline as skill-import-audit — but the output is **data with attribution, not an installed skill**. A candidate that perfectly reflects the need ends in an install question to the user; nothing is installed without their fresh explicit approval, and any install then goes through the full skill-import-audit.

## When to Use
- The user asks "does a skill for X exist?" or the task needs a capability this machine lacks.
- About to build a skill or workflow: check first what exists (avoid reinventing — the standing rule for hard problems).
- The user asks to "search the hubs / compare existing options."

## Step 1 — Requirements & dimensions
Extract from the request: the capability dimensions (e.g. security, portability, correctness) and the success bar ("perfectly reflects our need" = covers ALL of them). The dimensions become the columns of the comparison matrix. Write them down first — searching without columns is how you end up with a list instead of a verdict.

## Step 2 — Breadth search (the registry)
`clawhub search <query>` — run 8–12 varied query terms: synonyms + dimension words ("skill audit", "security audit", "skill vet", "malware scan", "supply chain", "trust skill" …). One query misses whole families. Result rows are `slug  @owner  displayName  installs/60d`; **slugs can be duplicated across owners** — duplicates appear as separate rows, and `clawhub inspect` has no `--owner` flag: use the `@owner/slug` form for ambiguous slugs. Install counts signal community trust, not correctness.

## Step 3 — Triage (depth without context bloat)
Per shortlisted candidate: `clawhub inspect <@owner/slug> --json` (the structured `moderation` object — TOP-LEVEL, not under `skill` — plus owner, `latestVersion`, and the full stored SKILL.md in `skill.description`) and `--files` (file listing with hashes → prompt-only vs script-driven; note the text "Security" line can DISAGREE with the JSON `moderation.verdict` for the same check — the JSON is the structured record). **Do not read all candidate descriptions into context**: dump each normalized `skill.description` to a scratch file (one `=== name ===` section per skill), then grep the dimension keywords per section and emit a Y/– capability matrix. The empty columns of the matrix are the argument for building.

## Step 4 — Quality check (the import-audit passes, data not code)
For every claim you intend to keep, run the import-audit discipline — but you are **harvesting data, not installing a skill**:
- **Security first**: the candidate's red flags determine how much its data is worth. A malicious or flagged skill's claims are suspect. Registry verdicts are advisory in BOTH directions (false positives and false negatives are both observed); a flagged candidate is still readable for reference (patterns, taxonomies) but must not be EXECUTED on this machine.
- **Portability (the harvest twist)**: import-audit *fixes* machine-specific residue in place; harvest *discards* it. Keep only machine-independent claims; the author's-machine residue (paths, usernames, "this machine has X") is genericized or dropped — it never transplants into our artifacts.
- **Correctness**: verify harvested claims against the live system before recording them. Wrong data is worse than no data — a harvested wrong claim becomes OUR wrong claim. Verify external facts against primary sources, not snippets.
- **Attribution (mandatory)**: every harvested item carries its source — `slug @owner vX.Y.Z, verified <date>` (the inspect `--files` hashes make the source re-checkable later). Unattributed harvests do not enter artifacts.

## Step 5 — Harvest report
Present: per candidate — coverage per dimension, what was harvested (attributed), what was rejected (and why); then the gap analysis (the dimensions no candidate covers). Close with the options: **(a)** adopt an existing skill that fully covers the need, **(b)** hybrid — build our own incorporating the harvested data, **(c)** build from scratch.

## Step 6 — Install gate (mandatory pause)
Only path (a) leads to installation, and only by asking the user: name the exact skill, version, and owner — "install `<slug>` @vX.Y.Z by @owner?" — and wait for **fresh explicit approval**. A prior "search for skills" request is NOT install authorization (the same discipline as the export stop-boundary). On approval, the install proceeds through the full **skill-import-audit** (provenance → security → portability → correctness → verdict): harvest triage is a pre-filter, not a substitute for the install audit. Nothing from the candidate touches `skills/` until that verdict is keep.

## Delegation — run the search and triage in a subagent (optional)
Steps 2–4 are the context-heavy core (8–12 searches, many inspect payloads, a 70KB candidate dump). Delegate them to a subagent: the child loads this skill, runs Steps 2–4 read-only (no Step 6 install gate — that is a user decision and stays in the main session), and returns a compact report: the dimension matrix, per-candidate keep/reject with attribution, the gap analysis, and the (a)/(b)/(c) options — with every candidate's full text in one scratch evidence file, never in the returned summary. The parent reads the evidence and presents the Step 5 report and options; the Step 6 gate always happens in the main session, on the presented evidence. When NOT to delegate: a single-query, single-candidate check — run it inline.

## Context management
The Step 3 candidate dump file is the source of truth: every matrix cell and harvest decision must be re-derivable from it alone. If this run continues from a compaction summary, re-derive the matrix from the dump file — never from the summary — and re-present the options: a harvest report the user never saw is not a report. For long harvests you may suggest to the user a manual `/compress` at a step boundary (a user command, not a tool the agent can call).

## Pitfalls
- Searching without dimension columns produces a list, not a verdict — Step 1 first, always.
- Reading every candidate's full description into context is how 70KB of markdown takes over the session — scratch file + grep matrix.
- Duplicated slugs: a bare `clawhub inspect <slug>` on an ambiguous slug is unreliable — use the `@owner/slug` form.
- High install counts are community signal, not a security verdict — the Step 4 passes still run.
- Harvested data without attribution is how unverifiable claims enter our artifacts — the exact failure the export-audit deletes.
- Flagged candidate ≠ unusable data; clean candidate ≠ trustworthy data — verdicts are advisory both directions, the passes decide.
