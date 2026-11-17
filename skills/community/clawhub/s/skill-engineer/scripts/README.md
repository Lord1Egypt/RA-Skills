# Validation Scripts for skill-engineer

These scripts provide deterministic validation of skill artifacts. Run them during the review phase to catch errors before manual review.

## Scripts

### `validate-scorecard.sh`
**Purpose:** Verify that the Quality Scorecard in README.md has correct math (individual scores sum to claimed total).

**Usage:**
```bash
bash scripts/validate-scorecard.sh /path/to/skill/README.md
```

**Checks:**
- Parses scorecard table from README
- Sums individual category scores
- Compares to claimed total
- Exit 0 if match, exit 1 if mismatch

**When to run:** After Orchestrator adds final scorecard to README, before git push.

---

### `check-completeness.sh`
**Purpose:** Verify all required skill files exist.

**Usage:**
```bash
bash scripts/check-completeness.sh /path/to/skill/
```

**Checks:**
- Required: SKILL.md, skill.yml, README.md
- Optional (warns if missing): tests/, scripts/, references/, CHANGELOG.md

**When to run:** After Designer produces artifacts, before Reviewer evaluation.

---

### `count-rubric-checks.sh`
**Purpose:** Count quality rubric checks in SKILL.md and verify the total matches expected (33).

**Usage:**
```bash
bash scripts/count-rubric-checks.sh /path/to/skill/SKILL.md
```

**Checks:**
- Counts SQ-A, SQ-B, SQ-C, SQ-D checks
- Counts SCOPE, OPSEC, REF, ARCH checks
- Verifies total = 33

**When to run:** When designing or refactoring skill-engineer itself, to ensure rubric integrity.

---

## Integration with Reviewer Workflow

The Reviewer should run these scripts BEFORE manual evaluation:

```bash
# 1. Check file completeness
bash scripts/check-completeness.sh /path/to/skill/

# 2. Verify rubric (for skill-engineer itself)
bash scripts/count-rubric-checks.sh /path/to/skill/SKILL.md

# 3. After Orchestrator adds scorecard, validate math
bash scripts/validate-scorecard.sh /path/to/skill/README.md
```

These deterministic checks catch mechanical errors, allowing the Reviewer to focus on judgment-based evaluation (clarity, design quality, edge cases).
