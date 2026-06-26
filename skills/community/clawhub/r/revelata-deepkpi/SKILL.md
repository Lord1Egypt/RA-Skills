---
name: revelata-deepkpi
description: >
  Financial and operational KPI research for US public companies using Revelata deepKPI. Pulls
  SEC metrics (10-K/10-Q/8-K): segments, unit KPIs (stores, comps, ARPU, users), statements, cash
  flow; filing markdown and verbatim quotes via retrieve-sec-filing; implied Q4/per-unit, seasonality,
  Excel. For "pull data", historicals, "find the KPI", seasonality, .xlsx, filing excerpts. Also:
  analyst-report-pressure-test (analyst PDF vs SEC HTML); peer-benchmark (peers, comps, benchmark,
  similar companies—operating, vertical-first); idea-generation-survey ("what should I invest in?",
  new ideas, interesting companies—no ticker); company-summary-segments (what cos do, segments,
  thematic discovery). OpenClaw: deepkpi-api.
version: 1.0.0
homepage: https://www.revelata.com
metadata:
  openclaw:
    emoji: "📊"
    requires:
      env:
        - DEEPKPI_API_KEY
      bins:
        - curl
    primaryEnv: DEEPKPI_API_KEY
---

# deepKPI Financial Analysis and Research Tools

