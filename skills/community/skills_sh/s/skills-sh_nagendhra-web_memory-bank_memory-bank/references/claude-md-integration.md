# CLAUDE.md Integration Guide

## What is CLAUDE.md?

`CLAUDE.md` is a configuration file that Claude Code reads automatically at
the start of every session. By adding memory instructions here, Claude loads
your project context without you needing to ask.

You can place it:
- **Project-level:** `./CLAUDE.md` in your project root (one project)
- **Global:** `~/.claude/CLAUDE.md` (all projects, every session)

---

## Minimal Setup (5 lines)

The bare minimum to get memory working:

```markdown
## Memory

At session start, check for MEMORY.md and summarize where we left off.
At session end, update MEMORY.md with what we did and the next step.
```

This gives you basic load/save. No branch awareness, no diffing, no
compression — but it works.

---

## Standard Setup (Full v2.0)

Enable every feature:

```markdown
## Memory

At the start of every session:
1. Check for MEMORY.md in the project root
2. Check for ~/.claude/GLOBAL-MEMORY.md (global preferences)
3. Detect current git branch with `git branch --show-current`
4. Check for .memory/branches/<branch-slug>.md overlay
5. Run session diff: what changed since "Last updated" in MEMORY.md
6. Validate all Key Files paths still exist
7. Score memory health (freshness, relevance, completeness, actionability)
8. Greet me with a specific 2-3 sentence summary including:
   - Where we left off (current task and status)
   - Any drift detected (stale files, new commits, branch changes)
   - The next immediate step
   - Memory health score
9. Ask: "Ready to continue, or has the plan changed?"

During sessions:
- When I say "remember this" or complete a milestone, update MEMORY.md
- Track key decisions with reasoning in the Key Decisions table
- Save checkpoints every 60 minutes of active work

At session end (when I say "wrap up", "save", "done for now"):
1. Write comprehensive MEMORY.md with full current state
2. Ensure "Next immediate step" is crystal clear
3. Run compression if over 150 lines
4. Check if any cross-project patterns should go to GLOBAL-MEMORY.md
5. Confirm what was saved

Branch memory:
- On branch switch, check for .memory/branches/<branch>.md
- Keep branch-specific work in overlays, shared decisions in base MEMORY.md
- On branch merge, fold overlay into base and clean up
```

---

## Project-Level vs Global

### Project-level (`./CLAUDE.md`)

Best for: project-specific memory settings.

```
project-root/
  CLAUDE.md        ← memory instructions for this project
  MEMORY.md        ← this project's memory
```

Pros:
- Memory config lives with the project
- Team members get it automatically if committed
- Can customize per project (different compression thresholds, etc.)

### Global (`~/.claude/CLAUDE.md`)

Best for: enabling memory across all projects without setup.

Pros:
- One-time setup, works everywhere
- New projects automatically get memory
- Consistent behavior across all your work

### Both together

They stack. Global loads first, project overrides:

```
~/.claude/CLAUDE.md     → "Always check for MEMORY.md at session start"
./CLAUDE.md             → "Also run pnpm install as pre-flight check"
```

**Recommendation:** Put memory instructions in global CLAUDE.md, and
project-specific hooks (pre-flight checks, team protocol) in project CLAUDE.md.

---

## Integration with Existing CLAUDE.md

If you already have a CLAUDE.md with coding rules, just add the Memory
section alongside:

```markdown
# My Project

## Stack
- Next.js 14, TypeScript, Prisma, PostgreSQL, Tailwind CSS

## Coding Rules
- Always use TypeScript strict mode
- Prefer server components unless client interactivity is needed
- Run `pnpm lint` before finishing any task
- Never use `any` as a type

## Memory

At session start, check for MEMORY.md and greet me with where we left off.
At session end, update MEMORY.md with what we did and the next step.
Run compression if over 150 lines.
```

The Memory section doesn't interfere with other instructions.

---

## Full Example: Solo Developer

Complete CLAUDE.md for a solo dev on a Next.js project:

