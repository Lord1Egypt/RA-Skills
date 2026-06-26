# BUG: wip-release silently skips ALL quality gates when .license-guard.json is missing

**Date:** 2026-04-08
**Filed by:** cc-mini
**Severity:** CRITICAL
**Status:** open

## Superseded / Consolidated By

This bug is consolidated into `ai/product/bugs/release-pipeline/2026-04-24--codex--canary-release-pipeline-master-plan.md`, especially Phase 1: Audit Existing Release Fixes and Phase 2: `wip-release check`.

Keep this file for historical context and exact failure detail. Use the 2026-04-24 canary release pipeline master plan as the current implementation map.

## What happened

A subagent built a new repo (wip-x-xai-grok-private). The repo had:
- Wrong license (MIT only, not dual MIT+AGPL)
- No .license-guard.json
- No CLA.md
- README without license section, without built-by line, not from template
- No release notes
- No repo scaffold (wip-repo-init never ran)

The code was merged via PR. Then `wip-release alpha` ran successfully. npm published. `deploy-public.sh` ran. The package went live. None of the quality gates fired.

## Root cause

`wip-release` line 1744 (stable) and line 2594 (alpha):
```javascript
const configPath = join(repoPath, '.license-guard.json');
```

If `.license-guard.json` doesn't exist, the ENTIRE license compliance gate is skipped silently. No warning. No error. Just skipped.

The release notes gate (line 1805) also has issues:
- Alpha with `--notes="..."` bypasses the file-only requirement
- No gate checks README format, built-by line, or template compliance

## Why this is critical

1. **Any new repo ships without guardrails.** The gates only protect repos that already have `.license-guard.json`. New repos get zero protection.
2. **Subagents don't scaffold.** When work is delegated to a subagent, it builds code but doesn't run `wip-repo-init`, doesn't know about templates, doesn't create `.license-guard.json`. The pipeline should catch this. It doesn't.
3. **The whole point of the pipeline is to prevent this.** We built wip-release specifically so bad releases can't ship. A missing config file defeats the entire system.

## The fix

### Option A: wip-release refuses to run without .license-guard.json (RECOMMENDED)

If `.license-guard.json` is missing, wip-release should:
1. Print: "No .license-guard.json found. Run `wip-repo-init` to scaffold this repo."
2. BLOCK the release (not warn, BLOCK)
3. Exit non-zero

This makes the gate mandatory, not opt-in.

### Option B: wip-release auto-scaffolds if missing

If `.license-guard.json` is missing, create a default one with WIP Computer standards, then run the gate. Repo gets fixed automatically.

### Option C: Both

Block, print the command, but also offer `--init` flag that scaffolds and continues.

### Additional gates needed

1. **README template check.** README must contain `## License`, built-by line, and match the org template.
2. **CLA.md check.** Must exist.
3. **.npmignore check.** Must exclude `ai/`, `CLAUDE.md`, `.claude/`.
4. **wip-repo-init check.** If `ai/` folder doesn't exist, the repo was never scaffolded. Block.

## What needs to change

| File | Change |
|---|---|
| `tools/wip-release/core.mjs` line ~1744 | Block if .license-guard.json missing (not skip) |
| `tools/wip-release/core.mjs` line ~2594 | Same for alpha path |
| `tools/wip-release/core.mjs` | Add README template gate |
| `tools/wip-release/core.mjs` | Add .npmignore gate |
| `tools/wip-release/core.mjs` | Add CLA.md gate |

## Incident details

- **Repo:** wip-x-xai-grok-private
- **Published version:** 1.0.1-alpha.1 (npm @alpha)
- **Public repo:** wip-x-xai-grok (v1.0.0 released with wrong license)
- **Impact:** Wrong license on public npm and GitHub. No release notes. No CLA.
- **Cost:** Parker's trust. Time debugging. Reputation risk from wrong license on public repo.

## Related

- `ai/product/bugs/release-pipeline/2026-04-05--cc-mini--release-pipeline-master-plan.md`
- `ai/product/bugs/release-pipeline/2026-04-06--cc-mini--shared-universal-config-layer.md`
- Incident: API key leaked via ecosystem.config.cjs (same session, same subagent delegation pattern)
- 1Password plan: `ai/product/plans-prds/1password/2026-04-08--cc-mini--1password-as-single-source.md`
