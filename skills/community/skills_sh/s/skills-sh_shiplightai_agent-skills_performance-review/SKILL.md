---
name: performance-review
description: "Performance review and testing: evaluate Core Web Vitals, page load times, bundle sizes, runtime performance, resource optimization, and rendering efficiency with browser-based measurement and benchmarking."
---

# Performance Review

Measure and evaluate your application's performance against Google's Core Web Vitals thresholds and industry benchmarks. This review catches performance issues that are invisible during development but impact real users — bundle bloat, layout shifts, slow interactions, unoptimized images, and render-blocking resources.

## When to use

Use `/performance-review` when:
- Before launching or after major feature additions
- Page load feels slow but you're not sure why
- Preparing for high-traffic events
- After adding new dependencies or third-party scripts
- SEO rankings depend on performance scores
- Users report slowness or abandonment

## Standards Referenced

- **Google Core Web Vitals** — LCP, INP, CLS (2024 thresholds)
- **Google Lighthouse** — Performance scoring methodology
- **HTTP Archive** — Web performance benchmarks (median, p75, p90)
- **Web.dev Performance Guidelines** — Best practices
- **RAIL Model** — Response, Animation, Idle, Load budgets

## Phase Overview

```
Phase 1: EDUCATE   → Performance impact on business and what we measure
Phase 2: SCOPE     → Identify key pages, performance budget, baseline
Phase 3: ANALYZE   → Browser-based performance measurement
Phase 4: REPORT    → Findings with metrics, scores, and comparisons
Phase 5: REMEDIATE → Fix guidance + YAML regression tests
```

---

## Phase 1: Educate

> **Why this matters:** A 1-second delay in page load reduces conversions by 7% (Akamai). Google uses Core Web Vitals as ranking signals since 2021. 53% of mobile visitors leave a page that takes >3 seconds to load (Google). Amazon found every 100ms of latency costs 1% of sales. Performance is a feature — and its absence is a bug.

This review measures real performance in a browser, not just static analysis. We capture actual load times, rendering behavior, and interaction responsiveness.

---

## Phase 2: Scope

### Gather context

1. **Auto-detect from codebase:**
   - Build system (Webpack, Vite, Next.js, etc.)
   - Bundle analysis setup (if any)
   - Image optimization pipeline (sharp, next/image, etc.)
   - Font loading strategy
   - Code splitting configuration
   - Service worker / caching strategy
   - CDN configuration

2. **Ask the user** (one at a time):
   - **Target URL**: Where is the app running? (production preferred for realistic measurements)
   - **Key pages**: Which pages matter most for performance? (recommend: landing page, main feature page, data-heavy page)
   - **Performance budget**: Any existing targets? (default: Core Web Vitals "Good" thresholds)
   - **Known concerns**: Any pages that feel slow? (optional)

3. **Define measurement plan:**
   - Pages to test (3-5 key pages)
   - Conditions: desktop and mobile simulated (Moto G4 / Slow 4G)
   - Metrics: Core Web Vitals + supplementary metrics
   - Baseline: first run establishes baseline for comparison

---

## Phase 3: Analyze

Open a browser session with `new_session` using `record_evidence: true`. For each page in scope, run all measurement categories.

### Category A: Core Web Vitals (CWV)

| Check ID | Metric | Good | Needs Improvement | Poor | Method |
|----------|--------|------|-------------------|------|--------|
| CWV-01 | **LCP** (Largest Contentful Paint) | ≤2.5s | 2.5-4.0s | >4.0s | `PerformanceObserver` for LCP entries |
| CWV-02 | **INP** (Interaction to Next Paint) | ≤200ms | 200-500ms | >500ms | Click key interactive elements, measure delay |
| CWV-03 | **CLS** (Cumulative Layout Shift) | ≤0.1 | 0.1-0.25 | >0.25 | `PerformanceObserver` for layout-shift entries |

**Browser validation:** Navigate to each page and capture metrics via JavaScript:

```javascript
// LCP
new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const lcp = entries[entries.length - 1];
  console.log('LCP:', lcp.startTime);
}).observe({ type: 'largest-contentful-paint', buffered: true });

// CLS
let clsValue = 0;
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (!entry.hadRecentInput) clsValue += entry.value;
  }
  console.log('CLS:', clsValue);
}).observe({ type: 'layout-shift', buffered: true });
```

### Category B: Page Load Performance (LOAD)

