# Incident Report

This template is used when an error occurs during any phase (SPECIFY, PLAN, IMPLEMENT, or VERIFY). It captures the error context, diagnoses the root cause, and defines the fix before any recovery action is taken. For Wrong Approachs (where the fundamental approach is wrong rather than a simple code bug), the template supports pivot documentation.

## Why Structured Incident Reports Exist

When an error occurs, the instinct is to fix it quickly and move on. This leads to treating symptoms instead of root causes, and to fixes that introduce new problems. The incident report forces a pause: capture the error, classify it, analyze the root cause, and evaluate side effects before applying any fix. This prevents cascading failures and ensures the error is fully understood before resolution.

---

## Template

Copy and complete the following when an error is encountered:

```markdown
# Incident Report

## Error Capture

| Field | Value |
|-------|-------|
| Phase When Error Occurred | SPECIFY / PLAN / IMPLEMENT / VERIFY |
| Error Message | [Exact error text — paste verbatim] |
| Error Classification | Compilation / Runtime / Network / Type / Database / Git / Version Control / Wrong Approach / Other |
| Stack Trace | [If available — paste in full] |
| Context | [What the agent was doing when the error occurred] |

## Root Cause Analysis

| Question | Answer |
|----------|--------|
| What failed? | [Precise description of the failure] |
| Why did it fail? | [Chain of causation — not just the immediate trigger] |
| Is this a symptom or root cause? | [Symptom / Root cause — if symptom, identify the root cause] |
| Could this error recur in other parts of the codebase? | [Yes / No — if Yes, list other locations] |

## Pivot Assessment

| Field | Value |
|-------|-------|
| Is Wrong Approach? | YES / NO |
| Pivot Signal | [Which signal triggered this: 50%+ rewrite / same error after 2 attempts / missing library feature / data model change / N/A] |
| Fallback Available? | YES / NO — if YES, reference the Scope's Fallback Approach |
| Fallback Viable? | [Is the fallback still viable given what was learned from the failure?]
| New Approach | [Describe the alternative approach — either the fallback or a new one] |
| User Approval Required? | YES / NO |

If Wrong Approach is YES, stop fixing the current approach and follow the pivot flow in `procedure/decision-trees/error-resolution.md`. If Bug, write N/A in all fields above and proceed to Proposed Fix.

## Proposed Fix

| Field | Value |
|-------|-------|
| Fix Description | [What change will resolve the root cause] |
| Files Modified | [List each file and what changes] |
| Has Side Effects? | YES / NO |
| Side Effect Details | [If YES: describe each side effect — file deletion, data loss, config changes, behavior changes in other components] |
| User Approval Required? | YES / NO |

## Resolution

| Field | Value |
|-------|-------|
| Fix Applied | [Description of what was actually done] |
| Return Phase | [Which phase to return to: VERIFY / IMPLEMENT / SPECIFY] |
| Re-verification Required? | YES / NO |
```

---

## Field Guidance

| Field | Guidance |
|-------|----------|
| **Phase When Error Occurred** | The phase that was active when the error was detected. This determines the return target after the fix. |
| **Error Message** | Paste the exact error text. Do not summarize or paraphrase — the exact wording often contains diagnostic clues. |
| **Error Classification** | Use the categories from the error resolution decision tree (`procedure/decision-trees/error-resolution.md`). **Wrong Approach** is for cases where the fundamental design/approach is wrong, not just a code bug. This classification triggers the Pivot instead of the normal fix-verify cycle. |
| **Pivot Assessment** | REQUIRED when error classification is Wrong Approach. If Bug, write N/A. Documents the alternative approach considered and the pivot rationale. References the Scope's Fallback Approach when available. |
| **Context** | What was the agent doing? Which Traceability ID was being implemented? What command was running? |
| **Root Cause Analysis** | The "Why did it fail?" question should go at least two levels deep. "The function threw because `x` was undefined" is level one. "The function threw because `x` was undefined because the database query returns null for new users" is level two. |
| **Side Effects** | A side effect is any change that goes beyond fixing the error itself. This includes: deleting files, modifying configuration, changing behavior in unrelated code, dropping database data, or altering git history. If any side effect exists, user approval is required before proceeding. |
| **Return Phase** | The default return target after a fix is VERIFY. Return to IMPLEMENT if the fix was incomplete. Return to PLAN if this is an Wrong Approach (with pivot). Return to SPECIFY if the error reveals a gap in the requirements or a misunderstanding of the problem. |
| **Re-verification** | Always YES after a fix. Even if the fix was trivial, re-run the verification report to confirm nothing was broken. |

---

## User Approval Threshold

User approval is required when the proposed fix has side effects. Side effects include but are not limited to:

- Deleting or renaming files
- Modifying git history (rebase, force push, reset)
- Dropping or altering database data
- Changing configuration that affects other parts of the system
- Installing or removing dependencies that other code depends on

If no side effects exist, the fix may be applied and re-verified without asking the user. When in doubt, ask.
