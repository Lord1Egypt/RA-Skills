---
name: heatmap-analyze
description: >
  Ptengine Heatmap end-to-end analysis skill. Fetches real heatmap data via the user-installed
  `ptengine-cli` tool and runs AI-powered CRO behavior analysis using a 4-stage psychology model.

  REQUIREMENTS (skill does not install or provide these itself):
  - External tool: `ptengine-cli` — user must install from https://github.com/Kocoro-lab/ptengine-cli
  - Credentials: a Ptengine API key, configured by the user via `ptengine-cli config set` (stored at
    `~/.config/ptengine-cli/config.yaml`) or `PTENGINE_API_KEY` env var. The skill never reads, writes,
    or transmits the key itself — all credential handling is performed by `ptengine-cli`.
  - Config file read: `~/.config/ptengine-cli/config.yaml` is checked only for existence/`api_key:`
    presence, to decide whether configuration is needed. Its contents are not parsed or exfiltrated.

  Use this skill when the user wants to: analyze a webpage's heatmap data, understand user behavior
  on a page, compare audience segments, validate A/B test results, evaluate ad channel performance,
  analyze audience characteristics, find conversion barriers or opportunities, or optimize a landing page.
  Trigger whenever: "analyze heatmap", "heatmap analysis", "page behavior", "analyze this URL/page",
  "how are users behaving", "compare segments", "A/B test results", "ad performance", "audience analysis",
  "ptengine", "block-level analysis", "conversion optimization", "exit rate", "dwell time", "user drop-off",
  "landing page analysis", or any request involving page analytics combined with behavioral insights.
---

# Ptengine Heatmap Analysis

You are an expert CRO (Conversion Rate Optimization) analyst using Ptengine heatmap data. This skill
bundles the analysis methodology (4-stage psychology model), quality constraints, and output schemas.
Heatmap data is fetched via `ptengine-cli`, an external open-source tool the user installs themselves
(see Phase 0).

## Requirements and Capability Disclosure

This skill is transparent about every external dependency and resource it touches. Nothing here is
hidden; all are listed so the user and any security review can verify expected behavior.

| Resource | Purpose | Who reads / writes |
|----------|---------|-------------------|
| `ptengine-cli` (external CLI) | Queries Ptengine Open API for heatmap data | User installs; skill invokes it as a subprocess |
| `~/.config/ptengine-cli/config.yaml` | Stores the API key the user configured | Written and read **only** by `ptengine-cli`. Skill only checks `api_key:` exists to decide whether to prompt for setup |
| `PTENGINE_API_KEY` env var (optional) | Alternative to the config file | Read **only** by `ptengine-cli`. Skill never accesses it |
| Ptengine Open API (`https://xbackend.ptengine.com`) | Source of heatmap metrics | Contacted by `ptengine-cli`, not by the skill directly |

**What this skill does NOT do:**
- Does not install `ptengine-cli` for the user (no bundled installer, no `curl | sh`)
- Does not read, parse, or transmit the contents of `config.yaml` or `PTENGINE_API_KEY`
- Does not access any URL other than the Ptengine API via the CLI
- Does not scrape the target webpage or use browser-automation tools (see Data Source Boundary)
- Does not require any other environment variables, credentials, or file-system access
- **Does not execute purchases, payments, checkouts, or any transaction.** Words like "purchase",
  "buy", "add to cart", and "checkout" appear throughout this skill because it **analyzes** the
  purchase funnel on a target webpage — they refer to user behavior being measured, not actions
  the skill itself performs.
- Does not perform cryptography, key generation, hashing, encryption/decryption, or any
  crypto-currency / blockchain operations. Credential storage is delegated entirely to
  `ptengine-cli`, which this skill only invokes as a subprocess.

---

## Skill Contents

```
heatmap-analyze/
├── SKILL.md                           # This file — workflow orchestration
└── references/
    ├── ptengine-cli.md                # CLI command reference and output format
    ├── data-transform.md              # Field mapping, tag/ranking computation
    ├── page-classification.md         # 7 page type definitions and classification
    ├── block-analysis.md              # Block content + stage classification (4-phase model)
    ├── quality-constraints.md         # Metric dictionary, evidence policy, terminology
    ├── page-types.md                  # Per-page-type interpretation guide
    ├── single-page-task.md            # Single page analysis task + schema
    ├── compare-task.md                # Segment comparison task + schema
    ├── ab-test-task.md                # A/B test validation task + schema
    ├── ad-performance.md              # Ad source quadrant analysis + schema
    └── audience-analysis.md           # Audience segment analysis + schema
```

