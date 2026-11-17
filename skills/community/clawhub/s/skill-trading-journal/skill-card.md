## Description:

Logs trades with context, generates weekly and monthly performance reports, and helps identify win/loss patterns for strategy review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Traders and trading-system operators use this skill to record entries, exits, PnL, thesis, emotion, and lessons. They can use the journal to generate weekly and monthly reviews that support strategy updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trade history, strategy notes, PnL, and emotion tags may be sensitive if stored on a shared machine or synced folder.

Mitigation: Use appropriate local file permissions, backups, and deletion practices for the journal file before installing or using the skill.

Risk: Generated reports and strategy adjustments may influence trading decisions.

Mitigation: Review performance summaries and proposed rule updates before acting on them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown reports and structured JSON trade records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local journal file path described by the skill when the agent follows the workflow.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
