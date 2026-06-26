---
name: domain-context
license: MIT
compatibility: Works with any AI coding assistant that supports the Agent Skills specification. No system packages or network access required.
metadata:
  author: ryan-price
  version: "1.5"
description: >
  Progressive Domain Crystallization (PDC) — a skill for building and maintaining a living
  domain knowledge base for any custom business application. Use this skill whenever the user
  is developing a business application and wants the AI to accumulate understanding of internal
  terminology, entities, relationships, and business rules over time — especially when that
  knowledge is not fully defined upfront and grows across sessions. Trigger on any of:
  "remember how our system works", "learn our domain", "track business entities", "build
  domain knowledge", "understand our terminology", "grow AI context over time", "domain
  model", "business rules documentation", or whenever a user says the AI doesn't understand
  their business-specific language or data model. Also use at the start of any session where
  a .tasks/domain.md file exists in the project — always read it before doing any work.
---

# Progressive Domain Crystallization (PDC) Skill

## What This Skill Does

This skill enables any AI assistant to build and use a **living domain knowledge base** for any business
application — accumulated incrementally across sessions through a human-AI collaborative protocol.

The AI never "knows" the domain by default. But with this skill, it can:
- Read a structured `.tasks/domain.md` file at the start of every session
- Use internal terminology and entity names exactly as the business defines them
- Flag gaps in domain understanding inline during work
- Propose structured additions to the domain file for human review
- Never corrupt the knowledge base — all updates are proposed, not auto-applied
- Manage domain knowledge growth through progressive disclosure — loading only what's relevant to the current session

---

## Core Protocol

### At Session Start

1. **Look for .tasks/domain.md** in the project root
2. If found → check the file structure:
   - **Single file** (under ~200 lines): Read it completely before doing any work.
   - **Index + detail files** (split structure): Read the root .tasks/domain.md index (Tier 1 — core context). Then determine which Tier 2 detail files are relevant to the current task and load only those. See § Progressive Disclosure.
3. If not found → offer to initialize one using the template at `.tasks/domain.md`
4. Confirm to the user: "I've loaded the domain context for [Project Name]. I'm familiar with [N] entities and [N] flows." If in split mode, also note: "I've loaded the core context. I'll pull in detail files as needed for what we're working on."

### During Work

- Use entity names, terminology, and abbreviations **exactly as defined** in .tasks/domain.md
- When encountering an undefined term or entity, mark it inline: `[UNKNOWN: <term>]`
- When a relationship between entities is unclear, mark it: `[RELATIONSHIP UNCLEAR: <entity-a> → <entity-b>]`
- When a business rule seems to be implied but isn't documented: `[RULE INFERRED: <description>]`
- Do not invent domain facts — use only what is documented or what the user confirms in session
- When working on a specific entity or flow, load its Tier 2 detail file if one exists and hasn't been loaded yet

### At Session End

Always generate a `## 📋 Proposed Domain Updates` section at the bottom of your final response.

Format it as:

```markdown
## 📋 Proposed Domain Updates

> Review these and copy any confirmed items into your .tasks/domain.md

### New Entities Discovered
- **[EntityName]**: [Definition as understood from this session]
  - Attributes: [list]
  - Related to: [other entities]

### Terminology Clarified
- `[term]` → [plain definition]

### Relationships Identified
- [Entity A] → [verb] → [Entity B]: [description]

### Business Rules Observed
- [Rule description]

### Open Questions
- [ ] [Question about something ambiguous or unresolved]

### Suggested .tasks/domain.md Sections to Add/Update
- [ ] [specific section or entry to update]
```

The human reviews this, edits as needed, and manually updates .tasks/domain.md. This keeps the human as domain authority.

---

## Progressive Disclosure

Domain knowledge files grow over time. A single .tasks/domain.md that works well at 80 lines becomes unwieldy at 400. Progressive disclosure keeps the AI focused on what's relevant to the current session without losing access to the full knowledge base.

### Three Tiers of Domain Knowledge

| Tier | What It Contains | When It's Loaded | Typical Size |
|------|-----------------|-------------------|-------------|
| **Tier 1 — Core** | Project overview, terminology glossary, entity names (one-liners only), business rules table, user roles table | **Always**, at session start | 80–120 lines |
| **Tier 2 — Working Context** | Full entity descriptions (lifecycle, notes, edge cases), full flow step-by-steps, relationship map, integration points | **On demand**, when the session touches that entity or flow | 30–80 lines per file |
| **Tier 3 — Archive** | Changelog, resolved open questions, data migration notes, vendor-specific details | **On explicit request**, or when reviewing project history | Variable |

### What Goes in Each Tier

