## Description:

Maximize your Claude Code subscription value with smart usage monitoring and burn rate optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rusel95](https://clawhub.ai/user/rusel95)

### License/Terms of Use:

MIT

## Use Case:

External Claude Code subscribers use this skill to monitor 5-hour session and 7-day weekly quota utilization, receive usage alerts, and adjust daily burn rate against their subscription plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to handle Claude OAuth access and refresh tokens and stores them in plaintext inside the skill directory.

Mitigation: Review the credential flow before installation, keep token files permissioned to owner read/write only, ensure tokens are ignored by source control, and rotate tokens if they were committed, logged, or shared.

Risk: The optional token health check may read or rewrite Claude CLI credentials.

Mitigation: Enable the cron or auto-refresh workflow only after reviewing that behavior and confirming it matches the user's credential-management expectations.

Risk: Usage checks send OAuth bearer tokens to the Anthropic usage endpoint.

Mitigation: Avoid logging command output that could expose tokens, use the built-in cache to reduce request frequency, and run only from trusted local environments.

## Reference(s):

- [Token Usage Optimizer on ClawHub](https://clawhub.ai/rusel95/skills/token-usage-optimizer)
- [Anthropic OAuth Usage API](references/api-endpoint.md)
- [Token Extraction Guide](references/token-extraction.md)
- [Claude Code Subscription Plans](references/plans.md)
- [Claude Code Pricing](https://claude.ai/pricing)
- [Anthropic API Docs](https://docs.anthropic.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text reports, KEY=VALUE status lines, and Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses cached usage data by default and may emit one-time threshold or token-expiry alerts.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
