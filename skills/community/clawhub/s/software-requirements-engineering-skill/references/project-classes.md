# Project Classes Reference

Use this when tailoring requirements engineering for agile, enhancement/replacement, packaged solution, outsourced, business process automation, business analytics, or embedded/real-time projects.

## Table of Contents

- Agile Projects
- Enhancement and Replacement Projects
- Packaged Solution Projects
- Outsourced Projects
- Business Process Automation Projects
- Business Analytics Projects
- Embedded and Real-Time Systems
- Tailoring Checklist

## Agile Projects

Agile does not remove requirements engineering; it changes timing, detail, and containers.

Emphasize:

- continuous customer/product owner involvement
- product/release backlog as a dynamic requirements container
- epics, features, user stories, acceptance criteria, and tests
- prioritization every iteration
- enough documentation for shared understanding, future maintenance, compliance, and distributed work
- early attention to architecture-driving quality attributes and constraints
- change expected, but not unmanaged

Outputs:

- product vision and business objectives
- user class/product champion coverage
- product backlog with source, priority, acceptance criteria, and NFR links
- release/iteration allocation
- definition of ready/done tied to requirement quality
- traceability lightweight enough to support impact analysis

Cautions:

- a single product owner may not represent all user classes
- user stories without acceptance criteria are too weak for implementation
- cross-cutting NFRs cannot wait until "later"
- backlog churn still needs visible decision-making

## Enhancement and Replacement Projects

Expected challenges:

- little or obsolete documentation for the current system
- users resist changes to familiar workflows
- new changes can degrade current performance or usability
- vital hidden functionality can be omitted
- stakeholders may request opportunistic features unrelated to business objectives

Techniques:

- create a feature tree showing retained, added, changed, and removed features
- identify affected user classes and adoption risks
- model as-is and to-be business processes
- mine business rules embedded in existing code, screens, reports, and procedures
- create use cases/user stories for current and future behavior
- compare old and new data/report/interface behavior
- preserve or explicitly renegotiate important quality levels
- prioritize with business objectives, not nostalgia

When old requirements do not exist, reverse-engineer from system behavior, users, data, interfaces, logs, reports, tests, help docs, and operational procedures.

## Packaged Solution Projects

For COTS/SaaS/package selection, focus requirements at the user and business level. The package will constrain exact functional behavior.

Selection requirements:

- user tasks/use cases the package must support
- business rules that cannot be changed
- data needs and source/target systems
- quality requirements such as security, availability, usability, scalability, reporting, audit
- vendor, licensing, support, compliance, localization, and integration constraints
- evaluation scenarios and acceptance criteria

Implementation requirements:

- configuration requirements
- integration requirements
- extension/customization requirements
- data migration and mapping requirements
- business process changes
- security/role mapping
- reporting and analytics needs
- operational support requirements

Cautions:

- distinguish must-have needs from preferences that can adapt to the package
- avoid excessive customization unless business value justifies lifecycle cost
- perform fit-gap analysis against real user tasks, not feature checklists only

## Outsourced Projects

Outsourced work demands clearer written requirements because informal clarification is limited.

Provide:

- RFP or supplier brief with business objectives and scope
- rich user requirements and key functional requirements
- explicit quality attributes, interfaces, data, constraints, and acceptance criteria
- glossary and domain rules
- review/clarification cadence
- change-control process and contractual implications
- acceptance test responsibilities and evidence

Cautions:

- suppliers may build exactly what is written, not implied assumptions
- offshore/distributed work increases communication and cultural risks
- under-specified requirements create expensive iteration and disputes
- acceptance criteria must be objective before work is committed

## Business Process Automation Projects

Start with business process understanding.

Model:

- as-is processes: current tasks, roles, handoffs, systems, data, delays, controls
- to-be processes: desired future tasks, automation, decisions, exceptions, controls
- business performance metrics: cycle time, throughput, cost, error rate, compliance, user/customer satisfaction

Use swimlanes, BPMN, DFDs, use cases, event-response tables, and business rules.

Requirements should state how software supports improved processes, not merely automate poor current practice. When process redesign is part of the work, separate process requirements from software requirements.

## Business Analytics Projects

Analytics projects still need business, user, functional, and quality requirements, but decision and data understanding are central.

Elicit:

- business decisions to improve
- actions users will take from analytics
- questions the analytics must answer
- measures, KPIs, dimensions, definitions, and calculations
- data sources, lineage, ownership, quality, history, freshness, granularity
- transformations, algorithms, models, assumptions, and explainability needs
- reports, dashboards, alerts, exports, and drilldowns
- privacy, security, retention, audit, and compliance
- success metrics for analytics value

Use incremental development when stakeholders need to learn what analytics can provide. Prioritize by decision value and time sensitivity.

Cautions:

- do not start with tool/dashboard features before clarifying decisions
- vague metric definitions produce distrust
- data quality and lineage are requirements, not afterthoughts

## Embedded and Real-Time Systems

Use systems engineering thinking. Create a system requirements specification when hardware, software, people, and processes collaborate.

Key activities:

- define system requirements and allocate them to software, hardware, and manual components
- model context, states, events, timing, interfaces, and architecture
- specify external interfaces to sensors, actuators, networks, hardware, and operators
- specify timing requirements: latency, response deadlines, sampling rates, startup/shutdown, synchronization
- emphasize quality attributes: performance, efficiency, reliability, robustness, safety, security, usability
- use prototypes/proofs of concept for timing, performance, hardware interaction, and algorithm risk
- maintain strong traceability for safety, certification, and impact analysis

Cautions:

- software cannot always compensate for hardware limitations
- allocation decisions should be made top-down
- timing and safety requirements must be measurable
- interface changes can ripple across hardware, firmware, software, tests, and certification

## Tailoring Checklist

For any project class, decide:

- What is the requirements container: SRS, backlog, tool, contract, SyRS, package evaluation matrix?
- How much detail is needed before commitment?
- Who represents each user class?
- Which quality attributes drive architecture or vendor choice?
- Which artifacts require formal validation?
- What level of traceability is justified by risk, scale, regulation, or outsourcing?
- How will changes be evaluated and communicated?
- Which project-specific risks require mitigation?