## Data Source Boundary

The **only authoritative data source** for this skill is `ptengine-cli`. All metrics,
block identifiers, block content, and page structure MUST come from its responses.

**Do not** access the target URL through any other channel, including:
- `browser_*`, `screenshot`, `computer`, any Playwright MCP (`mcp__playwright__*`),
  or any other browser-automation tool
- `http` GET / `WebFetch` against the target URL to scrape HTML or assets

**Why it matters (not just a preference):** ptengine-cli returns aggregated behavior
over the selected date range. The live page may have been edited — blocks added,
removed, or reordered — since those users visited. Mixing a live scrape with
historical aggregate data produces misleading analysis (e.g. attributing a low
dwell time to copy that did not exist when the data was collected).

If block content information is genuinely missing from ptengine-cli's response,
ask the user — do not fetch the page yourself.

## Analysis Types

| Type | Description | When to use |
|------|-------------|-------------|
| `single_page` | Deep single-page behavior analysis | Default. "How are users behaving on this page?" |
| `compare` | Cross-segment comparison | "Compare new vs returning visitors" |
| `ab_test` | A/B test hypothesis validation | "Which version won and why?" |
| `ad_performance` | Ad source quadrant analysis | "Which ad channels are performing?" |
| `audience_analysis` | Audience segment characteristics | "Who is visiting and how do they differ?" |

## Pipeline

```
Phase 0: Prerequisites + Parameters
Phase 1: Data Fetch (ptengine-cli)
Phase 2: Page Classification
Phase 3: Data Enrichment (block content + phase assignment)
Phase 4: Input Assembly (transform to analysis format)
Phase 5: Analysis (apply methodology from references/)
Phase 6: Results Presentation
```

---

## Phase 0: Prerequisites and Parameters

### Check ptengine-cli

Run these checks in order:

1. **Is it installed?** `command -v ptengine-cli`
2. **Is it configured?** Check that `$HOME/.config/ptengine-cli/config.yaml` exists
   and contains an `api_key:` entry.

Branch on the result:

- **Installed + configured** → proceed to parameter collection.
- **Installed but not configured** → ask the user for their API Key and Profile ID,
  then run:
  `ptengine-cli config set --api-key <KEY> --profile-id <ID>`
- **Not installed** → follow the "Install ptengine-cli" procedure below, then configure.

### Install ptengine-cli

ptengine-cli is an external open-source tool. This skill does **not** ship an installer
and does **not** fetch or execute install scripts itself.

When the user needs to install it, show them this message (do not run anything yourself):

> ptengine-cli is not installed. Please install it from the upstream repository:
> <https://github.com/Kocoro-lab/ptengine-cli>
>
> Prebuilt binaries (recommended): <https://github.com/Kocoro-lab/ptengine-cli/releases>
>
> Follow the install instructions in the repo's README. Once installed, tell me and I'll
> continue.

After the user reports install is done, verify with `ptengine-cli version`. If not found,
ask them to check `$PATH`.

### Collect Parameters

| Parameter | Required | Default | Notes |
|-----------|----------|---------|-------|
| URL | Yes | — | Page URL to analyze |
| Date range | Yes | Last 30 days | YYYY-MM-DD |
| Analysis type | Yes | single_page | 5 types above |
| Device type | For block data | MOBILE | PC or MOBILE (block_metrics cannot use ALL) |
| Language | No | ENGLISH | CHINESE / ENGLISH / JAPANESE |
| Conversion name | No | — | Fuzzy match for conversion metrics |

For **compare**: which segments to compare (e.g. new vs returning visitors)
For **ab_test**: campaign name, type (inline/popup/redirect), version info

---

## Phase 1: Data Fetch

Read `references/ptengine-cli.md` for full command reference.

### Core commands

```bash
# Page-level metrics
ptengine-cli heatmap query --query-type page_metrics \
  --url "<URL>" --start-date <START> --end-date <END> --output json

# Block-level metrics (MUST specify device type)
ptengine-cli heatmap query --query-type block_metrics \
  --url "<URL>" --start-date <START> --end-date <END> \
  --device-type <PC|MOBILE> --output json

# Dimension-grouped insights (for ad/audience analysis)
ptengine-cli heatmap query --query-type page_insight \
  --url "<URL>" --fun-name <sourceType|visitType|terminalType> \
  --start-date <START> --end-date <END> --output json

# Filtered data (for compare)
ptengine-cli heatmap query --query-type block_metrics \
  --url "<URL>" --start-date <START> --end-date <END> \
  --device-type MOBILE --filter "visitType include newVisitor" --output json
```

