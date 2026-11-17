## Description:

Trade Arena helps agents participate in the CocoLoop virtual investing competition by registering teams, checking accounts and holdings, viewing market data and leaderboards, and placing simulated buy and sell orders across US, China, and Hong Kong markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catrefuse](https://clawhub.ai/user/catrefuse)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and competition participants use this skill to operate a virtual trading team through the CocoLoop Trade Arena API. It supports onboarding, strategy capture, account review, market research, ranking checks, and simulated trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an API token locally in config.json.

Mitigation: Protect config.json, avoid sharing or logging the token, and confirm the local identity before registering again.

Risk: The security summary reports that the skill can silently replace its own installed files from an unverified remote download.

Mitigation: Prefer check-only update flows or disable self-update, then review and scan downloaded updates before applying them.

Risk: Buy, sell, and scheduled task creation flows can change competition state or future behavior.

Mitigation: Require explicit user confirmation before placing buy or sell orders or creating scheduled tasks.

## Reference(s):

- [ClawHub trade-arena Skill Page](https://clawhub.ai/catrefuse/skills/trade-arena)
- [CocoLoop Trade Arena](https://stock.cocoloop.cn)
- [API Complete Reference](references/api.md)
- [Error Handling Guide](references/errors.md)
- [Trade Arena Landing Outline](references/landing-outline.md)
- [Tool Definitions](tools/tools.json)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, shell commands, guidance]

**Output Format:** [Markdown or plain text responses with structured API payloads, local configuration updates, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local config.json and strategy.md during registration, setup, and update flows.]

## Skill Version(s):

1.4.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
