## Description:

Real-time crypto market intelligence for autonomous agents. Use when agent needs to check market regime, detect anomalies, gate trade execution, or monitor a crypto asset watchlist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paperbuddha](https://clawhub.ai/user/paperbuddha)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to query RiskGate market-regime, anomaly, and sentiment signals for supported crypto assets before monitoring reports or trading gates. The skill helps agents decide when to proceed, pause, use conservative defaults, or surface a market condition to a human.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crypto market signals may be overused as trading advice or as the sole basis for automatic execution.

Mitigation: Treat RiskGate responses as decision support only, keep human responsibility explicit, and avoid automatic trading based solely on these signals.

Risk: RiskGate API keys, demo keys, or M2M credentials could be exposed in prompts, logs, or agent output.

Mitigation: Use scoped credentials, prefer the RISKGATE_API_KEY environment variable for paid keys, and instruct agents not to print or persist secrets.

Risk: Demo-tier quota exhaustion or rate limits can leave an agent without a current signal.

Mitigation: Check account credits, prioritize high-value assets, halt execution when credits are exhausted, and notify a human before proceeding.

Risk: Quota-upgrade language can read as commercial promotion in contexts where that is not acceptable.

Mitigation: Replace upgrade prompts with a neutral status message when commercial wording is unsuitable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paperbuddha/skills/riskgate-market-signals)
- [PaperBuddha publisher profile](https://clawhub.ai/user/paperbuddha)
- [RiskGate API base](https://api.riskgate.xyz)
- [RiskGate portal](https://riskgate.xyz/portal)
- [RiskGate API reference](artifact/api-reference.md)
- [RiskGate decision logic](artifact/decision-logic.md)
- [RiskGate monitoring pattern](artifact/monitoring.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, plain-text alerts, API request examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference RiskGate API responses and credential handling; the skill itself does not produce persistent files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
