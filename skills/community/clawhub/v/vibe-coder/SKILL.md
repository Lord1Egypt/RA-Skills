---
name: vibe-coder
description: "Expert vibe-coding workflow for building apps, tools, and scripts from scratch based on plain-English descriptions. Use when a user asks to build something — an app, tool, CLI, script, web app, automation, or any software project — described in natural language. Handles the full build lifecycle: understanding the brief, planning phases, building incrementally, error recovery, iteration, and final delivery. Never silently gets stuck."
---

# Vibe-Coder

Build anything from a plain-English description. Six phases. No silent failures.

## Phase 1 — Understand the Brief

Before writing a single line of code:
- Restate the core idea back to the user in 2-3 sentences
- Confirm: core features, tech stack (propose one if not specified), UI/UX expectations
- Ask any clarifying questions needed — but batch them, don't ask one at a time
- Do not proceed to Phase 2 until the user confirms understanding

**Questions to consider:**
- What platform? (web, CLI, desktop, mobile, API)
- Any existing codebase to integrate with, or greenfield?
- Key constraints? (language, dependencies, hosting, runtime)
- Who's the user? (just them, a team, public)

## Phase 2 — Plan the Build

Break into exactly 5 phases:
1. **Structure** — project scaffold, file layout, dependencies
2. **Functionality** — core logic, data flow, business rules
3. **UI Polish** — interface, UX, error states, edge cases
4. **Testing** — happy path, edge cases, error scenarios
5. **Final Review** — cleanup, docs, delivery packaging

Present the plan with bullet points under each phase. Get explicit approval before starting Phase 3.

## Phase 3 — Build Phase by Phase

For each phase:
1. **Announce what you're about to build** before writing code
2. Write clean, commented code
3. Explain each major section in plain English (1-2 sentences max per section)
4. After each phase, ask: "Does this look right? Anything to change before I move on?"
5. Incorporate feedback before proceeding

Never skip a phase. Never start the next phase without confirmation.

## Phase 4 — Error Handling

If you hit a bug or blocker:
- Describe the problem in plain English (no jargon dumps)
- Propose exactly **two fixes** with trade-offs
- Ask which to try
- Never get stuck silently — if you don't know the fix, say so and propose a research step

## Phase 5 — Iterate

After each phase, active feedback loop:
- "Here's what was built. Here's what's next."
- Incorporate changes immediately — don't defer
- If scope expands mid-build, flag it explicitly: "This adds scope. Want to include it or keep to the original plan?"

## Phase 6 — Final Delivery

Deliver:
1. **Working product** — all files, runnable as described
2. **Build summary** — what was built, key decisions made, anything deferred
3. **Usage instructions** — how to run it, configure it, and extend it

Format the summary as:
```
## What Was Built
[2-3 sentences]

## Key Decisions
- [decision + rationale]

## How to Run
[commands]

## Known Limitations / Next Steps
- [if any]
```

## General Rules

- Plain English first, code second — always explain before or alongside
- Never present code without context
- Short explanations beat long ones — if a section needs a paragraph, the code is probably too complex
- If uncertain about user intent, ask — don't assume and build the wrong thing
- Prefer working simple over impressive broken
