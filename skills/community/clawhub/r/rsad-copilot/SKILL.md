---
name: ibm-rsad-copilot
description: >
  Use this skill when working with IBM Rational Software Architect Designer (RSAD/RSA) in the context
  of IBM FTM (Financial Transaction Manager) development. Trigger when the user mentions: IBM RSA,
  IBM RSAD, Rational Software Architect, UML modeling in FTM, Service Participant design, Channel
  design, FSM modeling in RSA, state machine diagrams, UML sequence diagrams for payments, UML use
  case diagrams, class diagrams, RSA stereotypes, PMP_Alert, PMP_Terminal, PMP_OpsControl, FSM
  export to SQL, RSA config scripts, RSA workspace, RSA profiles, model-driven development for FTM,
  design artifacts for FTM, producing FTM design artifacts, RSA transformations, UML to SQL export,
  FTM design phase, modeling payment flows, designing FTM interfaces, or any RSA/RSAD design-time
  task in the FTM development workflow. Also trigger when the user is in the DESIGN step of the
  FTM methodology (Design → Build → Deploy → Operate). When in doubt, trigger this skill.
license: MIT
metadata:
  version: 1.0.0
  tags:
    - ibm
    - rsad
    - rsa
    - rational-software-architect
    - uml
    - ftm
    - payments
    - modeling
    - fsm
    - design
  author:
    name: Shoaib Khan
    github: https://github.com/ShoaibKhan
    email: shoaibthedev@gmail.com
---

# IBM RSAD Copilot

You are an expert IBM Rational Software Architect Designer (RSAD) practitioner specializing in IBM
FTM (Financial Transaction Manager) development. You help teams produce design artifacts, model
Service Participants and FSMs, create UML diagrams, and export configuration to DB2 — all within
the FTM design methodology.

> Note: IBM RSA and IBM RSAD refer to the same Eclipse-based modeling tool. "RSA" is the common
> shorthand used in FTM documentation.

## Role of RSAD in FTM

RSAD is the **design-time tool** in the FTM development lifecycle:

```
1. DESIGN (RSAD)  → Model SPs, Channels, FSMs, sequence diagrams → export SQL config scripts
2. BUILD  (ACE)   → Implement mapper flows + action subflows → package as BAR files
3. DEPLOY         → Import config to DB2 + deploy BARs to integration node
4. OPERATE (OAC)  → Monitor transaction states, resolve alerts, manage SP lifecycle
```

Every FTM interface begins in RSAD. The models you create here drive both the DB2 configuration
and the ACE implementation.

## Core References

- [UML Modeling](references/uml-modeling.md) — Diagram types, when to use each, FTM-specific content
- [FTM Design Workflow](references/ftm-design-workflow.md) — Step-by-step interface design process, SP/Channel modeling
- [FSM Design](references/fsm-design.md) — State machines: states, transitions, events, stereotypes, export
- [Mapping Design](references/mapping-design.md) — Mapping strategies, metadata modeling, technology selection
- [Patterns & Artifacts](references/patterns-artifacts.md) — All 15 FTM patterns with required RSAD artifacts

## Key Concepts

| Concept | Description |
|---|---|
| **Service Participant (SP)** | Represents an external system or internal FTM service; has channels, FSMs, and configuration |
| **Channel** | Communication path on an SP; carries a specific message format and transport |
| **FSM (Finite State Machine)** | Defines transaction/transmission lifecycle; modeled as UML state machine in RSAD |
| **ISF** | Internal Standard Format — IBM's ISO 20022-based canonical XML (`http://www.ibm.com/xmlns/prod/ftm/isf/v3`) |
| **UML Profile** | RSAD's mechanism for adding FTM-specific stereotypes (PMP_Alert, PMP_Terminal, etc.) to UML elements |
| **SQL Export** | RSAD generates DB2 INSERT scripts from models; these are the deployment config artifacts |
| **Transformation** | RSAD feature that generates code/config from UML models (model-to-text or model-to-model) |

## Standard Design Artifacts

Every FTM interface requires these 7 artifacts produced in RSAD:

| # | Artifact | Diagram Type | Purpose |
|---|---|---|---|
| 1 | Functional Use Case | Use Case | Shows actors, the new interface, and related SPs |
| 2 | Functional Sequence | Sequence | End-to-end message flow across systems |
| 3 | Object Lifecycle | State Machine | FSM for transaction or transmission object |
| 4 | SP/Channel Config | Class / RSA Model | Defines SP attributes, channels, mapper references |
| 5 | Service Interaction | Sequence | Detailed technical flow within FTM components |
| 6 | Deployment Topology | Deployment | Integration node, servers, MQ queues, external systems |
| 7 | SQL Config Scripts | (Export) | DB2 INSERT statements generated from the RSAD model |

## FTM UML Profiles and Stereotypes

RSAD uses stereotypes to annotate FTM-specific semantics on UML states:

| Stereotype | Applies To | Meaning |
|---|---|---|
| `PMP_Alert` | State | Operator-visible alert in OAC; requires `Constraints` tag |
| `PMP_Terminal` | State | Final lifecycle state (e.g., Completed, Cancelled) |
| `PMP_OpsControl` | State | Requires operator interaction; not an alert |

**PMP_Alert Constraints** (tagged values): `Cancel`, `Resubmit`, `Release`, `Continue`

Always apply `PMP_Alert` on every failure path. Every alert state must have at least one Constraint.

## Quick Design Checklist

When designing a new FTM interface in RSAD:

- [ ] Identify the FTM pattern (9.1–9.15) for this interface
- [ ] Draw functional use case diagram (actors + new SP + related SPs)
- [ ] Draw functional sequence diagram (inbound PT flow → EP flow → action → outbound)
- [ ] Model the SP with channels, mapper references, and transport config
- [ ] Model the FSM(s): states, transitions, events, actions
  - [ ] Every path has a terminal state
  - [ ] Every path has a `PMP_Alert` state with Constraints
  - [ ] Heartbeat transitions use Object Filter on `timeout`
- [ ] Select mapping technology (ESQL / Java / XSLT / WTX)
- [ ] Export SQL config scripts from RSAD model
- [ ] Validate exported SQL against DB2 schema

## Typical Workflow (JIRA → RSAD → ACE → PR)

When a JIRA ticket requires a new or modified FTM interface:

1. Read JIRA ticket and Confluence description to understand the change
2. Open RSAD workspace and locate the relevant SP/Channel model
3. Modify or create the required UML diagrams (use case, sequence, FSM)
4. Apply correct stereotypes and tagged values to FSM states
5. Export updated SQL config scripts from the model
6. Hand off to ACE implementation: implement mapper flows and action subflows
7. Commit design artifacts and SQL scripts; open Bitbucket PR for human review
