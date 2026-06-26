# Browser Automation Flow (Fallback)

When the Python script is unavailable, use `agent-browser` directly.

## Steps

```bash
# 1. Open
agent-browser open 'https://substack.com/search/QUERY?utm_source=global-search&searching=all_posts&dateRange=day'

# 2. Wait
agent-browser wait --load networkidle

# 3. Snapshot
agent-browser snapshot -i

# 4. Optional: scroll for more results
agent-browser scroll down 800
agent-browser snapshot -i

# 5. Close
agent-browser close
```

## Key Snapshot Patterns to Extract

Look for lines matching:
```
- link "PUBLICATION_NAME" [ref=eN]
- button "Copy link" [ref=eM]
```

Article text is embedded within the `link` element that precedes a `Copy link` button.
It typically contains: publication name, date, title, subtitle, author, read time.

## Date Range Values

- `day` — Last 24 hours
- `week` — Past 7 days
- `month` — Past 30 days

Change the URL parameter `dateRange=` accordingly.
