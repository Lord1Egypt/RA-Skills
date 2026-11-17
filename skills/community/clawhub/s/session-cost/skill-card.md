## Description:

Analyze OpenClaw session logs to report token usage, costs, and performance metrics grouped by agent and model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khaney64](https://clawhub.ai/user/khaney64)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect local OpenClaw session logs, estimate API spending, and summarize token, cache, cost, duration, provider, model, and agent usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw session log files, which may include usage metadata and session identifiers.

Mitigation: Run it only on logs you are authorized to inspect, and use --agent, --path, --provider, or --offset to narrow scans when appropriate.

Risk: Cost and token summaries depend on usage fields recorded in local session logs and may be incomplete when a model or provider does not report tokens.

Mitigation: Treat summaries as operational estimates and inspect detail or JSON output when values appear incomplete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/khaney64/skills/session-cost)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Analysis]

**Output Format:** [Plain text summaries, tabular text details, JSON, or markdown-friendly chat summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports agent, provider, time-window, path, detail, table, JSON, and chat-summary filters.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
