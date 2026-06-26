## Description: <br>
Monitors cryptocurrency whale wallets, large transfers, exchange fund flows, and alert workflows for crypto activity analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and crypto analysts use this skill to configure whale wallet monitoring, large transfer alerts, exchange flow tracking, and whale behavior reports. It is for informational monitoring and should not be treated as trading, compliance, or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill advertises real crypto monitoring while mostly generating simulated financial data. <br>
Mitigation: Treat outputs as informational unless the publisher documents and verifies live data sources before use. <br>
Risk: The security review identifies direct billing behavior and payment requirements. <br>
Mitigation: Confirm when charges occur, rotate or remove exposed billing credentials, and review payment behavior before installation or execution. <br>
Risk: The skill can send Telegram, Discord, or webhook notifications that may disclose wallet monitoring details. <br>
Mitigation: Use dedicated notification channels and review destination tokens, webhook URLs, and shared data before enabling alerts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shenmeng/shenmeng-whale-alert-2025) <br>
- [API configuration guide](references/api-configuration.md) <br>
- [Wallet labels reference](references/wallet-labels.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python examples, and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet addresses, alert thresholds, payment prompts, third-party API configuration, and notification setup details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
