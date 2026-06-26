# Case Study: Cruise Intelligence Migration

> A real EXISTING-mode run of `slim-claude-md`. Read this in EXISTING mode before proposing your section→destination map. Use it as a reference for shape, not a literal template — every project's mapping will differ.
>
> **⚠️ Historical note:** This case study describes the *old* approach where CLAUDE.local.md held inline credentials. The current recommended pattern uses env var name references instead. The structural migration steps (extracting content, creating docs/) are still valid — just don't follow the credential-inlining pattern shown here. See the updated `CLAUDE-local-template.md` for the current approach.

## Problem state (before)

The project had grown for ~6 months and CLAUDE.md had become a journal:

| Metric | Value |
|--------|-------|
| `CLAUDE.md` lines | **2,275** |
| `CLAUDE.md` size | **96 KB** |
| Eager-loaded tokens per session | **~25K** (about 12% of context window before user typed anything) |
| Production DB connection strings in CLAUDE.md (tracked) | **3** (staging, canary, production — all live passwords) |
| FalkorDB credentials in CLAUDE.md | **3** (one per env, plaintext) |
| GitHub PAT in `~/.claude/CLAUDE.md` global | **1** |
| Sections | 19 top-level `##` sections, many with multi-page deep dives |
| "Updated 2026-XX-XX" markers scattered through file | dozens |
| Stat tables that had silently rotted | several (entity counts from old pipeline runs) |

User-reported pain points:
1. **Context bloat** — every session burned a quarter of working memory on the same wall of text.
2. **Sessions losing environment context** — when sessions got compacted or restarted, Claude forgot which DB URL belonged to which environment and either asked the user or pointed at the wrong one. Production DB URLs lived inside the tracked CLAUDE.md, so removing them risked losing them entirely.

## Mode chosen

EXISTING mode (CLAUDE.md was substantial, project was mid-life). Goal: reproduce the slim structure without losing any information and without checking secrets into git.

## Pre-flight audit

Single Explore subagent run gathered:

- `.gitignore` already covered `.env` and `.env*.local` but NOT `CLAUDE.local.md`
- `.claude/` only contained `settings.local.json`
- `docs/` was flat — 28 markdown files, no subdirectories, including 8 `SESSION-RECAP-*.md` files cluttering the root
- `.env.example` (49 lines) and `docs/RAILWAY-ENV-VARS.md` (5.9 KB) already existed and were good non-secret reference files — kept as-is
- No existing `CLAUDE.local.md`

## Section → destination map

The 19 sections of the original CLAUDE.md mapped to:

| Original section | Destination |
|---|---|
| Business Context, Founder Context, Revenue Model | `docs/BUSINESS-CONTEXT.md` |
| Tech Stack, Project Structure, Local Dev | `docs/architecture/overview.md` |
| Database (counts, key tables, schema rules) | `docs/architecture/database.md` |
| Authentication (NextAuth, IATA flow) | `docs/architecture/auth.md` |
| Caching Architecture | `docs/architecture/caching.md` |
| Rating Systems formulas | `docs/architecture/rating-systems.md` |
| AI Chat System (pipeline, tools, tiers, costs) | `docs/features/ai-chat.md` |
| Knowledge Graph (FalkorDB, profiles, sync) | `docs/features/knowledge-graph.md` |
| Route Corridor Intelligence | `docs/features/route-corridors.md` |
| UI Features (a giant section) | split into `docs/features/{ui,blog,social-media,route-maps,ship-images}.md` |
| Stripe Billing | `docs/features/billing.md` |
| Support System (FreeScout) | `docs/features/support.md` |
| Data Pipeline (10 phases) | `docs/pipeline/README.md` |
| Scraper Worker | `docs/pipeline/scraper-worker.md` |
| Differential Sync v3 | `docs/pipeline/sync-v3.md` |
| Scripts Reference (~80 scripts) | `docs/scripts/README.md` |
| Troubleshooting | `docs/TROUBLESHOOTING.md` |
| **Railway Environments** (full URLs and credentials) | **`CLAUDE.local.md`** (gitignored) |
| **Stat tables** (844 ships, 107K itineraries, etc.) | `docs/STATE-SNAPSHOT.md` (single dated file, not edited in place) |
| **"Updated YYYY-MM-DD" markers and narrative changelogs** | Deleted entirely — git history covers this |

What stayed in slim CLAUDE.md (the load-bearing minimum):
- Hard rules (snake_case in raw SQL, `Prisma` namespace import, default-to-staging, dry-run mandate, destructive-op approval rule, FalkorDB `closeFalkorDB()` requirement, Redis vs FalkorDB distinction)
- Branch → environment topology table (no secrets)
- "Where to find things" pointer index (24 pointers)
- 5 common commands
- 4-bullet "Today's state"
- The full housekeeping protocol
- A 4-step session protocol

