---
name: sol-seo-health
description: Daily SEO health check — validates all blog posts for SEO completeness, checks sitemap, robots.txt, meta tags, broken links, and RSS feed.
version: 1.0.0
author: TheSolAI
permissions: ["file.read", "file.write", "http.request"]
---

# Sol SEO Health Check

Daily automated SEO audit for thesolai.github.io. Catches issues before they become problems.

## What it checks

- All blog posts have title, description, image, canonical URL
- OG tags present on every post
- No broken internal links
- `sitemap.xml` present and non-empty
- `robots.txt` references sitemap
- No duplicate post titles
- RSS feed present
- SKILL.md files have frontmatter

## Schedule

Runs **daily after site build** via launchd.

## Output

Logs to `logs/sol-seo.log`. Reports issues count with individual problem listings.

## Setup

Requires site repo at `/Users/amre/Projects/thesolai.github.io`

## Source

`scripts/content-pipeline/seo-health.py` in [sol-skills-bundle](https://github.com/TheSolAI/sol-skills-bundle)
