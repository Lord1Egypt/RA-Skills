# E2E Test Execution

## Part 1: Execution Modes

Two modes for E2E test execution:

| Mode | When to use | Output |
| --- | --- | --- |
| Code mode (default) | Persistent tests, CI integration, regression | `.spec.ts` Playwright test files |
| Live operation mode | Exploratory testing, one-off verification | Agent Browser operation record + screenshots |

Code mode MUST be the default. Live mode is triggered ONLY when the user explicitly asks for interactive browser testing or when the Agent Browser skill is invoked.

## Part 2: From Interaction Test Plan to Executable Code

Conversion rules:
- Each row in the interaction test plan table → one `test()` block.
- Element column → Playwright locator (Priority: `getByRole` > `getByLabel` > `getByPlaceholder` > `getByTestId` > CSS selector).
- Action column → Playwright action (`click()`, `fill()`, `press()`, `selectOption()`, `check()`, `setInputFiles()`, `dragTo()`).
- Expected Behavior column → Playwright assertion (`expect(locator).toBeVisible()`, `.toHaveText()`, `.toHaveCSS()`, `.toBeDisabled()`, `.toHaveURL()`).
- State Type column → `test.describe()` grouping.
- Selector column (from updated interaction-test-plan) → used directly as the locator.

### Concrete Example: 5-Row Test Plan to `.spec.ts`

```typescript
import { test, expect } from '@playwright/test';

test.describe('Login Flow', () => {
  test('User can log in with valid credentials', async ({ page }) => {
    // Row 1: Navigate to page
    await page.goto('/login');
    
    // Row 2: Enter username
    await page.getByLabel('Username').fill('testuser123');
    
    // Row 3: Enter password
    await page.getByLabel('Password').fill('SecurePassword!');
    
    // Row 4: Click login button
    await page.getByRole('button', { name: 'Log in' }).click();
    
    // Row 5: Verify successful login redirection
    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByRole('heading', { name: 'Welcome, testuser123' })).toBeVisible();
  });
});
```

### Wait Strategy Rules
- MUST use condition-based waits: `waitForSelector`, `waitForResponse`, `waitForLoadState`, `waitForURL`.
- FORBIDDEN: `setTimeout`, `page.waitForTimeout` (except as absolute last resort with a block comment explaining why).
- For API-dependent UI: MUST `await page.waitForResponse('**/api/endpoint')` before asserting on the UI outcome.

## Part 3: Regression Testing

Four mechanisms for evaluating regressions:

1. **Visual baseline snapshots**: `page.screenshot()` on first run → `expect(page).toHaveScreenshot('name.png', { maxDiffPixelRatio: 0.01 })` on subsequent runs.
2. **Change-driven test selection**: Based on changed files/modules, determine which E2E tests to re-run (not full suite). Mapping strategy: Changed file path patterns (`src/features/login/**`) → Relevant test files (`e2e/login.spec.ts`).
3. **API response regression**: Intercept API responses with `page.route()`, validate response structure against baseline schema (field existence, types, required fields).
4. **Before/After report**: Each regression run outputs: change scope → affected tests → pass/fail/new diffs → screenshot comparisons.

### Regression Code Examples

```typescript
import { test, expect } from '@playwright/test';

// Mechanism 1: Visual baseline snapshots
test('Dashboard visual regression', async ({ page }) => {
  await page.goto('/dashboard');
  // Compares against a baseline image, fails if diff > 1%
  await expect(page).toHaveScreenshot('dashboard-baseline.png', { maxDiffPixelRatio: 0.01 });
});

// Mechanism 3: API response regression
test('User profile API response schema validation', async ({ page }) => {
  await page.route('**/api/profile', async (route) => {
    const response = await route.fetch();
    const json = await response.json();
    
    // Baseline schema validations
    expect(json).toHaveProperty('id');
    expect(typeof json.id).toBe('string');
    expect(json).toHaveProperty('email');
    expect(typeof json.email).toBe('string');
    expect(json).toHaveProperty('roles');
    expect(Array.isArray(json.roles)).toBeTruthy();
    
    await route.fulfill({ response, json });
  });
  
  await page.goto('/profile');
});
```

## Part 4: Robustness & Boundary Testing

Each feature point MUST be evaluated against all 8 categories (mark N/A with reason if not applicable).

| # | Category | What to test | Severity |
|---|----------|-------------|----------|
| 1 | Input boundary | Empty, 10000-char string, `<script>alert(1)</script>`, emoji 🎉, zero-width chars, SQL injection fragments, negative/zero/huge numbers, whitespace-only, leading/trailing spaces | P0 |
| 2 | Network & API failure | API timeout (simulate 30s delay with `page.route()`), API 500/502/503, empty response body, malformed JSON, offline mode (`page.context().setOffline(true)`) | P0 |
| 3 | Concurrent & repeated operations | Button double-click/rapid clicks, form double-submit, rapid page navigation (navigate before load completes), parallel request race conditions | P1 |
| 4 | Auth & permissions | Unauthenticated access to protected pages, expired token operations, cross-user data access, missing/expired CSRF token | P0 |
| 5 | State persistence | Form data after page refresh, browser back/forward navigation, LocalStorage/SessionStorage anomalies (full/unavailable) | P1 |
| 6 | Browser compatibility | Chromium + Firefox + WebKit via Playwright `projects` config | P2 |
| 7 | Responsive & viewport | Desktop (1280×720), tablet (768×1024), mobile (375×667) — layout and interaction | P1 |
| 8 | Accessibility | Tab order, Enter/Space activation, Escape to close, `aria-label` for screen readers, visible focus indicators | P2 |

