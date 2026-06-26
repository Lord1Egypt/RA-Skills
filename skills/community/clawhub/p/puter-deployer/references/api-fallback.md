# Puter API Fallback (when puter-cli is unstable)

Use this only if CLI deployment path fails but auth/session is valid.

## Principles
- Reuse existing authenticated context where possible.
- Do not expose secrets in logs.
- Validate response status + deployed URL.

## Minimal fallback pattern

1. Confirm CLI login first (`puter whoami`).
2. Package output directory (zip/tar) if API expects artifact upload.
3. Call Puter endpoint used by CLI for deploy/publish (inspect CLI/network if needed).
4. Poll deployment status endpoint until success/failure.
5. Verify resulting URL with HTTP checks.

## Failure triage
- 401/403: auth/session expired
- 404: wrong app/site identifier
- 413: artifact too large
- 5xx/timeouts: transient platform issue; retry with backoff
