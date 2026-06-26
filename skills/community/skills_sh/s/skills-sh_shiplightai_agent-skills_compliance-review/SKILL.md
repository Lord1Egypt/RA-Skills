---
name: compliance-review
description: "Compliance review and testing: evaluate your application against HIPAA, SOC 2, PCI-DSS, and GDPR technical requirements with browser-based validation and YAML regression tests for continuous compliance."
---

# Compliance Review

Evaluate your application against industry-specific regulatory requirements. This review translates dense compliance frameworks into concrete, testable technical checks — and validates them through browser-based testing. Non-compliance can result in severe fines, legal action, and loss of business.

## When to use

Use `/compliance-review` when:
- Building applications for regulated industries (healthcare, finance, government)
- Preparing for a compliance audit (SOC 2, HIPAA, PCI-DSS)
- Adding payment processing or health data features
- Expanding to GDPR-regulated markets
- After infrastructure or architecture changes that affect data handling

## Standards Referenced

- **HIPAA** — Health Insurance Portability and Accountability Act (Technical Safeguards §164.312)
- **SOC 2** — Service Organization Control (Trust Service Criteria)
- **PCI-DSS v4.0** — Payment Card Industry Data Security Standard
- **GDPR** — General Data Protection Regulation (Technical Measures)

## Phase Overview

```
Phase 1: EDUCATE   → Compliance context and applicable frameworks
Phase 2: SCOPE     → Determine which frameworks apply, identify regulated data
Phase 3: ANALYZE   → Browser-based checks against framework requirements
Phase 4: REPORT    → Findings mapped to specific regulatory sections
Phase 5: REMEDIATE → Fix guidance + YAML regression tests for continuous compliance
```

---

## Phase 1: Educate

> **Why this matters:** HIPAA violations: up to $1.9M per violation category per year. PCI-DSS non-compliance: $5,000-$100,000/month in fines plus liability for breaches. SOC 2 failures: loss of enterprise customers who require it. GDPR: up to 4% of global annual revenue. These aren't theoretical — enforcement is active and increasing.

Compliance frameworks are large documents. This review extracts the **technical requirements testable in a web application** — not the organizational/procedural requirements (policies, training, vendor management) that require human process review.

---

## Phase 2: Scope

### Determine applicable frameworks

1. **Auto-detect from codebase:**
   - Health data handling (HIPAA indicators: HL7, FHIR, patient records, PHI references)
   - Payment processing (PCI-DSS indicators: Stripe, Braintree, credit card fields, payment forms)
   - EU user data (GDPR indicators: consent banners, cookie notices, EU deployments)
   - Audit logging (SOC 2 indicators: audit trail, event logging, access logs)

2. **Ask the user:**
   - **Which frameworks apply?** (auto-detected, confirm)
     - [ ] HIPAA — healthcare / protected health information
     - [ ] SOC 2 — enterprise SaaS / customer data
     - [ ] PCI-DSS — payment card data
     - [ ] GDPR — EU personal data
     - [ ] Other (specify)
   - **Target URL**: Where is the app running?
   - **Regulated data types**: What regulated data does the app handle? (auto-detected)
   - **Test credentials**: Accounts with access to regulated data for testing

3. **Map regulated data flows:**
   - Where regulated data enters the system (forms, APIs, imports)
   - Where it's displayed (dashboards, reports, exports)
   - Where it's stored client-side (if anywhere)
   - Where it's transmitted (API endpoints, third-party services)

---

## Phase 3: Analyze

Run only the sections applicable based on Phase 2 scoping. Open a browser session with `new_session` using `record_evidence: true`.

### HIPAA Technical Safeguards (HIP)

Applicable when: application handles Protected Health Information (PHI).

| Check ID | Check | HIPAA Section | Method |
|----------|-------|---------------|--------|
| HIP-01 | PHI not displayed without authentication | §164.312(d) | Access PHI pages without auth, verify 401/redirect |
| HIP-02 | Session auto-timeout after inactivity | §164.312(a)(2)(iii) | Wait for idle period, verify session expiration |
| HIP-03 | PHI not in URL parameters | §164.312(e)(1) | Navigate PHI pages, check URLs |
| HIP-04 | PHI not in browser console/logs | §164.312(b) | Check `get_browser_console_logs` for PHI patterns |
| HIP-05 | PHI not cached in browser storage | §164.312(a)(2)(iv) | Check localStorage, sessionStorage for PHI |
| HIP-06 | PHI transmitted over HTTPS only | §164.312(e)(1) | Verify all PHI API calls use HTTPS |
| HIP-07 | Audit trail for PHI access | §164.312(b) | Access PHI, verify audit log entry exists |
| HIP-08 | Role-based access to PHI | §164.312(a)(1) | Test PHI access with different user roles |
| HIP-09 | PHI display has minimum necessary principle | §164.502(b) | Check if UI shows only needed PHI fields |
| HIP-10 | Emergency access procedure exists | §164.312(a)(2)(ii) | Check for break-glass or emergency access UI |
| HIP-11 | No PHI in error messages | §164.312(b) | Trigger errors on PHI pages, check messages |
| HIP-12 | Logout fully terminates PHI access | §164.312(a)(2)(iii) | Logout, back button, check no PHI visible |

