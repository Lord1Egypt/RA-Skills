---
name: sec-13f-tracker
description: Track top fund managers' holdings via SEC 13F filings. Fetches quarterly filings from SEC EDGAR, compares quarter-over-quarter changes (new positions, increases, decreases, exits), and generates analysis reports with cross-fund convergence insights. Use when user asks about hedge fund holdings, 13F filings, whale tracking, what Buffett/Dalio/Ackman/Soros/Cathie Wood are buying or selling, or institutional investor portfolio changes.
---

# SEC 13F Whale Tracker

Track what Buffett, Dalio, Ackman, Soros, and Cathie Wood are buying and selling via SEC EDGAR 13F filings.

## Setup (one-time)

```bash
SKILL_DIR="$(dirname "$(readlink -f "$0")")"  # or resolve from skill path
cd /tmp && python3 -m venv sec13f-venv
source sec13f-venv/bin/activate
pip install -r "$SKILL_DIR/scripts/requirements.txt"
```

Or reuse an existing venv if available. The only dependency is `requests`.

## Run Tracker

```bash
python3 scripts/tracker.py
```

Output:
- `data/` — cached holdings JSON per fund per quarter (auto-created)
- `reports/latest.md` — most recent report
- `reports/13f-report-YYYY-MM-DD.md` — dated report

## Default Tracked Funds

| Fund | Manager | CIK |
|------|---------|-----|
| Berkshire Hathaway | Warren Buffett | 0001067983 |
| Bridgewater Associates | Ray Dalio | 0001350694 |
| Pershing Square | Bill Ackman | 0001336528 |
| Soros Fund Management | George Soros | 0001029160 |
| ARK Invest | Cathie Wood | 0001697748 |

To add funds, edit the `FUNDS` dict in `scripts/tracker.py`. Find CIK numbers at [SEC EDGAR](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany).

## Report Structure

Each fund section includes:
- Report period and filing date
- Total holdings value and count
- 🆕 New positions with value and shares
- 📈 Increased positions with % change
- 📉 Decreased positions with % change
- 🚫 Closed positions

Cross-fund insights section highlights:
- Stocks where multiple managers converge (buy or sell simultaneously)

## Cron Integration

Schedule quarterly runs (13F filings are due ~45 days after quarter end):

```
# Run mid-February, May, August, November
0 8 15 2,5,8,11 * cd /path/to/project && venv/bin/python scripts/tracker.py
```

Or use OpenClaw cron to run and send the report to a channel.

## Technical Notes

- SEC EDGAR API is free and public; requires `User-Agent` header
- Rate limited to <10 req/sec (script adds 150ms delay between requests)
- Parses 13F information table XML, handles namespace detection
- Merges holdings by CUSIP, separates put/call options
- Caches data in `data/` to avoid re-fetching known quarters
- No proxy needed for SEC EDGAR (script clears proxy env vars)
