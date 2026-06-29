# MBA / Academic Thesis Multi-Agent Workflow

A complete workflow for writing MBA and academic theses using multi-agent collaboration, supporting dual-version drafting, review, integration, and finalization.

Suitable for the full lifecycle from thesis proposal to final graduation thesis.

## Core Features

- **Dual-Version Drafting**: Version H (Hermes deep reasoning) + Version O (OpenClaw format compliance)
- **Phase 3 Review**: 7-dimension strict review (format / outline / content accuracy / plagiarism check / academic standards / literature completeness / writing grammar)
- **Phase 3.5 Academic Deep Review**: 3-round deep review (macro structure → chapter-by-chapter → cross-chapter consistency)
- **Phase 4 Integration**: Review Agent produces integration plan, Orchestrator executes
- **Phase 5 Word Output**: md2docx_strict.py compliant script + optional AI humanization (Phase 5.1) → Word generation (Phase 5.2)

### v1.7 New: Loop Agent Architecture

- **Orchestrator Loop**: Auto-decides next action after each Phase completion
- **Self-Check Guardrails**: 10 automated checks (chapter completeness, citations, word count, table format)
- **Review Loop**: Auto-revisits revisions, passes after 2 consecutive rounds with no new P0 issues
- **Human-in-the-Loop**: 4 mandatory checkpoints for key decisions

### New Files (v1.7)

- `scripts/loop_self_check.py`: Automated Guardrails validation script (10 checks + JSON output)
- `references/checklist.md`: Academic standards checklist
- `references/loop-design.md`: Loop design principles documentation

## Supported Use Cases

- MBA graduation thesis (strategic management / corporate analysis)
- Academic research reports (competitive strategy / industry analysis)
- Formal long-form documents requiring multi-round review and multi-version integration

## Quick Start

### Method 1: Direct Install

```bash
openclaw skills install git:hehe973781230/thesis-workflow
```

### Method 2: ClawHub

```bash
openclaw skills search "mba thesis workflow"
openclaw skills install thesis-workflow
```

ClawHub Page: https://clawhub.ai/hehe973781230/thesis-workflow

## Workflow

```
User → Phase 1 (Confirmation Checklist) → Phase 2 (Dual-Version Drafting) → Phase 2.5 (User Confirmation)
     → Phase 3 (Review) → Phase 3.5 (Academic Deep Review) → Phase 4 (Integration)
     → Phase 5 (Finalization) → [Phase 5.1 (Optional AI Removal)] → Phase 5.2 (Word Generation)
```

## v1.7.6 New

- **Orchestrator Phase 1.3 Integration**: The original Phase 1 only handled directory confirmation and jumped directly to Phase 2, **skipping proposal attribution**. Now Phase 1.3 is mandatory: user uploads proposal → auto-extract content → AI attributes to directory nodes → fine-grained display of each node's `content_hint` + `matched_paragraphs` → user can manually adjust → confirm to enter Phase 2
- **Phase 1.3 State Machine**: Uses enum field `phase1_3_status = "pending|submitted|confirmed|skipped"`, mandatory per decision #1: must be `confirmed` to enter Phase 2
- **5 New Orchestrator Actions**: `phase1_confirm` / `phase1_3_submit` / `phase1_3_update_hint` / `phase1_3_confirm` / `phase1_3_skip`
- **Test Suite Expanded**: 10 additional tests (63 total), covering full state machine + user adjustment + mandatory checks + end-to-end integration

## v1.7.5 New

- **Pre-Writing Info Check (Enhancement 4)**: Before node writing, automatically check 3 information sources (content_hint / user_hints / bridge). If any one is missing (Standard A), returns `action="needs_user_input"` and Orchestrator asks user for 3 options: provide hint / AI self-generate / skip node
- **Complete content_hint Pipeline**: `extract_content_hints()` extracts → `save_content_hints_to_outline()` writes to state → `build_prompt_package()` reads and adds `## 开题报告方向参考` (Proposal Direction Reference) section, enabling LLM to write more accurately based on the proposal
- **Test Suite Expanded**: 8 additional tests (53 total), covering all 3 decision paths + complete end-to-end loop

## v1.7.4 New

