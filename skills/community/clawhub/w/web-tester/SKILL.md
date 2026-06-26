---
name: web-tester
description: >
  Web UI testing and browser automation using Playwright or Selenium.
  Navigate pages, interact with elements, take screenshots, validate UI state,
  generate E2E test scripts. Requires Node.js and npx for Playwright.
  Use when: (1) UI functional testing, (2) E2E test scripting, (3) screenshot
  comparison, (4) form testing, (5) cross-browser testing, (6) accessibility checks,
  (7) "UI测试", "页面测试", "自动化测试", "截图对比", "E2E测试", "浏览器自动化",
  "Playwright", "Selenium".
  NOT for: API testing (use api-tester), mobile app testing, or performance/load testing.
metadata:
  openclaw:
    emoji: "🌐"
    requires:
      bins: [node]
---

# Web Tester

Browser-based UI testing and E2E automation.

## When to Use

✅ **USE this skill when:**
- Testing web page functionality (click, fill, navigate)
- Writing E2E test scripts (Playwright/Selenium)
- Taking screenshots for visual regression
- Validating page content, forms, navigation
- Accessibility testing
- "帮我测试这个页面" / "写个E2E自动化脚本"

❌ **DON'T use this skill when:**
- API testing → use `api-tester`
- Mobile app testing → use dedicated mobile tools
- Load/stress testing → use k6/JMeter/locust

## Quick Start: Playwright

### One-shot Page Test

```bash
# Navigate and screenshot
npx -y playwright@latest test --browser=chromium -g "test name"

# Or write inline script
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('https://example.com');
  console.log('Title:', await page.title());
  await page.screenshot({ path: '/tmp/screenshot.png' });
  await browser.close();
})();
"
```

### Generate Playwright Test Script

When user provides a page URL and test scenario, generate:

```javascript
// tests/example.spec.js
const { test, expect } = require('@playwright/test');

test.describe('Login Page Tests', () => {

  test('TC001: Successful login', async ({ page }) => {
    await page.goto('https://app.example.com/login');

    // Fill form
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'Admin@123');
    await page.click('button[type="submit"]');

    // Verify redirect
    await expect(page).toHaveURL(/dashboard/);
    await expect(page.locator('h1')).toContainText('Welcome');
  });

  test('TC002: Login with empty fields', async ({ page }) => {
    await page.goto('https://app.example.com/login');
    await page.click('button[type="submit"]');

    // Verify validation messages
    await expect(page.locator('.error-message')).toBeVisible();
  });

  test('TC003: Login with wrong password', async ({ page }) => {
    await page.goto('https://app.example.com/login');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'wrongpass');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error-alert')).toContainText('Invalid');
  });
});
```

Run tests:

```bash
# Install Playwright browsers (first time)
npx playwright install chromium

# Run tests
npx playwright test tests/example.spec.js --reporter=list

# Run with headed browser (visible)
npx playwright test --headed

# Run specific test
npx playwright test -g "TC001"

# Generate HTML report
npx playwright test --reporter=html
npx playwright show-report
```

## Common UI Test Patterns

### Element Locator Strategies (priority order)

1. `data-testid` attribute (most stable)
2. `role` + accessible name
3. `placeholder` / `label` text
4. CSS selector
5. XPath (last resort)

```javascript
// Preferred
page.getByTestId('submit-btn')
page.getByRole('button', { name: 'Submit' })
page.getByPlaceholder('Enter email')
page.getByLabel('Username')

// Fallback
page.locator('button.submit-btn')
page.locator('//button[contains(text(),"Submit")]')
```

### Wait Strategies

```javascript
// Wait for element
await page.waitForSelector('.result-list');

// Wait for navigation
await page.waitForURL('**/dashboard');

// Wait for network idle
await page.waitForLoadState('networkidle');

// Wait for specific response
const response = await page.waitForResponse('**/api/users');
```

### Screenshot & Visual Comparison

```javascript
// Full page screenshot
await page.screenshot({ path: 'full-page.png', fullPage: true });

// Element screenshot
await page.locator('.chart').screenshot({ path: 'chart.png' });

// Visual comparison (Playwright built-in)
await expect(page).toHaveScreenshot('homepage.png');
```

## Test Scenarios Checklist

For any web page, consider testing:

| Category | Test Points |
|----------|-------------|
| **Navigation** | Links work, breadcrumbs correct, back button, deep links |
| **Forms** | Required fields, validation messages, submit, reset |
| **Auth** | Login, logout, session expiry, role-based access |
| **Responsive** | Mobile viewport, tablet, desktop breakpoints |
| **Accessibility** | Tab order, screen reader, color contrast, ARIA |
| **Error States** | 404 page, network error, empty state, timeout |
| **Data Display** | Pagination, sorting, filtering, search |
| **File Operations** | Upload, download, preview |

## Accessibility Quick Check

```javascript
// Install axe-core for a11y testing
// npm install @axe-core/playwright

const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

test('accessibility scan', async ({ page }) => {
  await page.goto('https://example.com');
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

## Tips

- Always use `headless: true` in CI environments
- Set reasonable timeouts (default 30s is often too long)
- Use `page.waitForLoadState('networkidle')` before assertions
- For flaky tests: add retries in config, not in test code
- Screenshot on failure is invaluable for debugging

## Selenium (Python) Reference

When Playwright is not available or user prefers Selenium:

```python
"""Selenium E2E Test Example"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    d = webdriver.Chrome(options=opts)
    d.implicitly_wait(10)
    yield d
    d.quit()

class TestLogin:
    def test_successful_login(self, driver):
        driver.get('https://app.example.com/login')
        driver.find_element(By.NAME, 'username').send_keys('admin')
        driver.find_element(By.NAME, 'password').send_keys('Admin@123')
        driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()

        WebDriverWait(driver, 10).until(
            EC.url_contains('/dashboard')
        )
        assert 'dashboard' in driver.current_url

    def test_screenshot_on_failure(self, driver):
        driver.get('https://app.example.com/broken-page')
        driver.save_screenshot('/tmp/failure.png')
```

Install: `pip install selenium webdriver-manager`

### Playwright vs Selenium — When to Choose

| 维度 | Playwright | Selenium |
|------|-----------|----------|
| 安装 | `npx playwright install` 一键搞定 | 需要 WebDriver + 浏览器匹配 |
| 速度 | 更快（原生 CDP/WebSocket） | 较慢（HTTP 协议通信） |
| 自动等待 | 内置智能等待 | 需手动写 WebDriverWait |
| 多浏览器 | Chromium/Firefox/WebKit | Chrome/Firefox/Edge/Safari |
| 语言 | JS/TS/Python/Java/.NET | Python/Java/C#/Ruby/JS |
| 适合 | 新项目、快速验证、CI | 已有 Selenium 框架的团队 |

**建议**: 新项目优先 Playwright，已有 Selenium 资产的项目继续用 Selenium。
