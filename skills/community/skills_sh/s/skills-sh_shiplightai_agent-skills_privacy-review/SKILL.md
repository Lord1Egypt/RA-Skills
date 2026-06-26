---
name: privacy-review
description: "Privacy review and testing: evaluate PII handling, data flows, tracking inventory, consent mechanisms, storage practices, and data leakage risks with browser-based validation against GDPR, CCPA, and industry best practices."
---

# Privacy Review

Evaluate how your application handles personal data — where it's collected, processed, stored, transmitted, and potentially leaked. This review catches privacy issues that code review alone misses: runtime data flows, third-party tracking, console/network leaks, and consent implementation gaps.

## When to use

Use `/privacy-review` when:
- Your app collects any personal information (names, emails, addresses, etc.)
- Before launching in GDPR/CCPA jurisdictions
- Adding third-party analytics, tracking, or marketing tools
- After a data incident or privacy complaint
- Building features that handle sensitive data (health, financial, biometric)
- Integrating with third-party APIs that receive user data

## Standards Referenced

- **GDPR** — EU General Data Protection Regulation (Articles 5, 6, 7, 12-22, 25, 32)
- **CCPA/CPRA** — California Consumer Privacy Act
- **OWASP Privacy Risks Top 10**
- **NIST Privacy Framework**
- **ISO 27701** — Privacy Information Management
- **ePrivacy Directive** — Cookie consent requirements

## Phase Overview

```
Phase 1: EDUCATE   → Privacy principles and what we check
Phase 2: SCOPE     → Map data flows, PII types, third parties
Phase 3: ANALYZE   → Browser-based validation of privacy practices
Phase 4: REPORT    → Findings with evidence and confidence scores
Phase 5: REMEDIATE → Fix guidance + YAML regression tests
```

---

## Phase 1: Educate

> **Why this matters:** GDPR fines reached €2.1B in 2023. CCPA gives consumers the right to sue for data breaches ($100-$750 per consumer per incident). Beyond compliance, privacy violations erode user trust — 79% of consumers say they'd stop engaging with a brand after a privacy breach. Many privacy issues are invisible in code review but obvious in runtime behavior.

This review focuses on observable runtime privacy behavior — what actually happens in the browser when users interact with your app.

---

## Phase 2: Scope

### Gather context

1. **Auto-detect from codebase:**
   - Forms that collect user input (registration, profile, payment, contact)
   - Analytics/tracking scripts (Google Analytics, Mixpanel, Segment, Hotjar, etc.)
   - Cookie-setting code and cookie consent mechanisms
   - Logging statements that might include PII
   - API calls that transmit user data
   - Third-party SDKs and their data sharing behavior
   - Privacy policy and terms of service pages

2. **Ask the user** (one at a time):
   - **Target URL**: Where is the app running?
   - **Data types**: What personal data does your app collect? (auto-detected, confirm)
   - **Jurisdictions**: Where are your users? (determines GDPR/CCPA/other applicability)
   - **Third parties**: What analytics/tracking/marketing tools do you use? (auto-detected, confirm)
   - **Known concerns**: Any specific privacy areas you're worried about? (optional)

3. **Build data flow map:**
   - PII entry points (forms, URL params, imports)
   - PII processing (client-side or server-side)
   - PII storage (cookies, localStorage, server DB)
   - PII transmission (API calls, third-party scripts)
   - PII display (profile pages, admin panels, logs)

---

## Phase 3: Analyze

Open a browser session with `new_session` using `record_evidence: true`. Run all applicable check categories.

### Category A: Data Collection & Consent (CON)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| CON-01 | Cookie consent banner shown before setting non-essential cookies | ePrivacy / GDPR Art.7 | Load page, check if tracking cookies exist before consent |
| CON-02 | No tracking scripts fire before consent | ePrivacy / GDPR | Monitor network requests on fresh page load (no consent given) |
| CON-03 | Consent is granular (not just "accept all") | GDPR Art.7 | Check consent UI for category-level options |
| CON-04 | Rejecting consent actually prevents tracking | GDPR Art.7 | Reject all, verify no tracking cookies/requests |
| CON-05 | Consent preference is persisted and respected | GDPR Art.7 | Set preference, reload page, verify it's remembered |
| CON-06 | Consent can be withdrawn (modify/revoke) | GDPR Art.7(3) | Find mechanism to change consent after initial choice |
| CON-07 | Privacy policy is accessible and linked | GDPR Art.12-14 | Check for privacy policy link in footer/consent banner |
| CON-08 | Data collection is proportionate (no unnecessary fields) | GDPR Art.5(1)(c) | Review forms for fields not needed for stated purpose |

