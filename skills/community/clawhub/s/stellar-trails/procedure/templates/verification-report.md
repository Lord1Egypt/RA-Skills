# Verification Report

This template is the output of the VERIFY phase. It documents systematic checks that confirm the implementation satisfies the requirements and handles edge cases correctly.

## Why Structured Verification Exists

Ad hoc verification ("it seems to work") is unreliable because it depends on the verifier's mood and attention in the moment. A structured report forces the agent to check every requirement, every traceability ID, and every edge case — nothing is left to assumption. The report also serves as an audit trail: if a bug surfaces later, the verification report shows what was checked and what passed.

---

## Compact Template (Simple Tasks)

For Simple tasks (single file, no schema change), use this abbreviated format:

```markdown
# Verification Report: [Task Name]

| Check | Status | Note |
|-------|--------|------|
| Lint / Type Check | PASS / FAIL | |
| Key behavior verified | PASS / FAIL | |
| Edge cases tested | PASS / FAIL | |
| Defects found | [n] | Fixed: [n] |
| Overall | PASS / FAIL | |
```

## Full Template (Standard/Complex Tasks)

Copy and complete the following after the IMPLEMENT phase:

```markdown
# Verification Report: [Task Name]

## Automated Checks

| Check | Tool/Command | Expected Result | Actual Result | Status |
|-------|-------------|-----------------|---------------|--------|
| Lint | `bun run lint` | No errors | [Paste relevant output] | PASS / FAIL |
| Type Check | `bunx tsc --noEmit` | No type errors | [Paste relevant output] | PASS / FAIL |
| Tests | `bun test` | All tests pass | [Paste relevant output] | PASS / FAIL |

## Pre-Deploy Verification

| Check | Method | Expected Result | Actual Result | Status |
|-------|--------|-----------------|---------------|--------|
| [Pre-Deploy step from Scope, or N/A] | [e.g., `secilc` local compile, SAM emulator] | [Expected outcome] | [Actual outcome] | PASS / FAIL / N/A |

If Scope's Pre-Deploy field is "N/A" (no external target), mark this entire section as N/A and skip.

## Traceability Verification

| Traceability ID | Implementation Verified | Verification Method | Status |
|-----------------|------------------------|---------------------|--------|
| IMPL-001 | [Brief description of what was verified] | [How it was checked] | PASS / FAIL |
| IMPL-002 | [Brief description of what was verified] | [How it was checked] | PASS / FAIL |
| IMPL-003 | [Brief description of what was verified] | [How it was checked] | PASS / FAIL |

## Edge Case Verification

| Edge Case | Test Input | Expected Behavior | Actual Behavior | Status |
|-----------|-----------|-------------------|-----------------|--------|
| [Edge case from problem spec] | [Concrete input used to test] | [What should happen] | [What actually happened] | PASS / FAIL |
| [Edge case from problem spec] | [Concrete input used to test] | [What should happen] | [What actually happened] | PASS / FAIL |

## Review Checklist

| Check | Status |
|-------|--------|
| No `any` type used | PASS / FAIL / N/A |
| Explicit return types on all functions | PASS / FAIL / N/A |
| No `console.log` in delivered code | PASS / FAIL / N/A |
| No dead code (unused imports, variables, functions) | PASS / FAIL / N/A |
| Error paths handled (no silent try-catch) | PASS / FAIL / N/A |
| Single responsibility per function | PASS / FAIL / N/A |
| No function exceeds 50 lines | PASS / FAIL / N/A |
| Imports ordered correctly | PASS / FAIL / N/A |
| Source data verified against authoritative source (remote/origin) | PASS / FAIL / N/A |

## Summary

| Metric | Value |
|--------|-------|
| Total automated checks | [n] |
| Automated checks passed | [n] |
| Total traceability items | [n] |
| Traceability items passed | [n] |
| Total edge cases verified | [n] |
| Edge cases passed | [n] |
| Defects found during verification | [n] |
| Defects fixed before attestation | [n] |
| Overall result | PASS / FAIL |

## Outcome Statement

[In 1-2 sentences, state whether the code satisfies all requirements from the problem specification. If defects were found and fixed, describe them here. If the overall result is FAIL, explain what failed and why delivery is blocked.]

## Failures (if any)

[If any check failed, describe the failure, the root cause, and the fix applied. If no failures, write "None."]
```

---

## Field Guidance

| Field | Guidance |
|-------|----------|
| **Automated Checks** | Run the actual commands and paste real output. Do not write "looks fine" — paste the terminal output. If a linter is not available for the language, note "No linter available" in the Tool/Command column and mark N/A. |
| **Traceability Verification** | Every Traceability ID from the implementation plan must appear here. The verification method should be concrete: "manually traced code flow with input X" or "confirmed function returns expected type." |
| **Edge Case Verification** | Use concrete test inputs, not abstract descriptions. "Empty array" is abstract — `items = []` is concrete. |
| **Review Checklist** | Adapt the checklist to the language and framework. Items marked N/A should still appear in the table — they are excluded from the pass/fail count. |
| **Failures** | If a check fails, do not proceed to DELIVER. Document the failure, fix it, and re-run verification. The incident report template at `procedure/templates/incident-report.md` may be used for significant failures. |
| **Defects found/fixed** | These two numbers must match unless there are unresolved defects. If defects found > defects fixed, the overall result must be FAIL and delivery is blocked. |
| **Outcome Statement** | This is the single source of truth for the QA Attestation OUTCOME row. It must be a specific claim about the code, not a process description. "Code satisfies all 4 requirements" is valid. "Verification was performed" is not — that's a process claim, not an outcome claim. |

---

## Verification Failure Protocol

If any item in this report has a FAIL status:

1. Do not transition to DELIVER.
2. Determine whether the failure is a code defect or a specification gap.
   - Code defect → fix the code, return to VERIFY, re-run the full report.
   - Specification gap → return to SPECIFY, update the specification, re-plan, re-implement, re-verify.
3. If the failure is ambiguous, ask the user for guidance before choosing a path.
