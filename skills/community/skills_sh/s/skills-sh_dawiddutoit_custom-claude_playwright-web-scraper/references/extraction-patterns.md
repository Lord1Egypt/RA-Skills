# Data Extraction JavaScript Patterns

Common patterns for extracting data from web pages using `browser_evaluate`.

## Basic Patterns

### Extract Text Content

```javascript
// Single element
document.querySelector('.product-title')?.textContent?.trim()

// Multiple elements
Array.from(document.querySelectorAll('.product-item'))
  .map(el => el.textContent.trim())

// With null safety
document.querySelector('.price')?.textContent?.trim() || 'N/A'
```

### Extract Attributes

```javascript
// Single attribute
document.querySelector('img.product')?.getAttribute('src')

// Multiple attributes
document.querySelector('a.product-link')
  ? {
      href: document.querySelector('a.product-link').getAttribute('href'),
      title: document.querySelector('a.product-link').getAttribute('title')
    }
  : null

// Data attributes
document.querySelector('.product')?.dataset.productId
```

### Extract Structured Data

```javascript
// Product listing
Array.from(document.querySelectorAll('.product-card')).map(card => ({
  title: card.querySelector('.title')?.textContent?.trim(),
  price: card.querySelector('.price')?.textContent?.trim(),
  rating: card.querySelector('.rating')?.textContent?.trim(),
  url: card.querySelector('a')?.getAttribute('href'),
  image: card.querySelector('img')?.getAttribute('src')
}))
```

## Advanced Patterns

### Extract with Fallbacks

```javascript
// Try multiple selectors
function extractPrice(el) {
  return el.querySelector('.sale-price')?.textContent?.trim() ||
         el.querySelector('.price')?.textContent?.trim() ||
         el.querySelector('[data-price]')?.dataset.price ||
         'N/A';
}
```

### Clean Extracted Data

```javascript
// Remove extra whitespace and normalize
function cleanText(text) {
  return text?.replace(/\s+/g, ' ').trim() || '';
}

// Extract numeric values
function extractNumber(text) {
  const match = text?.match(/[\d,]+\.?\d*/);
  return match ? parseFloat(match[0].replace(/,/g, '')) : null;
}

// Usage
Array.from(document.querySelectorAll('.product')).map(el => ({
  title: cleanText(el.querySelector('.title')?.textContent),
  price: extractNumber(el.querySelector('.price')?.textContent)
}))
```

### Extract from Shadow DOM

```javascript
// Access shadow DOM
const host = document.querySelector('#shadow-host');
const shadowRoot = host?.shadowRoot;
const data = shadowRoot?.querySelector('.data')?.textContent;
```

### Extract JSON-LD Structured Data

```javascript
// Extract JSON-LD schema
const scripts = document.querySelectorAll('script[type="application/ld+json"]');
const structuredData = Array.from(scripts).map(script => {
  try {
    return JSON.parse(script.textContent);
  } catch (e) {
    return null;
  }
}).filter(Boolean);
```

## Pagination Patterns

### Detect Next Page

```javascript
// Check for next button
const nextButton = document.querySelector('.pagination .next:not(.disabled)');
const hasNextPage = nextButton !== null;

// Check for page numbers
const currentPage = parseInt(document.querySelector('.pagination .active')?.textContent || '1');
const lastPage = parseInt(document.querySelector('.pagination .page:last-child')?.textContent || '1');
const hasMorePages = currentPage < lastPage;
```

### Extract Pagination URLs

```javascript
// All page URLs
Array.from(document.querySelectorAll('.pagination a.page'))
  .map(a => a.getAttribute('href'))
  .filter(Boolean)

// Next page URL
document.querySelector('.pagination .next')?.getAttribute('href')
```

## Table Extraction

### Extract Table Rows

```javascript
// Simple table
Array.from(document.querySelectorAll('table tbody tr')).map(row => {
  const cells = Array.from(row.querySelectorAll('td'));
  return cells.map(cell => cell.textContent.trim());
})

// Table with headers
const headers = Array.from(document.querySelectorAll('table th'))
  .map(th => th.textContent.trim());

const rows = Array.from(document.querySelectorAll('table tbody tr')).map(row => {
  const cells = Array.from(row.querySelectorAll('td'));
  const obj = {};
  headers.forEach((header, i) => {
    obj[header] = cells[i]?.textContent?.trim();
  });
  return obj;
});
```

## Error Handling Patterns

### Safe Extraction

```javascript
// Wrap in try-catch for safety
try {
  return Array.from(document.querySelectorAll('.item')).map(el => ({
    title: el.querySelector('.title')?.textContent?.trim(),
    price: el.querySelector('.price')?.textContent?.trim()
  }));
} catch (e) {
  console.error('Extraction failed:', e);
  return [];
}
```

### Validate Extracted Data

```javascript
// Filter out incomplete records
const products = Array.from(document.querySelectorAll('.product'))
  .map(el => ({
    title: el.querySelector('.title')?.textContent?.trim(),
    price: el.querySelector('.price')?.textContent?.trim(),
    url: el.querySelector('a')?.getAttribute('href')
  }))
  .filter(p => p.title && p.price && p.url); // Only keep complete records
```

## Wait for Content Patterns

### Wait for Elements

Before extracting, ensure elements are loaded:

```javascript
// Check if content is loaded
const contentLoaded = document.querySelectorAll('.product').length > 0;

// Check for specific text
const textPresent = document.body.textContent.includes('Expected Text');

// Check for loading indicators
const isLoading = document.querySelector('.spinner, .loading') !== null;
```

Use with `browser_wait_for`:

```javascript
// In workflow
await browser_wait_for({ text: 'Products loaded' });
// Then extract
```

## Common Selectors Reference

| Element | CSS Selector Examples |
|---------|----------------------|
| By class | `.product`, `.item-title` |
| By ID | `#main-content`, `#product-123` |
| By attribute | `[data-product-id]`, `[href*="product"]` |
| By tag | `article`, `section`, `table` |
| Nested | `.product .title`, `.card > .header` |
| Multiple | `.price, .sale-price` |
| Not | `.item:not(.disabled)` |
| Contains text | (use textContent filter after selection) |

## Performance Considerations

### Efficient Selectors

```javascript
// ❌ Slow - multiple queries
const titles = document.querySelectorAll('.product .title');
const prices = document.querySelectorAll('.product .price');

// ✅ Fast - single query, then map
const products = Array.from(document.querySelectorAll('.product')).map(el => ({
  title: el.querySelector('.title')?.textContent?.trim(),
  price: el.querySelector('.price')?.textContent?.trim()
}));
```

### Limit Result Size

```javascript
// Limit results to avoid memory issues
const MAX_ITEMS = 1000;
const items = Array.from(document.querySelectorAll('.item'))
  .slice(0, MAX_ITEMS)
  .map(extractData);
```

## Debugging Extraction

### Log Extraction Results

```javascript
const products = Array.from(document.querySelectorAll('.product')).map(el => {
  const data = {
    title: el.querySelector('.title')?.textContent?.trim(),
    price: el.querySelector('.price')?.textContent?.trim()
  };
  console.log('Extracted:', data);
  return data;
});

console.log(`Total extracted: ${products.length}`);
return products;
```

### Test Selectors in Console

Before using in script, test selectors in browser DevTools console:

```javascript
// Test selector
document.querySelectorAll('.product').length
// Should return expected count

// Test extraction
document.querySelector('.product .title')?.textContent?.trim()
// Should return expected text
```