**Browser validation:** Load page in fresh session (no cookies). Use `get_browser_console_logs` and monitor network via JavaScript. Check cookies before and after consent interaction. Use `act` to interact with consent banner.

### Category B: PII Leakage Detection (LEAK)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| LEAK-01 | No PII in URL parameters | OWASP Privacy #1 | Check URLs after form submissions, navigation |
| LEAK-02 | No PII in browser console logs | OWASP Privacy #4 | Check `get_browser_console_logs` for email, names, IDs |
| LEAK-03 | No PII in localStorage/sessionStorage | Data minimization | Inspect client storage for personal data |
| LEAK-04 | No PII in page source/comments | Information leak | Check HTML comments, hidden fields |
| LEAK-05 | No PII in error messages | OWASP Privacy #7 | Trigger errors, check for user data in messages |
| LEAK-06 | No PII in Referer headers | OWASP Privacy | Check Referrer-Policy, inspect outbound requests |
| LEAK-07 | No PII in meta tags or Open Graph | Information leak | Check `<meta>` for user-specific data on shared pages |
| LEAK-08 | No PII in cached responses (browser cache) | Data minimization | Check Cache-Control headers on pages with PII |
| LEAK-09 | No PII leaked to third-party scripts | GDPR Art.28 | Monitor data sent to analytics/tracking endpoints |
| LEAK-10 | Autocomplete appropriate on sensitive fields | Usability/Privacy | Check `autocomplete` attribute on password, CC fields |

**Browser validation:** Navigate through user flows. After each action, check URLs, console logs, storage, and network requests for PII patterns (email regex, phone patterns, SSN patterns, etc.). Use JavaScript to inspect `performance.getEntries()` for request URLs.

### Category C: Third-Party Tracking Inventory (TRACK)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| TRACK-01 | Inventory all third-party scripts | GDPR Art.30 | List all external script sources and their domains |
| TRACK-02 | All third-party scripts are documented | Transparency | Cross-reference with privacy policy |
| TRACK-03 | No unknown/unexpected tracking pixels | Privacy | Check for 1x1 images, beacon requests |
| TRACK-04 | Third-party cookies inventory | ePrivacy | List all cookies by domain |
| TRACK-05 | No fingerprinting scripts | Privacy | Check for canvas fingerprint, WebGL, AudioContext probing |
| TRACK-06 | Data sent to third parties is proportionate | GDPR Art.5(1)(c) | Inspect payloads to analytics endpoints |
| TRACK-07 | Tracking respects Do-Not-Track header | Best practice | Set DNT header, check if tracking still fires |

**Browser validation:** Load page with fresh session. Use JavaScript to enumerate all `<script>` sources, all cookie domains, all network requests to external domains. Check for fingerprinting API usage (Canvas, WebGL, AudioContext).

### Category D: Data Storage & Retention (STOR)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| STOR-01 | Sensitive data encrypted in transit (HTTPS) | GDPR Art.32 | Check all resource URLs use HTTPS |
| STOR-02 | Session data has appropriate expiry | Data minimization | Check cookie/token expiration times |
| STOR-03 | No excessive data in cookies | Data minimization | Check cookie sizes and contents |
| STOR-04 | Client-side storage is minimal | Data minimization | Audit localStorage/sessionStorage contents |
| STOR-05 | Sensitive form data not persisted in history | Privacy | Check if sensitive forms use POST, not GET |
| STOR-06 | Browser back button doesn't show sensitive data after logout | Session management | Logout, press back, check for cached sensitive content |

**Browser validation:** Inspect all cookies (name, value, domain, expiry, flags). Check localStorage/sessionStorage. Test logout + back button behavior.

