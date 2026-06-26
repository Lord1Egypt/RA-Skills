---
name: "@web-scraper-trae"
description: "Opens browser and scrapes webpage content using Playwright. Invoke when user wants to crawl/scrape a webpage, extract data from a website, or get content from a URL."
allowed-tools: Bash(node:*)
---

# Web Scraper Trae

Opens a browser using Playwright and scrapes webpage content.

## Prerequisites

```bash
npm install playwright
npx playwright install chromium
```

## Usage

When user provides a URL, create a Node.js script to scrape the page:

```javascript
const { chromium } = require('playwright');

async function scrape(url) {
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });

  const title = await page.title();
  const text = await page.textContent('body');
  const html = await page.content();

  await browser.close();

  return { title, text, html, url };
}

const url = process.argv[2];
if (!url) {
  console.error('请提供 URL 参数');
  process.exit(1);
}

scrape(url).then(result => {
  console.log('=== SCRAPE_RESULT ===');
  console.log(JSON.stringify(result, null, 2));
}).catch(err => {
  console.error('爬取失败:', err.message);
  process.exit(1);
});
```

## Execution

Run the script with:
```bash
node scrape.js "https://example.com"
```

## Output Format

Return JSON with:
- `title`: Page title
- `text`: Visible text content (HTML stripped)
- `html`: Full HTML source
- `url`: Original URL

## Notes

- Use `headless: true` for server environments
- Use `waitUntil: 'networkidle'` to ensure full page load
- Set timeout to 60 seconds for slow pages
- Handle SPA (Single Page Applications) that load content dynamically
- For pages requiring interaction, use `playwright-cli` skill instead
