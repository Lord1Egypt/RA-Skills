# [Project Name] — Domain Context File

> **What is this file?**
> This is a living knowledge base for the AI working on this project. It defines the business
> domain: who the users are, what the core entities are, how they relate, and what the rules are.
> It grows over time as the AI and team learn more. The AI reads this at the start of every session.
>
> **Who maintains it?** The human team. The AI proposes updates; humans review and apply them.
> **Where does it live?** Project root as `DOMAIN.md`, or `docs/domain/DOMAIN.md`.
>
> **Version:** [1.0]
> **Last updated:** [YYYY-MM-DD] ([session name or source])
> **Changes:** [brief summary of last update — e.g., "+3 entities, +2 rules, updated Quote-to-Close flow"]
>
> **Progressive Disclosure:** Sections are marked with tiers.
> - **Tier 1 (Core)** — Always loaded at session start. Ground truth.
> - **Tier 2 (Working Context)** — Loaded on demand when the session touches that entity or flow.
> - **Tier 3 (Archive)** — Loaded on explicit request.
>
> When this file exceeds ~200 lines, split Tier 2 and 3 sections into `docs/domain/` files
> and keep this file as a Tier 1 index. See SKILL.md § Progressive Disclosure.

---

## Project Overview
<!-- TIER 1 — always loaded -->

**Project Name:** [Name]
**Description:** [1-3 sentences: what does this app do and who is it for?]
**Primary Users:** [Who uses this system day-to-day?]
**Business Goal:** [What problem does it solve / what value does it deliver?]
**Stage:** [e.g., Discovery / MVP / Active Development / Mature]

---

## Domain Boundaries
<!-- TIER 1 — always loaded -->

> What's in scope, what's supporting, and what's explicitly excluded.
> This prevents the AI from overbuilding or making assumptions about adjacent systems.

### Core operational scope
- [Primary capability 1 — e.g., "Inventory control for individual SKUs"]
- [Primary capability 2]
- [Primary capability 3]

### Supporting scope
- [Supporting system or feature — e.g., "Seeded product catalog for dev/staging"]
- [Supporting system or feature]

### Explicitly out of scope
- [What this system does NOT do — e.g., "Does not handle payment processing"]
- [Adjacent system that exists but is not part of this domain]

### Explicit domain notes
- [Clarifications about source of truth — e.g., "The operational SKU registry is the source of truth, not the seeded product catalog"]

---

## Terminology Glossary
<!-- TIER 1 — always loaded -->

> Internal jargon, abbreviations, and domain-specific terms used by staff.
> Format: `term` → definition

| Term | Definition | Notes |
|------|-----------|-------|
| `[term]` | [plain definition] | [any context or synonyms] |
| `[term]` | [plain definition] | |

---

## Entity Registry
<!-- TIER 1 (names + one-liners) / TIER 2 (full descriptions) -->

> The core "things" in this business domain — objects that have identity, attributes, and behavior.
>
> In single-file mode, full details live here.
> In split mode, this section has names and one-liners only. Full specs live in `docs/domain/entities/`.

### [EntityName]

**What it is:** [1-2 sentence plain description]
**Also called:** [synonyms or aliases used internally]
**Key attributes:**
- `[attribute]`: [type and description]
- `[attribute]`: [type and description]

**Lifecycle:** [How does this entity come into existence? How does it end/expire/close?]
**Owner:** [Which user role or system is responsible for this entity?]
**Notes:** [Any quirks, edge cases, or important context]

---

### [EntityName]

**What it is:**
**Also called:**
**Key attributes:**
**Lifecycle:**
**Owner:**
**Notes:**

---

## State Models
<!-- TIER 1 — always loaded -->

> Named enumerations and state machines for entities that have explicit statuses or lifecycle stages.
> These are the valid values the system enforces — not suggestions.

### [Entity or attribute name] statuses
- `[status_1]`
- `[status_2]`
- `[status_3]`

### [Entity or attribute name] types
- `[type_1]`
- `[type_2]`

> For entities with sequential workflows, document the valid transitions:
> `new` → `picking` → `packing` → `ready_to_ship` → `shipped`
> Exception states: `on_hold` (requires note, can resume), `cancelled` (requires Management)

---

## Relationship Map
<!-- TIER 2 — loaded when working on entity connections -->

> How entities connect to each other. Use plain verb phrases.
> Format: `[Entity A]` → [verb] → `[Entity B]` : [description]

