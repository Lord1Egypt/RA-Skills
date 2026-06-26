# Performance Metrics Reference

Core Web Vitals and performance metrics with thresholds, extraction paths, and optimization strategies.

## Core Web Vitals (Google's Official Metrics)

### LCP - Largest Contentful Paint

**What it measures:** Time to render the largest visible content element (image, video, text block).

| Rating | Threshold |
|--------|-----------|
| ⚪ Good | < 2.5s |
| 🟡 Needs Improvement | 2.5s - 4.0s |
| 🔴 Poor | > 4.0s |

**Lighthouse audit ID:** `largest-contentful-paint`

**JSON extraction path:**
```javascript
lhr.audits['largest-contentful-paint'].numericValue // milliseconds
lhr.audits['largest-contentful-paint'].displayValue // formatted string
lhr.audits['largest-contentful-paint'].score // 0-1
```

**Common causes of poor LCP:**
- Slow server response times
- Render-blocking JavaScript/CSS
- Large unoptimized images
- Client-side rendering

**Optimization strategies:**
1. Optimize server configuration (caching, CDN)
2. Preload critical resources: `<link rel="preload" as="image" href="hero.jpg">`
3. Compress and resize images (WebP/AVIF format)
4. Remove unused CSS/JavaScript
5. Use SSR or SSG instead of CSR

---

### CLS - Cumulative Layout Shift

**What it measures:** Sum of unexpected layout shifts during page lifecycle.

| Rating | Threshold |
|--------|-----------|
| ⚪ Good | < 0.1 |
| 🟡 Needs Improvement | 0.1 - 0.25 |
| 🔴 Poor | > 0.25 |

**Lighthouse audit ID:** `cumulative-layout-shift`

**JSON extraction path:**
```javascript
lhr.audits['cumulative-layout-shift'].numericValue
lhr.audits['cumulative-layout-shift'].score
```

**Common causes of poor CLS:**
- Images without explicit dimensions
- Ads/embeds without reserved space
- Dynamically injected content
- Web fonts causing FOIT/FOUT
- Late-loading CSS

**Optimization strategies:**
1. Always include `width` and `height` on images/video
2. Reserve space for ads and embeds
3. Use `aspect-ratio` CSS property
4. Preload critical web fonts
5. Avoid inserting content above existing content

---

### INP - Interaction to Next Paint

**What it measures:** Responsiveness to user interactions throughout page lifecycle (replaced FID in 2024).

| Rating | Threshold |
|--------|-----------|
| ⚪ Good | < 200ms |
| 🟡 Needs Improvement | 200ms - 500ms |
| 🔴 Poor | > 500ms |

**Lighthouse audit ID:** `interaction-to-next-paint`

**JSON extraction path:**
```javascript
lhr.audits['interaction-to-next-paint'].numericValue
lhr.audits['interaction-to-next-paint'].score
```

**Common causes of poor INP:**
- Long tasks blocking main thread
- Heavy JavaScript execution
- Synchronous event handlers
- Layout thrashing during interactions

**Optimization strategies:**
1. Break up long tasks (>50ms)
2. Use web workers for heavy computations
3. Debounce/throttle input handlers
4. Use `requestIdleCallback` for non-critical work
5. Optimize CSS selectors

---

## Additional Performance Metrics

### FCP - First Contentful Paint

**What it measures:** Time from navigation to first content render (text, images, SVG, non-white canvas).

| Rating | Threshold |
|--------|-----------|
| ⚪ Good | < 1.8s |
| 🟡 Needs Improvement | 1.8s - 3.0s |
| 🔴 Poor | > 3.0s |

**Lighthouse audit ID:** `first-contentful-paint`

**JSON extraction path:**
```javascript
lhr.audits['first-contentful-paint'].numericValue
lhr.audits['first-contentful-paint'].score
```

---

### TBT - Total Blocking Time

**What it measures:** Sum of time periods where main thread was blocked >50ms between FCP and Time to Interactive.

| Rating | Threshold |
|--------|-----------|
| ⚪ Good | < 200ms |
| 🟡 Needs Improvement | 200ms - 600ms |
| 🔴 Poor | > 600ms |

**Lighthouse audit ID:** `total-blocking-time`

**JSON extraction path:**
```javascript
lhr.audits['total-blocking-time'].numericValue
lhr.audits['total-blocking-time'].score
```

**Common causes of poor TBT:**
- Excessive JavaScript execution
- Large script bundles
- Inefficient event listeners
- Third-party scripts

**Optimization strategies:**
1. Code splitting and lazy loading
2. Remove unused JavaScript
3. Defer non-critical scripts
4. Use `async` for third-party scripts
5. Minimize main thread work

---

### SI - Speed Index

**What it measures:** How quickly content is visually populated during page load.

| Rating | Threshold |
|--------|-----------|
| ⚪ Good | < 3.4s |
| 🟡 Needs Improvement | 3.4s - 5.8s |
| 🔴 Poor | > 5.8s |

**Lighthouse audit ID:** `speed-index`

**JSON extraction path:**
```javascript
lhr.audits['speed-index'].numericValue
lhr.audits['speed-index'].score
```

---

### TTI - Time to Interactive

**What it measures:** Time until page is fully interactive (responds to input within 50ms).

| Rating | Threshold |
|--------|-----------|
| ⚪ Good | < 3.8s |
| 🟡 Needs Improvement | 3.8s - 7.3s |
| 🔴 Poor | > 7.3s |

