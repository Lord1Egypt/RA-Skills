# Puter Deploy Failure Playbook

## 1) Auth/session failure

Symptoms:
- `puter whoami` fails
- 401/403 from API endpoints

Fix:
1. `puter logout`
2. `puter login`
3. rerun preflight

## 2) Build artifact failure

Symptoms:
- build dir missing/empty
- missing `index.html`

Fix:
1. run project build (`npm run build` or project equivalent)
2. confirm output dir and `index.html`
3. rerun preflight

## 3) Target mismatch

Symptoms:
- app/site not found
- wrong remote path/url

Fix:
1. verify target app/site identifier
2. verify expected URL and domain mapping
3. retry deploy to corrected target

## 4) Platform/API issue

Symptoms:
- 5xx/timeouts
- intermittent success/failure

Fix:
1. retry with backoff (3 attempts)
2. capture request/response status only (no token logs)
3. report outage condition and stop destructive changes
