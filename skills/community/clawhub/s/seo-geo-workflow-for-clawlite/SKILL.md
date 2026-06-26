---
name: openclaw-seo-geo-workflow
description: Use when Ray asks about the OpenClaw SEO-GEO Workflow, ClawLite/OpenClaw daily SEO/GEO workflow, Hunter/Tony/Peter blog production, daily blog factory delivery, source publish readiness, live publish QA, SEO/GEO patrol, ranking/indexing/GA4/DataForSEO blockers, or why a blog/workflow did not publish.
version: "0.4.3"
license: private
tags:
  - clawlite
  - openclaw
  - seo
  - geo
  - daily-workflow
  - hunter
  - tony
  - peter
  - patrol
---

# OpenClaw SEO-GEO Workflow

This is the controlling runbook for Ray's OpenClaw SEO-GEO daily workflow. It coordinates Hunter discovery, Tony content production, the 12-post SEO/GEO factory, Peter publish/build/live QA, and daily SEO patrol for ClawLite/OpenClaw marketing.

Use this skill as the first stop. Do not invent a parallel workflow. The source of truth is the deterministic scripts and receipts under `/Users/m1/.openclaw/workspace`.

## Default Stance

- Receipt first, then claims. Inspect durable JSON/Markdown receipts before saying a workflow passed, failed, published, or used a skill.
- Local staging is not production publishing. `STAGED_LOCAL`, Peter local build success, and source publish are not live deployment.
- Production publish claims require deploy evidence plus live QA.
- Monitor/ranking/backlink/AI-citation claims require connector or live patrol data.
- Missing live dependencies should degrade to explicit `SKIPPED`, `NEEDS_DATA`, or `PASS_WITH_WARNINGS`, not silent success.
- Never let the legacy `/Users/m1/Projects/clawlite` project take over `clawlite.ai` production aliases unless Ray explicitly asks.
- Never write into `/Users/m1/Projects/clawlite/content/blog` from chat-triggered workflow runs unless Ray explicitly asks for main-site local apply and the command uses `--allow-main-site-write`.

## Main Commands

Run from `/Users/m1/.openclaw/workspace`.

Full daily workflow, recommended default:

```bash
node scripts/run-hunter-tony-seo-geo-workflow.mjs --date YYYY-MM-DD
```

Factory-only workflow:

```bash
node scripts/run-daily-seo-geo-blog-factory.mjs --date YYYY-MM-DD
```

Safe full workflow with no live deploy:

```bash
node scripts/run-hunter-tony-seo-geo-workflow.mjs \
  --date YYYY-MM-DD \
  --peter-skip-live-deploy \
  --peter-skip-live-qa
```

Protected main-site local apply requires an explicit override. Do not add this flag unless Ray asked to modify the main ClawLite repo:

```bash
node scripts/run-clawlite-publish-apply.mjs \
  --date YYYY-MM-DD \
  --allow-main-site-write
```

Live deploy path requires explicit evidence:

```bash
node scripts/run-hunter-tony-seo-geo-workflow.mjs \
  --date YYYY-MM-DD \
  --peter-allow-live-deploy \
  --peter-deploy-command "npm exec -- vercel deploy --prod --prebuilt" \
  --peter-deploy-evidence-path /path/to/deploy-evidence.json \
  --peter-live-qa-base-url https://clawlite.ai
```

Environment equivalents:

- `CLAWLITE_PETER_DEPLOY_COMMAND`
- `CLAWLITE_PETER_DEPLOY_EVIDENCE_PATH`
- `CLAWLITE_PETER_SKIP_LIVE_DEPLOY=1`
- `OPENCLAW_SEO_PATROL_MODE=live`
- `DATAFORSEO_B64`

## Role Boundaries

- Hunter: topic radar, multi-source discovery, keyword opportunity scouting, raw scouting receipts, durable wiki handoff briefs, and 14-30 day dedupe.
- Tony: keyword briefs, SEO/GEO drafts, quality audit, preflight, and source-ready delivery. Tony does not claim live production publication.
- Factory: creates the daily 12-post SEO/GEO package, phase receipts, manifests, repairs, and local publish artifacts.
- Peter: ClawLite publish apply, build QA, optional live deploy, live QA, canonical safety, and closeout.
- Patrol: post-publish and daily visibility checks for SERP/indexing, `llms.txt`, GA4, canonical/cannibalization, locale paths, and rescue signals.

