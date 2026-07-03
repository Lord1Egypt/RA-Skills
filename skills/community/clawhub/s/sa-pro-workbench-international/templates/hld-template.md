# High-Level Design (HLD)

> **Document ID**: `SA-HLD-{YYYYMMDD}-{ClientAbbreviation}`
> **Version**: v1.0
> **Confidentiality**: Internal Confidential
> **Author**: {Name}
> **Reviewer**: {Name}
> **Date**: {YYYY-MM-DD}

---

## Chapter 1 — Project Overview

### 1.1 Project Background
{Describe the background and business drivers that initiated the project}

### 1.2 Objectives
1. {Objective 1}
2. {Objective 2}
3. {Objective 3}

### 1.3 Scope
- **Organizational Scope**: {Which departments/units are involved}
- **Business Scope**: {Which business processes are involved}
- **System Scope**: {Which systems/modules are involved}
- **Data Scope**: {Which data domains are involved}

### 1.4 References
- {Relevant regulations / standards / policy documents}
- {Client's existing technical specifications}
- {Industry best practices}

---

## Chapter 2 — Requirements Analysis

### 2.1 Business Requirements

| ID | Business Requirement | Priority | Source |
|------|----------------------|----------|--------|
| BR-001 | | High / Medium / Low | |
| BR-002 | | | |

### 2.2 Functional Requirements

| ID | Functional Requirement | Priority | Related BR |
|------|------------------------|----------|-------------|
| FR-001 | | | |
| FR-002 | | | |

### 2.3 Non-Functional Requirements (NFR)

| Category | Requirement | Target |
|----------|-------------|--------|
| Performance | Response time | p95 ≤ {X} ms |
| Availability | System uptime | ≥ 99.{X}% |
| Security | Protection level | Level {X} |
| Scalability | Concurrent users | ≥ {X} |
| Data | Data retention period | {X} years |

### 2.4 Constraints
1. {Technical constraints}
2. {Schedule constraints}
3. {Budget constraints}
4. {Compliance constraints}

---

## Chapter 3 — Overall Architecture Design

### 3.1 Design Principles
1. **{Principle 1}**: {Description}
2. **{Principle 2}**: {Description}
3. **{Principle 3}**: {Description}

### 3.2 System Context Diagram (C1)
{Insert C1 system context diagram showing interactions between the system and external users/systems}

### 3.3 Container Diagram (C2)
{Insert C2 container diagram showing the main technical services / applications / databases within the system}

---

## Chapter 4 — Business Architecture

### 4.1 Business Capability Map
{Insert business capability map, displayed at L1–L3 levels}

### 4.2 Core Business Processes

#### 4.2.1 Process 1: {Process Name}
{Insert swimlane diagram / BPMN process flow}

#### 4.2.2 Process 2: {Process Name}
{Insert process flow diagram}

---

## Chapter 5 — Application Architecture

### 5.1 Application Breakdown

| Application / Module | Functional Description | Technology Stack | Deployment Method |
|----------------------|------------------------|------------------|-------------------|
| | | | |
| | | | |

### 5.2 Application Integration

| Source System | Target System | Integration Method | Data Flow Direction | Frequency |
|---------------|---------------|-------------------|---------------------|-----------|
| | | API / Messaging / File | | Real-time / Near-real-time / Batch |

### 5.3 Functional Architecture Diagram
{Insert functional architecture diagram}

---

## Chapter 6 — Data Architecture

### 6.1 Data Domain Breakdown

| Data Domain | Description | Master Data / Transaction Data / Analytical Data |
|-------------|-------------|---------------------------------------------------|
| | | |
| | | |

### 6.2 Core Data Model (Conceptual Level)
{Insert ER diagram or five-layer data architecture diagram}

### 6.3 Data Flow
{Insert DFD data flow diagram (Level 0–1)}

### 6.4 Data Governance
- **Data Standards**: {Standards adopted}
- **Data Quality**: {Quality rules}
- **Master Data Management**: {MDM strategy}
- **Data Security**: {Classification and tiering strategy}

---

## Chapter 7 — Technology Architecture

### 7.1 Technology Selection

| Technology Domain | Selection | Version | Rationale |
|-------------------|-----------|---------|-----------|
| Programming Language | | | |
| Framework | | | |
| Database | | | |
| Middleware | | | |
| Frontend | | | |
| Deployment | | | |

### 7.2 Deployment Architecture
{Insert deployment architecture diagram, including CIDR / security groups / instance specifications}

### 7.3 Network Topology
{Insert network topology diagram}

### 7.4 Key Architecture Decisions (ADR)

| ADR ID | Decision | Status | Rationale |
|--------|----------|--------|-----------|
| ADR-001 | | Proposed / Accepted / Deprecated | |
| ADR-002 | | | |

---

## Chapter 8 — Security Architecture

### 8.1 Security Framework
{Refer to NIST CSF 2.0 or equivalent standards}

### 8.2 Identity & Access Control
- **Authentication Method**: {SSO / LDAP / MFA}
- **Authorization Model**: {RBAC / ABAC / ReBAC}
- **Audit Logging**: {Scope and retention period}

### 8.3 Data Security
- **Encryption in Transit**: {TLS version}
- **Encryption at Rest**: {Encryption algorithm}
- **Data Masking Policy**: {Rules}

---

## Chapter 9 — Implementation Plan

### 9.1 Implementation Roadmap
{Insert Gantt chart / roadmap}

### 9.2 Phased Rollout

| Phase | Timeline | Deliverables | Acceptance Criteria |
|-------|----------|--------------|---------------------|
| Phase 1 | | | |
| Phase 2 | | | |
| Phase 3 | | | |

### 9.3 Organizational Structure

| Role | Responsibilities | Suggested Candidate |
|------|-----------------|---------------------|
| Project Sponsor | | |
| Project Manager | | |
| Technical Lead | | |
| Business Lead | | |

---

## Chapter 10 — Operations Plan

### 10.1 Operations Model
- {Internal operations / Outsourced operations / Hybrid}

### 10.2 SLI / SLO Definitions

| Service | SLI | SLO | Measurement Method |
|---------|-----|-----|-------------------|
| | | | |
| | | | |

### 10.3 Disaster Recovery Plan
- **RTO (Recovery Time Objective)**: {Target recovery time}
- **RPO (Recovery Point Objective)**: {Target recovery point}
- **Strategy**: {Hot standby / Warm standby / Cold standby}

---

## Chapter 11 — Cost Estimation

### 11.1 One-Time Investment

| Item | Description | Estimated Amount |
|------|-------------|------------------|
| Software Licenses | | |
| Hardware Equipment | | |
| Implementation Services | | |
| Training | | |

### 11.2 Annual Operating Cost

| Item | Description | Annual Estimated Amount |
|------|-------------|-------------------------|
| Operations Services | | |
| Cloud Resources | | |
| License Renewals | | |

### 11.3 TCO 5-Year Overview
{Insert TCO analysis table}

---

## Chapter 12 — Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| | | | |
| | | | |

---

*Template Version: v1.0 | Skill: sa-pro-workbench*