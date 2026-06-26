# Security Entry Examples

Concrete examples of well-formatted security entries with all fields.

## Learning: Vulnerability (SQL Injection)

```markdown
## [LRN-20250415-001] vulnerability

**Logged**: 2025-04-15T09:30:00Z
**Priority**: critical
**Status**: pending
**Area**: endpoint
**CVSS**: 9.8

### Summary
SQL injection vulnerability in legacy `/api/v1/users/search` endpoint via unparameterized query

### Details
The legacy search endpoint constructs SQL queries by concatenating user-supplied
`q` parameter directly into the WHERE clause without parameterization. The endpoint
was excluded from the newer ORM-based query builder during the v2 migration.

Affected code: `src/api/v1/controllers/userSearch.js:47`
Pattern: `"SELECT * FROM users WHERE name LIKE '%" + req.query.q + "%'"`

### Remediation
1. Replace string concatenation with parameterized query using the ORM
2. Add input validation middleware for the `q` parameter
3. Add SQL injection tests to the security test suite
4. Consider deprecating the v1 endpoint entirely

### Metadata
- Source: pen_test
- Related Files: src/api/v1/controllers/userSearch.js
- Tags: sql-injection, legacy-code, input-validation
- CWE: CWE-89
- CVE: N/A (internal finding)
- See Also: LRN-20250320-003

---
```

## Learning: Misconfiguration (S3 Bucket Public Access)

```markdown
## [LRN-20250415-002] misconfiguration

**Logged**: 2025-04-15T11:00:00Z
**Priority**: high
**Status**: resolved
**Area**: cloud
**CVSS**: 7.5

### Summary
S3 bucket `company-internal-docs` configured with public read access, exposing internal documentation

### Details
During cloud posture review, discovered that the `company-internal-docs` S3 bucket
had `PublicReadAccess` enabled via a legacy bucket policy. The bucket contained
internal architecture diagrams, API documentation, and onboarding guides. No
credentials or PII were stored in the bucket.

The misconfiguration was introduced during the 2024 migration from the old
storage account when the bucket policy was copied without review.

### Remediation
1. Immediately set bucket to private: `aws s3api put-public-access-block`
2. Audit all S3 buckets for public access: `aws s3api get-public-access-block`
3. Enable S3 Block Public Access at the account level
4. Add Terraform policy to enforce private-by-default on all new buckets

### Metadata
- Source: audit
- Related Files: terraform/modules/s3/main.tf
- Tags: s3, public-access, cloud-posture, aws
- CWE: CWE-732
- Pattern-Key: harden.s3_public_access
- Recurrence-Count: 1
- First-Seen: 2025-04-15
- Last-Seen: 2025-04-15

### Resolution
- **Resolved**: 2025-04-15T13:00:00Z
- **Commit/PR**: #287
- **Remediation Applied**: Bucket set to private, account-level public access block enabled
- **Verified By**: manual review + AWS Config rule

---
```

## Learning: Compliance Gap (GDPR Consent)

```markdown
## [LRN-20250415-003] compliance_gap

**Logged**: 2025-04-15T14:00:00Z
**Priority**: high
**Status**: in_progress
**Area**: compliance
**CVSS**: N/A

### Summary
Missing explicit GDPR consent mechanism for marketing email collection on signup form

### Details
The signup form collects email addresses and automatically opts users into marketing
communications without a separate, unambiguous consent checkbox. Under GDPR Article 7,
consent must be freely given, specific, informed, and unambiguous. The current
implementation bundles marketing consent with account creation consent.

Discovered during Q2 compliance audit. Affects all EU users who signed up since
the form was redesigned in January 2025.

### Remediation
1. Add separate opt-in checkbox for marketing communications (unchecked by default)
2. Store consent timestamp and version in the users table
3. Implement consent withdrawal mechanism (unsubscribe endpoint)
4. Backfill: send re-consent email to affected EU users
5. Update privacy policy to reflect the change

### Metadata
- Source: audit
- Related Files: src/components/SignupForm.tsx, src/api/auth/register.ts
- Tags: gdpr, consent, compliance, marketing, privacy
- CWE: N/A
- Compliance: GDPR Article 7
- Pattern-Key: comply.gdpr_consent
- Recurrence-Count: 1
- First-Seen: 2025-04-15
- Last-Seen: 2025-04-15

---
```

