---
name: client-side-pentest
description: >
  Perform a thorough client-side / browser-facing security assessment of a target web application.
  Use this skill whenever the user asks to pentest, audit, or review the security of a website or
  web app from the browser/frontend perspective, mentions client-side vulnerabilities (XSS, CORS,
  open redirect, clickjacking, prototype pollution, JWT leakage, source maps, etc.), wants to find
  sensitive data exposed in JavaScript bundles or client code, or asks for a security report on
  front-end attack surface. Trigger even if the user just says "test the security of this site",
  "find vulnerabilities in this web app", or "run a pentest on the frontend".
---

# Client-Side / Front-End Security Assessment

A skill for conducting thorough, non-destructive client-side security reviews of web applications,
producing a structured Markdown report covering all major browser-facing attack surface categories.

---

## Setup: Fill in Before Starting

Before executing, confirm these values with the user if not already provided:

| Variable | Description |
|---|---|
| `TARGET` | Primary target URL |
| `LOGIN` | Login URL or credentials (if authenticated testing is in scope) |
| `CRED_AREAS` | Credential areas needing extra attention |
| `TOOLS_DIR` | Path to any custom tools folder |
| `SCOPE` | Client-side and front-end only (unless user explicitly extends) |

---

## Authorization & Safety Constraints

- This assessment is authorized by the asset owner
- **Non-destructive only** — no DoS, brute force, spam, mass account creation, credential attacks
- Keep request volume moderate; avoid noisy scans unless the user explicitly approves
- Prefer passive analysis first, then low-risk validation
- Only attempt proof-of-concept when necessary to confirm a finding
- Never exceed the defined scope without explicit user approval

---

## Mission

Identify the following across the client-side attack surface:

1. **Vulnerable / outdated client-side dependencies** (JS libraries, third-party scripts)
2. **Sensitive information exposed in client-side assets** (keys, tokens, internal endpoints, configs, source maps)
3. **Client-side vulnerabilities** — see full checklist below

---

## Vulnerability Checklist

Cover all of the following (mark each as Confirmed / Likely / Informational / False Positive):

**Injection & Scripting**
- [ ] Reflected XSS
- [ ] Stored XSS
- [ ] DOM-based XSS
- [ ] Mutation XSS (mXSS)
- [ ] Client-Side Template Injection (CSTI)
- [ ] HTML Injection
- [ ] CSS Injection
- [ ] Dangling markup injection
- [ ] Unsafe use of `innerHTML`, `outerHTML`, `document.write`
- [ ] Unsafe `eval` / dynamic code execution

**Redirects & Framing**
- [ ] Open redirect
- [ ] DOM-based open redirect
- [ ] Reverse tabnabbing / `window.opener` abuse
- [ ] Clickjacking / UI redressing
- [ ] Unsafe iframe embedding
- [ ] Weak iframe sandboxing
- [ ] Form action hijacking

**Cross-Origin & Trust**
- [ ] CORS misconfiguration
- [ ] `postMessage` flaws (origin validation)
- [ ] Cross-site WebSocket hijacking
- [ ] Missing Subresource Integrity (SRI) on third-party scripts
- [ ] Unsafe third-party script trust

**Caching & Service Workers**
- [ ] Web cache deception
- [ ] Web cache poisoning
- [ ] Service worker abuse / misconfiguration
- [ ] Offline cache poisoning

**Data Exposure**
- [ ] JWT / token leakage in `localStorage` / `sessionStorage` / cookies
- [ ] Sensitive data in JS bundles or source
- [ ] Source map exposure (`.map` files reachable)
- [ ] Hardcoded secrets / API keys in frontend code
- [ ] Stack traces or debug data visible to client
- [ ] Hidden admin functionality / feature flags exposed

**Client-Side Logic & Manipulation**
- [ ] Client-side authorization bypass
- [ ] Business logic manipulation in browser
- [ ] Parameter tampering
- [ ] Hidden field manipulation
- [ ] Client-side prototype pollution
- [ ] Insecure client-side deserialization
- [ ] Client-side path traversal
- [ ] DOM clobbering

**Browser & Misc**
- [ ] CSRF risk from frontend request patterns
- [ ] Mixed content
- [ ] MIME sniffing / content-type confusion
- [ ] Referer leakage
- [ ] Browser history leakage
- [ ] Autofill abuse / credential leakage
- [ ] Clipboard abuse
- [ ] File upload client-side validation bypass
- [ ] XS-Leaks
- [ ] LocalStorage / SessionStorage abuse
- [ ] Vulnerable third-party JavaScript libraries (CVE-matched)

