# SEO Intel — Agent Integration Guide

Machine-readable guide for AI agents using SEO Intel as a module.

## Quick Start

```javascript
import { run, capabilities, pipeline } from 'seo-intel/froggo';

// Run any command — always returns structured JSON
const result = await run('aeo', 'myproject');
// → { ok: true, command: 'aeo', project: 'myproject', timestamp: '...', data: { scores, summary } }

// List all available capabilities
capabilities.forEach(c => console.log(c.id, c.description));

// Check dependency order
pipeline.graph['gap-intel']; // → ['crawl', 'extract']
```

## Pipeline Order

SEO Intel follows a strict dependency pipeline. Agents must respect this order:

```
Phase 1: COLLECT    crawl → pages + structure stored in SQLite
Phase 2: EXTRACT    extract → keywords, entities, intent, CTAs (requires Ollama)
Phase 3: ANALYZE    analyze, aeo, watch, shallow, decay, entities, schemas, friction, keywords, etc.
Phase 4: REPORT     brief, velocity, html, serve
Phase 5: CREATE     gap-intel, export-actions, competitive-actions, suggest-usecases, blog-draft
```

### Practical interpretation layer

Agents should map command outputs to work decisions like this:

| Signal type | Main commands | What it means for downstream work |
|---|---|---|
| Structural truth | `crawl`, `watch`, `schemas`, `headings-audit`, `orphans` | what exists, how it is shaped, what changed, and what is technically broken |
| Semantic truth | `extract`, `entities`, `keywords`, `friction` | what the pages are actually about, who they serve, and where intent mismatches happen |
| Competitive proof | `analyze`, `gap-intel`, `competitive-actions` | what competitors cover that the target lacks or covers weakly |
| AI-answer fitness | `aeo` | whether pages are shaped to be cited by ChatGPT / Perplexity / Claude |
| Implementation layer | `brief`, `export-actions`, `suggest-usecases`, `blog-draft` | what to build, fix, rewrite, expand, or publish next |

For isolated docs/page-builder agents: do not stop at “competitor X has this topic.” Convert that into a page brief, doc section, comparison page, schema fix, rewrite plan, or action list.

**Rules:**
- `crawl` must run before ANY analysis
- `extract` must run before: orphans, entities, friction, gap-intel, blog-draft
- `aeo` only needs crawl data (no extraction needed)
- `schemas` only needs crawl data
- Most analysis commands are independent — can run in parallel after dependencies met

## Model Selection Guidance

Use the right model tier for each phase — don't over-allocate:

| Phase | Task type | Recommended model | Why |
|-------|-----------|-------------------|-----|
| Extract | Structured data extraction | Light local: `gemma4:e2b` or `gemma4:e4b` | Pattern matching, not reasoning |
| Analyze (local) | AEO, schemas, decay, shallow | No model needed | Pure heuristics on crawl data |
| Analyze (LLM) | gap-intel, entities, friction | Light local: `gemma4:e4b` | Topic clustering, not deep reasoning |
| Synthesize | Strategic analysis, action plans | Cloud: Opus, Sonnet, GPT-4 | Needs real reasoning |
| Create | Blog drafts, content briefs | Cloud: Sonnet or equivalent | Creative + strategic |

**Principle:** Extraction is structured data work — use the lightest model that produces clean output. Reserve heavy models for synthesis and strategic reasoning.

## Full Command Surface

Use this as the single-source command map when the agent environment is isolated and cannot infer missing commands from the repo.

### Setup / Core

- `run('setup')` or CLI `seo-intel setup` — first-time setup wizard
- `run('status')` or CLI `seo-intel status` — project/system status
- CLI `seo-intel guide` — interactive walkthrough
- CLI `seo-intel serve` — open dashboard server
- CLI `seo-intel html <project>` — generate dashboard HTML
- CLI `seo-intel run <project>` — full pipeline run
- CLI `seo-intel export <project>` — raw JSON/CSV export

