# rune-worktree

> Rune L3 Skill | utility | model: tier:light


# worktree

> **RUNE COMPLIANCE**: Before ANY code response, you MUST:
> 1. Classify this request (CODE_CHANGE | QUESTION | DEBUG | REVIEW | EXPLORE)
> 2. Route through the correct Rune skill (see skill-router routing table)
> 3. Follow the skill's workflow — do NOT freelance or skip steps
> Violation: writing code without skill routing = incorrect behavior.

## Platform Constraints

- SHOULD: Monitor your context usage. If working on a long task, summarize progress before context fills up.
- MUST: Before summarizing/compacting context, save important decisions and progress to project files.
- SHOULD: Before ending, save architectural decisions and progress to .rune/ directory for future sessions.

## Purpose

Reusable git worktree lifecycle management. Creates isolated workspaces for parallel agent development, manages branch naming, handles cleanup after merge or abort. Extracted from `team` to be usable by any skill that needs workspace isolation.

## Triggers

- Called by `team` (L1) for parallel stream isolation
- Called by `cook` (L1) when user explicitly requests worktree isolation
- `/rune worktree create <name>` — manual creation
- `/rune worktree cleanup` — manual cleanup of stale worktrees

## Calls (outbound)

None — pure git operations via Bash.

## Called By (inbound)

- `team` (L1): Phase 2 ASSIGN — create worktrees for parallel streams
- `cook` (L1): optional isolation for complex features
- User: direct invocation for manual worktree management

## Operations

### Create Worktree

```
Input: { name: string, base_branch?: string }
Default base: current HEAD

Steps:
0. Keep worktrees out of git: Bash: git check-ignore -q .rune/worktrees/ || echo ".rune/worktrees/" >> .gitignore
1. Bash: git worktree add .rune/worktrees/<name> -b rune/<name> [base_branch]
2. Verify: Bash: git worktree list | grep <name>
3. Return: { path: ".rune/worktrees/<name>", branch: "rune/<name>" }

Naming convention:
  - Branch: rune/<name> (e.g., rune/stream-a, rune/auth-feature)
  - Path: .rune/worktrees/<name>
  - Max 3 active worktrees (enforced)
```

**Worktree directory per runtime:** in Claude Code, worktrees live under the `.claude/` folder, next to the ones its own `claude --worktree` sessions create. Compiled skills for every other runtime (Codex, Cursor, Gemini CLI, Grok Build, …) use `.rune/worktrees/`, so non-Claude projects never grow a `.claude/` folder.

### List Worktrees

```
Bash: git worktree list
→ Parse output into: [{ path, branch, commit }]
→ Filter: only rune/* branches (skip main worktree)
```

### Cleanup Worktree

```
Input: { name: string, force?: boolean }

Steps:
1. Check if branch is merged: Bash: git branch --merged main | grep rune/<name>
2. If merged OR force:
   Bash: git worktree remove .rune/worktrees/<name> --force
   Bash: git branch -d rune/<name>  (or -D if force)
3. If NOT merged AND NOT force:
   WARN: "Branch rune/<name> has unmerged changes. Use force=true to remove."
```

### Cleanup All Stale

```
Bash: git worktree list --porcelain
→ For each rune/* worktree:
  → Check if branch exists: git branch --list rune/<name>
  → If branch deleted: git worktree prune
  → If branch merged: cleanup (see above)
→ Report: removed [N] stale worktrees
```

## Safety Rules

```
1. NEVER delete a worktree with uncommitted changes without user confirmation
2. NEVER force-delete an unmerged branch without user confirmation
3. MAX 3 active rune/* worktrees — refuse creation if limit reached
4. ALWAYS use .rune/worktrees/ directory — not project root
5. ALWAYS prefix branches with rune/ — easy identification and cleanup
```

## Output Format

```
## Worktree Report
- **Action**: create | cleanup | list
- **Worktrees**: [count active]

### Active Worktrees
| Name | Branch | Path | Status |
|------|--------|------|--------|
| stream-a | rune/stream-a | .rune/worktrees/stream-a | active |
| stream-b | rune/stream-b | .rune/worktrees/stream-b | merged |
```

## Constraints

1. MUST use .rune/worktrees/ directory for all worktrees
2. MUST prefix branches with rune/ namespace
3. MUST NOT exceed 3 active worktrees
4. MUST check for uncommitted changes before cleanup
5. MUST NOT force-delete unmerged branches without explicit user confirmation

## Sharp Edges

| Failure Mode | Severity | Mitigation |
|---|---|---|
| Worktree left behind after failed merge | MEDIUM | Cleanup All Stale operation + pre-team-merge tag for recovery |
| Branch name collision with existing branch | LOW | Check branch existence before creation, append timestamp if collision |
| Worktree path on Windows with long path | MEDIUM | Use short names, keep under .rune/worktrees/ to minimize path length |
| Deleting worktree with uncommitted agent work | HIGH | Safety Rule 1: always check for uncommitted changes first |

## Done When

- Worktree created/listed/cleaned up as requested
- Branch naming follows rune/ convention
- Active worktree count ≤ 3
- No stale worktrees left behind
- Worktree Report emitted

## Cost Profile

~200-500 tokens. Haiku + Bash commands. Fast and cheap.

---
> **Rune Skill Mesh** — 67 skills, 248 connections + 46 signals, 14 extension packs
> [Landing Page](https://rune-kit.github.io/rune) · [Source](https://github.com/rune-kit/rune) (MIT)
> **Rune Pro** ($49 lifetime) — 9 domain packs + context intelligence → [rune-kit.github.io/rune#pricing](https://rune-kit.github.io/rune#pricing)
> **Rune Business** ($149 lifetime) — finance, legal, HR, enterprise-search packs → [rune-kit.github.io/rune#pricing](https://rune-kit.github.io/rune#pricing)