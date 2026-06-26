# Implemented Features

Updated: 2026-04-15

## Core Journal System

- local SQLite-backed ledger and runtime storage
- plans, trades, reviews, reports, drafts, and session threads
- JSON and Markdown artifact generation
- Obsidian-style vault export

## Conversation and Session Logic

- `intake parse` / `intake apply`
- draft state machine with start, reply, show, apply, list, cancel
- `session turn`, `session state`, `session reset`
- same-day and same-symbol short-term session reuse
- statement-import continuation through session state

## Trade Memory Layer

- `memory_cells`, `memory_scenes`, `memory_hyperedges`, `memory_skill_cards`
- SQLite FTS5-backed coarse recall
- structured memory filtering by symbol / stage / strategy / tags
- scene expansion and linked skill-card retrieval
- manual memory revision for tags / market stage / quality score / correction note
- manual skill-card revision for trigger conditions and `do_not_use_when` guards
- memory snapshots written to `_runtime/memory/`
- `memory rebuild`, `memory query`, `memory skillize`, `memory revise`, `memory skill-edit`

## Planning, Trading, Review, and Analytics

- plan creation, listing, status update, and enrichment
- trade logging, closing, and enrichment
- statement import with fact-first alignment
- post-trade review cycle
- self-evolution report and reminder
- style portrait generation
- behavior health reporting

## Evolution and Skill Solidification

- trajectory self-evolution still uses contextual-bandit-style reranking
- long-term memory now acts as the recall layer before bandit prioritization
- stable high-value paths can be solidified into skill cards
- skill cards can be marked as community-shareable when evidence is sufficient

## Documentation and Repo Packaging

- `TRADE_MEMORY_ARCHITECTURE.md` for the concise design note
- `TRADE_MEMORY_SYSTEM_PAPER.md` for the paper-style architecture write-up
- `OPENCLAW_DEMO_WORKFLOW.md` for classroom-ready OpenClaw interaction demos
- `MEMORY_RETRIEVAL_BENCHMARK.md` plus `run_memory_benchmark.py` for retrieval evaluation
- updated public/private sync policy in `README.md` and `README.zh-CN.md`
- legacy news bootstrap tables removed from the active schema bootstrap

## Verified Locally

- `python -m compileall finance_journal_core finance-journal-orchestrator\scripts tests`
- `python -m unittest discover -s tests -v`
