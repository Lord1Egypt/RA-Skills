## Description:

Manage Steven's A-share shadow trading dashboard, including simulated trades, positions, equity data, trade history, P&L, and dashboard files under trade/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j97feng-beep](https://clawhub.ai/user/j97feng-beep)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to maintain a local A-share simulated trading dashboard, update trade records, calculate equity and fees, and refresh dashboard data after buy, sell, stop-loss, or take-profit events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill updates local simulated trading records, including positions, orders, metrics, CSVs, dashboard data, and trade history.

Mitigation: Review proposed file changes before accepting them and keep backups of trade/ if those records matter.

Risk: Incorrect prices, quantities, fees, or equity calculations could make the dashboard misleading.

Mitigation: Check trade inputs, fee calculations, and current equity values before using refreshed dashboard results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/j97feng-beep/skills/shadow-trading-dashboard)
- [Publisher Profile](https://clawhub.ai/user/j97feng-beep)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON, CSV, JSONL, HTML, and shell command updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local simulated-trading file updates under trade/ and dashboard refresh instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
