# Web Automated Testing / Web自动化测试

## Overview / 概述

自动化浏览器测试技能。使用 Playwright 进行浏览器交互与 DOM 断言，tesseract.js 做 OCR 截图文字验证。支持冒烟测试、全量测试、截图回归测试。

Automated browser testing Skill. Uses Playwright for browser interaction and DOM assertions, tesseract.js for OCR screenshot text verification. Supports smoke tests, full tests, and screenshot regression testing.

## Trigger Conditions

- After code change self-check passes
- User asks to "test", "verify page"
- Need to confirm UI rendering correctness
- Screenshot regression testing

## Configuration (read from pipeline.json)

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `{{pipeline.project.testUrl}}` | Test target URL | `http://localhost:3000` |
| `{{pipeline.project.testPagePath}}` | Test page path | `/` |
| `{{pipeline.paths.tests}}` | Test script directory | `tests/auto/` |

## Test Types / 测试类型

### 1. Smoke Test (fast, always run)
- Page loads successfully
- Key DOM elements exist
- No JS runtime errors

### 2. Full Test (after major changes)
- All interaction flows
- Form submissions
- Modal/overlay open/close
- Async data loading
- Screenshot comparison

### 3. OCR Verification (optional, requires tesseract.js)
- Screenshot text recognition
- Key copy verification
- Multi-language support

## Workflow

### Step 1: Prepare
Check test dependencies installed:
```bash
npx playwright install chromium
```

### Step 2: Create Test Script
Write test cases to `{{pipeline.paths.tests}}smoke-test.cjs`:
```javascript
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('{{pipeline.project.testUrl}}{{pipeline.project.testPagePath}}');
  await page.waitForLoadState('networkidle');
  
  // DOM assertions
  const el = await page.$('{{pipeline.testing.domSelectors.mainContainer}}');
  if (!el) { console.error('FAIL: Main container not found'); process.exit(1); }
  
  console.log('OK: Page loaded successfully');
  await browser.close();
})().catch(e => { console.error('FAIL:', e.message); process.exit(1); });
```

### Step 3: Execute
```bash
node {{pipeline.paths.tests}}smoke-test.cjs
```

### Step 4: Report
Report test results: pass count / fail count, failed item screenshots and reasons.

## Dependencies

```bash
npm install playwright
npx playwright install chromium
# OCR (optional)
npm install tesseract.js sharp
```
