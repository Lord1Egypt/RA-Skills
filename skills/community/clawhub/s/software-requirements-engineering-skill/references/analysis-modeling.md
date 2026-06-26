# Requirements Analysis and Modeling Reference

Use this for use cases, user stories, scenarios, business rules, analysis models, data requirements, prototypes, prioritization, and reuse.

## Table of Contents

- Analysis Goals
- User Requirements
- Use Cases
- User Stories
- Business Rules
- Models and When to Use Them
- Data and Reports
- Prototyping
- Prioritization
- Requirements Reuse
- Analysis Quality Gate

## Analysis Goals

Analysis transforms raw elicitation findings into structured, consistent, feasible, prioritized, and testable requirement knowledge. It exposes:

- ambiguity and multiple interpretations
- omitted user classes, tasks, exceptions, data, reports, states, interfaces, rules, and quality attributes
- conflicts among stakeholders or quality attributes
- infeasible or expensive requirements
- redundant or gold-plated functionality
- solution ideas that hide real needs
- requirements that do not support business objectives

Use text plus models. No single representation is sufficient.

## User Requirements

Represent user requirements with use cases, user stories, event-response tables, and scenarios. User requirements describe what users need to accomplish, not the detailed software implementation.

Keep traceability:

`BR -> user class -> UC/US/event/scenario -> FR/NFR/IR/DATA/BRULE/CON -> tests`

## Use Cases

Use cases express user goals and interactions. They are especially useful when the system supports workflows with alternatives and exceptions.

Use case fields:

| Field | Purpose |
|---|---|
| ID/name | Stable reference and goal phrase |
| Primary actor | User or external system initiating the goal |
| Supporting actors/systems | Other participants |
| Stakeholders/interests | Who cares about the result |
| Preconditions | What must be true before start |
| Trigger | Event that starts the use case |
| Minimal guarantee | What remains true after failure |
| Success guarantee/postconditions | What is true after success |
| Main success scenario | Normal flow |
| Alternative flows | Valid variations |
| Exceptions | Error/abnormal paths |
| Business rules | Rules affecting behavior |
| Special requirements | Quality/interface/data constraints |
| Frequency/volume | Usage profile |
| Priority | Release planning |
| Open issues | TBDs |

Do not confuse use cases with screens. A use case can involve multiple screens, and a screen can support parts of multiple use cases.

Derive functional requirements from use case flows:

- each user action that requires system response implies system behavior
- each alternative/exception path implies requirements for conditions, validations, messages, recovery, or logging
- each business rule implies functional enforcement or validation
- each special requirement may become a quality, interface, or constraint requirement

Validate use cases with product champions, testers, developers, and UX/design participants.

## User Stories

Use user stories when an agile or backlog-centered approach is appropriate:

`As a <user class>, I want <goal/capability> so that <business/user value>.`

For each story include:

- acceptance criteria
- business rule references
- quality expectations
- dependencies
- priority
- estimate/risk
- split notes for large stories

Stories are placeholders for conversation and confirmation. Do not let them remain too vague for implementation or testing.

## Business Rules

Business rules are not themselves software requirements, but they often originate or constrain software requirements.

Taxonomy:

| Rule type | Meaning |
|---|---|
| Fact | Term, relationship, or truth about the business domain |
| Constraint | Restriction on business actions or data |
| Action enabler | Condition that permits or triggers an action |
| Inference | Conclusion derived from facts/rules |
| Computation | Formula or algorithm |
| Atomic rule | Rule small enough to be managed and traced independently |

Business rules catalog:

| ID | Rule statement | Type | Source | Rationale | Enforcement point | Related requirements |
|---|---|---|---|---|---|---|

If a rule changes independently of the software, keep it in a business rules catalog and trace requirements to it.

## Models and When to Use Them

