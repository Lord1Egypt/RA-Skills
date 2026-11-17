## Description:

Monitors A-share stock prices using the Sina Finance API, supports scheduled trading-hours checks, threshold alerts, real-time queries, and local price logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[likepost](https://clawhub.ai/user/likepost)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor configured China A-share symbols during trading hours, query current prices, and receive threshold alerts while retaining daily price and alert logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring market checks may send alert details through a hardcoded Xiaoyi delivery target.

Mitigation: Review and change stock_config.json before installing, especially delivery_channel and delivery_target.

Risk: Price and alert history are retained in local JSON log/state files.

Mitigation: Install only where local retention of price and alert logs is acceptable, and clear generated log/state files according to the user's retention needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/likepost/skills/stock-monitor-a)
- [Publisher profile](https://clawhub.ai/user/likepost)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, configuration]

**Output Format:** [Plain text responses with JSON configuration and local JSON log/state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The action parameter selects check, query, log, or log_history output.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact files declare 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
