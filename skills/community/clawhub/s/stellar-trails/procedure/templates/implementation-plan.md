# Implementation Plan

This template is the output of the PLAN phase. It translates the problem specification into a step-by-step implementation strategy with traceability IDs that connect requirements to code to verification.

## Why Traceability IDs Exist

Each implementation step receives a Traceability ID (IMPL-001, IMPL-002, etc.). During the IMPLEMENT phase, each code change references its Traceability ID. During the VERIFY phase, each verification item traces back to a Traceability ID. This chain is the primary mechanism that prevents drift between what was planned, what was built, and what was verified. If a verification item fails, the Traceability ID points directly to the implementation step and, through it, to the original requirement.

---

## Template

Copy and complete the following for every task:

```markdown
# Implementation Plan: [Task Name]

## Approach

[2-3 sentences describing the solution strategy. Explain the high-level design decision and why it was chosen over alternatives.]

## Alternatives Considered

[List 2+ alternative approaches that were considered but not chosen. 1 sentence each. Why were they rejected? This prevents binary thinking (primary OR fallback only) and encourages exploring options before committing.]

- Alt 1: [Alternative approach] — [Why rejected]
- Alt 2: [Alternative approach] — [Why rejected]

## Pre-Deploy Verification

[If this task targets an external system (Android device, remote server, cloud, production), name a local verification step that exercises the same code path before deployment. Example: "secilc local compile test on CIL policy" or "SAM local emulator test". If no external target, state "N/A".]

## Fallback Approach

[Alternative approach if the primary fails. 1-2 sentences. If no viable fallback exists, state "No viable fallback — would require user input." This feeds the Pivot's pivot recovery path.]

## Scope Boundary

| | Items |
|--|-------|
| **IN** (included) | [What this implementation covers — be specific] |
| **OUT** (excluded) | [What is explicitly NOT covered — prevents scope creep] |

## Implementation Steps

| Step | Action | Target File | Traceability ID |
|------|--------|-------------|-----------------|
| 1 | [Specific action — what code to write or change] | [File path] | IMPL-001 |
| 2 | [Specific action — what code to write or change] | [File path] | IMPL-002 |
| 3 | [Specific action — what code to write or change] | [File path] | IMPL-003 |

## Requirements Mapping

| Traceability ID | Maps to Requirement | Notes |
|-----------------|--------------------|----|
| IMPL-001 | [Functional requirement from problem spec] | [Any relevant context] |
| IMPL-002 | [Functional requirement from problem spec] | [Any relevant context] |
| IMPL-003 | [Edge case # from problem spec] | [Any relevant context] |

## Verification Strategy

| What to Verify | Method | Expected Outcome | Traceability ID |
|----------------|--------|------------------|-----------------|
| [Specific behavior or constraint] | [How to check: lint, manual test, type check, etc.] | [What a correct result looks like] | IMPL-001 |
| [Specific behavior or constraint] | [How to check] | [What a correct result looks like] | IMPL-002 |

## Dependencies

| Dependency | Install Command | Required By Step |
|------------|----------------|-----------------|
| [Package or service name] | [e.g., `bun add package-name`] | [IMPL-XXX] |

## Notes

[Any design decisions, trade-offs, or context the implementer should know]
```

---

## Field Guidance

| Field | Guidance |
|-------|----------|
| **Approach** | State the design decision clearly. If there are alternatives, explain why this one was chosen. Keep it to 2-3 sentences. |
| **Fallback Approach** | REQUIRED for Standard/Complex tasks. This is the recovery path if the primary approach fails during IMPLEMENT. It should be a concrete alternative, not "try harder." If no fallback exists (e.g., the task requires a specific library that may not support the needed feature), say so explicitly. This field feeds the Pivot — when an Wrong Approach is detected, the agent checks this field first before inventing a new approach. |
| **Scope Boundary** | REQUIRED for Standard/Complex tasks. The IN list defines what will be delivered. The OUT list defines what will NOT be delivered. The OUT list is critical for preventing scope creep — if IMPLEMENT starts producing work not in the IN list, it's a deviation. The delivery report's Scope Drift field measures this. |
| **Implementation Steps** | Each step must be specific enough that another developer could execute it without additional context. "Add a submit button" is too vague — "Add a submit button to the form in `src/app/page.tsx` that calls `handleSubmit` on click" is specific. |
| **Traceability ID** | Sequential numbering: IMPL-001, IMPL-002, etc. These IDs are referenced in code comments during IMPLEMENT and in verification items during VERIFY. |
| **Requirements Mapping** | Every functional requirement and edge case from the problem specification must appear here. This confirms nothing was dropped between specification and planning. |
| **Verification Strategy** | Define verification before writing code. This prevents the common failure mode of writing tests that pass trivially because they were designed after the code was already written. |
| **Dependencies** | If a new package is needed, specify the install command. The implementer must install it before writing code that depends on it. |

---

## Complexity Tier Abbreviation

For simple tasks, this template is combined with the problem specification template into a single output. All fields from both templates must still be present. The combined document is presented to the user as one artifact for approval.
