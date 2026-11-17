---
name: smart-web-search
description: Smart web search with auto region detection and dual-tier content fetching. Works in both China and international networks.
version: 3.2.2
author: smart-web-search
trigger_keywords:
  - search
  - find
  - look up
  - 搜索
  - 查一下
tools:
  - name: search
    description: Smart search with auto Bing/DDG selection and content fetching
    script: scripts/search.js
    parameters:
      query:
        type: string
        description: "Search query"
        required: true
      max:
        type: integer
        description: "Max results 1-30, default 10"
        required: false
      fetch:
        type: integer
        description: "Fetch top N page contents, default 3, 0 to disable"
        required: false
      region:
        type: string
        description: "Region override: auto/cn/intl (auto = IP detection)"
        required: false
---

# smart-web-search v2.0.0

Intelligent web search with region auto-detection and dual-tier content extraction.

## Core features

### 1. Auto region detection
- Detects CN vs international via IP geolocation APIs + cn.bing.com probe
  - CN → Bing CN (Playwright full flow)
  - International → DDG HTML (Playwright full flow)
- Fallback: defaults to DDG on detection failure (proxy/timeout)
- Manual override available via `--region cn/intl`

### 2. Dual-tier content fetching
After search, auto-fetches top N page contents (default 3):
- Tier 1: HTTP + cheerio (fast, no browser)
- Tier 2: Playwright headed (JS rendering fallback)

## Install

All dependencies are installed upfront by the setup script. **The skill never runs `npm install` or `pip install` at runtime.**

### Prerequisites

| Dependency | Purpose | Size |
|---|---|---|
| Node.js >= 18 | Runtime | — |
| cheerio | HTML parsing | small |
| commander | CLI arg parsing | small |
| iconv-lite | GBK charset | small |
| playwright | Browser automation | ~50 MB |
| Chromium (Playwright) | Browser engine | ~150 MB |

### One-command setup

```bash
# Linux / macOS
bash scripts/setup.sh

# Windows
powershell -File scripts/setup.ps1
```

Auto-detects region and uses `npmmirror.com` mirrors inside China.

### Manual install

```bash
cd skills/smart-web-search
npm install
npx playwright install chromium

# Verify
node scripts/check-env.js
```

Skip 150 MB download if you have system Chrome:

```bash
export CHROMIUM_EXECUTABLE_PATH="/path/to/chrome"
```

## Usage

```bash
# Search with auto-fetch (top 3 pages)
node scripts/search.js "白银价格"
node scripts/search.js "how to deploy docker" --max=5

# Disable fetch (search only)
node scripts/search.js "xxx" --fetch=0

# Override region detection
node scripts/search.js "深圳旅游攻略" --region=cn

# Fetch specific URLs
node scripts/fetch.js "https://example.com/page1" "https://example.com/page2"
```

## Privacy & network

- Searches connect to Bing CN / DDG HTML via Playwright (full browser automation)
- **Playwright session**: Opens browser homepage to establish session cookies, then submits search via form input. Browser context closes after search completes.
- No analytics, no telemetry, no third-party logging beyond search engine server logs

## Known limitations

- **Playwright overhead adds 5–8s**: Full browser automation for cookie/session handling
- **Proxy interference**: IP detection may misclassify; use `--region cn/intl` to override
- **JS-required pages**: HTTP tier returns empty for SPA pages; headed tier catches them

## Verification

```bash
node scripts/check-env.js
node scripts/search.js "OpenClaw" --max 2 --fetch 0
```

Common issues:
- `node_modules not found` → run `npm install`
- `Executable doesn't exist` → run `bash scripts/setup.sh` or set `CHROMIUM_EXECUTABLE_PATH`
- 0 results → network issue or search engine blocking; try different query
