---
name: xhs-suggest-keywords
description: Xiaohongshu (RED) search suggestion keyword collection tool. Uses browser automation to visit the Xiaohongshu Explore page, type keywords in the search bar, and collect the auto-suggest keyword list from the dropdown. 
---

# Xiaohongshu Search Suggest Keywords Collection

Collect Xiaohongshu search bar auto-suggest keywords via Playwright browser automation, for SEO/GEO content optimization.

## Use Cases

Used for SEO/GEO optimization. Suitable for keyword research, content strategy, and search optimization scenarios.

## Workflow

```
Input seed keywords → Visit xiaohongshu.com/explore → Focus search bar → Type keyword → Wait for suggestion dropdown → Collect suggestion list → Output results
```

## Prerequisites

```bash
npm install playwright
npx playwright install chromium
```

## Core Script

```js
const { chromium } = require('playwright');

async function collectSuggestKeywords(seedKeywords, options = {}) {
  const { headless = true, delay = 800, maxPerSeed = 10 } = options;
  const browser = await chromium.launch({ headless });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
  });
  const page = await context.newPage();
  
  const results = {};
  
  for (const keyword of seedKeywords) {
    try {
      // Visit the search explore page
      await page.goto('https://www.xiaohongshu.com/explore', { 
        waitUntil: 'networkidle', 
        timeout: 15000 
      });
      
      // Wait for the search bar to appear and click it
      await page.waitForSelector('#search-input', { timeout: 10000 });
      await page.click('#search-input');
      await page.waitForTimeout(500);
      
      // Clear and type the keyword
      await page.fill('#search-input', '');
      await page.type('#search-input', keyword, { delay: 100 });
      await page.waitForTimeout(delay);
      
      // Wait for the suggestion dropdown to appear
      const suggestSelector = '.suggest-item, .search-suggest-item, [class*="suggest"]';
      await page.waitForSelector(suggestSelector, { timeout: 5000 }).catch(() => {});
      await page.waitForTimeout(300);
      
      // Extract suggested keywords
      const suggestions = await page.evaluate((selector) => {
        const items = document.querySelectorAll(
          '.suggest-item, .search-suggest-item, [class*="suggest"] span, .suggest-item .text'
        );
        return Array.from(items)
          .map(el => el.textContent?.trim())
          .filter(t => t && t.length > 0);
      }, suggestSelector);
      
      results[keyword] = [...new Set(suggestions)].slice(0, maxPerSeed);
      console.log(`[${keyword}] → ${results[keyword].length} suggestions`);
      
    } catch (err) {
      console.error(`[${keyword}] collection failed:`, err.message);
      results[keyword] = [];
    }
  }
  
  await browser.close();
  return results;
}

// Usage example
(async () => {
  const seeds = ['skincare', 'outfits', 'travel guide', 'fitness'];
  const result = await collectSuggestKeywords(seeds, {
    headless: false,   // Set to false for debugging
    delay: 1000,
    maxPerSeed: 15
  });
  
  console.log('\n=== Collection Results ===');
  for (const [seed, keywords] of Object.entries(result)) {
    console.log(`\n📌 ${seed}:`);
    keywords.forEach((kw, i) => console.log(`  ${i + 1}. ${kw}`));
  }
})();
```

## Selector Adaptation

The DOM structure of Xiaohongshu's search suggestions may change. Alternative selectors:

| Scenario | Selector |
|----------|----------|
| Search input box | `#search-input`, `input[placeholder*="search"]` |
| Suggestion item container | `.suggest-list`, `.search-suggest`, `[class*="suggest"]` |
| Individual suggestion item | `.suggest-item .text`, `.suggest-item span`, `.suggest-word` |

> Actual selectors may need adjustment based on the current page DOM. See [references/selectors.md](references/selectors.md) for details.