| From | Relationship | To | Notes |
|------|-------------|-----|-------|
| `[Entity]` | has many | `[Entity]` | [description] |
| `[Entity]` | belongs to | `[Entity]` | [description] |
| `[Entity]` | triggers | `[Entity]` | [description] |
| `[Entity]` | references | `[Entity]` | [description] |

---

## Flow Catalog
<!-- TIER 2 — loaded when working on a specific flow -->

> Named business processes — sequences of steps with information moving through entities.
>
> In single-file mode, full step-by-step details live here.
> In split mode, this section has flow names and one-liners only. Full specs live in `docs/domain/flows/`.

### [Flow Name]

**Description:** [What does this flow accomplish?]
**Triggered by:** [What starts it? User action, event, schedule?]
**Actors:** [Which users or systems are involved?]

**Steps:**
1. [Step 1 — who does what, what entity is involved]
2. [Step 2]
3. [Step 3]
4. ...

**Outcome:** [What is the end state?]
**Edge Cases:** [What can go wrong or differ?]

---

### [Flow Name]

**Description:**
**Triggered by:**
**Actors:**
**Steps:**
1.
2.
**Outcome:**
**Edge Cases:**

---

## Business Rules
<!-- TIER 1 — always loaded. These are ground truth. -->

> Constraints, validations, and behavioral rules that govern the system.
> These are facts the AI must treat as ground truth.

| Rule ID | Rule | Applies To | Notes |
|---------|------|-----------|-------|
| BR-001 | [Rule description] | [Entity or Flow] | [source or context] |
| BR-002 | [Rule description] | [Entity or Flow] | |

---

## Integration Points
<!-- TIER 2 — loaded when working on external system connections -->

> External systems, APIs, databases, or services this app connects to.

| System | Purpose | Direction | Notes |
|--------|---------|-----------|-------|
| [System name] | [what it does for us] | In / Out / Both | [auth, format, frequency] |

---

## User Roles
<!-- TIER 1 — always loaded -->

> Who uses the system and what they can do.

| Role | Description | Key Permissions |
|------|-------------|----------------|
| `[role]` | [who they are] | [what they can do] |

---

## Stakeholder Map
<!-- TIER 1 — always loaded -->

> People identified during discovery who interact with or are affected by the system.
> This is not an org chart. It maps individuals to their relationship with the system
> being built — what they do, what they care about, and when their input matters.
>
> Named people create accountability. Unnamed roles create gaps.
> When a name is mentioned, capture it. When only a role is mentioned, add an Open Question.

| Name | Role | Relationship to System | Key Concern | Involve When |
|------|------|----------------------|-------------|--------------|
| [name] | [title/function] | [sponsor / power user / downstream consumer / approval gate / beneficiary] | [what will make them resist or champion] | [phase or feature area] |

> **Relationship types:**
> - **Sponsor** — initiated the project, has budget authority, needs to see ROI
> - **Power user** — uses the system daily, has deep process knowledge, will reject if it doesn't match their workflow
> - **Downstream consumer** — receives output from the system (reports, documents, handoffs), cares about format and reliability
> - **Approval gate** — must approve or review before something proceeds, cares about accuracy and control
> - **Beneficiary** — benefits from the system but wasn't involved in designing it (e.g., new hires who need guided workflows)

---

## Open Questions
<!-- TIER 1 — always loaded -->

> Unresolved ambiguities. Review and clear these as they get answered.

- [ ] [Question — added [date]]
- [ ] [Question — added [date]]

---

## Detail Files
<!-- TIER 1 — always loaded (only present in split mode) -->

> Index of Tier 2 and Tier 3 detail files. Add entries here when the domain is split.

<!--
| File | Contents |
|------|----------|
| `docs/domain/entities/[entity].md` | [one-line summary] |
| `docs/domain/flows/[flow].md` | [one-line summary] |
| `docs/domain/relationships.md` | Complete entity relationship map |
| `docs/domain/integrations.md` | External system details |
| `docs/domain/archive/changelog.md` | Session-by-session learning history |
-->

---

## Changelog
<!-- TIER 3 — loaded on request or during project review -->

> What was learned and when. AI proposes entries; human approves.
> In split mode, move this to `docs/domain/archive/changelog.md`.

| Date | Session Summary | Entities Added | Rules Added |
|------|----------------|----------------|-------------|
| [YYYY-MM-DD] | [Brief description of session] | [list] | [list] |

