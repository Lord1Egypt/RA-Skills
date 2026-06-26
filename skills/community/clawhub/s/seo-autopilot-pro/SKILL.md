---
name: seo-autopilot
description: |
  Fully automated SEO content freshness engine. Monitors a keyword research reports
  directory, automatically generates landing pages and blog posts, runs SEO audits,
  and pushes updates. Use when: you need to keep SEO content fresh without manual
  publishing, you want to automate the flow from keyword research to live pages, or
  you need a pipeline that converts keyword reports into deployed web pages.
  Works with Next.js, Astro, Nuxt, and static site frameworks.
  Trigger phrases: "automate SEO content", "keyword report to page", "auto-generate
  SEO pages", "content freshness engine", "deploy SEO pages automatically"
---

# SEO Autopilot

Turns keyword research reports into deployed SEO pages, zero manual work.

## What It Does

When an external Agent (like OpenClaw) regularly generates keyword research reports
and pushes them to a Git repo, this skill handles everything else:

1. Detects new reports (git autofetch + fileCreated hook)
2. Parses Top keywords and recommended actions from the report
3. Deduplicates against existing pages
4. Decides page type (landing page vs blog post)
5. Generates page code matching your project style
6. Runs SEO audit (Technical + EEAT checks)
7. Pushes to git (triggers auto-deploy)

## Automation Flow

```
External Agent generates report -> git push
  -> IDE auto-fetches every 2 min
  -> fileCreated hook triggers Agent
  -> Agent runs 8-phase pipeline
  -> git push -> auto-deploy to production
```

## Setup (Agent Runs This)

### Step 1: Discover Project Structure

Identify:
- Framework type (Next.js / Astro / Nuxt / static)
- Page system (how pages are created)
- Blog system (how posts are stored)
- Navigation/sitemap registration method
- Existing SEO patterns (metadata, JSON-LD, canonical)
- Report directory location

### Step 2: Configure Git Auto-Fetch

Update `.vscode/settings.json`:

```json
{
  "git.autofetch": true,
  "git.autofetchPeriod": 120,
  "git.autoStash": true,
  "git.pullOnFetch": true
}
```

Only merge these keys, do not overwrite existing settings.

### Step 3: Create fileCreated Hook

Create a Kiro hook listening on the report directory:

```json
{
  "name": "SEO Autopilot",
  "version": "1.0.0",
  "when": {
    "type": "fileCreated",
    "patterns": ["{report_dir}/*.md"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "New keyword report detected. Execute the full #seo-autopilot pipeline: parse report -> deduplicate -> decide page types -> generate pages (max 3) -> register navigation + sitemap -> SEO audit -> git commit and push -> update processed.json."
  }
}
```

### Step 4: Create Steering File

Create `.kiro/steering/seo-autopilot.md` with the full 8-phase processing instructions.

### Step 5: Initialize State Tracking

Create `{report_dir}/processed.json`:

```json
{ "processed": [] }
```

### Step 6: Verify

- autofetch + pullOnFetch configured in settings.json
- Hook file created
- Steering file created
- processed.json initialized
- At least one report available for testing

### Step 7: Test Run

Run the full pipeline on an existing report to verify all steps work.

## 8-Phase Processing Pipeline

### Phase 0: Discover New Reports
Read processed.json -> scan report dir -> filter unprocessed reports

### Phase 1: Parse Report
Extract Top keywords, search intent, competition, recommended page type

### Phase 2: Deduplicate
Compare against existing pages (navigation + blog), skip already-covered keywords

### Phase 3: Decide Page Type
- Transactional / Emotional -> landing page
- Informational -> blog post
- Max 3 pages per report

### Phase 4: Generate Content
Generate page code matching your project patterns (metadata, JSON-LD, FAQ, internal links, CTA)

### Phase 5: Register
Add to navigation system + sitemap

### Phase 6: SEO Audit
- Title < 60 chars with primary keyword
- Description < 160 chars
- Canonical URL
- JSON-LD WebPage + FAQ schema
- H1 unique with keyword
- 3-5 internal links
- CTA to main conversion page

### Phase 7: Commit and Push
git add -> commit -> push

### Phase 8: Update State
Update processed.json with report and pages created

## Report Format

Reports are Markdown with at least one of:
- "Top N keywords" or "Recommended actions" section listing keywords + priority
- Table with keyword / intent / competition / action columns

The Agent parses adaptively across different formats.

## State Tracking Format

```json
{
  "processed": [
    {
      "report": "2026-04-10-keyword-research.md",
      "processedAt": "2026-04-10",
      "pagesCreated": [
        { "type": "landing", "slug": "/personalized-tarot", "keyword": "personalized tarot card generator" }
      ],
      "skipped": [
        { "keyword": "oracle card generator AI", "reason": "Already covered by /ai-oracle-card-generator" }
      ]
    }
  ]
}
```

## Framework Adaptation

| Framework | Page Location | Blog Location | Sitemap |
|-----------|--------------|---------------|---------|
| Next.js (App Router) | app/{slug}/page.tsx | lib/blog.ts or content/blog/*.mdx | app/sitemap.ts |
| Next.js (Pages Router) | pages/{slug}.tsx | pages/blog/[slug].tsx | next-sitemap.config.js |
| Astro | src/pages/{slug}.astro | src/content/blog/*.md | astro.config.mjs |
| Nuxt | pages/{slug}.vue | content/blog/*.md | nuxt.config.ts |
| Static HTML | {slug}/index.html | blog/{slug}/index.html | sitemap.xml |

## Limitations

- IDE must stay open (hook only runs when IDE is active)
- Max 3 pages per report (prevents quality drop)
- Semantic deduplication, not just URL matching
- Only creates new pages, never overwrites existing content
- Requires network for git operations

## Prerequisites

| Dependency | Required |
|-----------|----------|
| Git repo (GitHub/GitLab/Bitbucket) | Yes |
| External keyword report source | Yes |
| Web framework (Next.js/Astro/Nuxt/static) | Yes |
| Auto-deploy (Vercel/Cloudflare/Netlify) | Yes |
| IDE stays open (Kiro/Claude Code/Cursor) | Yes |
