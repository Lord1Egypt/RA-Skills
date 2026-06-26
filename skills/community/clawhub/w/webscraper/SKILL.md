---
name: webscraper
description: "Extract readable content from web pages. Use when: user wants to read article content, fetch documentation, grab product info, or get text from URLs. NOT for: interactive sites, login-required pages, or complex JavaScript-rendered content."
homepage: https://docs.openclaw.ai/tools/web
metadata: { "openclaw": { "emoji": "🕸️", "requires": { "bins": ["curl", "node"] } } }
---

# WebScraper Skill

Extract and parse content from web pages into readable markdown or plain text.

## When to Use

✅ **USE this skill when:**

- "Read this article: [URL]"
- "What does this page say?"
- "Get the content from [URL]"
- Fetch documentation, blog posts, news articles
- Extract product information from e-commerce sites
- Grab API documentation or tutorials
- Summarize web page content

## When NOT to Use

❌ **DON'T use this skill when:**

- Login-required pages (use BrowserAgent with session)
- Heavy JavaScript-rendered content (use BrowserAgent)
- Interactive web apps (dashboards, SPAs)
- CAPTCHA-protected sites
- Sites with strict anti-bot measures
- Real-time data (stock tickers, live scores)

## Commands

### Fetch URL Content

```bash
# Using OpenClaw web_fetch tool (recommended)
# Called via tool, not direct CLI

# Basic fetch (markdown output)
web_fetch(url: "https://example.com/article")

# Text-only mode (no markdown)
web_fetch(url: "https://example.com/article", extractMode: "text")

# Limit content length
web_fetch(url: "https://example.com/article", maxChars: 5000)
```

### Using curl (fallback)

```bash
# Simple HTML fetch
curl -s "https://example.com" | html2text -width 80

# With user-agent (avoid bot detection)
curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "https://example.com"

# Fetch and extract main content (requires readability-cli)
curl -s "https://example.com" | readability

# Get just the title
curl -s "https://example.com" | grep -oP '(?<=<title>).*?(?=</title>)'
```

### Using Node.js (advanced)

```bash
# Install cheerio for HTML parsing
npm install -g cheerio

# Parse HTML with Node
node -e "
const cheerio = require('cheerio');
const html = \`\$(curl -s 'https://example.com')\`;
const \$ = cheerio.load(html);
console.log(\$('article').text());
"
```

## Response Format

When fetching content, structure responses as:

```markdown
## 📄 [Page Title]

**Source:** [URL](https://...)
**Fetched:** 2026-03-20

### Content

[Extracted content here...]

---
*Summary: [1-2 sentence summary if helpful]*
```

## Best Practices

### 1. Respect Rate Limits

```bash
# Add delay between requests
sleep 2 && curl "https://example.com/page1"
sleep 2 && curl "https://example.com/page2"
```

### 2. Use Proper User-Agent

```bash
# Desktop Chrome
curl -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Mobile Safari
curl -A "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
```

### 3. Handle Errors

```bash
# Check HTTP status
curl -s -o /dev/null -w "%{http_code}" "https://example.com"

# Timeout after 10 seconds
curl -s --max-time 10 "https://example.com"

# Retry on failure
curl -s --retry 3 "https://example.com"
```

### 4. Extract Specific Content

```bash
# Get all links
curl -s "https://example.com" | grep -oP 'href="\K[^"]+' | head -20

# Get images
curl -s "https://example.com" | grep -oP 'src="\K[^"]+\.(jpg|png|webp)'

# Get meta description
curl -s "https://example.com" | grep -oP '(?<=<meta name="description" content=")[^"]+'
```

## Integration with OpenClaw

### Using web_fetch Tool

```javascript
// In your agent code
const content = await web_fetch({
  url: "https://example.com/article",
  extractMode: "markdown",  // or "text"
  maxChars: 10000
});
```

### Batch Processing

For multiple URLs, process sequentially with delays:

```
URL1 → fetch → wait 2s → URL2 → fetch → wait 2s → URL3 → fetch
```

## Common Use Cases

### 1. Article Summarization

```
1. Fetch article content
2. Extract main text (remove nav, footer, ads)
3. Generate summary
4. Return with source attribution
```

### 2. Product Information

```
1. Fetch product page
2. Extract: name, price, description, specs
3. Format as structured data
4. Return comparison-ready format
```

### 3. Documentation Lookup

```
1. Fetch docs page
2. Extract relevant section
3. Search for specific topic
4. Return code examples + explanations
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Content empty/missing | Site uses JS rendering → use BrowserAgent |
| Blocked by site | Add User-Agent, add delay, use proxy |
| Timeout | Increase timeout, check URL validity |
| Garbled text | Check charset, try text mode |
| Login required | Use BrowserAgent with session cookies |

## Related Skills

- **BrowserAgent** - For interactive/JS-heavy sites
- **web_search** - For finding URLs before fetching
- **coding-agent** - For processing extracted data

## Security Notes

⚠️ **Important:**

- Respect robots.txt
- Don't scrape personal data
- Honor copyright/terms of service
- Add delays between requests (2-5s)
- Don't overload servers
- Use official APIs when available
