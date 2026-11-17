## Description:

Solana Market helps agents query real-time prices and market overviews for selected Solana ecosystem tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liji3597](https://clawhub.ai/user/liji3597)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to have an agent answer current price and market-overview questions for supported Solana ecosystem tokens while avoiding price predictions and trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an undocumented wallet-monitoring script that can repeatedly query a wallet address through Helius when HELIUS_API_KEY is configured.

Mitigation: Review the package before installing, remove or disable wallet monitoring unless it is explicitly needed, and only configure HELIUS_API_KEY when wallet monitoring is approved.

Risk: Market and token-risk outputs depend on external price and risk data and may be unavailable, delayed, or unsuitable for trading decisions.

Mitigation: Use the outputs as informational context, preserve the documented guardrails against predictions and trading advice, and verify important prices or risk reports against authoritative sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liji3597/skills/solana-market)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or plain text with command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese by default and English with --lang en; requires node and may require HELIUS_API_KEY for wallet monitoring.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
