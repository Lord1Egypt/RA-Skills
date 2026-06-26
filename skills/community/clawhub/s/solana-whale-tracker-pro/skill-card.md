## Description: <br>
Real-time monitoring of Solana token prices, large transfers, liquidity pools, new tokens, and price alerts via Telegram and email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chungvic](https://clawhub.ai/user/chungvic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
DeFi traders, NFT traders, project teams, and developers use this skill to monitor Solana ecosystem activity, configure token price alerts, and inspect large-transfer or liquidity signals. Some artifact-documented monitoring features are described as MVP or in development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram or email alert credentials can be exposed through local configuration or environment handling. <br>
Mitigation: Store secrets in environment variables or a secrets manager, avoid committing configuration files, and rotate exposed tokens. <br>
Risk: Long-running monitoring depends on third-party APIs and Python dependencies that may change, fail, or be rate limited. <br>
Mitigation: Pin or audit dependencies, test API behavior before deployment, and monitor failures during operation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chungvic/solana-whale-tracker-pro) <br>
- [Publisher Profile](https://clawhub.ai/user/chungvic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include YAML or environment-variable configuration examples and operational alert guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
