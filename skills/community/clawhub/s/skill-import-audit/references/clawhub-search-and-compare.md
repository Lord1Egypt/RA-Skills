# ClawHub Search & Candidate Comparison

Use when about to install or build audit/vetting skill tooling and the registry should first be checked for what exists (the import-audit pre-phase). The full search-and-compare workflow is **skill-import-harvest** (dimensions → search → triage → quality check → report → install gate); this file is its condensed data source.

## Search
- `clawhub search <query>` — run 8–12 varied query terms (synonyms + dimension words: "skill audit", "security audit", "skill security", "skill vet", "malware scan", "supply chain skill", "trust skill", "skill import"). One query misses whole families.
- Result rows are `slug  @owner  displayName  installs/60d`. Slugs can be DUPLICATED across owners — duplicates appear as separate rows.
- `clawhub inspect` has no `--owner` flag; for duplicated slugs use the `@owner/slug` form: `clawhub inspect @owner/slug --json`.

## Inspecting a candidate (what the JSON actually contains)
- `clawhub inspect <slug-or-@owner/slug> --json`: top-level keys are `file`, `version` (null unless a non-latest version is selected), `latestVersion` (only `changelog`/`createdAt`/`license`/`version` — no versionId), `moderation` (structured verdict: `verdict`, `isSuspicious`, `isMalwareBlocked`, `reasonCodes`, `engineVersion`, `updatedAt`), `owner`, `skill` (contains the full stored SKILL.md in `description`, plus the install `stats`), `versions`. The plain JSON has NO file listing or hashes.
- `--files` (text output): file listing with names, sizes, SHA-256 hashes, plus a "Security" line. This is the script inventory — tells you prompt-only (markdown only) vs script-driven. Caveat: the text "Security" line can DISAGREE with the JSON `moderation.verdict` for the same check (observed: text `SUSPICIOUS` vs JSON `clean` at identical check timestamps) — the JSON is the structured record.
- `--version` / `--tag` inspect a non-latest version.

## Capability matrix (how to compare without reading 70KB into context)
1. Dump each candidate's normalized `skill.description` to a scratch file (one `=== name ===` section per skill).
2. Define dimension columns from the user's spec (e.g. security, portability/hardcoded-paths, correctness/claims, pre-install scope, report format); grep each section for dimension keywords and emit a Y/– matrix. Do NOT read the whole blob.
3. Classify each candidate: prompt-only vs script-driven (file listing), network behavior (external-oracle / "submission" models — read the latest changelog line; a privacy/consent change is a data-flow signal), and the registry's own `moderation.verdict`.
4. Present options: adopt (name the closest), hybrid (adopt the best CLEAN candidate for the part it covers + build the gap), or build our own. The empty columns of the matrix are the argument for building.

## Rules
- A candidate's own registry security verdict is data, not a verdict: well-built audit skills have been flagged suspicious, and a clean flag is not proof. Treat "flagged" as an extra scrutiny step, never as disqualification — and never treat clean as passing.
- A flagged candidate is still readable for reference (patterns, threat taxonomies); the flag means it must not be EXECUTED on this machine.
- A skill that phones home to an external scoring oracle sends data off the machine — weigh its disclosure against the user's standard (no data leaves the machine without the user knowing).