**Browser validation:** Navigate to pages with PHI. Test access controls. Check for PHI in URLs, storage, console. Test session timeout by waiting. Test logout completeness.

### SOC 2 Trust Service Criteria (SOC)

Applicable when: enterprise SaaS handling customer data.

| Check ID | Check | SOC 2 Criteria | Method |
|----------|-------|----------------|--------|
| SOC-01 | Authentication required for all data access | CC6.1 | Access data pages without auth |
| SOC-02 | Strong password requirements enforced | CC6.1 | Test signup/password change with weak passwords |
| SOC-03 | MFA available for user accounts | CC6.1 | Check account security settings for MFA option |
| SOC-04 | Session management is secure | CC6.1 | Check cookie flags, timeout, logout behavior |
| SOC-05 | Data is encrypted in transit | CC6.7 | Verify HTTPS everywhere, check for mixed content |
| SOC-06 | Access is logged (audit trail) | CC7.2 | Perform actions, verify audit log entries |
| SOC-07 | Failed login attempts are monitored | CC7.2 | Multiple failed logins, check for alerting/lockout |
| SOC-08 | User permissions are role-based | CC6.3 | Test different roles, verify appropriate access |
| SOC-09 | Data deletion is available | CC6.5 | Test account/data deletion functionality |
| SOC-10 | System status page or health endpoint | CC7.1 | Check for status page or /health endpoint |
| SOC-11 | Error handling doesn't leak internal details | CC7.4 | Trigger errors, check for stack traces |
| SOC-12 | Change management evident (versioning) | CC8.1 | Check for version info, changelog |

**Browser validation:** Test authentication boundaries, password policies, MFA flows, role-based access, audit logging visibility.

### PCI-DSS v4.0 (PCI)

Applicable when: application processes, stores, or transmits cardholder data.

| Check ID | Check | PCI-DSS Req | Method |
|----------|-------|-------------|--------|
| PCI-01 | Credit card numbers never fully displayed | 3.4 | View saved cards, verify masking (show last 4 only) |
| PCI-02 | CVV never stored or displayed after authorization | 3.3.2 | Check storage, API responses for CVV |
| PCI-03 | Payment form uses HTTPS | 4.1 | Verify payment page URL and all resources |
| PCI-04 | Payment form is on compliant iframe/redirect | SAQ A | Check if using Stripe Elements, PayPal, or similar |
| PCI-05 | No cardholder data in URL parameters | 4.2 | Check URLs during payment flow |
| PCI-06 | No cardholder data in client storage | 3.2 | Check localStorage, sessionStorage, cookies |
| PCI-07 | No cardholder data in console logs | 3.2 | Check `get_browser_console_logs` during payment |
| PCI-08 | Payment form prevents autocomplete on card fields | Best practice | Check `autocomplete="off"` on sensitive fields |
| PCI-09 | Strong authentication for payment admin | 8.3 | Verify admin/payment management requires strong auth |
| PCI-10 | Access to cardholder data is role-restricted | 7.1 | Test access to payment data with non-admin users |
| PCI-11 | Payment error messages don't reveal card details | 3.2 | Trigger payment errors, check messages |
| PCI-12 | CSP prevents unauthorized scripts on payment pages | 6.4.3 | Check CSP header on payment pages specifically |

**Browser validation:** Walk through the payment flow. Check card display masking. Inspect storage and console for cardholder data. Verify payment form is iframe/hosted (SAQ A compliance).

### GDPR Technical Requirements (GDPR)

