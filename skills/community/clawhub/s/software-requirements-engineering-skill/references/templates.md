# Templates Reference

Use these forms when producing requirements engineering artifacts. Tailor sections to project risk and lifecycle.

## Table of Contents

- Vision and Scope
- Stakeholder and User Class Registers
- Product Champion Agreement
- Elicitation Plan and Notes
- Event-Response Table
- Use Case
- User Story
- Business Rules Catalog
- Requirement Table
- SRS Skeleton
- Quality Attribute Requirement
- Data Dictionary and Report Spec
- Review Defect Log
- Acceptance Criteria
- Change Request
- Impact Analysis
- Traceability Matrix
- Risk Register

## Vision and Scope

```markdown
# Vision and Scope

## 1. Business Requirements
### 1.1 Background
### 1.2 Business Opportunity or Problem
### 1.3 Business Objectives and Success Metrics
| ID | Objective | Metric | Target | Owner | Deadline |
### 1.4 Customer or Market Needs
### 1.5 Business Risks

## 2. Scope and Limitations
### 2.1 Major Features
| Feature ID | Feature | Business objective | Priority | Release |
### 2.2 Scope of Initial Release
### 2.3 Scope of Subsequent Releases
### 2.4 Limitations and Exclusions

## 3. Business Context
### 3.1 Stakeholder Profiles
### 3.2 Project Priorities
### 3.3 Operating Environment
### 3.4 Assumptions and Dependencies
```

## Stakeholder and User Class Registers

| Stakeholder | Role/interest | Requirement input | Decisions owned | Representative | Risk if omitted |
|---|---|---|---|---|---|

| User class | Size/volume | Key tasks | Skill level | Environment | Quality concerns | Product champion |
|---|---|---|---|---|---|---|

## Product Champion Agreement

| User class | Champion | Authority | Time commitment | Responsibilities | Backup/peer group | Escalation |
|---|---|---|---|---|---|---|

## Elicitation Plan and Notes

Plan:

| Session | Objective | Method | Participants | Inputs/prework | Outputs | Date |
|---|---|---|---|---|---|---|

Notes:

| Date | Source | Method | Raw statement/finding | Classification | Candidate requirement/TBD | Owner |
|---|---|---|---|---|---|---|

## Event-Response Table

| Event ID | Event/trigger | Source | Condition/state | System response | Related UC/FR | Priority |
|---|---|---|---|---|---|---|

## Use Case

```markdown
## UC-XX: Use Case Name

| Field | Content |
|---|---|
| Primary actor | |
| Supporting actors/systems | |
| Stakeholders/interests | |
| Goal | |
| Preconditions | |
| Trigger | |
| Minimal guarantee | |
| Success guarantee/postconditions | |
| Frequency/volume | |
| Priority | |

### Main Success Scenario
1. 

### Alternative Flows

### Exceptions

### Business Rules

### Special Requirements

### Data Used or Produced

### Open Issues
```

## User Story

```markdown
## US-XX
As a <user class>, I want <goal/capability> so that <business/user value>.

### Acceptance Criteria
- Given ...

### Notes
| Source | Priority | Estimate | Risk | Related BR/UC/NFR |
```

## Business Rules Catalog

| ID | Rule statement | Type | Source | Rationale | Enforcement point | Related requirements |
|---|---|---|---|---|---|---|

## Requirement Table

| ID | Type | Requirement | Source | Rationale | Owner | Priority | Status | Release | Verification | Trace |
|---|---|---|---|---|---|---|---|---|---|---|

## SRS Skeleton

```markdown
# Software Requirements Specification

## 1. Introduction
### 1.1 Purpose
### 1.2 Document Conventions
### 1.3 Intended Audience and Reading Suggestions
### 1.4 Product Scope
### 1.5 References

## 2. Overall Description
### 2.1 Product Perspective
### 2.2 Product Functions
### 2.3 User Classes and Characteristics
### 2.4 Operating Environment
### 2.5 Design and Implementation Constraints
### 2.6 User Documentation
### 2.7 Assumptions and Dependencies

## 3. System Features
### 3.x Feature Name
#### 3.x.1 Description and Priority
#### 3.x.2 Functional Requirements

## 4. Data Requirements
### 4.1 Logical Data Model
### 4.2 Data Dictionary
### 4.3 Reports and Dashboards
### 4.4 Data Acquisition, Integrity, Retention, and Disposal

## 5. External Interface Requirements
### 5.1 User Interfaces
### 5.2 Software Interfaces
### 5.3 Hardware Interfaces
### 5.4 Communications Interfaces

## 6. Quality Attributes
### 6.1 Usability
### 6.2 Performance
### 6.3 Security and Privacy
### 6.4 Safety
### 6.x Other Quality Attributes

## 7. Internationalization and Localization

## 8. Other Requirements

## Appendix A. Glossary
## Appendix B. Analysis Models
## Appendix C. TBD List
```

## Quality Attribute Requirement

Use this as a Planguage-lite form for measurable quality goals.

| Field | Content |
|---|---|
| ID/tag | |
| Ambition/rationale | |
| Attribute | |
| Rationale/source | |
| Scale | |
| Meter/verification method | |
| Goal | |
| Stretch/wish | |
| Conditions/environment | |
| Related FR/UC/US | |

## Data Dictionary and Report Spec

Data dictionary:

| Data item | Definition | Type/format | Allowed values | Source of truth | CRUD users | Quality rule | Retention |
|---|---|---|---|---|---|---|---|

Report/dashboard:

| Report ID | Purpose/decision | Audience | Frequency | Fields/calculations | Filters/sort/grouping | Data sources | Freshness | Access |
|---|---|---|---|---|---|---|---|---|

## Review Defect Log

| Defect ID | Artifact/section | Requirement ID | Defect type | Severity | Description | Owner | Disposition | Due date |
|---|---|---|---|---|---|---|---|---|

## Acceptance Criteria

| ID | Related requirement/story | Scenario | Given | When | Then | Quality/data expectation |
|---|---|---|---|---|---|---|

## Change Request

| Field | Description |
|---|---|
| CR ID/title | |
| Submitter/date | |
| Description | |
| Reason/business value | |
| Affected requirement IDs | |
| Desired release/urgency | |
| Priority | |
| Impact summary | |
| Decision | |
| Decision authority/date | |
| Implementation owner | |
| Verification evidence | |

## Impact Analysis

| Area | Impact | Affected items | Effort/cost | Risk | Owner |
|---|---|---|---|---|---|
| Business objectives/scope | | | | | |
| Requirements/models | | | | | |
| Architecture/design/code/config | | | | | |
| Interfaces/data/reports | | | | | |
| Tests/acceptance | | | | | |
| Documentation/training/support | | | | | |
| Schedule/budget/resources | | | | | |
| Compliance/security/operations | | | | | |

## Traceability Matrix

| Business objective | BR | User class | UC/US/Event | FR/NFR/IR/DATA/BRULE/CON | Design/config | Test/acceptance | Docs/support |
|---|---|---|---|---|---|---|---|

## Risk Register

| ID | Risk | Category | Probability | Impact | Trigger | Mitigation | Contingency | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|
