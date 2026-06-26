# Report Narration Prompt

Use this after the audit report is generated, when replying to the user in chat.

- Match the user's language when it is clearly supported; otherwise use English.
- Start with the practical answer: what should stay, what needs evidence, and what needs review.
- Do not paste raw JSON unless the user explicitly asked for raw data or machine-readable output.
- Mention the Markdown report path when useful; mention the JSON path only if the user asked for JSON or automation output.
- Keep action codes, risk flags, env vars, skill names, file paths, and CLI flags unchanged.
- Do not repeat every table row. Summarize by decision group and name only the highest-impact skills.
- Say clearly that `delete`, `merge-delete`, and `quarantine-review` are manual-review recommendations, not automatic actions.
- If the report is `structure-only`, say that cleanup decisions need usage evidence before deletion.

Suggested shape:

1. One-sentence overall result.
2. Keep: strongest skills and why.
3. Watch or review: missing evidence, missing env, or risk signals.
4. Removal candidates: what to inspect before deleting.
5. Next step: collect usage, run ablation, configure env, or review risky files.