### Robustness Examples (Login Form)

```typescript
import { test, expect } from '@playwright/test';

test.describe('Robustness & Boundary Testing - Login Form', () => {
  
  // 1. Input boundary
  test('Handles malicious and boundary inputs without crashing', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Username').fill('<script>alert(1)</script>'.repeat(50));
    await page.getByLabel('Password').fill('emoji 🎉 zero width \u200B');
    await page.getByRole('button', { name: 'Log in' }).click();
    await expect(page.getByText('Invalid credentials')).toBeVisible();
  });

  // 2. Network & API failure
  test('Handles API timeout gracefully', async ({ page }) => {
    await page.route('**/api/login', async route => {
      // Simulate timeout
      await new Promise(r => setTimeout(r, 5000));
      await route.abort('timedout');
    });
    await page.goto('/login');
    await page.getByLabel('Username').fill('user');
    await page.getByLabel('Password').fill('pass');
    await page.getByRole('button', { name: 'Log in' }).click();
    await expect(page.getByText('Network timeout. Please try again.')).toBeVisible();
  });

  // 3. Concurrent & repeated operations
  test('Prevents duplicate submissions on double-click', async ({ page }) => {
    let apiCalls = 0;
    await page.route('**/api/login', async route => {
      apiCalls++;
      await new Promise(r => setTimeout(r, 500)); // Delay to allow double click
      await route.fulfill({ status: 200, json: { token: 'mock' } });
    });
    await page.goto('/login');
    await page.getByLabel('Username').fill('user');
    await page.getByLabel('Password').fill('pass');
    
    const loginBtn = page.getByRole('button', { name: 'Log in' });
    await loginBtn.click();
    await loginBtn.click(); // Attempt double click
    
    expect(apiCalls).toBe(1); // Assert only 1 request was dispatched
  });

  // 4. Auth & permissions
  test('Redirects to login when accessing authenticated route', async ({ page }) => {
    await page.goto('/settings');
    await expect(page).toHaveURL(/.*\/login/);
  });

  // 5. State persistence
  test('Maintains entered username after page refresh', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Username').fill('persistentUser');
    await page.reload();
    await expect(page.getByLabel('Username')).toHaveValue('persistentUser');
  });

  // 6. Browser compatibility
  test('Renders login button correctly across browsers', async ({ page }) => {
    // Note: Cross-browser execution is handled via Playwright projects config.
    await page.goto('/login');
    await expect(page.getByRole('button', { name: 'Log in' })).toBeVisible();
  });

  // 7. Responsive & viewport
  test('Adjusts layout on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/login');
    const btnBox = await page.getByRole('button', { name: 'Log in' }).boundingBox();
    expect(btnBox?.width).toBeLessThanOrEqual(375);
  });

  // 8. Accessibility
  test('Supports keyboard navigation and focus management', async ({ page }) => {
    await page.goto('/login');
    await page.keyboard.press('Tab');
    await expect(page.getByLabel('Username')).toBeFocused();
    await page.keyboard.press('Tab');
    await expect(page.getByLabel('Password')).toBeFocused();
    await page.keyboard.press('Tab');
    await expect(page.getByRole('button', { name: 'Log in' })).toBeFocused();
  });
});
```

## Part 5: Failure Path Checklist

Mandatory failure paths — NOT optional:

| Failure type | Specific scenarios | Expected behavior |
|-------------|-------------------|-------------------|
| API 4xx | 400 bad request, 401 unauthorized, 403 forbidden, 404 not found, 409 conflict, 422 validation, 429 rate limit | Show user-understandable error message specific to the status |
| API 5xx | 500 server error, 502 bad gateway, 503 maintenance | Show generic error + retry option |
| Empty data | Empty list, no search results, detail page data missing | Show empty state placeholder UI (illustration + copy + CTA) |
| Partial failure | Batch operation with some success/some failure, file upload half-failed | Clearly state which succeeded, which failed, how to handle |
| Race condition | Same data modified by another user, optimistic update conflict | Show conflict prompt, offer refresh/overwrite options |
| Resource limits | File size exceeded, upload count exceeded, storage full | Show limit clearly before or at failure |
| Timeout | Long operations (large file upload, report export) timeout | Show progress + retry option after timeout |

### Simulating API Failure Paths

