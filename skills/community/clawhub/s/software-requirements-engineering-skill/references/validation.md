# Requirements Validation Reference

Use this for requirements reviews, inspections, validation, verification, defect logging, acceptance criteria, and test requirements.

## Table of Contents

- Validation and Verification
- Review Types
- Inspection Roles
- Inspection Process
- Entry and Exit Criteria
- Review Checklist
- Defect Log
- Prototype and Model Validation
- Acceptance Criteria and Tests

## Validation and Verification

For requirements:

- validation asks whether the team has captured the **right requirements** that satisfy real customer and business needs
- verification asks whether the requirements are **written right** with the qualities of excellent requirements

Both are required before baseline. Requirements validation should trace back to business objectives and user needs; requirements verification should check clarity, completeness, consistency, feasibility, necessity, priority, and testability.

## Review Types

Use one or more:

- informal peer review for small/low-risk artifacts
- walkthrough for shared understanding
- inspection/formal review for baseline candidates or high-risk artifacts
- role-based review to cover customer, developer, tester, architect, security, operations, data, and compliance perspectives
- checklist-based review for repeatable quality
- prototype evaluation to validate uncertain requirements
- model review for context, data, state, decision, or workflow errors

Use formal inspection for high-impact SRS, regulated work, outsourced work, safety/security-critical requirements, or baseline approval.

## Inspection Roles

| Role | Responsibility |
|---|---|
| Author | Explains artifact when needed and performs rework |
| Moderator/facilitator | Plans and runs the inspection, keeps the meeting focused on defects |
| Recorder/scribe | Captures defects, issues, and decisions accurately |
| Reader/paraphraser | Walks the team through the artifact in a disciplined way |
| Customer/product representative | Checks correctness, necessity, user value, business alignment |
| Developer/architect | Checks feasibility, allocation, constraints, design implications |
| Tester/QA | Checks verifiability, acceptance criteria, and test derivation |
| Operations/security/compliance/data reviewer | Checks production, regulatory, security, privacy, data quality, and audit needs |

Do not hold an inspection without the perspectives needed to make the artifact trustworthy.

## Inspection Process

1. Plan scope, artifacts, participants, roles, and schedule.
2. Ensure entry criteria are met.
3. Hold overview meeting if the artifact/domain is unfamiliar.
4. Reviewers prepare individually using checklists.
5. Inspection meeting identifies defects; avoid solving every problem in-session.
6. Author performs rework.
7. Moderator verifies rework or schedules re-inspection.
8. Record decision: accept, accept with rework, re-inspect, or reject.

Most value comes from disciplined preparation. Meeting time is for comparing interpretations and finding defects, not reading for the first time.

## Entry and Exit Criteria

Entry:

- artifact is complete enough for review
- IDs and version are assigned
- scope of review is clear
- glossary/data dictionary/TBD list are available
- participants received material early enough
- required roles are present

Exit:

- defects are logged and classified
- critical defects are corrected or risk-accepted
- TBDs/issues have owners and due dates
- revised version is recorded
- approval/re-inspection decision is explicit
- trace/status updates are made if the artifact is baselined

## Review Checklist

| Area | Questions |
|---|---|
| Business alignment | Does each requirement trace to a business objective, user need, rule, regulation, or justified constraint? |
| Correctness | Do source stakeholders agree the requirement represents their intent? |
| Completeness | Are flows, exceptions, states, data, interfaces, reports, and quality attributes covered? |
| Feasibility | Can the requirement be implemented within technical, cost, schedule, and environment constraints? |
| Necessity | Would removing it harm business value, compliance, user success, or product quality? |
| Priority | Is priority meaningful and agreed? |
| Ambiguity | Could reasonable readers interpret it differently? |
| Verifiability | Can test, inspection, demonstration, or analysis objectively confirm satisfaction? |
| Consistency | Does it conflict with another requirement, rule, model, or higher-level objective? |
| Modifiability | Is it uniquely labeled, atomic enough, nonredundant, and easy to change? |
| Traceability | Are backward and forward links possible and recorded where needed? |
| TBD/issues | Are incomplete items visible, owned, and time-bounded? |

## Defect Log

Use:

| Defect ID | Artifact/section | Requirement ID | Defect type | Severity | Description | Owner | Disposition | Due date |
|---|---|---|---|---|---|---|---|---|

Common defect types:

- omission
- ambiguity
- conflict
- incorrect fact/rule
- infeasible
- unverifiable
- unnecessary/gold-plated
- wrong priority
- design bias
- duplicate
- inconsistent terminology
- missing source/rationale
- missing acceptance criteria

## Prototype and Model Validation

For prototypes:

- confirm the question/risk being investigated
- choose representative users
- evaluate with realistic scenarios and data
- capture missing requirements, incorrect flows, usability issues, exceptions, and business rules
- state whether the prototype is throwaway or evolutionary
- convert validated findings into requirements or design notes

For models:

- walk through events, flows, states, decisions, and data with stakeholders
- ask what happens before/after each step
- test edge states and invalid transitions
- compare model terms to glossary/data dictionary
- trace model elements to requirements

## Acceptance Criteria and Tests

Acceptance criteria define conditions the product must satisfy to be acceptable. They may include:

- user task success under normal conditions
- handling of anticipated errors and invalid actions
- quality targets such as response time, security, availability, accessibility, or defect levels
- regulatory/certification conditions
- data/report correctness
- operational readiness

Acceptance tests and conceptual tests help validate requirements early. Cover:

- normal behavior with valid data
- alternative flows
- exception/failure scenarios
- boundary values and equivalence classes
- state-driven behavior
- event-driven behavior
- data-driven behavior
- quality attribute targets

Each committed functional requirement should map to at least one verification approach. Missing tests often reveal missing or unclear requirements.
