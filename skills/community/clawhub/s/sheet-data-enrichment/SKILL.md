---
name: sheet-data-enrichment
description: "Enrich spreadsheet data by fetching external sources (URLs, APIs) to fill missing columns, then aggregate results into summary sheets. Use when: (1) a spreadsheet has URLs/links in one column and you need to extract specific info (author, title, date, etc.) into another column, (2) batch-processing rows that require visiting web pages to scrape/extract data, (3) creating pivot/summary tables from enriched data (group-by, sum, count), (4) user says fill in, complete the table, extract from links, summarize by, aggregate, enrich spreadsheet, 补全表格, 汇总统计, 信息补齐. Works with Feishu Sheets, Google Sheets, or local CSV/Excel files."
---

# Sheet Data Enrichment & Summarization

## Workflow

### Phase 1: Reconnaissance

1. Read the full sheet (or specify range) to understand the schema
2. Identify the **source column** (e.g., URLs/links) and **target column** (data to fill)
3. Count empty rows in the target column — these are the work items
4. Confirm the plan with the user before proceeding

### Phase 2: Extraction

Process rows in batches. For each row with an empty target column:

1. **Classify the source** before fetching:
   - Regular article URL → `web_fetch`
   - SPA / JS-rendered page → browser automation
   - WeChat article (mp.weixin.qq.com) → browser (captcha may block `web_fetch`)
   - Social media (Weibo, Douyin, etc.) → browser or note as "no extractable data"
   - Dead link / paywall → flag for user

2. **Extract the target data** from the fetched content:
   - Search for the data in multiple locations (top, bottom, metadata)
   - Use targeted patterns (see [references/extraction-patterns.md](references/extraction-patterns.md))
   - If ambiguous, flag for manual review rather than guessing

3. **Verify before writing** (每篇先核实):
   - Confirm the extracted value is correct before writing to the sheet
   - Cross-reference with known mappings if available
   - When batch-processing, verify a sample first, then apply patterns

### Phase 3: Write-back

1. Write confirmed values to the target column
2. **Always verify row alignment** — read the row before writing to confirm the target cell matches the expected entry
3. Use single-cell writes (`G5:G5`) not bare references (`G5`)
4. For Feishu Sheets: range format must be `sheetId!G5:G5`

### Phase 4: Summarization

When the user requests aggregation:

1. Re-read all enriched sheets to capture any manual corrections
2. Group by the requested dimensions (e.g., assignee → contributor → sum)
3. Sort groups by total descending for readability
4. Output to a new sheet/spreadsheet with headers + subtotals + grand total

## Key Lessons (Extraction)

### Where to find data on a web page

Data placement varies by source. Always check multiple locations:

| Position | Example |
|---|---|
| Below title | `作者：张三` / `By Jane Doe` |
| End of article | `（记者 李四）` / `Reporter: John` |
| Before timestamp | `王五 2026-03-18 14:00` |
| Metadata line | `文｜赵六` / `Author: Sarah` |
| Combined format | `采写：记者 孙七 编辑：周八` |

**Never conclude "no data" after checking only the top of the page.** Always check the end too.

### When to use browser vs web_fetch

| Signal | Tool |
|---|---|
| Static HTML, server-rendered | `web_fetch` (fast, cheap) |
| Returns empty/minimal content | Switch to browser |
| URL contains `mp.weixin.qq.com` | Browser (WeChat captcha) |
| SPA framework (React/Vue/Angular) | Browser |
| Baidu mini-program (`smartapps.cn`) | Browser or find alternate URL |
| Social media embeds (Weibo, Douyin) | Browser, but often no structured data |

### Reusable mappings

When the same source consistently maps to the same value across rows/sheets:
1. Build a mapping table after confirming 2+ instances
2. Apply mappings to future rows without re-fetching
3. Always note the mapping source for audit

### Common "no data" patterns

These formats typically have no individual attribution:
- Flash news / wire alerts (e.g., "财联社电", "每经AI快讯")
- Press releases / corporate announcements
- Social media reposts without original attribution
- Aggregated roundup articles

Mark these clearly (leave blank or use a placeholder like "/" per user preference).

## Row Alignment Safety

**Critical**: Off-by-one errors are the #1 failure mode when writing to spreadsheets.

Before every write:
1. Read the target row to verify the adjacent cells match expectations
2. If processing multiple rows, re-read periodically to catch drift
3. Never assume row N in your data maps to row N in the sheet — always verify

## Feishu Sheets Specifics

- Range format: `sheetId!A1:B2` (not sheet name)
- Single-cell write: `sheetId!G5:G5` (not `sheetId!G5`)
- Get sheet IDs via `feishu_sheet` action `info`
- Write returns `revision` number — useful for tracking changes
- Cannot create new sheet tabs in existing spreadsheet via API; create a new spreadsheet for summaries

## Output Format

Summary sheets should include:
- **Headers**: Group dimension, detail dimension, count, total
- **Subtotals**: Per group
- **Grand total**: Final row
- **Sorting**: By total descending within each group, groups ordered by subtotal descending
