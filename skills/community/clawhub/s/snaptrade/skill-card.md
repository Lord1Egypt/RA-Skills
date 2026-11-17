## Description:

Connects to a user's investment accounts through the SnapTrade SDK to create brokerage connection links, manage reconnections, list accounts and brokerages, generate portfolio value reports, and place or monitor stock and ETF orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brendanwood](https://clawhub.ai/user/brendanwood)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to connect brokerage accounts through SnapTrade, retrieve account and portfolio data, create connection or reconnect links, and run explicitly configured stock or ETF order workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live stock or ETF trades when trading credentials and account scope are configured.

Mitigation: Before running order workflows, verify the account, action, symbol, units, order type, limit price, time in force, and whether monitoring is enabled.

Risk: Brokerage credentials and SnapTrade user secrets are stored in a local configuration file.

Mitigation: Keep the configuration outside the repository, restrict file permissions, and remove or rotate credentials when access is no longer needed.

Risk: Scheduled portfolio reports can repeatedly expose financial information to an external destination.

Mitigation: Confirm the report recipient, delivery channel, schedule, and removal steps before enabling cron-based reporting.

Risk: Portfolio totals may include disabled connections or stale synchronization states.

Mitigation: Review disabled-connection and sync-timeout output before using portfolio totals for financial decisions.

## Reference(s):

- [ClawHub SnapTrade Skill Page](https://clawhub.ai/brendanwood/skills/snaptrade)
- [SnapTrade](https://snaptrade.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or text outputs from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include connection or reconnect URLs, account and brokerage lists, portfolio totals, order status updates, and scheduled reporting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
