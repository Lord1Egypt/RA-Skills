---
name: security-review
description: "Security review and penetration testing: evaluate your application against OWASP Top 10, authentication security, HTTP headers, CORS, CSP, supply chain risks, and common attack vectors with browser-based validation."
---

# Security Review

Evaluate your application's security posture against industry standards and validate findings through browser-based penetration testing. This review covers the attack surface that static analysis tools miss — runtime behavior, header configuration, authentication flows, and client-side vulnerabilities.

## When to use

Use `/security-review` when:
- Before launching a new application or feature
- After adding authentication or authorization changes
- When handling sensitive data (user credentials, payment info, PII)
- Preparing for a security audit
- After a security incident to check for similar issues
- Reviewing third-party integrations

## Standards Referenced

- **OWASP Top 10 (2021)** — Top web application security risks
- **OWASP ASVS v4.0** — Application Security Verification Standard
- **OWASP Session Management Cheat Sheet**
- **NIST 800-63B** — Digital Identity Guidelines (authentication)
- **CWE/SANS Top 25** — Most Dangerous Software Weaknesses
- **Mozilla Observatory** — HTTP security header best practices

## Phase Overview

```
Phase 1: EDUCATE   → Security context and what we check
Phase 2: SCOPE     → Identify attack surface, auth mechanisms, data flows
Phase 3: ANALYZE   → Automated checks + browser-based penetration testing
Phase 4: REPORT    → Findings with evidence, CVE references, confidence scores
Phase 5: REMEDIATE → Fix guidance + YAML regression tests
```

---

## Phase 1: Educate

> **Why this matters:** The average cost of a data breach is $4.45M (IBM 2023). 83% of web applications have at least one critical vulnerability. Many security issues are only detectable at runtime — misconfigured headers, insecure token storage, broken access controls — which is exactly what browser-based testing catches.

This review checks your app against objective security criteria with browser-based validation. Every finding references a specific standard (OWASP, CWE, NIST).

---

## Phase 2: Scope

### Gather context

1. **Auto-detect from codebase:**
   - Authentication mechanism (JWT, sessions, OAuth, API keys)
   - Framework security features in use (CSRF tokens, CORS config, CSP)
   - Dependencies with known vulnerabilities (`npm audit` / `pip audit`)
   - API routes and endpoints
   - Environment variable handling
   - File upload capabilities
   - Third-party scripts and CDN usage

2. **Ask the user** (one at a time):
   - **Target URL**: Where is the app running?
   - **Auth mechanism**: How do users log in? (auto-detected, confirm)
   - **Test credentials**: Do you have test accounts I can use? (needed for authenticated testing)
   - **Sensitive data**: What sensitive data does the app handle? (PII, payments, health records)
   - **Known concerns**: Any specific areas you're worried about? (optional)

3. **Map the attack surface:**
   - List all user input points (forms, URL params, file uploads, WebSocket messages)
   - List all API endpoints with their auth requirements
   - List all third-party integrations
   - Identify data flow: where does sensitive data enter, process, store, and exit?

---

## Phase 3: Analyze

Open a browser session with `new_session` using `record_evidence: true`. Run all applicable check categories.

### Category A: HTTP Security Headers (HDR)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| HDR-01 | Content-Security-Policy header present and restrictive | OWASP A05 | Inspect response headers |
| HDR-02 | Strict-Transport-Security (HSTS) with long max-age | OWASP Transport | Check header presence and value |
| HDR-03 | X-Content-Type-Options: nosniff | Mozilla Observatory | Check header |
| HDR-04 | X-Frame-Options or CSP frame-ancestors | OWASP Clickjacking | Check header |
| HDR-05 | Referrer-Policy set appropriately | Privacy/Security | Check header value |
| HDR-06 | Permissions-Policy restricts sensitive APIs | Browser security | Check camera, microphone, geolocation policies |
| HDR-07 | No Server/X-Powered-By version disclosure | Information leak | Check for version strings in headers |
| HDR-08 | Cache-Control for sensitive pages | OWASP Session | Check no-store for authenticated content |
| HDR-09 | CORS not overly permissive | OWASP A05 | Check Access-Control-Allow-Origin |
| HDR-10 | No mixed content (HTTP resources on HTTPS page) | Transport security | Inspect all resource URLs |

**Browser validation:** Use JavaScript via `act` to inspect `document.querySelector('meta[http-equiv]')` and fetch response headers via a same-origin request. Use `get_browser_console_logs` to check for mixed content warnings.

