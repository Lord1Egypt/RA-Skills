---
name: wos-zotero-hunter
description: Search Web of Science for academic literature through institutional access, filter by journal, impact factor, or date, and automatically import results into Zotero. Use when the user wants to find and import scholarly papers from WoS into Zotero — they will describe a topic, quality criteria (IF, journal names, citation count), desired paper count, and a Zotero collection name.
---

# WoS → Zotero Literature Hunter

Search Web of Science through the user's institutional access, filter results by quality criteria, and import papers to a new Zotero collection with full metadata.

## Prerequisites

Before first use, confirm the user has:

1. **Web of Science institutional access** — via their university/library portal
2. **Zotero API key** — from https://www.zotero.org/settings/keys (needs read/write)
3. **Zotero user ID** — numeric, shown on the same page
4. **pyzotero** installed — `pip install pyzotero`

The Zotero credentials are typically found in `~/.config/zotcli/config.ini` or can be provided by the user.

## Workflow

### Phase 1: Collect Search Parameters

Ask the user for these parameters. All are required unless marked optional:

| Parameter | Example |
|-----------|---------|
| Keywords / topic | "perovskite solar cell stability" |
| Journal or IF filter | "IF>15" or "Nature, Science, Joule" |
| Paper count | 5 |
| Zotero collection name | "perovskite_stability" |
| Date range (optional) | "2020-2025" |

### Phase 2: Search Web of Science via Browser

Use browser automation with the user's profile (to preserve institutional login session):

1. **Navigate to WoS through institution.** The user's library portal typically has a direct WoS link. Navigate there first (the user may need to guide this step the first time).

2. **Perform topic search:**
   - Enter keywords in the search box (Topic field)
   - Click Search

3. **Apply quality filters** in this order:
   - *Highly Cited Papers* (Quick Filters) — this naturally filters for high-impact papers
   - *Publication Titles* — select target journals (e.g., Nature, Science, Joule, Advanced Materials, Energy & Environmental Science)
   - *Publication Years* — if date range specified
   - Click **Refine** after selecting each set of filters

4. **Sort** by Citations (highest first) if needed.

5. **Extract paper metadata.** From the search result page, extract for each of the top N papers:
   - Title
   - Authors (first/last at minimum)
   - Year
   - Journal name
   - DOI (if visible)

WoS result pages show papers in a consistent format: title link, author list with ";" separators, date, journal button, volume/issue/pages. Extract these from the page snapshot.

### Phase 3: Enrich & Import via Zotero API

Use `scripts/import_to_zotero.py` to import papers:

```bash
echo '[
  {"title": "...", "authors": "Smith, J; Doe, K", "year": "2023", "journal": "Nature"},
  ...
]' | python3 scripts/import_to_zotero.py \
    --zotero-key <API_KEY> \
    --zotero-id <USER_ID> \
    --collection "collection-name"
```

The script will:
1. Create the collection if it doesn't exist
2. For each paper, enrich metadata via Crossref API (resolves DOIs, full author lists, abstracts, volume/pages/ISSN)
3. Create full Zotero items with all metadata
4. Assign items to the specified collection
5. Report results

**Paper JSON format** accepted by the script:

```json
[
  {
    "title": "Paper title",
    "doi": "10.xxx/xxx",
    "authors": "LastName, FirstName; LastName, FirstName",
    "year": "2023",
    "journal": "Journal Name",
    "volume": "1",
    "issue": "2",
    "pages": "100-120",
    "abstract": "Optional abstract text",
    "extra": "Optional Zotero extra field",
    "source": "Web of Science"
  }
]
```

All fields except `title` are optional. When DOI is provided, the script auto-resolves missing metadata via Crossref.

### Phase 4: Report Results

After import, list the papers with title, journal, year, and DOI. Remind the user to check the Zotero collection.

### Dry Run

Test paper extraction without importing:

```bash
cat papers.json | python3 scripts/import_to_zotero.py \
    --zotero-key KEY --zotero-id ID \
    --collection "test" --dry-run
```

## Security & Privacy

This skill operates entirely within the user's local environment:

- **Browser automation** only interacts with Web of Science search pages through the user's existing authenticated browser session. No credentials are captured, stored, or transmitted.
- **Network requests** are limited to three destinations, all user-initiated and transparent:
  - `api.crossref.org` — public, free scholarly metadata API (no authentication)
  - `api.zotero.org` — user's own Zotero library via their API key
  - Web of Science — accessed through the user's institutional browser session
- **No data exfiltration.** Paper metadata fetched from Crossref and WoS is written only to the user's Zotero library. No information is sent to any other service.
- **Zotero API key** is passed via CLI arguments and used exclusively to authenticate with `api.zotero.org`. It is never written to disk or transmitted elsewhere.
- **Use `--dry-run`** to preview what will be imported before any data is written to Zotero.
- **Review extracted papers** before importing — the agent will always show a summary before proceeding.
- All source code is in `scripts/import_to_zotero.py` — review it before running if desired.

The browser automation and network capabilities flagged by automated scanners are the core, documented features of this skill and serve no other purpose.

## Notes

- The Zotero API key must have write access (check "Allow library access" and "Allow notes access" when creating the key)
- Crossref API is rate-limited. The script includes delays to stay within limits
- WoS institutional login flow varies by institution. The browser must already have an active authenticated session
- Always create a **new** collection — never import into existing collections without explicit user permission
- Use `--dry-run` first to verify extracted papers before importing
