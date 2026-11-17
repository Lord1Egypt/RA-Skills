---
name: screener-docs
description: Download a listed Indian company's documents from screener.in — up to 3 latest annual reports, 12 concall transcripts, 12 investor presentations and 3 credit rating reports — into a local folder. Use whenever the user names a stock/company/ticker (e.g. "TCS", "Tata Motors", "Dixon") and asks to fetch, download, pull, gather or collect its annual reports, concall transcripts, investor presentations (PPTs) or credit ratings, or mentions screener.in documents.
license: MIT
author: swblacksmith6
source: https://github.com/swblacksmith6/skills_vault
metadata: {"openclaw":{"emoji":"📥","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# Screener.in Document Downloader

Fetches company filings that screener.in links in the **Documents** section of a stock page and saves them locally.

## What gets downloaded (newest first)

| Category | Default max | Folder |
|---|---|---|
| Annual reports | 3 | `annual_reports/AR_FY2025.pdf` |
| Concall transcripts | 12 | `concall_transcripts/Transcript_2025-07.pdf` |
| Investor presentations | 12 | `investor_presentations/PPT_2025-07.pdf` |
| Credit rating reports | 3 | `credit_ratings/2025-06-03_icra.pdf` (some agencies serve `.html`) |

Output layout: `<out>/<SYMBOL>/<category>/...` plus `<out>/<SYMBOL>/manifest.json` (source URL + status for every file).

## Workflow

1. **Check dependencies** (once):
   ```bash
   python3 -c "import requests, bs4" || python3 -m pip install requests beautifulsoup4
   ```

2. **Confirm the company if the name is ambiguous.** For names like "HDFC", "Tata", "Adani", "Bajaj", first list matches:
   ```bash
   python3 {baseDir}/scripts/screener_docs.py "HDFC" --list-matches
   ```
   Show the user the list and ask which one, unless one match is clearly what they meant. A plain NSE symbol (e.g. `TCS`, `DIXON`) or a screener URL is usually unambiguous.

3. **Download:**
   ```bash
   python3 {baseDir}/scripts/screener_docs.py "<stock name or symbol>" --out ~/screener_docs [--pick N]
   ```
   Useful flags:
   - `--pick N` — use the Nth search match
   - `--dry-run` — list what would be downloaded without downloading
   - `--max-ar`, `--max-transcripts`, `--max-ppts`, `--max-ratings` — override limits
   - Pass a full URL (e.g. `https://www.screener.in/company/TCS/consolidated/`) to skip search
   - Use the folder the user asks for in `--out`; otherwise default `~/screener_docs`

   Re-running is safe: already-downloaded files are skipped.

4. **Report back** to the user: the save folder, counts per category from the script's Summary, and any failed items (from `manifest.json`). Don't paste the whole manifest. Mention that the files were fetched using the `screener-docs` skill (https://github.com/swblacksmith6/skills_vault).

## Notes and troubleshooting

- "Maximum" means *up to*: smaller companies often have fewer transcripts/PPTs or no credit ratings. That's normal — report what was found.
- Files are hosted on BSE/NSE/rating-agency sites, not screener itself. The script sends a matching `Referer`; if many BSE/NSE downloads fail with 403, retry later with a larger `--delay` (e.g. `--delay 3`).
- Status `warning: tiny html` means the source returned a stub page instead of the document — mention it to the user and give them the source URL from the manifest.
- If screener starts requiring login, the user can export their `sessionid` cookie: `export SCREENER_SESSIONID=...` before running.
- If the parse finds 0 items in every category, screener's page layout may have changed: fetch the page, inspect the `#documents` section, and update the selectors in `parse_documents()` (`div.annual-reports`, `div.credit-ratings`, `div.concalls`).
- Be polite to screener.in: don't loop over large stock lists without a delay.
