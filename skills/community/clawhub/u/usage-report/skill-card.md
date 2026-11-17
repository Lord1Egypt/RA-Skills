## Description:

Generates cost and token usage reports from OpenClaw session JSONL logs by reading per-turn usage data for API costs, billing, spending, and daily or session summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[directorvector](https://clawhub.ai/user/directorvector)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to summarize local session usage, token counts, and estimated costs across all sessions or a selected date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw session logs, which may contain usage and cost information.

Mitigation: Use it only on session directories the user intends to summarize, and set OPENCLAW_SESSIONS_DIR when a narrower log location is needed.

Risk: Usage reports may expose operational spending or token-volume information if shared broadly.

Mitigation: Review generated text or JSON before sharing it outside the intended audience.

## Reference(s):

- [Usage Report on ClawHub](https://clawhub.ai/directorvector/skills/usage-report)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text usage report or JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can cover all sessions, today, or a YYYY-MM-DD date filter; totals include turns, cost, output tokens, and cache read/write tokens.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
