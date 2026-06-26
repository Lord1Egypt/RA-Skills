# Audit Checklist

Complete checklists for Accessibility, Best Practices, and SEO audits with Lighthouse audit IDs and fix examples.

---

## Accessibility Audit Checklist

### Critical Issues (WCAG A/AA)

| Audit ID | Issue | WCAG Level | Fix Example |
|----------|-------|------------|-------------|
| `color-contrast` | Background/foreground contrast <4.5:1 | AA | `color: #333; background: #fff;` |
| `image-alt` | Images missing alt text | A | `<img src="logo.png" alt="Company Logo">` |
| `label` | Form inputs without labels | A | `<label for="email">Email</label><input id="email">` |
| `link-name` | Links without accessible names | A | `<a href="/home">Go to Homepage</a>` |
| `button-name` | Buttons without accessible names | A | `<button aria-label="Close modal">×</button>` |
| `html-has-lang` | HTML element missing lang attribute | A | `<html lang="en">` |
| `valid-lang` | Invalid lang attribute value | A | `<html lang="en-US">` |
| `heading-order` | Skipped heading levels | A | Use h1→h2→h3 sequentially |
| `document-title` | Document missing title | A | `<title>Page Title</title>` |
| `meta-refresh` | Auto-redirecting page | A | Remove `<meta http-equiv="refresh">` |

### Additional Accessibility Checks

| Audit ID | Issue | Priority |
|----------|-------|----------|
| `aria-allowed-attr` | Invalid ARIA attributes | High |
| `aria-hidden-body` | aria-hidden on body | High |
| `aria-required-attr` | Missing required ARIA attributes | High |
| `aria-roles` | Invalid ARIA role values | High |
| `aria-valid-attr` | Malformed ARIA attributes | High |
| `aria-valid-attr-value` | Invalid ARIA attribute values | High |
| `autocomplete-valid` | Invalid autocomplete values | Medium |
| `axis` | Invalid table axis attribute | Low |
| `blink` | Blinking content detected | Medium |
| `bypass` | No skip links for keyboard users | AA |
| `definition-list` | Definition list markup errors | Low |
| `dlitem` | Definition list item outside list | Low |
| `duplicate-id` | Duplicate ID attributes | Medium |
| `duplicate-id-active` | Duplicate IDs in interactive elements | High |
| `frame-title` | iframes missing title | A |
| `input-image-alt` | Input type="image" missing alt | A |
| `landmark-one-main` | Multiple or missing main landmarks | AA |
| `layout-table` | Layout tables not marked as such | Low |
| `list` | List markup errors | Low |
| `listitem` | List items outside lists | Low |
| `marquee` | Marquee content detected | Low |
| `object-alt` | Object elements missing alt | A |
| `region` | Content outside landmarks | AA |
| `scope-attr` | Invalid scope attributes | Low |
| `select-name` | Select elements without labels | A |
| `skip-link` | Skip links not functional | AA |
| `tabindex` | tabindex > 0 | AA |
| `td-headers-attr` | Table cell headers attribute errors | Low |
| `th-has-data-cells` | Data tables missing headers | A |
| `valid-lang` | Invalid lang values | A |
| `video-caption` | Videos missing captions | A |

### Accessibility Fix Examples

**1. Fix Color Contrast:**
```css
/* Before: Contrast ratio 3.2:1 */
.text { color: #999; background: #fff; }

/* After: Contrast ratio 7.5:1 */
.text { color: #333; background: #fff; }
```

**2. Add Image Alt Text:**
```html
<!-- Before -->
<img src="product.jpg">

<!-- After -->
<img src="product.jpg" alt="Blue wireless headphones on white background">
```

**3. Add Form Labels:**
```html
<!-- Before -->
<input type="email" placeholder="Enter email">

<!-- After -->
<label for="email">Email Address</label>
<input type="email" id="email" name="email" required>
```

**4. Fix Heading Order:**
```html
<!-- Before: Skips h2 -->
<h1>Main Title</h1>
<h3>Subsection</h3>

<!-- After: Sequential -->
<h1>Main Title</h1>
<h2>Section Title</h2>
<h3>Subsection</h3>
```

---

## Best Practices Audit Checklist

### Trust & Safety

| Audit ID | Issue | Severity | Fix |
|----------|-------|----------|-----|
| `is-on-https` | Page not using HTTPS | Critical | Enable HTTPS, redirect HTTP to HTTPS |
| `uses-http2` | Not using HTTP/2 | Medium | Enable HTTP/2 on server |
| `no-vulnerable-libraries` | Known vulnerable JavaScript libraries | High | Update libraries to latest versions |
| `csp-xss` | CSP not effective against XSS | Medium | Implement Content Security Policy |

### Modern Web Development

| Audit ID | Issue | Severity | Fix |
|----------|-------|----------|-----|
| `uses-passive-event-listeners` | Non-passive touch event listeners | Low | Add `{ passive: true }` to touch handlers |
| `no-document-write` | Uses document.write() | High | Replace with DOM manipulation methods |
| `deprecations` | Uses deprecated APIs | Medium | Update to modern APIs |
| `geolocation-on-start` | Requests geolocation on load | Medium | Request geolocation on user interaction |
| `notification-on-start` | Requests notifications on load | Medium | Request notifications on user interaction |

### User Experience