### Category B: Authentication & Session Management (AUTH)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| AUTH-01 | Tokens not stored in localStorage | OWASP ASVS 3.3.2 | Check localStorage/sessionStorage for tokens |
| AUTH-02 | Session cookies have HttpOnly flag | OWASP Session | Inspect Set-Cookie headers |
| AUTH-03 | Session cookies have Secure flag | OWASP Session | Inspect Set-Cookie headers |
| AUTH-04 | Session cookies have SameSite attribute | OWASP CSRF | Inspect Set-Cookie headers |
| AUTH-05 | Session expires after idle timeout | OWASP ASVS 3.3.1 | Wait and verify session invalidation |
| AUTH-06 | Logout invalidates server-side session | OWASP ASVS 3.3.1 | Logout, replay old token, check response |
| AUTH-07 | Password reset tokens are single-use | OWASP Auth | Use reset link twice, verify second fails |
| AUTH-08 | No credentials in URL parameters | OWASP Transport | Check URL for tokens/passwords |
| AUTH-09 | Brute force protection on login | OWASP Auth | Attempt multiple failed logins, check for lockout/rate-limit |
| AUTH-10 | CSRF protection on state-changing requests | OWASP A01 | Submit forms without CSRF token |
| AUTH-11 | JWT signature verified (if applicable) | OWASP Auth | Send modified JWT, check rejection |
| AUTH-12 | OAuth state parameter used (if applicable) | OWASP Auth | Check OAuth flow for state param |