## Required Phase Matrix

Every generated article should have receipts for:

1. Research: `keyword-research`, `competitor-analysis`, `serp-analysis`, `content-gap-analysis`
2. Build: `seo-content-writer`, `geo-content-optimizer`, `meta-tags-optimizer`, `schema-markup-generator`
3. Optimize: `on-page-seo-auditor`, `technical-seo-checker`, `internal-linking-optimizer`, `content-refresher`
4. Monitor: `rank-tracker`, `backlink-analyzer`, `performance-reporter`, `alert-manager`
5. Cross-cutting: `content-quality-auditor`, `domain-authority-auditor`, `entity-optimizer`, `memory-management`

Monitor receipts may be `NEEDS_DATA` until live URLs, rank provider data, analytics, and backlink data exist.

## Receipt Map

Core daily receipts:

- `mission-control/data/runner/hunter-tony-seo-geo-YYYY-MM-DD.json`
- `mission-control/data/runner/hunter-daily-topic-delivery-YYYY-MM-DD.json`
- `mission-control/data/runner/clawlite-publish-apply-build-YYYY-MM-DD.json`
- `mission-control/data/content-delivery/hunter-daily-topic-radar-raw-YYYY-MM-DD.json`
- `mission-control/data/content-delivery/hunter-daily-topics-YYYY-MM-DD.json`
- `mission-control/data/content-delivery/tony-keyword-brief-YYYY-MM-DD.json`
- `mission-control/data/content-delivery/tony-content-quality-audit-YYYY-MM-DD.json`
- `mission-control/data/content-delivery/tony-blog-preflight-YYYY-MM-DD.json`
- `mission-control/data/content-delivery/tony-blog-source-publish-YYYY-MM-DD.json`
- `mission-control/data/peter/peter-blog-closeout-verify-YYYY-MM-DD.json`
- `mission-control/data/peter/peter-live-publish-qa-YYYY-MM-DD.json`
- `mission-control/data/seo-patrol/gr-seo-patrol-YYYY-MM-DD.json`
- `mission-control/data/seo-patrol/gr-seo-patrol-YYYY-MM-DD.md`

Daily package outputs:

- `delivery/seo-geo/YYYY-MM-DD/manifest.md`
- `delivery/seo-geo/YYYY-MM-DD/manifest.json`
- `delivery/seo-geo/YYYY-MM-DD/blogs/`
- `delivery/seo-geo/YYYY-MM-DD/metadata/`
- `delivery/seo-geo/YYYY-MM-DD/audits/`
- `delivery/seo-geo/YYYY-MM-DD/skills/<phase>/<skill>/`
- `delivery/seo-geo/YYYY-MM-DD/repairs/`
- `delivery/seo-geo/YYYY-MM-DD/publish/clawlite-content/`
- `synthadoc/wiki/*hunter-daily-topic*`

## Operating Loop

1. Identify target date. Default to today only when Ray did not provide a date.
2. Read the runner receipt first: `mission-control/data/runner/hunter-tony-seo-geo-YYYY-MM-DD.json`.
3. If the runner receipt is missing and Ray asked to run delivery, run the full daily command.
4. Inspect Hunter raw radar and durable topic delivery before judging topic selection.
5. Inspect `delivery/seo-geo/YYYY-MM-DD/manifest.md` and `manifest.json` before judging article readiness.
6. Check `repairSummary`, `skillPipeline`, `publishQueue`, `deploy`, `patrol`, and Peter closeout.
7. If any article has `humanReviewRequired > 0`, inspect `repairs/` and failed skill receipts before editing.
8. If Peter/local build passed but live deploy was skipped, say staged/build passed, not published.
9. If live deploy ran, verify deploy evidence and `peter-live-publish-qa`.
10. Treat overall workflow as not fully green until patrol blockers are cleared.

## Status Meanings

