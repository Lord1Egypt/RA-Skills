---
name: requirements-spec
description: Assists in writing high-quality requirements documents using an 8-dimension framework. Covers background, objectives, scope, detailed flows, non-functional needs, data tracking, acceptance criteria, and risk assessment. Use when drafting, writing, reviewing, or structuring product requirements, PRDs, or requirements documents.
version: 1.0.0
---

# Requirements Specification

Framework for writing complete, measurable, and actionable requirements documents.

## Core Principles

1. **Completeness first** — All 8 dimensions must be covered; none optional
2. **Measurable** — Every objective and acceptance criterion must be quantifiable
3. **Clear and unambiguous** — Developers, testers, and product managers must reach the same understanding
4. **Risk-forward** — Identify risks early with mitigation plans

## The 8 Dimensions

### 1. Background (15%)

**What to include:**
- **Business context** — Why this requirement exists; what problem it solves
- **User scenario** — Who encounters what problem in which situation
- **Data support** — Metrics that demonstrate problem severity or opportunity size
- **Strategic alignment** — How this connects to team/org/company goals

**Checklist:**
- [ ] Explains "why" not just "what"
- [ ] Backed by concrete data or facts
- [ ] Identifies target user group
- [ ] Links to higher-level objectives

### 2. Objectives (20%)

**What to include:**
- **Core objective** — One sentence summarizing the desired outcome
- **SMART criteria:**
  - Specific — Clear and unambiguous
  - Measurable — Has quantifiable metrics
  - Achievable — Feasible within resource and time constraints
  - Relevant — Directly addresses the background problem
  - Time-bound — Has a clear deadline
- **Priority ranking** — Label must-have vs. nice-to-have

**Checklist:**
- [ ] Each objective follows SMART criteria
- [ ] Includes quantified targets (e.g., "reduce rejection rate from 30% to 20%")
- [ ] Objectives logically connect to background
- [ ] Distinguishes between must-achieve and stretch goals

### 3. Scope (20%)

**What to include:**
- **In Scope** — Explicit list of features/modules covered by this requirement
- **Out of Scope** — Explicitly excluded items to prevent scope creep
- **User stories** — Format: "As a [user], I want [action], so that [benefit]"
- **Feature list** — Structured feature list with priority labels (P0/P1/P2)
- **Boundary conditions** — Edge cases and exception handling scope

**Checklist:**
- [ ] Clear boundary between what is and isn't included
- [ ] Every feature has a priority label
- [ ] Covers both happy path and exception flows
- [ ] Specifies platform coverage (Web, mobile, mini-program, etc.)

### 4. Detailed Features & Flows (20%)

**What to include:**
- **Flow diagrams** — Mermaid or flowchart for key business processes
- **Feature descriptions** — Input, processing, output for each feature
- **Change highlights** — Diff against existing system; mark changes clearly
- **Test focus points** — Scenarios and edge cases that need special testing attention

**Checklist:**
- [ ] Flow diagram or sequence diagram exists
- [ ] Changes are clearly marked/highlighted
- [ ] Test focus points are documented
- [ ] Exception flows are covered

### 5. Non-Functional Requirements (5%)

**What to include:**
- **Performance** — Response time, concurrency, throughput targets
- **Operations confirmation** — Operations team sign-off and conclusions
- **Customer support SOP** — Standard operating procedures for support team

**Checklist:**
- [ ] Operations team has confirmed requirements
- [ ] Customer support SOP is documented
- [ ] Performance metrics are specified

### 6. Data Tracking (10%)

**What to include:**
- **Tracking plan** — Event names, trigger conditions, parameter definitions
- **Dashboard metrics** — Core metrics to monitor and dashboard design
- **Data validation** — How to verify tracking data accuracy

**Checklist:**
- [ ] Complete tracking plan exists
- [ ] Dashboard metrics are defined
- [ ] Data validation approach is specified

### 7. Acceptance Criteria (5%)

**What to include:**
- **Functional acceptance** — Acceptance conditions per feature
- **Acceptance scenarios** — Specific pre-launch test scenarios
- **Owner** — Person responsible for acceptance sign-off
- **Post-launch tracking** — Tracking cadence and metrics

**Checklist:**
- [ ] Every feature has corresponding acceptance conditions
- [ ] Criteria are quantifiable and verifiable
- [ ] Post-launch tracking plan exists

### 8. Risk Assessment (5%)

**What to include:**
- **System risks** — Technical implementation, stability concerns
- **Reputation risks** — User feedback, PR concerns
- **Business risks** — Revenue impact, operational disruption
- **Mitigation plans** — Response strategy and contingency plan per risk

**Checklist:**
- [ ] Key risks are identified
- [ ] Each risk has a mitigation plan
- [ ] Risk owner is assigned

## Workflow

### Step 1: Gather Information

Ask the user:
- Business background and goals
- Target users and scenarios
- Constraints (timeline, resources, technical)
- Existing reference docs or designs

### Step 2: Build the Document

Guide the user through each of the 8 dimensions. For missing information, ask targeted questions or propose reasonable defaults.

### Step 3: Quality Check

After drafting, review against each dimension's checklist. Flag gaps and suggest improvements.

### Step 4: Score Estimate

Rate the document quality:
- **Excellent (8.0+)** — All dimensions complete and high quality
- **Good (6.0-7.9)** — Core dimensions complete, minor items need polish
- **Acceptable (4.0-5.9)** — Main dimensions covered, several items need improvement
- **Needs Work (<4.0)** — Missing core dimensions or content severely incomplete

## Common Pitfalls

| Pitfall | Bad Example | Good Example |
|---------|-------------|--------------|
| Unquantified goal | "Improve user experience" | "Reduce page load from 3s to 1.5s" |
| Unclear scope | No Out of Scope section | Explicitly lists exclusions |
| Missing acceptance | Describes features only | Defines "done" criteria per feature |
| Ignored risks | No risk section | Identifies dependency risks with plans |

## Document Template

```markdown
# [Requirement Name]

## 1. Background
### 1.1 Business Context
### 1.2 User Scenario
### 1.3 Data Support
### 1.4 Strategic Alignment

## 2. Objectives
### 2.1 Core Objective
### 2.2 Quantified Metrics
### 2.3 Priorities

## 3. Scope
### 3.1 In Scope
### 3.2 Out of Scope
### 3.3 User Stories
### 3.4 Feature List

## 4. Detailed Features & Flows
### 4.1 Business Flow Diagram
### 4.2 Feature Descriptions
### 4.3 Change Highlights
### 4.4 Test Focus Points

## 5. Non-Functional Requirements
### 5.1 Performance
### 5.2 Operations Confirmation
### 5.3 Support SOP

## 6. Data Tracking
### 6.1 Tracking Plan
### 6.2 Dashboard Metrics
### 6.3 Data Validation

## 7. Acceptance Criteria
### 7.1 Functional Acceptance
### 7.2 Acceptance Scenarios
### 7.3 Post-Launch Tracking

## 8. Risk Assessment
### 8.1 Risk Register
### 8.2 Mitigation Plans
```

## Trigger

Activate when the user asks to write, draft, review, or structure a requirements document, PRD, or product spec.
