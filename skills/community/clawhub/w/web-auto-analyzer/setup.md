# Setup — Chrome DevTools Auto Analyzer

Installation and setup instructions for automated website analysis.

> **⚡ Quick Start:** For fastest setup, see [`quick-start.md`](quick-start.md) for the 5-minute guide.

---

## Prerequisites

### Required Software

| Software | Minimum Version | Purpose |
|----------|-----------------|---------|
| Node.js | 18.x | JavaScript runtime |
| npm | 9.x | Package manager |
| Chrome/Chromium | 115+ | Browser for audits |

### Verify Installation

```bash
# Check Node.js version
node --version
# Expected: v18.x.x or higher

# Check npm version
npm --version
# Expected: 9.x.x or higher

# Check if Chrome is available
google-chrome --version  # Linux
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version  # macOS
```

---

## Installation Steps

### Step 1: Create Project Directory

```bash
mkdir website-analyzer
cd website-analyzer
npm init -y
```

### Step 2: Install Dependencies

```bash
# Install Lighthouse and Chrome launcher
npm install lighthouse chrome-launcher

# Optional: Install Puppeteer for custom metrics
npm install puppeteer
```

### Step 3: Configure ES Modules (Required)

Lighthouse v10+ requires ES modules. Add to `package.json`:

```bash
# Method 1: Using echo
echo '{
  "type": "module",
  "dependencies": {
    "lighthouse": "^12.x",
    "chrome-launcher": "^1.x"
  }
}' > package.json

# Method 2: Edit manually
# Add "type": "module" to package.json
```

**⚠️ Important:** Without this step, you'll get "lighthouse is not a function" error.

### Step 4: Copy Automation Script

Copy `automation-script.js` from this skill to your project directory:

```bash
cp /path/to/skill/automation-script.js ./analyze.js
```

### Step 5: Make Script Executable (Optional)

```bash
chmod +x analyze.js
```

---

## Quick Start

### Run Your First Audit

```bash
# Basic audit (desktop)
node analyze.js https://example.com

# Mobile emulation
node analyze.js https://example.com --mobile

# Save to custom output directory
node analyze.js https://example.com --output=./my-results
```

### Expected Output

```
🚀 Starting Lighthouse audit for: https://example.com
📱 Device: desktop
✅ Audit complete!

============================================================
📊 Analysis Results for: https://example.com
🕐 Timestamp: 2026-03-19T10:30:00.000Z
📱 Device: desktop
============================================================

📈 Category Scores:
  Performance: 85/100 ⚪ Good
  Accessibility: 92/100 ⚪ Good
  Best Practices: 100/100 ⚪ Good
  SEO: 95/100 ⚪ Good

⚡ Performance Metrics:
  FCP: 1200ms ⚪ Good
  LCP: 2100ms ⚪ Good
  CLS: 0.05 ⚪ Good
  TBT: 150ms ⚪ Good
  SI: 2800ms ⚪ Good
  INP: 180ms ⚪ Good

❌ Critical Issues:
  Performance:
    🔴 Largest Contentful Paint element took too long to load
       Value: 2.1 s

💾 Results saved to: ./results/example_com_2026-03-19T10-30-00-000Z.json
📄 HTML report saved to: ./results/example_com_2026-03-19T10-30-00-000Z.html
```

---

## Configuration Options

### Command Line Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--mobile` | Use mobile emulation | `node analyze.js URL --mobile` |
| `--output=DIR` | Save results to directory | `node analyze.js URL --output=./reports` |
| `--help` | Show help message | `node analyze.js --help` |

### Modify Script Configuration

Edit `automation-script.js` to customize defaults:

```javascript
const CONFIG = {
  logLevel: 'info',        // 'silent', 'error', 'warn', 'info', 'verbose'
  output: 'json',          // 'json', 'html', 'csv'
  onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
  emulatedFormFactor: 'desktop',  // 'mobile' or 'desktop'
  numberOfRuns: 1,         // Number of runs for averaging
};
```

---

## Advanced Usage

### Run Lighthouse CLI Directly

```bash
# Full audit with JSON output
lighthouse https://example.com --output=json --output-path=report.json

# Performance only
lighthouse https://example.com --only-categories=performance

# Mobile emulation
lighthouse https://example.com --emulated-form-factor=mobile

# Custom throttling
lighthouse https://example.com --throttling.cpuSlowdownMultiplier=4

# View report in browser
lighthouse https://example.com --view
```

### Use Lighthouse as Node Module