Query structured KPIs extracted from SEC filings for US public companies.
Powered by [Revelata](https://www.revelata.com).

This skill suite covers different aspects of financial analysis workflows. 
This includes data access via MCP for Claude or REST API for OpenClaw, 
data retrieval, metric derivation, seasonality analysis, and Excel export. 
Sub-skills are organized so that each layer can be loaded independently — 
only read what the task requires.

## Data access — Claude vs. OpenClaw

The deepKPI operations (`query_company_id`, `list_kpis`, `search_kpis`,
`company_summary_search`, `get_company_summary`, `get_company_segments`, `list_sec_filing_markdowns`, `get_sec_filing_markdown`) are available two ways depending on the runtime:

| Runtime | How to call deepKPI |
|---------|---------------------|
| **Claude** (MCP tools available) | Use the native MCP tools directly — no API key or `deepkpi-api` skill needed |
| **OpenClaw** (no MCP) | Read `deepkpi-api/deepkpi-api.md` and call the REST endpoints using `$DEEPKPI_API_KEY` |

`retrieve-kpi-data/retrieve-kpi-data.md` is the KPI metrics workflow;
`retrieve-sec-filing/retrieve-sec-filing.md` is the SEC filing markdown workflow;
`company-summary-segments/company-summary-segments.md` is **what companies do** (summary),
**segment / geo structure**, and **thematic discovery** (`get_company_summary`,
`get_company_segments`, `company_summary_search`). The `DEEPKPI_API_KEY` env var and `deepkpi-api` reference doc
are only needed in OpenClaw (or as an env-var fallback when MCP is unavailable).

## Hard stop: deepKPI connection failures

If deepKPI access fails (MCP connector not working, REST calls failing, auth errors, network issues, or you cannot retrieve data), you MUST STOP and ask the user:

**“I can’t access deepKPI right now. Do you want to proceed without deepKPI?”**

- If the user says **no**, stop.
- If the user says **yes**, you may proceed using other sources (e.g. web), BUT you MUST NOT use deepKPI skill branding, templates, formatting conventions, or “Powered by Revelata deepKPI” framing for non-deepKPI data. Clearly label alternate sources.

This rule applies to ALL sub-skills in this bundle.

## Sub-skill routing

**Read the relevant reference doc(s) before doing any work.** Multiple docs
may apply to a single request — load all that are relevant.

| User need | File to read |
|-----------|--------------|
| No specific company or thesis — "what should I invest in?", "what stock should I buy?", **new ideas**, **interesting companies**, boredom / open exploration | `idea-generation-survey/idea-generation-survey.md` — interactive funnel + `company_summary_search` screen; then `retrieve-kpi-data` for deep pulls |
| Pull historical KPIs / financials from deepKPI | `retrieve-kpi-data/retrieve-kpi-data.md` |
| **What a company does**, **segments / geographies**, or **thematic** “who does X?” lists | `company-summary-segments/company-summary-segments.md` — named company: `get_company_summary` / `get_company_segments`; discovery: `company_summary_search` then hydrate as needed |
| Pull **full filing markdown** into chat, **verbatim SEC text**, quotes, MD&A / risk-factor language, or “what did they say” | `retrieve-sec-filing/retrieve-sec-filing.md` — **before any web/SEC.gov**: `list_sec_filing_markdowns` (free) → `get_sec_filing_markdown` (10 credits). Return full markdown when they want the document; blockquoted excerpts for quote-style asks; no paraphrase as quotes |
| Derive missing Q4 numbers, a segment remainder, or per-unit economics (ASP, ARPU, AUV, take rate) | `derive-implied-metric/derive-implied-metric.md` |
| Split annual forecasts into quarterly estimates / seasonality patterns | `analyze-seasonality/analyze-seasonality.md` |
| Produce an Excel workbook (.xlsx) from deepKPI data | `format-deepkpi-for-excel/format-deepkpi-for-excel.md` |
| REST API calls (OpenClaw / env-var fallback only) | `deepkpi-api/deepkpi-api.md` |
| Pressure-test a sell-side / analyst report against SEC filing data (HTML report, Chart.js, provenance links) | `analyst-report-pressure-test/analyst-report-pressure-test.md` |
| **Peers / comps**, **benchmark** a company, **most similar** public companies, or operational comp sets | `peer-benchmark/peer-benchmark.md` — read `retrieve-kpi-data` first for KPI mechanics |

**Default entry point:** For **metrics and modeling feeds**, start with
`retrieve-kpi-data/retrieve-kpi-data.md` (it references `derive-implied-metric`,
`analyze-seasonality`, and `format-deepkpi-for-excel` as needed). For **business
description, segment structure, or thematic company lists**, start with
`company-summary-segments/company-summary-segments.md`. For **filing markdown (full or
excerpts) and verbatim quotes**, start with `retrieve-sec-filing/retrieve-sec-filing.md`.
If a request mixes these, read **every** doc that applies.

## Sub-skill summary

**`deepkpi-api`** — Raw REST access to deepKPI endpoints:
`query_company_id`, `list_kpis`, `search_kpis`, `company_summary_search`,
`get_company_summary`, `get_company_segments`, `list_sec_filing_markdowns`, `get_sec_filing_markdown`. **OpenClaw / env-var fallback only** — in Claude, use
the native MCP tools instead.

**`retrieve-kpi-data`** — Primary workflow for **structured KPIs** (company ID,
`list_kpis` / `search_kpis`, gap handling including Q4 derivation), provenance
rules, in-chat tables, and the mandatory post-pull Excel offer.

**`company-summary-segments`** — **`get_company_summary`** (what they do) and
**`get_company_segments`** (how they break out segments / geos); **`company_summary_search`**
for **thematic** “who does X?” discovery. Not for KPI time series.

**`retrieve-sec-filing`** — **SEC filing markdown** in chat: full filing or
excerpts, verbatim quotes, MD&A / risk language. Tools: `list_sec_filing_markdowns`
→ `get_sec_filing_markdown`, source hierarchy (tool-first, not web), blockquote
discipline for quote-style asks. Distinct purpose from KPI time series.

**`derive-implied-metric`** — Compute metrics that deepKPI doesn't report
directly from data that IS reported: Q4 = FY − (Q1+Q2+Q3), missing segment = total − known segments,
per-unit economics (revenue per store, ARPU, ASP), take rates, penetration
rates, and geographic mix percentages.

**`analyze-seasonality`** — Compute each quarter's typical share of the full
fiscal year from 2–3 years of actuals, then apply those ratios to split an
annual projection into quarterly estimates.

**`format-deepkpi-for-excel`** — Canonical layout and styling spec for any
.xlsx export built from deepKPI data: wide layout with periods as columns
(annual block → blank column → quarterly block), Calibri font, green input
cells, clickable hyperlinks in cells, numeric date headers, freeze panes,
column grouping, and no redundant Source rows.

**`analyst-report-pressure-test`** — End-to-end workflow for uploaded analyst PDFs:
extract 4–6 claims, pull granular deepKPI metrics per claim, build paired
"supports" / "complicates" evidence with mandatory provenance hyperlinks, and
emit a Revelata-branded interactive HTML report (`references/html-template.md`,
`references/chart-patterns.md`). After the draft HTML exists, run the mandatory internal
**draft HTML QA** rubric in `analyst-report-pressure-test/pressure-test-double-check.md`,
then revise and re-check as needed before presenting the file. **Always** read `retrieve-kpi-data` for KPI
mechanics; use `retrieve-sec-filing` when the test needs verbatim filing
passages; use `company-summary-segments` for business description / segment structure /
thematic lists when useful; use `derive-implied-metric` when filling Q4 or segment gaps.

**`peer-benchmark`** — Curated **operational** benchmark sets (not trading multiples):
`company_summary_search` for candidates, KPI fingerprint + alignment, diff-driven
segment sub-benchmarks, chat 1-pager, optional HTML (`references/html-template.md`),
Excel via `format-deepkpi-for-excel`. **Always** read `retrieve-kpi-data` first.

**`idea-generation-survey`** — Onramp when the user has **no ticker and no thesis**: rapid interview
(multiple-choice by default), `company_summary_search` for a 10–15 name screen with thesis-matched
KPIs, then deep pulls on 1–2 chosen names per `retrieve-kpi-data`. `references/sector-kpi-map.md`
for diagnostic KPI concepts. **No** default Excel offer. Not for users who already named a company
or a specific metric — use `retrieve-kpi-data` instead.
