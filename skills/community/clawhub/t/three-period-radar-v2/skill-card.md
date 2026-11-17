## Description:

Chinese-language A-share technical analysis skill that uses monthly, weekly, and daily trend alignment to score securities, scan sectors, and produce position-management guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentforge-cyber](https://clawhub.ai/user/agentforge-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to research A-share holdings, watchlists, and sector ETFs with a three-period trend framework. It turns radar scores into structured technical-analysis reports with trigger conditions, stop-loss levels, position guidance, and disclaimers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat buy, sell, stop-loss, or position-size outputs as authoritative financial advice.

Mitigation: Present outputs as research signals, preserve trigger conditions and risk notes, and require human review before any trading decision.

Risk: Daily auto-run wording may lead to unsupervised recurring execution.

Mitigation: Configure recurring scans only deliberately, monitor each run, and keep generated reports under user-controlled review.

Risk: Market data may be stale or incomplete when a report is generated.

Mitigation: Include the data cutoff date, verify the latest trading day, and note when current-market correction is needed.

## Reference(s):

- [Three-period framework reference](references/framework.md)
- [ClawHub skill page](https://clawhub.ai/agentforge-cyber/skills/three-period-radar-v2)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Chinese-language Markdown reports and structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses daily OHLCV CSV inputs; reports should include data cutoff, ranked signals, risk notes, and a disclaimer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
