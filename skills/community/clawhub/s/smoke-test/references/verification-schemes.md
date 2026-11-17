# Verification Schemes (V1–V11)

Detailed reference for the 11 internal verification schemes used in the QA workflow. Each scheme includes purpose, tool, method, and what class of defect it detects.

---

## V1: DOM Text Assertion

**Tool**: Playwright `page.evaluate()` — direct DOM read, not OCR

**Method**: Read `.metric-value`, `.metric-sub`, `.metric-card` element textContent from each view. Assert numeric values against expected API truth.

**Pattern**:
```js
const metrics = await page.evaluate(() =>
  Array.from(document.querySelectorAll('#view-dashboard .metric-value'))
    .map(e => e.textContent.trim())
);
```

**Catches**: wrong values, NaN displays, placeholder strings, formatting errors (missing `%`/`¥`), swapped labels.

**Precision**: Much more accurate than OCR-based screenshot verification—text comparison is exact.

---

## V2: Forbidden String Scanning

**Tool**: `innerText.includes()` on each view's root element

**Method**: Maintain a list of known bug-signature strings from past defects. Scan every view's full text content.

**Pattern**:
```js
const FORBIDDEN = ['12300%', 'NaN%', 'undefined%', '-NaN'];
const fullText = view.innerText.replace(/\s+/g, ' ');
const hits = FORBIDDEN.filter(f => fullText.includes(f));
```

**Catches**: regression of previously-fixed defects (e.g., 100× inflation producing `12300%` instead of `123.00%`).

**Rule**: 0 hits = pass. Any hit = fail and requires root cause investigation.

---

## V3: Screenshot Evidence Chain

**Tool**: `page.screenshot({ path: 'shots/reg_viewname.png' })`

**Method**: Screenshot every view during each test round. Compare visually and embed in reports as base64.

**Catches**: layout issues, missing charts/table rows, incorrectly rendered modals, color/theme problems.

**Best practice**: Always take "before-fix" and "after-fix" screenshots of the same view for report comparison.

---

## V4: API Truth Comparison

**Tool**: `curl` or Node.js `fetch()` to backend API endpoints

**Method**: For every metric displayed on screen, fetch the raw API response and compare values:
- Screen shows `-12.50%` → API returns `max_drawdown: 12.5` → correct (drawdown magnitude)
- Screen shows `+8.30%` → API returns `return_1m: 8.3` → correct (percent value)

**Catches**: 100× inflation (`8.3` on screen → `830%`), data-source mismatch (wrong endpoint feeding wrong data), truncation/rounding errors.

---

## V5: Function Probe + Runtime Source Verification

**Tool**: `typeof window.fn === 'function'` and `window.fn.toString()`

**Method**:
1. Probe: verify every `onclick="fn()"` referenced function exists globally
2. Source: read the actual function source at runtime to confirm which file's implementation is loaded

**Pattern**:
```js
// Probe check
const missing = onclickFns.filter(f => typeof window[f] !== 'function');

// Runtime source verification (diagnose loader competition)
const src = await page.evaluate(() => window.loadReportData.toString());
// Check if it calls 'reports/status' (wrong) or 'reports/summary' (correct)
```

**Catches**: IIFE-closure-trapped functions, overwritten fix functions (multi-loader competition), wrong API endpoint routing.

---

## V6: Console / Page Error / Network Monitoring

**Tool**: Playwright event listeners

**Method**: Collect errors globally across the entire test session.

**Pattern**:
```js
const consoleErrors = [];
const pageErrors = [];
page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
page.on('pageerror', e => pageErrors.push(e.message));
page.on('requestfailed', r => networkFails.push(r.url()));
```

**Catches**: ReferenceError, 404s on API calls, CORS issues, uncaught promises.

**Passing standard**: `consoleErrors.length === 0` and `pageErrors.length === 0` and `networkFails.length === 0`.

---

## V7: Concurrent Stress Testing

**Tool**: Custom perf probe script sending parallel requests

**Method**: Fire 16+ concurrent HTTP requests to backend endpoints and measure total time, timeout count.

**Pattern**:
```js
const start = Date.now();
const results = await Promise.all(urls.map(async url => {
  try {
    await page.evaluate(u => fetch(u, { signal: AbortSignal.timeout(15000) }), url);
    return 'ok';
  } catch { return 'timeout'; }
}));
const elapsed = Date.now() - start;
```

**Catches**: event-loop blocking regression (sync I/O in async handlers), single-worker bottlenecks.

**Passing standard**: 0 timeouts, all requests complete under a reasonable total time.

---

## V8: Protocol Consistency Audit

**Tool**: Custom Python/Node script comparing OpenAPI schema vs frontend source

**Method**:
1. Fetch `/openapi.json` from the backend
2. Parse all write endpoints: required fields, enum values, parameter types
3. Scan frontend JS source for all `tdAPI.post(path, body)` calls
4. Compare body fields against schema

**Catches**: missing required field on a write endpoint, wrong enum value (e.g., `"stop"` instead of `"halt"`), type mismatches.

**Goal**: 0 mismatches. Run as part of regression for every fix round that changes API.

---

## V9: DB Snapshot Restore

**Tool**: Shell commands via SSH — stop service, copy DB files, restart

**Method**:
1. **Before destructive tests**: stop backend, `cp` sqlite `.db` + config `.json` to `data/backups/round_N/`
2. **After tests**: stop backend, copy backup files back, restart
3. **Verify**: query restored baseline (cash, positions, order count) matches pre-test state

**Catches**: test-induced data pollution, incomplete restore, missing backup files.

**Best practice**: Always include a "pre-snapshot → test → post-snapshot → restore → verify" cycle in every round of C-level destructive testing.

---

## V10: Degraded-Mode Banner Verification

**Tool**: DOM inspection of a specific banner element

**Method**: The frontend should show a visible banner (`#degraded-banner` or equivalent) whenever data is served from mock/fallback instead of live API. Verify:
1. Banner is hidden when live API is healthy
2. Banner appears after a failed API request
3. Banner auto-hides when live API recovers

**Catches**: silent mock-data fallback that makes users believe they see real data when they don't.

---

## V11: Pre/Post State Assertion

**Tool**: DOM read + API query before and after each destructive action

**Method**: For C-level operations (buy, sell, cancel, liquidate):
1. Record pre-action state (order count, position count, cash balance) via API
2. Execute the action via UI
3. Record post-action state via API
4. Assert: expected delta = actual delta

**Example**: Buy 100 shares of ticker X → orders count increases by 1, available cash decreases by ~price×quantity

**Catches**: operations that appear successful in UI but don't actually reach the backend, partial failures.

---

## Tool Selection Guide

| Suspicion | Use |
|-----------|-----|
| "Numbers look wrong on screen" | V1 + V4 |
| "An old bug might be back" | V2 |
| "Not sure which code is running" | V5 |
| "Layout looks broken" | V3 |
| "Something failing silently" | V6 |
| "API calls timing out" | V7 |
| "Protocol mismatch between front/back" | V8 |
| "Need clean test environment" | V9 |
| "Users seeing stale/mock data" | V10 |
| "Did the operation actually work?" | V11 |