**Tier 1 — Core (root .tasks/domain.md, always loaded):**
- `## Project Overview` — what it is, who uses it, business goal (5 lines)
- `## Domain Boundaries` — what's in scope, what's supporting, what's explicitly excluded. Prevents overbuilding.
- `## Terminology Glossary` — the shorthand table
- `## Entity Registry` — **names and one-liner descriptions only** (not full attribute lists, not lifecycle details, not notes). Think of this as a table of contents for the entities.
- `## State Models` — named enumerations and valid state transitions for entities with statuses or lifecycle stages. The AI must treat these as the only valid values.
- `## Business Rules` — the hard rules table (BR-001, BR-002, etc.). These are ground truth the AI must always know.
- `## User Roles` — the roles table
- `## Stakeholder Map` — named people, their relationship to the system, their key concerns, and when to involve them. Critical for adoption and buy-in.
- `## Open Questions` — current unresolved items
- `## Detail Files` — index of Tier 2 files with one-line summaries (see file layout below)

**Tier 2 — Working Context (separate files, loaded by task):**
- Full entity specs — attributes, lifecycle, relationships, notes, edge cases (one file per major entity)
- Full flow descriptions — step-by-step process walkthroughs (one file per flow)
- Relationship map — the full entity-to-entity table
- Integration points — external system details

**Tier 3 — Archive (separate files, loaded on request):**
- Changelog — session-by-session history of what was learned
- Resolved questions — historical record of closed open questions
- Data migration notes — vendor catalog details, import procedures
- Vendor-specific details — price sheet structures, portal access notes

### When to Split: The ~200 Line Rule

A single .tasks/domain.md works well for early-stage projects. The trigger to split is simple:

**When .tasks/domain.md exceeds ~200 lines, propose the split.**

Say to the user: "The domain file is getting substantial — [N] lines with [N] entities and [N] flows. Want me to split it into an index file with detail files? This keeps sessions focused on what's relevant without losing anything."

If the user agrees, restructure into the tiered file layout (see below). If they prefer a single file, respect that — it's a preference, not a hard requirement.

### How the AI Uses Tiers at Session Start

```
1. Read root .tasks/domain.md (Tier 1 — always)
      ↓
2. Understand the current task
      ↓
3. Determine which entities/flows are relevant
      ↓
4. Load only those Tier 2 files
      ↓
5. Work — loading additional Tier 2 files if the task expands
      ↓
6. Propose updates — specifying which file each update belongs to
```

Example: User says "I need to update the PM renewal flow." The AI:
1. Reads root .tasks/domain.md (core context — knows all entity names, all business rules)
2. Loads `docs/domain/flows/pm-renewal.md` (the relevant flow)
3. Loads `docs/domain/entities/pm-renewal.md` (the relevant entity)
4. Does NOT load `docs/domain/flows/lead-distribution.md` or `docs/domain/entities/customer.md` — not relevant to this task.

### Proposing Updates in Split Mode

When the domain is split across files, the Proposed Domain Updates section should specify **which file** each update belongs to:

```markdown
## 📋 Proposed Domain Updates

### Update: `.tasks/domain.md` (Tier 1 — core)
- Add to Business Rules: BR-013 — [rule description]

### Update: `docs/domain/entities/pm-renewal.md` (Tier 2)
- Add attribute: `priceAdjustmentPercent` — annual price increase applied on renewal

### New File: `docs/domain/flows/engineering-review.md` (Tier 2)
- [Full flow description to create]

### Update: `docs/domain/archive/changelog.md` (Tier 3)
- [Session summary entry]
```

### Versioning

.tasks/domain.md includes a version header in its frontmatter. This is the human-readable version — it tells the AI and the team what state the domain knowledge is in.

**Version format:** `MAJOR.MINOR`
- **MAJOR** increments when the fundamental scope changes (new business process, major entity restructure, domain boundary shift)
- **MINOR** increments on every approved update (new entities, new rules, flow adjustments, stakeholder additions)

**Who increments:** The system auto-increments MINOR on each approved update. MAJOR is incremented manually when the team decides the domain has fundamentally expanded.

**The version header lives in the .tasks/domain.md frontmatter:**

```markdown
> **Version:** 1.5
> **Last updated:** 2026-04-06 (Session 30)
> **Changes:** +Commission Report entity, +BR-013–015, updated Quote-to-Close flow
```

**On every approved update, the AI must:**
1. Increment the version number (MINOR +1)
2. Update the "Last updated" date and session reference
3. Update the "Changes" line with a brief summary
4. Append an entry to the Changelog section

**If the system uses git**, the commit message should mirror the Changes line. The version header and git history serve different audiences — the header is for the AI and the business user, git is for engineering.

---

## .tasks/domain.md File Structure

See `.tasks/domain.md` for the full template.

### Single-File Mode (under ~200 lines)

The file uses these top-level sections, all in one file:

