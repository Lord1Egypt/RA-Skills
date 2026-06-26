# IDS UI Doctor Report Template

Use this template when generating compliance reports.

```markdown
# IDS UI Doctor Report

**Application:** [App Name]
**Date:** [Audit Date]
**Overall Score:** [X/100]

## Executive Summary

[2-3 sentence summary of overall IDS compliance status]

## Score Breakdown

| Category                | Score | Max     | Status   |
| ----------------------- | ----- | ------- | -------- |
| IDS Component Usage     | X     | 25      | 🔴/🟡/🟢 |
| IDS Pattern Compliance  | X     | 20      | 🔴/🟡/🟢 |
| Accessibility           | X     | 20      | 🔴/🟡/🟢 |
| Design Token Compliance | X     | 15      | 🔴/🟡/🟢 |
| Layout & Spacing        | X     | 10      | 🔴/🟡/🟢 |
| Provider & Setup        | X     | 10      | 🔴/🟡/🟢 |
| **Total**               | **X** | **100** |          |

### Scoring Guide

- 🟢 **90–100%** — Excellent IDS compliance
- 🟡 **60–89%** — Moderate compliance, improvements needed
- 🔴 **Below 60%** — Significant gaps, prioritise remediation

## Detailed Findings

### IDS Component Usage (X/25)

#### Components Correctly Used

- [List of IDS components found and correctly used]

#### Missing IDS Component Opportunities

| Location    | Current Code | Recommended IDS Component | Priority |
| ----------- | ------------ | ------------------------- | -------- |
| [file:line] | `<button>`   | `IressButton`             | High     |
| ...         | ...          | ...                       | ...      |

### IDS Pattern Compliance (X/20)

#### Pattern Usage

| Location    | Current Pattern               | Recommended IDS Pattern        | Priority |
| ----------- | ----------------------------- | ------------------------------ | -------- |
| [file:line] | Custom `<form>` with useState | `IressForm` + `IressFormField` | High     |
| [file:line] | Custom loading spinner        | `IressLoading pattern="page"`  | High     |
| [file:line] | Custom context menu           | `IressContextualMenu`          | Medium   |
| ...         | ...                           | ...                            | ...      |

### Accessibility (X/20)

#### Issues Found

| Location    | Issue                        | Severity | WCAG Criterion               |
| ----------- | ---------------------------- | -------- | ---------------------------- |
| [file:line] | Input missing label          | Critical | 1.3.1 Info and Relationships |
| [file:line] | No skip link                 | High     | 2.4.1 Bypass Blocks          |
| [file:line] | Colour-only status indicator | High     | 1.4.1 Use of Color           |
| [file:line] | Missing alt text on image    | Medium   | 1.1.1 Non-text Content       |
| ...         | ...                          | ...      | ...                          |

### Design Token Compliance (X/15)

#### Hardcoded Values Found

| Location    | Current Value | Recommended Token     | Category |
| ----------- | ------------- | --------------------- | -------- |
| [file:line] | `#003271`     | `colour.primary.fill` | Colour   |
| [file:line] | `16px`        | `spacing.4`           | Spacing  |
| ...         | ...           | ...                   | ...      |

### Layout & Spacing (X/10)

#### Custom Layout Patterns

| Location    | Current Pattern                         | IDS Alternative |
| ----------- | --------------------------------------- | --------------- |
| [file:line] | `display: flex; flex-direction: column` | `IressStack`    |
| ...         | ...                                     | ...             |

### Provider & Setup (X/10)

- [ ] IressProvider wraps application root (or IressShadow, which is a superset)
- [ ] `@iress-oss/ids-components/dist/style.css` imported (not needed if using IressShadow)
- [ ] `@iress-oss/ids-tokens/build/css-vars.css` imported (only if using tokens directly)
- [ ] `react-hook-form` installed (if using IressForm)
- [ ] No conflicting CSS resets

## Recommendations Summary

### Critical (Fix Immediately)

1. [Finding and remediation]

### High Priority (Current Sprint)

1. [Finding and remediation]

### Medium Priority (Next Sprint)

1. [Finding and remediation]

### Low Priority (Backlog)

1. [Finding and remediation]

## IDS Components Available But Not Used

[List any IDS components that could benefit the application but are not currently imported]
```
