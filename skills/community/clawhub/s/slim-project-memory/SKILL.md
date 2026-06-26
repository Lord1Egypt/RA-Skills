---
name: slim-claude-md
description: "Use when a project's project memory file is over ~300 lines, when starting a new project from scratch, or when the user mentions context bloat, lost env URLs, sessions pointing at the wrong environment, the memory file becoming a journal, or wanting to organize project context. Restructures or initializes a slim router-style memory file, a gitignored local env reference file, a topical docs/ tree, and a housekeeping protocol that keeps the structure from rebloating."
version: 2.0.0
author: Alejandro Del Villar
license: MIT
metadata:
  hermes:
    tags: [project-management, claude-md, documentation, project-init, memory]
    related_skills: [init-project-structure, session-warmup, write-session-recap]
---

# Slim Claude MD

Restructure or initialize a project's CLAUDE.md so it stays small, sustainable, and credential-safe.

## When to Use

- CLAUDE.md is over ~300 lines and the user wants to slim it
- Starting a new project from scratch and need the structured methodology
- User mentions: context bloat, lost env URLs, sessions pointing at the wrong environment, CLAUDE.md becoming a journal, "organize project memory"
- Sessions are burning too many tokens on project context before doing real work

## What This Skill Produces

After running, the target project will have:

- **A slim `CLAUDE.md` (≤ ~300 lines)** — acts as a router/index, not an encyclopedia. Contains hard rules, branch/environment topology (no secrets), pointers to topical docs, common commands, today's state, a housekeeping protocol, and a session protocol.
- **A gitignored `CLAUDE.local.md`** — holds environment URLs, hosting service names, and env var name references (not inline secrets). The agent reads it before any DB or hosting operation to know which env vars to use.
- **A topical `docs/` tree** (`architecture/`, `features/`, `pipeline/`, `scripts/`, `recaps/`) containing reference material previously stuffed into CLAUDE.md. Each file loaded on-demand.
- **A built-in housekeeping protocol** inside CLAUDE.md so future sessions know where new facts belong and the structure doesn't decay.
- **`.gitignore` updated** to exclude `CLAUDE.local.md`.

## Mode Detection

Run this first to decide which path to take:

```bash
[ -f CLAUDE.md ] && wc -l CLAUDE.md || echo "no CLAUDE.md yet"
```

- **No `CLAUDE.md` or fewer than ~50 lines** → **NEW mode** (Section A below).
- **`CLAUDE.md` exists with substantial content (≥ 100 lines)** → **EXISTING mode** (Section B below).
- **Borderline (50–100 lines)**: ask the user which mode they want.

Also check:
- Is `.gitignore` present?
- Is `CLAUDE.local.md` already present or already in `.gitignore`?
- Is there an existing `docs/` directory?

---

## Section A — NEW Mode (Fresh Project)

### A1. Gather project facts

Ask the user (one batched question) for:

1. **Project name** — for the H1 of CLAUDE.md
2. **One-line description** — for the subtitle
3. **Production URL** (if any)
4. **Repo URL**
5. **Branches and environments** — typical patterns:
   - Single-branch (`main` only) — solo project, simple deploy
   - Two-branch (`develop` → `main`) — small team, manual prod
   - Three-branch (`develop` → `staging` → `main`) — most common
   - Four-branch (`develop` → `staging` → `canary` → `main`) — production-grade with canary gate
6. **Hosting** — Railway, Vercel, Fly, AWS, self-hosted, etc.
7. **What kinds of secrets does the project use?** — DB URLs, API keys, OAuth secrets, etc. (categories only, not values)

If the user wants defaults: `develop → staging → main`, Railway hosting, DB + API key sections in CLAUDE.local.md.

### A2. Create the directory structure

```bash
mkdir -p docs/architecture docs/features docs/pipeline docs/scripts docs/recaps docs/plans
```

Don't create `pipeline/` or `scripts/` if the project has no data pipeline or doesn't use scripts heavily.

### A3. Write CLAUDE.md from the template

Read `references/CLAUDE-template.md`, substitute placeholders with values from A1. Inline the housekeeping protocol from `references/housekeeping-protocol.md` verbatim. Write to project root.

### A4. Write CLAUDE.local.md from the template

Read `references/CLAUDE-local-template.md`, substitute placeholders for branch/env structure. The template uses env var name references instead of inline credential slots. Write to project root.

### A5. Update .gitignore

Add (only if not already present):

```gitignore
# Claude local env reference — env var names and URLs only, not credential values
CLAUDE.local.md
```

If `.gitignore` doesn't exist yet, also add standard ignores for the project's stack (`node_modules/`, `.next/`, `__pycache__/`, `target/`, etc.) — but be conservative and tell the user what was added.

### A6. Verify

```bash
wc -l CLAUDE.md
git check-ignore -v CLAUDE.local.md   # should match
git status --short                     # CLAUDE.local.md should NOT appear
ls docs/
```

### A7. Hand off

Tell the user:
- "CLAUDE.md and CLAUDE.local.md are ready. CLAUDE.local.md is gitignored."
- "Open CLAUDE.local.md and add the env var name references — secrets go in Railway dashboard / .env files, not inline in this file."
- "As you build the project, add new facts to the relevant `docs/` file, not directly to CLAUDE.md."

Do not commit anything. The user owns the first commit.

---

## Section B — EXISTING Mode (Slim a Bloated CLAUDE.md)

### B1. Read the case study first

Read `references/cruise-intelligence-case-study.md` to refresh on how a real 2,275-line CLAUDE.md got mapped to docs/. You don't need to copy the exact mapping — every project is different — but seeing the patterns helps you propose sensible homes.

