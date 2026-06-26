# Reach Agent Web Interface — Real-World Test Report

**Date**: 2026-03-21
**Tester**: Ollie (automated)
**Environment**: WSL2 / Node 22 / Playwright 1.58.2

---

## Summary

**5 PASS / 5 FAIL out of 10 tests**

| # | Test | Status | Notes |
|---|------|--------|-------|
| 1 | fetch — HTTP read | PASS | Base docs fetched via HTTP, 4053 chars markdown |
| 2 | fetch — JS page | PASS | Cantina competitions via browser, 856 chars, correct data |
| 3 | authenticate — Cantina login | FAIL | Could not find email input (navigated to homepage, not login page) |
| 4 | act — Click and navigate | FAIL | Found "Competitions" text but in hidden breadcrumb span, not clickable |
| 5 | sign — Sign message | FAIL | No PRIVATE_KEY in .env |
| 6 | persist/recall | PASS | Store and retrieve works correctly |
| 7 | Router — Routing decisions | PASS | Correct routing for all 3 URLs (uses sites.json learning) |
| 8 | CLI — Command line | PASS | fetch, store, recall, sessions all work |
| 9 | Full workflow — Auth + navigate | NOT RUN | Blocked by Test 3 failure |
| 10 | Screenshot | PASS | Saved to data/screenshots/example.com-*.png, verified correct |

---

## Detailed Results

### Test 1: fetch — Read a webpage (HTTP) — PASS

Fetched `https://docs.base.org` via HTTP (no browser needed). Returned 4053 chars of markdown including navigation structure, headings, and links. `htmlToMarkdown` conversion works but output includes some navigation clutter. The content is usable.

**Source**: http
**Format**: markdown

### Test 2: fetch — JavaScript-required page — PASS

Fetched `https://cantina.xyz/competitions` with `javascript: true`. Browser rendered the React SPA correctly. Returned actual competition data: payouts ($46M available), vulnerability count (7,160), researcher count (12,894), and individual competition listings with names, amounts, and status.

**Source**: browser
**Format**: markdown (innerText extraction)

### Test 3: authenticate — Login to Cantina — FAIL

**Error**: `Could not find email input field`

**Root cause**: Two issues:
1. The `authenticate` API signature is `authenticate(service, method, credentials)` but the test passed the full URL as `service`. The function treated `https://cantina.xyz` as the service name and used it as the domain for cookie storage.
2. Cantina's login flow requires first clicking "Sign in" on the homepage to open the login modal/page. The `authWithLogin` function navigated to the homepage URL and immediately tried to find `input[type="email"]`. The homepage doesn't have a visible email field — it's behind the "Sign in" button.

**Fix needed**: The `authWithLogin` function needs to either:
- Accept a separate login page URL (not homepage)
- Or detect "Sign in" / "Log in" buttons and click them first before looking for input fields

**Screenshot**: `data/screenshots/auth-fail-https:/cantina.xyz-*.png` shows the Cantina homepage with "Sign in" button visible in the top nav.

### Test 4: act — Click and navigate — FAIL

**Error**: `Timeout 30000ms exceeded` — element found but not visible

**Root cause**: Playwright found `text=Competitions` matching a hidden `<span>` inside a breadcrumb component (`chakra-breadcrumb__link`), not the visible page element. The locator `text=Competitions` with `.first()` grabbed the first match (the breadcrumb) which was CSS-hidden.

**Fix needed**: The `doClick` function should use a more targeted locator strategy:
- Prefer visible elements: `page.locator('text=Competitions').filter({ visible: true }).first()`
- Or use `getByRole` for semantic matching: `page.getByRole('link', { name: 'Competitions' })`

### Test 5: sign — Sign a message — FAIL

**Error**: `No private key provided. Set PRIVATE_KEY env var or pass privateKey option.`

