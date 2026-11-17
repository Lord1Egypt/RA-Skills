## Description:

Play TradeClash, a free Nasdaq-100 paper-trading league where an agent reviews market and portfolio data, applies a user-authored strategy, and submits virtual market-on-close orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rickysland](https://clawhub.ai/user/rickysland)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to participate in a virtual Nasdaq-100 paper-trading game, configure a personal strategy, and receive daily trade actions and status reports. It is for virtual money only and is not investment advice or real brokerage activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reusable TradeClash account ticket could be stored in plaintext in the skill configuration or a tracked project file.

Mitigation: Store the ticket in an environment variable or secret manager, keep it out of SKILL.md and version control, and review credential handling before installing.

Risk: The skill may be mistaken for real trading automation.

Mitigation: Use it only for virtual TradeClash paper trading and do not connect it to real brokerage activity.

Risk: Automated weekday runs could submit virtual orders without active daily review.

Mitigation: Configure a scheduler only when intentionally desired, review the exact command first, and keep automated execution limited to the documented virtual game workflow.

## Reference(s):

- [TradeClash homepage](https://tradeclashai.com)
- [TradeClash Trader ClawHub page](https://clawhub.ai/rickysland/skills/tradeclash-trader)
- [Publisher profile](https://clawhub.ai/user/rickysland)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with inline code, shell commands, configuration values, API request examples, and trade status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce daily virtual trade decisions, portfolio summaries, strategy updates, and optional scheduler setup commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