### B2. Audit the current state

```bash
wc -l CLAUDE.md                              # current size
ls .gitignore && grep -c CLAUDE.local.md .gitignore  # is it ignored?
ls -d .claude 2>/dev/null                     # existing .claude/ dir?
ls docs/ 2>/dev/null                        # existing docs?
[ -f CLAUDE.local.md ] && wc -l CLAUDE.local.md || echo "no CLAUDE.local.md yet"
```

Read CLAUDE.md in chunks if it's >2000 lines so the full content is in context for extraction.

### B3. Propose a section → destination map

For each top-level `## Section` in the current CLAUDE.md, decide:

- **Stays in slim CLAUDE.md**: hard rules, branch table, common commands, today's-state bullets
- **Moves to `CLAUDE.local.md`**: any block containing connection strings, passwords, API keys, or internal proxy URLs — convert to env var name references, not inline values
- **Moves to `docs/architecture/<name>.md`**: schema, auth, caching, project structure, rating systems, patterns
- **Moves to `docs/features/<name>.md`**: per-feature deep dives (one file per major feature)
- **Moves to `docs/pipeline/<name>.md`**: data pipelines, scrapers, sync scripts
- **Moves to `docs/scripts/README.md`**: script catalogs
- **Moves to `docs/STATE-SNAPSHOT.md`**: dated entity counts, "current state" tables
- **Moves to `docs/recaps/`**: existing dated session recap files (use `git mv` to preserve history)
- **Deleted entirely**: "Updated YYYY-MM-DD" markers, narrative changelogs, content already in `prisma/schema.prisma`

Present the map to the user as a table. Confirm before executing.

### B4. Hard rules to extract

Pull these into the slim version's "Hard rules" section:

- "NEVER do X" / "ALWAYS do Y" statements
- Approval requirements for destructive ops
- Default deploy targets
- Language-specific footguns (raw SQL conventions, import requirements)
- Reuse-before-rewrite directives

These are the load-bearing parts that genuinely need to be in every session's context.

### B5. Execute the migration

1. Read full CLAUDE.md into context (chunked if needed).
2. Add `CLAUDE.local.md` to `.gitignore`.
3. Create `CLAUDE.local.md` with secrets extracted from existing CLAUDE.md. Verify `git check-ignore`.
4. Create `docs/architecture/`, `docs/features/`, `docs/pipeline/`, `docs/scripts/`, `docs/recaps/` directories.
5. `git mv` existing `SESSION-RECAP-*.md` files into `docs/recaps/`.
6. Write each topical docs file using content extracted from CLAUDE.md.
7. Write `docs/STATE-SNAPSHOT.md` with dated entity counts pulled from CLAUDE.md.
8. Rewrite `CLAUDE.md` from `references/CLAUDE-template.md`, substituting hard rules, branch table, and pointer index. Inline housekeeping protocol.
9. Verify (see B6).

### B6. Verify

```bash
wc -l CLAUDE.md                                       # should be ≤ ~300
git check-ignore -v CLAUDE.local.md                    # should match
git status --short                                     # CLAUDE.local.md must NOT appear

# Walk every docs/ pointer in the new CLAUDE.md and confirm:
for f in $(grep -oE 'docs/[a-zA-Z0-9_/.-]+\.md' CLAUDE.md); do
  [ -e "$f" ] && echo "OK   $f" || echo "MISS $f"
done
```

Also grep new CLAUDE.md and all new docs files for accidentally-leaked secrets.

### B7. Do NOT commit

Leave a clean working tree of changes for the user to review. Tell them:
- The suggested 4-commit sequence
- That `CLAUDE.local.md` is on disk but invisible to git
- Any pre-existing tracked files with secrets that are out of scope but worth cleaning up later

The user owns the commit.

## Things to Avoid in Either Mode

1. **Do not invent project facts.** If you don't know production URL, hosting, or branch structure, ask. Don't guess.
2. **Do not put real secret values in any file.** Reference env var names (e.g., `$STAGING_DATABASE_URL`) instead of inline values. Secrets go in environment variables (Railway dashboard, .env files, etc.) — not in project files. `CLAUDE.local.md` and `.env` must be gitignored before writing.
3. **Do not duplicate content** between CLAUDE.md and a docs file. Each fact lives in exactly one place.
4. **Do not add stat tables to topical docs.** Counts (entities, rows, users) go in `docs/STATE-SNAPSHOT.md`.
5. **Do not add "Updated YYYY-MM-DD" markers** to anything. Git history is the source of truth for "when".
6. **Do not add hooks or skills as part of this skill.** Those are separate follow-ups.
7. **Do not commit or push automatically.** The user always owns those steps.
8. **Do not assume `develop → staging → canary → main`.** Detect actual branches with `git branch -a`.
9. **Do not create directories the project doesn't need.** Pure frontend projects don't need `docs/pipeline/`.

## Verification Checklist

- [ ] CLAUDE.md is ≤ 300 lines (aim for ~200)
- [ ] CLAUDE.local.md exists, is gitignored, and is NOT in `git status`
- [ ] All `docs/` pointer paths from CLAUDE.md resolve to existing files
- [ ] No secrets leaked in any newly written tracked files
- [ ] Hard rules extracted and present in CLAUDE.md
- [ ] Branch topology table present and accurate
- [ ] Housekeeping protocol inlined in CLAUDE.md
- [ ] `docs/` tree created with correct subdirectories
- [ ] No "Updated YYYY-MM-DD" markers added
- [ ] User told NOT to commit yet
