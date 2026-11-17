## Description:

Stock Select helps agents screen stocks with natural-language criteria, retrieve market and Level 2 capital-flow data, monitor call-auction activity, manage broker accounts, and assist with authenticated trading workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanghl-cn](https://clawhub.ai/user/wanghl-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query stock quotes, run natural-language stock screens, inspect Level 2 market data, and prepare account or order API calls. Trading workflows require authenticated access and should be gated by explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real financial orders without clearly requiring final user confirmation.

Mitigation: Require a separate explicit confirmation before submitting any order, including account, symbol, side, quantity, price type, and price where applicable.

Risk: Authentication data, SMS codes, access tokens, refresh tokens, or account details could be exposed in ordinary chat or shell history.

Mitigation: Avoid pasting real secrets into chat or plain shell commands; verify the API endpoint before login and keep tokens session-scoped.

## Reference(s):

- [Stock Select on ClawHub](https://clawhub.ai/wanghl-cn/skills/stock-select)
- [Publisher profile](https://clawhub.ai/user/wanghl-cn)
- [Stockbot homepage](https://stockbot.me)
- [Stockbot API endpoint](https://api.stockbot.me)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown guidance with JSON request examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated stock-account and trading API calls.]

## Skill Version(s):

2.0.2 (source: release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
