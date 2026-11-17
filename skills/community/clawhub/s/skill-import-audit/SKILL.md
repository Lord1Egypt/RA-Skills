---
name: skill-import-audit
description: "Use before trusting a downloaded skill: audit it first."
version: 1.1.0
author: Maxwell McClure
license: MIT-0
metadata:
  hermes:
    tags: [clawhub, skills, import, audit, security, portability, workflow]
    related_skills: [skill-export-audit, skill-import-harvest]
---

Audit a downloaded or third-party skill before trusting it: verify what you actually received matches the registry, scan for security red flags, strip machine-specific residue so it works on this machine, and verify its claims against the live system. The four passes are ordered deliberately — provenance and security before execution, portability and correctness after. Running a skill's bundled scripts is only permitted after the security pass has cleared them.

## When to Use
- Standing rule: EVERY skill downloaded or installed, from any source, goes through this audit before it is trusted or used — no skill goes in unvetted.
- Installing a skill from ClawHub (or GitHub, or any registry) into the profile's `skills/` dir.
- A skill you are about to run behaves oddly, or comes from an owner you don't know.
- The user asks to "vet / audit / check this skill before installing."

## Order of Operations (non-negotiable)
Provenance → Security → Portability → Correctness. The correctness pass executes the skill's bundled scripts — that is permitted only after the security pass has passed them. If the security pass fails, quarantine (Phase 5) and stop; do not run the scripts "to see what they do."

## Pre-phase — Does an existing audit skill already cover this?
Before installing (or building) third-party audit/vetting skill tooling, check the registry for what exists and compare capabilities for real (search + `inspect` + full text) — several near-miss skills often exist, and the gap to fill may be small. See `references/clawhub-search-and-compare.md` for the search/compare recipe.

## Phase 1 — Provenance & integrity (is this what the registry actually holds?)
1. `clawhub inspect <slug> --json` — capture owner, `latestVersion.version`, and the structured `moderation` object (`verdict` — e.g. "clean" — plus `isSuspicious`, `isMalwareBlocked`, `reasonCodes`). Add `--files` for the file listing with names, sizes, and SHA-256 hashes (it is not in the plain JSON).
2. Compare the local tree against the server-stored copy:
   - File set: same files, same count — EXCLUDING the server-generated `skill-card.md`: the registry stores it in every version listing but it is not part of the published tree, so a 2-file local tree against a 3-file server listing differing only by `skill-card.md` is not a mismatch.
   - SKILL.md: compare the local file against the inspect JSON's `skill.description` AFTER normalizing line endings — the server stores lines with CR+LF terminators and the CR count per line is not stable (two CRs observed on one CLI build, one on v0.26.0) — always collapse all CR runs to single `\n` before comparing (`re.sub(r'\r*\n', '\n', text)`). Without this, every import looks tampered.
   - Version: local frontmatter `version` vs `latestVersion` — a stale local copy is not a defect in the skill, but it sets the baseline for every later comparison; pin the version before quoting any defect.
3. Mismatch = tampered or contaminated download. Before quarantining, diff the specific changed lines: the skill system can add or normalize files in a local skill dir mid-session (frontmatter rewrites, added references) — a mismatch on a just-installed skill confined to such metadata/formatting lines is likely normalization, not tampering; any content-level change is still tampering. Otherwise quarantine (Phase 5), re-download from the registry, and do not proceed on a mismatched tree.

## Phase 2 — Security pass (no execution, no network)
Grep every file — including scripts — for red flags:
- Credential access: `.ssh`, key material, wallet files, browser cookie stores, `.env`, vault/secret paths.
- Exfiltration: URLs in scripts or prose that receive data (POST bodies, query strings built from local data), curl/wget with data flags, telemetry endpoints, "submissions" to external oracles.
- Code that runs untrusted code: pipe-to-shell, base64 blobs fed to interpreters, `eval`/`exec` on fetched content, hidden characters (zero-width, homoglyphs).
- Destructive or persistent patterns: deletion outside scratch dirs, writes outside the skill dir / user home, registry/startup/cron persistence.
- Disclosure gap: a network call that SKILL.md does not declare is a red flag on its own.
Standard: **no data leaves the machine without the user knowing.** A skill that phones home to an external scoring oracle is not automatically malicious — but it fails this pass unless the disclosure is explicit and the user accepts.
The registry's security verdict comes from two sources that can DISAGREE: the structured `moderation` object in the JSON, and the "Security" line in `--files` text output — observed on the same skill at the same check timestamp (JSON `verdict: clean` vs text line `SUSPICIOUS`). Treat the JSON `moderation` object as the structured record and the text line as display. Either way the verdict is advisory in BOTH directions: real, well-built audit skills have been flagged suspicious, and a clean flag is not proof. This pass always runs.