**Root cause**: The `.env` file has no `PRIVATE_KEY` or `DEPLOYMENT_KEY` variable set. This is by design (don't store private keys unnecessarily), but the test should have passed a key explicitly.

**Not a bug in Reach** — the error message is clear and correct. To fix: either add `PRIVATE_KEY` to `.env` or pass `privateKey` in options.

### Test 6: persist/recall — State storage — PASS

Stored `{ hello: 'world', timestamp: ... }` under key `test_key`. Recalled it back correctly. TTL system and JSON serialization both work. Files stored at `data/state/test_key.json`.

### Test 7: Router — Routing decisions — PASS

All three routes returned correct decisions:
- **Twitter API** (`api.twitter.com`): routed to `fetch` via `http` layer (default, no special config)
- **Cantina** (`cantina.xyz`): routed to `fetch` via `browser` layer with `javascript: true` (learned from sites.json: `needsJS: true`)
- **Base docs** (`docs.base.org`): routed to `fetch` via `http` layer (default)

The router correctly uses learned site info from `data/sites.json`.

### Test 8: CLI — Command line — PASS

All CLI commands work:
- `reach fetch https://example.com --format markdown` — fetched and displayed (fell back to browser due to TLS cert issue in WSL2)
- `reach store test_value "hello from CLI"` — stored successfully
- `reach store test_value` (recall) — returned "hello from CLI"
- `reach sessions` — listed 4 saved sessions (test-service, cantina.xyz, example.com, httpbin.org)

**Note**: HTTP fetch of example.com failed with `unable to get local issuer certificate` (WSL2 TLS issue), automatically fell back to browser. The fallback works correctly.

### Test 9: Full workflow — NOT RUN

Blocked by Test 3 (authenticate) failure. Cannot test authenticated navigation without a working login flow.

### Test 10: Screenshot — PASS

Screenshot of `https://example.com` saved to `data/screenshots/example.com-1774132483493.png`. File is 22KB, shows the Example Domain page correctly rendered at 1920x1080 viewport.

---

## Issues Found (by severity)

### High — Fix before using in production

1. **authenticate login flow doesn't handle "Sign in" button clicks** — It assumes the login URL already has email/password fields visible. Most modern sites have a "Sign in" button that opens a modal or navigates to a login page. The function should try clicking common sign-in buttons before looking for input fields.

2. **act click matches hidden elements** — The `text=` locator grabs the first DOM match including hidden/invisible elements. Should filter to visible elements only.

### Medium — Should fix

3. **authenticate passes URL as service name** — When called with `authenticate('https://cantina.xyz', ...)`, the service name becomes the full URL. Cookies are saved as `cookies-https:/cantina.xyz.json` which creates filesystem issues (colon in filename). Should extract domain automatically.

4. **HTTP fetch TLS errors in WSL2** — `node-fetch` fails on sites with certain certificate chains. The browser fallback works but adds ~3s latency. Could set `NODE_TLS_REJECT_UNAUTHORIZED=0` for non-sensitive fetches or use the system cert store.

### Low — Nice to have

5. **htmlToMarkdown is lossy** — Navigation, footers, and boilerplate are included in markdown output. A smarter extraction (Readability.js or similar) would improve content quality.

6. **No PRIVATE_KEY in .env** — The sign primitive works but needs a key to test. Consider documenting which env vars are required.

---

## What Works Well

- **Smart fallback**: HTTP-first with automatic browser fallback is the right pattern
- **Browser pool**: Singleton browser, per-domain contexts, cookie persistence all solid
- **Router learning**: sites.json memory means the router gets smarter over time
- **CLI**: Clean interface, good help text, all commands functional
- **Persist/recall**: Simple, reliable, TTL support
- **Screenshot**: Just works
- **Anti-detection**: User agent, webdriver flag removal, viewport settings

## Architecture Notes

The 7-primitive design is clean. The router is simple but effective. The main gap is the authenticate primitive — modern auth flows (OAuth, SSO, multi-step) need more sophistication than "find email input, find password input, click submit."