### Pipeline / Analysis

- `crawl`
- `extract`
- `analyze`
- `aeo`
- `keywords`
- `brief`
- `gap-intel`
- `schemas`
- `headings-audit`
- `orphans`
- `entities`
- `friction`
- `velocity`
- `decay`
- `js-delta`
- `shallow`
- `templates`
- `watch`

### Action / Execution Layer

- `export-actions`
- `competitive-actions`
- `suggest-usecases`
- `blog-draft`

### Project / Scope Management

- CLI `seo-intel competitors <project>`
- CLI `seo-intel competitors <project> --add <domain>`
- CLI `seo-intel competitors <project> --remove <domain>`
- CLI `seo-intel subdomains <domain>`

## Command Reference

### Collect Phase

**`run('crawl', project)`**
Crawl target + competitor domains. Stores pages, metadata, schemas in SQLite.
- Requires: Playwright (browser automation)
- Options: `{ stealth: true, maxPages: 100, scope: 'full|new|sitemap' }`
- Note: Long-running (minutes). Returns when complete.

**`run('extract', project)`**
Extract SEO signals from crawled pages using local LLM.
- Requires: Ollama running with gemma4:e4b (or configured model)
- Options: `{ model: 'gemma4:e4b' }`
- Note: Processes all un-extracted pages. Can take 5-60 minutes.
- **Model guidance:** Use the lightest model that produces acceptable extraction quality. `gemma4:e2b` (6.7 GB) is sufficient for most extraction tasks and runs at ~47 t/s. `gemma4:e4b` (8.9 GB) is the balanced default. For cloud-based extraction, use the lightest available model — extraction is structured data work, not reasoning. Reserve heavier models (Opus, Sonnet, GPT-4) for analysis and gap synthesis.

### Analyze Phase

**`run('aeo', project)`** — AI Citability Audit
- Returns: `{ target: PageScore[], competitors: Map, summary: { avgScore, tierCounts, weakestSignals } }`
- Use when: Agent needs to know which pages AI search engines will/won't cite

**`run('shallow', project, { maxWords: 700 })`** — Shallow Champion Attack
- Returns: `{ targets: Page[], totalTargets }`
- Use when: Finding easy wins — thin competitor pages you can outwrite

**`run('decay', project, { months: 18 })`** — Content Decay
- Returns: `{ confirmedStale: Page[], unknownFreshness: Page[] }`
- Use when: Finding stale competitor content to replace with fresh versions

**`run('orphans', project)`** — Orphan Entity Attack
- Returns: `{ orphans: [{ entity, domains, suggestedUrl }] }`
- Use when: Finding content opportunities — entities competitors mention but nobody owns
- Requires: extraction data

**`run('entities', project)`** — Entity Coverage Map
- Returns: `{ gaps, shared, unique, summary }`
- Use when: Understanding semantic coverage vs competitors
- Requires: extraction data

**`run('schemas', project)`** — Schema Intelligence
- Returns: `{ coverageMatrix, gaps, exclusives, ratings, pricing, actions }`
- Use when: Auditing structured data / rich results competitive position

**`run('friction', project)`** — Intent Friction Analysis
- Returns: `{ targets: FrictionTarget[], totalAnalyzed }`
- Use when: Finding competitor pages with mismatched CTA/intent
- Requires: extraction data

**`run('velocity', project, { days: 30 })`** — Content Velocity
- Returns: `{ velocities: DomainVelocity[], period }`
- Use when: Comparing publishing rates across domains

**`run('watch', project)`** — Site Health Watch
- Returns: `{ snapshot, events: WatchEvent[], healthScore: number, previousHealthScore, trend, isBaseline }`
- Use when: Checking what changed between crawl runs, monitoring site health over time
- Events: page_added, page_removed, status_changed, new_error, title_changed, h1_changed, meta_desc_changed, word_count_changed, indexability_changed, content_changed
- Note: Auto-runs after every crawl. Free tier.