| Section | Tier | Purpose |
|---|---|---|
| `## Project Overview` | 1 | What the app does, who uses it, primary goals |
| `## Domain Boundaries` | 1 | What's in scope, what's supporting, what's excluded |
| `## Terminology Glossary` | 1 | Internal jargon mapped to plain definitions |
| `## Entity Registry` | 1 (names) / 2 (details) | Business objects with attributes and descriptions |
| `## State Models` | 1 | Valid statuses, types, and state transitions for entities |
| `## Relationship Map` | 2 | How entities connect to each other |
| `## Flow Catalog` | 2 | Named business processes with step-by-step info flow |
| `## Business Rules` | 1 | Constraints, validations, edge cases |
| `## Integration Points` | 2 | External systems, APIs, data sources |
| `## User Roles` | 1 | Who uses the system and what they can do |
| `## Stakeholder Map` | 1 | Named people, their relationship to the system, concerns, involvement timing |
| `## Open Questions` | 1 | Unresolved ambiguities — reviewed and cleared over time |
| `## Changelog` | 3 | What was learned and when |

In single-file mode, all tiers are in one file. This is fine — the tier labels are just annotations that guide the future split.

### Split-File Mode (over ~200 lines)

```
your-project/
├── .tasks/domain.md                   ← Tier 1: Core index (always loaded)
├── docs/
│   └── domain/
│       ├── entities/                  ← Tier 2: One file per major entity
│       │   ├── quote.md
│       │   ├── customer.md
│       │   ├── product.md
│       │   └── ...
│       ├── flows/                     ← Tier 2: One file per business process
│       │   ├── quote-to-close.md
│       │   ├── pm-renewal.md
│       │   └── ...
│       ├── relationships.md           ← Tier 2: Full relationship map
│       ├── integrations.md            ← Tier 2: External system details
│       └── archive/                   ← Tier 3: Historical records
│           ├── changelog.md
│           └── resolved-questions.md
└── ... (rest of your project)
```

The root .tasks/domain.md in split mode contains:
- Tier 1 sections in full (Project Overview, Domain Boundaries, Glossary, Entity names table, State Models, Business Rules, User Roles, Stakeholder Map, Open Questions)
- A `## Detail Files` index pointing to each Tier 2 file with a one-line summary:

```markdown
## Detail Files

| File | Contents |
|------|----------|
| `docs/domain/entities/quote.md` | Quote entity — lifecycle, attributes, status workflow |
| `docs/domain/entities/customer.md` | Customer/Account entity — parent-child, territory assignment |
| `docs/domain/flows/quote-to-close.md` | Full quote lifecycle from opportunity to installation |
| `docs/domain/flows/pm-renewal.md` | PM contract renewal process |
| `docs/domain/relationships.md` | Complete entity relationship map |
| `docs/domain/integrations.md` | Salesforce, Watertight, Procore, vendor portals |
| `docs/domain/archive/changelog.md` | Session-by-session learning history |
```

---

## Initialization Workflow

If no .tasks/domain.md exists, the AI should:

1. Ask the user 5 seed questions (see `references/seed-questions.md`)
2. Use the answers to populate the template
3. Write a draft .tasks/domain.md
4. Present it for review before saving

The initial file will be well under 200 lines. Start in single-file mode. Split later when it grows.

---

## Growing the Domain Over Time

Each session follows this cycle:

```
READ .tasks/domain.md (+ relevant Tier 2 files if split)
      ↓
DO WORK (flag unknowns inline)
      ↓
PROPOSE UPDATES (specify target file if split)
      ↓
HUMAN REVIEWS & APPROVES
      ↓
HUMAN UPDATES .tasks/domain.md (or detail files)
      ↓
(next session reads updated files)
```

### Growth Lifecycle

```
Sessions 1–3:     Single .tasks/domain.md, ~60–80 lines      (Tier 1 only)
Sessions 4–10:    Single .tasks/domain.md, ~100–200 lines     (Tier 1 + 2 mixed)
Sessions 10+:     Split into index + detail files       (Tier 1 / 2 / 3 separated)
Mature project:   Full three-tier structure with archive
```

When the file crosses ~200 lines, the AI should proactively offer to split:

> "The domain file is at [N] lines now — it covers [N] entities and [N] flows in detail. Want me to split it into a core index file with separate detail files? Each session would load just the parts relevant to what we're working on, and nothing is lost."

If the user agrees:
1. Extract Tier 1 content into a slim root .tasks/domain.md (~80–120 lines)
2. Move each entity's full description into `docs/domain/entities/[name].md`
3. Move each flow's full description into `docs/domain/flows/[name].md`
4. Move relationship map and integration points into their own Tier 2 files
5. Move changelog into `docs/domain/archive/changelog.md`
6. Add the `## Detail Files` index to the root .tasks/domain.md
7. Present the new structure for review before saving

Over time, the .tasks/domain.md becomes the single source of truth for:
- New developers onboarding
- Future AI sessions (any model, any tool)
- Documentation and specs
- Test case grounding

---

## Reference Files

- `.tasks/domain.md` — Blank template to initialize a new domain file
- `references/seed-questions.md` — Questions to ask when bootstrapping a new domain
- `references/entity-template.md` — Template for individual entity files (large projects)
- `references/anti-patterns.md` — Common mistakes to avoid when building domain context
