---
name: testing-strategy
description: Deep testing strategy workflow—risk mapping, test pyramid, levels of isolation, flakiness, data, CI gates, and quality signals beyond coverage %. Use when designing test approach, fighting flaky CI, or restructuring QA vs dev ownership.
---

# Testing Strategy (Deep Workflow)

Testing strategy answers: **what failures would hurt users**, **what’s cheap to catch**, and **what signals we trust in CI**. Coverage percentage alone is a weak proxy—**risk alignment** matters.

## When to Offer This Workflow

**Trigger conditions:**

- New service or major refactor; “what should we test?”
- Flaky CI, long runtimes, or tests nobody trusts
- Debate: unit vs integration vs e2e; QA headcount vs automation

**Initial offer:**

Use **six stages**: (1) risk & quality goals, (2) pyramid & layers, (3) design per layer, (4) data & environments, (5) CI & gates, (6) observability of test health. Confirm **release cadence** and **regulatory** needs.

---

## Stage 1: Risk & Quality Goals

**Goal:** Connect tests to **user impact** and **business risk**.

### Questions

1. Worst **failure categories**: payments wrong, data leak, outage, wrong advice (AI)?
2. **SLO** for critical paths—what must never break silently?
3. **Change velocity**—how fast must PRs merge safely?

### Output

**Risk register** → **test priorities** (not every line equally important).

**Exit condition:** Top **5 risks** have explicit **test intent**.

---

## Stage 2: Pyramid & Layers

**Goal:** **Many fast tests**, **some integration**, **few e2e**—proportion tuned to risk.

### Layers (typical)

- **Unit**: pure logic, cheap, deterministic
- **Integration**: DB, queue, real dependencies in containers—slower but valuable
- **Contract**: between services—consumer-driven contracts when decoupled teams
- **E2E**: full stack—expensive; **minimal happy path + critical regressions**

### Anti-patterns

- **E2E-only** (slow, flaky)
- **Mock everything** (misses real integration bugs)

**Exit condition:** Written **policy**: what belongs in each layer for this codebase.

---

## Stage 3: Design Per Layer

**Goal:** Tests are **readable**, **stable**, and **debuggable**.

### Unit

- **Given/when/then** clarity; **avoid** testing implementation details
- **Property-based** tests for tricky invariants (dates, money, parsers)

### Integration

- **Testcontainers** or docker-compose in CI; **migrations** applied
- **Parallel** safe—unique DB schemas or transactions

### E2E

- **Stable selectors** (data-testid); **retry** policy disciplined—**fix flakes**, don’t hide them
- **Seed data** minimal; **idempotent** setup

**Exit condition:** **Flake** classification process exists (quarantine + ticket).

---

## Stage 4: Data & Environments

**Goal:** **Representative** data without **PII** leakage.

### Practices

- **Fixtures** versioned; **factories** for variations
- **Anonymized** prod-like datasets for perf tests—**governance** for access
- **Env parity**: staging behaves like prod enough for meaningful e2e

**Exit condition:** Data **generation** documented; **secrets** not in tests.

---

## Stage 5: CI & Gates

**Goal:** **Fast feedback** on PRs; **nightly** heavier suites if needed.

### Tiers

- **PR**: lint, unit, fast integration subset
- **Main**: full integration; **optional** e2e against ephemeral env
- **Release**: smoke + canary in prod

### Metrics

- **Flake rate**, **duration**, **quarantined** tests count—**visible**

**Exit condition:** **Merge policy** tied to green checks; **exceptions** process defined.

---

## Stage 6: Test Health & Culture

**Goal:** Tests are **owned** like features.

### Practices

- **Ownership** per suite; **on-call** for CI when org size supports
- **Delete** tests that don’t pay rent—**or** fix them

---

## Final Review Checklist

- [ ] Risks mapped to test layers
- [ ] Pyramid policy documented
- [ ] Flake management process exists
- [ ] CI tiers match team velocity
- [ ] Data/fixture strategy safe and maintainable

## Tips for Effective Guidance

- Recommend **testing seams**: boundaries where contracts are stable.
- Warn against **snapshot abuse** for large UI—**diff noise** kills trust.
- For **AI/LLM**, discuss **eval harnesses** beyond classic unit tests.

## Handling Deviations

- **Legacy untestable code**: **characterization tests** then refactor seams.
- **Startup speed**: **smoke** + **critical path** first; expand as pain appears.
