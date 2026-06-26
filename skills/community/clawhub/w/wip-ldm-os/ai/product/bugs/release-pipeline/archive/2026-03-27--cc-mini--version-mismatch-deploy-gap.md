# Bug Fix: Version mismatches + deploy-public gap

**Date:** 2026-03-27
**Tickets:** #225, #226, #223
**Save to:** wip-ldm-os-private/ai/product/bugs/

## Root cause

The installer clones from PUBLIC repos. wip-release publishes to npm but doesn't run deploy-public.sh. So the public repo stays at the old version. The installer clones the old version, sees it matches what's installed, skips.

## What was fixed

- Ran deploy-public.sh for wip-xai-grok (1.0.2 -> 1.0.3 on public)
- Ran deploy-public.sh for wip-ai-devops-toolbox (1.9.51 -> 1.9.52 on public)
- Tavily: third-party npm package, different issue (openclaw-tavily wrapper repo)

## What still needs fixing

- #223: wip-release should run deploy-public.sh automatically
- #231: pre-commit hook blocks wip-release on main
- Tavily version mismatch (wrapper repo vs npm package)

## Verification

```bash
ldm install --dry-run
# grok and toolbox should no longer show as update available
```
