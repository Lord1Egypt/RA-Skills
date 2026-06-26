---
name: seo-intel
description: >
  Local SEO competitive intelligence tool. Use when the user asks about SEO analysis, competitor research,
  keyword gaps, content strategy, site audits, AI citability, or wants to crawl/analyze websites. Covers: setup,
  crawling, extraction, analysis, AEO (AI citability scoring), keyword invention, content briefs, dashboards,
  agentic exports, suggestive SEO, and competitive action planning.
  Also use when asked to generate implementation briefs from SEO data, compare sites, audit AI citability,
  or suggest what pages/docs/features to build based on competitor intelligence.
  Includes gap-intel for topic/content gap analysis between your site and competitors.
---

# SEO Intel (v1.5.21)

Local SEO competitive intelligence — crawl your site + competitors, extract structure and semantic signals, then use OpenClaw to reason over the data and drive real implementation.

**OpenClaw is the recommended primary experience.** Standalone local Qwen handles extraction fine. But analysis, gap synthesis, and "what should I build next" reasoning needs a real model — Opus, Sonnet, GPT — and OpenClaw routes that automatically. No API keys to manage, no model config, just results.

## Install

```bash
npm install -g seo-intel
seo-intel setup      # detects OpenClaw automatically, configures everything
```

## Pipeline

```
Crawl → Extract (Ollama local) → Analyze (OpenClaw cloud model) → AEO → Export Actions → Implement
```

| Stage | Command | Gate | Best engine |
|---|---|---|---|
| **Scan** | `seo-intel scan <domain>` | Solo | Full pipeline (no config) |
| Crawl | `seo-intel crawl <project>` | Free | Playwright |
| Extract | `seo-intel extract <project>` | Solo | Ollama / Gemma 4 or Qwen local |
| Analyze | `seo-intel analyze <project>` | Solo | OpenClaw (Opus/Sonnet) |
| AEO | `seo-intel aeo <project>` | Solo | Pure local (no AI needed) |
| Watch | `seo-intel watch <project>` | Free | Pure local (diff engine) |
| Keywords | `seo-intel keywords <project>` | Solo | OpenClaw (Opus/Sonnet) |
| Blog Draft | `seo-intel blog-draft <project>` | Solo | Cloud LLM (Gemini/Claude/GPT) |
| Actions | `seo-intel export-actions <project>` | Free (technical) / Solo (full) | SQL heuristics |
| Dashboard | `seo-intel serve` | Free (limited) / Solo (full) | HTML |

### Agent interpretation rule

Do **not** treat SEO Intel as just a report generator. It is a decision layer.

Agents using this skill should interpret outputs like this:
- **crawl** = structural ground truth (pages, headings, links, schemas, domain roles)
- **extract** = semantic layer (entities, intent, CTAs, page types, signals)
- **analyze / gap-intel / keywords / competitive-actions** = what competitors prove is working or missing
- **aeo** = whether pages are shaped for AI citation and answer engines
- **watch** = what changed since last crawl — regressions, new pages, content shifts
- **export-actions / brief / suggest-usecases / blog-draft** = implementation-ready next steps

When helping a docs writer, page builder, or implementation agent:
1. identify what competitors cover that the target does not
2. identify where the target exists but is weaker / shallower / less citable
3. convert those gaps into concrete pages, docs, comparison pages, landing pages, schema fixes, or brief-driven updates
4. prefer evidence-backed actions over vague “do more SEO” advice

## Core Commands

```bash
seo-intel scan <domain>            # One-shot full audit (no config needed)
seo-intel setup                    # First-time wizard — detects OpenClaw
seo-intel crawl <project>          # Crawl target + competitors
seo-intel extract <project>        # Local AI extraction (Ollama)
seo-intel analyze <project>        # Strategic gap analysis → Intelligence Ledger
seo-intel aeo <project>            # AI Citability Audit — score pages for AI citation
seo-intel keywords <project>       # Keyword Inventor — traditional + AI/agent queries
seo-intel brief <project>          # Generate content briefs for new pages
seo-intel gap-intel <project>      # Topic/content gap analysis vs competitors (Solo)
seo-intel watch <project>          # Site health monitor — diff between crawl runs
seo-intel blog-draft <project>     # Generate AEO-optimised blog post draft (Solo)
seo-intel html <project>           # Generate dashboard
seo-intel serve                    # Web dashboard at localhost:3000
seo-intel status                   # Data freshness + summary
seo-intel run                      # Full pipeline: crawl → extract → analyze → dashboard
seo-intel guide                    # Interactive chapter-based walkthrough
seo-intel export <project>         # Raw data export (JSON/CSV)
```

