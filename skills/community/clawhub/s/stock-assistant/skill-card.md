## Description: <br>
Stock Assistant is a Python A-share trading helper for quote lookup, trade record management, position tracking, PnL analysis, CSV import/export, and optional Feishu notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[54meteor](https://clawhub.ai/user/54meteor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to run a local CLI for A-share market quote checks, portfolio record keeping, PnL calculations, and CSV-based trade import/export. Users can also format quote and position updates for Feishu delivery when they provide trusted notification credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock and portfolio details can be sent to Feishu or arbitrary webhook destinations. <br>
Mitigation: Use only trusted webhook URLs and verified recipients, and disable or avoid notification commands when portfolio disclosure is not acceptable. <br>
Risk: Feishu App Secret values may be passed on the command line for private-message delivery. <br>
Mitigation: Prefer safer secret handling outside shell history and process listings, and rotate credentials if they may have been exposed. <br>
Risk: Local trade data can be imported, deleted, exported, and stored in a SQLite database. <br>
Mitigation: Review bundled CSV files before import and back up or export the local database before destructive record changes. <br>


## Reference(s): <br>
- [Detailed design](references/design.md) <br>
- [Tencent Finance](https://finance.qq.com/) <br>
- [ClawHub skill page](https://clawhub.ai/54meteor/stock-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [CLI text, Python dictionaries, Feishu card JSON, CSV files, and SQLite-backed local records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read and write local trade data and can send portfolio-related quote summaries to Feishu or webhook destinations when configured.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