| Check ID | Check | Threshold | Method |
|----------|-------|-----------|--------|
| LOAD-01 | Time to First Byte (TTFB) | ≤800ms | `performance.timing.responseStart - navigationStart` |
| LOAD-02 | First Contentful Paint (FCP) | ≤1.8s | `performance.getEntriesByName('first-contentful-paint')` |
| LOAD-03 | DOM Content Loaded | ≤2.0s | `performance.timing.domContentLoadedEventEnd` |
| LOAD-04 | Total page weight | ≤3MB (mobile) / ≤5MB (desktop) | `performance.getEntriesByType('resource')` sum |
| LOAD-05 | Number of HTTP requests | ≤50 | Count resource entries |
| LOAD-06 | Time to Interactive (TTI) | ≤3.8s | Long task analysis |
| LOAD-07 | Total Blocking Time (TBT) | ≤200ms | Sum of long tasks (>50ms portions) |
| LOAD-08 | Speed Index | ≤3.4s | Visual progress analysis |

**Browser validation:** Use Performance API and `performance.getEntries()` to gather all metrics.

### Category C: Resource Optimization (RES)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| RES-01 | Images use modern formats (WebP/AVIF) | Web.dev | Check image URLs and Content-Type |
| RES-02 | Images are appropriately sized (not oversized) | Web.dev | Compare display size vs natural size |
| RES-03 | Images use lazy loading (below-fold) | Web.dev | Check `loading="lazy"` on below-fold images |
| RES-04 | Images have explicit dimensions (width/height) | CLS prevention | Check for width/height attributes |
| RES-05 | CSS is not render-blocking (or is critical-inlined) | Web.dev | Check CSS loading strategy |
| RES-06 | JavaScript is deferred or async | Web.dev | Check script loading attributes |
| RES-07 | Fonts use font-display: swap or optional | Web.dev | Check @font-face declarations |
| RES-08 | Fonts are preloaded | Web.dev | Check for `<link rel="preload" as="font">` |
| RES-09 | Gzip/Brotli compression enabled | HTTP best practice | Check Content-Encoding headers |
| RES-10 | HTTP/2 or HTTP/3 in use | HTTP best practice | Check protocol via Performance API |
| RES-11 | Effective caching headers | HTTP best practice | Check Cache-Control on static assets |
| RES-12 | No unused CSS/JS loaded | Bundle efficiency | Check coverage via Page.startJSCoverage/startCSSCoverage |

**Browser validation:** Use JavaScript to inspect all loaded resources, their types, sizes, and loading attributes. Use `performance.getEntriesByType('resource')` for detailed resource metrics.

### Category D: Bundle Analysis (BUN)

| Check ID | Check | Threshold | Method |
|----------|-------|-----------|--------|
| BUN-01 | Main JS bundle size | ≤250KB gzipped | Check transfer size of main bundle |
| BUN-02 | Total JS size | ≤500KB gzipped | Sum all JS transfer sizes |
| BUN-03 | Total CSS size | ≤100KB gzipped | Sum all CSS transfer sizes |
| BUN-04 | Code splitting implemented | Best practice | Check for multiple JS chunks |
| BUN-05 | No duplicate dependencies | Bundle efficiency | Analyze chunk contents for duplicates |
| BUN-06 | Tree shaking effective | Bundle efficiency | Check for known large unused exports |
| BUN-07 | Source maps not exposed in production | Security/Performance | Check for .map files accessibility |
| BUN-08 | Third-party JS budget | ≤30% of total JS | Calculate third-party vs first-party ratio |

**Browser validation:** Use Performance API to measure transfer sizes. Check for source map URLs. Analyze script domain origins.

### Category E: Runtime Performance (RUN)

| Check ID | Check | Threshold | Method |
|----------|-------|-----------|--------|
| RUN-01 | No long tasks during interaction | >50ms = long task | Use `PerformanceObserver` for long tasks |
| RUN-02 | Scroll performance is smooth | 60fps | Scroll page, measure frame drops |
| RUN-03 | Animation performance | 60fps | Trigger animations, measure jank |
| RUN-04 | Memory usage is stable (no leaks) | No growth pattern | Measure `performance.memory` over time |
| RUN-05 | No excessive DOM nodes | ≤1500 nodes | Count `document.querySelectorAll('*').length` |
| RUN-06 | No layout thrashing | 0 forced reflows | Monitor forced style recalculations |
| RUN-07 | Efficient event listeners | No excessive listeners | Check for scroll/resize listeners without throttle |

**Browser validation:** Navigate and interact with the app while measuring performance metrics via JavaScript.

---

## Phase 4: Report