### Scan — One-Shot Full Audit (v1.5.21+)

Zero-config audit pipeline. Just pass a domain — no project setup, no competitor config needed.

```bash
seo-intel scan carbium.io                # Full pipeline with AI-enriched export
seo-intel scan carbium.io --no-ai        # Deterministic export only (no LLM enrichment)
seo-intel scan carbium.io --pages 50     # Limit crawl to 50 pages
seo-intel scan carbium.io --model claude # Use Claude instead of Gemini
seo-intel scan carbium.io --no-stealth   # Disable stealth browser mode
```

**Pipeline:** crawl (stealth) → extract (Ollama) → analyze (Gemini/Claude) → AI-enriched markdown export.

Output: `reports/scan-<domain>-<date>.md` — full report with filled tables, instruction blocks, and AI action plan.

**Dashboard export:** The web dashboard (`seo-intel serve`) has per-card download buttons (MD/JSON/CSV) and profile-based export via `/api/export/download`.

### Export Report (v1.5.21+)

Single unified export — everything actionable in one file. Sections: Technical Scorecard, Site Watch, Technical Gaps, Quick Wins, Keyword Gaps, Long-tails, New Pages, Content Gaps, Positioning, AI Citability, Internal Links, Schema Types, Keyword Ideas.

**Deterministic fills:** Empty table columns are now auto-filled from DB data (long-tail parents, content gap suggestions, keyword potential, page rationale). Instruction blocks between sections explain how to use each data set.

**AI Smart Export:** Toggle in dashboard opens a popup with swarm animation + progress bar. Gemini enriches the report: fills remaining gaps, scores priorities, adds a top-10 AI Action Plan. Non-blocking (async spawn).

Formats: Markdown, JSON, CSV, ZIP. API: `/api/export/download?project=<name>&format=<md|json|csv|zip>&ai=true`

Per-card exports (MD/JSON/CSV) on individual dashboard cards still work for granular downloads.

## Full Command Surface

Use this section when an isolated agent needs the whole toolbox in one place.

### Setup / Core Flow

```bash
seo-intel scan <domain>            # One-shot full audit (no config needed)
seo-intel setup                    # First-time wizard — detects OpenClaw
seo-intel guide                    # Interactive chapter-based walkthrough
seo-intel status                   # Data freshness + system summary
seo-intel serve                    # Web dashboard at localhost:3000
seo-intel html <project>           # Generate dashboard HTML
seo-intel run <project>            # Full pipeline: crawl → extract → analyze → dashboard
seo-intel export <project>         # Raw data export (JSON/CSV)
```

### Pipeline Commands

```bash
seo-intel crawl <project>          # Crawl target + competitors
seo-intel extract <project>        # Local AI extraction (Ollama)
seo-intel analyze <project>        # Strategic competitive analysis
seo-intel aeo <project>            # AI citability audit
seo-intel watch <project>          # Site health monitor — diff between crawl runs
seo-intel keywords <project>       # Traditional + AI/agent keyword discovery
seo-intel brief <project>          # Content brief generation
seo-intel blog-draft <project>     # AEO-optimised blog post draft
seo-intel gap-intel <project>      # Topic/content gap analysis vs competitors
```

### Agentic / Implementation Commands

```bash
seo-intel export-actions <project>                     # Action export (technical by default / full in Solo)
seo-intel export-actions <project> --scope technical   # Technical fixes from crawl data
seo-intel export-actions <project> --scope all         # Combined action export
seo-intel competitive-actions <project>                # Competitor-backed action list
seo-intel suggest-usecases <project>                   # Suggest missing pages/docs/features
```

### Audit / Analysis Commands

