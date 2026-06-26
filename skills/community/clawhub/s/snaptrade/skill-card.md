## Description: <br>
Connect to a user's investment accounts via SnapTrade SDK and generate portfolio reports, connection portal links, account registration support, brokerage reconnection flows, and order-related workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brendanwood](https://clawhub.ai/user/brendanwood) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to connect brokerage accounts through SnapTrade, retrieve portfolio account data, produce total-value reports, and support order placement or monitoring when trading authority is intentionally enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real brokerage trades when SnapTrade trade authority is available. <br>
Mitigation: Require explicit confirmation of account, symbol, side, quantity, order type, time in force, and price before any trade; avoid order scripts for read-only reporting workflows. <br>
Risk: Stored SnapTrade credentials and user secrets grant ongoing brokerage access. <br>
Mitigation: Store the secrets file with restrictive permissions, avoid sharing it, and use read-only brokerage permissions where possible. <br>
Risk: Recurring reporting or messaging automation can repeatedly access financial account data. <br>
Mitigation: Review cron and messaging automation before enabling it and limit scheduled jobs to the minimum reporting scope needed. <br>


## Reference(s): <br>
- [SnapTrade](https://snaptrade.com) <br>
- [ClawHub SnapTrade release](https://clawhub.ai/brendanwood/snaptrade) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit connection or reconnect URLs, account lists, portfolio totals, order placement status, and order monitoring updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
