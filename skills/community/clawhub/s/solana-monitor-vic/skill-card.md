## Description:

Monitors Solana ecosystem data including token prices, Telegram and email alerts, large-transfer tracking, liquidity pool changes, and new token discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chungvic](https://clawhub.ai/user/chungvic)

### License/Terms of Use:

MIT-0

## Use Case:

External users, DeFi and NFT traders, and project teams use this skill to monitor Solana token prices, whale activity, liquidity changes, and notification alerts for market operations. It helps configure and run Python-based monitoring workflows that read public market and chain data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to configure Telegram bot tokens and email-sending credentials.

Mitigation: Use dedicated low-privilege bot and email accounts, keep secrets out of source control, restrict config file permissions, and rotate exposed credentials.

Risk: Security evidence reports weak disclosure and unsafe error logging around notification credentials.

Mitigation: Avoid logging raw request exceptions or credential-bearing values, and review notification setup before deployment.

Risk: The skill depends on live third-party APIs and public Solana RPC endpoints for price and transaction data.

Mitigation: Review dependency versions, handle API failures and rate limits, and validate monitoring results before acting on alerts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chungvic/skills/solana-monitor-vic)
- [Publisher profile](https://clawhub.ai/user/chungvic)
- [Project repository](https://github.com/vic-ai-company/solana-monitor)
- [Project issues](https://github.com/vic-ai-company/solana-monitor/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce configuration guidance for Telegram bot tokens, SMTP credentials, price alerts, and polling intervals.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
