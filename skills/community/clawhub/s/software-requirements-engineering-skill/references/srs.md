# SRS Reference

Use this for drafting, improving, or reviewing a software requirements specification or equivalent requirements repository.

## Table of Contents

- SRS Purpose
- SRS Template
- Requirement IDs and Attributes
- Excellent Requirement Qualities
- Writing Rules
- Functional Requirements
- Data Requirements
- External Interfaces
- Quality Attributes and Constraints
- Agile Specification
- SRS Quality Gate

## SRS Purpose

An SRS states the software product's required behavior, data, interfaces, quality attributes, constraints, and other requirements precisely enough for planning, design, construction, testing, documentation, training, maintenance, and change control.

"Document" means any agreed container: a document, spreadsheet, repository, backlog, requirements management tool, diagrams, or a generated report.

Do not include project tasks, design, construction, or test implementation details unless they are true constraints or necessary acceptance information.

## SRS Template

Tailor this structure:

1. **Introduction**
   - purpose
   - document conventions
   - intended audience and reading suggestions
   - product scope
   - references

2. **Overall Description**
   - product perspective
   - product functions summary
   - user classes and characteristics
   - operating environment
   - design and implementation constraints
   - user documentation
   - assumptions and dependencies

3. **System Features**
   - feature name/description
   - priority
   - functional requirements
   - related use cases/user stories
   - error/invalid-input handling

4. **Data Requirements**
   - logical data model
   - data dictionary
   - reports/dashboards
   - data acquisition, integrity, retention, and disposal
   - migration/conversion where product behavior is involved

5. **External Interface Requirements**
   - user interfaces
   - software interfaces
   - hardware interfaces
   - communication interfaces

6. **Quality Attributes**
   - usability
   - performance
   - security/privacy
   - safety
   - availability, reliability, robustness, integrity, interoperability, scalability, portability, installability, modifiability, reusability, verifiability, efficiency as relevant

7. **Internationalization and Localization**
   - language, culture, laws, currencies, dates, numbers, addresses, units, time zones, paper sizes, naming order, spelling conventions

8. **Other Requirements**
   - legal/regulatory/financial compliance
   - installation/configuration/startup/shutdown
   - logging/monitoring/audit trail
   - operational or transition requirements that affect the software

9. **Appendices**
   - glossary
   - analysis models
   - TBD list
   - traceability references

## Requirement IDs and Attributes

Use stable, persistent IDs:

| Prefix | Meaning |
|---|---|
| BR | Business requirement |
| UR | User requirement |
| US | User story |
| UC | Use case |
| FR | Functional requirement |
| NFR | Quality/nonfunctional requirement |
| IR | External interface requirement |
| DATA | Data requirement |
| BRULE | Business rule |
| CON | Constraint |
| TBD | To be determined |

Recommended attributes:

| Attribute | Purpose |
|---|---|
| ID/title | Stable reference |
| Text | Requirement statement |
| Type | Classification |
| Source/origin | Who or what supplied it |
| Rationale | Why it is needed |
| Owner/contact | Who answers questions/decides changes |
| Priority | Release and trade-off decisions |
| Status | Lifecycle state |
| Release/iteration | Baseline allocation |
| Verification method | Test, inspection, demonstration, analysis |
| Acceptance criteria | Objective pass/fail expectations |
| Trace links | Parent/child, tests, design, code, docs |

## Excellent Requirement Qualities

Individual requirement statements should be:

- complete: enough information for readers to understand and implement/test
- correct: accurately represents a real need or source
- feasible: possible within technical and project constraints
- necessary: supports business value, user need, regulation, rule, or justified constraint
- prioritized: ranked for release and trade-off decisions
- unambiguous: reasonable readers reach the same interpretation
- verifiable: objective tests, inspection, demonstration, or analysis can confirm satisfaction

Requirement collections should be:

- complete enough for the commitment being made
- consistent across levels, artifacts, and related requirements
- modifiable through unique labels, one requirement per statement, low redundancy, and change history
- traceable backward to origins and forward to downstream artifacts

