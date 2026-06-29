# Interview Flow

Use English unless the user explicitly asks for a different language. Ask plain-language questions and avoid forcing agent or skill terminology on non-technical users.

Before asking route questions, determine the execution path. If omitted, default to `direct-skill` and ask guided intake items directly through the Skill2Team skill. Only if the user explicitly chooses `meta-team-first`, run the meta-team execution preflight from `references/meta-team-execution.md`; in that mode, decompose the intake itself by role. If real subagents are unavailable in Codex `meta-team-first`, stop with `meta-team-first blocked`, give the reason, and do not proceed under the `meta-team-first` label.

# Interview Flow Prompt

Start with concrete tasks, not architecture terminology.

1. Ask for 2-3 representative tasks.
2. Ask what currently exists.
3. Ask what current workflow does well.
4. Ask what often fails.
5. Ask risk/data/review questions.
6. Ask whether the user wants `direct-skill` or `meta-team-first` only if they did not already choose; state that `direct-skill` is default.
7. Ask for the human-interaction execution mode before source conversion starts: preserve source human-interaction steps, selectively preserve/convert them, or fully automate with audit. Default to preserving source human-interaction steps.
8. If deployable agents are needed, confirm Codex, remind that model execution defaults to OpenAI Codex rather than direct API calls, and collect any optional Codex project-root context only for Codex package-end guidance.
9. Summarize architecture drivers.
