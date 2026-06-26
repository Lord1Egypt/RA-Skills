# Vibe Coding Blueprint

A document-driven AI programming methodology. AI is a "highly capable but occasionally careless new hire." Your role is **Architect and Decision Maker** — not overseer.

## What It Does

The problem with vibe coding: AI produces code that works once but becomes unmaintainable over time. This methodology solves that through **documents as memory** — a self-referential system where every code change triggers documentation updates. AI can resume from any state without losing context.

## The Core Loop

1. **Plan first** — AI outputs the technical plan before writing any code
2. **Small steps** — Break features into independently verifiable tasks
3. **Document everything** — Header comments, folder docs, and architecture docs sync automatically
4. **Human in command** — When the same bug resists 2–3 fixes, stop and diagnose the root cause yourself

## Three-Layer Documentation System

```
docs/
├── ARCHITECTURE.md       # System overview
├── PROJECT_STRUCTURE.md  # Quick navigation
└── [folder]/FOLDER.md   # Per-folder: ≤3 lines
```

Every code file starts with 3 header lines:
```typescript
// input:  [dependencies]
// output: [what it provides]
// pos:    [its role in the system]
```

## How to Trigger

- *"Start a new project with vibe coding blueprint"*
- *"Add [feature] to [module]"*
- *"My code has a bug I can't fix after 3 attempts"*
- *"Refactor messy code"*

## Efficiency Target

< 5% of writing is done by you (wording tweaks, root cause diagnosis, boundary decisions). AI handles the rest.
