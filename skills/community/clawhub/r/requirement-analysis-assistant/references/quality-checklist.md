# Requirement Quality Checklist

Use this checklist to review a draft PRD or to self-check generated output.

## Completeness

- The business objective is clear.
- The target user and platform are clear.
- The core user path is complete.
- The scope and non-scope are separated.
- Functional rules are specific enough for engineering.
- Interaction states are covered.
- Admin and configuration rules are included when relevant.
- Data and analytics needs are defined.
- Edge cases are listed.
- Acceptance criteria are testable.
- Open questions are visible.

## Risk Levels

Use these levels when reviewing:

- P0 risk: Blocks launch, breaks core flow, creates payment/security/compliance risk, or causes data loss.
- P1 risk: Causes major ambiguity, rework, operational inefficiency, or poor user experience.
- P2 risk: Minor enhancement, wording issue, or non-blocking detail.

## Review Output Format

When reviewing an existing PRD, lead with findings:

| Severity | Issue | Why It Matters | Suggested Fix |
| --- | --- | --- | --- |
| P0/P1/P2 |  |  |  |

Then provide:

- Missing information
- Suggested clarification questions
- Revised section drafts
- Launch and QA focus

## Functional Rule Checks

Check whether each function includes:

- Trigger condition
- Entry point
- User action
- System response
- Success state
- Failure state
- Permission rule
- Data rule
- Configuration dependency
- Acceptance criteria

## Interaction Checks

Check:

- Loading state
- Empty state
- Error state
- Disabled state
- Repeat click or duplicate submit
- Back and refresh behavior
- Login expiration
- Mobile and desktop differences
- Dialog close behavior
- Toast or notification wording

## Admin Checks

Check:

- Required fields
- Field validation
- Default values
- Draft and publish lifecycle
- Effective time and timezone
- Review workflow
- Role permission
- Operation log
- Rollback
- Conflict handling

## Data Checks

Check:

- Event names
- Trigger points
- Event properties
- Funnel definition
- Success metric
- Report dimensions
- Data owner
- Refresh frequency
- Data reconciliation needs

## Common Red Flags

- "Support configuration" is written without fields or rules.
- "Show error message" is written without specific error conditions.
- Payment or reward logic has no idempotency or duplicate handling.
- SDK requirements lack version compatibility and error codes.
- Activity rules lack timezone or effective time.
- Data requirements lack event trigger and property definitions.
- Acceptance criteria are written as vague statements.
- AI-generated assumptions are mixed with confirmed facts.
