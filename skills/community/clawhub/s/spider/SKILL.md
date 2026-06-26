---
name: spider
version: 1.0.0
author: swei
description: Web scraping using Chrome + WebMCP. Primary method for all web crawling tasks.
metadata: { "openclaw": { "emoji": "🕷️" } }
---

# Spider — Web Scraping Tool

**This is the default web scraping method**, replacing older approaches like web_fetch.

---

## Trigger Conditions

**Use this skill when user says**:

| Keywords | Action |
|----------|--------|
| **抓取 / crawl / scrape / fetch** | Use Chrome + WebMCP to scrape web pages |
| **采集** | Same as above |
| **获取...新闻** | Scrape news pages |
| **从...网站** | Specify website to scrape |
| **同花顺** | Scrape Tonghuashun (10jqka) data |
| **东方财富** | Scrape East Money data |
| **雪球** | Scrape Xueqiu data |
| **百度** | Search or scrape Baidu content |

---

## Usage Examples

| User Input | Execution |
|------------|-----------|
| "抓取光库科技的新闻" | Open Tonghuashun in Chrome, extract news |
| "抓取宁德时代的股吧" | Open East Money guba in Chrome |
| "从同花顺抓取xxx" | Open Tonghuashun page in Chrome |
| "search xxx" | Open Google search in Chrome |
| "查一下xxx" | Search or scrape in Chrome |

---

## Operation Flow

### 1. Check Chrome Status

```javascript
{ action: "status" }
```

If not running, start it:
```javascript
{ action: "start" }
```

### 2. Open Target Page

```javascript
{ action: "open", targetUrl: "https://stockpage.10jqka.com.cn/300620/news/", target: "host" }
```

### 3. Get Page Snapshot

```javascript
{ action: "snapshot", targetId: "xxx", maxChars: 20000 }
```

### 4. Page Interaction (click, type, etc.)

```javascript
{ action: "act", targetId: "xxx", request: {"kind": "click", ref: "e33"} }
```

### 5. Cleanup: Return to about:blank

```javascript
{ action: "navigate", targetId: "xxx", url: "about:blank" }
```

---

## Common Website Templates

### Tonghuashun Stock News

```
URL: https://stockpage.10jqka.com.cn/{stock_code}/news/
Example: https://stockpage.10jqka.com.cn/300620/news/
```

### East Money Guba (Stock Forum)

```
URL: https://guba.eastmoney.com/list,{stock_code}.html
Example: https://guba.eastmoney.com/list,300620.html
```

### Xueqiu (Snowball)

```
URL: https://xueqiu.com/S/SZ{stock_code}
Example: https://xueqiu.com/S/SZ300620
```

### Baidu News Search

```
URL: https://www.baidu.com/s?wd={keyword}&tn=news
```

---

## Chrome Setup (One-time)

1. Open Chrome Flags:
   - `chrome://flags/#enable-experimental-web-platform-features` → Enabled
   - `chrome://flags/#enable-webmcp-testing` → Enabled
2. Fully quit Chrome (Cmd+Q) and restart

---

## Important Rules

1. **Use target="host"** instead of "sandbox"
2. **Must cleanup after each task**:
   - If multiple tabs exist, **keep only one**, close others
   - The remaining tab must navigate to `about:blank`
   - If multiple `about:blank` tabs exist, keep only the latest one, close others
   - Use `browser action: tabs` to check current tab status
   - After cleanup, ensure only one `about:blank` tab remains
3. **Reuse existing tabs**, avoid opening new tabs frequently
4. **Handle anti-scraping sites**: Tonghuashun, East Money need complete JavaScript loading

---

## Error Handling

| Error | Solution |
|-------|----------|
| Sandbox unavailable | Use target="host" |
| Slow page load | Wait for snapshot to return before操作 |
| Content extraction failed | Use snapshot's maxChars to get more content |
| Anti-scraping blocked | Try other finance sites or wait and retry |

---

## Default Scraping Priority

1. **Spider (Chrome + WebMCP)** ← Primary method
   - Suitable for: Finance websites, stock news, forums
   - Advantages: Full JavaScript rendering, interactive

2. **web_fetch** ← Backup method
   - Suitable for: Simple static pages
   - Disadvantage: Cannot handle JavaScript-rendered pages
