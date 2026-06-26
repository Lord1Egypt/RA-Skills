# Roadmap

## Stage 1: Public Skill

Goal: make the repository easy to install, test, and share as a self-contained skill.

Completed:

- `SKILL.md` as the skill entrypoint
- Live search through Desearch
- X OAuth execution for approved actions
- Packaging script for a clean skill bundle
- Public GitHub repo and first release flow

## Stage 2: Better Operators

Goal: improve action quality and reduce failed interactions.

Planned:

- Preflight checks for `reply` and `quote_post` eligibility
- Better opportunity filtering for open conversations
- Stronger drafting for replies and quote posts
- More explicit risk scoring and mission guardrails

## Stage 3: Project Core

Goal: extract the reusable engine from the skill.

Planned:

- `core/` package for scoring, drafting, and execution adapters
- More formal action schema and event model
- Dedicated storage layer for mission, memory, and execution history
- Provider adapters for additional search and execution sources

In progress:

- `core/mission.py` for mission parsing and mission-derived helpers
- `core/scoring.py` for opportunity scoring and action selection
- `core/drafting.py` for action draft generation
- `core/execution.py` for action mapping, preflight, and X execution orchestration
- `core/storage.py` for file-backed mission, memory, action, and execution state
- `core/planning.py` for ranked action plan generation
- `core/feedback.py` for feedback aggregation and cycle recommendations

## Stage 4: Product Surface

Goal: move beyond a CLI-driven skill into an operator product.

Planned:

- Review dashboard for opportunities and actions
- Mission management UI
- Execution history and learning reports
- Scheduled runs and daily or weekly planning loops

## Stage 5: Autonomous Operation

Goal: safe, bounded automation instead of pure review-first workflows.

Planned:

- Approval thresholds by action type and risk
- Automatic post generation for high-confidence opportunities
- Human-in-the-loop escalation for risky topics
- More explicit self-optimization based on outcomes
