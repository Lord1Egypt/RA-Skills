# Quality Enhancements — Checkpoints, Checklists, and Automation

This document describes optional quality enhancements that can be added to any SPM project to strengthen delivery confidence. These enhancements are inspired by professional software engineering practices and are **recommended for production or multi-contributor projects**.

---

## Implementation Phases

These enhancements are delivered in two phases:

### Phase 1 (Implemented Now)

- **Checkpoint Hard Stops** — Templates in `CHECKPOINTS/`, runner `scripts/checkpoint.sh`
- **Checklist Self-Review** — Templates in `CHECKLISTS/`, validator `scripts/verify_checklists.py`

**Setup:**
```bash
cd your-spm-project
bash skills/spm/scripts/setup-checkpoints.sh
```

This installs templates, scripts, and npm wrappers. See usage guide below.

### Phase 2 (Optional — Contract, E2E, Config)

- **Single Source of Truth** — `api/openapi.yaml` + `scripts/generate.sh` + `scripts/validate_contract.sh`
- **End-to-End Automation** — `scripts/e2e.sh` (build → test → deploy → health check)
- **Configuration-as-Code** — `config/default.yaml` + `src/config/` loader

Enable after Phase 1 is stable. See respective sections for details.

---

## 1. Checkpoint Hard Stops

### Purpose

Prevent drifting by forcing a deliberate pause at critical junctures. The agent generates a structured report, asks for user confirmation, and only proceeds with explicit approval.

### Checkpoints

| Checkpoint | When | Template |
|------------|------|----------|
| **Phase 1 — Requirements** | After `docs/requirements.md` written | `CHECKPOINTS/PHASE-1-REQUIREMENTS.md` |
| **Phase 2 — Planning** | After WBS ledger created (`docs/spm/ledger.md`) | `CHECKPOINTS/PHASE-2-PLANNING.md` |
| **Phase 3 — Execution** | At each milestone completion | `CHECKPOINTS/PHASE-3-EXECUTION.md` |
| **Phase 5 — Delivery** | Before production deployment | `CHECKPOINTS/PHASE-5-DELIVERY.md` |

### Usage

```bash
# After completing Phase 1 work
./scripts/checkpoint.sh phase-1

# The script generates a timestamped report in docs/checkpoints/
# Fill in the blanks (answers, evidence paths), then present to user.

# After user approves, proceed to next phase.
```

### Integration with Workflows

Each phase's workflow should include a step:

- **Phase 1 Workflow** → after brainstorming/design doc, run `./scripts/checkpoint.sh phase-1` → user confirms → proceed to Planning
- **Phase 2 Workflow** → after WBS created, run `./scripts/checkpoint.sh phase-2` → user confirms → proceed to Execution
- **Phase 3 Workflow** → after milestone tasks done, run `./scripts/checkpoint.sh phase-3` → user confirms → next milestone
- **Phase 5 Workflow** → after E2E passed, run `./scripts/checkpoint.sh phase-5` → user authorizes deploy

If user requests revisions, go back and update artifacts, then re-run checkpoint.

---

## 2. Checklist-Driven Self-Review

### Purpose

Move from "I think it's done" to "I verified every item on the list". Checklists are the acceptance criteria for each type of work.

### Checklists

| Checklist | When | Automated? |
|-----------|------|------------|
| `CODE-COMPLETION.md` | Before marking any code task `done` | Partially (type check, lint, tests, secrets, coverage, no console.log) |
| `DEPLOYMENT-READINESS.md` | Before deploying to any environment | Partially (E2E existence, .env.example, config file, health URL) |
| `ARCHITECTURE-REVIEW.md` (future) | After architecture design, before implementation | Low (mostly manual) |
| `TEST-COVERAGE.md` (future) | When creating test plan | Medium (coverage thresholds) |

### Automated Verification

Run `./scripts/verify_checklists.py` to check the automated items:

```bash
# Check all automated items
npm run verify:checklists   # or: python3 scripts/verify_checklists.py all

# Check only code-related items
npm run verify:code

# Check only deployment items
npm run verify:deploy
```

Output:
- Console summary with ✅/❌ per item
- JSON report at `docs/checklists/verification-report.json` (attach to checklist)

### Manual Completion

For items that need human judgment (edge cases, performance, design), answer directly in the checklist markdown before submitting for review.

### Rule

**No task can be marked `done` until its corresponding checklist is fully completed and evidence attached.** The WBS `Evidence` column should reference the filled checklist file (e.g., `docs/checklists/code-completion-2024-05-09.md`).

---

## 3. Single Source of Truth (Contract Management)

### Problem

Without a central contract, the backend, frontend, and other services can drift apart: different field names, types, required/optional mismatches.

### Solution

Define API contracts in `api/openapi.yaml` (OpenAPI 3) or `schemas/*.json` (JSON Schema). Generate types and clients from it.

### Recommended: OpenAPI-First

1. **Create `api/openapi.yaml`**
   - Define all endpoints, request/response schemas, error codes
   - This is the **single source of truth** for the API contract

2. **Generate Code**
   ```bash
   ./scripts/generate.sh
   ```
   What it does:
   - Generates TypeScript types for Worker: `src/worker/generated/api-types.ts`
   - Generates API client for Pages: `src/pages/src/api/generated/client.ts`
   - Optionally generates HTML docs: `docs/API.html`

3. **Implement Handlers**
   - Worker code imports types from `generated/api-types.ts`
   - Pages code uses `generated/client.ts` to call API
   - **Never** hand-write types that duplicate the spec