## Writing Rules

Use clear, direct language:

- write complete sentences
- use active voice and named actors/user classes
- keep each requirement separately identifiable
- state trigger/precondition when behavior depends on one
- define terms in glossary and data dictionary
- avoid synonyms for the same concept
- avoid subjective words unless quantified
- record rationale/source when not obvious
- use tables, models, and structured lists when clearer than prose

Useful functional requirement patterns:

```text
[optional precondition] [optional trigger event] the system shall [expected system response].
```

```text
The [user class/actor] shall be able to [action] [object] [qualifying condition or quality statement].
```

Avoid:

- "support", "handle", "allow appropriate", "fast", "easy", "robust", "seamless", "as needed"
- compound statements that hide multiple requirements
- negative requirements when positive behavior is clearer
- design choices unless they are real constraints
- open-ended lists such as "including but not limited to" without bounds

## Functional Requirements

A functional requirement describes observable system behavior under specified conditions. Include:

- actor or triggering event
- precondition/state if relevant
- expected system response
- data read/created/updated/deleted
- alternative and exception handling
- business rule references
- related user requirement/use case/story
- acceptance criteria or verification method

## Data Requirements

Specify:

- logical data entities and relationships
- data dictionary: meaning, type, format, length, allowed values, units, source of truth
- data quality: accuracy, completeness, timeliness, reconciliation, integrity checks
- reports/dashboards: audience, purpose, fields, filters, grouping, sorting, totals, calculations, frequency, freshness, export
- acquisition and interfaces
- retention, disposal, archive, cache, temporary data, and audit obligations

Do not bury data definitions in glossary if they belong in a data dictionary.

## External Interfaces

For each interface specify:

- participating system/user/device/network
- purpose
- data/message formats and mappings
- validation and error handling
- timing, throughput, frequency, and availability expectations
- security, authentication, authorization, encryption, privacy
- protocol/version/standard
- ownership and change-control path

Interface changes require communication and change control across both sides of the interface.

## Quality Attributes and Constraints

External quality attributes:

- availability
- installability
- integrity
- interoperability
- performance
- reliability
- robustness
- safety
- security
- usability

Internal quality attributes:

- efficiency
- modifiability
- portability
- reusability
- scalability
- verifiability

For each important quality attribute:

| Field | Meaning |
|---|---|
| Tag/ID | Stable reference |
| Rationale/source | Why and who needs it |
| Scale | Unit of measurement |
| Meter | How measurement will be made |
| Goal | Minimum acceptable target |
| Stretch/wish | Better target if useful |
| Conditions | Platform, load, data, user class, environment |
| Verification | Test/analysis/demo/inspection method |

This is a lightweight Planguage-style structure. Use the full Planguage mindset when quality goals are risky or contentious: define the tag, ambition/rationale, scale, meter, goal, stretch/wish values, source, and environmental assumptions so "fast", "secure", or "available" becomes measurable.

Use SMART and fit-criteria thinking: specific, measurable, attainable, relevant, time-sensitive. Prioritize quality attributes because they can conflict, such as security versus performance.

Constraints restrict design/implementation choices. Record source and rationale. Ask why a constraint exists to uncover the underlying requirement.

## Agile Specification

For agile work:

- use product/release backlog as a requirements container
- write user stories with acceptance criteria
- split large stories into implementable slices
- keep NFRs visible alongside stories; do not postpone cross-cutting quality attributes
- derive backlog items from business objectives, user requirements, rules, and quality needs
- maintain enough traceability for impact analysis and acceptance

## SRS Quality Gate

Review before baseline:

- each requirement has ID, source, rationale, owner, priority, status, release/iteration, verification method
- no vague adjective remains without a measurable fit criterion or TBD
- functional requirements include conditions and responses
- external interfaces include data formats, mappings, errors, security, and ownership
- quality attributes are measurable and prioritized
- business rules and constraints are separated
- data requirements and reports are explicit
- assumptions/dependencies/TBDs are owned
- glossary and data dictionary are aligned
- requirement set is complete enough, consistent, modifiable, and traceable