Generate a structured report saved to `shiplight/reports/performance-review-{date}.md`:

```markdown
# Performance Review Report
**Date:** {date}
**URL:** {url}
**Pages tested:** {list}
**Conditions:** Desktop + Mobile (simulated Moto G4 / Slow 4G)

## Overall Score: {X}/10 | Confidence: {X}%

## Core Web Vitals Summary
| Metric | Desktop | Mobile | Status |
|--------|---------|--------|--------|
| LCP | 1.8s | 3.2s | ⚠️ Mobile needs work |
| INP | 95ms | 180ms | ✅ Good |
| CLS | 0.05 | 0.15 | ⚠️ Mobile needs work |

## Score Breakdown
| Category | Score | Findings |
|----------|-------|----------|
| Core Web Vitals (CWV) | 6/10 | 1 high, 1 medium |
| Page Load (LOAD) | 7/10 | 1 high |
| Resources (RES) | 5/10 | 2 high, 2 medium |
| Bundle (BUN) | 6/10 | 1 high, 1 medium |
| Runtime (RUN) | 8/10 | 1 medium |

## Resource Waterfall
(Top 10 slowest resources with load times)

## Bundle Breakdown
| Category | Size (gzipped) | Budget | Status |
|----------|---------------|--------|--------|
| First-party JS | 180KB | 250KB | ✅ |
| Third-party JS | 220KB | 150KB | ❌ Over budget |
| CSS | 45KB | 100KB | ✅ |
| Images | 1.2MB | 1.5MB | ✅ |
| Fonts | 85KB | 100KB | ✅ |

## Findings
(structured findings with metrics and evidence)
```

### Confidence Scoring
- **90-100%**: Measured in browser with specific values (e.g., LCP: 3.2s)
- **70-89%**: Derived from resource analysis (e.g., unoptimized images detected)
- **50-69%**: Code-level pattern (e.g., no lazy loading attributes found)
- **Below 50%**: Don't report

---

## Phase 5: Remediate

### 1. Fix guidance (example)
```markdown
#### RES-01: Images not using modern formats
**Impact:** ~40% larger images than necessary, adds ~500KB to page weight
**Current:** 8 PNG images totaling 1.2MB
**Fix:** Convert to WebP with fallback:
- Use `<picture>` with WebP source and PNG fallback
- Or use Next.js `<Image>` / `sharp` for automatic format negotiation
- Expected savings: ~480KB (40% reduction)
**Priority files:**
- /images/hero.png (320KB → ~190KB as WebP)
- /images/features.png (280KB → ~165KB as WebP)
```

### 2. YAML regression test
```yaml
- name: cwv-01-lcp-under-threshold
  description: Verify Largest Contentful Paint is under 2.5 seconds
  severity: high
  standard: Core-Web-Vitals-LCP
  steps:
    - description: Set up an LCP observer before navigation
      js: |
        // Set up LCP observer before navigation
        await page.evaluateOnNewDocument(() => {
          window.__lcp = 0;
          new PerformanceObserver((list) => {
            const entries = list.getEntries();
            window.__lcp = entries[entries.length - 1].startTime;
          }).observe({ type: 'largest-contentful-paint', buffered: true });
        });
    - URL: /
    - WAIT_UNTIL: Page has fully loaded including all images and content
      timeout_seconds: 30
    - description: Assert Largest Contentful Paint is under 2.5s
      js: |
        const lcp = await page.evaluate(() => window.__lcp);
        if (lcp > 2500) {
          throw new Error(`LCP is ${lcp}ms, exceeds 2500ms threshold`);
        }
        console.log(`LCP: ${lcp}ms (threshold: 2500ms)`);
    - VERIFY: Page loaded with Largest Contentful Paint under 2.5 seconds
```

Save all YAML tests to `shiplight/tests/performance-review.test.yaml`.

---

## Depth Levels

- **`--quick`**: Core Web Vitals only on the main page. ~2 minutes.
- **default**: All categories on key pages, desktop + mobile. ~8-12 minutes.
- **`--thorough`**: All categories + extended pages + multiple runs for statistical confidence + runtime profiling. ~20-30 minutes.

## Tips

- Measure on production (or production-like build) — dev mode performance is misleading
- Run multiple times — performance measurements vary; look for patterns, not single data points
- Mobile simulation reveals issues that desktop hides — always test both
- Use `performance.getEntries()` — it's the richest source of performance data in the browser
- Focus on Core Web Vitals first — they're the metrics Google uses for ranking
- Close session with `close_session` and use `generate_html_report` for evidence
