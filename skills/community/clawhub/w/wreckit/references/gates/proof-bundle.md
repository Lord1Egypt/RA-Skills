# Gate: Proof Bundle (all modes, always last)

**Question:** Can you prove it works?

## Output Structure

Commit to repo:
```
.wreckit/
├── proof.json             # Gate results, timestamps, pass/fail, mode, iterations
├── plan.md                # Final IMPLEMENTATION_PLAN.md state
├── slop-report.md         # AI slop findings
├── type-check.log         # Raw type checker output
├── test-quality.md        # Assertion density, coverage, edge cases
├── mutations.md           # Mutation kill results + survivors
├── judge-review.md        # LLM-as-judge results (if applicable)
├── cross-verify.md        # Re-gen diff (BUILD mode)
├── behavior-capture.md    # Golden fixtures (REBUILD mode)
├── regression.md          # Regression results (REBUILD/FIX mode)
├── security-review.md     # SAST findings (FIX mode)
├── dashboard.json         # Machine-readable results for dashboard
└── decision.md            # Ship / Caution / Blocked + reasoning
```

## Decision Framework

| Verdict | Criteria |
|---------|----------|
| **Ship** ✅ | All gates pass, ≥95% mutation kill, zero slop, subjective met |
| **Caution** ⚠️ | All gates pass, mutation kill 90-94%, or minor slop in non-critical, or judge needed 2+ iterations |
| **Blocked** 🚫 | Any gate fails, hallucinated deps, <90% mutation kill, or hard cap hit |
