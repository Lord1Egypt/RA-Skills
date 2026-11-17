---
name: system-architecture-builder
description: Build repeatable system architectures, operating systems, target architectures, control layers, agent runtimes, and governance models using the user's OS-style architecture pattern. Use when the user asks to design, structure, extend, audit, or standardize an architecture rather than make a small isolated implementation change.
---

# System Architecture Builder

Use this skill to turn an idea, business function, workflow, platform, or organization into a reusable operating architecture. Treat this as Brasco's default OS architecture standard: not a loose document, but a layered system that can be operated, measured, governed, improved, and eventually delegated to agents.

Apply this standard by default for new OS architectures, target architectures, operating models, autonomous systems, agent systems, client delivery systems, data quality systems, growth systems, or business-function systems. Scale the output to the size of the request instead of forcing the full enterprise structure every time.

## Core Architecture Rule

Every architecture should answer:

- What is the system for?
- What inputs does it consume?
- What decisions does it make or support?
- What work does it execute?
- What outputs does it produce?
- What feedback loops improve it?
- What must humans approve?
- What can agents or automations do safely?
- What evidence proves the system is working?

Do not stop at a conceptual map. Produce enough structure that a competent person or agent can rebuild, operate, audit, and improve the system.

## Architecture Depth

Choose the smallest depth that still makes the system operational:

- Micro OS: use for a narrow workflow, playbook, or single function. Deliver an overview, workflow, templates, gates, metrics, and next actions.
- Standard OS: use for a reusable business system. Deliver layers, knowledge, decisions, workflows, agents or roles, integrations, governance, observability, templates, and roadmap.
- Enterprise OS: use for systems with clients, money movement, data quality risk, external platforms, multiple agents, or automation. Deliver the full control plane: decision OS, knowledge OS, integration OS, action layer, permission model, audit trail, rollback, runtime observability, control tower, and governance.

When uncertain, start with Standard OS and explicitly note which Enterprise OS modules can be added later.

## Default Shape

When building a new architecture, use this layer model unless the user gives a stronger domain-specific structure:

```text
Strategy Layer -> Knowledge Layer -> Decision Layer -> Agent Layer ->
Execution Layer -> Integration Layer -> Event / Feedback Layer ->
Governance Layer -> Observability / Control Tower
```

Adapt the names to the domain, but preserve the responsibilities:

- Strategy Layer: market, purpose, audience, positioning, goals, constraints.
- Knowledge Layer: durable repositories, evidence, assumptions, lessons, source of truth.
- Decision Layer: decision types, tradeoffs, approval rules, risk classes, backlog.
- Agent Layer: roles, responsibilities, triggers, handoffs, reviewer agents.
- Execution Layer: workflows, SOPs, templates, campaigns, actions, deliverables.
- Integration Layer: tools, connectors, APIs, permissions, data contracts.
- Event / Feedback Layer: events, metrics, incidents, learning loops, state changes.
- Governance Layer: human approval, audit trail, versioning, rollback, compliance.
- Observability / Control Tower: dashboards, trust state, alerts, operating rhythm.

## Required Outputs

For a substantial architecture request, create or propose these artifacts:

- `README.md` or overview: purpose, mission, operating principles, folder map, quick start.
- `target-architecture.md`: final layer map, system map, runtime map, integration map.
- `workflow/`: core operating workflow from intake to output.
- `templates/`: reusable briefs, decision records, scorecards, blueprints, reports.
- `gates/`: quality gates and approval gates.
- `agents/` or `agent-operating-layer/`: agent roles, permissions, handoff rules.
- `decision-os/`: decision taxonomy, approval matrix, risk register, tradeoff model.
- `knowledge-os/`: repositories, evidence standard, knowledge maintenance loop.
- `integration-os/`: connectors, authentication, read/write access, sync engine.
- `action-layer/`: action registry, action limits, action policies, rollback.
- `runtime-observability/` or `control-tower/`: KPIs, health checks, alerts.
- `roadmap/`: implementation phases and next highest leverage actions.

For smaller requests, return the smallest useful subset instead of forcing every file.

## Brasco OS Standard

For this user, default to this architecture stance:

- Build systems as reusable operating systems, not one-off strategy documents.
- Make every OS agent-ready: define roles, triggers, permissions, handoffs, review points, and escalation paths.
- Make every OS evidence-aware: distinguish known facts, assumptions, confidence, missing data, and verification paths.
- Make every OS commercially useful: connect architecture to leverage, throughput, risk reduction, decision speed, or client value.
- Make every OS productizable where reasonable: define what could become a service package, control tower, audit, managed service, or platform feature.
- Prefer a read-only or diagnostic runtime first when the system touches external tools, client accounts, analytics, CRM, ads, revenue, or publishing.
- Separate the architecture from its current implementation state: describe target state, current state, gaps, and migration path.
- Preserve a clear human authority layer for strategy, budget, trust, irreversible action, and high-risk external writes.

## Operating Standards

- Make the architecture operational, not decorative.
- Separate strategy, knowledge, decisions, execution, integration, and governance.
- Define explicit human approval boundaries before high-risk or irreversible action.
- Prefer read-only and audited runtime stages before write automation.
- Include evidence standards and confidence levels where decisions depend on external facts.
- Make feedback loops concrete: events should update knowledge, metrics, decisions, and next actions.
- Include data quality and source-of-truth rules whenever metrics, attribution, leads, revenue, or reporting are involved.
- Include permission classes for tools and agents: read, draft, annotate, bounded write, high-risk write, human-only.
- Design for progressive autonomy: manual -> assisted -> read-only runtime -> bounded automation -> governed autonomy.
- End with the next highest leverage action, not just a static blueprint.

## Review Checklist

Before finalizing, check that the architecture has:

- A clear mission and scope boundary.
- Named layers with responsibilities.
- Inputs, outputs, owners, and handoffs.
- Data, event, and feedback flows.
- Governance, approvals, and rollback logic.
- Templates or artifacts that make the system repeatable.
- Observability and success metrics.
- Known risks, assumptions, and open decisions.
- A practical implementation roadmap.

## File And Naming Conventions

When creating files in a repo, follow the local structure first. If no structure exists, use lowercase folder names and hyphenated Markdown filenames, for example:

```text
system-name/
  README.md
  architecture/target-architecture.md
  workflow/core-workflow.md
  templates/
  gates/
  agents/
  decision-os/
  knowledge-os/
  integration-os/
  action-layer/
  control-tower/
  roadmap/implementation-roadmap.md
```
