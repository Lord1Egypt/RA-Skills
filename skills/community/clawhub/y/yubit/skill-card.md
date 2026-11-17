## Description:

Use this skill whenever the user wants to do anything on the Yubit exchange: check prices, query wallet/spot/TradFi/earn/perp balances, transfer funds, inspect positions/orders/history/wallet flow records, place or cancel perp orders, manage leverage or mode, set take-profit / stop-loss, or troubleshoot exchange requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yubit-exchange](https://clawhub.ai/user/yubit-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate the Yubit exchange through an agent, including market-data lookup, balance review, diagnostics, wallet transfers, and perpetual futures order management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit real trades, leverage or mode changes, position closes, TP/SL updates, and wallet transfers when authenticated write tools are available.

Mitigation: Require manual confirmation for every write action and verify resulting state before treating an operation as successful.

Risk: Exchange-account credentials may grant broad access if configured with unnecessary permissions.

Mitigation: Use restricted API credentials and avoid withdrawal-like permissions unless they are explicitly required.

Risk: The release installs an unpinned npm runtime package.

Mitigation: Install only after reviewing and trusting the Yubit npm package for this release.

## Reference(s):

- [Yubit Exchange Skill on ClawHub](https://clawhub.ai/yubit-exchange/skills/yubit)
- [Yubit Exchange Skill npm package](https://www.npmjs.com/package/@yubit/exchange-skill)
- [Publisher profile: yubit-exchange](https://clawhub.ai/user/yubit-exchange)

## Skill Output:

**Output Type(s):** [guidance, API calls, shell commands, configuration]

**Output Format:** [Markdown with tool-call guidance and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce exchange actions through MCP tools when the current session exposes authenticated write capabilities.]

## Skill Version(s):

1.0.6 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
