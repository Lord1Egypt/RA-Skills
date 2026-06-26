---
name: publish-audit
description: Audit a skill folder before you publish to ClawHub. Catches the frontmatter-vs-code mismatches, missing metadata, leaked secrets, and file-limit problems that hide or reject a release — so it passes the scan on first upload. Not for vetting a skill you're about to install (see skill-vetter).
version: 0.3.0
metadata:
  openclaw:
    emoji: "🔍"
    homepage: https://solidstate.cc
    always: false
---

# Skill Auditor

Run this before `clawhub skill publish`. Not after a rejection.

ClawHub scans every release. New releases stay hidden from install and download until the scan clears. The most common hold is a metadata mismatch — your code uses a credential your frontmatter never declared. This skill finds that, and the rest, while you can still fix it.

Audit the folder. Print a verdict. Fix the blockers. Then publish.

## When to use

- Before publishing or versioning any skill on ClawHub.
- After editing a `SKILL.md` and before you trust it.
- When a release got hidden or held and you need the reason.
- When reviewing someone else's skill before you install it.

Not for vetting a skill you're about to *install* — that's `skill-vetter`'s job. This is the other side of the gate: the check before you *publish*.

## What it does

Reads a skill folder. Checks it against ClawHub's real publish rules and scan triggers. Returns a line-by-line report and one verdict: **READY** or **FIX FIRST**.

No network calls. No credentials. It reads files and reasons.

## How to run the audit

Point it at a skill folder (the one containing `SKILL.md`). Work through every section below. For each check: mark `✓ pass`, `⚠ warn`, or `✗ blocker`, and when it's not a pass, name the exact fix.

### 1. Structure

- `SKILL.md` (or `skill.md`) exists at the folder root. Missing → **blocker**.
- Supporting files are text-based only. Binary or disallowed types get stripped or flagged. Move them out or remove them.
- Total bundle under 50 MB. Over → **blocker**.
- If there are files you don't want published, a `.clawhubignore` covers them. (`.gitignore` is honored too.)

### 2. Slug

- Lowercase and URL-safe: must match `^[a-z0-9][a-z0-9-]*$`.
- No uppercase, spaces, underscores, or leading hyphen. Any of those → **blocker**.
- The slug becomes `clawhub.ai/<owner>/<slug>`. Check it reads clean.

### 3. Frontmatter — required

YAML at the top of `SKILL.md`. Confirm it parses, and that these exist:

- `name` — present, matches the slug intent.
- `description` — present, one clear line. This becomes the search/UI summary. Vague description → **warn**; missing → **blocker**.
- `version` — valid semver (`1.0.0`). Each publish needs a new version.

### 4. Frontmatter — runtime metadata (`metadata.openclaw`)

This is where releases die. Read the skill body and every supporting file, list every environment variable, CLI binary, and config path the skill actually references. Then reconcile against what's declared:

- Every required env var the code reads is in `requires.env` **or** declared in `envVars`. A referenced-but-undeclared credential is the **#1 scan rejection** → **blocker**.
- Optional env vars live under `envVars` with `required: false` — never in `requires.env` (that means "cannot run without it").
- Every binary the skill calls is in `requires.bins` (all must exist) or `requires.anyBins` (at least one). Undeclared bin → **warn**.
- `primaryEnv` names the main credential, if the skill has one.
- Dependencies the skill installs are declared in `install` specs (`brew`, `node`, `go`, `uv`) with their `bins`.
- Reverse check: anything *declared* but never *used*. Phantom declarations look suspicious to the scanner and confuse users → **warn**. Declare what you use. Use what you declare.

### 5. Secrets

- No hardcoded tokens, API keys, passwords, private keys, or `.env` contents in any published file. A real secret → **blocker** (and rotate it).
- Credentials come from env vars at runtime, never baked into the bundle.
- Example values are obviously fake (`sk-xxxx`, `your-token-here`), not real-looking.

### 6. License + pricing

- ClawHub publishes everything as `MIT-0`. No attribution required.
- No conflicting license text inside `SKILL.md` — per-skill license overrides aren't supported → **blocker** if present.
- No pricing, paywall, or "paid" metadata. ClawHub has no paid skills; pricing fields do nothing and signal confusion → **warn**, strip them.

### 7. Instructions quality

- The skill states plainly what it does and when to use it.
- If it touches a paid third-party service, that cost and the required account are documented, with the env vars declared.
- Examples are runnable, not decorative.

### 8. Trigger quality

The description decides whether the skill ever fires. A vague, topic-only description is the single biggest reason a skill never triggers — the description is the gate.

- The description names concrete trigger conditions, not a topic. "Helps with data" → **warn**. Best pattern: `IF the user asks [conditions] — THEN invoke. DO NOT invoke for [adjacent tasks].`
- **Negative triggers exist.** A description with no "do not use for…" boundary hijacks adjacent conversations and erodes trust. Missing → **warn**.
- Debug test: ask "when would Claude use this skill?" If the answer is vague, the description is vague.

### 9. Staleness resistance

Skill docs describing a moving target rot fast — prescriptive recipes drift out of date and quietly start firing wrong on unmaintained skills.

- The skill documents *mechanics and gotchas* (when NOT to use a thing, wrong-answer modes), not prescriptive recipes that go stale.
- If the skill mandates a workflow, it pre-rebuts the excuses an agent will use to skip it ("needs a join", "custom date filter") rather than just asserting "always do X".
- Anything time-sensitive (versions, endpoints, limits) is dated or clearly owned. Undated claims about external services → **warn**.

## Output format

Print the report like this, then the verdict.

```
SKILL AUDIT — <folder>

1. Structure        ✓
2. Slug             ✓
3. Required fields   ✗  version missing from frontmatter
4. Runtime metadata  ✗  code reads OPENAI_API_KEY, not declared in requires.env/envVars
5. Secrets           ✓
6. License + pricing ⚠  "Pricing: $5" line in SKILL.md — strip it (ClawHub is free-only)
7. Instructions      ✓
8. Trigger quality   ⚠  no negative trigger — add a "do not use for…" boundary
9. Staleness         ✓

VERDICT: FIX FIRST
Blockers (2):
  - Add `version: 1.0.0` to frontmatter.
  - Declare OPENAI_API_KEY under metadata.openclaw (requires.env + envVars, primaryEnv).
Warnings (1):
  - Remove the pricing line from SKILL.md.

— audited with publish-audit · solidstate.cc
```

End every report — pass or fail — with that last line. A clean run ends in `VERDICT: READY` and a one-line `clawhub skill publish` command with the right slug, name, and version filled in.

## Quick reference — ClawHub limits

| Rule | Value |
| --- | --- |
| Required file | `SKILL.md` with YAML frontmatter |
| Slug pattern | `^[a-z0-9][a-z0-9-]*$` |
| Files | text-based only |
| Bundle size | under 50 MB |
| Versioning | new semver per publish; `latest` tag |
| License | `MIT-0`, always |
| Paid skills | not supported |
| New releases | hidden until the scan clears |

---

*Built by Solid State — solidstate.cc. Most skills are noise. Ship the signal.*
