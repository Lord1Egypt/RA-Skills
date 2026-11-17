## Description:

Token Cockpit helps agents analyze local OpenClaw and LLM usage logs to estimate token spend, project monthly costs, check budgets, and identify routing changes that may reduce costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris](https://clawhub.ai/user/chris)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to understand local OpenClaw or LLM usage costs, monitor budget status, and evaluate model-routing changes that may lower spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local usage logs, which may contain sensitive operational metadata.

Mitigation: Review the selected log path before running analysis and pass --logs explicitly in sensitive environments.

Risk: Built-in model prices may be outdated, and unknown models are counted as zero cost.

Mitigation: Supply current pricing with --pricing before relying on exact dollar amounts or budget alerts.

Risk: Routing and simulation savings assume cheaper models use similar token counts and meet quality needs.

Mitigation: Validate task quality before changing model defaults based on estimated savings.

## Reference(s):

- [Token Cockpit on ClawHub](https://clawhub.ai/chris/skills/token-cockpit)
- [Publisher profile: chris](https://clawhub.ai/user/chris)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown reports or JSON command output, accompanied by concise agent guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cost figures are estimates unless current pricing is supplied with --pricing.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