### Error handling
- `"success": false` → show error message and hint
- Rate limited → check `rateLimit.remainingMinute`, wait if needed
- No data → suggest checking URL and date range

### Data preprocessing (important)

ptengine-cli returns all metric values as **formatted strings** (e.g. `"6,777"`, `"55.08%"`,
`"3m 13s"`), not raw numbers. Before proceeding to analysis, parse these strings into numeric
values following the rules in `references/data-transform.md` § "Value format parsing". Getting
this step wrong will produce incorrect analysis — pay special attention to percentage values
(already percentages, do NOT multiply by 100 again) and duration formats (page-level uses
"Xm Ys", block-level uses "Xs").

---

## Phase 2: Page Classification

Read `references/page-classification.md` for full criteria.

Classify the URL into one of 7 types and map to internal key:

| Result | Key | Notes |
|---|---|---|
| Sales Landing Page | `sales_lp` or `ad_lp` | ad_lp if ad traffic >50% |
| Article LP | `article_lp` | |
| Product Detail Page | `pdp` | |
| Homepage | `homepage` | |
| Campaign / Promotion | `sales_lp` | |
| Other Content | `other_content` | |
| Other Function | `other_function` | |

If uncertain, ask the user.

---

## Phase 3: Data Enrichment

Read `references/block-analysis.md` for the 4-phase psychology model and module categories.

### 3a. Block Content Analysis
For each block, determine `module_category`, `content_summary`, `marketing_intent` using the
module categories for the detected page type.

### 3b. Block Stage Classification
Assign each block to phase 1-4 using the criteria in block-analysis.md. Load the correct
phase names for the page_type and language from the phase name tables.

Use block_name and block position as primary signals when screenshots are not included
in ptengine-cli's response. Do not obtain screenshots by other means (see Data Source Boundary).

---

## Phase 4: Input Assembly

Read `references/data-transform.md` for detailed field mapping, tag computation, and ranking algorithms.

Key steps:
1. Assemble `base_metric` from page_metrics response
2. Assemble `block_data[]` from block_metrics + Phase 3 enrichment
3. Compute tags (High/Medium/Low) and rankings if not provided by API
4. For ad/audience analysis: compute quadrant assignments

---

## Phase 5: Execute Analysis

Based on analysis type, read the corresponding reference and follow its methodology:

| Type | Reference file | Key output fields |
|------|---------------|-------------------|
| single_page | `references/single-page-task.md` | core_insight, narrative_structure, barriers, opportunities |
| compare | `references/compare-task.md` | macro_performance, narrative_comparison, barriers/opportunities per segment |
| ab_test | `references/ab-test-task.md` | core_conclusion, hypothesis_validation with win_version_index |
| ad_performance | `references/ad-performance.md` | core_insights.summary, ad_performance_overview.description |
| audience_analysis | `references/audience-analysis.md` | core_insights.summary, user_profile.description |

Before writing analysis, also read:
- `references/page-types.md` — interpretation guide for the detected page type
- `references/quality-constraints.md` — metric dictionary, evidence policy, terminology enforcement

### Critical quality gates (always apply)

1. **Full block coverage**: ALL blocks must appear in narrative structure (no omissions)
2. **Directional consistency**: Verify metric direction language matches the direction table
3. **Evidence grounding**: Always cite dwell + exit, use hedging for causal claims
4. **No technical leaks**: No block_ids, camelCase keys, or raw tags in output text
5. **Language purity**: No mixed-language output; apply terminology enforcement
6. **Source separation**: fvDropOffRate from base_metric only; exitRate from block_data only
7. **Low sample warning**: If total visits < 100 or a block's impressionRate is very low (< 10%),
   note the limited data confidence in the analysis. Metrics from very few sessions can be misleading.

---

## Phase 6: Present Results

Output a **human-readable Markdown report** in the target language — not JSON. The report is for
marketing practitioners, CRO specialists, and site operators who need actionable insights.

Each analysis type has its own report template defined in the corresponding reference file.
The general structure is:

1. **Core finding** — the single most important insight, prominently displayed
2. **Detailed analysis** — phase-by-phase narrative (behavior tasks) or structured comparison
3. **Barriers and opportunities** — clearly separated with supporting data
4. **Improvement suggestions** — 1-3 concrete, actionable recommendations
5. **Next steps** — offer to run a different analysis type, compare segments, or save results
