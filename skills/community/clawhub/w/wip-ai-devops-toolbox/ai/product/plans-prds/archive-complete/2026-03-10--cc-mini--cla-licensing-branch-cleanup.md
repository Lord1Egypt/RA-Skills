# Plan: CLA, Licensing Clarity, Branch Cleanup

**Date:** 2026-03-10
**Author:** cc-mini
**Repo:** wip-ai-devops-toolbox-private

## Goal

Three improvements: protect commercial rights on PR contributions, clarify licensing intent, and automate branch cleanup.

---

## Phase 1: Contributor License Agreement (CLA)

**Problem:** Without a CLA, contributors who submit PRs own their code. AGPL means we can't relicense their contributions commercially. We need contributors to grant WIP Computer, Inc. the right to use their contributions under any license.

**What to build:**
- `CLA.md` at repo root. Plain-English agreement: contributors grant WIP Computer, Inc. a broad license to use contributions under any license, including commercial. Contributors keep their own copyright.
- Add CLA reference to README (small note in the License section or a Contributing section)
- Add CLA reference to PR template so contributors see it before submitting

**Not doing now (deferred):**
- GitHub CLA bot (need external users first, premature for now)
- Separate CLA signing service (overkill at current scale)

**Status:** DONE

---

## Phase 2: Licensing Clarity

**Problem:** Current wording says "Commercial redistribution, marketplace listings, or bundling into paid services." That's accurate but doesn't clarify: using the tools to build your own software is fine. Reselling the tools themselves is what needs a license.

**What to change:**
- Add one line to the "Can I use this?" section: "Using these tools to build your own software is fine. Reselling the tools themselves is what requires a commercial license."
- Update `generateReadmeBlock()` in `tools/wip-license-guard/core.mjs` so future repos get the same wording
- Update the LICENSE file template in `generateLicense()` if needed

**Status:** DONE

---

## Phase 3: Branch Cleanup Automation

**Problem:** Merged branches pile up on the remote. The post-merge-rename script renames them with `--merged-YYYY-MM-DD` but never deletes old ones. Right now there are 30+ stale branches on the private repo. Manually deleting them is error-prone and doesn't scale.

**What to build:**
- Add a `--prune` flag to the post-merge-rename script (or a new `prune` command)
- Logic: for each developer prefix (`cc-mini/`, `mini/`, `lesa-mini/`, etc.), keep only the last 3 `--merged` branches. Delete the rest from the remote.
- Also delete branches that have a `--merged` copy but still exist without the suffix (stale duplicates like `cc-mini/tagline-update` when `cc-mini/tagline-update--merged-2026-03-10` doesn't exist but the PR is merged)
- Run this as part of `wip-release` after the post-merge-rename step
- Dry-run mode so you can preview what would be deleted

**Rules:**
- Never delete branches without `--merged` suffix unless the associated PR is confirmed merged
- Never delete the current working branch
- Never delete `main`
- Keep last 3 `--merged` branches per developer prefix
- Log what was deleted

**Status:** DONE

---

## Done criteria

- CLA.md exists and is referenced in README/PR template
- License section has the clarifying line about using vs reselling
- Branch cleanup runs automatically as part of wip-release
- Private repo has clean branch list (last 3 per developer)
- All changes deployed to public
