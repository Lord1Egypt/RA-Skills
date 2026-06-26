# 🛡️ Safe Change

**Map the blast radius before an AI agent edits code.**

Safe Change is the “look left and right before crossing” skill for code changes. It scans the target file, finds importers, routes, tests, ENV variables, and migration risk, then forces a go/no-go checkpoint before anything is modified.

## What It Prevents

- Renaming a shared method and breaking hidden callers
- Editing an auth/payment/data path without knowing affected routes
- Shipping a refactor with no tests covering the changed path
- Letting an agent make a “small” change that touches half the system

## What It Does

- Builds an **Impact Map** for the target file
- Calculates **Low / Medium / High** risk with concrete reasons
- Shows **test gaps** and likely verification commands
- Flags **ENV/config/migration** risk
- Pauses for explicit **go / shrink scope / abort** before editing
- Runs a post-change verify gate: typecheck → lint → test → build

## Quick Example

```bash
node scripts/scan-impact.mjs src/auth/auth.service.ts
```

Condensed report:

```json
{
  "target": "src/auth/auth.service.ts",
  "imports": { "count": 7 },
  "routes": { "endpoints": ["POST /auth/login", "GET /auth/me"] },
  "tests": { "count": 0, "gap": true },
  "env_vars": ["JWT_SECRET"],
  "risk_score": "high",
  "risk_factors": ["7 importers", "auth routes", "no direct tests", "JWT env"]
}
```

Agent response should be:

```text
Risk: HIGH.
Recommendation: shrink scope or add/locate tests before editing.
Go / shrink / abort?
```

## Best Targets

- NestJS services/controllers/guards
- Next.js route handlers/server actions/hooks
- Shared TypeScript utilities
- Auth, billing, data import/export, migrations

## Not For

- Pure text/README edits
- Obvious typo fixes
- Throwaway prototypes

## Companion Skills

- **coding-pipeline** — wraps the full plan/code/validate/debug loop
- **deep-debugging** — use after a bug already exists

Safe Change is proactive. Run it before the mess.

---

*by brasco05 · read-only impact scanning, zero dependencies*
