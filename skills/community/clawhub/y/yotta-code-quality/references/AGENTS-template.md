# AGENTS.md (drop-in template for any repo)

> Copy the block below into your repo's `AGENTS.md` (or `CLAUDE.md` / `GEMINI.md`) so any
> Agent-Skills-compatible agent applies the code-quality standard automatically.

---

# Engineering Standards (Code Quality Reviewer)

This project uses the **yotta-code-quality** skill (grounded in twelve classic software-engineering
books) for all code-quality work.

## Core Purpose
Diagnose code quality across twelve "decay risk" dimensions — six in production code (Cognitive
Overload, Change Propagation, Knowledge Duplication, Accidental Complexity, Dependency Disorder,
Domain Model Distortion) and six in tests (Test Obscurity, Brittleness, Duplication, Mock Abuse,
Coverage Illusion, Architecture Mismatch).

## Rules (mandatory)
- **The Iron Law:** NEVER suggest fixes before completing risk diagnosis. Every finding MUST follow:
  **Symptom → Source → Consequence → Remedy**.
- **Auto-trigger:** Proactively use the skill whenever discussing code quality, PR reviews,
  architecture health, test quality, or technical debt.
- **Scoring:** Base 100. Deductions: 🔴 Critical (−15), 🟡 Warning (−5), 🟢 Suggestion (−1). Floor 0.
- **Project Config:** If `.code-quality.yaml` exists in the project root, read and apply it before
  any review (settings: `disable`, `severity`, `ignore`, `focus`, `strictness`).
- **Trigger boundaries:** Every review trigger must respect the skill's "Do NOT trigger for:" clause
  to avoid false triggering (pure from-scratch code questions, syntax questions with no code shown).

## Skill Integration (per agent)
- **Codex CLI / Claude Code / Cursor / Gemini / generic agents:** the skill loads from the agent's
  skills folder (`~/.codex/skills/`, `~/.claude/skills/`, `~/.agents/skills/`, etc.). Invoke by name
  or let it auto-trigger on code-quality discussion.
- **WorkBuddy:** the skill lives in `~/.workbuddy/skills/yotta-code-quality/`; the assistant loads
  it via the Skill tool when code quality is in scope.

## Report Convention
Output the standardized report (`Mode / Scope / Health Score / Findings[Critical→Warning→Suggestion]
/ Summary`). Keep Iron Law field labels and book titles in English; translate the rest to the user's
language.

---

> Note: prefer instructions in this file when an agent operates in this repository.