| Audit ID | Issue | Severity | Fix |
|----------|-------|----------|-----|
| `image-aspect-ratio` | Images with incorrect aspect ratio | Medium | Use correct width/height or aspect-ratio CSS |
| `image-size-responsive` | Images not sized for viewport | Medium | Use srcset for responsive images |
| `doctype` | Missing or invalid doctype | Medium | Add `<!DOCTYPE html>` |
| `charset` | Missing charset declaration | Medium | Add `<meta charset="utf-8">` |
| `js-libraries` | Outdated JavaScript libraries | Medium | Update to latest stable versions |

### Best Practices Fix Examples

**1. Add Passive Event Listeners:**
```javascript
// Before
element.addEventListener('touchstart', handler);

// After
element.addEventListener('touchstart', handler, { passive: true });
```

**2. Replace document.write():**
```javascript
// Before
document.write('<div>Content</div>');

// After
const div = document.createElement('div');
div.textContent = 'Content';
document.body.appendChild(div);
```

**3. Add CSP Header:**
```
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'
```

**4. Update Vulnerable Libraries:**
```bash
# Check for vulnerabilities
npm audit

# Update vulnerable packages
npm update jquery
# or
npm install jquery@latest --save
```

---

## SEO Audit Checklist

### Content Best Practices

| Audit ID | Issue | Impact | Fix |
|----------|-------|--------|-----|
| `document-title` | Document missing title | High | Add descriptive `<title>` tag |
| `meta-description` | Document missing meta description | Medium | Add `<meta name="description">` |
| `http-status-code` | Page returns non-200 status | Critical | Fix server errors, redirects |
| `link-text` | Links without descriptive text | Medium | Use meaningful link text |
| `crawlable-anchors` | Links not crawlable | High | Use proper `<a href>` elements |
| `is-crawlable` | Page blocked from indexing | Critical | Remove noindex, allow in robots.txt |
| `robots-txt` | Invalid robots.txt | High | Fix robots.txt syntax |
| `image-alt` | Images missing alt text | Medium | Add descriptive alt attributes |
| `hreflang` | Missing hreflang for localized pages | Medium | Add hreflang tags for translations |
| `canonical` | Missing or invalid canonical URL | High | Add `<link rel="canonical">` |

### Mobile Friendly

| Audit ID | Issue | Impact | Fix |
|----------|-------|--------|-----|
| `viewport` | Missing viewport meta tag | Critical | Add `<meta name="viewport" content="width=device-width, initial-scale=1">` |
| `font-size` | Font sizes too small | Medium | Use minimum 16px for body text |
| `tap-targets` | Tap targets too small/close | Medium | Make buttons ≥48×48px with spacing |
| `content-width` | Content wider than screen | High | Use responsive design |

### Structured Data

| Audit ID | Issue | Impact | Fix |
|----------|-------|--------|-----|
| `structured-data` | Invalid structured data | Medium | Fix schema.org markup |

### SEO Fix Examples

**1. Add Meta Description:**
```html
<head>
  <meta name="description" content="Learn how to optimize your website performance with our comprehensive guide. Step-by-step tutorials and best practices.">
</head>
```

**2. Add Canonical URL:**
```html
<head>
  <link rel="canonical" href="https://example.com/preferred-url">
</head>
```

**3. Fix Link Text:**
```html
<!-- Before: Non-descriptive -->
<a href="/product/123">Click here</a>

<!-- After: Descriptive -->
<a href="/product/123">View Product Details</a>
```

**4. Add Hreflang Tags:**
```html
<head>
  <link rel="alternate" hreflang="en" href="https://example.com/en/page">
  <link rel="alternate" hreflang="es" href="https://example.com/es/page">
  <link rel="alternate" hreflang="x-default" href="https://example.com/page">
</head>
```

**5. Add Structured Data (JSON-LD):**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "datePublished": "2026-03-19"
}
</script>
```

---

## Audit Extraction Script

Extract all audit issues from Lighthouse result:

```javascript
function extractAuditIssues(lhr, category) {
  const audits = lhr.audits;
  const categoryAudits = lhr.categories[category]?.auditRefs || [];
  
  const issues = [];
  
  for (const ref of categoryAudits) {
    const audit = audits[ref.id];
    if (audit && audit.score !== null && audit.score < 1) {
      issues.push({
        id: ref.id,
        title: audit.title,
        description: audit.description,
        score: audit.score,
        displayValue: audit.displayValue,
        weight: ref.weight,
        details: audit.details,
      });
    }
  }
  
  // Sort by weight (importance)
  issues.sort((a, b) => b.weight - a.weight);
  
  return issues;
}

// Usage
const accessibilityIssues = extractAuditIssues(lhr, 'accessibility');
const seoIssues = extractAuditIssues(lhr, 'seo');
const bestPracticesIssues = extractAuditIssues(lhr, 'best-practices');
```

---

## Priority Matrix

### Critical (Fix Immediately)
- HTTPS not enabled
- Page returns 4xx/5xx errors
- Page blocked from indexing
- Missing viewport meta tag
- Critical accessibility blockers

### High (Fix This Week)
- Poor Core Web Vitals scores
- Missing alt text on images
- Form inputs without labels
- Vulnerable JavaScript libraries
- Invalid robots.txt

### Medium (Fix This Month)
- Color contrast issues
- Missing meta descriptions
- Non-descriptive link text
- Heading order issues
- Missing canonical URLs

### Low (Fix When Possible)
- Minor markup issues
- Deprecated API usage
- Non-passive event listeners
- Missing structured data