**Browser validation:** Log in via `act`, inspect cookies with JavaScript (`document.cookie` — HttpOnly cookies won't appear, which is correct). Check localStorage. Perform logout, replay requests. Attempt brute force (5 wrong passwords). Modify JWT tokens and test.

### Category C: Input Validation & Injection (INJ)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| INJ-01 | XSS: reflected input in page | OWASP A03 / CWE-79 | Submit `<script>alert(1)</script>` in all inputs, check if rendered |
| INJ-02 | XSS: stored input from database | OWASP A03 / CWE-79 | Submit script via form, check if rendered on subsequent page loads |
| INJ-03 | SQL injection in form inputs | OWASP A03 / CWE-89 | Submit `' OR '1'='1` patterns, check for errors |
| INJ-04 | Open redirect via URL parameters | CWE-601 | Test redirect params with external URLs |
| INJ-05 | Path traversal in file operations | CWE-22 | Test `../../etc/passwd` in file-related params |
| INJ-06 | Command injection in input fields | CWE-78 | Test `; ls` or `| whoami` patterns where inputs might reach shell |
| INJ-07 | HTML injection in user content | CWE-79 | Submit HTML tags, check if rendered |
| INJ-08 | URL scheme validation (javascript:) | CWE-79 | Test `javascript:alert(1)` in URL inputs |
| INJ-09 | File upload validation | OWASP A04 | Upload files with wrong extensions, oversized files, executable content |
| INJ-10 | API input validation | OWASP A03 | Send malformed JSON, missing fields, wrong types to API endpoints |

**Browser validation:** Use `act` to fill form fields with test payloads. Capture page state after submission. Check for script execution, error messages, unexpected behavior. Use `get_browser_console_logs` for JavaScript errors that indicate injection vectors.

**Important:** These are non-destructive test payloads for detection only. Do not attempt actual exploitation. Alert-based XSS tests use `alert(1)` which is harmless.

### Category D: Access Control (AC)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| AC-01 | Authenticated pages return 401/403 without auth | OWASP A01 | Access protected URLs without authentication |
| AC-02 | No IDOR (Insecure Direct Object Reference) | OWASP A01 / CWE-639 | Change resource IDs in URLs, check for unauthorized access |
| AC-03 | API endpoints enforce authorization | OWASP A01 | Call API endpoints with wrong/missing auth |
| AC-04 | Admin pages are not accessible to regular users | OWASP A01 | Navigate to admin routes with regular user session |
| AC-05 | No sensitive data in client-side source | Information leak | Check JavaScript bundles for API keys, secrets |
| AC-06 | Directory listing disabled | Information leak | Access directory URLs (e.g., /api/, /static/) |
| AC-07 | Debug endpoints not exposed in production | OWASP A05 | Check common debug paths (/debug, /trace, /graphql playground) |
| AC-08 | Error messages don't leak internal details | OWASP A05 | Trigger errors, check for stack traces, DB details |

**Browser validation:** Navigate to protected pages without auth. Try accessing resources belonging to other users. Check JavaScript source for hardcoded secrets using `act` with JavaScript to scan script contents.

### Category E: Client-Side Security (CLI)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| CLI-01 | No sensitive data in client-side storage | OWASP Storage | Inspect localStorage, sessionStorage, IndexedDB |
| CLI-02 | Subresource Integrity (SRI) on CDN resources | Supply chain | Check `integrity` attribute on external scripts/styles |
| CLI-03 | Third-party scripts inventory | Supply chain | List all external script sources |
| CLI-04 | No eval() or innerHTML with user input | CWE-79 | Scan JavaScript for dangerous patterns |
| CLI-05 | Service worker scope is restricted | Client security | Check SW registration scope |
| CLI-06 | WebSocket connections use WSS | Transport | Check WS connection URLs |
| CLI-07 | No sensitive data in console logs | Information leak | Check `get_browser_console_logs` output |
| CLI-08 | Clickjacking protection works | OWASP Clickjacking | Test embedding page in iframe |

**Browser validation:** Use JavaScript via `act` to enumerate localStorage keys, check script tags for SRI, list all network requests to external domains. Use `get_browser_console_logs` to check for leaked data.

### Category F: Dependency & Supply Chain (DEP)

| Check ID | Check | Standard | Method |
|----------|-------|----------|--------|
| DEP-01 | No known vulnerable dependencies | OWASP A06 / CWE-1035 | Run `npm audit` / `pip audit` |
| DEP-02 | Lock file exists and is committed | Supply chain | Check for package-lock.json / yarn.lock / pnpm-lock.yaml |
| DEP-03 | No unnecessary dependencies | Attack surface | Check for unused packages |
| DEP-04 | CDN resources use SRI | Supply chain | Check integrity attributes (same as CLI-02) |
| DEP-05 | No typosquatting risk in dependencies | Supply chain | Check package names against known packages |

**Validation:** Run dependency audit commands. Cross-reference with codebase scan from Phase 2.

---

## Phase 4: Report

Generate a structured report saved to `shiplight/reports/security-review-{date}.md`:

```markdown
# Security Review Report
**Date:** {date}
**URL:** {url}
**Auth mechanism:** {type}
**Attack surface:** {summary}

## Overall Score: {X}/10 | Confidence: {X}%

## Score Breakdown
| Category | Score | Findings |
|----------|-------|----------|
| HTTP Headers (HDR) | 6/10 | 1 critical, 2 high |
| Auth & Sessions (AUTH) | 4/10 | 2 critical, 1 high |
| Input Validation (INJ) | 7/10 | 1 high, 2 medium |
| Access Control (AC) | 8/10 | 1 medium |
| Client-Side (CLI) | 5/10 | 1 critical, 1 high |
| Dependencies (DEP) | 9/10 | 1 low |

## Findings

### CRITICAL

#### AUTH-01: JWT stored in localStorage — XSS leads to full account takeover
- **Standard:** OWASP ASVS 3.3.2 / CWE-922
- **Finding:** Access token stored in `localStorage` under key `auth_token`, accessible to any XSS payload
- **Evidence:** [screenshot of Application > Storage showing JWT]
- **Attack scenario:** Any XSS vulnerability (even via third-party script) can exfiltrate all user tokens
- **CVSS estimate:** 8.1 (High)
- **Confidence:** 95%

...
```

### Confidence Scoring
- **90-100%**: Exploited and verified in browser (e.g., XSS payload executed, unauthorized access confirmed)
- **70-89%**: Strong evidence from inspection (e.g., missing header confirmed, insecure cookie flags observed)
- **50-69%**: Code-level evidence, not fully validated at runtime
- **Below 50%**: Don't report — too speculative

---

## Phase 5: Remediate

For each finding, provide:

### 1. Fix guidance
```markdown
#### AUTH-01: JWT stored in localStorage
**Risk:** Any XSS → full account takeover
**File:** src/lib/auth.ts:47
**Current:** `localStorage.setItem('auth_token', jwt)`
**Fix:** Move to HttpOnly cookie set by the server
- Server: `Set-Cookie: token=<jwt>; HttpOnly; Secure; SameSite=Strict; Path=/`
- Client: Remove all localStorage token operations
- API calls: Cookies sent automatically (remove Authorization header)
**Migration steps:**
1. Add cookie-setting endpoint on server
2. Update API middleware to read from cookie
3. Remove client-side token storage
4. Update CORS to allow credentials
```

### 2. YAML regression test
```yaml
- name: auth-01-no-tokens-in-localstorage
  description: Verify authentication tokens are not stored in localStorage
  severity: critical
  standard: OWASP-ASVS-3.3.2
  steps:
    - URL: /login
    - intent: Enter test username
      action: fill
      locator: "getByLabel('Email')"
      value: "test@example.com"
    - intent: Enter test password
      action: fill
      locator: "getByLabel('Password')"
      value: "testpass123"
    - intent: Click login button
      action: click
      locator: "getByRole('button', { name: 'Sign in' })"
    - WAIT_UNTIL: User is logged in and dashboard is visible
      timeout_seconds: 15
    - description: Assert no auth tokens are stored in localStorage
      js: |
        const keys = Object.keys(localStorage);
        const tokenKeys = keys.filter(k =>
          /token|jwt|auth|session|access/i.test(k)
        );
        if (tokenKeys.length > 0) {
          throw new Error(
            `Auth tokens found in localStorage: ${tokenKeys.join(', ')}`
          );
        }
    - VERIFY: No authentication tokens are stored in browser localStorage
```

Save all YAML tests to `shiplight/tests/security-review.test.yaml`.

---

## Penetration Test Depth Levels

- **`--quick`**: Headers (HDR) + Cookie flags (AUTH-02/03/04) + localStorage check (AUTH-01) + dependency audit (DEP-01). ~2 minutes.
- **default**: All categories, standard payloads. ~10 minutes.
- **`--thorough`**: All categories + extended injection payloads + IDOR enumeration + brute force testing + full third-party script analysis. ~20-30 minutes.

## Tips

- Always use test credentials, never production credentials
- XSS test payloads are non-destructive (`alert(1)`) — safe for staging environments
- For authenticated testing, save the session with `save_storage_state` after login
- Run `npm audit` before the browser-based review to catch known CVEs early
- Use `get_browser_console_logs` — many security issues produce console warnings
- Close the session with `close_session` and use `generate_html_report` for evidence
