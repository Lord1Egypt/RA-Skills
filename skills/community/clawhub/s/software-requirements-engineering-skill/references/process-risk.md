# Process Improvement and Requirements Risk Reference

Use this when diagnosing requirements problems, improving requirements practices, building process assets, or identifying requirements-related risks.

## Table of Contents

- Process Improvement Cycle
- Requirements Process Assets
- Stakeholder Commitment
- Requirements Risk Management
- Risk Catalog
- Troubleshooting Signals
- Improvement Output

## Process Improvement Cycle

Use an incremental improvement cycle:

1. Assess current requirements practices.
2. Identify root causes of recurring problems.
3. Plan improvement actions.
4. Create or update process assets.
5. Pilot the new practice on a suitable project.
6. Roll out with training and support.
7. Evaluate results using metrics and retrospectives.
8. Adjust and repeat.

Avoid imposing a heavyweight process all at once. Scale practices to project risk, size, distribution, regulation, novelty, and stakeholder maturity.

## Requirements Process Assets

Useful development assets:

- requirements development process description
- role descriptions for BA, product champion, reviewer, product owner, CCB
- elicitation technique guidance and agendas
- stakeholder/user-class catalog template
- vision and scope template
- use case/user story templates
- SRS template
- analysis modeling examples
- business rules catalog template
- data dictionary/report specification templates
- quality attribute question sets and patterns
- review checklists and defect taxonomy

Useful management assets:

- requirements management plan/process
- version-control conventions
- baseline approval process
- change-control process
- impact-analysis checklist/template
- status model and transition rules
- traceability procedure
- metrics definitions
- tool usage conventions
- reuse library and requirement patterns

## Stakeholder Commitment

Requirements process improvement affects customers, developers, testers, managers, operations, and support. Gain commitment by showing how better requirements reduce rework, unmanaged change, expectation gaps, and late defects.

When people resist:

- identify what they fear losing: speed, authority, flexibility, autonomy, or time
- show lightweight versions of the practice
- explain the value of each artifact
- pilot on a real pain point
- keep feedback loops short
- avoid process for its own sake

## Requirements Risk Management

Risk management means addressing concerns before they become crises.

Risk register:

| ID | Risk | Category | Probability | Impact | Trigger | Mitigation | Contingency | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|

Manage risks by:

- identifying risk factors early
- estimating probability and impact
- prioritizing exposure
- choosing avoidance, mitigation, transfer, or acceptance
- tracking mitigation actions
- reassessing periodically

## Risk Catalog

| Category | Risk | Mitigation |
|---|---|---|
| Elicitation | Important user classes are omitted | Create user class catalog; appoint product champions; review stakeholder coverage |
| Elicitation | Customer input is vague or solution-biased | Ask why, classify input, use models/prototypes, record TBDs |
| Elicitation | Assumed/implied requirements remain hidden | Use observation, document analysis, interface analysis, checklists, exception questions |
| Analysis | Conflicting requirements are not resolved | Define decision authority; use workshops, prioritization, business objectives |
| Analysis | Data, states, reports, or interfaces are missing | Use data dictionary, ERD, state tables, report specs, context/interface models |
| Analysis | Quality attributes are discovered too late | Elicit and prioritize NFRs early; involve architects, testers, operations, security |
| Analysis | Requirements are infeasible or too costly | Involve developers/architects; use proofs of concept; analyze value-cost-risk |
| Specification | Requirements are ambiguous or incomplete | Use writing rules, examples, fit criteria, peer review, owned TBDs |
| Specification | SRS mixes requirements, design, and project tasks | Classify items; move project tasks to project plan; record only true constraints |
| Validation | Stakeholders skip reviews | Review in small chunks; assign roles; use checklists; set baseline gate |
| Validation | Requirements are not testable | Include testers; derive acceptance criteria and conceptual tests early |
| Management | No baseline exists | Define approval point and versioning; identify committed release scope |
| Management | Scope creep bypasses change control | Use CR process, fast path, impact analysis, decision authority |
| Management | Traceability is added too late | Populate trace links incrementally; use tools for scale |
| Management | Requirement status is vague | Use explicit statuses and transition conditions |
| Project class | Outsourced supplier relies on implied needs | Write detailed requirements, glossary, acceptance criteria, and change process |
| Project class | Packaged solution overcustomization grows | Use fit-gap, must-have criteria, lifecycle cost analysis |
| Project class | Agile backlog misses cross-cutting NFRs | Track NFRs with stories, acceptance tests, and architecture decisions |

## Troubleshooting Signals

Watch for:

- users reject delivered functionality
- developers repeatedly ask "what does this mean?"
- testers cannot derive objective tests
- many defects are caused by missing or misunderstood requirements
- every requirement is high priority
- requirements exist without rationale or source
- changes arrive through private conversations
- SRS/backlog and implemented behavior diverge
- old requirements resurface because rejection rationale was not recorded
- reports, data fields, or interfaces are discovered late
- quality attributes are stated only as adjectives
- no one can say which requirements are in the current baseline

## Improvement Output

When asked to improve a requirements process, produce:

- current-state diagnosis
- root causes
- target practices
- lightweight pilot plan
- updated process assets/templates/checklists
- roles and decision rights
- training/adoption plan
- metrics to evaluate improvement
- risk register and mitigation actions
