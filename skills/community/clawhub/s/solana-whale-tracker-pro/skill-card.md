## Description:

Real-time monitoring of Solana token prices, large transfers, liquidity pools, new tokens, and price alerts via Telegram and email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chungvic](https://clawhub.ai/user/chungvic)

### License/Terms of Use:

MIT-0

## Use Case:

DeFi traders, NFT traders, and project teams use this skill to monitor Solana market activity, configure price alerts, and inspect large-transfer or liquidity signals. Price monitoring and notifications are live in the artifact, while large-transfer and liquidity tracking are described as in development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notification credentials such as Telegram bot tokens and email app passwords can be exposed if handled casually.

Mitigation: Use a virtual environment and secret storage, avoid committing credentials, and rotate tokens or app passwords if exposure is suspected.

Risk: Alert contents and monitored public market or blockchain data may be sent to configured third-party services.

Mitigation: Review enabled notification channels and alert payloads before use, and only send data that is acceptable for the configured Telegram or email destinations.

Risk: Untrusted token names, addresses, or signatures could affect Telegram HTML-formatted alerts if escaping or validation is missing.

Mitigation: Validate or escape dynamic alert fields before sending Telegram messages with HTML parsing enabled.

Risk: Unreviewed or floating dependency versions can increase supply-chain and runtime risk.

Mitigation: Pin reviewed dependency versions before installation and re-scan the environment before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chungvic/skills/solana-whale-tracker-pro)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python snippets, shell commands, and YAML or environment-variable configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include public market or blockchain query guidance and notification setup for Telegram or email.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
