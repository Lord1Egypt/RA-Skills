## Description:

Produces a research-only directional brief on a US stock or index proxy by combining paid market, technical, news, earnings, social, and macro reads into a bullish, bearish, mixed, or insufficient-data assessment.

This skill is for research and development only.

## Publisher:

[selat-dev](https://clawhub.ai/user/selat-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to prepare non-advisory stock direction research briefs before making any independent investment or analysis decision. It is intended for data purchase and synthesis only, not trade execution or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run mutable external wallet-adjacent code before spending real USDC.

Mitigation: Review the upstream code before execution, pin dependencies or commits where possible, and use a dedicated low-balance wallet.

Risk: A run purchases nine paid reads, so unexpected execution can spend real funds.

Mitigation: Dry-run first, show the quoted per-step prices and total, and proceed only after explicit user approval.

Risk: Wallet approvals can authorize unintended spending if the address, network, token, amount, or quote is wrong or stale.

Mitigation: Confirm approval details before signing, keep funding limits conservative, and discard expired approvals.

Risk: The generated market brief could be mistaken for financial advice or a trade signal.

Mitigation: Present the output as research only, include uncertainty and invalidation risks, and decline requests to trade based on the result.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/selat-dev/skills/stock-signal)
- [stock-direction-signals Homepage](https://github.com/SELAT-AI/selat-metamask-skills/tree/main/skills/stock-direction-signals)
- [SELAT MetaMask Skills Repository](https://github.com/SELAT-AI/selat-metamask-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown brief with inline shell commands and sourced plain-language analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes verdict, confidence, catalysts, technical setup, social sentiment, macro context, invalidation risks, and actual spend; raw JSON and merchant URLs are not intended for end-user output.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
