---
name: uplo-nonprofit
description: AI-powered nonprofit knowledge management. Search grant documentation, donor records, program reports, and compliance data with structured extraction.
---

# UPLO Nonprofit

Nonprofits generate mountains of documentation — grant proposals, funder reports, board minutes, program evaluations, donor correspondence, compliance filings — yet the institutional knowledge often lives in the heads of a few long-tenured staff. This skill gives your AI assistant structured access to your organization's knowledge base so that grant deadlines don't slip, reporting requirements aren't missed, and program learnings carry forward even when team members move on.

## Session Start

Start by understanding your organizational context and current strategic priorities. For nonprofits, directives often reflect multi-year strategic plans, annual fundraising goals, and board-approved program priorities.

```
use_mcp_tool: get_identity_context
use_mcp_tool: get_directives
```

Then check for anything time-sensitive — upcoming grant deadlines, pending funder reports, or board action items:

```
use_mcp_tool: search_knowledge query="upcoming grant deadlines funder report due dates board action items next 30 days"
```

## When to Use

- Writing a grant proposal and need to pull outcome data, logic models, and budget templates from previous successful applications
- Preparing a board packet and need to assemble program updates, financial summaries, and committee reports
- A program officer from a foundation is asking about your evaluation methodology — find the relevant program evaluation framework
- Checking restricted vs. unrestricted fund balances before committing to a new program expansion
- Onboarding a new development director who needs to understand donor history and cultivation strategies
- Responding to an audit request for documentation on how grant funds were allocated and spent
- Figuring out which foundations in your pipeline fund youth workforce development in the Midwest

## Example Workflows

### Grant Proposal Development

You're applying to a new foundation and need to assemble supporting materials from your track record.

```
use_mcp_tool: search_knowledge query="program outcomes data youth employment placement rates graduation rates last two years"
use_mcp_tool: search_with_context query="successful grant proposals workforce development logic model theory of change"
use_mcp_tool: search_knowledge query="organizational budget functional expenses program service ratio"
```

The structured extraction pulls outcome metrics as typed data (percentages, counts, dollar amounts) rather than buried-in-narrative text, making it straightforward to populate funder application forms.

### Funder Report Compilation

A major foundation's annual report is due in two weeks. You need to gather data across multiple program areas.

```
use_mcp_tool: search_knowledge query="Ford Foundation grant #2024-1187 deliverables milestones reporting requirements"
use_mcp_tool: search_knowledge query="program participants served demographics outputs outcomes July 2024 through June 2025"
use_mcp_tool: search_knowledge query="expenditure reports grant fund allocation budget to actual variance"
```

Match deliverables from the original grant agreement against actual program data and financials to build the narrative and data tables the funder expects.

## Key Tools for Nonprofits

**search_knowledge** — Search across grant documents, program reports, donor records, and board materials in one query. The extraction engine recognizes nonprofit-specific structures like logic models, grant budgets, and outcome frameworks. Example: `"evidence-based practices mentoring program RCT quasi-experimental evaluation results"`

**search_with_context** — Trace relationships between grants, programs, and outcomes. A single program might have multiple funding sources with different reporting requirements. Example: `"all funding sources and reporting obligations for the East Side Community Health Initiative"`

**export_org_context** — Produces a structured overview of your organization: programs, staff, governance, and strategic direction. Extremely useful when introducing your org to new funders or partners who want to understand your capacity.

**get_directives** — Pulls board-approved strategic priorities, annual fundraising targets, and programmatic focus areas. Essential for ensuring that grant-seeking aligns with organizational strategy rather than chasing dollars.

**report_knowledge_gap** — Identify missing documentation that could hurt you in an audit or site visit. No evaluation plan for a major program? No conflict of interest policy on file? Flag it before a funder asks.

## Tips

- Grant terminology matters in search. Use funder-specific language: "deliverables" vs "milestones" vs "benchmarks" — different foundations use different terms, and your extracted documents will reflect whatever language was in the original grant agreement.
- Nonprofit financial data follows specific structures (functional expenses, program service ratios, cost allocation plans). Search with these terms to get structured financial data rather than narrative descriptions.
- Use `log_conversation` after calls with program officers or major donors. These relationship notes are gold for cultivation strategy, and they're the first thing lost when a development officer leaves.
- When preparing for a site visit, use `export_org_context` to generate a comprehensive briefing document rather than assembling it manually from scattered files.