---

## Methodology (Execute in Order)

### Phase 1 — Reconnaissance & Asset Enumeration

- Crawl target: enumerate pages, scripts, endpoints, static assets
- Identify JS bundles, source maps (`.map`), manifests, service workers, web workers
- Enumerate first-party and third-party JS resources (CDN scripts, analytics, tag managers)
- Check storage usage: `localStorage`, `sessionStorage`, `IndexedDB`, cookies
- Identify public config artifacts: `robots.txt`, `sitemap.xml`, `.well-known/*`, `manifest.json`
- Review HTTP response headers: CSP, CORS, `X-Frame-Options`, `X-Content-Type-Options`,
  `Referrer-Policy`, `Permissions-Policy`, `HSTS`

**Tools to use:** `curl`, `wget`, browser DevTools, `gau`, `waybackurls`, `hakrawler`, `katana`,
`subfinder`, `httpx`, `nuclei`, custom scripts in `TOOLS_DIR`, Chrome (manual review)

### Phase 2 — Static Analysis

- Download and review all reachable JS bundles and source maps
- Search for: hardcoded keys, tokens, credentials, internal URLs, debug flags, feature flags
- Parse source maps to reconstruct original source where available
- Identify JS library names and versions; cross-reference against known CVEs (RetireJS, Snyk DB)
- Review HTML for: inline scripts, hidden fields, form actions, iframes, `rel="noopener"` presence
- Review CSP policy for bypasses (wildcards, unsafe-inline, unsafe-eval, missing directives)

**Tools:** `retire.js`, `npm audit`, `semgrep`, `grep`/`ripgrep`, browser DevTools Sources tab,
`js-beautify`, `source-map` CLI

### Phase 3 — Targeted Low-Risk Runtime Validation

- Open the target in Chrome; observe network requests, console errors, storage
- Test CORS by issuing cross-origin requests with crafted `Origin` headers
- Check `postMessage` handlers: send crafted messages with untrusted origins
- Test open redirect candidates with controlled payloads
- Test XSS candidates with non-alerting, non-destructive probes (e.g., unique string reflection)
- Inspect cookies: flags (`HttpOnly`, `Secure`, `SameSite`), scope, expiry
- Check service workers: scope, fetch event handlers, cache strategies
- Test iframe embedding from external origin

### Phase 4 — Risk Confirmation (Only Where Needed)

- Construct minimal PoC to confirm exploitability where finding is likely but unconfirmed
- Do not automate or repeat; single manual validation only
- Document exact reproduction steps

---

## JavaScript Library Review Format

For each identified library:

| Field | Value |
|---|---|
| Library name | |
| Detected version | |
| File path / URL | |
| Evidence | |
| Known CVEs / issues | |
| Assessment | Vulnerable / Outdated / OK |
| Security relevance | |

---

## Running Log (Keep Updated Throughout)

Maintain a running log as you work:

```
[STEP] Description of action
[TOOL] Tool and command used
[OUTPUT] Key evidence or finding
[CONFIDENCE] High / Medium / Low
```

---

## Output

Save the final report as:

```
client_side_pentest_report.md
```

in the current working directory.

---

## Report Structure

```markdown
# Client-Side Penetration Test Report

## Executive Summary
## Scope & Assumptions
## Methodology
## Asset Inventory (client-side relevant)
## JavaScript Library Inventory
## Sensitive Data Exposure Findings
## Vulnerability Findings
## Informational Observations
## False Positives Ruled Out
## Recommended Remediation
## Appendix (commands, URLs, raw evidence, notes)
```

### Per-Finding Format

```markdown
### [FINDING TITLE]

- **Severity**: Critical / High / Medium / Low / Informational
- **CWE**: CWE-XXXX — [name]
- **Affected asset(s)**:
- **Description**:
- **Evidence**:
- **Reproduction steps**:
- **Security impact**:
- **Likelihood / Confidence**: Confirmed / Likely / Informational / False Positive
- **Remediation**:
- **References**:
```

---

## Execution Style

- Be systematic, concise, and technical
- Prefer high signal over noisy output
- Do not stop at the first issue — continue until all phases are complete
- Distinguish clearly between Confirmed, Likely, Informational, and False Positive findings
- Do not overstate severity; be skeptical and evidence-driven
- If a noisier step is needed (e.g., active scanning, fuzzing), **pause and ask the user for approval**
  with a clear explanation of what will be done and why