**Lighthouse audit ID:** `interactive`

**JSON extraction path:**
```javascript
lhr.audits['interactive'].numericValue
lhr.audits['interactive'].score
```

---

### TTFB - Time to First Byte

**What it measures:** Time from navigation to first byte of response from server.

| Rating | Threshold |
|--------|-----------|
| ⚪ Good | < 800ms |
| 🟡 Needs Improvement | 800ms - 1800ms |
| 🔴 Poor | > 1800ms |

**Lighthouse audit ID:** `server-response-time`

**JSON extraction path:**
```javascript
lhr.audits['server-response-time'].numericValue
lhr.audits['server-response-time'].score
```

**Optimization strategies:**
1. Use CDN for static assets
2. Enable server-side caching
3. Optimize database queries
4. Use HTTP/2 or HTTP/3
5. Reduce server processing time

---

## Metrics Extraction Script

Complete extraction from Lighthouse JSON:

```javascript
function extractAllMetrics(lhr) {
  const audits = lhr.audits;
  
  return {
    // Core Web Vitals
    LCP: {
      value: audits['largest-contentful-paint']?.numericValue,
      score: audits['largest-contentful-paint']?.score,
      displayValue: audits['largest-contentful-paint']?.displayValue,
      status: getMetricStatus('LCP', audits['largest-contentful-paint']?.numericValue),
    },
    CLS: {
      value: audits['cumulative-layout-shift']?.numericValue,
      score: audits['cumulative-layout-shift']?.score,
      displayValue: audits['cumulative-layout-shift']?.displayValue,
      status: getMetricStatus('CLS', audits['cumulative-layout-shift']?.numericValue),
    },
    INP: {
      value: audits['interaction-to-next-paint']?.numericValue,
      score: audits['interaction-to-next-paint']?.score,
      displayValue: audits['interaction-to-next-paint']?.displayValue,
      status: getMetricStatus('INP', audits['interaction-to-next-paint']?.numericValue),
    },
    // Additional metrics
    FCP: {
      value: audits['first-contentful-paint']?.numericValue,
      score: audits['first-contentful-paint']?.score,
      displayValue: audits['first-contentful-paint']?.displayValue,
      status: getMetricStatus('FCP', audits['first-contentful-paint']?.numericValue),
    },
    TBT: {
      value: audits['total-blocking-time']?.numericValue,
      score: audits['total-blocking-time']?.score,
      displayValue: audits['total-blocking-time']?.displayValue,
      status: getMetricStatus('TBT', audits['total-blocking-time']?.numericValue),
    },
    SI: {
      value: audits['speed-index']?.numericValue,
      score: audits['speed-index']?.score,
      displayValue: audits['speed-index']?.displayValue,
      status: getMetricStatus('SI', audits['speed-index']?.numericValue),
    },
    TTI: {
      value: audits['interactive']?.numericValue,
      score: audits['interactive']?.score,
      displayValue: audits['interactive']?.displayValue,
      status: getMetricStatus('TTI', audits['interactive']?.numericValue),
    },
    TTFB: {
      value: audits['server-response-time']?.numericValue,
      score: audits['server-response-time']?.score,
      displayValue: audits['server-response-time']?.displayValue,
      status: getMetricStatus('TTFB', audits['server-response-time']?.numericValue),
    },
  };
}

function getMetricStatus(metric, value) {
  if (value === undefined || value === null) return 'N/A';
  
  const thresholds = {
    LCP: { good: 2500, poor: 4000 },
    CLS: { good: 0.1, poor: 0.25 },
    INP: { good: 200, poor: 500 },
    FCP: { good: 1800, poor: 3000 },
    TBT: { good: 200, poor: 600 },
    SI: { good: 3400, poor: 5800 },
    TTI: { good: 3800, poor: 7300 },
    TTFB: { good: 800, poor: 1800 },
  };
  
  const t = thresholds[metric];
  if (!t) return '';
  
  if (value <= t.good) return '⚪ Good';
  if (value <= t.poor) return '🟡 Needs Improvement';
  return '🔴 Poor';
}
```

---

## Performance Score Calculation

Lighthouse Performance score is a weighted combination:

| Metric | Weight |
|--------|--------|
| LCP | 25% |
| FCP | 10% |
| TBT | 30% |
| CLS | 25% |
| SI | 10% |

**Note:** Weights may vary by Lighthouse version. Check `lhr.configSettings` for current weights.

---

## Mobile vs Desktop Thresholds

Mobile thresholds are more lenient due to hardware limitations:

| Metric | Desktop Good | Mobile Good |
|--------|--------------|-------------|
| LCP | < 2.5s | < 2.5s |
| FCP | < 1.5s | < 1.8s |
| TBT | < 150ms | < 200ms |
| SI | < 3.0s | < 3.4s |

---

## Quick Reference Table

| Metric | ID | Good | Poor | Unit |
|--------|-----|------|------|------|
| LCP | `largest-contentful-paint` | <2500 | >4000 | ms |
| CLS | `cumulative-layout-shift` | <0.1 | >0.25 | score |
| INP | `interaction-to-next-paint` | <200 | >500 | ms |
| FCP | `first-contentful-paint` | <1800 | >3000 | ms |
| TBT | `total-blocking-time` | <200 | >600 | ms |
| SI | `speed-index` | <3400 | >5800 | ms |
| TTI | `interactive` | <3800 | >7300 | ms |
| TTFB | `server-response-time` | <800 | >1800 | ms |