- **Cross-Parent Bridge — Chapter Summary Nodes (Enhancement 1)**: Solves the bridge breakage where `2.1` cannot find `1.2`'s `key_conclusion`. Each L1 chapter automatically gets a virtual `__ch{N}_summary__` node appended, which absorbs all L2/L3 key conclusions and synthesizes a 200-300 word summary via LLM, providing coherence for the next chapter's bridge.
- **Three-tier Bridge Priority**: `generate_bridge()` now has P3 fallback chain: P1 previous node → P2 parent node → P3 previous chapter virtual summary
- **LLM Failure Safe Degradation**: `synthesize_chapter_summary()` returns `action="ask_user"` when LLM fails, allowing Orchestrator to collect user-written summaries instead of degrading to error-prone concatenation
- **Test Suite Expanded**: 20 additional tests (45 total), including full end-to-end integration tests

## v2.0.0 🎉

**BREAKING CHANGES**: Upgrading from v1.7.3 is a breaking change.

- **Mandatory Phase 1.3**: Must upload proposal docx OR paste outline text, confirm attribution before Phase 2
- **outline_state Structure Change**: Virtual nodes `__ch{N}_summary__` auto-inserted at the end of each L1 chapter; node fields add `content_hint`
- **orchestrate_state Adds 5 phase1_3_* Fields**: Enum `pending|submitted|confirmed|skipped`
- **generate_bridge 3-tier Fallback Chain**: P1 previous node → P2 parent node → P3 previous chapter virtual summary (new)
- **Pre-Writing Info Check**: `check_info_scarcity()` — any of `content_hint` / `user_hints` / `bridge` missing → returns `action="needs_user_input"` + 3 decision paths

**New Capabilities**:

- **Step 9** — Cross-Parent Bridge: chapter summary nodes + P3 fallback
- **Step 10** — Pre-Writing Info Check: 3 information sources + Standard A + 3 decision paths
- **Step 11** — Orchestrator Phase 1.3 Integration: docx/text parse entry + attribution state machine
- **Step 12** — End-to-end Integration Tests

**Migration Guide**: See `CHANGELOG.md` v2.0.0 section.

Total tests: **72**, all passing ✅. See `CHANGELOG.md` for details.

## v1.7.3 New

- **Orchestrator Auto-Advance**: `scripts/orchestrator.py` decision engine + Review Loop auto-revision
- **Verification Loop**: 6 real Word format checks (fonts/sizes/line spacing/table borders/bold residue/references)
- **Guardrails**: 10 automated checks (chapter completeness/word count/citations/headings/bold/tables/keywords)
- **Unit Tests**: 25 tests covering all scripts

## File Naming Convention

| Version | Description |
|---------|-------------|
| v1.0_*_H_*.md | Hermes version (deep reasoning) |
| v1.0_*_O_*.md | OpenClaw version (format compliance) |
| v2.0_Review*.md | Review report |
| v3.0_Integrated.md | Source markdown for Word conversion |
| v3.0_*_Original.docx | Original Word document |
| v3.0_*_Polished.docx | AI-humanized Word document (optional) |

## Writing Standards

- **Citation Format**: GB/T 7714 Author-Year style (Author, Year)
- **Minimum Word Count**: 35,000 Chinese characters
- **Writing Grammar**: No `**bold**` emphasis in body paragraphs
- **Chinese Font**: SimSun 12pt, line spacing 20pt
- **English Font**: Times New Roman
- **Heading Fonts**: SimHei 16pt (level 1) / 14pt (level 2) / 13pt (level 3)

## Agent Architecture

| Role | Responsibility |
|------|---------------|
| Orchestrator | Task scheduling, workflow progression, node decisions |
| Executor | Version O drafting, format execution |
| H-generator | Version H drafting via Hermes CLI |
| Reviewer | Phase 3/5 rule-based rapid review |
| DeepReviewer | Phase 3.5 academic deep review |
| Integrator | Phase 4 integration plan design |
| WordAgent | md2docx execution |
| HumanizerAgent | Phase 5.1 AI humanization (optional) |

## Key Changes (v1.6)

- **No Email Sending**: Word documents saved to `~/.openclaw/workspace/`, user retrieves files directly
- **No Contact Required**: Phase 1 confirmation streamlined (company mapping + outline only)
- **Optional AI Removal**: Phase 5.1 humanizes AI-written text via humanize-chinese skill before Word output

## Tech Stack

- OpenClaw subagent (sessions_spawn)
- Hermes CLI (deep reasoning)
- academic-thesis-review-skill (academic deep review)
- humanize-chinese skill (AI humanization, optional)
- md2docx_strict.py (Word conversion)

## License

MIT-0 — Free to use, modify, and distribute without attribution

## Author

GitHub: [hehe973781230](https://github.com/hehe973781230)

---

*If this skill is helpful to you, please give it a ⭐*