| Model | Use when | Reveals |
|---|---|---|
| Context diagram | Need system boundary and external entities | Scope, interfaces, external actors |
| Ecosystem map | Need wider business/system environment | Neighbor systems, organizations, upstream/downstream dependencies |
| Feature tree | Need hierarchy of related capabilities | Scope chunks, release planning, feature decomposition |
| Event list/event-response table | System reacts to external events | Missing triggers, responses, related use cases |
| Data flow diagram | Need transformations, data stores, and flows | Missing processes, stores, external flows |
| Swimlane diagram | Need process roles and handoffs | Role responsibility, bottlenecks, current/future process |
| State-transition diagram/table | Object/system has lifecycle states | Missing states, invalid transitions, event handling |
| Dialog map | Need navigation or UI flow structure | Missing screens, navigation loops, workflow gaps |
| Decision table/tree | Logic has complex condition combinations | Missing rule combinations and conflicts |
| ERD/logical data model | Need data entities and relationships | Cardinality, ownership, missing entities |
| UML class/activity models | Object relationships or activity flow matter | Domain concepts, responsibilities, concurrency |

Model only what helps answer requirement questions. Keep models aligned with textual requirements and trace IDs.

## Event-Response Table

Use this when triggers matter:

| Event ID | Event/trigger | Source | Condition/state | System response | Related UC/FR | Priority |
|---|---|---|---|---|---|---|

Include external events, temporal events, error events, business events, and data/interface events.

## Data and Reports

Analyze data because functions manipulate data.

Data model/dictionary fields:

| Item | Meaning |
|---|---|
| Entity/data structure | Business object or collection |
| Attribute | Data element |
| Definition | Business meaning |
| Type/format/length | Valid representation |
| Allowed values/range | Validation basis |
| Source of truth | Origin/owner |
| Create/read/update/delete users | Access and workflow |
| Retention/disposal | Lifecycle obligation |
| Quality rules | Accuracy, completeness, timeliness, reconciliation |

For reports and dashboards capture:

- report/dashboard purpose and decision supported
- audience and frequency
- data sources and filters
- calculations and business rules
- grouping, sorting, totals, drilldown
- freshness/latency
- export, access, audit, retention
- acceptance examples

## Prototyping

Use prototypes to reduce uncertainty, not to skip requirements.

Classify each prototype:

| Dimension | Options | Guidance |
|---|---|---|
| Scope | Mock-up/horizontal or proof-of-concept/vertical | Mock-ups explore user experience; proof-of-concept explores technical feasibility |
| Future use | Throwaway or evolutionary | Throwaway code must not become production code; evolutionary prototypes must be production-quality from the start |
| Form | Paper/low-fidelity or electronic/high-fidelity | Use low fidelity for early flow/functionality; high fidelity for refined interaction |

For every prototype record:

- question/risk being investigated
- fidelity and boundaries
- evaluator user classes
- scenarios tested
- findings
- requirement changes
- discard/evolve decision

## Prioritization

Prioritize because not everything fits in the project box.

Use simple methods for small projects and structured methods for large or contentious projects:

| Method | Use when |
|---|---|
| In/out | Need first scoping cut |
| Pairwise comparison/rank ordering | Need relative ranking of a small set |
| Three-level scale | Need simple high/medium/low priority with clear definitions |
| MoSCoW | Need must/should/could/won't release planning |
| $100 allocation | Need stakeholder value trade-off signals |
| Value-cost-risk | Need economic and delivery-risk balance |

Priority definition should consider value, cost, technical risk, business risk, dependencies, deadlines, compliance, and user-class importance. "Everything is high priority" is not a priority scheme.

## Requirements Reuse

Look for reuse when requirements recur across products, releases, domains, regulatory contexts, interfaces, reports, quality attributes, or product lines.

Reusable items:

- requirement patterns
- business rules
- glossary/data definitions
- quality attribute templates
- interface requirements
- use case fragments
- compliance requirements
- acceptance criteria

Make requirements reusable by writing them clearly, separating context-specific values, storing rationale/source, and avoiding unnecessary implementation detail.

## Analysis Quality Gate

Before specification, verify:

- every user requirement traces to business value
- every functional requirement candidate traces to a user requirement, rule, regulation, or justified constraint
- all use cases include normal, alternative, and exception flows
- analysis models are consistent with each other
- data definitions and reports are sufficient for implementation/test planning
- quality attributes and constraints are explicit
- priority method and decision authority are clear
- infeasible or high-risk items have prototype, analysis, or decision actions
- open issues and assumptions have owners and dates
