---
name: web-quality-audit
description: Comprehensive web quality audit covering performance, accessibility, SEO, best practices, and browser automation testing. Supports automated testing with PinchTab for headless/headed browser control, multi-instance orchestration, and token-efficient content extraction.
license: MIT
metadata:
  author: web-quality-skills
  version: "2.0"
  origin: "web-quality-skills + PinchTab"
---

# Web Quality Audit

Comprehensive quality review based on Google Lighthouse audits. Covers Performance, Accessibility, SEO, and Best Practices across 150+ checks. Includes browser automation testing with PinchTab for real-world validation.

## How it works

1. Analyze the provided code/project for quality issues
2. Categorize findings by severity (Critical, High, Medium, Low)
3. Provide specific, actionable recommendations
4. Include code examples for fixes
5. **NEW:** Validate with browser automation (PinchTab) for real-world testing

## Audit categories

### Performance (40% of typical issues)

**Core Web Vitals** — Must pass for good page experience:
* **LCP (Largest Contentful Paint) < 2.5s.** The largest visible element must render quickly. Optimize images, fonts, and server response time.
* **INP (Interaction to Next Paint) < 200ms.** User interactions must feel instant. Reduce JavaScript execution time and break up long tasks.
* **CLS (Cumulative Layout Shift) < 0.1.** Content must not jump around. Set explicit dimensions on images, embeds, and ads.

**Resource Optimization:**
* **Compress images.** Use WebP/AVIF with fallbacks. Serve correctly sized images via `srcset`.
* **Minimize JavaScript.** Remove unused code. Use code splitting. Defer non-critical scripts.
* **Optimize CSS.** Extract critical CSS. Remove unused styles. Avoid `@import`.
* **Efficient fonts.** Use `font-display: swap`. Preload critical fonts. Subset to needed characters.

**Loading Strategy:**
* **Preconnect to origins.** Add `<link rel="preconnect">` for third-party domains.
* **Preload critical assets.** LCP images, fonts, and above-fold CSS.
* **Lazy load below-fold content.** Images, iframes, and heavy components.
* **Cache effectively.** Long cache TTLs for static assets. Immutable caching for hashed files.

### Accessibility (30% of typical issues)

**Perceivable:**
* **Text alternatives.** Every `<img>` has meaningful `alt` text. Decorative images use `alt=""`.
* **Color contrast.** Minimum 4.5:1 for normal text, 3:1 for large text (WCAG AA).
* **Don't rely on color alone.** Use icons, patterns, or text alongside color indicators.
* **Captions and transcripts.** Video has captions. Audio has transcripts.

**Operable:**
* **Keyboard accessible.** All functionality available via keyboard. No keyboard traps.
* **Focus visible.** Clear focus indicators on all interactive elements.
* **Skip links.** Provide "Skip to main content" for keyboard users.
* **Sufficient time.** Users can extend time limits. No auto-advancing content without controls.

**Understandable:**
* **Page language.** Set `lang` attribute on `<html>`.
* **Consistent navigation.** Same navigation structure across pages.
* **Error identification.** Form errors clearly described and associated with fields.
* **Labels and instructions.** All form inputs have associated labels.

**Robust:**
* **Valid HTML.** No duplicate IDs. Properly nested elements.
* **ARIA used correctly.** Prefer native elements. ARIA roles match behavior.
* **Name, role, value.** Interactive elements have accessible names and correct roles.

### SEO (15% of typical issues)

**Crawlability:**
* **Valid robots.txt.** Doesn't block important resources.
* **XML sitemap.** Lists all important pages. Submitted to Search Console.
* **Canonical URLs.** Prevent duplicate content issues.
* **No noindex on important pages.** Check meta robots and headers.

**On-Page SEO:**
* **Unique title tags.** 50-60 characters. Primary keyword included.
* **Meta descriptions.** 150-160 characters. Compelling and unique.
* **Heading hierarchy.** Single `<h1>`. Logical heading structure.
* **Descriptive link text.** Not "click here" or "read more".

**Technical SEO:**
* **Mobile-friendly.** Responsive design. Tap targets ≥ 48px.
* **HTTPS.** Secure connection required.
* **Fast loading.** Performance directly impacts ranking.
* **Structured data.** JSON-LD for rich snippets (Article, Product, FAQ, etc.).

### Best practices (15% of typical issues)

**Security:**
* **HTTPS everywhere.** No mixed content. HSTS enabled.
* **No vulnerable libraries.** Keep dependencies updated.
* **CSP headers.** Content Security Policy to prevent XSS.
* **No exposed source maps.** In production builds.

**Modern Standards:**
* **No deprecated APIs.** Replace `document.write`, synchronous XHR, etc.
* **Valid doctype.** Use `<!DOCTYPE html>`.
* **Charset declared.** `<meta charset="UTF-8">` as first element in `<head>`.
* **No browser errors.** Clean console. No CORS issues.

**UX Patterns:**
* **No intrusive interstitials.** Especially on mobile.
* **Clear permission requests.** Only ask when needed, with context.
* **No misleading buttons.** Buttons do what they say.