```bash
seo-intel schemas <project>           # Schema coverage audit
seo-intel headings-audit <project>    # H1-H6 structure analysis
seo-intel orphans <project>           # Orphan page/entity detection
seo-intel entities <project>          # Entity/topic mapping
seo-intel friction <project>          # Intent/CTA friction detection
seo-intel velocity <project>          # Content publishing velocity
seo-intel decay <project>             # Content freshness / decay detection
seo-intel js-delta <project>          # JS-rendered vs raw HTML changes
seo-intel shallow <project>           # Thin/shallow content opportunity scan
seo-intel templates <project>         # URL pattern / content type mapping
```

### Project Management Commands

```bash
seo-intel competitors <project>                    # List competitors
seo-intel competitors <project> --add rival.com   # Add competitor
seo-intel competitors <project> --remove rival.com# Remove competitor
seo-intel subdomains <domain>                     # Discover subdomains
```

## Analysis & Audit Commands

```bash
seo-intel aeo <project>            # AI Citability Audit (0-100 per page, 6 signals)
seo-intel keywords <project>       # Keyword Inventor (traditional + Perplexity + agent queries)
seo-intel brief <project>          # Content brief generation for gap pages
seo-intel templates <project>      # URL pattern analysis and content type mapping
seo-intel entities <project>       # Entity extraction and topic mapping (Ollama)
seo-intel schemas <project>        # Schema.org markup audit
seo-intel headings-audit <project> # H1-H6 structure analysis
seo-intel orphans <project>        # Find orphan pages (no internal links)
seo-intel decay <project>          # Content freshness and decay detection
seo-intel friction <project>       # UX friction and conversion blocker detection (Ollama)
seo-intel velocity <project>       # Content publishing velocity tracking
seo-intel js-delta <project>       # JavaScript dependency change detection
seo-intel shallow <project>        # Quick technical audit (no full crawl needed)
seo-intel competitors <project>    # Manage competitor list
seo-intel subdomains <domain>      # Subdomain discovery
seo-intel gap-intel <project>      # Topic gap analysis vs competitor domains (Solo)
seo-intel watch <project>          # Site health monitor — diff between crawl runs (Solo)
seo-intel blog-draft <project>     # AEO-optimised blog post draft (Solo)
```

## Site Watch — Health Monitoring & Change Detection (v1.4.2+)

Tracks crawl-to-crawl changes and computes a site health score (0-100) from page errors, missing titles, and missing H1s. Site Watch is available on the free tier and auto-runs after every crawl.

```bash
seo-intel watch <project>                # Brief health report
seo-intel watch <project> --format json  # Structured JSON output
```

**How it works:**
- First run captures a baseline snapshot
- Subsequent runs diff against the previous snapshot
- Significant changes feed into the Intelligence Ledger as `site_watch` insights
- Dashboard shows the Site Watch card with health score, trend arrows, severity deltas, and a “What’s New” event feed
- Available via CLI, dashboard terminal, and programmatic API: `run('watch', project)`

**Detected event types (10):**
- `page_added`
- `page_removed`
- `status_changed`
- `new_error`
- `title_changed`
- `h1_changed`
- `meta_desc_changed`
- `word_count_changed`
- `indexability_changed`
- `content_changed`

**Severity classes:** `critical`, `warning`, `notice`

**Agent use:** Run `watch` after every crawl to detect regressions early. If the health score drops, investigate critical/warning events before spending cycles on higher-order analysis.

## Blog Draft — AEO-Optimised Content Generation (v1.3.0)

Generates blog post drafts from Intelligence Ledger data — keyword gaps, citability insights, and competitor patterns feed into structured markdown with frontmatter.

```bash
seo-intel blog-draft <project>                          # Auto-pick topic from ledger
seo-intel blog-draft <project> --topic "api security"   # Specific topic
seo-intel blog-draft <project> --lang fi                # Finnish
seo-intel blog-draft <project> --model claude --save    # Use Claude, save to reports/
```

**Models:** gemini (default), claude, gpt, deepseek

Solo tier only.

## Gap Intel — Topic Coverage Gap Analysis (v1.4.0)

Compares your crawled pages against competitor domains to surface topic gaps — content they cover that you don't, and depth gaps where they go deeper.

