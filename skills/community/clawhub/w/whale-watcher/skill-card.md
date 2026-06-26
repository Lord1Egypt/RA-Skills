## Description: <br>
Monitor crypto whale wallets for large transactions, track big moves on Ethereum and BSC, and surface alerts for significant transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexbrc20](https://clawhub.ai/user/alexbrc20) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and crypto analysts use this skill to check monitored wallet addresses for large Ethereum or BSC transactions and review high-value transfer details. It can support market monitoring and risk awareness, but its outputs are informational and not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitored wallet addresses and explorer API keys may be sent to third-party blockchain explorer APIs. <br>
Mitigation: Use low-privilege or disposable API keys and monitor only addresses you are comfortable sharing with Etherscan or BscScan. <br>
Risk: Advertised Telegram real-time alert behavior may not be implemented by the included script. <br>
Mitigation: Test notification behavior before relying on Telegram alerts, and avoid providing a valuable Telegram bot token unless the integration is verified. <br>
Risk: Transaction values are informational and may rely on approximate price assumptions. <br>
Mitigation: Confirm large transfers and valuations against trusted market data and block explorers before making decisions. <br>


## Reference(s): <br>
- [Whale Watcher ClawHub listing](https://clawhub.ai/alexbrc20/whale-watcher) <br>
- [Publisher profile](https://clawhub.ai/user/alexbrc20) <br>
- [Etherscan API](https://api.etherscan.io/api) <br>
- [BscScan API](https://api.bscscan.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with command examples and text transaction summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transaction summaries may include wallet addresses, timestamps, transfer values, and block explorer transaction links.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter and README state 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
