# PRD Output Template

Use this template to create a structured product requirement draft. Respond in the user's language unless they ask otherwise.

## 1. Requirement Summary

- Requirement name:
- Scenario:
- Request source:
- Target users:
- Target platform:
- Priority:
- Expected launch window:
- Current status:

## 2. Background And Objective

Cover:

- Business background
- Current problem or opportunity
- Why this should be done now
- Success metric
- Business value

Suggested format:

| Item | Content |
| --- | --- |
| Background |  |
| Problem |  |
| Objective |  |
| Success metric |  |
| Value |  |

## 3. User Scenarios

For each scenario, describe:

- User role
- Trigger
- Entry point
- User goal
- Main path
- Alternative or failure path

Suggested format:

| Scenario | User | Trigger | Expected Result |
| --- | --- | --- | --- |
|  |  |  |  |

## 4. Scope

### In Scope

List the features that must be delivered in this requirement.

### Out Of Scope

List features that are explicitly excluded from this release.

### Dependencies

List dependencies such as backend service, SDK version, payment channel, third-party platform, campaign operation, legal review, or data platform.

## 5. Functional Breakdown

For each function, use this format:

| Field | Description |
| --- | --- |
| Function name |  |
| User story |  |
| Trigger condition |  |
| Display rule |  |
| Operation rule |  |
| Data rule |  |
| Permission rule |  |
| Configuration rule |  |
| Exception handling |  |
| Acceptance criteria |  |

## 6. Interaction Rules

Cover the following when relevant:

- Page flow
- Button state
- Form validation
- Dialog, toast, loading, and success feedback
- Empty state
- Error state
- Login or authorization state
- Mobile and desktop differences
- Repeat operation handling
- Refresh, back, and deep-link behavior

## 7. Admin And Configuration

Include this section when operators or admins need to configure the feature.

Suggested field table:

| Field | Type | Required | Default | Validation | Effective Rule | Notes |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

Cover:

- Role and permission
- Draft, publish, pause, resume, and offline states
- Effective time and timezone
- Audit or approval flow
- Operation log
- Rollback rule

## 8. Data And Analytics

Cover:

- Event tracking
- Funnel metrics
- Conversion metric
- Revenue or reward metric
- Report dimensions
- Data refresh frequency
- Data ownership

Suggested event format:

| Event | Trigger | Properties | Purpose |
| --- | --- | --- | --- |
|  |  |  |  |

## 9. Edge Cases

Common cases:

- User not logged in
- User has no permission
- Campaign not started
- Campaign ended
- Configuration missing
- Reward inventory insufficient
- Duplicate submission or duplicate claim
- Network failure
- API timeout
- Payment callback delayed
- SDK version incompatible
- Data synchronization failed

## 10. Priority

Use:

- P0: Required for the core flow to work.
- P1: Important for experience, efficiency, or launch quality.
- P2: Useful enhancement that can be deferred.

## 11. Acceptance Criteria

Write clear, testable criteria:

- Given a condition, when a user takes an action, then the expected result occurs.
- Include normal flow, edge cases, admin configuration, and data verification.
- Avoid vague criteria such as "works normally" or "good experience".

## 12. Open Questions

Separate questions by owner when possible:

| Question | Owner | Impact | Suggested Deadline |
| --- | --- | --- | --- |
|  |  |  |  |

## 13. Product Value

Summarize:

- Value to users
- Value to business teams
- Value to product and operations
- Value to engineering and QA
- Value to data review and iteration
