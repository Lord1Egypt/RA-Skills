## Description:

Provides a Node.js Upbit cryptocurrency monitoring bot with technical indicators, GLM-based market analysis, and event logging for price, target-profit, and stop-loss signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smeuse-dev](https://clawhub.ai/user/smeuse-dev)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to set up and review a Korean-language Upbit market monitoring workflow that checks balances, calculates indicators, watches positions, and records trading signals. It is relevant for agent-assisted configuration, code review, and cautious operation of a cryptocurrency monitoring bot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for Upbit exchange credentials and can affect a real trading account.

Mitigation: Use restricted Upbit API keys with no withdrawal permission, prefer a test or low-balance account, and protect environment files containing secrets.

Risk: The security evidence flags an unreviewed external GLM execution path and unsafe shell invocation.

Mitigation: Review and fix the external GLM execution path and shell invocation before installation or operation.

Risk: The security evidence says the skill overstates automated-trading and Telegram behavior.

Mitigation: Do not rely on automated-trading or Telegram behavior unless the missing pieces are supplied, reviewed, and tested.

## Reference(s):

- [Upbit Open API Management](https://upbit.com/mypage/open_api_management)
- [Upbit accounts API endpoint](https://api.upbit.com/v1/accounts)
- [Upbit ticker API endpoint](https://api.upbit.com/v1/ticker?markets=${market})

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JavaScript references, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local JSON state files, Upbit API credentials, GLM analysis, and event logs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
