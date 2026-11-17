## Description:

Sur helps agents create and trade tokens on SURGE through an API, including wallet setup, one-time funding, token launch, and pre-DEX or post-DEX trading.

This skill is for research and development only.

## Publisher:

[nkhromovweway](https://clawhub.ai/user/nkhromovweway)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide an agent through SURGE token creation, server-managed wallet setup, one-time funding, and follow-on token trading on supported EVM and Solana routes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a SURGE API key to create server-managed wallets, fund wallets, launch tokens, approve token allowances, and place live trades.

Mitigation: Install only when those capabilities are intended, keep the API key scoped and revocable, and require explicit user confirmation for every wallet, funding, launch, approval, and trade action.

Risk: Token launch and trade actions can be irreversible and can move real funds.

Mitigation: Show the full action summary, chain, wallet, token, amount, and fee details before execution, then proceed only after an explicit user confirmation.

Risk: EVM trades using amountOutMin set to 0 have no slippage protection.

Mitigation: Use quotes when available and set a protective nonzero minimum output for EVM trades instead of accepting amountOutMin of 0.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nkhromovweway/skills/sur-pub)
- [ClawHub publisher profile](https://clawhub.ai/user/nkhromovweway)
- [SURGE app and API key management](https://app.surgedevs.xyz)
- [SURGE DEV API base URL](https://back.surgedevs.xyz)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request examples, JSON payload examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance requires a user-provided SURGE API key and explicit confirmation before irreversible launch or trading actions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata); artifact frontmatter lists 6.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
