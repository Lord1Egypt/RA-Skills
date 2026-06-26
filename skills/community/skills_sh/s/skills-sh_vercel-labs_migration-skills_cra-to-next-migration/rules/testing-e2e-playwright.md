---
title: Configure Playwright for Next.js
impact: LOW
impactDescription: Modern E2E testing
tags: testing, playwright, e2e
---

## Configure Playwright for Next.js

Configure Playwright for fast, reliable end-to-end testing.

**Installation:**

```bash
npm init playwright@latest
```

**Playwright configuration:**

```ts
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

**Example E2E test:**

```ts
// e2e/navigation.spec.ts
import { test, expect } from '@playwright/test'

test('homepage has title', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveTitle(/My App/)
})

test('navigation to about', async ({ page }) => {
  await page.goto('/')
  await page.click('text=About')
  await expect(page).toHaveURL('/about')
  await expect(page.locator('h1')).toContainText('About')
})

test('search functionality', async ({ page }) => {
  await page.goto('/')
  await page.fill('input[placeholder="Search..."]', 'react')
  await page.click('button[type="submit"]')
  await expect(page).toHaveURL(/search\?q=react/)
})
```

**Testing with authentication:**

```ts
// e2e/auth.setup.ts
import { test as setup, expect } from '@playwright/test'

const authFile = 'playwright/.auth/user.json'

setup('authenticate', async ({ page }) => {
  await page.goto('/login')
  await page.fill('input[name="email"]', 'user@example.com')
  await page.fill('input[name="password"]', 'password')
  await page.click('button[type="submit"]')
  await expect(page).toHaveURL('/dashboard')
  await page.context().storageState({ path: authFile })
})

// playwright.config.ts - add to projects
{
  name: 'authenticated',
  use: { storageState: 'playwright/.auth/user.json' },
  dependencies: ['authenticate'],
}
```
