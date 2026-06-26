---
name: sec-finance-ai
description: AI-Powered SEC Filing Integration skill. 40+ SEC filing tools. Access 10-K, 10-Q, 8-K, insider trading, beneficial ownership (13D/G), company facts, XBRL data, and more through the SEC's EDGAR database.
version: 1.3.3
metadata:
  openclaw:
    install:
      - kind: uv
        package: .
---

# SEC-AI Skill

40+ SEC filing tools. Access 10-K, 10-Q, 8-K, 13D/G beneficial ownership, insider transactions, company XBRL facts, and institutional holdings.

## Github Open-Source
Please star Github if you like the skill.

Also available for OpenWebUI.

https://github.com/lkcair/sec-finance-ai


## Setup

Run from the skill directory:

```bash
python3 -m venv .venv
.venv/bin/python3 -m pip install -r requirements.txt
```

> **Windows:** use `.venv\Scripts\python3` instead of `.venv/bin/python3`.

## AGNOSTIC OS / One-shot Design ( Goals )
- This skill is designed to be agnostic to OS and execution environment.
- It loads only essential context on first use and uses a single-shot interaction pattern for reliability.
- Basic usage pattern provided and All Functions list in SKILL.md body.

## Quotation / Command Execution Reliability (common pitfall)
- If a command invocation uses complex shell quoting, it may fail in various environments. Use a here-doc style or a tiny helper script to avoid escaping issues.
- **Crucially, ensure you are executing Python scripts using the interpreter from the skill's virtual environment.** Simply calling `python3` might not use the correct interpreter if the venv is not activated, leading to `ModuleNotFoundError`.
- **Always use the full path to the venv's Python interpreter** for execution, e.g.:
  `/home/openclaw/.openclaw/venv/sec-finance-ai/bin/python3`
- Ensure that all necessary packages (like `pandas`, `pydantic`, `requests`, `beautifulsoup4`) are installed within this specific venv using its associated `pip` command.

## Agent Quick-Start

After setup, copy the template below into your agent's `TOOLS.md`.

**Replace `SKILL_DIR`** with the absolute path to this skill's directory.

````markdown
# SEC-AI Skill

## Usage

```bash
cd SKILL_DIR && SKILL_DIR/.venv/bin/python3 -c "
import asyncio, sys
sys.path.insert(0, '.')
from sec_finance_ai import Tools
t = Tools()
async def main():
    result = await t.METHOD(ARGS)
    print(result)
asyncio.run(main())
" 2>/dev/null
```

Replace METHOD(ARGS) with any call below.

## Common Calls

| Need | Method |
|---|---|
| Annual Report (US) | `get_latest_10k(ticker='AAPL')` |
| Quarterly Report (US) | `get_latest_10q(ticker='AAPL')` |
| Current Report | `get_recent_8k_filings(ticker='AAPL')` |
| Beneficial Ownership | `get_beneficial_ownership(ticker='GME')` |
| Insider Transactions | `get_insider_transactions(ticker='TSLA')` |
| Company Facts | `get_company_facts(ticker='AAPL')` |
| Filing Content | `get_filing_content(ticker='AAPL', get_full_content=True)` |
| Search Filings | `search_filings(query='Apple')` |
| Download Text | `download_filing_text(filing_url='...')` |

## Routing

- "Get 10-K" → `get_latest_10k`
- "Get 10-Q" → `get_latest_10q`
- "Get 8-K" → `get_recent_8k_filings`
- "Beneficial ownership" → `get_beneficial_ownership`
- "Insider trading" → `get_insider_transactions`
- "Financials/Facts" → `get_company_facts`
- "Search SEC" → `search_filings`
- "Download filing" → `download_filing_text`
- "Read full 10-K" → `get_filing_content(ticker='...', filing_type='10-K', get_full_content=True)`
- "Get links only" → `get_company_filings`
````

---

## All Functions

By Categories:

- **Filing Access**: `get_company_filings`, `get_latest_10k`, `get_latest_10q`, `get_recent_8k_filings`, `analyze_8k_filing`, `get_proxy_statements`
- **Ownership/Insider**: `get_insider_transactions`, `get_beneficial_ownership`
- **Financial Facts**: `get_company_facts`, `get_company_concept`, `get_available_metrics`
- **Content Retrieval**: `get_filing_content`, `download_filing_text`
- **Utility**: `search_filings`, `get_recent_ipos`, `get_sec_api_status`, `run_self_test`, `get_available_functions`

## Notes

- Data directly from official SEC EDGAR database.
- All functions are async — the `asyncio.run()` wrapper handles this.
- Remember to update `SEC_HEADERS` in `sec_finance_ai.py` with your User-Agent info.
