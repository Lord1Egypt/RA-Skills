---
name: safe-change
description: "Map blast radius before shipping — run when editing a service, controller, hook, or shared utility to surface all importers, affected API routes, test gaps, ENV vars, and recent migrations."
---

# Safe Change

Know exactly what breaks before you touch it.

Safe Change maps the blast radius of any code change — importers, API routes, test coverage, ENV vars, database migrations — then gives you a risk score and waits for your go/no-go before running the verify gate.

It is the proactive companion to deep-debugging: **catch impact before the bug ships**, not after.

---

## Quick Reference

| Situation | Action |
|-----------|--------|
| About to edit a shared service | → Run `scan-impact.mjs` on the target file first |
| Risk score is High | → Stop, read the impact report, get explicit go/no-go |
| Test gap detected (`gap: true`) | → Write tests before changing, not after |
| Recent migrations found | → Confirm migration compatibility before deploying |
| All checks pass | → Run `verify-gate.sh` to confirm build integrity |
| Risk score is Low, tests green | → Proceed, run verify gate at end |

---

## When to Use

Activate this skill whenever:

- You are about to **rename or extract** a function/class used across multiple files
- You are changing the **signature** of a service method
- You are modifying a **NestJS controller** or **Next.js API route**
- You are touching a file that is imported by more than 3 other files
- You are changing code that reads from `process.env`
- There is an **active DB migration** in the migrations folder
- A teammate asks "is it safe to change X?"

Do not skip this step for "small" changes. Most production incidents start as changes that felt small.

---

## How It Works — 6 Phases

### Phase 1 — Detect Stack

The agent reads `package.json` at the project root to determine:
- Is this NestJS, Next.js, or generic TypeScript?
- Are both frameworks present (monorepo)?

### Phase 2 — Build Impact Map

Run `scripts/scan-impact.mjs <target-file>` from the project root.

The script uses regex-based static analysis (no AST compiler, zero install friction) to collect:

| Dimension | What is collected |
|-----------|-------------------|
| **Importers** | All `.ts`/`.tsx` files that import the target |
| **API Routes** | NestJS `@Controller` + HTTP verb decorators; Next.js `app/api/**/route.ts` |
| **Tests** | Spec/test files that import the target; gap flag when none exist |
| **ENV vars** | All `process.env.X` references in the target file |
| **DB migrations** | Files in `migrations/` modified in the last 7 days |

### Phase 3 — Risk Score

Heuristic scoring (see table below). The agent reads the JSON output and renders it as a human-readable report.

| Score | Conditions |
|-------|------------|
| **Low** | ≤2 importers, no API routes, tests exist, no ENV vars, no recent migrations |
| **Medium** | 3–7 importers OR 1–2 routes OR test gap OR ENV vars present |
| **High** | ≥8 importers OR ≥3 routes OR test gap + ENV vars + recent migration |

### Phase 4 — Render Report

The agent formats the JSON from `scan-impact.mjs` into a Markdown report (see Output Format below). It presents the report and **explicitly states the risk score** at the top.

### Phase 5 — Checkpoint (mandatory)

After presenting the report the agent **must pause and ask**:

> "Risk score is [Low/Medium/High]. Do you want to proceed with this change? (yes / no / adjust scope)"

Do not proceed until the user confirms. This is the core safety gate.

### Phase 6 — Verify Gate

After the change is made, run `scripts/verify-gate.sh` from the project root.

The gate runs in order:
1. `tsc --noEmit` — type-check
2. `npm run lint` (if script exists)
3. `npm test` (if script exists)
4. `npm run build` (if script exists)

Stops on first failure. Color-coded output. Non-zero exit on failure.

---

## Output Format

The agent renders the JSON from `scan-impact.mjs` as:

```markdown
## Safe Change Report — src/notifications/notifications.service.ts

**Risk Score: MEDIUM**
Risk factors: 5 importers, 1 API route, test coverage exists

### Importers (5)
- src/users/users.service.ts
- src/appointments/appointments.service.ts
- src/billing/billing.service.ts
- src/reports/reports.service.ts
- src/audit/audit.service.ts

### API Routes Affected
| Controller | Endpoints |
|------------|-----------|
| NotificationsController | POST /notifications, GET /notifications |

### Test Coverage
- src/notifications/notifications.service.spec.ts ✓
- Gap: no

### ENV Variables Referenced
- SMTP_HOST
- SMTP_USER
- SMTP_PASS

### Recent Migrations (last 7 days)
- None

---
**Checkpoint:** Do you want to proceed with this change? (yes / no / adjust scope)
```

---

## Limitations

See `references/limitations.md` for the full list. Key constraints:

- Regex-based: dynamic imports (`import(path)`) are not detected
- Re-exports through barrel files (`index.ts`) may undercount importers
- Decorator aliases (custom `@Route()` wrapping `@Controller`) are not detected
- TypeScript only — no Python, Go, Rust adapters in v0.1

---

## Companion Skills

- **deep-debugging** — use after a bug ships; safe-change is what you run before
- **self-improving-agent** — log the impact report as a learning when a change causes an incident

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/scan-impact.mjs` | Builds impact map, outputs JSON |
| `scripts/verify-gate.sh` | Runs tsc → lint → test → build in sequence |

---

## File Structure

```
safe-change/
├── SKILL.md                          # This file
├── README.md                         # Marketing overview
├── package.json                      # ClawHub metadata
├── scripts/
│   ├── scan-impact.mjs               # Impact analyzer (Node ESM, no deps)
│   └── verify-gate.sh                # Verify gate (bash)
├── references/
│   ├── example-impact-report.md      # Full SMTP swap example
│   ├── usage.md                      # How agent invokes the scripts
│   └── limitations.md                # Known limitations + trade-offs
└── assets/
    └── SKILL-TEMPLATE.md             # Template for creating similar skills
```