## Execution sequence

The migration ran as a 9-step task list mirroring Section B of the SKILL.md:

1. Read full CLAUDE.md in chunks (2,275 lines exceeded the default Read limit, used 4 chunked reads with explicit `offset`/`limit`)
2. Add `CLAUDE.local.md` to `.gitignore`
3. Create `CLAUDE.local.md` with all 3 envs' DB URLs, Redis URLs, FalkorDB credentials, GitHub PAT
4. Verify with `git check-ignore -v CLAUDE.local.md` (matched line 70)
5. `mkdir -p docs/{architecture,features,pipeline,scripts,recaps}`
6. `git mv` 7 tracked recaps + plain `mv` 1 untracked recap into `docs/recaps/`
7. Write 22 new doc files (5 architecture, 10 features, 3 pipeline, 1 scripts, 3 top-level)
8. Rewrite `CLAUDE.md` from 2,275 → 144 lines, inlining the housekeeping protocol verbatim
9. Verification suite

## Verification results

| Check | Result |
|-------|--------|
| `wc -l CLAUDE.md` | 144 (target: ≤ 300) ✅ |
| `git check-ignore -v CLAUDE.local.md` | matched `.gitignore:70` ✅ |
| `git status --short` shows CLAUDE.local.md? | NO ✅ |
| All 24 `docs/*` pointers in CLAUDE.md resolve | 24/24 ✅ |
| Secrets leaked into any new tracked file | 0 ✅ |
| Combined eager-loaded tokens (CLAUDE.md + CLAUDE.local.md) | ~4K (vs original 25K) — 84% reduction in eager context burn |

## Outcome (after)

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| `CLAUDE.md` lines | 2,275 | 144 | **−94%** |
| `CLAUDE.md` size | 96 KB | 9.6 KB | **−90%** |
| Eager-loaded tokens | ~25K | ~4K | **−84%** |
| Secrets in tracked files | 7 | 0 | **−100%** |
| Doc files in `docs/` | 28 (flat) | 51 (organized in 5 subdirs) | structured |
| Session recaps cluttering `docs/` root | 8 | 0 (moved to `docs/recaps/`) | clean |

## Commit sequence

The migration was committed in 3 logical chunks (the suggested 4-commit sequence collapsed to 3 because the recap moves and the new docs tree shared an index state and were cleaner together):

1. `chore: gitignore CLAUDE.local.md for local env credentials` — just `.gitignore`
2. `docs: split CLAUDE.md content into topical docs/ tree` — 33 files: 7 renames + 26 new files
3. `docs: slim CLAUDE.md to 144-line router with housekeeping protocol` — −2222 / +94 lines

Then `git push origin staging`. No secrets in the pushed history; `CLAUDE.local.md` invisible to git.

## Findings worth carrying to other migrations

1. **Pre-existing tracked files often have secrets too.** The `Grep` for connection strings turned up 5 other tracked files in this repo (session handoffs, plan docs, deploy checklists, and one app route file) that still had plaintext DB credentials. These were out of scope for the migration but flagged to the user. **Always run the secret-leak grep against the whole repo at the end and report any pre-existing leaks** — even if you don't fix them.

2. **`git mv` rename detection requires both halves staged at the same time.** When intermediate `git status` invocations refreshed the index, the staged renames became unstaged. The fix was to use `git add -A docs/` (which picks up both deletions and additions) rather than trying to stage paths individually. Lesson: don't poke the index between `git mv` and `git commit`.

3. **Untracked session recaps need plain `mv`, not `git mv`.** This project had 7 tracked recaps + 1 untracked one. `git mv` on the untracked one errors out. Branch on `git ls-files --error-unmatch` to decide which to use.

4. **Stat tables decay silently.** The original CLAUDE.md had counts that referenced "the April 4 pipeline run" but the file had been edited 3 days later without updating them. Moving stats to a single `STATE-SNAPSHOT.md` makes the staleness obvious because the file has one date at the top.

5. **The housekeeping protocol is what makes the structure last.** Without the 8-rule protocol explicitly inside CLAUDE.md, the next session would have started adding new feature deep-dives directly to the slim file and the rebloat would begin within a week. The protocol is the entire point — don't omit it.

6. **Defer commits to the user.** The migration produced a clean working tree of 22 changes and the user reviewed them before authorizing 3 commits and a push. Never auto-commit a documentation migration.
