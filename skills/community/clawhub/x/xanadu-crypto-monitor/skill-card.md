## Description: <br>
Monitor cryptocurrency prices, set customizable price alerts, track large whale transactions, analyze on-chain metrics, and manage crypto portfolios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saintlittlefish](https://clawhub.ai/user/saintlittlefish) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to monitor cryptocurrency market data, create price alerts, inspect whale and on-chain activity, and track portfolio holdings from an agent-assisted workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled billing code includes an exposed SkillPay key and mismatched product references. <br>
Mitigation: Treat the key as compromised, remove or rotate it before use, and require clear user approval before any charge flow is enabled. <br>
Risk: Portfolio holdings and alert details may be stored locally under ~/.openclaw/crypto-monitor. <br>
Mitigation: Use the skill only on trusted systems and avoid storing sensitive financial details unless local data handling is acceptable. <br>
Risk: The server security verdict marks this release suspicious pending review. <br>
Mitigation: Review the package before installing and verify billing, data storage, and network behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/saintlittlefish/xanadu-crypto-monitor) <br>
- [CoinGecko API](https://api.coingecko.com/api/v3) <br>
- [SkillPay API](https://api.skillpay.me/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON data files when commands are executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores alerts and portfolio data under ~/.openclaw/crypto-monitor when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
