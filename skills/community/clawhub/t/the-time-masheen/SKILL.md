---
name: time-masheen
description: THE_TIME_MASHEEN — full-spectrum web intelligence combining live scraping, historical time travel, and interactive browser automation. Use when: (1) scraping or crawling any live website (static, JS-heavy, or rendering-protected), (2) going back in time to retrieve archived or historical versions of any page via the Wayback Machine, (3) comparing what a site looks like now vs. what it looked like in any previous year, (4) automating browser interactions (login, click, fill forms) on web apps that can't be passively scraped, (5) extracting data from login-gated or paywalled pages, or (6) any task requiring live scraping + historical research + browser interaction in combination. Triggers on: "scrape this", "crawl", "wayback", "archive", "what did this site look like", "compare current vs historical", "browser automation", "extract data from", "log in and scrape", "go back in time on".
---

# THE_TIME_MASHEEN

> *Step in. Go back. Scrape the dead. Automate the living.*

Three-layer web intelligence stack. Pick the right layer — or combine all three.

| Layer | Tool | Job |
|-------|------|-----|
| **Live** | Scrapling | Extract content from any live URL |
| **Historical** | Wayback Machine CDX API | Travel back in time to any archived snapshot |
| **Interactive** | playwright-cli | Drive a real browser — login, click, scroll, fill forms |

---

## Decision Tree

```
Need web data?
│
├─ Historical / "what did it look like before"?
│    └─ Wayback CDX API → scrape snapshot via Scrapling or web_fetch
│
├─ Need to click / log in / fill forms first?
│    └─ playwright-cli → authenticate → hand off to Scrapling
│
└─ Just current content?
     ├─ Static / simple       → scrapling get
     ├─ JS-heavy / React      → scrapling fetch --network-idle
     └─ Heavily protected sites → scrapling stealthy-fetch --solve-cloudflare
```

---

## Layer 1 — Live Scraping (Scrapling)

### Escalation path (always start at the top)

```bash
# 1. Static sites, blogs, docs
scrapling extract get "https://example.com" output.md

# 2. JS-heavy / React / Next.js / dynamic content
scrapling extract fetch "https://example.com" output.md --network-idle --wait 3000

# 3. Cloudflare / rendering-protected
scrapling extract stealthy-fetch "https://example.com" output.md --solve-cloudflare
```

### Extract specific sections (saves tokens)
```bash
scrapling extract fetch "https://example.com" output.md --css-selector "main article"
scrapling extract get "https://example.com" output.md --css-selector ".pricing-table"
```

**Rules:**
- Always clean up temp files after reading
- Use `.md` output for readable text, `.html` only for structure parsing
- Use `--css-selector` to avoid giant HTML blobs

See `references/scrapling.md` for full CLI flags, spider framework, and Python API.

---

## Layer 2 — Time Travel (Wayback Machine)

### Find all snapshots of a URL
```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=example.com&output=json&fl=timestamp,statuscode&filter=statuscode:200&limit=20"
```

### One snapshot per year (change tracking)
```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=example.com&output=json&collapse=timestamp:4&fl=timestamp,statuscode&filter=statuscode:200"
```

### Scrape a specific point in time
```bash
# Scrapling for clean extraction:
scrapling extract get "https://web.archive.org/web/20230601000000/https://example.com/" archive.md

# Or read via web_fetch:
# web_fetch: https://web.archive.org/web/20230601000000/https://example.com/
```

### Check if a URL has ever been archived
```bash
curl -s "https://archive.org/wayback/available?url=example.com" | python3 -m json.tool
```

See `references/wayback.md` for full CDX API reference and `ia` CLI usage.

---

## Layer 3 — Interactive Automation (playwright-cli)

Use when the page requires login, clicking, or dynamic interaction before content is accessible.

```bash
# Open browser
playwright-cli open https://app.example.com

# Snapshot to get element refs
playwright-cli snapshot

# Interact
playwright-cli click e12
playwright-cli fill e5 "username@example.com"
playwright-cli press Tab
playwright-cli fill e6 "password"
playwright-cli press Enter

# Capture state
playwright-cli screenshot
playwright-cli eval "document.title"

# Close
playwright-cli close
```

### Handoff pattern — authenticate then bulk scrape
```bash
# 1. playwright-cli open → log in → navigate to target
# 2. playwright-cli screenshot  # verify you're authenticated
# 3. scrapling extract get <url> output.md  # scrape while session is active
```

---

## Combining All Three

### Live vs. archived comparison (price changes, content drift, competitive intel)
```bash
# 1. Scrape current state
scrapling extract get "https://competitor.com/pricing" current.md

# 2. Find yearly snapshots
curl -s "https://web.archive.org/cdx/search/cdx?url=competitor.com/pricing&output=json&collapse=timestamp:4&fl=timestamp&filter=statuscode:200"

# 3. Scrape archived version from any year
scrapling extract get "https://web.archive.org/web/20230101000000/https://competitor.com/pricing" archive.md

# 4. Diff
diff archive.md current.md
```

### Login-gated site — full extraction
```bash
# playwright handles auth → Scrapling does the bulk lift
playwright-cli open https://example.com/login
playwright-cli fill e5 "your@email.com"
playwright-cli fill e6 "password"
playwright-cli press Enter
playwright-cli screenshot  # verify you're in
scrapling extract get "https://example.com/members/content" output.md
```

---

## Security

This skill opens real browser sessions and can scrape login-protected pages. A few things to understand before using it:

- **You control the browser.** playwright-cli drives a browser on your machine. It navigates to URLs you specify and interacts with elements you tell it to.
- **All data stays local.** Any session state used during automation exists only on your machine and is used only for the scraping task you initiate.
- **Use only on sites you have access to.** This skill is designed for legitimate web research — competitive intelligence, content monitoring, archival work, and accessing sites you have an account on. It is not a tool for unauthorized access.
- **Review commands before running.** As with any automation tool, understand what you're running before you run it.

---

### CLI-Anything — make any software agent-native
When you need a full CLI harness for any desktop or web application:
```bash
# Install once in Claude Code
/plugin marketplace add HKUDS/CLI-Anything
/plugin install cli-anything

# Build a complete CLI for any software (7-phase pipeline)
/cli-anything:cli-anything ./target-app

# Iteratively refine
/cli-anything:refine ./target-app "focus on data export workflows"
```
