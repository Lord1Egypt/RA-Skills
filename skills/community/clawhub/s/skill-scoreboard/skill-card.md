## Description:

Skill Scoreboard helps OpenClaw users track skill usage, calculate daily, weekly, monthly, yearly, and all-time scoreboards, and generate usage snapshots and workflow review reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luis1213899](https://clawhub.ai/user/luis1213899)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to record skill calls, review usage and error history, compare scoreboards over several time windows, and generate daily workflow review reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists local usage history, call logs, and error history.

Mitigation: Install only where retaining skill activity and error history is acceptable, and periodically review or remove stored data under ~/.skill_scoreboard.

Risk: The bundled gateway-log parser reads OpenClaw gateway logs and infers skill usage from message text.

Mitigation: Review, remove, or disable parse_gateway_logs.py unless reading /tmp/openclaw logs and inferring activity from message text is within the intended scope.

Risk: The cron example can automate recurring snapshots and workflow reviews, extending collection over time.

Mitigation: Do not enable the cron schedule until retention, redaction, and collection scope are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luis1213899/skills/skill-scoreboard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local JSON/text report outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled scripts can write local JSON score data, text call logs, text error logs, daily JSON snapshots, and workflow review JSON files.]

## Skill Version(s):

1.3.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
