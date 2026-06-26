---
name: wechat-article-reader
description: Read and summarize WeChat Official Account articles (微信公众号文章) by URL. Bypasses WeChat's anti-bot detection to extract full article text, title, author, date, and optionally capture a full-page screenshot with lazy-loaded images. Use when a user shares a mp.weixin.qq.com link and asks to read, summarize, analyze, or screenshot it.
---

# WeChat Article Reader

Read and summarize WeChat Official Account articles that `web_fetch` and standard headless browsers cannot access.

## Recommended Workflow

When a user shares a WeChat article link:

1. **Fetch text** — `node scripts/fetch_wechat.js <url> --json` (required)
2. **Take screenshot** — `node scripts/screenshot_wechat.js <url> --out=/tmp/wechat_article.png` (best-effort, run in parallel with step 1)
3. **Send screenshot** — `message(action=send, media=/tmp/wechat_article.png)` if step 2 succeeded; skip silently if it failed
4. **Send summary** — text summary following the output format below
5. **Clean up** — delete the temporary screenshot file

Steps 1 and 2 can run in parallel. The screenshot is recommended but not mandatory — if it fails (timeout, rendering issue, etc.), proceed with the text summary only. Do not block the response waiting for a screenshot that may never succeed.

## Why Standard Methods Fail

WeChat blocks bots by checking four signals. This skill defeats all four:

| Signal | Standard browser | This skill |
|--------|-----------------|-----------|
| Chrome binary | Chromium (bot fingerprint) | Real Chrome |
| User-Agent | Desktop/headless | iPhone Safari |
| `navigator.webdriver` | `true` (exposed) | `undefined` (hidden) |
| Blink automation flag | Present | Disabled |

## Prerequisites

Two dependencies are required. The scripts auto-detect their paths but do NOT auto-install them.

**1. Google Chrome (stable)**
```bash
# Check
which google-chrome-stable

# Install (Debian/Ubuntu)
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt-get update && apt-get install -y google-chrome-stable

# macOS
brew install --cask google-chrome
```

**2. playwright-core**
```bash
# Check (auto-discovered from nvm paths)
node -e "require('playwright-core')"

# Install if missing
npm install -g playwright-core
```

If either dependency is missing, the scripts will exit with a clear error message and the install command above.

## Standard Workflow (Always Follow This Order)

When a user shares a `mp.weixin.qq.com` link and asks to read/summarize/explain it, execute these steps **every time** — no skipping:

1. **Fetch text** — run `fetch_wechat.js --json` to get title, author, date, content
2. **Take screenshot** — run `screenshot_wechat.js --out=/tmp/wechat_screenshot.png`
3. **Send screenshot** — use `message(action=send, media=/tmp/wechat_screenshot.png)` to push the image to the channel
4. **Send text summary** — reply with the two-part format (📌 Overview + 🔎 Deep Dive)
5. **Delete temp file** — `rm /tmp/wechat_screenshot.png`

Steps 1 and 2 can run in parallel. Step 3 must complete before step 4 (image first, text second).

**Never skip the screenshot.** Even if the user only asks to "explain" or "summarize" — always send the screenshot alongside the text. It gives visual context and confirms the article was actually read.

---

## Fetching Article Text

```bash
# Basic text output
node scripts/fetch_wechat.js "https://mp.weixin.qq.com/s/XXXXX"

# JSON output (title + author + date + content)
node scripts/fetch_wechat.js "https://mp.weixin.qq.com/s/XXXXX" --json

# Limit output length
node scripts/fetch_wechat.js "https://mp.weixin.qq.com/s/XXXXX" --max-chars=5000

# Custom Chrome path
node scripts/fetch_wechat.js "https://mp.weixin.qq.com/s/XXXXX" --chrome-path=/usr/bin/chromium
```

## Taking a Screenshot

Captures the full article area (title + author + body), with CSS injection to hide WeChat promotional footers, action bars, and contact sections. All fixed/sticky DOM elements are hidden before capture to prevent overlay artifacts.

Selector priority: `#js_article` → `.rich_media_wrp` → `#js_content` (fallback, no title).

The script auto-scrolls to bottom before capture to trigger lazy-loaded images.

```bash
# Default output: /tmp/wechat_screenshot.png
node scripts/screenshot_wechat.js "https://mp.weixin.qq.com/s/XXXXX"

# Custom path
node scripts/screenshot_wechat.js "https://mp.weixin.qq.com/s/XXXXX" --out=/tmp/article.png
```

**Important:** Uses `waitUntil: 'load'` (not `networkidle`) — WeChat pages have background requests that never settle, causing `networkidle` to time out.

After sending the screenshot, delete the temporary file.

## Summarizing Articles — Output Format

Two-part structure. **Match the user's language** — respond in Chinese if the user writes in Chinese, English if English.

Both parts cover the same content at different depths. Same voice throughout. Keep it objective: report only what the article says — no personal session context, no action items, no subjective opinions.

### Part 1 — Summary (📌 Overview)

- Open with 1–2 sentences: what happened and why it matters
- Follow with 3–5 bullet points (▸) — the most important points
- Each bullet: one sentence, specific enough to be informative, short enough to scan

### Part 2 — Details (🔎 Deep Dive)

- **Must cover every item from Part 1**, in the same order — no cherry-picking, no reordering
- Open with a transition sentence that connects back to Part 1
- Each item: grouped under a ▸ topic header + 2–3 sentences covering mechanism, data/quotes, and the author's angle
- Close with 1–2 sentences capturing the article's core thesis
- Aim for 200–400 words depending on article length. Do NOT reproduce the full article.

### Example Output (English article)

```
📌 Overview

OpenClaw 2026.3.7 upgrades memory management from a closed architecture to a
plugin-based system. With the lossless-claw plugin, long-context performance
now surpasses Claude Code for the first time on the OOLONG benchmark.

▸ New ContextEngine plugin slot lets third parties replace built-in lossy compression
▸ ACP channel bindings now persist across server restarts
▸ Toolchain improvements: search accuracy, local model inference, Docker deployment
▸ Security layer adds prompt-injection protection and credential safeguards
▸ Breaking change: gateway.auth.mode must be explicitly set when both auth methods are configured


🔎 Deep Dive

The following expands on each point from the overview above.

▸ Pluggable Memory
lossless-claw uses a DAG structure for lossless compression, scoring 74.8 on
OOLONG vs. Claude Code's 70.3 — a gap that widens with longer context. One
engineer who tested it for a week called the improvement "conservative to call
it 'working well'."

▸ Persistent ACP Bindings
Discord and Telegram topics can now bind to a dedicated agent, with the
binding surviving restarts and context carrying over. Each topic can route
to a different agent independently.

▸ Toolchain Upgrades
Perplexity replaced with Search API, adding language/region/time filters.
Ollama streaming no longer interleaves reasoning traces. Docker now ships
with pre-packaged extension dependencies.

▸ Security Hardening
New prependSystemContext / appendSystemContext hooks added alongside prompt
injection protection and credential-scraping prevention.

▸ Breaking Change
If both gateway.auth.token and gateway.auth.password are set, you must now
explicitly specify gateway.auth.mode — otherwise the gateway may fail to start.

Overall, this release marks a shift from a monolithic architecture toward a
plugin ecosystem where the community can replace and extend core components.
```

## Limitations

Cannot read:
- Deleted articles
- Paid/subscriber-only content
- Followers-only articles (require WeChat login)

Transient CAPTCHA may appear rarely — retrying usually works.
