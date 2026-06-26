# zao-skill · 造技能

**The Meta-Skill Framework — AI creating skills for AI.**

A lightweight, standardized, self-evolving lifecycle framework for building production-grade AI agent skills. Born from three rounds of ruthless de-duplication and systematic upgrades against industry best practices.

[![GitHub release](https://img.shields.io/github/v/release/Sensenkawa/zao-skill?include_prereleases&label=version&style=flat-square)](https://github.com/Sensenkawa/zao-skill/releases)
[![License](https://img.shields.io/github/license/Sensenkawa/zao-skill?style=flat-square)](LICENSE.txt)
![Platform](https://img.shields.io/badge/platform-ClawPro%20%7C%20WorkBuddy%20%7C%20CodeBuddy-blue?style=flat-square)

---

## Why zao-skill?

Most skill frameworks solve one problem: *writing a skill*. They don't solve:
- **AI behavior drift** — Agent acts on frozen context, not current files
- **Unreliable execution** — Steps skipped, references ignored, premature closure
- **Unmaintainable evolution** — No versioning, no traceability, no iteration discipline

zao-skill is the first meta-framework that treats these as first-class design problems.

---

## Core Innovations

### 1. Three-Layer Anti-Drift Architecture

A self-reinforcing grid against AI rationalization bias:

| Layer | Mechanism | Role |
|-------|-----------|------|
| **Principle** | Files Are Truth — `#3 Core Principle` | Declarative: set the rule |
| **Execution** | Pre-Step Rationalization Bias Check | Actionable: must pass before every operation |
| **Feedback** | Gotchas G01–G03 (real failure cases) | Archival: replay error patterns |

This is the industry's first systematic skill-grade behavior correction architecture.

### 2. Lightweight Verification, Not Heavy Testing

Industry convention (Claude Code 2.0, Darwin Skills) favors heavy automated testing — complex prompt design, test loops, I/O fixtures. We reject that.

**Verification over Testing**: dual-lane quality assurance:
- **Static Check** — Automated script (`quick_validate.py`): syntax, format, structure, duplication
- **Interactive Check** — Human-in-the-loop: logic, edge cases, workflow soundness

Result: rigorous quality assurance at <10% of the cost of traditional testing.

### 3. Evolution in Usage (Not in Lab)

Skills improve through real use, not pre-flight testing. The framework includes:
- **Gotcha Archives** — Real failures with repeatable fixes, tiered escalation
- **Success Patterns** — Free-form records of parameter tuning, workflow redesigns, platform adaptations
- **Git-forced versioning** — Every change tracked, every regression traceable

This replaces finite pre-release testing with infinite real-world adaptation.

---

## Workflow Overview

```
Pre-Step Rationalization Bias Check (mandatory before every phase)
                            │
                            ▼
                    ┌──────────────┐
                    │  User Need?  │
                    └──────┬───────┘
                           │
         ┌─────────────────┼──────────────────┐
         ▼                 ▼                  ▼
   Phase 1: Design   Phase 2: Drafting   Phase 3: Validation
   (align + search   (standardized       (dual-lane verify
    + run first       sections +          + gotcha collection)
    + LOOP confirm)   Critical Directives)  │
         │                 │               │
         └─────────────────┴───────────────┘
                           │
                           ▼
                    Phase 4: Packaging
                           │
                           ▼
              Deployment → Evolution in Usage
                          (self-improving)
```

### Phase 1: Design
- **Intent extraction** — Interview, clarify, scope. "Is this even a skill?"
- **Skill search** — Scan local + online (`search-compare.md`) for existing solutions
- **Run first, code later** — Validate workflow in practice before writing SKILL.md
- **LOOP confirmation** — Explicit wait-for-user loop around search decision, prevents AI from skipping the search step
- **Design Context** — All findings append to `workflow-extraction.md` — single source of truth for Phase 2

### Phase 2: Drafting
- **Critical Directives** — All behavioral constraints upfront (AI reads top section most carefully)
- **Files Are Truth** — Every decision reads from disk, not frozen context
- **Imperative tone** — No "consider" or "suggest". Direct commands only.
- **Structured workflows** — TL;DR + ASCII flowcharts for decisions, pseudocode for fixed logic, scripts for mechanical tasks

### Phase 3: Validation
- `quick_validate.py` — Static checks: line count, reference existence, Pre-Step Bias presence, no orphaned refs
- Interactive checklist — 7 evidence-backed quality dimensions
- **Gotcha collection** — New gotchas discovered during validation auto-proposed for Critical Gotchas table
- Loop until: zero FAILs + all evidence filled + user approved

### Phase 4: Packaging
- `package_skill.py` — Auto-excludes `.wip/` directories, validates before build
- Outputs: `<skill-name>.skill` (standard format, ready for submission/audit/deployment)

---

## Key Differentiators

| Dimension | Industry Convention | zao-skill |
|-----------|-------------------|-----------|
| Testing approach | Heavy automated testing | Lightweight dual-lane verification |
| Error handling | Pre-flight only | Real-use evolution with tiered escalation |
| File consistency | Assumes context is fresh | Forces re-read: Files Are Truth |
| Workflow writing | Educational/didactic | Imperative, pseudocode-locked |
| Versioning | Optional | Mandatory Git tracking |
| Learning mechanism | One-time instruction | Self-evolving gotcha + pattern archives |
| Reference naming | Inconsistent | Convention-aligned: verification-gate, workflow-examples |

---

## Quick Start

```bash
# Load the skill (trigger phrase)
"Use zao-skill to create a new skill"
```

**Every skill execution follows the Overarching Process (outer wrapper):**
```
→ Read Overview and Critical Directives
→ Follow Workflows with Pre-Step Rationalization Bias Check
→ After run and before exit:
    1. Evolution Check (record gotchas / success patterns)
    2. Exit Verification (check compliance)
```

**Within the workflow wrapper, the framework walks you through:**
```
User Need?
   ├─ Phase 1: Design     — interview → search → run-first → LOOP confirm
   ├─ Phase 2: Drafting   — Critical Directives + Standard Sections
   ├─ Phase 3: Validation — quick_validate.py + interactive checklist
   └─ Phase 4: Packaging  — package_skill.py (optional)
All paths → Evolution in Usage (self-improve)
```

---

## Meta-Skill Note

zao-skill is itself a skill — and it eats its own dog food:
- ✅ Uses its own design protocol
- ✅ Passes its own validation
- ✅ Records its own gotchas (G01–G03 from real failures)
- ✅ Maintains its own success patterns
- ✅ Version-controlled with semantic tags (v0.1.0 → v0.8.3)
- ✅ Reference files follow naming conventions: verification-gate, workflow-examples

---

## Recognition & References

- **Base inspiration**: Skill Creator V0.1.0 (2026-01-27)
- **Standards aligned**: agentskills.io, Claude Code 2.0 (2026-04)
- **Practitioners referenced**: Matt Pocock, Garry Tan, Addy Osmani, Darwin Skills

---

*"A skill that teaches AI how to build skills — not just write them, but design, verify, evolve, and trust them."*
