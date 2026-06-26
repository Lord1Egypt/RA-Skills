---
name: Quizlet
slug: quizlet
version: 1.0.0
homepage: https://clawic.com/skills/quizlet
description: Build high-yield Quizlet study sets, tune Learn and Test sessions, and improve weak cards with spaced repetition diagnostics.
changelog: Initial release with Quizlet set design, study mode tuning, and weak-card diagnostics workflows.
metadata: {"clawdbot":{"emoji":"Q","requires":{"bins":[],"config":["~/quizlet/"]},"os":["darwin","linux","win32"],"configPaths":["~/quizlet/"]}}
---

## Setup

On first use, read `setup.md` for activation boundaries and context capture priorities.

## When to Use

Use this skill when the user is studying with Quizlet and needs better set design, mode selection, session planning, or recovery from weak retention.

## Architecture

Memory lives in `~/quizlet/`. See `memory-template.md` for structure and status fields.

```text
~/quizlet/
|-- memory.md           # Status, activation boundaries, and learning context
|-- set-playbooks.md    # Reusable set patterns by subject and goal
|-- weak-cards.md       # Rewritten cards and recurring failure patterns
`-- session-plans.md    # Time-boxed study plans and exam countdown strategy
```

## Quick Reference

Use the smallest relevant file for faster and more accurate recommendations.

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |
| Building high-yield sets | `set-design.md` |
| Choosing study modes | `study-modes.md` |
| Diagnosing poor retention | `diagnostics.md` |
| Import and cleanup workflows | `imports.md` |

## Core Rules

### 1. Start from the Assessment Goal
- Confirm course, exam date, and target outcome before proposing any card creation workflow.
- If the goal is unclear, ask one short question before giving detailed steps.

### 2. Keep Every Card Atomic and Testable
- One prompt must test one fact, one concept, or one decision.
- Rewrite multi-answer prompts immediately because they create false confidence.

### 3. Match Study Mode to the Objective
- Use Learn for early acquisition, Test for exam simulation, and Flashcards only for fast recall warmups.
- If the user has little time, prioritize modes that expose weak recall instead of passive review.

### 4. Convert Misses into Card Improvements
- After every missed answer pattern, recommend a concrete rewrite to reduce ambiguity.
- Track recurring misses in `~/quizlet/weak-cards.md` to prevent repeating the same mistakes.

### 5. Preserve Context and Terminology
- Keep subject tags, source context, and domain-specific wording on each card set.
- Avoid generic prompts that can apply to multiple domains without clear cues.

### 6. Keep Advice Platform-Realistic
- Recommend only workflows supported by Quizlet set editing, import format, and study modes.
- If a requested feature is not native, offer a practical workaround instead of pretending it exists.

### 7. Protect Data Boundaries
- Store only study preferences and workflow notes in `~/quizlet/`.
- Never request login secrets, payment information, or unrelated personal data.

## Common Traps

- Writing definition lists instead of atomic prompts -> lower retention and weak transfer under exam pressure.
- Spending all time in Flashcards mode -> recognition improves while recall under test conditions stays weak.
- Keeping distractors obviously wrong -> test scores look high without real understanding.
- Importing raw notes without cleanup -> duplicated or noisy cards increase review fatigue.
- Ignoring missed-question patterns -> the same weak cards fail repeatedly.
- Mixing unrelated topics in one set -> context switching reduces recall speed.

## Data Storage

- Local notes only in `~/quizlet/` for memory, weak-card logs, and reusable set patterns.
- Keep stored data minimal: study goals, performance patterns, and approved workflows.
- Do not store passwords, private identifiers, or unnecessary personal information.

## Security & Privacy

Data that leaves your machine:
- None by default. This skill provides workflow guidance and local note structure only.

Data that stays local:
- Study context and planning notes in `~/quizlet/`.

This skill does NOT:
- Log in to Quizlet automatically.
- Scrape private user data from browser sessions.
- Make undeclared network requests.
- Store files outside `~/quizlet/` for memory.
- Modify its own skill definition files.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `anki` - Spaced repetition card design and retention tuning for Anki workflows.
- `flashcards` - Core flashcard writing rules and question quality patterns.
- `quiz` - Quiz construction and scoring logic for assessment scenarios.
- `study` - Structured study planning and session management workflows.
- `exam` - Exam-specific preparation, prioritization, and review strategy.

## Feedback

- If useful: `clawhub star quizlet`
- Stay updated: `clawhub sync`
