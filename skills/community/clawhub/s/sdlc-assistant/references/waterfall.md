# Waterfall SDLC Reference Guide

> **Analogy:** Waterfall is like constructing a bridge - you complete every design drawing, get all approvals, then build from foundation to deck. Going back to change the foundation after laying the road surface is expensive and risky.

---

## Waterfall Phases & Roles

### Phase 1: Requirements Gathering & Analysis

**Goal:** Capture all business and system requirements before any design or coding begins.

| Role | Key Tasks |
|------|-----------|
| **BA** | Conduct stakeholder interviews, workshops; produce BRD (Business Requirements Document) |
| **PO** | Validate business requirements align to strategic goals, sign off on BRD |
| **PM** | Manage scope boundary, stakeholder communication plan, project kick-off |
| **Dev** | Review for technical feasibility, flag ambiguities early |
| **QA** | Review for testability; begin drafting Master Test Plan |

**Artifacts:** Business Requirements Document (BRD), Functional Requirements Document (FRD), Stakeholder Register, Project Charter, RTM (shell)

**Sign-off Gate:** BRD / FRD signed by business stakeholders before proceeding.

> **Tip:** Any requirement change after this gate requires a formal **Change Request (CR)** - documented, estimated, approved, and logged.

---

### Phase 2: System Design

**Goal:** Translate requirements into technical architecture and detailed design.

**Sub-phases:**
- **High-Level Design (HLD):** Architecture, technology stack, system interfaces
- **Low-Level Design (LLD):** Module design, DB schema, API specifications, class diagrams

| Role | Key Tasks |
|------|-----------|
| **Dev** | Produce HLD and LLD documents, architecture diagrams, API contracts |
| **BA** | Validate design maps completely to requirements; update RTM |
| **QA** | Review design for testability; define test environment requirements |
| **PM** | Confirm design review milestones are met; track design sign-off |
| **PO** | Approve UI/UX designs and prototypes |

**Artifacts:** HLD Document, LLD Document, DB Schema, API Specification, UI Wireframes/Prototypes, Test Environment Plan

**Sign-off Gate:** Design documents reviewed and signed off before development begins.

---

### Phase 3: Development / Implementation

**Goal:** Build the system based on approved design documents.

| Role | Key Tasks |
|------|-----------|
| **Dev** | Code modules per LLD, write unit tests, conduct peer code reviews |
| **QA** | Finalize test cases, prepare test data, set up test environments |
| **BA** | Answer clarification queries from developers; maintain requirements traceability |
| **PM** | Track progress against schedule (Gantt), manage risks, report status weekly |
| **PO** | Available for critical clarifications; monitor milestone delivery |

**PM Tracking Tools:**
- Gantt Chart - track timeline vs. actuals
- Risk Register - log and monitor risks
- RAID Log - Risks, Assumptions, Issues, Dependencies

> **Analogy:** Development in Waterfall is like a factory assembly line - each station (module) must complete its task before passing to the next. No component skips its station.

---

### Phase 4: Testing / Quality Assurance

**Goal:** Systematically verify the system meets all specified requirements.

| Role | Key Tasks |
|------|-----------|
| **QA** | Execute test cases per Master Test Plan, log defects with severity/priority |
| **Dev** | Fix defects within agreed SLA, perform unit/integration re-tests |
| **BA** | Support UAT scripting; verify requirements coverage via RTM |
| **PO** | Conduct UAT sessions; sign off UAT completion |
| **PM** | Track defect lifecycle, hold go/no-go review meeting |

**Testing Phases:**

| Phase | Owner | Description |
|-------|-------|-------------|
| Unit Testing | Dev | Individual module testing |
| Integration Testing | Dev + QA | Module-to-module interface testing |
| System Testing | QA | End-to-end functional testing |
| Regression Testing | QA | Verify fixes didn't break existing functionality |
| Performance / Load Testing | QA | Non-functional requirements validation |
| UAT (User Acceptance Testing) | PO / Business | Business sign-off on full system |
| SIT (System Integration Testing) | QA + Dev | Third-party/external system integration |