4. **Validate Contract**
   ```bash
   ./scripts/validate_contract.sh
   ```
   Checks that generated files are up-to-date with the spec.

### CI Enforcement

Add to `.github/workflows/`:
```yaml
- name: Validate API Contract
  run: ./scripts/validate_contract.sh
```

Any PR that modifies API without updating `openapi.yaml` will fail.

---

## 4. End-to-End Automation

### Purpose

One script to prove the entire pipeline works: build → deploy → smoke test → health check.

### Script: `scripts/e2e.sh`

Usage:
```bash
./scripts/e2e.sh
```

What it does:
1. Clears staging database (safe because staging is disposable)
2. Runs build and test on the project
3. Calls Worker ingest API
4. Verifies data landed in D1 (row count check)
5. Deploys Pages to staging
6. Runs Playwright smoke test (chart renders, crosshair works)
7. Prints ✅ or ❌ summary

### Output

If all passes:
```
✅ E2E Pipeline PASSED
  • Build:    ✓ (exit 0)
  • Test:     ✓ (47/47 pass)
  • Ingest API: ✓ (SPY=247 rows)
  • Frontend:   ✓ (chart rendered, crosshair works)
```

If any step fails, the script exits non-zero and prints the failure point.

### CI Integration

Add `.github/workflows/e2e.yml`:
```yaml
on: [pull_request]
jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: ./scripts/e2e.sh
        env:
          STAGE: staging
          STAGING_TOKEN: ${{ secrets.STAGING_TOKEN }}
```

PR cannot merge unless E2E passes.

---

## 5. Configuration-as-Code

### Purpose

Hard-coded values (coverage targets, heartbeat intervals, reviewer settings) force code changes for simple tweaks. Externalize them to config files that can be adjusted without rebuilding.

### Structure

```
config/
├── default.yaml        # Default values (committed)
├── production.yaml     # Overrides (gitignored)
├── staging.yaml        # Overrides (gitignored)
└── indices.yaml        # Indicator parameters (committed)

src/config/
├── index.ts            # Loader (loads proper env file)
├── schema.ts           # Zod validation schema
└── validators.ts       # Custom validation (e.g., range checks)
```

### Example `config/default.yaml`

```yaml
project:
  execution_mode: subagent
  parallel_subagents: true

quality:
  coverage_target: 80
  auto_checkpoint: true

tracking:
  heartbeat_interval: 10m

logging:
  level: info
  format: json
```

### Usage in Code

```typescript
import { get } from '@/config';

const COVERAGE_TARGET = get('quality.coverage_target');  // 80
const EXEC_MODE = get('project.execution_mode');  // "subagent"
```

### Override per Environment

- `config/staging.yaml` can set `logging.level: debug` to increase verbosity for staging
- Production secrets (API keys) go in `config/production.yaml` (gitignored) or cloud environment variables

### Validation

On startup, load config and validate against Zod schema. Fail fast if invalid.

---

## Enabling in an Existing Project

Run the setup script:

```bash
cd /path/to/spm-project
bash skills/spm/scripts/setup-checkpoints.sh
```

This will:
- Copy `CHECKPOINTS/` templates to project root
- Copy `CHECKLISTS/` templates
- Install `scripts/checkpoint.sh` and `scripts/verify_checklists.py`
- Add npm scripts to `package.json` (if present)
- Create `docs/checkpoints/` and `docs/checklists/` directories

After setup:
1. Use checklists for upcoming tasks
2. Run checkpoints at phase boundaries
3. (Optional) Add OpenAPI contract and generation scripts if API-heavy project

---

## Incremental Adoption Guide

| Maturity | Checklist | Checkpoint | Contract | E2E | Config |
|----------|-----------|-----------|----------|-----|--------|
| **Level 1** (Starter) | Use CODE-COMPLETION.md (manual fill) | Use PHASE-1/PHASE-2 templates (manual fill) | None | None | None |
| **Level 2** (Automated QA) | Run `verify:code` + `verify:deploy` scripts | Auto-fill blanks from actual files | None | Run `e2e.sh` manually before deploy | Basic `.env.example` |
| **Level 3** (Contract-First) | Full checklist suite | Checkpoint auto-gathers data from ledger/config | Implement `api/openapi.yaml` + `generate.sh` | Add CI E2E stage | Full config schema |
| **Level 4** (Production-Grade) | All checklists + automated gates | Checkpoint blocks PR merge until approved | Contract validation in CI | E2E required on PR | Config validation on startup, env-specific overrides |

**Start at Level 1** — even manual checklists are better than none. Automate gradually.

---

## FAQ

**Q: This feels heavy for a small project.**  
A: Start with only Phase 1 checkpoint and CODE-COMPLETION checklist. Drop the rest if unnecessary. These tools exist to scale; for a 1-day task you may skip them.

**Q: My project doesn't use Cloudflare Workers/Pages.**  
A: The patterns are platform-agnostic. Replace `wrangler` commands with your own deploy tooling. E2E script should reflect your actual stack.

**Q: Do I have to use OpenAPI?**  
A: No. You can use JSON Schema (`schemas/`) or even shared TypeScript package (`spm-common`). The principle is "single source", not the specific format.

**Q: How do I know which checklist to use?**  
A: CODE-COMPLETION for any code task; DEPLOYMENT-READINESS for going live. Add more as needed (e.g., ARCHITECTURE-REVIEW after spec).

---

## Conclusion

These five enhancements transform SPM from "just a workflow" to a **production-grade delivery system**. They add friction, but that friction is *intentional* — it catches problems before they become costly.

Start small. Adopt one mode at a time. Let the project's complexity dictate which gates are necessary.
