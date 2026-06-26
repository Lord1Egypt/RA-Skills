---
name: tokopedia_unofficial_mcp
description: Use Tokopedia MCP tools for universal shopping tasks: discovery, comparison, detail lookup, reviews, shop checks, and media inspection.
user-invocable: true
metadata: {"openclaw":{"homepage":"https://github.com/its-benjamin/Tokopedia-unofficial-mcp-server"}}
---

# Tokopedia Unofficial MCP Skill

Use this skill for general Tokopedia workflows: finding products, comparing options, checking product details, reading reviews, evaluating shops, and collecting review media.

## Objectives

- Find relevant products quickly and efficiently.
- Compare options using objective signals such as price, rating, review count, sold count, and seller quality.
- Extract product information from detail fields, description, variants, and review summaries.
- Present clear recommendations with transparent tradeoffs.

## Workflow

1. Understand user constraints such as budget, preferred brand, category, and must-have features.
2. Search products with broad-to-specific queries and continue pagination when useful.
3. Build a shortlist using relevance and quality signals.
4. Fetch full product details for shortlisted items.
5. Add review and shop context when it affects buying confidence.
6. If variants exist, compare variant-specific price and stock.
7. Return a concise recommendation plus alternatives.

## General Guidance

- Use listing titles for discovery, then validate with detail fields and description when precision matters.
- If data is missing or ambiguous, state uncertainty clearly instead of guessing.
- Keep recommendations aligned with user priorities and constraints.

## Output Format

Return:

- A shortlist table with product name, price, rating, review count, sold count, and URL.
- A brief strengths and tradeoffs summary for each option.
- A final recommendation and at least one alternative.
- Optional next action, for example checking another page, adding review evidence, or narrowing by specific features.
