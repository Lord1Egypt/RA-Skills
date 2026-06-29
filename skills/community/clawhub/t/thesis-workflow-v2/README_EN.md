# MBA / Academic Thesis Multi-Agent Workflow (v2 Framework)

A complete multi-agent workflow for MBA and academic thesis writing, supporting outline-anchored writing, node-by-node generation, deep review, integration, and Word export.

Suitable for the full lifecycle from thesis proposal to final graduation thesis.

---

## ⚠️ Dual Version Lines

This repository contains **two independent version lines**, published separately:

| Version | ClawHub Slug | Latest | Status |
|---------|-------------|--------|--------|
| **v1.x** (stable) | `thesis-workflow` | **v1.7.3** | Maintenance only, compatibility fixes |
| **v2.x** (new framework) | `thesis-workflow-v2` | **v2.0.12-beta** | ⚠️ Beta, outline-anchored + 9 HIL |

### Selection Guide

- **Production / v1 users** → `thesis-workflow` (v1.7.3, stable)
- **New framework / outline-anchored / 9 HIL** → `thesis-workflow-v2` (v2.0.12-beta, testing)
- **Multiple theses** → Both can coexist

## Core Features (v2 Framework)

- **Outline-Anchored Writing**: Generate content node-by-node anchored to the outline, with automatic bridge paragraphs between nodes
- **BGE-small-zh Vector Title Matching**: Phase 1.3 proposal attribution accelerated from 30-90s to 2-5s
- **Multi-Tool Parallel Search**: 4 tools (Tavily/arXiv/OpenAlex/web_search) search simultaneously, dedup + sort by relevance
- **Phase 3.5 Academic Deep Review**: P0/P1/P2 graded issue list, auto-fix + re-review loop
- **RuntimeLLM**: Zero hardcoded config, auto-reuse current session model
- **9 HIL Nodes**: Human-in-the-loop checkpoints for key decisions
- **Guardrails**: 10 automated checks (chapter completeness, citations, word count, table format)
- **Loop Architecture**: Orchestrator Loop / Self-Check Loop / Review Loop / Verification Loop
- **Phase 5 Word Output**: md2docx_strict.py with proper formatting (three-line tables, fonts, spacing)

## Workflow

```
User → Phase 1 (Outline + Proposal) → Phase 2 (Node-by-Node Writing) → Phase 2.5 (Review)
     → Phase 3 (Integration) → Phase 3.5 (Deep Review → P0 fix loop)
     → Phase 4 (Fixes) → Phase 5 (Final Review + Word Export)
```

## v2.0.x Changelog (see [CHANGELOG-v2.md](./CHANGELOG-v2.md))

| Version | Highlights |
|---------|-----------|
| 2.0.12-beta | Phase 3.5 outline-anchored chapter split + P0/P1 fixes (F1-F6) |
| 2.0.11-beta | Removed v1 remnants + clawhubignore |
| 2.0.10-beta | Phase 3.5/4/5 + requirements.txt + lazy BGE |
| 2.0.9-beta | BGE-small-zh vector title matching (Layer 2) |
| 2.0.8-beta | Multi-search engine + RuntimeLLM |
| 2.0.7 | outline_parser fallback (B→A) |
| 2.0.6 | Dual version split + real CLI entry |
| 2.0.5 | B-2 state sync fix |
| 2.0.4 | B-1 HIL deadloop fix |
| 2.0.3 | P2 code cleanup |
| 2.0.2 | P0/P1 fixes |
| 2.0.1 | End-to-end verification |
| 2.0.0 | outline-anchored feature complete |

## Agent Roles

| Agent | Invocation | Responsibility |
|-------|-----------|---------------|
| **Orchestrator** | Current session | Scheduling / Decisions |
| **NodeWriter** | `sessions_spawn` | Node-by-node content generation |
| **Reviewer** | `sessions_spawn` | Phase 3/5 rule-based review |
| **DeepReviewer** | `sessions_spawn` | Phase 3.5 academic deep review |
| **Integrator** | `sessions_spawn` | Phase 4 integration plan |
| **WordAgent** | `exec python3` | md2docx + format verification |

## Tech Stack

- OpenClaw subagent (sessions_spawn)
- BGE-small-zh Chinese embedding model (Layer 2 title matching)
- Tavily / arXiv / OpenAlex multi-tool search
- md2docx_strict.py (Word conversion)
- Guardrails loop_self_check.py (10 automated checks)

## License

MIT-0 — Free to use, modify, and distribute without attribution

## Author

GitHub: [hehe973781230](https://github.com/hehe973781230)

---

*If this skill is helpful to you, please give it a ⭐*