## Security Incident: Secrets Exposed in CI Logs

```markdown
## [SEC-20250415-001] secrets_exposure

**Logged**: 2025-04-15T08:15:00Z
**Priority**: critical
**Status**: resolved
**Area**: cloud
**Severity**: critical
**CVSS**: N/A

### Summary
Database connection string with embedded credentials printed to GitHub Actions build logs

### Incident Details
```
Build step "Run integration tests" printed the full DATABASE_URL environment variable
to stdout, which included embedded credentials:
  DATABASE_URL=postgres://REDACTED_USER:REDACTED_PASSWORD@REDACTED_HOST:5432/REDACTED_DB

The log was visible to all repository collaborators (~40 people) for approximately
2 hours before detection.
```

NOTE: Actual credentials have been redacted above. The original values were
rotated immediately upon detection.

### Impact Assessment
- Affected systems: Production PostgreSQL database
- Data at risk: All application data (user records, transactions)
- Blast radius: Repository collaborators with Actions log access

### Containment & Remediation
- **Immediate**: Rotated database credentials within 15 minutes of detection
- **Short-term**: Deleted the exposed GitHub Actions run logs
- **Root cause**: Test script used `echo $DATABASE_URL` for debugging and was merged without review
- **Long-term**:
  1. Added GitHub Actions log redaction for all `*_URL`, `*_KEY`, `*_SECRET` patterns
  2. Enabled GitHub secret scanning on the repository
  3. Added pre-merge CI check that greps for credential patterns in test scripts
  4. Implemented `GITHUB_ACTIONS` environment detection to suppress debug output in CI

### Timeline
- **Detected**: 2025-04-15T08:15:00Z (via secret scanning alert)
- **Contained**: 2025-04-15T08:30:00Z (credentials rotated)
- **Resolved**: 2025-04-15T10:00:00Z (logs deleted, preventive controls deployed)

### Metadata
- CVE: N/A
- CWE: CWE-532 (Insertion of Sensitive Information into Log File)
- Attack Vector: network (logs accessible via GitHub web UI)
- Reproducible: yes (any push triggering the test workflow)
- Related Files: .github/workflows/integration-tests.yml, scripts/run-tests.sh
- See Also: LRN-20250310-007

---
```

## Security Incident: Unauthorized API Access via Expired JWT

```markdown
## [SEC-20250415-002] access_violation

**Logged**: 2025-04-15T16:30:00Z
**Priority**: high
**Status**: resolved
**Area**: authentication
**Severity**: high
**CVSS**: 8.1

### Summary
Expired JWT tokens accepted by `/api/v2/admin` endpoints due to missing expiry validation in custom middleware

### Incident Details
```
Monitoring detected admin API calls from a token issued 72 hours ago (tokens
should expire after 1 hour). Investigation revealed the custom JWT middleware
on admin routes checked signature validity but skipped the `exp` claim check.