**`run('gap-intel', project, { vs: ['competitor.com'] })`** — Topic Gap Analysis
- Returns: `{ report: 'markdown string with prioritised gaps' }`
- Use when: Finding what topics competitors cover that you don't
- Requires: Ollama for topic extraction

### Report Phase

**`run('brief', project, { days: 7 })`** — Weekly Intel Brief
- Returns: `{ competitorMoves, keywordGaps, schemaGaps, actions, period }`
- Use when: Getting a summary of what changed recently

### Export Phase

**`run('export-actions', project)`** — Technical fix list
**`run('competitive-actions', project)`** — Competitive action list
**`run('suggest-usecases', project)`** — AI-suggested pages to build
- All return: `{ actions: Action[] }` where Action has id, type, priority, title, why, evidence, implementationHints

### Create Phase

**`run('blog-draft', project, { topic: '...', lang: 'en' })`** — Blog Draft Generator
- Returns: `{ context, prompt }` — context is gathered data, prompt is ready for LLM

### Utility

**`run('insights', project)`** — Get active Intelligence Ledger items
**`run('status')`** — List all configured projects

## Agent Orchestration Patterns

### Full Site Audit
```javascript
// 1. Crawl
await run('crawl', project);
// 2. Extract (if Ollama available)
await run('extract', project);
// 3. Run all analyses in parallel (watch auto-runs after crawl, but can also be explicit)
const [aeo, watch, schemas, shallow, decay, entities, friction] = await Promise.all([
  run('aeo', project),
  run('watch', project),
  run('schemas', project),
  run('shallow', project),
  run('decay', project),
  run('entities', project),
  run('friction', project),
]);
// 4. Generate actions
const actions = await run('export-actions', project);
// 5. Brief
const brief = await run('brief', project);
```

### Quick Competitive Check
```javascript
await run('crawl', project);
const [schemas, velocity] = await Promise.all([
  run('schemas', project),
  run('velocity', project),
]);
```

### Content Gap Discovery
```javascript
await run('crawl', project);
await run('extract', project);
const [gaps, orphans, entities] = await Promise.all([
  run('gap-intel', project, { vs: ['competitor1.com', 'competitor2.com'] }),
  run('orphans', project),
  run('entities', project),
]);
```

### Doc Creator / Page Builder Pattern
```javascript
await run('crawl', project);
await run('extract', project);

const [gaps, actions, usecases, aeo] = await Promise.all([
  run('gap-intel', project),
  run('competitive-actions', project),
  run('suggest-usecases', project),
  run('aeo', project),
]);

// Then convert overlapping themes into:
// - new docs pages
// - comparison pages
// - integration pages
// - rewrites for weak existing pages
// - AEO/citability improvements on important pages
```

### Interpretation Rules for Isolated Agents

- If `gap-intel` shows missing topic clusters → plan **net-new content**
- If `competitive-actions` repeats the same area → raise priority
- If `aeo` is weak on important existing pages → prefer **rewrite/reshape** over creating more pages
- If `export-actions --scope technical` is noisy with structural issues → fix the site skeleton before sophisticated content work
- If `suggest-usecases` proposes docs/integration/comparison assets that competitors already validate → treat that as commercially meaningful evidence, not speculation

## Deploy Loop — Applying SEO Fixes via Wrangler

SEO Intel produces findings. Wrangler deploys fixes. Agents can close the loop automatically.

### Prerequisites

```bash
npm install -g wrangler
wrangler login         # OAuth via browser, once only
```

The target site needs a `wrangler.toml` in its root:

```toml
name = "your-cloudflare-project-name"
compatibility_date = "2024-01-01"
assets = { directory = "." }
```

And a `.wranglerignore` to keep internal files off the public site:

```
.DS_Store
.gitignore
.claude/
.wrangler/
deploy.sh
wrangler.toml
*.local.json
```

### Deploy Command

