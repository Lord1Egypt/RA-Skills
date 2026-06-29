# Brief-to-Team Prompt

Given a skill, team, or workflow brief, produce a draft before asking many questions.

Before producing the draft, determine the execution path. If the user did not choose one, use `direct-skill` by default and do not run meta-team preflight. If the user explicitly chose `meta-team-first`, run the meta-team execution preflight from `references/meta-team-execution.md`; real Codex subagent fan-out is mandatory. If it cannot be confirmed, stop with `meta-team-first blocked`, give the reason, and do not proceed under the `meta-team-first` label.

Use `Route: brief-to-team` and default to `Delivery: design` unless the user explicitly asks for packaging or registration.

Output:

1. Execution-path log: route, delivery, selected execution path, source status, target runtime, and synthesis owner. Include meta-team fan-out status only for `meta-team-first`.
2. Detected responsibilities.
3. Likely overloaded areas.
4. Draft agent team.
5. Skill allocation assumptions.
6. Original workflow sketch with concrete nodes, edges, stage mappings, stage-internal deliverables, required user input nodes, human intervention points, gates, checkpoints, and terminal boundaries when inferable.
7. Workflow migration map draft, including a workflow-preservation gap list instead of silently filling unknowns.
8. Recommended orchestration.
9. Source material completeness check: what source skill/team/workflow was provided and what is missing.
10. Runtime target confirmation when deployable artifacts are requested: Codex only. Remind that actual model execution defaults to OpenAI Codex, not direct model API calls. Package output should include `design-output.zip`, an entry-agent startup welcome page, and Codex-only post-package prompt templates instead of any delivery beyond package.
11. Human-interaction execution mode question before conversion: preserve source human-interaction steps, selectively preserve/convert them, or fully automate with audit. Default to preserving source human-interaction steps.
12. Human intervention retention question: which detected waits, approvals, selection points, user input nodes, or terminal boundaries should be preserved, converted to reviewer gates, auto-advanced with audit, or removed as redundant.
13. High-impact follow-up questions.
