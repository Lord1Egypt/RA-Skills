# domain-context

**Progressive Domain Crystallization (PDC)** — a skill for building and maintaining a living domain knowledge base for any custom business application.

## What It Does

Enables any AI assistant to accumulate understanding of a customer's business domain over time — terminology, entities, relationships, business rules, processes, stakeholders, and institutional knowledge — through a human-AI collaborative protocol.

The AI reads a structured `DOMAIN.md` file at the start of every session, uses domain terminology exactly as defined, flags gaps inline during work, and proposes structured updates for human review at session end.

## Key Features

- **Living knowledge base** — grows incrementally across sessions, never auto-modified
- **Progressive disclosure** — three-tier system (Core / Working Context / Archive) that scales from a single 60-line file to a multi-file domain model
- **Human-in-the-loop governance** — AI proposes updates, humans review and apply
- **Domain boundaries** — explicit scope definition prevents AI overbuilding
- **State models** — named enumerations and valid state transitions as first-class citizens
- **Stakeholder map** — named people, their relationship to the system, concerns, and involvement timing to prevent adoption failure
- **Versioning** — MAJOR.MINOR version header with change summary, auto-incremented on each approved update
- **Template-driven** — blank DOMAIN.md template with 14 sections and tier annotations, ready to initialize
- **Anti-pattern awareness** — documented failure modes for both AI and human participants

## DOMAIN.md Sections

| Section | Tier | Purpose |
|---|---|---|
| Project Overview | 1 | What the app does, who uses it, goals |
| Domain Boundaries | 1 | What's in scope, supporting, and excluded |
| Terminology Glossary | 1 | Internal jargon mapped to plain definitions |
| Entity Registry | 1/2 | Business objects with attributes and descriptions |
| State Models | 1 | Valid statuses, types, and state transitions |
| Relationship Map | 2 | How entities connect to each other |
| Flow Catalog | 2 | Named business processes with step-by-step flows |
| Business Rules | 1 | Constraints, validations, edge cases |
| Integration Points | 2 | External systems, APIs, data sources |
| User Roles | 1 | Who uses the system and what they can do |
| Stakeholder Map | 1 | Named people, concerns, and when to involve them |
| Open Questions | 1 | Unresolved ambiguities |
| Detail Files | 1 | Index of split files (when >200 lines) |
| Changelog | 3 | Session-by-session learning history |

## Installation

```bash
npx skills add customware-ai/skills --skill domain-context
```

## File Structure

```
domain-context/
├── SKILL.md                         ← Main skill instructions (v1.5)
├── assets/
│   └── templates/
│       └── DOMAIN.md                ← Blank template with 14 sections
└── references/
    ├── seed-questions.md            ← Questions to bootstrap a new domain
    ├── entity-template.md           ← Template for individual entity files
    └── anti-patterns.md             ← Common mistakes to avoid
```

## Versioning

DOMAIN.md includes a version header that the AI auto-increments on each approved update:

```markdown
> **Version:** 1.5
> **Last updated:** 2026-04-06 (Session 30)
> **Changes:** +Commission Report entity, +BR-013–015, updated Quote-to-Close flow
```

MINOR increments on every approved update. MAJOR increments on fundamental scope changes.

## License

MIT

