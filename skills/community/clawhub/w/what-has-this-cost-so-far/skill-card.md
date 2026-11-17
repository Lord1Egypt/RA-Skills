## Description:

Reports OpenClaw session token totals, provider-reported cost, tool call counts, and the most expensive session so an agent can decide whether another attempt is worth the spend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to summarize OpenClaw transcript usage, cost, tool calls, and the highest-cost session before deciding whether to keep spending effort on a task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw session transcripts, which may contain sensitive conversation context.

Mitigation: Install and run it only when transcript access is acceptable, and avoid sharing detailed output beyond the cost and token totals needed for the decision.

Risk: Provider costs may be absent when a provider or local model reports token usage without cost data.

Mitigation: Treat missing cost as unavailable rather than zero spend, and use the token and tool-call totals as supporting signals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/what-has-this-cost-so-far)
- [Project homepage](https://github.com/aeneassoft/clawphylax)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or terminal text with optional JSON from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an action recommendation, aggregate sessions, tokens, cost when reported by the provider, tool calls, cost per tool call, and the most expensive session.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
