# Quick Start — Chrome DevTools Auto Analyzer

Get started in 5 minutes with automated website analysis.

---

## 1-Minute Setup

### Step 1: Install Dependencies

```bash
cd /path/to/chrome-devtools-auto-analyzer
npm install
```

### Step 2: Verify Installation

```bash
node --version  # Should be v18+
npm list lighthouse chrome-launcher
```

### Step 3: Run Your First Audit

```bash
node automation-script.js https://example.com
```

**That's it!** You'll see results like:

```
======================================================================
📊 Analysis Results for: https://example.com
🕐 Timestamp: 2026-03-19T10:30:00.000Z
📱 Device: desktop
======================================================================

📈 Category Scores:
  Performance: 85/100 ⚪ Good
  Accessibility: 92/100 ⚪ Good
  Best Practices: 100/100 ⚪ Good
  SEO: 95/100 ⚪ Good

⚡ Core Web Vitals & Performance Metrics:
  FCP: 1200ms ⚪ Good (target: <1800ms)
  LCP: 2100ms ⚪ Good (target: <2500ms)
  CLS: 0.05 ⚪ Good (target: <0.1)
  TBT: 150ms ⚪ Good (target: <200ms)
  SI: 2800ms ⚪ Good (target: <3400ms)

✅ No critical issues found! Great job!

======================================================================
📊 Overall Score: 93/100 ⚪ Good
======================================================================

💡 Tip: Run with --mobile flag to test mobile performance

💾 Results saved to: results/example_com_2026-03-19T10-30-00.json
```

---

## Common Commands

### Desktop Audit
```bash
node automation-script.js https://example.com
```

### Mobile Audit
```bash
node automation-script.js https://example.com --mobile
```

### Custom Output Directory
```bash
node automation-script.js https://example.com --output=./my-reports
```

### View HTML Report
```bash
# HTML reports are saved alongside JSON files
open results/example_com_*.html  # macOS
xdg-open results/example_com_*.html  # Linux
start results/example_com_*.html  # Windows
```

---

## Understanding Results

### Score Ratings

| Score | Rating | Emoji |
|-------|--------|-------|
| 90-100 | Good | ⚪ |
| 50-89 | Needs Improvement | 🟡 |
| 0-49 | Poor | 🔴 |

### Core Web Vitals Targets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | <2.5s | 2.5-4.0s | >4.0s |
| CLS | <0.1 | 0.1-0.25 | >0.25 |
| INP | <200ms | 200-500ms | >500ms |
| FCP | <1.8s | 1.8-3.0s | >3.0s |
| TBT | <200ms | 200-600ms | >600ms |

---

## Fixing Issues

When issues are found, the script provides fix suggestions:

```
❌ Critical Issues & Fixes:

  [Performance] Cumulative Layout Shift
    Value: 0.83
    Fix: 🔴 CRITICAL: Add width/height to images, reserve space for ads/embeds, use CSS aspect-ratio

  [Accessibility] Image elements have [alt] attributes
    Fix: 🔴 Add descriptive alt attributes to all images
```

### Common Fixes

**High CLS (>0.1):**
```html
<!-- Add width and height to images -->
<img src="hero.jpg" width="1200" height="630" alt="Hero">
```

**Missing Alt Text:**
```html
<!-- Add descriptive alt text -->
<img src="product.jpg" alt="Blue wireless headphones on white background">
```

**Poor LCP (>2.5s):**
```html
<!-- Preload critical images -->
<link rel="preload" as="image" href="hero.jpg">
```

---

## Troubleshooting

### "lighthouse is not a function"

```bash
# Fix: Add to package.json
echo '{"type": "module"}' > package.json
```

### "Chrome not found"

```bash
# Install Chrome
# Ubuntu/Debian:
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb

# Or use Puppeteer's bundled Chromium:
npm install puppeteer
```

### "JavaScript heap out of memory"

```bash
node --max-old-space-size=4096 automation-script.js https://example.com
```

**See [`troubleshooting.md`](troubleshooting.md) for more solutions.**

---

## Next Steps

1. **Analyze multiple pages:**
   ```bash
   for url in https://example.com https://example.com/about; do
     node automation-script.js $url
   done
   ```

2. **Track progress over time:**
   - Save results to memory using the skill's memory template
   - Compare scores before/after optimizations

3. **Integrate with CI/CD:**
   - Add to GitHub Actions (see [`setup.md`](setup.md))
   - Set up Lighthouse CI for automated checks

4. **Learn more:**
   - [`metrics-reference.md`](metrics-reference.md) - Detailed metric explanations
   - [`audit-checklist.md`](audit-checklist.md) - Complete audit checklists
   - [`troubleshooting.md`](troubleshooting.md) - Common errors and solutions

---

## Need Help?

- **Quick fixes:** See [`troubleshooting.md`](troubleshooting.md)
- **Detailed setup:** See [`setup.md`](setup.md)
- **Metric details:** See [`metrics-reference.md`](metrics-reference.md)