## Severity levels

| Level | Description | Action |
|-------|-------------|--------|
| **Critical** | Security vulnerabilities, complete failures | Fix immediately |
| **High** | Core Web Vitals failures, major a11y barriers | Fix before launch |
| **Medium** | Performance opportunities, SEO improvements | Fix within sprint |
| **Low** | Minor optimizations, code quality | Fix when convenient |

## Audit output format

When performing an audit, structure findings as:

```markdown
## Audit results

### Critical issues (X found)
- **[Category]** Issue description. File: `path/to/file.js:123`
  - **Impact:** Why this matters
  - **Fix:** Specific code change or recommendation

### High priority (X found)
...

### Summary
- Performance: X issues (Y critical)
- Accessibility: X issues (Y critical)
- SEO: X issues
- Best Practices: X issues

### Recommended priority
1. First fix this because...
2. Then address...
3. Finally optimize...
```

## Quick checklist

### Before every deploy
- [ ] Core Web Vitals passing
- [ ] No accessibility errors (axe/Lighthouse)
- [ ] No console errors
- [ ] HTTPS working
- [ ] Meta tags present

### Weekly review
- [ ] Check Search Console for issues
- [ ] Review Core Web Vitals trends
- [ ] Update dependencies
- [ ] Test with screen reader

### Monthly deep dive
- [ ] Full Lighthouse audit
- [ ] Performance profiling
- [ ] Accessibility audit with real users
- [ ] SEO keyword review
- [ ] Browser automation regression tests (PinchTab)

---

## Browser Automation Testing (PinchTab)

PinchTab is a high-performance browser automation bridge for AI agents. Use it to validate your site in real browsers.

### What is PinchTab?

- **Standalone HTTP server** — Control Chrome via HTTP API
- **Token-efficient** — 800 tokens/page with text extraction (vs 10,000+ for screenshots)
- **Multi-instance** — Run multiple parallel Chrome processes
- **Headless or Headed** — Run with or without visible window
- **Self-contained** — 12MB binary, no dependencies
- **MCP integration** — Native support via SMCP plugin

### Installation

```bash
# macOS / Linux
curl -fsSL https://pinchtab.com/install.sh | bash

# npm
npm install -g pinchtab

# Docker
docker run -d -p 9867:9867 pinchtab/pinchtab
```

### Start Server

```bash
# Terminal 1: Start PinchTab server
pinchtab
# Server runs on http://localhost:9867
```

### Basic Usage

#### Navigate and Snapshot

```bash
# Navigate to URL
pinchtab nav https://example.com

# Wait 3 seconds for accessibility tree to populate
sleep 3

# Get interactive elements snapshot
pinchtab snap -i -c
```

#### Text Extraction (Token-Efficient)

```bash
# Extract text (~800 tokens vs 10,000+ for screenshots)
pinchtab nav https://example.com/article
sleep 3
pinchtab text
```

#### Click and Interact

```bash
# Get snapshot with element refs
pinchtab snap -i
# Output shows: e5: "Submit button", e12: "Email input"

# Click element by ref
pinchtab click e5

# Fill input
pinchtab fill e12 "user@example.com"

# Press key
pinchtab press e12 Enter
```

### HTTP API

```bash
# Create instance
TAB=$(curl -s -X POST http://localhost:9867/instances \
  -d '{"profile":"work"}' | jq -r '.id')

# Navigate
curl -X POST "http://localhost:9867/instances/$TAB/tabs/open" \
  -d '{"url":"https://example.com"}'

# Get snapshot (wait 3s first)
sleep 3
curl "http://localhost:9867/instances/$TAB/snapshot?filter=interactive"

# Click element
curl -X POST "http://localhost:9867/instances/$TAB/action" \
  -d '{"kind":"click","ref":"e5"}'

# Extract text
curl "http://localhost:9867/instances/$TAB/text"
```

### Web Quality Audit Patterns

#### 1. Core Web Vitals Validation

```bash
#!/bin/bash
# validate-cwv.sh

URL=${1:-"https://example.com"}
INST=$(curl -s -X POST http://localhost:9867/instances \
  -d '{"mode":"headless"}' | jq -r '.id')

# Navigate and measure load time
START=$(date +%s%N)
curl -s -X POST "http://localhost:9867/instances/$INST/tabs/open" \
  -d "{\"url\":\"$URL\"}" > /dev/null
sleep 3
END=$(date +%s%N)

# Calculate LCP estimate (simplified)
LOAD_TIME=$(( (END - START) / 1000000 ))  # ms
echo "Estimated LCP: ${LOAD_TIME}ms"

# Check if < 2.5s
if [ $LOAD_TIME -lt 2500 ]; then
  echo "✅ LCP passing"
else
  echo "❌ LCP failing (> 2.5s)"
fi

# Cleanup
curl -s -X POST "http://localhost:9867/instances/$INST/stop" > /dev/null
```

#### 2. Accessibility Tree Validation

