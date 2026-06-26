# Xiaohongshu Search Suggest DOM Selectors

Xiaohongshu's web client uses a React SPA, with the suggestion list rendered dynamically. Below are common selector patterns.

## Search Entry

```
URL: https://www.xiaohongshu.com/explore
Search bar: input[placeholder="Search Xiaohongshu"]
            #search-input
```

## Suggestion Dropdown Selectors (by Priority)

| Priority | Selector | Description |
|----------|----------|-------------|
| 1 | `.suggest-list .suggest-item .text` | Most common structure |
| 2 | `.search-suggest-item span` | Alternative structure |
| 3 | `div[class*="suggest"] span:not(.icon)` | Generic match |
| 4 | `[class*="SearchSuggest"] [class*="item"] div` | CSS Module style |

## DOM Observation Method

When static selectors are ineffective, use MutationObserver for dynamic capture:

```js
const suggestions = await page.evaluate(() => {
  return new Promise((resolve) => {
    const results = [];
    const observer = new MutationObserver((mutations) => {
      for (const m of mutations) {
        for (const node of m.addedNodes) {
          // Match suggestion items
          if (node.textContent && node.tagName !== 'SCRIPT') {
            const text = node.textContent.trim();
            if (text && !results.includes(text)) {
              results.push(text);
            }
          }
        }
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });
    setTimeout(() => {
      observer.disconnect();
      resolve(results);
    }, 1500);
  });
});
```

## Anti-Crawling Measures

- Set a reasonable `userAgent` (emulate a real browser)
- Add random delays of 500–1500ms between keywords
- Avoid high-frequency requests within short time windows
- Use `headless: false` to bypass CAPTCHA if necessary
- Set `viewport: { width: 1280, height: 800 }` to emulate a normal resolution

## Output Format

```json
{
  "skincare": [
    "skincare routine",
    "skincare brand recommendations",
    "skincare ingredients",
    "skincare tips"
  ],
  "outfits": [
    "outfit blogger recommendations",
    "outfit formulas",
    "seasonal outfits",
    "outfit styles"
  ]
}
```

## SEO/GEO Applications

Collected keywords can be used for:

1. **Title optimization** — Incorporate high-frequency suggestion words into note titles
2. **Hashtag strategy** — Use long-tail keywords with high search volume as hashtags
3. **Content topic selection** — Determine content direction based on suggestion word popularity
4. **Competitive analysis** — Compare keyword performance across different brands/categories