# Requirements Elicitation Reference

Use this for requirements acquisition, stakeholder analysis, user classes, product champions, interview/workshop planning, observation, and raw input classification.

## Table of Contents

- Goals
- Stakeholders and User Classes
- Product Champions and Product Owners
- Elicitation Methods
- Planning and Preparing
- Performing Sessions
- Follow-Up
- Classifying Customer Input
- Done Criteria
- Cautions

## Goals

Elicitation discovers, clarifies, and revises stakeholder needs. Do not simply transcribe what customers say. Combine facilitated techniques with independent analysis, because different stakeholders reveal different kinds of requirements in different ways.

## Stakeholders and User Classes

Create a stakeholder register:

| Stakeholder | Role/interest | Requirement input | Decisions owned | Risk if omitted | Representative |
|---|---|---|---|---|---|

Classify user classes by:

- tasks and goals
- frequency and volume of use
- domain expertise
- system expertise
- permissions/security needs
- location and operating environment
- quality expectations
- favored or high-priority class status

Use a user class catalog:

| User class | Size/volume | Key tasks | Skill level | Environment | Quality concerns | Product champion |
|---|---|---|---|---|---|---|

Do not assume one user can speak for all users. If a user class has no representative, record the risk.

## Product Champions and Product Owners

A product champion represents a specific user class and makes or recommends decisions at the user-requirements level. They may:

- collect input from peers
- develop use cases, user stories, and scenarios
- resolve within-class conflicts
- define priorities and acceptance criteria
- review requirements and prototypes
- provide test data
- participate in UAT/beta testing
- evaluate change requests and user impact
- support adoption, documentation, or training

Product champion checks:

- belongs to or credibly understands the user class
- represents the class, not only personal preferences
- has time and authority
- communicates with peers
- can make timely decisions
- understands business scope boundaries

On agile projects, a product owner may span business, user, and functional decisions. For complex products, the product owner should still use product champions or BAs to cover multiple user classes.

## Elicitation Methods

Select multiple techniques:

| Method | Use when | Typical output |
|---|---|---|
| Interview | Need depth, executive goals, domain rules, sensitive topics | Notes, candidate requirements, glossary |
| Requirements workshop | Need collaboration, conflict resolution, fast shared modeling | Decisions, models, issue list, draft requirements |
| Focus group | Need input from representative users, especially for commercial products | Preferences, quality expectations, feature ideas |
| Observation/contextual inquiry | Users cannot fully articulate tacit work | Real task steps, workarounds, exceptions |
| Questionnaire | Need broad input from many users | Frequency/priority signals, pain-point data |
| System interface analysis | Existing or external systems interact | Interface needs, data exchanges, constraints |
| User interface analysis | Existing UI reveals workflows and missing behavior | Screen/task inventory, usability issues |
| Document analysis | Current procedures, forms, contracts, reports, regulations exist | Rules, fields, reports, compliance needs |
| Prototype evaluation | Interaction, workflow, or feasibility is uncertain | Feedback, missing requirements, revised flows |

Facilitated methods primarily discover business and user requirements. Independent methods reveal hidden rules, interfaces, data, implied functionality, and constraints.

## Planning and Preparing

Before sessions:

- confirm business objectives and scope boundaries
- select participants by user class, authority, knowledge, and availability
- define session objective and abstraction level
- prepare questions, straw-man models, draft use cases, process maps, or prototypes
- decide who facilitates, who scribes, and who controls scope/time
- send agenda and pre-read material
- plan parking lots for off-topic issues

Core questions:

- What business problem or opportunity is being addressed?
- What happens today, step by step?
- Who performs each task and who is affected?
- What triggers the work?
- What information is read, created, changed, approved, retained, or discarded?
- What exceptions, errors, delays, workarounds, and handoffs occur?
- What policies, regulations, standards, or computations govern the work?
- What external systems, devices, reports, documents, or APIs are involved?
- What quality expectations matter: performance, security, availability, usability, reliability, safety, integrity, interoperability?
- What must the system never do?
- What would make the first release successful?

## Performing Sessions

Use these facilitation practices:

- establish rapport and explain the session goal
- keep the discussion within the stated scope
- listen actively and paraphrase
- propose ideas when stakeholders cannot imagine options, while labeling them as candidate ideas
- capture parking-lot items without derailing the session
- timebox difficult topics
- make sure quiet participants are heard
- separate need, rule, constraint, design idea, and project issue
- note open questions immediately
- do not resolve every design problem during elicitation

For observations:

- select important or risky tasks
- limit disruption
- capture actor, trigger, data, tools, decisions, exceptions, timing, workarounds, approvals, and interruptions
- generalize from the observed individual to the user class only after validation

## Follow-Up

After each activity:

- organize notes quickly
- classify raw input
- publish decisions, assumptions, open issues, and parking-lot items
- assign owners and dates for follow-up
- update glossary and user class catalog
- revise models or requirement candidates
- validate important points with participants while memory is fresh

## Classifying Customer Input

Use this table while processing notes:

| Category | Use for |
|---|---|
| Business requirement | Desired business outcome, objective, metric, market need |
| User requirement | User goal/task, usage scenario, user story, use case candidate |
| Functional requirement | Observable software behavior under conditions |
| Quality attribute/NFR | Performance, usability, security, reliability, availability, safety, integrity, interoperability, etc. |
| External interface | User/software/hardware/communication interface |
| Business rule | Policy, regulation, fact, computation, inference, action enabler |
| Data requirement | Data definition, relationship, report, retention, integrity, migration |
| Constraint | Required technology, platform, standard, compatibility, physical/environment limit |
| Feature | Related capability set that delivers user value |
| Project requirement | Training, rollout, schedule, documentation, staffing, support task outside product behavior |
| Assumption/dependency | Belief or external condition needing confirmation |
| Issue/TBD | Missing decision or information |
| Solution idea | Candidate implementation to analyze for underlying need |

## Done Criteria

Elicitation is "done enough" for the current commitment when:

- business objectives and scope boundaries are stable enough
- all important user classes and stakeholders have been sampled or risk-accepted
- major business events, workflows, exceptions, reports, interfaces, and data sources are covered
- hidden assumptions and implied requirements have been actively searched for
- quality attributes have been elicited beyond vague adjectives
- open issues have owners and dates
- additional sessions are producing diminishing new information

## Cautions

- Insufficient user involvement is a leading source of requirements failure.
- Managers may override valid product champion decisions; clarify decision authority early.
- A product champion may speak only for personal preferences or power users; check coverage.
- Users may present design solutions; ask why until the real need is visible.
- Assumed and implied requirements are risky; make them explicit or document the risk.
- Too many workshop participants can reduce progress; keep active groups small and representative.
- A focus group gives input, not binding decisions, unless authority is explicitly granted.
- Elicitation without follow-up creates a pile of notes, not requirements.
