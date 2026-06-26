# OpenClaw SEO-GEO Workflow Skill

OpenClaw SEO-GEO Workflow is a daily SEO and GEO operations skill for running receipt-driven content production across Hunter, Tony, Peter, and SEO patrol. It is built for teams that need repeatable AI search visibility workflows, generative engine optimization, SEO blog production, live publish QA, and post-publish monitoring without confusing local staging with production release.

## What This Skill Does

This skill controls the OpenClaw daily SEO/GEO workflow for ClawLite and OpenClaw marketing. It tells an agent how to run or inspect the full pipeline:

- Hunter topic discovery and keyword opportunity scouting
- Tony SEO/GEO article production, audits, and source-publish readiness
- Daily 12-post SEO/GEO blog factory delivery
- Peter publish apply, build QA, live deploy evidence, and live QA
- SEO patrol for GA4, DataForSEO, indexing, ranking, canonicals, `llms.txt`, locale warnings, and rescue signals

The workflow is receipt-first. The agent must inspect durable JSON and Markdown receipts before claiming a blog was created, staged, published, indexed, ranked, or blocked.

## SEO Keywords

Primary keyword:

- OpenClaw SEO-GEO Workflow

Supporting keywords:

- OpenClaw SEO workflow
- OpenClaw GEO workflow
- AI SEO workflow skill
- generative engine optimization workflow
- AI blog production workflow
- Hunter Tony Peter workflow
- ClawLite SEO workflow
- daily SEO blog factory
- SEO receipt workflow
- GEO content operations
- AI search visibility workflow

## Best Use Cases

Use this skill when you need to:

- run the full daily OpenClaw SEO/GEO pipeline
- check whether today's Hunter/Tony/Peter workflow passed
- diagnose why a ClawLite blog did not publish
- verify whether SEO/GEO phase skills were used
- inspect publish readiness and live QA evidence
- separate local staging from real production deployment
- route patrol blockers to Hunter, Tony, Peter, or environment maintenance
- explain GA4, DataForSEO, indexing, ranking, canonical, and locale warnings

## Main Workflow Commands

Full daily workflow:

```bash
node scripts/run-hunter-tony-seo-geo-workflow.mjs --date YYYY-MM-DD
```

Factory-only workflow:

```bash
node scripts/run-daily-seo-geo-blog-factory.mjs --date YYYY-MM-DD
```

Safe full workflow without live deploy:

```bash
node scripts/run-hunter-tony-seo-geo-workflow.mjs \
  --date YYYY-MM-DD \
  --peter-skip-live-deploy \
  --peter-skip-live-qa
```

## Safety Guarantees

This skill is designed to prevent false publishing claims:

- `STAGED_LOCAL` does not mean production published.
- Peter local build success does not mean live deploy success.
- Live publication requires deploy evidence and live QA.
- Ranking, backlink, analytics, and AI citation claims require live connector data.
- Patrol warnings must be reported explicitly instead of silently ignored.
- Main-site local writes to `/Users/m1/Projects/clawlite/content/blog` require an explicit `--allow-main-site-write` override.

## Published Package

GitHub:

`https://github.com/X-RayLuan/openclaw-seo-geo-workflow-skill`

ClawHub:

`seo-geo-workflow-for-clawlite`