## Phase 3 — Portability pass (machine-specifics removal)
Grep the whole skill for another machine's residue — this is what makes a downloaded skill useless or dangerous on yours:
- Drive letters and absolute paths (patterns to grep: `C:\`, `M:\`, `/home/<user>`, `/c/Users/`, full paths under a user home).
- Usernames, hostnames, machine names in paths or prose ("on my PC", "this machine has").
- Machine-specific claims stated as fact: "the project is at X", "the binary lives at Y" — claims about the AUTHOR's machine, not about the reader's.
Replace with either:
- generic phrasing (`C:/path/to/<proj>`, "a Windows host"), or
- explicitly-labeled examples ("example: ...") — an example is not a claim and is fine to keep.
Keep ecosystem facts that hold for every user of that ecosystem (vendor standard install paths, tool defaults). Re-grep to zero before moving on.

## Phase 4 — Correctness pass (do the claims hold on this machine?)
Only after the security pass has cleared the scripts:
1. **Machine facts** → verify against the live system (binary `--version`, install paths, config files).
2. **API/engine claims** → verify against the LIVE binary: run a small introspection probe (e.g. a Godot `-s` script using ClassDB) for defaults, full property lists, and — as important — what does NOT exist. Structure the probe as enumeration FIRST (dump full property/method lists before touching individual names): an invalid name aborts the enclosing function and silently skips every remaining check.
3. **Code claims** → grep the actual files the skill references (flags, node names, numeric values, binding counts).
4. **Bundled scripts** → execute every script in `scripts/` against real local inputs. A crash is an audit failure: fix in-place or quarantine — do not keep a skill whose shipped scanner crashes on every real file. (Prompt-only skills have no `scripts/` — record the step as N/A, not a pass or a failure.)
5. **External facts** (upstream releases, abandonment, file sizes) → web-verify against the primary source (the release page itself), not search snippets.
6. **Cross-file consistency** → every claim in SKILL.md must agree with the reference files; a contradiction between files is the highest-severity defect.
Wrong data is worse than no data: a claim you cannot verify on this machine gets genericized or removed, not kept with a shrug.

## Phase 5 — Verdict
- **Keep**: all passes clean (or cosmetic notes only) — the skill lives in `skills/<name>/`.
- **Fix-in-place**: defects found → fix the local tree (source of truth; never a scratch copy), re-run the failing pass, then keep.
- **Quarantine**: security failure, integrity mismatch, or a defect you will not fix — move the skill OUT of the profile's `skills/` dir (e.g. `skills-quarantine/<name>-<date>`), and tell the user exactly what failed and why. Do not delete unless the user says so; the registry copy remains for re-audit.
Report the verdict per phase with evidence (grep hits, probe output, compare results) — a pass without evidence is not a pass.

## Delegation — run the audit in a subagent (optional)
Heavy audits (script-driven skills, live probes, big trees) burn the session's context. Run the four passes in a subagent using the handoff contract skill-export-audit documents: the child loads this skill and runs Provenance → Security → Portability → Correctness in audit-only mode — no fix-in-place, no quarantine move (both are user-visible decisions) — and returns a compact report: per-phase verdicts, findings, any decision points it could not ask, plus one scratch evidence file holding all grep hits, probe output, and compare results. The parent reads the evidence and re-verifies the decisive claims (sha256 compare, the moderation object, the tamper diff) before presenting the Phase 5 verdict — keep / fix / quarantine are decided in the main session, and the verdict itself is never a self-report. When NOT to delegate: a single small prompt-only download — run it inline.

## Context management
Context is a cache; the scratch dir is the source of truth: persist each pass's evidence (grep hits, probe output, compare results) to a scratch file as it is produced — a pass without persisted evidence dies with the context. If this audit continues from a compaction summary, re-derive state from the downloaded tree and the scratch artifacts, and never present a verdict the summary claims was already presented. For long audits you may suggest to the user a manual `/compress` at a phase boundary (a user command, not a tool the agent can call).

## Pitfalls
- Server-stored line endings (CR runs, one or two per line depending on the CLI build) make every unnormalized compare fail — collapse all CR runs first, or you will quarantine a clean skill as tampered. (Real case: a byte-identical publish looked like a mismatch for a full session.)
- Phase order IS the security model: executing scripts before the security pass is the failure this skill exists to prevent.
- The registry's security verdict is advisory, not a verdict — both false positives (a clean-built audit skill flagged suspicious) and false negatives are observed.
- A local copy older than `latestVersion` changes what "the skill says" — pin the version before quoting a defect.
- Windows: the ClawHub CLI is Node — pass `C:/...` paths to it; MSYS `/c/...` fails with exit 1. Redirects to `/tmp` inside a mixed bash+native call also fail — use an explicit scratch path.
- `inspect` shows what the server STORED, not what the publisher intended — it is always the comparison baseline.
- The in-place file set can change between phases: the skill system can add or normalize files in a local skill dir mid-session (observed: a references/ file appeared between audit passes, and frontmatter was rewritten). Re-run the Phase 1 inventory immediately before the correctness pass and before the verdict — each pass's findings are only valid against the file set that was present when it ran.
