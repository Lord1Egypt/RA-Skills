---
name: sec-finance
description: Fetch structured financial data and filing metadata from SEC EDGAR and SEC XBRL companyfacts for US-listed companies, especially Chinese issuers. Use when the task is quarterly/annual financial analysis, CIK resolution, filing lookup, or extracting metrics such as revenue, net income, and EPS from SEC data. Do not use for downloading static IR PDFs; use ir-pdf-downloader for document discovery/download.
---

# SEC Finance

Use this skill for **structured SEC data**, not IR document downloading.

## Scope

- Resolve company name / alias / ticker to CIK
- Fetch SEC XBRL companyfacts
- Extract key metrics such as revenue, net income, EPS
- Normalize annual vs quarterly periods

## Do not use this skill for

- Downloading annual report PDFs from IR sites
- Cloudflare/IR-site document fetching
- Generic PDF discovery workflows

Use `ir-pdf-downloader` for those.

## Core commands

```bash
# Resolve a company and fetch recent financials
python3 scripts/sec_finance.py --search JD.com

# Query by known CIK
python3 scripts/sec_finance.py --cik 0001549802 --period quarterly

# JSON output for downstream processing
python3 scripts/sec_finance.py --search Alibaba --period annual --output json
```

## Workflow

1. If the user needs revenue / profit / EPS / structured filings, use this skill.
2. Resolve CIK via shared issuer data first; fall back to SEC lookup when needed.
3. Pull `companyfacts` from `data.sec.gov`.
4. Return structured results in table or JSON form.
5. If the user instead needs the original PDF document, stop and switch to `ir-pdf-downloader`.

## Notes

- Issuer aliases and validated CIK hints live in `references/issuers.json`.
- Prefer secure HTTPS by default; only fall back on relaxed SSL handling for endpoint compatibility.
- Keep this skill focused on **SEC data retrieval and normalization**.
