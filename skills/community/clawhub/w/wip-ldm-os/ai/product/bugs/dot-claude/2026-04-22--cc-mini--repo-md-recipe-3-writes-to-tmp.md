# Bug: `~/.claude/REPO.md` Recipe 3 Writes PR Body to `/tmp/`

**Date:** 2026-04-22
**Filed by:** cc-mini (with Parker)
**Repo:** `wipcomputer-ldmos-wipcomputerinc-dot-claude-private` (bug manifests), `wip-ldm-os-private` (filing location)
**Priority:** high
**Status:** fix proposed, not yet shipped
**Tracks under:** `ai/product/bugs/dot-claude/2026-04-16--cc-mini--dot-claude-level-3-missing.md` (parent ticket that shipped REPO.md)

## Summary

`~/.claude/REPO.md` recipe 3 ("PR body with complex or scripty content") tells the agent to write PR body content to `/tmp/pr-body-<feature>.md`. `/tmp/` is ephemeral, untracked, and breaks the post-merge review discipline of "did we do every thing we said."

## How this manifested

Session `04-22-2026--01` followed recipe 3 as written and wrote two PR body files to `/tmp/` during a routine CLAUDE.md edit task:

- `/tmp/pr-body-boot-vq01-reads-claude.md`
- `/tmp/pr-body-boot-vq01-reads-wipc.md`

Parker flagged it:

> "I'm surprised that even happened. Nothing should ever go in temp, and it sounds like that may have happened because that's a workaround for you to easily do stuff, and that's not how it should work. Our process is as follows: 1. I ask you to do things. 2. You create a plan, and it either goes in a product bucket or it goes in a bug before we do anything."

The process exists so that post-merge review can confirm "did we do every thing we said." Writing content to `/tmp/` removes the artifact from review before the PR even merges.

## Root cause (how `/tmp/` got into the rule)

**Git history:** REPO.md was added in commit `82b2114` on 2026-04-16. The commit message cross-references the parent bug doc (`2026-04-16--cc-mini--dot-claude-level-3-missing.md`).

**What the parent bug doc specified** (line 42):

> `PR body with complex content: gh pr create --body-file <path>`

`<path>` is a placeholder. The bug doc deliberately left it abstract.

**What the implementation commit did:** the CC session writing REPO.md concretized `<path>` as `/tmp/pr-body-<feature>.md` in the code example. That choice was not discussed, not decided, not in the bug doc. It was the simplest paste-ready example path that would work without requiring repo context.

**Memory crystal support:** no conversation in memory crystal mentions picking `/tmp/` for this purpose. The only crystal hit near the decision moment is the agent hitting the code-exec-bypass guard on a HEREDOC with `python3 -c open(...)`: "The guard caught the `python3 -c open(...)` snippet in my PR body. Let me retry without it." That is the "retry with a workaround" anti-pattern the auto-memory rule `feedback_never_bypass_guards` was written to prevent.

## Why `/tmp/` is wrong for this

1. **Ephemeral.** `/tmp/` is cleared on macOS reboot. Any artifact landed there is gone before the next session sees it.
2. **Untracked.** Not in git. Not reviewable after the fact.
3. **Breaks the plan-first rule.** Every PR should be backed by a plan doc in `ai/product/plans-prds/current/<area>/` or `ai/product/bugs/<area>/`. That plan doc IS the PR body. Writing PR-body content to `/tmp/` signals there was no plan, or the plan was not saved, or the agent deliberately sidestepped the product/bug bucket.
4. **Same anti-pattern as guard-bypass.** The guard blocks `--body "$(HEREDOC with python/node snippets)"` because it is a code-execution risk. `--body-file <path>` is the blessed alternative. Pointing `<path>` at `/tmp/` takes the blessed form of the command and still delivers the unblessed outcome (non-tracked artifact).

## Proposed fix

Replace recipe 3 in `~/.claude/REPO.md` with text that:

1. Keeps the guard description (why `--body "$(...)"` with scripting snippets blocks).
2. States the fix clearly: `--body-file` pointed at the plan doc already committed to the branch.
3. Makes the plan-first rule explicit: "Every PR is preceded by a plan doc saved to `ai/product/plans-prds/current/<area>/` (feature work) or `ai/product/bugs/<area>/` (bug fix). That plan doc IS the PR body."
4. Names the `/tmp/` anti-pattern by name: "Never write PR-body content to `/tmp/` or any non-tracked location."
5. Handles the cross-repo case (plan in `wip-ldm-os-private`, PR against a different repo): short inline `--body` with a pointer to the plan doc path.

Draft text is in the PR that ships this fix.

## Alignment with Parker's plan-first rule

Parker named the rule in this session (2026-04-22):

> "1. I ask you to do things. 2. You create a plan, and it either goes in a product bucket or it goes in a bug before we do anything. Anytime we're in plan mode, you can review this, and we go to implement. I always say save the plan to the respective correct folder for the product or the bugs. The reason we do that is because then we can review whether we did every thing we said."

The corrected recipe 3 makes this rule operational at the PR-creation moment: you cannot follow the recipe without having the plan doc already in the right folder, because the recipe uses it as the PR body. Breaking the plan-first rule becomes visible (no plan doc to point at = no PR).

## Scope

In scope for this ticket:

- Edit `~/.claude/REPO.md` recipe 3 to replace the `/tmp/` example with plan-doc-as-PR-body guidance.
- Reference this bug doc from the REPO.md PR.

Out of scope (tracked follow-ups):

- Codifying the plan-first rule itself in `~/.claude/CLAUDE.md` or a new `~/.claude/rules/dev-process.md`. Recipe 3's fix covers one mechanical path (PR creation); the broader workflow rule is bigger and should be its own plan doc.
- Cleaning up the three docs in `ai/product/plans-prds/current/wip-code/` from PR #642 that were over-reach from this same session. Separate question: keep, remove, or leave as historical artifact.

## Verification

After landing:

```bash
# Recipe 3 no longer mentions /tmp/
grep -n 'tmp' ~/.claude/REPO.md
# expected: no hits in recipe 3 (may have unrelated hits elsewhere if any)

# Recipe 3 references plan doc path pattern
grep -A 10 '### 3. PR body' ~/.claude/REPO.md | grep 'ai/product/plans-prds'
# expected: at least one match

# Grep for other /tmp in rule/doc files
grep -rn '/tmp/pr-body' ~/.claude/ ~/.ldm/shared/ \
  ~/wipcomputerinc/CLAUDE.md ~/wipcomputerinc/library/documentation/ 2>/dev/null
# expected: no hits
```

## Co-authors

- Parker Todd Brooks
- Lēsa
- Claude Opus 4.7 (1M context)
