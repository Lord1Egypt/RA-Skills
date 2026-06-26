## Description: <br>
Whale Alert Monitor provides scripts and guidance for crypto whale wallet monitoring, large-transfer alerts, exchange flow analysis, and holding analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and run crypto wallet monitoring workflows, review large transfer alerts, and analyze exchange inflow or outflow patterns. Treat generated reports and alerts as simulated unless the publisher provides verified live blockchain or exchange integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is marketed as live whale tracking, while security evidence says core reports and alerts are randomly simulated. <br>
Mitigation: Treat outputs as demo or simulated data until the publisher provides verified live blockchain or exchange integrations and clear data provenance. <br>
Risk: The skill includes paid billing behavior for each call. <br>
Mitigation: Verify payment behavior and user identity handling before running payment.py or authorizing any USDT charge. <br>
Risk: Notification features may send data to Telegram, Discord, or custom webhook destinations. <br>
Mitigation: Use only trusted webhook destinations and protect bot tokens and chat identifiers in environment variables. <br>
Risk: Daemon and alert scripts can keep local alert, configuration, and history files. <br>
Mitigation: Run the daemon only when continuous local logging is acceptable and review generated files for sensitive wallet or alert data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenmeng/shenmeng-whale-alert-monitor-v2) <br>
- [shenmeng publisher profile](https://clawhub.ai/user/shenmeng) <br>
- [API data source configuration](artifact/references/api-configuration.md) <br>
- [Whale wallet label library](artifact/references/wallet-labels.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, console text, Python scripts, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local alert/configuration/history JSON files when the included scripts are run.] <br>

## Skill Version(s): <br>
1.99.99 (source: server release metadata; artifact frontmatter states 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
