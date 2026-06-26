# Shopify Theme Performance Optimization

Comprehensive guide to optimizing Shopify theme performance for speed, Core Web Vitals, and user experience.

## Performance Goals

**Target Metrics (Lighthouse Mobile):**
- Performance Score: **90+**
- First Contentful Paint (FCP): **< 1.8s**
- Largest Contentful Paint (LCP): **< 2.5s**
- Total Blocking Time (TBT): **< 200ms**
- Cumulative Layout Shift (CLS): **< 0.1**
- Speed Index: **< 3.4s**

**Why It Matters:**
- **SEO:** Google uses Core Web Vitals as ranking factor
- **Conversions:** 1s delay = 7% reduction in conversions
- **UX:** Fast sites feel more trustworthy and professional

---

## 1. Image Optimization

Images are typically 50-70% of page weight. Optimize aggressively.

### Lazy Loading

Load images only when they enter the viewport:

```liquid
{{ product.featured_image | image_url: width: 800 | image_tag: loading: 'lazy' }}
```

**Best Practices:**
- Lazy load all images below the fold
- **Don't** lazy load hero images (delays LCP)
- Set explicit `width` and `height` to prevent CLS

### Responsive Images

Serve appropriately sized images for different viewports:

```liquid
<img
  src="{{ product.featured_image | image_url: width: 800 }}"
  srcset="
    {{ product.featured_image | image_url: width: 400 }} 400w,
    {{ product.featured_image | image_url: width: 800 }} 800w,
    {{ product.featured_image | image_url: width: 1200 }} 1200w,
    {{ product.featured_image | image_url: width: 1600 }} 1600w
  "
  sizes="(min-width: 1024px) 50vw, 100vw"
  alt="{{ product.title | escape }}"
  loading="lazy"
  width="800"
  height="800"
>
```

**Key Attributes:**
- `srcset` — Available image sizes
- `sizes` — Tell browser which size to use based on viewport
- `width`/`height` — Prevent layout shift (reserve space before image loads)

### Image Format

Shopify automatically serves WebP when supported. Use the `image_url` filter for automatic conversion:

```liquid
{{ product.featured_image | image_url: width: 800, format: 'pjpg' }}
```

**Format Options:**
- `pjpg` — Progressive JPEG (default, good balance)
- `jpg` — Standard JPEG
- WebP served automatically to supporting browsers

### Image Compression

Compress images before uploading:
- **Photos:** 75-85% JPEG quality
- **Graphics:** PNG with optimization
- **Large images:** Max 2000px width (Shopify resizes on-demand)

**Tools:**
- ImageOptim (Mac)
- TinyPNG (web)
- Squoosh (web)

---

## 2. Critical CSS

Inline critical CSS (above-the-fold styles) to eliminate render-blocking requests.

### Extract Critical CSS

Use tools to identify critical styles:
- **Critical:** https://github.com/addyosmani/critical
- **Penthouse:** https://github.com/pocketjoso/penthouse

### Inline Critical CSS

Add critical styles to `<head>` in `layout/theme.liquid`:

```liquid
<head>
  <style>
    /* Critical CSS (above-the-fold only) */
    body {
      font-family: {{ settings.font_body.family }};
      margin: 0;
      padding: 0;
    }
    .header {
      background: {{ settings.color_header_bg }};
      padding: 1rem;
    }
    /* ... more critical styles */
  </style>

  {%- # Defer non-critical CSS -%}
  <link rel="preload" href="{{ 'theme.css' | asset_url }}" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="{{ 'theme.css' | asset_url }}"></noscript>
</head>
```

**Benefits:**
- Eliminates render-blocking CSS
- Faster First Contentful Paint
- Perceived performance improvement

**Tradeoffs:**
- Larger HTML size (minor)
- Requires maintenance (extract critical CSS on major changes)

---

## 3. JavaScript Optimization

Minimize JavaScript usage. Native browser features > heavy frameworks.

### Defer Non-Critical JavaScript

Load scripts after page render:

```liquid
<script src="{{ 'theme.js' | asset_url }}" defer></script>
```

**`defer` vs `async`:**
- `defer` — Download in parallel, execute after HTML parsing (maintains order)
- `async` — Download and execute ASAP (can block rendering)

Use `defer` for scripts that depend on DOM or other scripts.