```bash
seo-intel gap-intel <project>                          # vs all crawled competitors
seo-intel gap-intel <project> --vs helius,quicknode   # specific competitors
seo-intel gap-intel <project> --type docs              # filter to doc pages only
seo-intel gap-intel <project> --raw                   # skip LLM, raw topic matrix
seo-intel gap-intel <project> --out ./gap-report.md   # write to file
```

**Output:** Prioritised gap report (High/Medium/Low buyer intent) with:
- Topics competitors cover → you don't
- Depth gaps (you have 1 page, they have 5)
- Topics where you lead
- Raw topic matrix per domain

Use `--out ~/clawd/projects/carbium/docs-mirror/waiting-room/gap-intel-latest.md` to feed the docs pipeline automatically.

Solo tier only.

## Default Extraction Model

**Gemma 4 e4b** is now the default extraction model (replaces Qwen 3 4B).

| Model | Size | Speed | Tier |
|-------|------|-------|------|
| `gemma4:e2b` | 6.7 GB | ~47 t/s | Budget |
| `gemma4:e4b` | 8.9 GB | ~23 t/s | **Balanced (default)** |
| `gemma4:26b` | ~18 GB | — | Quality |
| `gemma4:31b` | ~20 GB | — | Power |

All Qwen models remain available. Change model via `seo-intel setup` or edit `config/<project>.json`.

## AEO — AI Citability Audit (v1.2.0)

Score every page for how well AI assistants (ChatGPT, Perplexity, Claude) can cite it. This is not traditional SEO — it's Answer Engine Optimization.

```bash
seo-intel aeo <project>                # Full citability audit
seo-intel aeo <project> --target-only  # Skip competitor scoring
seo-intel aeo <project> --save         # Export .md report
```

**6 citability signals** scored per page:
- **Entity authority** — Is this page the canonical source for its entities?
- **Structured claims** — "X is Y because Z" patterns that AI can quote directly
- **Answer density** — Ratio of direct answers to filler content
- **Q&A proximity** — Question heading → answer paragraph pattern
- **Freshness** — dateModified, schema, "Updated March 2026" signals
- **Schema coverage** — JSON-LD structured data present

**AI Query Intent classification:** synthesis, decision support, implementation, exploration, validation

Low-scoring pages automatically feed into the Intelligence Ledger as `citability_gap` insights.

## Intelligence Ledger

Insights from `analyze`, `keywords`, and `aeo` **accumulate across runs** — they're never overwritten. The ledger uses fingerprint-based dedup: same insight found again = updated timestamp, not duplicated.

- Mark insights as **done** (fix applied) or **dismissed** (not relevant)
- Dashboard shows all active insights with done/dismiss buttons
- `POST /api/insights/:id/status` to toggle status programmatically

## Agentic Export Commands

These turn crawl data into prioritized implementation briefs. The right inputs for coding agents, docs writers, or any downstream workflow.

### Technical Audit (Free tier)
```bash
seo-intel export-actions <project> --scope technical
seo-intel export-actions <project> --scope technical --format json
```
Finds: missing schemas, broken links, orphan pages, thin content, deep pages, missing H1/meta, canonical issues. Works without AI — pure crawl data.

### Competitive Gaps (Solo)
```bash
seo-intel competitive-actions <project>
seo-intel competitive-actions <project> --vs helius.dev
seo-intel competitive-actions <project> --format json
```
Finds: content gaps, keyword gaps, schema coverage delta, topic authority gaps, missing trust/comparison pages. Needs extraction + analysis to have run first.

### Suggest What to Build (Solo)
```bash
seo-intel suggest-usecases <project>
seo-intel suggest-usecases <project> --scope docs
seo-intel suggest-usecases <project> --scope product-pages
seo-intel suggest-usecases <project> --scope onboarding
```
Infers what pages, docs, or features should exist based on competitor patterns. Uses the local intelligence DB to reason about what's missing, not just what's broken.

### Combined
```bash
seo-intel export-actions <project> --scope all --format json
seo-intel export-actions <project> --scope all --format brief
```

## How isolated writer / docs agents should use this skill

If the agent is writing docs, landing pages, comparison pages, or implementation briefs in an isolated environment, use this order:

1. **Establish reality**
   - use `crawl`, `watch`, `schemas`, `headings-audit`, `status`
   - identify target vs competitor coverage, detect regressions from previous crawl
