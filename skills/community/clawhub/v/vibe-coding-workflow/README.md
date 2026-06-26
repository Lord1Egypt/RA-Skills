# vibe-coding-workflow

A structured 5-phase workflow skill for AI-assisted software development. Guides you from a vague idea all the way to a working, maintainable product — with clear checkpoints at every stage.

## What it does

Instead of jumping straight into code, this skill enforces a disciplined collaboration pattern between you and the AI:

- **You make decisions.** The AI executes and documents.
- **Each phase produces an artifact** (requirements doc, architecture doc, debug summary) you can save and reuse.
- **No phase is skipped silently.** The AI checks a completion checklist before moving forward.

## The 5 Phases

| Phase | Goal | Key output |
|---|---|---|
| 1 · Requirements | Turn a vague idea into a structured spec | Requirements doc (Markdown) |
| 2 · Architecture | Define project structure and module contracts | Directory tree + Mermaid data flow diagram |
| 3 · Code Generation | Implement one module at a time | Working code, consistent with architecture |
| 4 · Debugging | Diagnose and fix problems step by step | One-line problem/cause/fix summary |
| 5 · Iteration | Re-enter the right phase for new features, optimizations, or refactors | Updated requirements or architecture doc |

## How to trigger it

Just describe what you want to build, or use any of these phrases:

- *"Help me build a ___ step by step"*
- *"Let's start from Phase 1"*
- *"Follow the vibe coding workflow"*
- *"I have a bug I can't fix"* → enters Phase 4
- *"My code works but it's a mess"* → enters Phase 2 (refactor)

## Why use it

Without structure, AI-assisted coding tends to produce code that works once but is hard to debug, extend, or hand off. This workflow trades a little upfront friction for a much smoother overall arc — especially useful for projects longer than a single session.
