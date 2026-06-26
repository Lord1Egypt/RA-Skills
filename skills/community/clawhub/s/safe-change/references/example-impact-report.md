# Example Impact Report — SMTP Provider Swap

**Scenario:** You are swapping the SMTP provider in a Caresys-style NestJS app. The target file is `src/notifications/notifications.service.ts`. It currently uses Nodemailer with SendGrid credentials. You want to switch to Resend.

This is a realistic "feels small" change that actually touches 5 modules and a live API route.

---

## Step 1 — Run the Scanner

```bash
node skills/safe-change/scripts/scan-impact.mjs src/notifications/notifications.service.ts
```

---

## Step 2 — Raw JSON Output

```json
{
  "target": "src/notifications/notifications.service.ts",
  "stack": {
    "framework": "nestjs",
    "hasNextJs": false
  },
  "imports": {
    "importers": [
      "src/users/users.service.ts",
      "src/appointments/appointments.service.ts",
      "src/billing/billing.service.ts",
      "src/reports/reports.service.ts",
      "src/audit/audit.service.ts"
    ],
    "count": 5
  },
  "routes": {
    "controllers": ["NotificationsController"],
    "endpoints": [
      "POST /notifications",
      "GET /notifications"
    ],
    "next_routes": []
  },
  "tests": {
    "covering": [
      "src/notifications/notifications.service.spec.ts"
    ],
    "count": 1,
    "gap": false
  },
  "env_vars": [
    "SMTP_HOST",
    "SMTP_PASS",
    "SMTP_USER"
  ],
  "migrations": {
    "recent_count": 0,
    "recent_files": []
  },
  "risk_score": "medium",
  "risk_factors": [
    "5 importers",
    "1 API route",
    "test coverage exists"
  ]
}
```

---

## Step 3 — Agent Renders Markdown Report

The agent reads the JSON and renders:

```markdown
## Safe Change Report — src/notifications/notifications.service.ts

**Risk Score: MEDIUM**
Risk factors: 5 importers, 1 API route, test coverage exists

### Importers (5)
These files call into NotificationsService. A breaking change here affects all of them.

- src/users/users.service.ts
- src/appointments/appointments.service.ts
- src/billing/billing.service.ts
- src/reports/reports.service.ts
- src/audit/audit.service.ts

### API Routes Affected

| Controller | Endpoints |
|------------|-----------|
| NotificationsController | POST /notifications |
| NotificationsController | GET /notifications |

The POST endpoint is called by the billing flow on invoice creation.
The GET endpoint is used by the frontend notification bell.

### Test Coverage

- src/notifications/notifications.service.spec.ts ✓
- Gap: no

One spec file exists. Before swapping providers, verify it mocks at the
interface level (not the Nodemailer transport directly) — otherwise tests
pass but the new provider is untested.

### ENV Variables Referenced

- SMTP_HOST — must be updated to Resend's SMTP gateway
- SMTP_USER — update to Resend API key (username format differs)
- SMTP_PASS — update to Resend API key value

All three ENV vars must be rotated in Railway (production) and .env.local
before deploying.

### Recent Migrations (last 7 days)

- None — no active schema changes in flight, safe to deploy separately

---

**Checkpoint:** Risk score is MEDIUM. 5 services depend on this file and
3 ENV vars must be rotated. Do you want to proceed? (yes / no / adjust scope)
```

---

## Step 4 — User Says Yes

User confirms: "yes, proceed."

The agent swaps the SMTP provider, updates the ENV var names, adjusts the spec mock.

---

## Step 5 — Verify Gate

```bash
bash skills/safe-change/scripts/verify-gate.sh
```

Output:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Safe Change — Verify Gate
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Root: /Users/numan/Desktop/Projekte/caresys/backend

▶ TypeScript (tsc --noEmit)
  node_modules/.bin/tsc --noEmit

✓ TypeScript passed

▶ Lint (npm run lint)
  npm run lint

✓ Lint passed

▶ Tests (npm test)
  npm test

✓ Tests passed

▶ Build (npm run build)
  npm run build

✓ Build passed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  All checks passed. Safe to proceed.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## What Would Have Gone Wrong Without safe-change

Without running the scanner first:

1. **ENV vars not rotated** — production uses old SMTP_HOST, emails fail silently
2. **NotificationsController tests pass locally** but mock the wrong transport layer
3. **billing.service.ts** now imports a changed interface signature — TypeScript would catch this, but only at build time, not before starting
4. **The spec file** mocked Nodemailer's `createTransport` — after the swap, the mock is orphaned and tests give a false green

The MEDIUM risk score is the signal: "this isn't risky enough to block, but it's risky enough to review each factor before touching anything."

A HIGH score would have been the signal to stop entirely and reassess scope.

---

## When the Score Would Be HIGH

Modify the scenario: same file, but add:

- `billing.service.ts` also has an active migration for a new `notification_log` table (recent migration +1)
- `notifications.service.ts` has no spec file (test gap)
- 9 other files import it (importer count ≥ 8)

Score jumps to **HIGH**. The agent stops and says:

> "Risk score is HIGH. 9 importers, no test coverage, and an active migration in flight.
> Recommended action: split this into two changes — (1) add tests first, then (2) swap provider after migration is deployed. Do you want to proceed anyway? (yes / no)"
