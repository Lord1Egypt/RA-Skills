## Description:

Build and run Polymarket copy-trading workflows for trader discovery, cycle detection, candidate ranking, risk limits, and execution handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangbo12bob2-source](https://clawhub.ai/user/wangbo12bob2-source)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn Polymarket leaderboard snapshots into ranked copy-trading candidates and dry-run or execute threshold-based order plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live execution mode can place repeated real-money Polymarket buy orders, and the advertised risk limits are not reliably enforced by the code.

Mitigation: Use dry-run mode by default. Enable live execution only with a tightly limited account, independently verified exposure controls, and manual supervision.

## Reference(s):

- [Auto copy-trade configuration example](references/auto-copytrade-config.example.json)
- [Polymarket leaderboard Data API](https://data-api.polymarket.com/v1/leaderboard)
- [ClawHub skill listing](https://clawhub.ai/wangbo12bob2-source/skills/wangbo-polymarket-copytrading)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce ranked trader summaries, dry-run order commands, or live execution handoff guidance.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
