# Lifecycle Reference

Use this when running a full software requirements engineering process or orienting a complex request.

## Table of Contents

- Principles
- Artifact Set
- Full Process
- Phase Gate Checklist
- Tailoring Hooks
- Traceability Spine

## Principles

Requirements engineering is iterative. Expect loops among elicitation, analysis, specification, and validation until the team has enough shared understanding to commit to a baseline or iteration.

Preserve these levels and containers:

| Level/type | Meaning | Primary artifact |
|---|---|---|
| Business requirement | Why the product is needed; business value and success measures | Vision and scope |
| User requirement | User goals/tasks and desired attributes | Use case, user story, event-response table |
| Functional requirement | Software behavior under specified conditions | SRS/repository |
| Quality attribute/NFR | Measurable product property or service characteristic | SRS quality section |
| External interface requirement | User/software/hardware/communication connection | SRS/interface spec |
| Business rule | Business policy, fact, computation, inference, or decision logic | Business rules catalog |
| Constraint | Legitimate restriction on solution choices | SRS constraints |
| Data requirement | Data entity, attribute, relationship, report, retention, integrity, migration | Data model/dictionary/SRS |
| Project requirement | Work outside product behavior, such as training or deployment | Project/rollout plan |

Do not let requirements drift into design unless the design decision is an intentional constraint with rationale.

## Artifact Set

For a full lifecycle, produce or reference:

1. Vision and scope document
2. Stakeholder register and decision-rights map
3. User class catalog and product champion/product owner structure
4. Customer-development working agreement
5. Elicitation plan, interview/workshop agendas, observation plan, and notes
6. Classified raw-input log and open-issue/TBD list
7. Event-response table
8. Use case model, use case specifications, user stories, and scenarios
9. Business rules catalog
10. Analysis models: context diagram, ecosystem map, feature tree, DFD, swimlane, state-transition diagram/table, dialog map, decision table/tree, ERD/class model as needed
11. Data dictionary, data analysis notes, report/dashboard specifications
12. Quality attribute register and constraint list
13. Prototype plan, evaluation notes, and learning log
14. Prioritization model and release/iteration allocation
15. SRS or requirements repository view
16. Review/inspection plan and defect log
17. Acceptance criteria, acceptance tests, and test requirements
18. Reuse candidate list or requirement pattern notes
19. Baseline record
20. Requirement attributes/status report
21. Change request and impact-analysis report
22. Traceability matrix
23. Requirements metrics and risk register
24. Enterprise readiness register for complex production systems

## Full Process

### 1. Establish Business Requirements

Inputs: business problem/opportunity, strategic goals, sponsor goals, current process/system pain, market/customer needs, regulations, constraints.

Outputs:

- business opportunity/problem
- business objectives with target metrics
- success criteria and business value
- product vision statement
- major features
- scope of initial release and later releases
- limitations and exclusions
- business risks
- stakeholder profiles and project priorities

Gate: decision makers agree on business objectives, success metrics, and scope boundaries.

### 2. Find the Voice of the User

Inputs: stakeholder map, target users, operations context, organizational decision rights.

Outputs:

- user classes, favored user classes, and omitted-user risks
- product champions or product owner structure
- customer-development responsibilities
- decision makers for requirement conflicts and scope
- initial user personas where helpful

Gate: each important user class has a credible representative or a documented risk.

### 3. Elicit Requirements

Inputs: vision/scope, user classes, source artifacts, current systems, planned sessions.

Outputs:

- elicitation plan and agendas
- notes from interviews, workshops, focus groups, observation, questionnaires, interface/UI/document analysis
- classified raw input: BR, UR, FR, NFR, IR, BRULE, CON, DATA, project requirement, assumption, dependency, TBD
- event-response table
- open issues and follow-up actions

Gate: major sources have been inspected and diminishing returns are visible; assumptions and implied requirements are exposed.

### 4. Analyze and Model

Inputs: raw findings and source artifacts.

Outputs:

- use cases, user stories, scenarios, normal/alternative/exception flows
- business rules catalog
- data model, data dictionary, report/dashboard requirements
- analysis models selected for the problem
- prototype plan/results for uncertain or risky areas
- priority values based on value, cost, risk, and stakeholder agreement
- refined requirement candidates

Gate: conflicts, missing requirements, edge cases, data gaps, state gaps, interface issues, and feasibility questions have owners.

### 5. Specify Requirements

Inputs: approved analysis outputs and scope.

Outputs:

- SRS or equivalent repository organized by feature, use case, process, user class, stimulus-response, or another understandable structure
- functional requirements
- data requirements
- external interface requirements
- quality attributes and constraints
- localization, compliance, operational, and other requirements
- glossary and analysis-model references
- requirement attributes and TBD list

Gate: requirements are complete, correct, feasible, necessary, prioritized, unambiguous, verifiable, consistent, modifiable, and traceable enough for the commitment being made.

### 6. Validate Requirements

Inputs: SRS/repository, models, prototypes, acceptance criteria.

Outputs:

- inspection/review plan
- defect log and rework decisions
- validated use cases/user stories/models
- acceptance criteria and conceptual tests
- approval or re-inspection decision

Gate: critical defects and blocking TBDs are resolved or explicitly accepted with risk.

### 7. Baseline and Manage

Inputs: validated requirements set.

Outputs:

- baseline record and version scheme
- requirement attributes and status workflow
- change-control policy/process
- CCB or product decision authority
- impact-analysis procedure
- traceability matrix
- requirements metrics and status report

Gate: post-baseline changes cannot bypass evaluation, decision, communication, implementation, verification, and trace updates.

### 8. Connect to Downstream Work

Inputs: baselined requirements, architecture/design/test plans, project plan.

Outputs:

- requirement-based estimates and release plan
- architecture/allocation notes for systems with multiple components
- design constraints and derived requirements
- acceptance tests and system tests linked to requirements
- user documentation/training requirements when product behavior depends on them

Gate: downstream work traces to requirements, and requirements can be tested at the appropriate level.

## Phase Gate Checklist

Before advancing, ask:

- Are the business objectives measurable and agreed?
- Are scope-in, scope-out, limitations, and release allocation explicit?
- Are all important user classes represented by suitable product champions or product owner inputs?
- Are business, user, functional, quality, interface, data, rule, constraint, and project items separated?
- Are normal, alternative, and exception flows represented?
- Are states, events, reports, and data definitions clear?
- Are quality attributes measurable and prioritized?
- Are requirement IDs, sources, rationale, priorities, owners, statuses, releases, and verification methods present?
- Are TBDs owned and time-bounded?
- Are reviews complete and defects dispositioned?
- Is there traceability from business objective to user requirement/use case to functional/NFR/interface/data requirement to test?
- Are change control and impact analysis active after baseline?

## Tailoring Hooks

Load `project-classes.md` when the project is agile, enhancement/replacement, packaged solution, outsourced, business process automation, analytics, or embedded/real-time.

Load `enterprise-governance.md` when the work spans multiple departments, external systems, data migration, privacy/security, audit, operational SLAs, high availability, high concurrency, or production support.

Load `process-risk.md` when the user asks to improve the requirements process, diagnose problems, or identify risks.

## Traceability Spine

Use this chain:

`Business objective -> business requirement -> user class/persona -> user requirement/use case/user story/event -> functional requirement/NFR/interface/data requirement/business rule/constraint -> design/allocation -> code/configuration -> test/acceptance criterion -> user documentation/support`

If a downstream item cannot trace backward, it is either scope creep or a missing requirement. If a high-level need does not trace forward, the solution is incomplete.
