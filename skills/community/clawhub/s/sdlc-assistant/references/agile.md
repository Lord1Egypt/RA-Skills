# Agile SDLC Reference Guide

> **Analogy:** Agile is like navigating with GPS - you have a destination, but the route adjusts in real time based on traffic (feedback, changing requirements).

---

## Agile Phases & Roles

### Phase 1: Project Initiation / Discovery

**Goal:** Align on vision, scope, and team structure.

| Role | Key Tasks |
|------|-----------|
| **PO** | Define product vision, create initial product backlog, identify stakeholders |
| **BA** | Elicit high-level requirements, create As-Is / To-Be process maps |
| **PM** | Set up project infrastructure, define team norms, create project charter |
| **Dev** | Review high-level requirements, flag feasibility concerns |
| **QA** | Review scope for testability, identify high-risk areas early |

**Artifacts:** Product Vision Statement, Initial Backlog, Project Charter, Stakeholder Map

---

### Phase 2: Sprint Planning

**Goal:** Commit to a set of backlog items for the sprint.

| Role | Key Tasks |
|------|-----------|
| **PO** | Prioritize and present backlog items, clarify acceptance criteria |
| **BA** | Ensure stories are well-defined and unambiguous |
| **PM** | Facilitate the ceremony, track capacity and velocity |
| **Dev** | Estimate effort (story points), break stories into tasks |
| **QA** | Review stories for testability, flag missing edge cases |

**Artifacts:** Sprint Backlog, Sprint Goal, Capacity Plan

> **Tip:** A story is "sprint-ready" when it is: Independent, Negotiable, Valuable, Estimable, Small, Testable - the INVEST criteria.

---

### Phase 3: Design

**Goal:** Define how the solution will be built - UI, architecture, data model.

| Role | Key Tasks |
|------|-----------|
| **Dev** | System design, DB schema, API contracts, component breakdown |
| **BA** | Validate design maps to requirements, update use cases |
| **PO** | Review UI/UX mockups, approve design direction |
| **QA** | Review design for testability; identify automation hooks |
| **PM** | Track design sign-off, flag dependencies |

**Artifacts:** Architecture Diagram, Wireframes/Mockups, API Spec, Data Dictionary

---

### Phase 4: Development (Sprint Execution)

**Goal:** Build features to the Definition of Done.

| Role | Key Tasks |
|------|-----------|
| **Dev** | Code features, write unit tests, raise PRs, participate in code review |
| **QA** | Write test cases in parallel, set up test environments, begin exploratory testing |
| **BA** | Clarify requirement ambiguities as they arise (Just-In-Time refinement) |
| **PO** | Review completed items, give early feedback, manage scope creep |
| **PM** | Run daily standups, track blockers, update burndown chart |

**Key Ceremonies:**
- **Daily Standup** (15 min): What did I do? What will I do? Any blockers?
- **Backlog Refinement** (ongoing): Groom upcoming stories, add details, re-estimate

> **Analogy:** The sprint is like a relay race. Devs build, hand off to QA, who verify, then PO accepts - each leg matters.

---

### Phase 5: Testing / QA

**Goal:** Validate that features meet acceptance criteria and non-functional requirements.

| Role | Key Tasks |
|------|-----------|
| **QA** | Execute test cases, perform regression, log defects in tracker |
| **Dev** | Fix defects, write targeted unit/integration tests |
| **BA** | Validate requirements coverage, assist in UAT scripting |
| **PO** | Conduct UAT, approve or reject stories per AC |
| **PM** | Track defect metrics, assess sprint exit criteria |

**Test Types by Phase:**
| Type | Owner | When |
|------|-------|------|
| Unit Testing | Dev | During development |
| Integration Testing | Dev / QA | After unit testing |
| Functional / Regression | QA | End of sprint |
| UAT | PO / Business | Pre-release |
| Performance / Security | QA / Dev | Release sprint |

**Entry/Exit Criteria (Sprint):**
- Entry: Story approved, environment ready, test cases written
- Exit: All P1/P2 defects fixed, AC met, PO sign-off received

---

### Phase 6: Sprint Review & Demo

**Goal:** Showcase completed work to stakeholders and gather feedback.

| Role | Key Tasks |
|------|-----------|
| **Dev** | Demo features built |
| **PO** | Accept/reject stories, gather stakeholder feedback |
| **PM** | Facilitate, capture feedback as new backlog items |
| **BA** | Note any gaps vs. original requirements |
| **QA** | Report on quality metrics (defect counts, test coverage) |

---

### Phase 7: Sprint Retrospective

**Goal:** Inspect and adapt team process.

> **Analogy:** Retro is like a pit stop in Formula 1 - a brief pause to tune the car before the next race.

**Format (Start / Stop / Continue):**
- **Start**: Things we should begin doing
- **Stop**: Things that aren't working
- **Continue**: Things working well - keep doing them

**PM/Scrum Master** facilitates. **All team members** participate.

---

### Phase 8: Release / Deployment

**Goal:** Deliver working software to production safely.

| Role | Key Tasks |
|------|-----------|
| **Dev** | Prepare release branch, deployment scripts, environment config |
| **QA** | Final smoke test on staging, sign off release checklist |
| **PM** | Coordinate release window, notify stakeholders, manage go/no-go |
| **PO** | Approve go-live, prepare release notes for users |
| **BA** | Update process documentation, user manuals if needed |

**Release Checklist:**
- [ ] All planned stories are "Done"
- [ ] No P1/P2 open bugs
- [ ] Staging tested and signed off
- [ ] Rollback plan documented
- [ ] Deployment runbook prepared
- [ ] Stakeholders notified
- [ ] Monitoring/alerting configured

---

### Phase 9: Post-Release / Maintenance

**Goal:** Monitor, stabilize, and support the live product.

| Role | Key Tasks |
|------|-----------|
| **Dev** | Monitor logs, hotfix critical issues |
| **QA** | Monitor production defects, update regression suite |
| **PM** | Post-release status report, lessons learned |
| **PO** | Collect user feedback, update backlog |
| **BA** | Document lessons learned, update requirements for next cycle |

---

## Quick Reference: Agile Ceremonies

| Ceremony | Frequency | Who | Purpose |
|----------|-----------|-----|---------|
| Sprint Planning | Start of sprint | All | Commit to sprint goal |
| Daily Standup | Daily | Dev, QA, PM | Sync and unblock |
| Backlog Refinement | Mid-sprint | PO, BA, Dev, QA | Groom upcoming stories |
| Sprint Review | End of sprint | All + Stakeholders | Demo and accept work |
| Retrospective | End of sprint | Core team | Improve team process |

---

## Agile Metrics

| Metric | What It Measures | Who Uses It |
|--------|-----------------|-------------|
| Velocity | Story points completed per sprint | PM, PO |
| Burndown | Remaining work in a sprint | PM, Dev |
| Defect Density | Bugs per feature/story | QA, PM |
| Cycle Time | Time from "In Progress" to "Done" | Dev, PM |
| Sprint Goal Achievement | % of sprint goal met | PO, PM |