Applicable when: application handles EU personal data. (Note: privacy-specific checks are in `/privacy-review` — this section covers GDPR's technical/compliance obligations.)

| Check ID | Check | GDPR Article | Method |
|----------|-------|-------------|--------|
| GDPR-01 | Consent collected before data processing | Art. 6, 7 | Load page, check if processing occurs before consent |
| GDPR-02 | Privacy policy is accessible and current | Art. 13, 14 | Find and verify privacy policy page |
| GDPR-03 | Data subject access request mechanism exists | Art. 15 | Find data export/download feature |
| GDPR-04 | Right to erasure is implemented | Art. 17 | Find and test account deletion |
| GDPR-05 | Data portability (export in standard format) | Art. 20 | Test data export, verify format (JSON/CSV) |
| GDPR-06 | Consent withdrawal is as easy as giving consent | Art. 7(3) | Compare consent-giving vs withdrawal UX |
| GDPR-07 | Age verification for minors (if applicable) | Art. 8 | Check for age gate or parental consent |
| GDPR-08 | Data processing records accessible | Art. 30 | Check for processing activity documentation |
| GDPR-09 | Data breach notification mechanism | Art. 33, 34 | Check for incident response documentation |
| GDPR-10 | Cross-border transfer safeguards | Art. 44-49 | Check where third-party services are hosted |

**Browser validation:** Test consent flows, data export, account deletion, privacy policy accessibility. Check third-party script origins for cross-border transfer concerns.

---

## Phase 4: Report

Generate a structured report saved to `shiplight/reports/compliance-review-{date}.md`:

```markdown
# Compliance Review Report
**Date:** {date}
**URL:** {url}
**Frameworks evaluated:** {HIPAA, SOC 2, PCI-DSS, GDPR}
**Regulated data types:** {PHI, cardholder data, EU personal data}

## Overall Compliance Score: {X}/10 | Confidence: {X}%

## Framework Scores
| Framework | Score | Pass | Fail | N/A | Critical Gaps |
|-----------|-------|------|------|-----|---------------|
| HIPAA | 6/10 | 8 | 3 | 1 | Session timeout, PHI in URL |
| SOC 2 | 7/10 | 9 | 2 | 1 | No MFA, weak audit trail |
| PCI-DSS | 8/10 | 10 | 1 | 1 | Card data in console |
| GDPR | 5/10 | 5 | 4 | 1 | Consent, data export, erasure |

## Compliance Status by Check
(Full table of all checks with PASS/FAIL/N-A status, evidence, and confidence)

## Critical Non-Compliance Items
(Findings that could result in regulatory action, ordered by risk)

## Audit Preparation Checklist
- [ ] Fix all CRITICAL findings
- [ ] Fix all HIGH findings
- [ ] Document accepted risks for MEDIUM findings
- [ ] Run YAML regression tests before audit date
- [ ] Prepare evidence documentation from this report
```

### Confidence Scoring
- **90-100%**: Browser-validated, compliance violation confirmed (e.g., PHI visible without auth, card number in console)
- **70-89%**: Strong evidence from inspection (e.g., missing header, no timeout behavior)
- **50-69%**: Architectural concern based on code patterns (e.g., audit logging might be incomplete)
- **Below 50%**: Don't report — compliance findings must be substantiated

---

## Phase 5: Remediate

### 1. Fix guidance (example)
```markdown
#### HIP-02: No session auto-timeout
**Regulation:** HIPAA §164.312(a)(2)(iii) — Automatic logoff
**Risk:** Unattended sessions with PHI visible
**Current:** Sessions persist indefinitely
**Fix:** Implement idle timeout (HIPAA recommends ≤15 minutes for PHI access)
- Add client-side idle detection (mouse, keyboard events)
- Server-side session expiry as backup
- Show warning dialog at 12 minutes
- Auto-logout and clear screen at 15 minutes
```

### 2. YAML regression test
```yaml
- name: hip-02-session-auto-timeout
  description: Verify session auto-timeout for HIPAA compliance
  severity: critical
  standard: HIPAA-164.312(a)(2)(iii)
  steps:
    - URL: /login
    - intent: Log in with test credentials
      action: fill
      locator: "getByLabel('Email')"
      value: "test@example.com"
    - intent: Enter password
      action: fill
      locator: "getByLabel('Password')"
      value: "testpass123"
    - intent: Submit login form
      action: click
      locator: "getByRole('button', { name: 'Sign in' })"
    - WAIT_UNTIL: Dashboard with PHI is visible
      timeout_seconds: 15
    - VERIFY: Session timeout warning appears after inactivity period
      timeout_seconds: 900
    - VERIFY: User is automatically logged out after timeout expires
      timeout_seconds: 300
```

Save all YAML tests to `shiplight/tests/compliance-review.test.yaml`.

---

## Depth Levels

- **`--quick`**: Critical checks only — authentication boundaries + data exposure. ~3 minutes.
- **default**: Full applicable framework. ~10-15 minutes.
- **`--thorough`**: All checks + multi-role testing + edge cases + documentation review. ~25-40 minutes.

## Tips

- Run the compliance review specific to your framework: "run HIPAA checks only"
- Compliance requires evidence — use `record_evidence: true` and `generate_html_report` for audit documentation
- YAML regression tests from this review serve as continuous compliance monitoring
- This review covers technical requirements only — organizational requirements (policies, training) need human review
- For privacy-specific concerns, complement with `/privacy-review`
- For security-specific concerns, complement with `/security-review`
- Close session with `close_session` and use `generate_html_report` for evidence