### Remove Unused JavaScript

Audit and remove:
- Unused libraries (jQuery if possible)
- Polyfills for modern browsers
- Analytics scripts not in use

### Code Splitting

Load JS only when needed:

```liquid
{%- # Only load cart JS on cart page -%}
{% if template == 'cart' %}
  <script src="{{ 'cart.js' | asset_url }}" defer></script>
{% endif %}
```

### Minification

Minify all JavaScript files:

```bash
# Use Terser or similar
npx terser assets/theme.js -o assets/theme.min.js -c -m
```

Shopify CLI auto-minifies during `theme push` (if configured).

---

## 4. Font Loading

Web fonts can block rendering. Optimize loading strategy.

### Font Display

Use `font-display: swap` to show fallback font while custom font loads:

```css
@font-face {
  font-family: 'CustomFont';
  src: url('custom-font.woff2') format('woff2');
  font-display: swap; /* Show fallback immediately */
}
```

### Preload Critical Fonts

Hint browser to load fonts early:

```liquid
<link rel="preload" href="{{ settings.font_heading | font_url }}" as="font" type="font/woff2" crossorigin>
```

**Best Practices:**
- Preload only 1-2 critical fonts (heading, body)
- Use WOFF2 format (best compression)
- Include `crossorigin` attribute (required for fonts)

### System Font Stack

Consider using system fonts for body text (instant, no download):

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}
```

**Benefits:**
- Zero network request
- Familiar to users
- Excellent performance

**Tradeoffs:**
- Less brand uniqueness
- Varies across platforms

---

## 5. Resource Hints

Help the browser prioritize and fetch resources efficiently.

### DNS Prefetch

Resolve DNS early for third-party domains:

```liquid
<link rel="dns-prefetch" href="https://cdn.shopify.com">
<link rel="dns-prefetch" href="https://fonts.googleapis.com">
```

### Preconnect

Establish early connection to critical origins:

```liquid
<link rel="preconnect" href="https://cdn.shopify.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

**Use for:**
- Shopify CDN
- Font providers
- Analytics scripts

### Prefetch

Load resources for next page navigation:

```liquid
{%- # On homepage, prefetch collection page assets -%}
<link rel="prefetch" href="{{ 'collection.css' | asset_url }}">
```

**Use sparingly** — only for very likely next actions.

---

## 6. Liquid Template Optimization

Optimize Liquid code for faster rendering.

### Limit Loop Iterations

```liquid
{%- # Bad: Renders all 100 products -%}
{% for product in collection.products %}
  {%- # ... -%}
{% endfor %}

{%- # Good: Limit to 12 products -%}
{% for product in collection.products limit: 12 %}
  {%- # ... -%}
{% endfor %}
```

### Strip Whitespace

Use `{%- -%}` to remove extra whitespace:

```liquid
{%- # Strips leading/trailing whitespace -%}
{%- if product.available -%}
  <button>Add to Cart</button>
{%- endif -%}
```

**Impact:** Reduces HTML size by 10-30%.

### Use `liquid` Tag

For logic-heavy blocks, use `liquid` tag to reduce delimiter overhead:

```liquid
{% liquid
  assign sale = false
  if product.compare_at_price > product.price
    assign sale = true
  endif
%}
```

### Avoid Nested Snippets

Deep snippet nesting increases render time. Flatten where possible:

```liquid
{%- # Bad: Deep nesting -%}
{% render 'outer' %}
  {%- # outer.liquid renders 'middle' -%}
  {%- # middle.liquid renders 'inner' -%}

{%- # Good: Single render -%}
{% render 'product-card', product: product %}
```

---

## 7. Third-Party Scripts

Third-party scripts (analytics, chat widgets, etc.) often harm performance.

### Audit Scripts

List all third-party scripts:
- Google Analytics
- Facebook Pixel
- Chat widgets (Intercom, Drift)
- Reviews apps (Yotpo, Judge.me)

**Remove unused scripts.**

### Load Asynchronously

Never load third-party scripts synchronously:

```liquid
{%- # Bad: Blocks rendering -%}
<script src="https://cdn.example.com/widget.js"></script>

{%- # Good: Async load -%}
<script src="https://cdn.example.com/widget.js" async></script>
```

### Delay Non-Essential Scripts