2. **Understand meaning**
   - use `extract`, `entities`, `keywords`, `gap-intel`
   - determine what themes, intents, and problem clusters competitors cover
3. **Prioritise action**
   - use `competitive-actions`, `export-actions`, `suggest-usecases`, `brief`
   - convert findings into pages/features/docs, not abstract insights
4. **Shape for answer engines**
   - use `aeo`
   - improve citability, answer density, structured claims, schema, and entity authority

### Interpretation heuristics for agents

- If competitors have whole topic clusters the target lacks → create **net-new pages or docs**
- If the target has the page but competitors go deeper → create **rewrite / expansion brief**
- If trust/comparison/integration pages are missing → create **commercial-intent pages**
- If schema / headings / orphan issues dominate → start with **technical actions**
- If AEO scores are low on important pages → restructure for **AI-citable answers**
- If `suggest-usecases` and `gap-intel` overlap on the same topic → treat that as a **high-confidence build target**

## How to use SEO Intel reports for automation

For automation, treat SEO Intel as the upstream decision layer, not a live database you rediscover every run.

### Prefer stable report artifacts over raw discovery

Automation should prefer:
- fixed-path exports like `waiting-room/gap-intel-latest.md`
- project-level aliases like `reports/<project>-latest-analysis.json`
- short docs-facing briefs like `reports/<project>-docs-brief.md`

Automation should avoid depending on:
- ad hoc CLI discovery
- guessing the newest timestamped file in multiple places
- direct `seo-intel.db` queries unless the workflow is explicitly advanced/custom

If timestamped files are all you have, read the newest `reports/<project>-analysis-*.json` and then normalize it into one stable handoff file for the downstream automation.

### What to read from the reports

The main report to automate against is the analysis export:

```text
reports/<project>-analysis-*.json
```

Useful keys:
- `new_pages` = net-new page candidates
- `content_gaps` = topics competitors cover that you do not, or where your coverage is materially weaker
- `keyword_gaps` = missing demand clusters or landing/doc opportunities
- `long_tails` = specific problem-led queries worth docs/blog coverage
- `quick_wins` = existing pages that can be improved quickly
- `technical_gaps` = crawl-backed fixes, usually for technical/site work rather than net-new content

Other high-value exports:
- `gap-intel` output = competitor-backed topic and depth gaps
- `competitive-actions` output = prioritized strategic actions
- `export-actions --scope technical` = technical fixes from crawl data
- `aeo` output = weakest pages by AI citability, answer density, and claim structure
- `suggest-usecases` output = inferred missing docs/pages/features based on competitor patterns

### Recommended automation mapping

Use the report fields like this:
- `new_pages` → create-page queue
- `content_gaps` → docs/product/content gap queue
- `keyword_gaps` → landing page, glossary, comparison, or docs opportunity queue
- `long_tails` → problem-led docs, recipes, or blog queue
- `quick_wins` → rewrite queue for weak existing pages
- `technical_gaps` → engineering/site-health queue

For docs automations specifically:
1. read the latest analysis JSON
2. read the latest `gap-intel` markdown if present
3. identify:
   - topics competitors cover that you lack entirely
   - existing pages with weak coverage or weak citability
   - overlap between `suggest-usecases`, `content_gaps`, and `aeo`
4. collapse that into one short docs brief with:
   - top 3 new pages to create
   - top 3 pages to rewrite
   - why they matter
   - competitor proof
   - blockers / confidence notes
5. let the downstream docs agent choose only from that brief, not from raw DB state

### Suggested handoff pattern

For recurring docs pipelines, create a stable file like:

```text
reports/<project>-docs-brief.md
```

Recommended sections:
- `New Pages to Create`
- `Content Gaps`
- `Weak Existing Pages`
- `Competitor Proof`
- `Blockers`
- `Best Next Pick`

This is the simplest way to make downstream automation reliable. The SEO Intel job does the heavy analysis once; docs/product automations consume a short, fixed-format brief instead of rediscovering the entire workspace each run.

## OpenClaw Workflow (Recommended)

When running inside OpenClaw, the full intelligence loop becomes conversational:

### "How citable is my site for AI assistants?"
1. Run `seo-intel aeo <project>`
2. Review citability scores — pages scoring <35 need restructuring
3. Check weakest signals (schema coverage, Q&A proximity, structured claims)
4. Generate briefs for low-scoring pages: `seo-intel brief <project>`
5. Implement restructuring → re-crawl → re-score to measure lift

### "What should I build next?"
1. Run `seo-intel suggest-usecases <project> --format json`
2. Read the output — it contains prioritized suggestions with competitor evidence
3. Cross-reference against workspace context (what's already built)
4. Generate implementation briefs for the top actions
5. Spawn a coding/docs agent to execute
6. Re-crawl after shipping to measure delta

### "Where are my biggest competitive gaps?"
1. Run `seo-intel competitive-actions <project> --format json`
2. Analyze: which gaps are highest priority, which competitors are strongest in each area
3. Map gaps to existing projects/docs/roadmap
4. Produce a prioritized action plan

### "What's technically broken on my site?"
1. Run `seo-intel export-actions <project> --scope technical --format json`
2. Triage by priority: critical → high → medium
3. Assign quick wins (missing H1, meta) vs structural work (canonical chains, orphans)

### "What keywords should I target — including AI search?"
1. Run `seo-intel keywords <project> --save`
2. Review: traditional keywords, Perplexity-style questions, agent queries
3. Cross with AEO scores to find high-value + low-citability gaps
4. Generate briefs: `seo-intel brief <project>`

## Deploy Loop — Applying Fixes via Wrangler

SEO Intel tells you what's wrong and what to build. Wrangler deploys it. Agents can close the loop end-to-end.

### Setup (once)

```bash
npm install -g wrangler
wrangler login        # opens browser for Cloudflare OAuth
```

The site needs a `wrangler.toml` in its root:
```toml
name = "your-cloudflare-project-name"
compatibility_date = "2024-01-01"
assets = { directory = "." }
```

And a `.wranglerignore` to keep internal files off the public site:
```
.DS_Store
.claude/
.wrangler/
deploy.sh
wrangler.toml
```

### Deploy

```bash
cd /path/to/site && wrangler deploy
```

Only changed files are uploaded. Deploy is instant and global (Cloudflare edge, no staging).

---

### "SEO Intel found issues — fix and deploy"

1. Run analysis to get findings
   ```bash
   seo-intel aeo <project> --format json
   seo-intel export-actions <project> --scope technical --format json
   seo-intel schemas <project> --format json
   ```

2. Apply fixes to static HTML based on findings:

   | SEO Intel finding | What to fix in the HTML |
   |---|---|
   | Low schema coverage (AEO) | Add/update `<script type="application/ld+json">` blocks |
   | Low answer density (AEO) | Add direct-answer paragraphs after H2/H3 headings |
   | Low Q&A proximity (AEO) | Add FAQ sections: `<h3>` question + `<p>` answer |
   | Low freshness signal (AEO) | Add `dateModified` to JSON-LD, add "Updated [date]" near content |
   | Schema gap vs competitors | Add the missing `@type` to JSON-LD |
   | Missing meta tags | Add `og:title`, `og:description`, `twitter:card`, `meta description` |
   | Missing hreflang | Add `<link rel="alternate" hreflang="...">` pairs in `<head>` |
   | Content/topic gap | Create new page, update `sitemap.xml` and `llms.txt` |
   | Version drift | Update `softwareVersion` in JSON-LD, nav badge, `llms.txt`, `skill.md` |

3. Deploy
   ```bash
   cd /path/to/site && wrangler deploy
   ```

4. Re-crawl to verify lift
   ```bash
   seo-intel crawl <project> --scope new
   seo-intel aeo <project>
   ```

---

### Keeping llms.txt / skill.md in sync after releases

After any version bump or feature release, update and redeploy. Also keep public listing surfaces aligned, not just local docs:

```bash
# Update skill.md from source
cp /path/to/seo-intel/skill/SKILL.md /path/to/site/seo-intel/skill.md

# Update version references in llms.txt and llms-ctx.txt
# (sed or agent edit — bump version number, update feature list)

# Deploy
cd /path/to/site && wrangler deploy
```

Files/surfaces that must stay in sync on every version bump:
- `skill/SKILL.md`
- public site `seo-intel/skill.md` — copy from `skill/SKILL.md`
- public site `llms.txt` — version number + feature summary
- public site `llms-ctx.txt` — full context, version number, feature descriptions
- JSON-LD `softwareVersion` on product pages
- nav / hero version badges in HTML
- ClawHub listing / manifest text and runtime expectation disclosure
- `CHANGELOG.md`

---

### Safety rules for deploy agents

- **Always read a file before editing it** — never blind-write HTML
- **Never change pricing or contact info** without explicit instruction
- **Keep all version references consistent** — JSON-LD, badge, llms.txt must all match
- **Deploy is live immediately** — no staging, no undo. Be deliberate.

## Direct DB Queries (Advanced)

The SQLite DB at `./seo-intel.db` (in your working directory) can be queried directly for custom reasoning.

Key tables: `pages`, `domains`, `headings`, `links`, `extractions`, `analyses`, `insights`, `citability_scores`

Key pattern — what competitors have that target doesn't:
```sql
-- Topic clusters in competitor pages missing from target
SELECT DISTINCT h.text FROM headings h
JOIN pages p ON p.id = h.page_id
JOIN domains d ON d.id = p.domain_id
WHERE d.role = 'competitor' AND d.project = 'myproject' AND h.level <= 2
AND h.text NOT IN (
  SELECT h2.text FROM headings h2
  JOIN pages p2 ON p2.id = h2.page_id
  JOIN domains d2 ON d2.id = p2.domain_id
  WHERE d2.role = 'target' AND d2.project = 'myproject' AND h2.level <= 2
);
```

```sql
-- Pages with low AI citability that have high keyword potential
SELECT cs.url, cs.total_score, cs.weakest_signal, i.data
FROM citability_scores cs
JOIN insights i ON i.project = cs.project AND i.type = 'long_tail' AND i.status = 'active'
WHERE cs.project = 'myproject' AND cs.total_score < 35
ORDER BY cs.total_score ASC;
```

## Programmatic API (for platform integrations)

All commands support `--format json` for structured output. For deep integration, use the programmatic API:

```javascript
import { run, capabilities, pipeline } from 'seo-intel/froggo';

// Unified runner — one function, all commands
const aeoResult = await run('aeo', 'myproject');
const gaps = await run('gap-intel', 'myproject', { vs: ['competitor.com'] });
const brief = await run('brief', 'myproject', { days: 7 });

// Every result: { ok, command, project, timestamp, data }
if (aeoResult.ok) {
  console.log(aeoResult.data.summary.avgTargetScore);
}

// Capability introspection
capabilities.forEach(c => console.log(c.id, c.phase, c.tier));

// Dependency graph for orchestration
pipeline.graph['entities']; // → ['extract']
```

Available: `aeo`, `gap-intel`, `watch`, `shallow`, `decay`, `headings-audit`, `orphans`, `entities`, `schemas`, `friction`, `brief`, `velocity`, `js-delta`, `export-actions`, `competitive-actions`, `suggest-usecases`, `blog-draft`, `insights`, `status`

See `AGENT_GUIDE.md` for full orchestration patterns.

## Cron Scheduling

```bash
# Daily crawl (14:00 recommended)
seo-intel crawl <project>

# Weekly analysis + AEO + brief (Sunday)
seo-intel analyze <project> && seo-intel aeo <project> && seo-intel export-actions <project> --format brief
```

For ongoing operator summaries, treat `reports/` as a folder-aware signal surface, not a one-file source. In practice, the most useful recurring artifacts are:
- `triage-continuous.md`
- latest dated `triage-YYYY-MM-DD.md`
- latest `bugscan-*`
- optional `bugfix-*`
- optional `cross-debate-*`
- optional briefs when they actually exist

Wire via OpenClaw cron for proactive briefings delivered to your chat.

## Pricing

| Tier | Price | Features |
|---|---|---|
| Free | €0 | Unlimited crawl, technical exports, crawl-only dashboard, Site Watch |
| Solo | €19.99/mo or €199.99/yr | Full AI pipeline, AEO, all exports, full dashboard |

Solo via [ukkometa.fi/seo-intel](https://ukkometa.fi/en/seo-intel/).
