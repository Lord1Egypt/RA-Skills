---
name: resilience-review
description: "Resilience review and testing: evaluate error handling, graceful degradation, API contract compliance, edge cases, and failure recovery with browser-based fault injection and validation."
---

# Resilience Review

Evaluate how your application behaves when things go wrong — network failures, API errors, slow connections, missing data, and edge cases. Most apps are built for the happy path; this review systematically tests the unhappy paths that real users encounter.

## When to use

Use `/resilience-review` when:
- Before launching a user-facing feature
- After adding new API integrations or data sources
- When reliability is critical (healthcare, finance, e-commerce checkout)
- After production incidents caused by unhandled errors
- When moving from prototype to production quality

## Standards Referenced

- **Google SRE Principles** — Error budgets, graceful degradation
- **Netflix Chaos Engineering Principles** — Verify steady state, inject real-world failures
- **OWASP Error Handling** — Secure and user-friendly error responses
- **Nielsen Norman Group** — Error message usability heuristics

## Phase Overview

```
Phase 1: EDUCATE   → Why resilience matters and what we test
Phase 2: SCOPE     → Map failure points, dependencies, critical flows
Phase 3: ANALYZE   → Browser-based fault injection and edge case testing
Phase 4: REPORT    → Findings with evidence and user impact assessment
Phase 5: REMEDIATE → Fix guidance + YAML regression tests
```

---

## Phase 1: Educate

> **Why this matters:** Users don't experience your app in ideal conditions. 53% of mobile visits are abandoned if a page takes >3 seconds. Error pages with no guidance increase support tickets 5x. A blank screen is the worst possible failure mode — it tells the user nothing and offers no recovery path. Resilient apps maintain trust even when backend systems fail.

This review simulates real-world failure conditions in the browser and evaluates how your UI responds.

---

## Phase 2: Scope

### Gather context

1. **Auto-detect from codebase:**
   - API calls and their endpoints
   - Error boundary components (React ErrorBoundary, Vue errorHandler)
   - Loading state implementations (spinners, skeletons, suspense)
   - Empty state components
   - Retry logic / error recovery patterns
   - Offline support (service workers, cache strategies)
   - Third-party service dependencies

2. **Ask the user** (one at a time):
   - **Target URL**: Where is the app running?
   - **Critical user flows**: Which flows must never show a blank screen? (auto-detect from routes)
   - **Key API dependencies**: Which APIs does the frontend depend on? (auto-detected)
   - **Known fragile areas**: Any pages/features that break frequently? (optional)

3. **Map failure points:**
   - API endpoints the frontend calls (and what happens if each fails)
   - Third-party dependencies (CDN, auth provider, analytics, maps, payment)
   - Data-dependent UI (what shows when data is empty, missing, or malformed)
   - User input edge cases (long text, special characters, empty submissions)

---

## Phase 3: Analyze

Open a browser session with `new_session` using `record_evidence: true`. Run all applicable check categories.

### Category A: Error Handling (ERR)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| ERR-01 | API errors show user-friendly message (not blank screen) | UX best practice | Mock API to return 500, check UI response |
| ERR-02 | Network timeout shows appropriate state | UX best practice | Mock network delay (30s), check UI |
| ERR-03 | 404 page exists and is helpful | UX best practice | Navigate to non-existent route |
| ERR-04 | JavaScript errors don't crash the page | Error boundaries | Inject JS error, check if page recovers |
| ERR-05 | Error messages are actionable | NN/g heuristics | Check error messages for: what happened, why, what to do |
| ERR-06 | Errors don't expose technical details | OWASP | Check error messages for stack traces, SQL, internal paths |
| ERR-07 | Form validation errors are clear and positioned | UX best practice | Submit invalid forms, check error placement and text |
| ERR-08 | Error states allow retry without page refresh | UX best practice | After error, check for retry button or recovery action |
| ERR-09 | Concurrent error handling (multiple simultaneous failures) | Resilience | Mock multiple API failures, check UI doesn't cascade |
| ERR-10 | Error logging doesn't expose PII | OWASP / Privacy | Check `get_browser_console_logs` during errors |

