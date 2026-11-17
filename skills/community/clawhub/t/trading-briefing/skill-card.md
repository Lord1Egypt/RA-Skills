## Description:

Trading Briefing generates a daily cryptocurrency trading report that combines market prices, trading bot status, positions and PnL, system health, and strategy discovery status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huili203](https://clawhub.ai/user/huili203)

### License/Terms of Use:

MIT-0

## Use Case:

Traders and trading-system operators use this skill to ask an agent for a concise daily status briefing across crypto market prices, local bot status, current positions, PnL, system health, and strategy discovery results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The briefing can expose local trading state, positions, PnL, logs, process status, disk, and memory through normal agent use.

Mitigation: Install only where agent users are allowed to view that operational and trading information, and narrow trigger phrases if accidental disclosure during ordinary chat is a concern.

Risk: Saved briefings may persist trading and system status information in the workspace.

Mitigation: Use saved output only when workspace storage is acceptable for that information.

## Reference(s):

- [Trading Briefing on ClawHub](https://clawhub.ai/huili203/skills/trading-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Formatted text report, with optional Markdown file output when saved]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local trading state, logs, process status, disk, and memory; can save the generated briefing to the workspace when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
