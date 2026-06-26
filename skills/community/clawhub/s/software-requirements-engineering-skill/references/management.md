# Requirements Management Reference

Use this for baselines, version control, requirement attributes/status, change control, CCB/product decision authority, impact analysis, traceability, metrics, and tools.

## Table of Contents

- Purpose
- Baseline and Version Control
- Requirement Attributes
- Requirement Status
- Change Control Policy
- Change Request
- Impact Analysis
- CCB or Decision Authority
- Traceability
- Metrics
- Tools

## Purpose

Requirements management maintains the integrity, accuracy, and currency of agreed requirements throughout development and maintenance. It does not block change; it makes change visible, evaluated, approved or rejected, communicated, implemented, verified, and traceable.

Core activities:

- version control
- change control
- status tracking
- traceability

## Baseline and Version Control

A requirements baseline is an approved set of requirements committed for a release, iteration, increment, contract, or decision point.

Baseline record:

| Baseline ID | Artifact/repository view | Version | Included releases/iterations | Approval date | Approvers | Notes |
|---|---|---|---|---|---|---|

Rules:

- distinguish drafts from approved/baselined versions
- identify requirements proposed but not accepted
- identify requirements deferred to a later release
- update the baseline when scope changes are approved
- do not let direct code/backlog changes bypass requirements records

Version scheme example:

- `Version 1.0 draft 1`, `Version 1.0 draft 2`
- `Version 1.0 approved`
- `Version 1.1 draft 1` for minor revision
- `Version 2.0 draft 1` for major revision

## Requirement Attributes

Track enough attributes to manage the work, but do not overwhelm the team.

Recommended attributes:

| Attribute | Purpose |
|---|---|
| Created date | Aging and history |
| Current version | Change tracking |
| Author | Origin of wording |
| Source/origin | Stakeholder, rule, regulation, document, system |
| Rationale | Why the requirement exists |
| Priority | Trade-off and release planning |
| Status | Progress and decision visibility |
| Release/iteration | Baseline allocation |
| Owner/contact | Questions and change decisions |
| Validation method/acceptance criteria | Objective verification |
| Risk/stability | Management attention |
| Trace links | Impact analysis |

Start with a small useful set, then add attributes only when they will be populated and used.

## Requirement Status

Use explicit statuses instead of vague percent-complete claims.

Suggested statuses:

| Status | Meaning |
|---|---|
| Proposed | Requested by an authorized source |
| In Progress | BA/analyst is actively crafting or analyzing it |
| Drafted | Initial version is written |
| Approved | Analyzed, impact estimated, allocated to a baseline, and agreed by key stakeholders |
| Implemented | Designed, coded/configured, unit tested, and traced to design/code elements |
| Verified | Acceptance criteria satisfied and traced to tests/verification evidence |
| Deferred | Approved but moved to a later release/iteration |
| Deleted | Removed from an approved baseline with decision rationale |
| Rejected | Proposed but not approved and not planned |

Update status only when transition conditions are satisfied. Record who changed status and why for deleted/rejected items.

## Change Control Policy

After baseline, route all requirement changes through a defined process, scaled to project risk. Include a fast path for low-risk, low-investment changes, but no change affecting more than one person's work should bypass visibility.

Change process:

1. Submit change request.
2. Register and classify.
3. Screen for completeness and duplicate requests.
4. Analyze value, feasibility, cost, risk, schedule, quality, and contractual impact.
5. Perform trace-based impact analysis.
6. Decide: approve, reject, defer, request more information, or combine with another change.
7. If approved, update baseline, requirements, models, tests, plans, docs, backlog, and commitments.
8. Implement and verify.
9. Close and report status.

## Change Request

Use:

| Field | Description |
|---|---|
| CR ID/title | Stable reference |
| Submitter/date | Who and when |
| Description | Requested change |
| Reason/business value | Why it is needed |
| Affected requirement IDs | Known scope |
| Desired release/urgency | Timing pressure |
| Priority | Business priority |
| Impact summary | Cost/schedule/risk/quality |
| Decision | Approved/rejected/deferred/more info |
| Decision authority/date | Who decided |
| Implementation owner | Who makes changes |
| Verification evidence | How completion is confirmed |

## Impact Analysis

Impact analysis prevents "small" changes from creating hidden rework.

Procedure:

1. Understand the implications of making the change.
2. Identify every artifact, requirement, design component, code/configuration element, interface, test, document, process, and stakeholder that might be affected.
3. Estimate effort, schedule, cost, risk, quality impact, and priority relative to other pending work.
4. Identify task sequence and dependencies.
5. Report results to the decision authority.

Impact checklist:

- affected business objectives and scope
- affected user classes and product champions
- affected use cases/stories/flows
- affected functional, quality, interface, data, rule, and constraint requirements
- affected prototypes/models/glossary/data dictionary
- affected architecture, configuration, APIs, reports, migrations
- affected test cases, acceptance criteria, automation, test data
- affected user documentation, training, support, operations
- regulatory, contract, security, privacy, and audit effects
- release, budget, staffing, and quality trade-offs

## CCB or Decision Authority

For traditional or high-governance work, use a change control board. For agile work, use product owner/backlog governance, but still keep impact visible.

CCB charter should state:

- scope of authority
- members and perspectives
- meeting cadence or asynchronous decision path
- voting/decision rules
- fast-path criteria
- escalation path
- communication rules
- commitment renegotiation process

Typical members: sponsor/product owner, BA, project manager, architect/developer lead, tester/QA, operations/security/compliance/data representatives where relevant.

## Traceability

Traceability records dependencies and logical links among requirements and other system elements.

Trace both directions:

- forward from customer/business need to requirements, design, code/configuration, tests, and docs
- backward from requirement to origin and rationale

Common link types:

- derives from / derived by
- specifies / specified by
- depends on
- parent of / child of
- constrains / constrained by
- verifies / verified by
- implements / implemented by

Traceability matrix:

| Business objective | User req/UC/US | FR/NFR/IR/DATA/BRULE/CON | Design/config | Code/module | Test/acceptance | Docs/support |
|---|---|---|---|---|---|---|

Populate trace links during development, not at the end. Retroactive tracing is expensive and error-prone.

Use tracing when:

- assessing change impact
- confirming coverage
- finding orphan requirements
- ensuring every requirement has tests
- planning release scope
- supporting audits or regulated work

## Metrics

Useful measures:

- requirements count by type/status/priority/release
- open TBDs/issues by age and owner
- review defects by type/severity/artifact
- volatility: additions, changes, deletions per period
- change request cycle time and approval rate
- percentage of requirements traced to tests
- percentage verified
- effort spent on elicitation, analysis, specification, validation, management
- escaped requirement defects discovered after baseline or release

Use metrics to manage, not to punish. Interpret trends with project context.

## Tools

Requirements development tools help with elicitation, prototyping, modeling, collaboration, and quality checks.

Requirements management tools help with:

- storing requirements and attributes
- versioning
- filtering and reports
- status tracking
- baseline management
- change workflow
- trace links
- import/export
- integration with design, test, issue, and documentation tools

Introduce tools with process and training. A tool cannot compensate for unclear roles or poor requirements discipline.
