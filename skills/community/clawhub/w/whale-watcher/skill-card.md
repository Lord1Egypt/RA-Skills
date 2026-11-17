## Description:

Monitor crypto whale wallets for large transactions, track big moves on Ethereum and BSC, and report significant wallet activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbrc20](https://clawhub.ai/user/alexbrc20)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to inspect crypto wallet activity, identify large transactions, and review wallet movement signals for monitoring or research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses and block explorer API keys may be shared with Etherscan or BscScan during transaction lookups.

Mitigation: Use only wallet addresses and API keys that are approved for those external services, and avoid monitoring targets that should not be disclosed.

Risk: The inspected version overstates real-time Telegram alerts, paid-tier behavior, historical analysis, and broader multi-chain support.

Mitigation: Validate required alerting and chain-support behavior before relying on the skill for operational monitoring.

Risk: Crypto transaction analysis can be incomplete, delayed, or misleading for investment decisions.

Mitigation: Treat outputs as informational signals and confirm transactions independently before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alexbrc20/skills/whale-watcher)
- [Etherscan API](https://api.etherscan.io/api)
- [BscScan API](https://api.bscscan.com/api)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and plain-text transaction summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include wallet addresses, transaction hashes, estimated transaction values, timestamps, and block explorer links.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
