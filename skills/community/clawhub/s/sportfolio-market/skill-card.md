## Description:

Sportfolio.Market helps agents connect to Sportfolio's authenticated MCP endpoint or repo-local CLI for account and portfolio reads, public tools, prompts, resources, and confirmation-gated gameplay action staging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelhmiv](https://clawhub.ai/user/michaelhmiv)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure authenticated Sportfolio access, inspect account and portfolio data, discover public docs and capabilities, and stage gameplay actions that require explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User API tokens can be exposed through shell history, process listings, or logs when pasted into command examples.

Mitigation: Use a user-scoped, revocable Sportfolio token and prefer interactive or otherwise non-logged credential entry when supported.

Risk: Gameplay changes such as trades, LP actions, boosts, and scout assignments can affect the user's account if executed without review.

Mitigation: Stage gameplay actions first and require explicit user confirmation before execution.

## Reference(s):

- [Sportfolio.Market skill page](https://clawhub.ai/michaelhmiv/skills/sportfolio-market)
- [Sportfolio production MCP endpoint](https://www.sportfolio.market/mcp)
- [Sportfolio web app](https://www.sportfolio.market)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented CLI command examples; gameplay mutations are staged and require user confirmation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