```javascript
const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');

async function audit(url) {
  const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless'] });
  
  const options = {
    logLevel: 'info',
    output: 'json',
    onlyCategories: ['performance'],
    port: chrome.port,
  };
  
  const result = await lighthouse(url, options);
  
  console.log('Performance score:', result.lhr.categories.performance.score * 100);
  
  await chrome.kill();
}

audit('https://example.com');
```

### Batch Analysis

Create a script to analyze multiple URLs:

```javascript
// batch-analyze.js
const { runLighthouseAudit, saveResults } = require('./analyze');

const urls = [
  'https://example.com',
  'https://example.com/about',
  'https://example.com/products',
];

async function batchAnalyze() {
  for (const url of urls) {
    try {
      const results = await runLighthouseAudit(url);
      saveResults(results, './batch-results');
    } catch (error) {
      console.error(`Failed to analyze ${url}:`, error.message);
    }
  }
}

batchAnalyze();
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse Audit

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: |
          npm install -g lighthouse
          npm install chrome-launcher
      
      - name: Run Lighthouse
        run: |
          lighthouse https://your-site.com \
            --output=json \
            --output-path=./lighthouse-results.json \
            --emulated-form-factor=mobile
      
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: lighthouse-results
          path: ./lighthouse-results.json
```

### Lighthouse CI

```bash
# Install LHCI
npm install -g @lhci/cli

# Create config
cat > lighthouserc.js << 'EOF'
module.exports = {
  ci: {
    collect: {
      url: ['https://example.com'],
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.8 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
      },
    },
  },
};
EOF

# Run LHCI
lhci autorun
```

---

## Troubleshooting

### Chrome Not Found

**Error:** `Chrome could not be found`

**Solutions:**
```bash
# Linux: Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb

# macOS: Install Chrome
open https://www.google.com/chrome/

# Or use Puppeteer's bundled Chromium
npm install puppeteer
```

### Headless Chrome Fails

**Error:** `Failed to launch Chrome`

**Solutions:**
```bash
# Linux: Install dependencies
sudo apt-get install -y \
  libnss3 \
  libnspr4 \
  libatk1.0-0 \
  libatk-bridge2.0-0 \
  libcups2 \
  libdrm2 \
  libxkbcommon0 \
  libxcomposite1 \
  libxdamage1 \
  libxfixes3 \
  libxrandr2 \
  libgbm1 \
  libasound2 \
  libpango-1.0-0 \
  libcairo2
```

### Port Already in Use

**Error:** `Port 9222 is already in use`

**Solution:** Specify a different port:
```javascript
const chrome = await chromeLauncher.launch({
  chromeFlags: ['--headless'],
  port: 9223, // Different port
});
```

### Memory Issues

**Error:** `JavaScript heap out of memory`

**Solution:** Increase Node.js memory limit:
```bash
node --max-old-space-size=4096 analyze.js https://example.com
```

---

## Troubleshooting Quick Reference

| Error | Solution |
|-------|----------|
| "lighthouse is not a function" | Add `"type": "module"` to package.json |
| "Chrome not found" | Install Chrome or `npm install puppeteer` |
| "Failed to launch Chrome" | Install Linux dependencies (see troubleshooting.md) |
| "Port already in use" | Kill Chrome or use different port |
| "Heap out of memory" | Use `--max-old-space-size=4096` |
| "INP: N/A" | Normal - requires user interaction |

**For detailed troubleshooting, see [`troubleshooting.md`](troubleshooting.md).**

---

## Security Considerations

1. **Authentication:** Do not run automated audits on pages requiring authentication without proper security measures.

2. **Rate Limiting:** When analyzing multiple URLs, add delays to avoid overwhelming servers:
   ```javascript
   await new Promise(resolve => setTimeout(resolve, 2000)); // 2 second delay
   ```

3. **Data Privacy:** JSON reports may contain URL structure and page content. Store securely.

4. **Third-Party Scripts:** Audits may trigger third-party tracking. Consider using ad blockers or network interception.

---

## Next Steps

After setup:
1. **Run your first audit:** `node analyze.js https://example.com`
2. **Review results:** Check `./results/` directory
3. **Understand metrics:** See [`metrics-reference.md`](metrics-reference.md)
4. **Fix issues:** See [`audit-checklist.md`](audit-checklist.md)
5. **Track progress:** Use [`memory-template.md`](memory-template.md)
6. **Get help:** See [`troubleshooting.md`](troubleshooting.md)

**For fastest setup, see [`quick-start.md`](quick-start.md) for the 5-minute guide.**
