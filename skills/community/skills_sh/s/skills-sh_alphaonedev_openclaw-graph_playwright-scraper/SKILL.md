---
name: playwright-scraper
cluster: community
description: "Playwright web scraping: dynamic content, auth flows, pagination, data extraction, screenshots"
tags: ["playwright","scraping","automation","web"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "playwright scrape dynamic content auth pagination extract screenshot"
---

## playwright-scraper

### Purpose
This skill enables web scraping using Playwright, a Node.js library for browser automation. It focuses on handling dynamic content, authentication flows, pagination, data extraction, and screenshots to reliably scrape modern websites.

### When to Use
Use this skill for scraping sites with JavaScript-rendered content (e.g., React or Angular apps), sites requiring login (e.g., dashboards), handling multi-page results (e.g., search results), or capturing visual data (e.g., screenshots for verification). Avoid for static HTML sites where simpler tools like requests suffice.

### Key Capabilities
- Dynamically load and interact with content using Playwright's browser control.
- Manage authentication flows, such as logging in via forms or API tokens.
- Handle pagination by navigating pages, clicking "next" buttons, or parsing URLs.
- Extract data using selectors, with options for JSON output or file saves.
- Capture screenshots or full-page PDFs for debugging or reporting.
- Supports headless or visible browser modes for flexibility.

### Usage Patterns
Always initialize a browser context first, then create pages for navigation. Use async patterns for reliability. For authenticated scraping, handle cookies or sessions per context. Structure scripts to loop through pages for pagination and use try-catch for flaky elements. Pass configurations via JSON files or environment variables for reusability.

### Common Commands/API
Use Playwright's Node.js API. Install via `npm install playwright`. Key methods include:
- Launch browser: `const browser = await playwright.chromium.launch({ headless: true });`
- Navigate page: `const page = await browser.newPage(); await page.goto('https://example.com');`
- Handle auth: `await page.fill('#username', process.env.USERNAME); await page.fill('#password', process.env.PASSWORD); await page.click('#login');`
- Extract data: `const data = await page.evaluate(() => document.querySelector('#target').innerText); console.log(data);`
- Pagination: `while (await page.$('#next-button')) { await page.click('#next-button'); await page.waitForSelector('.item'); }`
- Take screenshot: `await page.screenshot({ path: 'screenshot.png' });`
CLI flags for running scripts: Use `npx playwright test` with flags like `--headed` for visible mode or `--timeout 30000` for extended waits.

### Integration Notes
Integrate by importing Playwright in Node.js projects. For auth, use environment variables like `$PLAYWRIGHT_USERNAME` and `$PLAYWRIGHT_PASSWORD` to avoid hardcoding. Configuration format: Use a JSON file for settings, e.g., `{ "url": "https://target.com", "selector": "#data-element" }`. Pass it via script args: `node scraper.js --config config.json`. For larger systems, chain with tools like Puppeteer (if migrating) or export data to databases via `page.evaluate` results. Ensure compatibility with Node.js 14+ and handle proxy settings with `browser.launch({ proxy: { server: 'http://myproxy.com:8080' } })`.

### Error Handling
Anticipate common errors like timeout on dynamic loads or selector failures. Use `page.waitForSelector` with timeouts: `await page.waitForSelector('#element', { timeout: 10000 }).catch(err => console.error('Element not found:', err));`. For network issues, wrap `page.goto` in try-catch: `try { await page.goto(url, { waitUntil: 'networkidle' }); } catch (e) { console.error('Navigation failed:', e.message); await browser.close(); }`. Handle authentication failures by checking for error elements: `if (await page.$('#error-message')) { throw new Error('Login failed'); }`. Log errors with details and retry up to 3 times using a loop.

### Concrete Usage Examples
1. **Scraping a logged-in dashboard:** First, set env vars: `export PLAYWRIGHT_USERNAME='user@example.com'` and `export PLAYWRIGHT_PASSWORD='securepass'`. Then, run: `const browser = await playwright.chromium.launch(); const page = await browser.newPage(); await page.goto('https://dashboard.com/login'); await page.fill('#username', process.env.PLAYWRIGHT_USERNAME); await page.fill('#password', process.env.PLAYWRIGHT_PASSWORD); await page.click('#submit'); const data = await page.evaluate(() => document.querySelector('#dashboard-data').innerText); console.log(data); await browser.close();` This extracts data from a protected page.
2. **Handling pagination on a search site:** Script: `const browser = await playwright.chromium.launch(); const page = await browser.newPage(); await page.goto('https://search.com?q=query'); let items = []; while (true) { items.push(...await page.$$eval('.result-item', elements => elements.map(el => el.innerText))); const nextButton = await page.$('#next-page'); if (!nextButton) break; await nextButton.click(); await page.waitForTimeout(2000); } console.log(items); await browser.close();` This collects results across multiple pages.

### Graph Relationships
- Related to: "selenium-automation" (alternative browser automation tool)
- Depends on: "node-runtime" (for Playwright execution)
- Complements: "data-extraction" (for post-processing scraped data)
- In cluster: "community" (shared with other open-source tools)