**Browser validation:** Use `description: + js:` statements to intercept network requests via `page.route()` to simulate failures. Check UI state after each failure. Use `get_browser_console_logs` for JavaScript errors.

```javascript
// Example: Mock API 500 error
await page.route('**/api/**', route => {
  route.fulfill({ status: 500, body: JSON.stringify({ error: 'Internal Server Error' }) });
});
```

### Category B: Graceful Degradation (DEG)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| DEG-01 | Page works with JavaScript disabled (basic content) | Progressive enhancement | Disable JS, check if content is accessible |
| DEG-02 | Page works on slow connection (3G simulation) | Performance | Throttle to Slow 3G, check load behavior |
| DEG-03 | Non-critical features degrade without breaking critical ones | Graceful degradation | Disable third-party scripts, check core functionality |
| DEG-04 | Offline state is handled (if applicable) | PWA best practice | Go offline, check UI state and messaging |
| DEG-05 | Third-party service failure doesn't block page load | Resilience | Block third-party domains, check page loads |
| DEG-06 | Image loading failure shows fallback | UX best practice | Block image URLs, check for alt text/placeholder |
| DEG-07 | Font loading failure doesn't hide text | FOUT handling | Block font URLs, check text remains visible |
| DEG-08 | Feature detection over browser sniffing | Progressive enhancement | Check code for `navigator.userAgent` vs feature detection |

**Browser validation:** Use `page.route()` to block specific resources. Use CDP to simulate network conditions. Disable JavaScript via browser settings. Verify each degradation scenario.

### Category C: Empty & Edge States (EDGE)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| EDGE-01 | Empty data state shows helpful message | UX best practice | Navigate to pages with no data, check display |
| EDGE-02 | Pagination handles zero results | UX best practice | Search for nonexistent term, check pagination |
| EDGE-03 | Long text doesn't break layout | Defensive CSS | Enter very long strings (500+ chars), check overflow |
| EDGE-04 | Special characters in input don't break UI | Input handling | Enter `<script>`, `"'&<>`, emoji, Unicode |
| EDGE-05 | Large data sets don't freeze UI | Performance | Load pages with maximum data, check responsiveness |
| EDGE-06 | Rapid user actions don't cause duplicate submissions | State management | Double-click submit buttons, rapid nav |
| EDGE-07 | Back/forward navigation maintains state | History management | Fill form, navigate away, come back |
| EDGE-08 | Refresh preserves expected state | State persistence | Refresh during multi-step flow, check state |
| EDGE-09 | Concurrent tab/session behavior | Session management | Open same page in two tabs, perform actions |
| EDGE-10 | Maximum file upload size handled | Input validation | Upload oversized file, check error message |

**Browser validation:** Navigate to pages and test each edge case. Use `act` to interact with forms, submit empty/extreme data. Use JavaScript to check for UI overflow, frozen states.

### Category D: API Contract & Data Handling (API)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| API-01 | UI handles all HTTP error codes gracefully | API contract | Mock 400, 401, 403, 404, 422, 429, 500, 503 |
| API-02 | UI handles null/undefined fields without crashing | Defensive coding | Mock API response with null fields |
| API-03 | UI handles empty arrays/objects | Defensive coding | Mock API response with empty collections |
| API-04 | UI handles unexpected data types | Defensive coding | Mock API response with wrong types |
| API-05 | Loading states shown during API calls | UX best practice | Add 2s delay to API, verify loading indicator |
| API-06 | Race conditions handled (stale responses) | State management | Trigger rapid sequential requests, verify latest wins |
| API-07 | Rate limiting (429) handled with user feedback | API contract | Mock 429 response, check UI feedback |
| API-08 | Authentication expiry handled mid-session | Session management | Mock 401 during session, check redirect to login |

**Browser validation:** Use `page.route()` to mock each response scenario. Verify UI state after each mock.

### Category E: Recovery & User Communication (REC)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| REC-01 | Retry mechanisms exist for transient failures | Resilience | Mock intermittent failure, check auto-retry |
| REC-02 | User can manually retry after failure | UX best practice | After error, verify retry action available |
| REC-03 | Progress is not lost on errors | UX best practice | Fill long form, trigger error, check data persists |
| REC-04 | User is informed of degraded functionality | Communication | When features fail, check for degradation notice |
| REC-05 | Recovery actions are clear and accessible | NN/g heuristics | After each error type, evaluate recovery UX |
| REC-06 | Status indicators for background operations | UX best practice | Start async operation, verify progress feedback |

**Browser validation:** Use fault injection then verify recovery paths.

---

## Phase 4: Report

Generate a structured report saved to `shiplight/reports/resilience-review-{date}.md`:

```markdown
# Resilience Review Report
**Date:** {date}
**URL:** {url}
**Critical flows tested:** {list}
**API dependencies tested:** {count}
**Failure scenarios simulated:** {count}

