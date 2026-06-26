---
name: seo-geo-qa
displayName: SEO Content QA
description: "Check blog posts and articles before publishing. Finds broken links, weak sources, missing SEO elements, and citation problems. Use when: reviewing a draft, auditing content quality, checking if links still work, verifying sources are credible, running pre-publish QA, or doing post-publish page checks. Also triggers on: 'check this article', 'verify my links', 'review before publishing', 'content audit', 'source quality check', 'are my links working', 'SEO review', 'pre-publish checklist'. Generates markdown+JSON reports with PASS/FAIL verdict. Python stdlib only, no dependencies."
tags:
  - seo
  - content-qa
  - links
  - citations
  - publishing
---

# SEO Content QA

Use this skill to audit content reliability before or after publishing.

## Requirements

- **Python 3.10+** (scripts use modern type syntax)
- `curl` available in PATH (for HTTP HEAD checks)
- No pip dependencies — standard library only
- **Network access to `r.jina.ai`** — used as a fallback for SERP search and competitor page fetching (bypasses Cloudflare / anti-bot). Pass `--no-jina` to disable if needed.

## Quick start

Run the unified runner for normal draft review:

```bash
python3 skills/seo-geo-qa/scripts/seo_qa_runner.py path/to/article.md --keyword "best email apps"
```

If you know the site's main domain, pass it so internal vs external links are counted correctly:

```bash
python3 skills/seo-geo-qa/scripts/seo_qa_runner.py path/to/article.md --keyword "best email apps" --site-domain example.com
```

If you want project defaults, pass a lightweight JSON config:

```bash
python3 skills/seo-geo-qa/scripts/seo_qa_runner.py path/to/article.md --keyword "best email apps" --config path/to/seo-geo-qa.json
```

## Standard workflow

1. Run `seo_qa_runner.py` on the draft.
2. Read the markdown report for the human audit trail.
3. Use the JSON report for automation or later aggregation.
4. Fix critical issues first.
5. Re-run until the article reaches PASS (or REVISE in writer mode).
6. After publishing, run `post_publish_check.py` on the live URL.

## Lower-level tools

Use these only when debugging a specific failure mode.

### Link/source verification
```bash
python3 skills/seo-geo-qa/scripts/verify_links.py path/to/article.md
python3 skills/seo-geo-qa/scripts/verify_links.py path/to/article.md --json
```

### SERP gap analysis

```bash
# Auto-search (uses DuckDuckGo + Jina Reader fallback for anti-bot bypass)
python3 skills/seo-geo-qa/scripts/serp_gap_analyzer.py "best email apps" path/to/article.md

# Supply competitor URLs directly (skips search, still uses Jina to fetch pages)
python3 skills/seo-geo-qa/scripts/serp_gap_analyzer.py "best email apps" path/to/article.md --urls https://competitor1.com https://competitor2.com

# Disable Jina (direct HTTP only, faster but may fail on Cloudflare-protected sites)
python3 skills/seo-geo-qa/scripts/serp_gap_analyzer.py "best email apps" path/to/article.md --no-jina
```

**How the SERP search works:**
1. Tries DuckDuckGo's HTML endpoint via direct HTTP (fast path)
2. If blocked or returns no results, falls back to Jina Reader (`r.jina.ai`) which renders the page with a real browser and decodes DDG's redirect links
3. Competitor pages are always fetched via Jina first (bypasses Cloudflare), then falls back to direct HTTP

### Post-publish page check
```bash
python3 skills/seo-geo-qa/scripts/post_publish_check.py https://example.com/blog/post
python3 skills/seo-geo-qa/scripts/post_publish_check.py https://example.com/blog/post --json
```

## Report persistence

The runner writes timestamped markdown + JSON reports by default.

Default behavior:
- saves to `qa-reports/<article-slug>/` next to the article
- does not overwrite old reports
- uses markdown for human review and JSON for machine state

Override with `--report-dir` or config.

## Configuration

Read `references/configuration.md` when you need project-level defaults.

## Source quality

Read `references/source-tiers.md` when you need to decide whether a citation is acceptable.

## Verdict rules

Read `references/verdict-rules.md` when you need to tune PASS / FAIL / REVISE behavior.

## Example output

Read `references/example-report.md` for a real QA report with annotations on how to interpret each section.

## Design intent

This skill is not a writing assistant. It is a reliability layer.

Use scripts for deterministic checks.
Use AI judgment for tone, search intent, framing, and final editorial decisions.