**QA Entry Criteria:**
- Development phase complete
- Unit tests passed
- Build deployed to test environment
- Test cases reviewed and approved

**QA Exit Criteria:**
- All test cases executed
- No open P1/P2 (Critical/High) defects
- Defect closure rate meets agreed threshold
- UAT sign-off obtained

---

### Phase 5: Deployment / Release

**Goal:** Move the tested, approved system into production.

| Role | Key Tasks |
|------|-----------|
| **Dev** | Prepare deployment package, write runbook, configure environments |
| **QA** | Smoke test on production (or staging mirror), verify deployment sign-off checklist |
| **PM** | Coordinate release window, send go-live communication, manage rollback plan |
| **PO** | Final business approval for go-live, prepare user communications |
| **BA** | Update operational documentation, user manuals, training materials |

**Deployment Checklist:**
- [ ] All UAT defects closed or risk-accepted
- [ ] Deployment runbook reviewed
- [ ] Rollback procedure documented and rehearsed
- [ ] Production environment verified
- [ ] Backup taken before deployment
- [ ] Deployment window approved by stakeholders
- [ ] Post-deployment smoke test plan ready
- [ ] Support team briefed

> **Analogy:** Deployment is like launching a satellite. You have one window. You prepare exhaustively. You don't improvise.

---

### Phase 6: Maintenance & Support

**Goal:** Sustain system health, handle production issues, and manage enhancement requests.

| Role | Key Tasks |
|------|-----------|
| **Dev** | Hotfix critical production bugs, code reviews for patches |
| **QA** | Regression test patches; update test suite for defect fixes |
| **PM** | Track post-release defects; manage SLA for support tickets |
| **PO** | Gather user feedback; prioritize enhancement backlog |
| **BA** | Document changes; assess enhancement requests via formal CR process |

**Change Request (CR) Process:**
1. CR raised with business justification
2. Impact analysis by Dev + BA
3. Estimation and approval by PM + PO
4. CR scheduled into next release cycle
5. Development and testing per mini-waterfall
6. Sign-off and release

---

## Waterfall Document Hierarchy

```
Project
 Project Charter
 Requirements
    BRD (Business Requirements Document)
    FRD (Functional Requirements Document)
    RTM (Requirement Traceability Matrix)
 Design
    HLD (High-Level Design)
    LLD (Low-Level Design)
    API / DB Specifications
 Testing
    Master Test Plan
    Test Cases
    Defect Log
    UAT Sign-off Report
 Deployment
    Deployment Runbook
    Release Notes
 Closure
     Lessons Learned
     Project Closure Report
```

---

## Waterfall Sign-off Gates

| Gate | Before Phase | Signatories |
|------|-------------|-------------|
| Requirements Baseline | Design | Business Stakeholders, PO, PM |
| Design Baseline | Development | Tech Lead, BA, PM |
| Test Readiness Review | System Testing | QA Lead, PM |
| UAT Sign-off | Deployment | Business Owner, PO |
| Go-Live Approval | Production Deployment | PM, PO, IT Head |
| Project Closure | Archive | PM, Sponsor |

---

## Requirement Traceability Matrix (RTM) - Template

| Req ID | Requirement Description | Design Ref | Dev Module | Test Case IDs | Status |
|--------|------------------------|------------|------------|---------------|--------|
| REQ-001 | User must login with MFA | LLD-AUTH-01 | auth.service | TC-001, TC-002 | Passed |
| REQ-002 | System must handle 1000 concurrent users | LLD-PERF-01 | load-balancer | TC-045 | In Progress |

---

## Waterfall vs Agile - Quick Comparison

| Dimension | Waterfall | Agile |
|-----------|-----------|-------|
| Planning | Upfront, comprehensive | Iterative, just-in-time |
| Change management | Formal CR process | Backlog adjustment |
| Deliverable cadence | Single release at end | Working software every sprint |
| Best for | Fixed-scope, compliance-heavy, hardware-integrated | Evolving requirements, fast feedback needed |
| Documentation | Heavy, formal | Lightweight, living docs |
| Risk | Front-loaded discovery | Distributed across sprints |
| Customer involvement | At requirements + UAT | Every sprint |