## Overall Score: {X}/10 | Confidence: {X}%

## Score Breakdown
| Category | Score | Findings |
|----------|-------|----------|
| Error Handling (ERR) | 5/10 | 2 critical, 1 high |
| Graceful Degradation (DEG) | 6/10 | 1 high, 2 medium |
| Empty & Edge States (EDGE) | 4/10 | 1 critical, 3 high |
| API Contract (API) | 7/10 | 1 high, 1 medium |
| Recovery (REC) | 3/10 | 2 high, 1 medium |

## Failure Matrix
| Failure Scenario | Expected Behavior | Actual Behavior | Status |
|-----------------|-------------------|-----------------|--------|
| API returns 500 | Error message + retry | Blank screen | FAIL |
| Network timeout | Loading → timeout message | Infinite spinner | FAIL |
| Empty data set | "No results" message | Blank page | FAIL |
| ... | | | |

## Findings
(structured findings with evidence, screenshots of failure states)
```

### Confidence Scoring
- **90-100%**: Fault injected and failure behavior verified in browser
- **70-89%**: Code analysis shows missing error handling, not validated at runtime
- **50-69%**: Pattern-based assessment (e.g., no error boundary detected)
- **Below 50%**: Don't report

---

## Phase 5: Remediate

### 1. Fix guidance (example)
```markdown
#### ERR-01: API error shows blank screen instead of error message
**Impact:** Users see empty page, think app is broken, leave
**File:** src/pages/Dashboard.tsx:45
**Current:** `const data = await fetch('/api/data').then(r => r.json())`
**Problem:** No error handling — fetch throws on network error, .json() throws on non-JSON response
**Fix:**
- Wrap in try/catch
- Add error state: `const [error, setError] = useState(null)`
- Render error UI with retry button
- Add React Error Boundary as fallback
```

### 2. YAML regression test
```yaml
- name: err-01-api-error-shows-message
  description: Verify API failure shows user-friendly error message instead of blank screen
  severity: critical
  standard: UX-Error-Handling
  steps:
    - description: Mock the data API to return a 500 error
      js: |
        await page.route('**/api/data**', route => {
          route.fulfill({
            status: 500,
            contentType: 'application/json',
            body: JSON.stringify({ error: 'Internal Server Error' })
          });
        });
    - URL: /dashboard
    - WAIT_UNTIL: Page has finished attempting to load data
      timeout_seconds: 15
    - VERIFY: An error message is visible explaining that data could not be loaded
    - VERIFY: A retry button or recovery action is available to the user
    - VERIFY: The page is NOT blank — navigation and header are still visible
```

Save all YAML tests to `shiplight/tests/resilience-review.test.yaml`.

---

## Tips

- Use `page.route()` in `description: + js:` statements — it's the primary tool for fault injection
- Test the most critical user flows first (checkout, signup, core feature)
- A blank screen is always a CRITICAL finding — it's the worst failure mode
- Check `get_browser_console_logs` for uncaught promise rejections — they indicate missing error handling
- Edge case testing (EDGE category) often reveals the most bugs per minute spent
- Close session with `close_session` and use `generate_html_report` for evidence
