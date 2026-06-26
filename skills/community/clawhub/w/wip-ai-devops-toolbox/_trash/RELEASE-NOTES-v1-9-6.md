# v1.9.6 ... Enforcement Gates

Three fixes that move the release pipeline from "suggestions agents forget" to "gates that block."

---

## syncSkillVersion corrupted quoted versions (#71)

Every release was appending the old version instead of replacing it. SKILL.md went from `"1.9.5"` to `"1.9.5".9.4".9.3".9.2".9.1"` over five releases.

Root cause: the regex `"?\S+?"?` used non-greedy matching. For quoted values, it consumed only part of the string, leaving the rest as trailing garbage.

Fix: replaced with `(?:"[^\n]*|\S+)`. Quoted values now match through end of line. Unquoted values use greedy `\S+`. Also fixed the staleness-check regex to extract clean semver from corrupted strings.

**Files changed:**
- `tools/wip-release/core.mjs` ... `syncSkillVersion()` regex fix
- `SKILL.md` ... repaired corrupted version back to `"1.9.5"`

---

## gh pr merge now always deletes branch (#74)

Every `gh pr merge` call in the codebase now includes `--delete-branch`. Previously, deploy-public.sh had a manual 3-line `gh api -X DELETE` cleanup block. That's gone. The flag handles it.

Also verified every merge uses `--merge` (never squash). Dev Guide updated with the new convention.

**Files changed:**
- `scripts/deploy-public.sh` ... added `--delete-branch`, removed manual cleanup
- `tools/deploy-public/deploy-public.sh` ... same
- `DEV-GUIDE-GENERAL-PUBLIC.md` ... updated merge examples
- `ai/DEV-GUIDE-FOR-WIP-ONLY-PRIVATE.md` ... updated merge rules
- `ai/_trash/DEV-GUIDE-private.md` ... updated
- `ai/_sort/_trash/ai_old/_trash/DEV-GUIDE-private.md` ... updated

---

## wip-release blocks on stale remote branches (#75)

New gate in the release pipeline. Before releasing, wip-release checks for remote branches that are fully merged into main but haven't been cleaned up.

- **Patch:** warns with the list of stale branches (non-blocking)
- **Minor/major:** blocks the release. Clean up first.
- **`--skip-stale-check`:** override flag for emergencies

Follows the existing gate pattern: fetches with `--prune`, filters out `origin/main`, `origin/HEAD`, and `--merged-` branches. Fails gracefully if git commands error.

**Files changed:**
- `tools/wip-release/core.mjs` ... `checkStaleBranches()` function, integrated as gate 0.8
- `tools/wip-release/cli.js` ... `--skip-stale-check` flag, help text

---

## Diffstat

```
 10 files changed, 102 insertions(+), 21 deletions(-)
```

## Install

```bash
npm install -g @wipcomputer/wip-ai-devops-toolbox
```

Or update an existing install:
```bash
wip-install wipcomputer/wip-ai-devops-toolbox
```

---

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).