### Category E: User Rights Implementation (RIGHTS)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| RIGHTS-01 | Users can access their data (data export) | GDPR Art.15 / CCPA | Find and test data export feature |
| RIGHTS-02 | Users can delete their account/data | GDPR Art.17 | Find and verify account deletion flow |
| RIGHTS-03 | Users can update their personal information | GDPR Art.16 | Test profile edit functionality |
| RIGHTS-04 | Opt-out mechanism for data selling (CCPA) | CCPA §1798.120 | Check for "Do Not Sell" link |
| RIGHTS-05 | Account deletion is complete (not just deactivation) | GDPR Art.17 | Delete account, verify data is removed (check profile URL) |

**Browser validation:** Navigate to account settings, test data export, profile editing, and account deletion flows. Verify each right is accessible and functional.

---

## Phase 4: Report

Generate a structured report saved to `shiplight/reports/privacy-review-{date}.md`:

```markdown
# Privacy Review Report
**Date:** {date}
**URL:** {url}
**PII types handled:** {list}
**Jurisdictions:** {GDPR, CCPA, etc.}
**Third parties detected:** {count and list}

## Overall Score: {X}/10 | Confidence: {X}%

## Score Breakdown
| Category | Score | Findings |
|----------|-------|----------|
| Consent (CON) | 5/10 | 1 critical, 2 high |
| PII Leakage (LEAK) | 7/10 | 1 high, 1 medium |
| Tracking Inventory (TRACK) | 4/10 | 2 high, 1 medium |
| Data Storage (STOR) | 8/10 | 1 medium |
| User Rights (RIGHTS) | 6/10 | 1 high, 1 medium |

## Data Flow Map
(visual representation of PII flows through the application)

## Third-Party Tracking Inventory
| Domain | Type | Cookies Set | Data Sent | Consent Required |
|--------|------|-------------|-----------|-----------------|
| google-analytics.com | Analytics | _ga, _gid | Page URL, user agent | Yes |
| ... | | | | |

## Findings
(structured findings with evidence, severity, confidence)
```

### Confidence Scoring
- **90-100%**: Browser-validated — observed PII in console, URL, or network request
- **70-89%**: Strong evidence from storage/header inspection
- **50-69%**: Code-level pattern match, may not manifest at runtime
- **Below 50%**: Don't report

---

## Phase 5: Remediate

### 1. Fix guidance (example)
```markdown
#### LEAK-01: Email address in URL parameter after form submit
**Risk:** PII in URL is logged by servers, proxies, browser history, and analytics
**File:** src/pages/search.tsx:34
**Current:** `router.push(`/results?email=${email}`)`
**Fix:** Use POST request or session state
- `router.push('/results')` with email in request body or session
- Add `Referrer-Policy: no-referrer` header as defense-in-depth
```

### 2. YAML regression test
```yaml
- name: leak-01-no-pii-in-urls
  description: Verify email addresses are not exposed in URL parameters
  severity: high
  standard: OWASP-Privacy-1
  steps:
    - URL: /search
    - intent: Enter email in search form
      action: fill
      locator: "getByLabel('Email')"
      value: "test@example.com"
    - intent: Submit the search form
      action: click
      locator: "getByRole('button', { name: 'Search' })"
    - WAIT_UNTIL: Search results are displayed
      timeout_seconds: 15
    - description: Assert no email address appears in the URL
      js: |
        const url = page.url();
        if (/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/.test(url)) {
          throw new Error(`PII found in URL: ${url}`);
        }
    - VERIFY: No email addresses appear in the browser URL
```

Save all YAML tests to `shiplight/tests/privacy-review.test.yaml`.

---

## Tips

- Use a fresh browser session (no stored cookies) to test consent behavior accurately
- PII patterns to search for: email (`@`), phone (`\d{3}[-.]?\d{3}[-.]?\d{4}`), SSN, credit card numbers, names from test accounts
- Third-party scripts often load more scripts — check for cascade loading
- `get_browser_console_logs` often reveals PII that developers left in debug logging
- Test with consent rejected AND accepted — both paths matter
- Close session with `close_session` and use `generate_html_report` for evidence