```typescript
import { test, expect } from '@playwright/test';

test.describe('Failure Path Interceptions', () => {
  
  test('API 4xx: Shows 401 Unauthorized specific message', async ({ page }) => {
    await page.route('**/api/data', async route => {
      await route.fulfill({ status: 401, json: { error: 'Unauthorized' } });
    });
    
    await page.goto('/dashboard');
    await expect(page.getByText('Your session has expired. Please log in again.')).toBeVisible();
  });

  test('API 5xx: Shows 500 Server Error generic UI with retry', async ({ page }) => {
    await page.route('**/api/data', async route => {
      await route.fulfill({ status: 500, body: 'Internal Server Error' });
    });
    
    await page.goto('/dashboard');
    await expect(page.getByText('Something went wrong on our end.')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Retry' })).toBeVisible();
  });
});
```

## Part 6: Test Severity & Execution Priority

| Level | Definition | E2E meaning | Required? |
|-------|-----------|-------------|----------|
| P0 | Data loss, security vulnerability, core flow blocked | Input injection, auth bypass, payment anomaly, core CRUD failure | MUST cover |
| P1 | Functional error with workaround | Concurrent operation anomaly, state inconsistency, partial failure without notification | MUST cover |
| P2 | Experience issue | Visual regression, responsive breakage, accessibility defect | Recommended |
| P3 | Rare edge case | Extreme input (1MB text paste), extreme viewport (240px) | By risk assessment |

**Execution order**: P0 all → P1 all → P2 by feature priority → P3 by risk.

## Part 7: Browser Operation Specification

- **Locator priority**: `getByRole` > `getByLabel` > `getByPlaceholder` > `getByTestId` > CSS selector.
- **Wait strategy**: Condition-based (`waitForSelector` / `waitForResponse` / `waitForLoadState`). `setTimeout` is FORBIDDEN.
- **Screenshots**: Auto-capture at key steps, auto-capture on failure.
- **Viewport management**: Desktop (1280×720) + Tablet (768×1024) + Mobile (375×667).

### Multi-browser Config

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile-chrome', use: { ...devices['Pixel 5'] } },
    { name: 'mobile-safari', use: { ...devices['iPhone 12'] } },
  ],
});
```

### Live Operation Mode (Agent Browser) Standard Flow:
1. Open target URL
2. Follow test plan step by step
3. Screenshot each step
4. Compare with expected behavior
5. Report pass/fail per step

## Part 8: QA Report & Internal Quality Gate

**Design principles:**
- One unified report per task, produced once after all tests complete.
- **Deterministic Script Gate**: Enforced internally via `python3 scripts/validate_qa_gate.py check <qa_report.json> [--json]`.
- **Decoupled Block Handling**:
  - If `BLOCKED` in standalone mode: QA presents details and options to the user (`[Fix Code]` / `[Waive Block]` / `[Update Expectation]`), never hard-terminating.
  - If `BLOCKED` in `workflow-orchestrator` mode: `workflow-orchestrator`'s meta-orchestrator judge evaluates task context to decide whether to dispatch `fixer` or waive/skip.
- `workflow-orchestrator` displays this report if present, but does NOT depend on it (optional plugin pattern).

*Note: This report is written to the ledger as the `qa_report` field, and `workflow-orchestrator`'s visualization renders it only when present (optional plugin pattern).*

### QA Report Template

```markdown
## QA Report

**Task**: {task name}
**Test scope**: {features and modules tested}
**Produced at**: {timestamp}

---

### 0. Internal Quality Gate Verdict

**Verdict**: `PASSED` | `BLOCKED` | `CONDITIONAL_PASS`

- [x] Planning Integrity: Coverage matrix evaluated, all cells addressed with rationale
- [x] Execution Completeness: 100% of planned tests executed ({N} planned / {N} executed)
- [x] Defect Gate: 0 unresolved P0 failures on production code (or BLOCKED if unresolved)
- [x] Evidence Chain: Complete logs and screenshots attached for all failures

---

### 1. Summary

| Type | Test file | Planned | Executed | Passed | Failed | Skipped |
|------|-----------|---------|----------|--------|--------|---------|
| Integration | {path} | N | N | N | N | N |
| E2E | {path} | N | N | N | N | N |
| **Total** | | **N** | **N** | **N** | **N** | **N** |

External dependency coverage: {list}

---

### 2. Coverage Matrix

| Category | {Element 1} | {Element 2} | ... |
|----------|------------|------------|-----|
| Happy Path | ✅ | ✅ | ... |
| Input boundary | ✅ | N/A reason | ... |
| ... | ... | ... | ... |

Coverage: N ✅ / N N/A / N ⏭️ / N unfilled

Legend: ✅ = covered, N/A = not applicable (with reason), ⏭️ = intentionally skipped (with reason), empty = not evaluated

---

### 3. Failures

| # | Test name | Category | Severity | Error | Screenshot |
|---|-----------|----------|----------|-------|------------|
| ... | ... | ... | ... | ... | ... |

(Empty table if no failures)

---

### 4. Regression Baseline

- Screenshots: N captured ({list})
- Comparison: {first run / N diffs found}

---

### 5. Recommendations

1. {actionable recommendation}
2. {actionable recommendation}
```
