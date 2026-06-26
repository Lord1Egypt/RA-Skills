## Description: <br>
Onchain trade execution engine that takes a contract address and score, then handles sized entry, mode-based exits, on-chain verification, and trade logging through Bankr. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[riskanon](https://clawhub.ai/user/riskanon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use tradr to connect their own token signals to automated crypto trade entry, monitoring, exit rules, and trade logging. The skill is intended for users who already operate Bankr and want configurable position lifecycle management rather than signal generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent live crypto buy and sell automation can move real funds through Bankr once configured. <br>
Mitigation: Install only when automated crypto trading is intended, use an isolated wallet with limited funds, and review position-size caps and exit rules before enabling the daemon. <br>
Risk: Notification routing and dashboard data can expose sensitive trade or wallet activity. <br>
Mitigation: Disable notifications or verify Telegram routing before adding secrets, and do not expose dashboard API endpoints publicly without authentication and redaction. <br>
Risk: Running the exit manager as a broad system service increases operational exposure. <br>
Mitigation: Prefer a user-scoped service where possible and monitor the service status, logs, and generated trade files after installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/riskanon/tradr) <br>
- [Signal adapter interface](adapters/README.md) <br>
- [Bankr](https://bankr.bot) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, code, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, Python scripts, logs, and dashboard data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Bankr skill and user-provided wallet addresses for on-chain verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
