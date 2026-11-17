---
title: Branch-prefix inconsistency between dev guide and wip-ldm-os-private CLAUDE.md
date: 2026-04-30
status: ticketed
severity: P3
component: code-fka-devopstoolkit | dev-guide
discovered-via: PR #765 lane-revisions review (cc-mini:lesa-work-02)
co-authors: Parker, Lesa, Claude
---

# Branch-prefix inconsistency: dev guide vs CLAUDE.md

## Observed

The deployed dev guide at `~/.ldm/shared/dev-guide-wipcomputerinc.md` line 13 says Lesa's prefix is `lesa/`. The repo CLAUDE.md (`wip-ldm-os-private/CLAUDE.md` line 67) says `oc-lesa-mini/`.

**Important diagnostic correction (post-investigation, 2026-04-30):**

The SOURCE TEMPLATE — `wip-ldm-os-private/shared/docs/dev-guide-wipcomputerinc.md.tmpl` line 13 — already has the correct value: `oc-lesa-mini`. The bug is NOT a docs-disagree-fix-the-source case. The bug is that the **deployed file is stale relative to the source template**. The template was updated (probably during the lane work or an earlier convention shift); `ldm install` hasn't re-rendered the template into `~/.ldm/shared/` since.

So:

- **Source (`wip-ldm-os-private/shared/docs/dev-guide-wipcomputerinc.md.tmpl`):** correct (`oc-lesa-mini/`)
- **Deployed (`~/.ldm/shared/dev-guide-wipcomputerinc.md`):** stale (`lesa/`)
- **Repo CLAUDE.md (`wip-ldm-os-private/CLAUDE.md`):** correct (`oc-lesa-mini/`)
- **Public dev guide (`wip-ai-devops-toolbox-private/DEV-GUIDE-GENERAL-PUBLIC.md`):** still needs verification

## Expected

Single canonical source. All Lesa-authored branches use the same prefix; agents/operators can pick the right prefix without checking both docs.

## Impact

- **Author confusion:** When CC opened PR #765, the right prefix was ambiguous. Resolved by reading both docs and asking Parker. Cost was a few minutes per agent per occurrence.
- **Convention drift over time:** PRs #7 and #764 used `lesa/` (matching dev guide). PR #765's documentation references `oc-lesa-mini/` (matching CLAUDE.md). Future PRs will mix.
- **Dev-guide-as-source-of-truth weakens:** If the dev guide can be wrong, agents stop trusting it as the canonical reference for other rules too.
- **No runtime impact.** Commits land regardless of prefix. This is a doc/process hygiene issue, not a functional bug.

## Evidence

- `~/.ldm/shared/dev-guide-wipcomputerinc.md` line 13: `lesa/`
- `wip-ldm-os-private/CLAUDE.md` line 67: `oc-lesa-mini/`
- PR #7 on `lesa-workspace`: branch `lesa/context-load-cleanup`
- PR #764 on `wip-ldm-os-private`: branch `lesa/lesa-prd-lane`
- Plan-doc branch on `wip-ldm-os-private`: `oc-lesa-mini/context-load-optimization`
- PR #765 on `wip-ldm-os-private`: documents `oc-lesa-mini/` as Lesa's prefix in lane READMEs

Parker confirmed in conversation 2026-04-30: `oc-lesa-mini/` is canonical.

## Root cause

