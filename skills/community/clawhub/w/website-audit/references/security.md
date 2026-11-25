# Security checks (passive only)

**Scripts:** `check_headers.py` (TLS, HSTS, CSP, other headers, cookies, http→https), `check_html.py` (mixed content, SRI, library hints), `check_crawl.py` (security.txt). Behind a proxy or TLS inspection, certificate data is unconfirmed (see SKILL.md step 2). Not covered: anything active (deliberately).

Observe what the site openly sends. Do not probe for hidden files, test inputs, or attempt access. Most of this needs response headers (Tier B). With Tier A, mark header checks **Not checked**; page-fetch tools usually return content but not headers.

## Transport
- **HTTPS** (B): valid certificate, not near expiry; http redirects to https.
- **HSTS** (B): `Strict-Transport-Security` with a meaningful `max-age` (6 months or more); `includeSubDomains` where appropriate.
- **Mixed content** (A): `http://` resources loaded on https pages.

## Response headers (B)
- **Content-Security-Policy**: present; flag `unsafe-inline`/`unsafe-eval` and wildcard sources as weaknesses rather than absence.
- **X-Content-Type-Options**: `nosniff`.
- **Clickjacking protection**: CSP `frame-ancestors` or `X-Frame-Options`.
- **Referrer-Policy**: set to something stricter than the browser default where sensitive URLs exist.
- **Permissions-Policy**: Low priority unless the site uses powerful features.
- **Information leakage**: detailed `Server` / `X-Powered-By` versions are Low.

## Cookies (B)
Session or auth cookies should have `Secure`, `HttpOnly`, and a deliberate `SameSite`. Tracking cookies matter less than session cookies.

## Third-party and dependencies (A)
- External scripts without Subresource Integrity (Low to Medium, higher for scripts from small or unknown hosts).
- Library versions visible in HTML or filenames: report as "possibly outdated, check advisories". Only call something vulnerable if you verified a specific advisory.

## Published contact
- `/.well-known/security.txt` exists (Low, good practice). This is a standard published location, not a probe.

## Out of scope
Exposed admin paths, backup files, subdomain enumeration, port scans, login testing, and anything that sends non-standard requests. If the user wants those, say this skill does not cover active testing and suggest an authorized security assessment.