```bash
cd /path/to/site && wrangler deploy
```

Wrangler diffs against the last deployment — only changed files are uploaded.

---

### Full Analyze → Fix → Deploy Pattern

```javascript
import { run } from 'seo-intel/froggo';
import { execSync } from 'child_process';

const project = 'myproject';
const siteDir = '/path/to/site';

// 1. Analyze
const [aeo, schemas, gaps, actions] = await Promise.all([
  run('aeo', project),
  run('schemas', project),
  run('gap-intel', project),
  run('export-actions', project, { scope: 'technical', format: 'json' }),
]);

// 2. Agent applies fixes to site HTML/JSON files based on findings:
//    - JSON-LD schema gaps → add/update <script type="application/ld+json">
//    - Version numbers     → update softwareVersion, nav badges
//    - AEO weak signals    → restructure headings, add Q&A blocks, add dateModified
//    - Missing meta        → add og:title, og:description, twitter:card
//    - llms.txt / skill.md → update to match current feature set

// 3. Deploy
execSync(`cd ${siteDir} && wrangler deploy`, { stdio: 'inherit' });

// 4. Re-crawl to verify (optional — gives you a diff on next run)
await run('crawl', project, { scope: 'new' });
```

---

### What SEO Intel findings map to in static HTML

| Finding source | What to fix in the HTML |
|---|---|
| `aeo` — low schema coverage | Add/update `<script type="application/ld+json">` blocks |
| `aeo` — low answer density | Add direct-answer paragraphs after H2/H3 headings |
| `aeo` — low Q&A proximity | Add FAQ sections with `<h3>` question + `<p>` answer pairs |
| `aeo` — low freshness | Add `dateModified` to JSON-LD, add "Updated [date]" near content |
| `schemas` — competitors have, you don't | Add the missing `@type` to JSON-LD |
| `export-actions` — missing meta | Add `og:title`, `og:description`, `twitter:card`, `meta description` |
| `export-actions` — missing hreflang | Add `<link rel="alternate" hreflang="...">` pairs |
| `gap-intel` — topic gaps | Create new pages/sections, update `sitemap.xml` and `llms.txt` |
| Version drift | Update `softwareVersion` in JSON-LD, nav badges, `llms.txt`, `skill.md` |

---

### Keeping llms.txt / skill.md in sync

After any version bump or feature release, agents should also update:

- `llms.txt` — top-level AI context for the site (version, feature summary, links)
- `llms-ctx.txt` — full context file with detailed feature descriptions
- `seo-intel/skill.md` — mirrors the clawhub SKILL.md (copy from `seo-intel/skill/SKILL.md`)

Then redeploy:

```bash
cp /path/to/seo-intel/skill/SKILL.md /path/to/site/seo-intel/skill.md
cd /path/to/site && wrangler deploy
```

---

### Safety Rules for Deploy Agents

- **Never deploy without diffing first** — read the file you're editing before writing it
- **Never overwrite pricing or contact info** without explicit instruction
- **Always update `softwareVersion` consistently** — JSON-LD, nav badge, llms.txt, llms-ctx.txt must all match
- **Test schema changes** with `https://validator.schema.org` before deploying
- **Deploy is instant and global** — Cloudflare propagates in seconds, no staging environment

## Error Handling

Every `run()` call returns `{ ok: boolean }`. Check it:
```javascript
const result = await run('aeo', 'nonexistent');
if (!result.ok) {
  console.error(result.error); // "Project "nonexistent" not configured..."
}
```

## Dashboard Embedding

```javascript
import { getDashboardHtml } from 'seo-intel/froggo';
const { html } = await getDashboardHtml('myproject');
// Render in iframe, panel, or webview
```

## Data Persistence

All data is stored in SQLite (`seo-intel.db`). The database persists across runs.
Agents can run analyses multiple times — results accumulate, insights deduplicate.
The Intelligence Ledger (`insights` table) is the canonical source of active findings.
