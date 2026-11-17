# No Test Environment — Fallback Strategy

## Triage: Intentional or Technical Debt?

| Scenario | Classification | Strategy |
|----------|---------------|----------|
| Prototype, spike, throwaway code | Intentional — no tests needed yet | Document decision, revisit later |
| Legacy system, never had tests | Technical debt | Incremental adoption |
| New project, not set up yet | Normal stage | Build infrastructure now |
| "Too complex to test" | Architecture problem | Refactor for testability first |
| "No time" | Priority issue | Quantify risk, drive decision |

## Milestone-Based Adoption

### Milestone 1: Smoke Net

Install nothing. Create a minimal smoke script:

```bash
#!/bin/bash
# smoke.sh — Minimal safety net
curl -f http://localhost:3000/health || exit 1
curl -f http://localhost:3000/api/v1/status || exit 1
echo "Smoke passed"
```

Manual test checklist for critical paths:
```
□ User registration works
□ User login works
□ Core feature X works
□ Error case Y doesn't crash
```

### Milestone 2: Core Safety Net

- Install one test framework (matching project language)
- Write 3-5 unit tests for the most fragile module (where bugs happen most)
- Add one CI step to run tests

```yaml
# Minimal GitHub Actions test job
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
```

### Milestone 3: Layer Expansion & Dockerized Infrastructure

- Core path coverage reaches 20-30%
- Construct containerized test environment via Docker Compose or Testcontainers (real DB, Redis, services) to guarantee environment isolation
- Add integration tests (database, external APIs)
- Add 3 E2E smoke tests (if UI exists)
- Full test suite runs in CI with Docker service containers

### Milestone 4: Established Infrastructure

- All test pyramid layers covered
- Coverage reports in CI
- Pre-commit hooks (lint + unit tests)
- Flaky test handling strategy in place

## Staging-Only Testing

When local/CI test environment is impossible (legacy system, vendor lock-in, special hardware):

```bash
# Staging smoke tests
curl -f https://staging.example.com/health
curl -f https://staging.example.com/api/v1/status

# Read-only DB check
psql $STAGING_DB_URL -c "SELECT count(*) FROM users"

# Critical flow check
./scripts/staging-smoke.sh
```

**Constraints**:
- Test data must be isolated from production
- Run automatically after each deploy
- Alert on failure (Slack, PagerDuty)

## Decision Record Template

When choosing NOT to add tests:

```
## Testing Strategy Decision

### Reason for not testing
{Why specifically — not just "no time"}

### Accepted risk
{What can go wrong? How severe?}

### Alternative safeguards
{Monitoring? Alerts? Manual review? Canary deployments?}

### Re-evaluation checkpoint
{When to revisit this decision?}

### Owner
{Who made this decision?}
```