Load chat widgets and non-critical scripts after page load:

```javascript
window.addEventListener('load', function() {
  // Load chat widget after page is fully loaded
  const script = document.createElement('script');
  script.src = 'https://cdn.example.com/chat.js';
  script.async = true;
  document.body.appendChild(script);
});
```

### Self-Host When Possible

Third-party CDNs add DNS lookup + connection time. Self-host small scripts:

```bash
# Download script
curl -o assets/analytics.js https://cdn.example.com/analytics.js

# Reference in theme
<script src="{{ 'analytics.js' | asset_url }}" async></script>
```

---

## 8. Caching Strategy

Leverage browser caching for static assets.

### Asset Versioning

Shopify automatically versions assets (adds hash to URL):

```
https://cdn.shopify.com/s/files/1/0123/4567/8901/t/2/assets/theme.css?v=123456789
```

**Benefit:** Safe to cache forever (URL changes when file changes).

### Cache Headers

Shopify sets optimal cache headers for assets:
- `Cache-Control: public, max-age=31536000` (1 year)
- Assets served from global CDN (fast worldwide)

**You don't need to configure caching** — Shopify handles it.

---

## 9. Mobile Optimization

Mobile accounts for 70%+ of e-commerce traffic. Optimize mobile-first.

### Responsive Design

Use mobile-first CSS:

```css
/* Base styles for mobile */
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

/* Tablet and up */
@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Touch Targets

Ensure tap targets are at least 44×44px:

```css
button, a {
  min-height: 44px;
  min-width: 44px;
  padding: 0.75rem 1.5rem;
}
```

### Test on Real Devices

Simulators don't replicate:
- Network throttling
- CPU constraints
- Touch interactions

**Test on:**
- iPhone (Safari)
- Android (Chrome)
- Slow 3G network (Chrome DevTools)

---

## 10. Monitoring & Testing

Measure performance continuously.

### Lighthouse

Run Lighthouse audits (Chrome DevTools):

```bash
# Command line
npx lighthouse https://your-store.myshopify.com --view
```

**Focus on:**
- Performance score
- Core Web Vitals (LCP, FID, CLS)
- Opportunities section (biggest wins)

### WebPageTest

More detailed analysis: https://www.webpagetest.org

**Settings:**
- Location: Choose customer location
- Device: Mobile (Moto G4)
- Connection: 3G or 4G

### Real User Monitoring (RUM)

Use Shopify Analytics or third-party tools:
- Google Analytics (Real User Monitoring)
- SpeedCurve
- New Relic

**Benefits:**
- Real customer data (not lab tests)
- Geographic breakdown
- Device/browser trends

### Continuous Monitoring

Set up automated performance checks:
- Lighthouse CI (GitHub Actions)
- Weekly audits with alerts
- Performance budgets (fail build if score drops)

---

## Performance Checklist

Before launching:
- [ ] Images lazy loaded (except hero)
- [ ] Responsive images with `srcset`
- [ ] Critical CSS inlined
- [ ] Non-critical CSS deferred
- [ ] JavaScript deferred or async
- [ ] Fonts use `font-display: swap`
- [ ] Resource hints for critical origins
- [ ] Third-party scripts loaded async
- [ ] Lighthouse Performance Score 90+
- [ ] LCP < 2.5s on mobile
- [ ] CLS < 0.1
- [ ] Tested on real mobile devices
- [ ] Tested on slow 3G network

---

## Common Performance Killers

| Issue | Impact | Fix |
|-------|--------|-----|
| Render-blocking CSS | Delays FCP | Inline critical CSS, defer rest |
| Synchronous JS in `<head>` | Blocks parsing | Move to `<body>` or use `defer` |
| Massive hero image | Delays LCP | Compress, use responsive images |
| Unused JavaScript | Increases bundle size | Code split, tree shake |
| Too many fonts | Delays text render | Use system fonts or limit to 2 fonts |
| Third-party scripts | Blocks rendering | Load async, delay non-critical |
| No lazy loading | Loads all images upfront | Lazy load below-fold images |
| No image dimensions | Causes CLS | Set explicit `width`/`height` |
| Unoptimized images | Large file sizes | Compress, use WebP |
| Deep Liquid nesting | Slow server render | Flatten snippets, limit loops |

---

**Last Updated:** 2026-03-13