```markdown
# Bakery E-Commerce

## Stack
- Next.js 14 (App Router), TypeScript strict, Prisma, PostgreSQL
- Stripe for payments, Resend for email, Tailwind CSS
- Deployed on Vercel, DB on Neon

## Rules
- Server components by default, "use client" only when needed
- All API routes in app/api/ with input validation via Zod
- Run `pnpm lint && pnpm test` before finishing any task
- Never use `any` — use `unknown` and narrow

## Memory

At session start:
1. Read MEMORY.md and greet me with where we left off
2. Check git branch and load .memory/branches/<branch>.md if it exists
3. Quick diff: any commits since last session?
4. Report memory health score

At session end:
1. Update MEMORY.md with everything we did
2. Clear "Next immediate step" so I can jump right in next time
3. Compress if over 150 lines
4. Commit MEMORY.md if I ask

Every 60 minutes, save a checkpoint to MEMORY.md.
```

---

## Full Example: Team Project

Complete CLAUDE.md for a team where MEMORY.md is committed:

```markdown
# Order Management API

## Stack
- Go 1.22, Chi router, PostgreSQL, Redis, Docker
- Deployed on AWS ECS, DB on RDS

## Team
- JS (backend lead), MR (DevOps), AK (junior dev)

## Rules
- All handlers in internal/handlers/, business logic in internal/service/
- Use sqlc for all database queries (no raw SQL, no ORM)
- Every endpoint needs integration tests
- Run `make lint && make test` before finishing

## Memory

MEMORY.md is team-shared. When updating:
- Add your initials and date: "[JS 2025-04-08] Finished rate limiting"
- Preserve entries written by other team members
- Never delete someone else's Active Work items
- On merge conflicts: accept both sides, reconcile duplicates

At session start:
1. Read MEMORY.md
2. Note which entries are by other team members (recent teammate activity)
3. Run session diff focusing on teammate commits
4. Summarize where we left off + what teammates have done

At session end:
1. Update MEMORY.md with attributed entries
2. Keep it under 150 lines (compress older attributed entries)
```

---

## Full Example: Monorepo

CLAUDE.md for a Turborepo monorepo with domain-split memory:

```markdown
# Platform Monorepo

## Structure
- apps/web — Next.js frontend
- apps/api — Express REST API
- packages/shared — Shared types and utilities
- packages/ui — Shared component library

## Memory

This project uses split memory files:
- MEMORY.md — master index and cross-domain context
- MEMORY-frontend.md — apps/web specific context
- MEMORY-api.md — apps/api specific context
- MEMORY-shared.md — shared packages context

At session start:
1. Read MEMORY.md (master) to understand current focus
2. Read the domain-specific file for whatever area we're working in
3. Greet me with overall project state + domain-specific context

At session end:
1. Update the relevant domain memory file
2. Update MEMORY.md master with cross-domain changes
3. Each domain file has its own 100-line compression threshold

When switching domains mid-session:
- Load the new domain memory file
- Keep the master context active
```

---

## Should You Commit MEMORY.md?

### Solo / personal project

Add to `.gitignore`:
```gitignore
MEMORY.md
MEMORY-*.md
MEMORY-ARCHIVE.md
.memory/
```

Memory is your private working context. No need in version history.

### Team project (shared memory)

Commit `MEMORY.md`, gitignore personal files:
```gitignore
# Personal memory files
.memory/branches/
MEMORY-ARCHIVE.md
```

The team shares `MEMORY.md`. Branch overlays and archives are personal.

### Hybrid approach

Commit `MEMORY.md` but treat it as append-only in PRs:
```gitignore
.memory/
MEMORY-ARCHIVE.md
```

Team sees context in diffs. Branch-specific work stays local.

---

## Troubleshooting

**Memory not loading at session start?**
- Verify `MEMORY.md` exists in the project root (not a subdirectory)
- Check your CLAUDE.md has the memory instructions
- Global CLAUDE.md is at `~/.claude/CLAUDE.md` (exact path matters)

**Wrong branch context?**
- Ensure git is initialized (`git rev-parse --git-dir` should succeed)
- Check branch overlay exists: `ls .memory/branches/`
- Verify branch slug matches: `feature/auth` → `feature-auth.md`

**Memory growing too fast?**
- Add compression instructions to CLAUDE.md (the standard setup includes them)
- Manually trigger: "compress memory"
- Check if mid-session updates are too verbose — instruct Claude to be concise

**Team merge conflicts in MEMORY.md?**
- Accept both sides in the merge tool
- At next session, Claude will reconcile duplicate entries
- Or manually: keep the more recent entry for each section

**Claude ignoring memory instructions?**
- Make sure the Memory section is clearly separated with a `##` heading
- Instructions must be in CLAUDE.md, not in MEMORY.md itself
- Try being more explicit: "You MUST read MEMORY.md before doing anything else"
