---
name: software-architecture-design
version: 1.1.0
author: sunbinbin
license: MIT
tags: architecture, system-design, technical-design, sop, mermaid, plantuml, web, mobile, ml, embedded, data-pipeline
description: "Produces a complete software architecture design document following a 12-phase SOP. Supports web backend, mobile, ML/AI, data pipeline, embedded/IoT. Generates Mermaid and PlantUML diagrams. Use when asked to do architecture design, system design, technical design, or says: 做架构设计 系统设计 技术方案 架构文档."
metadata: {"openclaw": {"emoji": "🏗️", "os": ["darwin", "linux", "win32"]}}
---

# Software Architecture Design SOP

## Step 0 — Identify Architecture Type First

Before starting the 12 phases, identify the architecture type and load the matching specialization:

| Type | Trigger keywords | Specialization file |
|------|-----------------|---------------------|
| Web / API backend | API, 后端, 服务端, REST, 微服务, SaaS | `{baseDir}/specializations/web-backend.md` |
| ML / AI system | 模型, 推理, 训练, 算法平台, AI, LLM | `{baseDir}/specializations/ml-system.md` |
| Data pipeline | ETL, 数据仓库, 数据湖, Kafka, Spark | `{baseDir}/specializations/data-pipeline.md` |
| Embedded / IoT | 嵌入式, 固件, MCU, RTOS, 硬件, CAN | `{baseDir}/specializations/embedded.md` |
| Mobile app | iOS, Android, Flutter, React Native | `{baseDir}/specializations/mobile.md` |
| General / Mixed | (none of the above match clearly) | Use base SOP only |

Read the matched specialization file for domain-specific guidance on Phases 3, 6, 7, 9.

---

## Core Principles (apply throughout)

- **Constraint-driven** — Every decision traces back to a hard constraint (compliance, budget, team, deployment env).
- **Decision explicit** — For every non-trivial choice, show Option A vs Option B and the reason for selection.
- **MVP-first** — Define a clear MVP boundary. Defer everything not critical to v1.
- **Diagram every concept** — Each major phase produces at least one diagram (see diagram guide in `{baseDir}/reference.md`).
- **Executable** — The architecture must be buildable by the stated team with the stated tech stack.

---

## Phase 1 — Requirement Intake

**Input**: Requirements doc, RFP, PRD, user stories, or verbal description.

1. Classify all requirements:
   - **Functional** — what the system does (features, user journeys)
   - **Non-functional** — performance, availability SLA, latency, throughput, data volume
   - **Compliance / regulatory** — industry standards, data residency, audit requirements
   - **Deployment constraints** — air-gap, on-prem, cloud, edge, hardware limits, OS
2. List the top 5 user roles and their primary use cases.
3. Capture all explicit exclusions ("out of scope").
4. List open questions / ambiguities — ask the user to resolve before proceeding.

---

## Phase 2 — System Context & Boundary

1. Draw **System Context Diagram** (C4 Level 1): system as a black box + external actors + external systems.
2. Define MVP delivery boundary — two tables:
   - **MVP Includes**: feature / category / success criteria
   - **MVP Excludes**: feature / deferred to version / reason
3. State **performance targets** as a table: metric / target value / measurement method.

---

## Phase 3 — Layered Architecture

1. Select the architecture pattern and justify it against Phase 1 constraints:
   - Options: Layered (N-tier), Event-driven, Microservices, Plugin-based, Pipe-and-filter, Serverless, Monolith-first
2. Define 3–5 layers: name / responsibility / key technologies / protocol to adjacent layer.
3. Produce **Layer Architecture Diagram**.
4. Refer to the loaded specialization for domain-specific layer guidance.

---

## Phase 4 — Module Decomposition

1. Decompose each layer into cohesive, single-responsibility modules.
2. Draw **Module Dependency Diagram** (DAG — must have no cycles).
3. For each module: name / layer / one-sentence responsibility / key technology.

---

## Phase 5 — Core Business Flows

1. Identify the 3–7 most critical end-to-end flows.
2. For each flow: draw a **Sequence Diagram** or **Flowchart**.
3. For stateful entities: define **State Machine** (states + transitions + error states).
4. Document exception handling: what fails → what recovers → who is notified.

---

## Phase 6 — Data Architecture

1. Draw **ER Diagram** covering all core entities.
2. Storage selection table: data type → storage component → justification.
   - Rule: choose the simplest storage that meets the requirement. Escalate only when constrained.
3. Define key entity schemas: name / critical fields / types / indexes.
4. Data lifecycle: retention policy / archival / backup strategy.

---

## Phase 7 — Technology Selection

1. For each component category, compare **exactly two options** (A vs B selected).
2. Produce **Tech Stack Table**: category / selection / version / rationale.
3. Validate every selection against Phase 1 constraints (offline? open-source license? team skill?).
4. Record deliberate technical debt: "Chose X for MVP; plan to migrate to Y in vN because...".

---

## Phase 8 — Interface Design

1. **External API**: all endpoints in a table — method / path / purpose / sync or async / auth required.
2. **Extension contract (SPI/plugin)**: if the system is extensible, define the standard interface every extension must implement.
3. **Async protocols**: describe WebSocket, SSE, or message queue contracts.
4. **Error schema**: standard error response format + error code list.
5. **Versioning strategy**: URL path versioning (`/v1/`) or header-based.

---

## Phase 9 — Deployment Architecture

1. Draw **Deployment Topology Diagram**.
2. Server / hardware specs table: scenario / specs / notes.
3. All runtime components: name / role / port or address / resource requirements / restart policy.
4. Data flow between components: what data, which protocol, sync or async.
5. CI/CD pipeline: trigger → build → test → package → deploy steps.
6. Refer to the loaded specialization for deployment model specifics.

---

## Phase 10 — Non-Functional Design

Address all four areas:

| Area | Required content |
|------|-----------------|
| **High Availability** | Per failure scenario: what breaks, recovery action, RTO target |
| **Performance** | Each NFR target + specific implementation strategy to achieve it |
| **Security** | Auth/authz model, data isolation, secrets management, audit logging |
| **Observability** | MVP-phase monitoring (health endpoints, key logs) → full metrics plan |

---

## Phase 11 — MVP Scope Lock

1. Finalize **MVP Includes / Excludes** tables with target versions.
2. State **success criteria** — measurable conditions that define MVP as "done".
3. List all technical debt decisions with rationale.

---

## Phase 12 — Risk Register

Risk table: description / probability (H/M/L) / impact (H/M/L) / mitigation strategy.

Must include at least one risk from each category:
- Dependency (3rd-party libs, hardware, external APIs)
- Integration (external systems, compliance verification)
- Delivery (scope creep, unknowns requiring POC, timeline)

---

## Diagram Generation Guide

For every diagram, produce Mermaid code (preferred) or PlantUML code. See `{baseDir}/reference.md` for templates and when to use which tool.

| Phase | Diagram | Tool |
|-------|---------|------|
| 2 | System Context | Mermaid C4 or PlantUML C4 |
| 3 | Layer Architecture | PlantUML component or Mermaid graph |
| 4 | Module Dependencies | Mermaid graph TD |
| 5 | Sequence / Flow | Mermaid sequenceDiagram / flowchart |
| 5 | State Machine | Mermaid stateDiagram-v2 |
| 6 | ER Diagram | Mermaid erDiagram |
| 9 | Deployment Topology | PlantUML deployment |
| 9 | CI/CD Pipeline | Mermaid flowchart LR |

---

## Output

Follow the document chapter structure in `{baseDir}/template.md`.
After all 12 phases, self-check against the phase-by-phase checklist in `{baseDir}/reference.md`.
