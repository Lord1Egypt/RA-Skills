# AI DevOps Toolbox ... Product Update

What's new, how it works, how to test. Updated with every release.

---

## v1.9.50 (2026-03-20) ... Product update gate in wip-release

**What:** wip-release now checks that `ai/dev-updates/product-update/*-product-update.md` was modified since the last release. Warns on patch, blocks on minor/major. Same pattern as dev-updates, roadmap, and readme-first checks.

**How to test:**
```bash
wip-release patch --dry-run    # should warn if product update doc not modified
```

---

## v1.9.49 (2026-03-20) ... TECHNICAL.md audit (pass 2)

**What:** Release gates, license-guard hook, deploy pipeline, source table all documented in TECHNICAL.md.

**How to test:** Read TECHNICAL.md. Verify it matches actual tool behavior.

---

## v1.9.48 (2026-03-20) ... TECHNICAL.md audit (pass 1)

**What:** wip-repos claude command and branch guard features documented in TECHNICAL.md and SKILL.md.

**How to test:**
```bash
grep "wip-repos claude" SKILL.md TECHNICAL.md    # should find both
```

---

## v1.9.47 (2026-03-20) ... wip-repos claude + CLAUDE.md templates

**What:**
1. `wip-repos claude` command generates cross-repo ecosystem sections in CLAUDE.md files
2. Global CLAUDE.md template at `templates/global-claude-md.md`
3. Per-repo CLAUDE.md template at `templates/repo-claude-md.template`
4. Delimiter comments (`<!-- wip-repos:start/end -->`) protect hand-written content
5. `--init` creates CLAUDE.md for repos missing one
6. Relevance filtering: only related repos shown

**How to test:**
```bash
wip-repos claude --dry-run    # preview what would change across all repos
wip-repos claude --init       # create CLAUDE.md for repos missing one (use --dry-run first)
```

---

## v1.9.46 (2026-03-19) ... Worktree convention

**What:**
1. Branch guard warns when `git worktree add` creates outside `_worktrees/`
2. wip-release step 12: prunes merged worktrees from `_worktrees/` after release
3. Dev Guide updated with `_worktrees/` convention and `ldm worktree` command

**How to test:**
```bash
# Guard warning (should warn):
git worktree add ../my-test-worktree -b test-branch

# Correct path (should pass):
ldm worktree add cc-mini/test-feature

# After wip-release, check that merged worktrees in _worktrees/ are cleaned
```

---

## v1.9.45 (2026-03-19) ... Guard teaches the workflow

**What:** Branch guard error messages now include the full 8-step dev process. Separate message for "on branch but not in worktree." CLAUDE.md added to shared state allowlist.

**How to test:**
```bash
# On main, try to edit a file. Error should show:
# Step 1: git worktree add ...
# Step 2: Edit files in the worktree
# Step 3-8: commit, push, PR, merge, release, deploy

# CLAUDE.md should be editable on main without worktree
```

---

## v1.9.44 (2026-03-17) ... ldm enable/disable + conditional interface deployment

**What:** `ldm enable <extension>` and `ldm disable <extension>` control which extensions are active. Disabled extensions stay installed but MCP, hooks, and skills are not registered.

**How to test:**
```bash
ldm disable wip-xai-grok    # should deregister MCP
ldm enable wip-xai-grok     # should re-register MCP
ldm doctor                   # should show enabled/disabled state
```
