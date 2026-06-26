# Troubleshooting — Chrome DevTools Auto Analyzer

Common errors and solutions for automated website analysis.

---

## Installation Errors

### "lighthouse is not a function"

**Error:**
```
TypeError: lighthouse is not a function
```

**Cause:** Lighthouse v10+ uses ES modules, but package.json is missing `"type": "module"`.

**Solution:**
```bash
# Add to package.json
echo '{
  "type": "module",
  "dependencies": {
    "lighthouse": "^12.x",
    "chrome-launcher": "^1.x"
  }
}' > package.json
```

---

### "Cannot find module 'lighthouse'"

**Error:**
```
Error: Cannot find module 'lighthouse'
```

**Cause:** Dependencies not installed.

**Solution:**
```bash
npm install lighthouse chrome-launcher
```

---

## Chrome/Browser Errors

### "Chrome could not be found"

**Error:**
```
Error: Chrome could not be found
```

**Cause:** Chrome/Chromium not installed or not in PATH.

**Solutions:**

**Option 1: Install Chrome**
```bash
# Ubuntu/Debian
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb

# macOS
open https://www.google.com/chrome/

# Windows
# Download from https://www.google.com/chrome/
```

**Option 2: Use Puppeteer's bundled Chromium**
```bash
npm install puppeteer
```

**Option 3: Specify Chrome path**
```javascript
const chrome = await chromeLauncher.launch({
  chromePath: '/usr/bin/google-chrome', // Linux
  // chromePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', // macOS
  chromeFlags: ['--headless']
});
```

---

### "Failed to launch Chrome"

**Error:**
```
Error: Failed to launch Chrome!
```

**Cause:** Missing system dependencies (Linux) or sandbox issues.

**Solution (Linux):**
```bash
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

**Solution (Docker/Container):**
```javascript
chromeFlags: [
  '--headless',
  '--no-sandbox',
  '--disable-setuid-sandbox',
  '--disable-dev-shm-usage'
]
```

---

### "Port 9222 is already in use"

**Error:**
```
Error: Port 9222 is already in use
```

**Cause:** Another Chrome instance is using the debugging port.

**Solution:**
```javascript
// Specify different port
const chrome = await chromeLauncher.launch({
  port: 9223, // Different port
  chromeFlags: ['--headless']
});
```

Or kill existing Chrome:
```bash
# Linux
pkill -f chrome
pkill -f chromium

# macOS
killall "Google Chrome"

# Windows
taskkill /F /IM chrome.exe
```

---

## Memory Errors

### "JavaScript heap out of memory"

**Error:**
```
FATAL ERROR: Ineffective mark-compacts near heap limit
Allocation failed - JavaScript heap out of memory
```

**Cause:** Node.js default memory limit (2GB) exceeded.

**Solution:**
```bash
# Increase memory limit
node --max-old-space-size=4096 automation-script.js https://example.com

# Or set environment variable
export NODE_OPTIONS="--max-old-space-size=4096"
```

---

### "Timeout waiting for page load"

**Error:**
```
Error: Navigation timeout exceeded
```

**Cause:** Page takes too long to load.

**Solution:**
```javascript
// Increase timeout in script
const flags = {
  ...options,
  maxWaitForLoad: 60000, // 60 seconds
};
```

---

## Network Errors

### "Failed to fetch URL"

**Error:**
```
Error: Failed to fetch URL: https://example.com
```

**Cause:** Network issues, DNS resolution failure, or site is down.

**Solutions:**
1. Check internet connection
2. Verify URL is accessible in browser
3. Check DNS resolution: `nslookup example.com`
4. Try with different network

---

### "INP: N/A" in results

**Output:**
```
INP: N/A
```

**Cause:** INP (Interaction to Next Paint) requires user interaction. Headless audits don't simulate interactions.

**Solution:** This is normal for automated audits. For INP measurement:
1. Use Chrome DevTools manually
2. Use Puppeteer to simulate interactions
3. Use field data from Chrome UX Report (CrUX)

---

## Audit Quality Issues

### "Performance score varies between runs"

**Issue:** Scores differ by 5-10 points between runs.

**Cause:** Network variability, server response times, system load.

**Solutions:**
1. Run multiple audits and average: `numberOfRuns: 3`
2. Use simulated throttling (default)
3. Run from consistent environment
4. Clear cache between runs

```javascript
const CONFIG = {
  numberOfRuns: 3, // Average multiple runs
};
```

---

### "CLS score is very high"

**Issue:** CLS > 0.25 (Poor)

**Common Causes:**
1. Images without width/height attributes
2. Ads/embeds without reserved space
3. Dynamically injected content
4. Web fonts causing layout shifts

**Solutions:**
```html
<!-- Add explicit dimensions -->
<img src="hero.jpg" width="1200" height="630" alt="Hero">

<!-- Use CSS aspect-ratio -->
.image-container {
  aspect-ratio: 16 / 9;
}

<!-- Reserve space for ads -->
.ad-container {
  min-height: 250px;
}

<!-- Preload critical fonts -->
<link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin>
```

---

### "LCP score is poor"

**Issue:** LCP > 4.0s

**Common Causes:**
1. Slow server response
2. Large unoptimized images
3. Render-blocking resources
4. Client-side rendering

**Solutions:**
```html
<!-- Preload LCP image -->
<link rel="preload" as="image" href="hero.jpg">

<!-- Use modern image formats -->
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="Hero">
</picture>

<!-- Defer non-critical CSS -->
<link rel="preload" as="style" href="critical.css">
<link rel="stylesheet" href="non-critical.css" media="print" onload="this.media='all'">
```

---

## CI/CD Integration Issues

### "LHCI fails in GitHub Actions"

**Error:**
```
Error: Chrome not found
```

**Solution (GitHub Actions):**
```yaml
jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install Chrome
        run: |
          wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
          sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
          sudo apt-get update
          sudo apt-get install -y google-chrome-stable
      
      - name: Install dependencies
        run: npm install lighthouse chrome-launcher
      
      - name: Run Lighthouse
        run: node automation-script.js https://example.com
```

---

## Performance Optimization

### "Audit takes too long"

**Issue:** Audit takes >2 minutes.

**Solutions:**
1. Reduce categories to audit:
```javascript
const flags = {
  onlyCategories: ['performance'], // Only what you need
};
```

2. Use throttling:
```javascript
const flags = {
  throttlingMethod: 'simulate', // Faster than devtools
};
```

3. Skip resource-intensive audits:
```javascript
const flags = {
  skipAudits: ['screenshot-thumbnails', 'full-page-screenshot'],
};
```

---

## Getting Help

If issues persist:

1. **Check logs:** Run with `--logLevel=verbose`
2. **Update packages:** `npm update lighthouse chrome-launcher`
3. **Check versions:** Ensure Node.js v18+, Lighthouse v12+
4. **Report bugs:** Include error message, versions, and OS

---

## Quick Reference

| Error | Quick Fix |
|-------|-----------|
| "lighthouse is not a function" | Add `"type": "module"` to package.json |
| "Chrome not found" | Install Chrome or `npm install puppeteer` |
| "Heap out of memory" | `node --max-old-space-size=4096` |
| "Port in use" | Change port or kill Chrome |
| "Failed to launch" | Install Linux dependencies |
| "INP: N/A" | Normal - requires user interaction |
| "High CLS" | Add width/height to images |
| "High LCP" | Preload images, optimize server |