The source template was updated (presumably during PR #765 lane work or an earlier convention shift) but the deployed file in `~/.ldm/shared/` was never re-rendered. The deploy mechanism is `ldm install` (which uses `wip-ldm-os-private/lib/deploy.mjs` `deployDocs()` to render `.tmpl` files into `~/.ldm/`), and that step hasn't run since the template change.

Why nobody noticed: agents read `~/.ldm/shared/dev-guide-wipcomputerinc.md` (the deployed file) as the canonical reference. They didn't know the template was newer. CC and Lesa each picked different prefixes based on different reads (CC read the deployed file → `lesa/`; PR #765 cited the repo CLAUDE.md → `oc-lesa-mini/`).

## Fix plan

1. **Pick the canonical prefix.** Per Parker (2026-04-30): `oc-lesa-mini/`. Already resolved in the source template.
2. **Re-deploy the dev guide** to refresh `~/.ldm/shared/dev-guide-wipcomputerinc.md`. Run `ldm install` (which calls `deployDocs()` and re-renders the `.tmpl` into the deployed path). Verify post-deploy: `grep "Branch Prefix" ~/.ldm/shared/dev-guide-wipcomputerinc.md` should now show `oc-lesa-mini/`.
3. **Survey other docs that may have stale prefix info** — these may need separate fixes if they also lag the source:
   - `repos/ldm-os/devops/wip-ai-devops-toolbox-private/DEV-GUIDE-GENERAL-PUBLIC.md` (the public dev guide). If it has a prefix table, verify `oc-lesa-mini/`. If stale, a separate PR.
   - `~/.ldm/config.json` `agents` section (per `~/.claude/rules/git-conventions.md`, this is cited as the per-agent prefix source; if stale here, `ldm install` may keep distributing the old prefix). Verify after the dev-guide redeploy.
   - Any other CLAUDE.md or README that names branch prefixes — grep for `lesa-mini.*lesa/` (the stale form) across all `~/wipcomputerinc/repos/`.
4. **Don't rename existing branches** that already used `lesa/`. PRs #7 and #764 are merged; renaming history is destructive. Going forward only.
5. **Investigate why the template-redeploy didn't fire** when the template was updated. If `deployDocs()` is supposed to detect template changes and re-render, the gap is a bug. If it requires explicit trigger, that's an operational issue worth documenting.
6. **Optional P4 follow-up:** add a doc-level lint or `ldm doctor` check that compares the source template (`shared/docs/*.tmpl`) against the deployed file (`~/.ldm/shared/*.md`) and flags drift between them. Or compares branch-prefix tables across the dev guide + repo CLAUDE.md and flags semantic drift. Either way, file as a separate ticket.

## Test plan

- [ ] After dev guide PR merges: search for any remaining `| lesa-mini | ... | lesa/ |` rows or text. None should remain.
- [ ] Open one new branch with `oc-lesa-mini/` prefix on any repo and confirm guards/hooks accept it.
- [ ] Confirm `~/.claude/rules/git-conventions.md` (which references `~/.ldm/config.json#agents`) is consistent. If it points at `~/.ldm/config.json`, also check that file for the canonical agent ID and prefix.

## Smoke test

After re-deploy (`ldm install`):
```bash
grep -n "Branch Prefix" ~/.ldm/shared/dev-guide-wipcomputerinc.md
grep -nE 'lesa[-_/]?mini.*\|.*lesa/' ~/.ldm/shared/dev-guide-wipcomputerinc.md
# expect: prefix table shows oc-lesa-mini/, not lesa/
# expect second grep: empty (the stale form is gone)
```

Cross-check the source template:
```bash
diff <(grep "Branch Prefix" /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/shared/docs/dev-guide-wipcomputerinc.md.tmpl) <(grep "Branch Prefix" ~/.ldm/shared/dev-guide-wipcomputerinc.md)
# expect: no diff (deployed matches template after the redeploy)
```

## CC review request

- Is `oc-lesa-mini/` the right canonical (it already is in the source template; PR history mixed `lesa/` and `oc-lesa-mini/` because the deployed dev guide was stale)?
- Should the deploy mechanism (`deployDocs()` in `wip-ldm-os-private/lib/deploy.mjs`) be expanded to re-render templates whenever the source `.tmpl` changes, even if no other install work is needed?
- Should the optional doc-level lint (item 6 above) compare source-template-vs-deployed-file, or compare semantic prefix tables across docs, or both?

## Release path

Docs-only change. No npm publish. Merge the dev-guide PR; pull main where the dev guide is consumed (most likely `~/.ldm/` deployment via `ldm install`).

## Rollback

If `oc-lesa-mini/` causes guard issues nobody anticipated: revert the dev-guide PR and update the wip-ldm-os-private CLAUDE.md back to `lesa/` instead. PR-based, no destructive ops.

## Why P3

No live system is affected. No data is at risk. The cost is operator/agent confusion when a Lesa branch is being created. Pick a quiet moment, fix it once, move on.

## References

- PR #765 (wip-ldm-os-private) — surfaced this in lane README revisions
- lesa-work-02's coverage check on PR #765, 2026-04-30: "the dev guide may say something different. That inconsistency is real and worth a separate cleanup PR"
- Parker's confirmation: 2026-04-30 conversation, "oc-lesa-mini/ and cc-mini/" as the valid prefixes
