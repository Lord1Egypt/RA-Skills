## Description:

Monitors sports betting odds movement across Asian handicap, European odds, and over/under markets, then reports notable changes and betting-risk signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and betting-market analysts use this skill to monitor sports odds movement, compare market changes, detect anomalies, and generate concise monitoring reports with suggested actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid billing code embeds a live-looking billing API key.

Mitigation: Remove embedded billing credentials and require host-managed secret injection or a verified platform billing integration before deployment.

Risk: The payment flow can charge an environment-selected user identity without clear in-artifact authorization safeguards.

Mitigation: Bind charges to a verified platform identity and require explicit user confirmation or a trusted host-controlled charge flow.

Risk: The skill contacts both The Odds API and skillpay.me during normal operation.

Mitigation: Install only in environments where those external service calls and the paid usage model are expected and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenmeng/skills/shenmeng-odds-movement-monitor)
- [Publisher profile](https://clawhub.ai/user/shenmeng)
- [The Odds API endpoint](https://api.the-odds-api.com/v4)
- [SkillPay billing provider](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and console-style text reports with optional Python code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include odds snapshots, detected changes, anomaly labels, confidence scores, recommendations, and payment status.]

## Skill Version(s):

2026.4.15-100 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