The standard middleware used on user routes correctly validates expiry.
The admin middleware was a copy-paste that omitted the expiry check.
```

### Impact Assessment
- Affected systems: Admin API endpoints (/api/v2/admin/*)
- Data at risk: Admin operations (user management, config changes, reports)
- Blast radius: Any holder of a previously valid admin JWT could access admin APIs indefinitely

### Containment & Remediation
- **Immediate**: Deployed hotfix adding `exp` validation to admin middleware
- **Short-term**: Revoked all existing admin JWTs by rotating the signing key
- **Root cause**: Admin middleware was a copy of user middleware with the `exp` check accidentally removed
- **Long-term**:
  1. Consolidated JWT validation into a single shared middleware
  2. Added integration test that verifies expired tokens are rejected on all protected routes
  3. Added middleware audit to the security review checklist

### Timeline
- **Detected**: 2025-04-15T16:30:00Z (monitoring alert on stale token usage)
- **Contained**: 2025-04-15T17:00:00Z (hotfix deployed)
- **Resolved**: 2025-04-15T18:30:00Z (signing key rotated, all old tokens invalidated)

### Metadata
- CVE: N/A
- CWE: CWE-613 (Insufficient Session Expiration)
- Attack Vector: network
- Reproducible: yes
- Related Files: src/middleware/adminAuth.ts, src/middleware/auth.ts
- See Also: LRN-20250401-002

---
```

## Feature Request: Automated Secret Scanning in Pre-Commit

```markdown
## [FEAT-20250415-001] secret_scanning_precommit

**Logged**: 2025-04-15T12:00:00Z
**Priority**: high
**Status**: pending
**Area**: endpoint

### Requested Capability
Automated secret scanning as a pre-commit hook to prevent credentials, API keys,
and tokens from being committed to the repository.

### Security Justification
SEC-20250415-001 demonstrated that secrets can reach CI logs via committed debug code.
A pre-commit hook would catch these at the developer's machine before they ever enter
the repository. This is a preventive control that reduces the blast radius of accidental
secret exposure to zero (the commit never happens).

### Complexity Estimate
medium

### Suggested Implementation
1. Integrate `gitleaks` or `trufflehog` as a pre-commit hook via `.pre-commit-config.yaml`
2. Configure custom regex patterns for organization-specific secret formats
3. Add allowlist for known false positives (test fixtures, documentation examples)
4. Provide bypass mechanism for emergencies: `SKIP=gitleaks git commit`
5. Add CI-side scanning as a backup (in case developers skip the hook)

### Metadata
- Frequency: recurring (multiple secret exposure incidents)
- Related Features: GitHub secret scanning, CI log redaction
- Compliance: SOC2 CC6.1, PCI-DSS Requirement 6.5
- See Also: SEC-20250415-001

---
```

## Learning: Promoted to Hardening Checklist

```markdown
## [LRN-20250415-004] misconfiguration

**Logged**: 2025-04-15T10:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: HARDENING.md
**Area**: network

### Summary
CORS misconfiguration allowing wildcard origin on authenticated API endpoints

### Details
The API server was configured with `Access-Control-Allow-Origin: *` on all
endpoints, including authenticated ones. This allows any website to make
cross-origin requests to the API using the user's cookies/tokens, enabling
potential CSRF-like attacks and data exfiltration.

### Remediation
1. Replace wildcard with explicit allowed origins list
2. Use `Access-Control-Allow-Credentials: true` only with specific origins
3. Add CORS configuration to the infrastructure-as-code templates

### Metadata
- Source: pen_test
- Related Files: src/middleware/cors.ts, terraform/modules/api-gateway/main.tf
- Tags: cors, api-security, network
- CWE: CWE-942
- Pattern-Key: harden.cors_wildcard

---
```

## Learning: Promoted to Skill

```markdown
## [LRN-20250415-005] incident_response

**Logged**: 2025-04-15T09:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/secret-rotation-playbook
**Area**: authentication

### Summary
Documented and tested procedure for emergency credential rotation across all environments

### Details
After SEC-20250415-001, formalized the credential rotation procedure that was
executed ad-hoc during the incident. The procedure covers database credentials,
API keys, JWT signing keys, and service account tokens across dev, staging, and
production environments.

### Remediation
Procedure documented as a reusable skill with verification steps for each
credential type and environment.

### Metadata
- Source: incident
- Related Files: docs/runbooks/credential-rotation.md
- Tags: incident-response, credential-rotation, runbook
- See Also: SEC-20250415-001, SEC-20250310-002

---
```
