## Description:

Reports AI token usage and estimated costs for OpenClaw sessions, including current sessions, cron jobs, subagents, and date-based summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators use this skill to answer cost and token-usage questions for today, previous periods, or individual sessions, with estimates by session type and model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sources a local .context file, so a modified or untrusted context file could affect reported pricing or behavior.

Mitigation: Use the skill only where the external .context file is trusted, access-controlled, and protected from modification.

Risk: The skill may append usage aggregates to token-history.jsonl while producing reports.

Mitigation: Prefer read-only reporting by default and require explicit confirmation before persisting cost history.

Risk: Provider-specific cost extraction may be incomplete for Google Gemini or OpenAI GPT sessions.

Mitigation: Use provider billing dashboards when local usage records do not include authoritative cost fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/usage-costs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cost estimates depend on local OpenClaw session, cron, and token-history data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