```bash
# Get accessibility tree and check for common issues
pinchtab nav https://example.com
sleep 3

# Check for images without alt text
pinchtab snap | jq '.nodes[] | select(.role == "image" and .name == null) | {ref, role}'

# Check for buttons without labels
pinchtab snap | jq '.nodes[] | select(.role == "button" and .name == null) | {ref, role}'

# Check heading hierarchy
pinchtab snap | jq '.nodes[] | select(.role | startswith("heading")) | {role, name}'
```

#### 3. Mobile Responsiveness Check

```bash
# Create headed instance for visual inspection
pinchtab instances create --profile=mobile-test --mode=headed

# Navigate to site
pinchtab nav https://example.com

# Take screenshot for manual review
pinchtab screenshot --output=mobile-test.png

# Check viewport meta tag
pinchtab evaluate "document.querySelector('meta[name=viewport]')?.content"
```

#### 4. SEO Validation

```bash
# Extract page metadata
pinchtab nav https://example.com
sleep 2

# Get title
curl -s http://localhost:9867/instances/$INST/text | jq -r '.title'

# Get meta description (via evaluate)
pinchtab evaluate '
  document.querySelector("meta[name=description]")?.content
'

# Check for structured data
pinchtab evaluate '
  JSON.parse(document.querySelector("script[type=application/ld+json]")?.innerText || "{}")
'
```

### Agent Optimization Tips

Based on PinchTab documentation:

#### The 3-Second Wait Rule

```bash
# ❌ Too fast - accessibility tree not ready
pinchtab nav https://example.com
pinchtab snap
# Returns: {"count": 1, "nodes": [{"ref": "e0", "role": "RootWebArea"}]}

# ✅ Wait 3 seconds for full tree
pinchtab nav https://example.com
sleep 3
pinchtab snap
# Returns: {"count": 2645, "nodes": [...]}
```

#### Token-Efficient Extraction Pattern

```bash
# Navigate + wait + filter (14x more token-efficient)
curl -X POST http://localhost:9867/navigate \
  -d '{"url": "https://example.com"}' && \
sleep 3 && \
curl http://localhost:9867/snapshot | \
jq '.nodes[] | select(.name | length > 15) | .name' | \
head -30
```

**Why this works:**
1. Navigate + wait ensures full accessibility tree
2. jq filter extracts text nodes only
3. `length > 15` filters out buttons, labels
4. `head -30` limits output (saves tokens)

### Multi-Instance Testing

```bash
#!/bin/bash
# parallel-test.sh

URLS=("https://site1.com" "https://site2.com" "https://site3.com")
INSTANCES=()

# Create 3 headless instances
for i in {0..2}; do
  INST=$(curl -s -X POST http://localhost:9867/instances \
    -d '{"mode":"headless"}' | jq -r '.id')
  INSTANCES[$i]=$INST
done

# Run tests in parallel
for i in {0..2}; do
  (
    curl -s -X POST "http://localhost:9867/instances/${INSTANCES[$i]}/tabs/open" \
      -d "{\"url\":\"${URLS[$i]}\"}"
    sleep 3
    TITLE=$(curl -s "http://localhost:9867/instances/${INSTANCES[$i]}/text" | jq -r '.title')
    echo "Site $i: $TITLE"
    curl -s -X POST "http://localhost:9867/instances/${INSTANCES[$i]}/stop"
  ) &
done

wait
echo "All tests complete"
```

### MCP Integration

PinchTab provides an SMCP plugin for Claude Code integration:

```bash
# Set plugin directory
export MCP_PLUGINS_DIR=/path/to/pinchtab/plugins

# Available tools:
# - pinchtab__navigate
# - pinchtab__snapshot
# - pinchtab__action
# - pinchtab__text
# - pinchtab__screenshot
# - pinchtab__evaluate
# etc.
```

### Headless vs Headed

| Mode | Use Case | Memory | Speed |
|------|----------|--------|-------|
| **Headless** | CI/CD, scraping, batch | ~50-80 MB | Fast |
| **Headed** | Debugging, visual QA | ~100-150 MB | Slower |

```bash
# Headless for production
pinchtab instances create --mode=headless

# Headed for debugging
pinchtab instances create --mode=headed
```

---

## References

For detailed guidelines on specific areas:
- [Performance Optimization](../performance/SKILL.md)
- [Core Web Vitals](../core-web-vitals/SKILL.md)
- [Accessibility](../accessibility/SKILL.md)
- [SEO](../seo/SKILL.md)
- [Best Practices](../best-practices/SKILL.md)

### External Resources

- [PinchTab Documentation](https://pinchtab.com/docs) — Browser automation for AI agents
- [PinchTab GitHub](https://github.com/pinchtab/pinchtab) — Open source browser bridge
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) — Google's automated auditing tool
- [Web Vitals](https://web.dev/vitals/) — Essential metrics for healthy sites
- [axe DevTools](https://www.deque.com/axe/) — Accessibility testing engine

---

*Combine static analysis with real browser automation for comprehensive quality assurance.*