- `READY`: publish-queue eligible.
- `BLOCKED`: at least one blocking gate failed.
- `PASS`: a required step completed successfully.
- `FAIL`: a blocking step failed and needs repair or human review.
- `NEEDS_DATA`: non-blocking monitor step is waiting for live URL or connector data.
- `PASS_WITH_WARNINGS`: delivery may continue, but connector data or non-blocking checks are missing.
- `STAGED_LOCAL`: source files or local repo changes were prepared; production publication is not proven.
- `SKIPPED`: a step intentionally did not run and must include a reason.

## Gates

An article can enter publish queue only when:

- all blocking Research, Build, Optimize, and Cross-cutting receipts are `PASS`
- draft audit status is `PASS`
- audit score is at least `90`
- repair status is `NOT_NEEDED` or `REPAIRED`
- no blocking skill receipt has `FAIL`

If a blocking gate fails:

1. Mark the article `BLOCKED`.
2. Map audit failures to failed skills.
3. Write `delivery/seo-geo/YYYY-MM-DD/repairs/<article>.json`.
4. Repair only the failed surface: structure, word count, keyword placement, internal links, meta, or schema.
5. Rerun failed skill and downstream receipts.
6. Queue only if final audit reaches `PASS` and score `>= 90`.
7. If repair is disabled or still fails, mark failed blocking receipts `FAIL` with `humanReviewRequired: true`.

## Common Diagnostics

### "The blog did not publish"

Check in order:

1. `mission-control/data/runner/hunter-tony-seo-geo-YYYY-MM-DD.json`
2. `delivery/seo-geo/YYYY-MM-DD/manifest.md`
3. `mission-control/data/runner/clawlite-publish-apply-build-YYYY-MM-DD.json`
4. `mission-control/data/peter/peter-blog-closeout-verify-YYYY-MM-DD.json`
5. `mission-control/data/peter/peter-live-publish-qa-YYYY-MM-DD.json`
6. Live URL and sitemap only after Peter live QA exists.

Report the exact stage: Hunter, Tony, Factory, Peter local apply/build, live deploy, live QA, or patrol.

### "Did you use the SEO/GEO skill?"

Check `delivery/seo-geo/YYYY-MM-DD/skills/` and `manifest.json`. The expected skill family is `seo-geo-claude-skills`, with article-level receipts for the phase matrix. Do not answer from memory.

### "Daily workflow is stuck"

Check:

- OpenClaw logs: `/Users/m1/.openclaw/logs/*.log`
- LaunchAgents: `launchd/ai.openclaw.daily-seo-geo-blog-factory.plist`
- runner receipt freshness under `mission-control/data/runner/`
- active OpenClaw sessions if the task was triggered through Feishu/Discord/Telegram

If a chat-triggered task timed out, use the receipts to determine whether work completed after the chat reply failed.

### Patrol blockers

Known examples:

- `GA4_TAG_MISSING`: Peter/build/live site issue. Verify built layout and live HTML.
- `DATAFORSEO_B64_MISSING`: connector/env issue. Configure env/Keychain before rank/index checks can be complete.
- locale `/en/`, `/ja/`, `/ko/` 404 or redirect warnings: usually non-blocking unless Ray wants locale pages live.
- no top-100 keyword hits: monitor finding, not a publish blocker by itself.

### Production alias safety

If `clawlite.ai` shows old Mission Control or `/mission-control` unexpectedly returns 200, suspect the legacy Vercel project `clawlite` reclaimed the alias. Restore to the verified safe ClawLite main deployment before claiming live success.

## Patrol and Rescue Routing

- new top-30 long-tail opportunity -> Hunter
- title/body/internal-link decay -> Tony
- canonical, live URL, build, deploy, alias, sitemap, or GA4 issue -> Peter
- missing connector or API credential -> environment/config maintenance

Every daily run should produce a `gr-seo-patrol` receipt. Patrol checks include SERP rank diff when `DATAFORSEO_B64` exists, Google index count when supported, `llms.txt`, GA4, canonical/cannibalization, rescue signals, rank-tracking slots, and redirect-aware locale checks.

## Related Skills and References

- `ray-tony-seo-geo`: use for single-article Tony keyword/content/audit/source-publish work.
- `gr-seo-patrol`: use for focused patrol/rescue work.
- `/Users/m1/seo-geo-claude-skills`: upstream SEO/GEO phase skill library.
- `references/clawlite-seo-geo-workflow.md`: workflow reference notes.
