# Phase 4: Design

Propose concrete architectural approaches and let the user choose. This phase uses a two-step process: first generate brief approach summaries in parallel, then detail only the chosen one.

## What to Communicate

**Step One — Approach Summaries:** Each subagent returns a brief summary covering the approach name, a one-sentence description, the core mechanism, specific files affected, complexity level (Low/Medium/High), key risks, and how well it fits existing patterns.

**Step Two — Chosen Design:** After the user picks an approach, expand it into a full plan covering:
- Rationale for the choice
- Implementation steps — each with files to create or modify, what to change, and how to verify
- Data model changes (if applicable)
- API changes (if applicable)
- Testing strategy — unit, integration, and manual verification
- Migration or rollout plan (if applicable)

## Context to Preserve

Before finishing, make sure the conversation retains: the chosen approach and why, how many implementation steps, how many files affected, the key trade-off, and the testing strategy summary.

## Steps

1. TaskUpdate — set Phase 4 to `in_progress`.
2. Generate 3 approach summaries in parallel — use the Agent tool to spawn 3 subagents simultaneously. Include all carry-forward context in each prompt. Assign one approach per subagent:
   - **Subagent A:** Minimal Change — extend existing patterns, smallest scope, lowest risk
   - **Subagent B:** Balanced — moderate refactoring, good extensibility, reasonable risk
   - **Subagent C:** Architectural — introduce new abstraction, most extensible, highest complexity

   Each subagent returns only its assigned approach summary.

3. Present all three to the user. Use AskUserQuestion to let the user select one, with trade-offs in the option descriptions.
4. After the user chooses, expand that approach into a full implementation plan.
5. Preserve context for downstream phases.
6. TaskUpdate — set Phase 4 to `completed`.

## Rollback

If detailing the chosen approach reveals ambiguities: set Phase 3 back to `pending`, return with specific new questions.
