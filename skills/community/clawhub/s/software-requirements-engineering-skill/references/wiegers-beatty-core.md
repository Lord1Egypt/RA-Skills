# Wiegers & Beatty Core Method Reference

Use this when a task needs the underlying method, role model, or terminology before entering a specific phase.

## Table of Contents

- Requirements Engineering Structure
- Requirements Information Taxonomy
- Customer-Development Partnership
- Roles and Responsibilities
- Business Analyst Competencies
- Good Practice Map
- Quality Gates

## Requirements Engineering Structure

Use two major subdisciplines:

| Discipline | Purpose | Core activities |
|---|---|---|
| Requirements development | Discover and express the right requirements | Elicitation, analysis, specification, validation |
| Requirements management | Maintain agreed requirements over time | Baseline, version control, status tracking, change control, impact analysis, traceability, tool/process support |

Development is not a one-pass waterfall. Treat it as iterative progressive refinement: elicit information, analyze/classify/model it, specify it in a usable form, validate it, then loop when review exposes omissions, conflicts, or ambiguity.

## Requirements Information Taxonomy

Keep these categories distinct:

| Type | Meaning | Typical container |
|---|---|---|
| Business requirement | Business objective, benefit, or outcome that justifies the product | Vision and scope, business case |
| User requirement | User goal/task or desired product attribute for a user class | Use case, user story, event-response table |
| Functional requirement | System behavior under specified conditions | SRS or requirements repository |
| System requirement | Top-level requirement for a product containing software, hardware, human, or process components | SyRS/system spec |
| Nonfunctional requirement | Product property, constraint, external interface, or operating/environment need | SRS/supplement |
| Quality attribute | Measurable service/performance characteristic such as usability, security, reliability, performance | SRS quality section |
| External interface requirement | User/software/hardware/communication connection requirement | Interface section/spec |
| Constraint | Restriction on design or implementation choices | SRS constraint section |
| Business rule | Policy, regulation, guideline, fact, computation, inference, or decision rule independent of a single software solution | Business rules catalog |
| Feature | Related capabilities that deliver user value and are implemented by one or more functional requirements | Feature tree/backlog |
| Data requirement | Data entity, attribute, relationship, dictionary entry, report, acquisition, retention, integrity, or disposal need | Data model/dictionary/SRS |
| Project requirement | Requirement about project work, training, deployment, schedule, budget, documentation, or transition | Project plan, rollout plan |

Do not let solution ideas masquerade as requirements. Ask why a proposed solution is needed, preserve the real need, and record legitimate restrictions as constraints.

## Customer-Development Partnership

Set expectations early. Customers and user representatives have rights to business-language communication, requirements practices explained in usable terms, respectful collaboration, change handling, quality expectation elicitation, reuse options, and a product that satisfies agreed needs.

They also have responsibilities:

- educate the team about the business and terminology
- dedicate time for elicitation and clarification
- provide specific, precise input
- make timely decisions
- respect feasibility and cost assessments
- set realistic priorities with developers
- review requirements and evaluate prototypes
- establish acceptance criteria
- communicate changes promptly
- respect the requirements process

Use this partnership as a working agreement when stakeholders resist requirements activities.

## Roles and Responsibilities

| Role | Requirements responsibility |
|---|---|
| Sponsor/funding customer | Owns business objectives, scope authority, funding, success metrics |
| Business analyst/requirements analyst | Leads elicitation, analysis, modeling, specification, validation, and management setup |
| Product champion | Represents one user class; gathers input, resolves within-class conflicts, reviews, prioritizes, evaluates prototypes, supports acceptance |
| Product owner | Owns product vision/backlog and priority decisions; may coordinate several product champions |
| User class representative | Supplies user goals, workflow details, exceptions, quality expectations, acceptance criteria |
| Domain expert/SME | Explains specialized rules, policies, terminology, algorithms, constraints |
| Project manager | Aligns scope, schedule, resources, commitments, risks, and change decisions |
| Architect/developer | Checks feasibility, cost, allocation, constraints, design implications, reuse opportunities |
| Tester/QA | Checks verifiability, derives test requirements and acceptance tests, participates in reviews |
| UX/UI designer | Helps explore interaction requirements, dialog maps, prototypes, accessibility/usability needs |
| Data analyst/data steward | Owns data definitions, data quality, reporting/analytics, retention, lineage |
| Operations/security/compliance | Owns availability, monitoring, recovery, access control, privacy, legal/regulatory obligations |
| Change control board/decision authority | Evaluates, approves, rejects, or defers post-baseline changes |

One person may hold multiple roles, but do not omit the perspective. When a role is missing, record the risk.

## Business Analyst Competencies

A capable BA needs:

- active listening, interviewing, facilitation, conflict handling, negotiation
- ability to write clearly and structure information
- ability to model workflows, states, data, interfaces, decisions, and events
- domain learning ability and business curiosity
- enough technical awareness to discuss feasibility and constraints
- enough testing awareness to make requirements verifiable
- organizational awareness for decision rights and politics

If the BA role is distributed across product owner, tester, developer, or SME, explicitly assign the work products and decision authority.

## Good Practice Map

| Area | Practices to apply |
|---|---|
| Elicitation | Identify user classes; appoint product champions; combine interviews, workshops, focus groups, observation, questionnaires, interface/UI/document analysis; classify customer input; follow up on open issues |
| Analysis | Model context, features, process/data flows, states, dialogs, decisions, data, reports, interfaces; derive functional requirements from user requirements; detect conflicts and missing requirements |
| Specification | Use an SRS or repository; label requirements; handle incompleteness with owned TBDs; organize by feature/use case/process; write excellent requirements and store attributes |
| Validation | Use peer review/inspection, checklists, model review, prototype evaluation, acceptance criteria, and early test thinking |
| Management | Baseline agreed requirements; version artifacts and individual requirements; track status; manage changes; run impact analysis; maintain trace links; use tools when scale justifies |
| Knowledge | Maintain glossary, domain notes, reusable requirement patterns, lessons learned, and process assets |
| Project management | Estimate requirements effort, plan by priority, track requirement status, monitor requirements risks and change activity |

## Quality Gates

Single requirement statement quality:

- complete
- correct
- feasible
- necessary
- prioritized
- unambiguous
- verifiable

Requirement collection quality:

- complete enough for the work being committed
- consistent
- modifiable
- traceable

Gate questions:

- Does every requirement trace to a business objective, user need, rule, regulation, or justified constraint?
- Does every business objective have user and functional support?
- Are all key user classes represented by suitable people?
- Are vague quality expectations measurable?
- Are priority, source, rationale, owner, status, release, and verification method recorded?
- Can testers derive objective tests or acceptance checks?
- Are unresolved items explicitly marked as TBD/issues with owner and due date?
