---
name: ux-qa-gate
description: "Self-review gate for UI/UX work before delivering to the user. Run automatically after building, modifying, or completing any user-facing feature, page, component, or flow. Triggers on: finishing a build task, completing a UI change, delivering a web app feature, wrapping up frontend work. Also use when asked to QA this, review the UX, check for usability issues, or run the gate. What it does: (1) Functional completeness check — verifies every button, link, form, and flow works end-to-end, (2) Heuristic review — walks through all 10 Nielsen Norman usability heuristics with a detailed checklist, (3) State and edge case sweep — checks empty, loading, error, success, partial, overflow, and auth states, (4) Interaction and responsiveness — verifies clickability, keyboard access, and responsive layout, (5) Severity classification — blockers and major issues fixed before delivery, minor items noted. Catches missing functionality, broken flows, empty states, and usability problems before the user sees them."
---

# UX QA Gate

Run this gate after completing any user-facing work. Do not deliver work to the user
until this gate passes.

## When to Run

- After building or modifying any page, component, or flow
- After completing a feature request
- Before saying "done" or presenting work to the user

## Process

### 1. Functional Completeness Check

Before examining UX, verify the feature actually works end-to-end:

- Every button/link has a working handler
- Forms submit and process data correctly
- Navigation flows connect (no dead ends)
- Data displays where expected (not placeholder or undefined)
- The feature does what was asked — re-read the original request

### 2. Heuristic Review

Walk through each of Nielsen's 10 heuristics against the work just completed.
Load `references/heuristics-checklist.md` and evaluate each applicable item.
Not every heuristic applies to every change — skip items that are clearly irrelevant
to the scope of work, but err on the side of checking.

### 3. State & Edge Case Sweep

Check these states exist and are handled for every data-driven view:

| State | What to verify |
|-------|---------------|
| Empty | No data yet — helpful message, not blank screen |
| Loading | Spinner, skeleton, or indicator while fetching |
| Error | Clear message with recovery path (retry, go back) |
| Success | Confirmation after actions (toast, redirect, message) |
| Partial | Some data missing — graceful degradation, not crash |
| Overflow | Long text, many items, large images handled |
| Auth | Protected routes redirect or show appropriate state |

### 4. Interaction & Responsiveness

- Click every interactive element — does it respond?
- Tab through focusable elements — logical order?
- Resize viewport — does layout hold at mobile/tablet/desktop?
- Check touch targets on mobile — minimum 44×44px

### 5. Severity Classification

For each issue found:

| Severity | Meaning | Action |
|----------|---------|--------|
| 🔴 Blocker | User cannot complete the task | Fix before delivering |
| 🟠 Major | User struggles significantly | Fix before delivering |
| 🟡 Minor | User notices but can work around | Note to user, fix if quick |
| 🔵 Enhancement | Polish or improvement | Note to user for backlog |

### 6. Decision

- **Any 🔴 or 🟠 issues** → Fix them, then re-run the gate
- **Only 🟡 or 🔵** → Deliver the work with a brief note of known issues
- **No issues** → Deliver confidently

## Output Format

When reporting to the user, keep it brief:

```
✅ QA Gate passed — [summary of what was checked]
```

Or if issues were found and fixed:

```
🔧 QA Gate — found and fixed [N] issues:
- [brief description of each fix]
```

Or if minor issues remain:

```
⚠️ QA Gate — [N] minor items noted:
- [brief description + severity]
```

Do not produce a full heuristic evaluation report unless the user asks for one.
The gate is a self-check, not a deliverable.
