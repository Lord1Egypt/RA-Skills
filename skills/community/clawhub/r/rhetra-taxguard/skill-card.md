## Description:

Rhetra TaxGuard checks trading-agent orders for wash-sale, pattern-day-trader, holding-period, and tax-loss-harvesting issues, then supports daily tax-risk reports and optional Guardian Mode blocking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronahadi23](https://clawhub.ai/user/aaronahadi23)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and agent developers use this skill to add pre-trade tax and trading-compliance checks to trading agents and to produce daily tax-risk summaries from checked activity.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill sends detailed trading, account, income, and tax context to Rhetra for every checked trade.

Mitigation: Review data-sharing requirements before installation, collect trader consent, and send only the fields needed for the chosen check.

Risk: API keys and sensitive trading context may be exposed if stored in ordinary agent memory or shell history.

Mitigation: Store the Rhetra API key in a real secret store or protected environment variable and avoid placing secrets in prompts, logs, or command history.

Risk: Guardian Mode can proceed silently when TaxGuard is unreachable, so a protected trade may execute without a compliance check.

Mitigation: For protected workflows, configure outages to fail closed or require explicit trader confirmation before an unchecked trade proceeds.

Risk: Tax and trading-compliance guidance can affect financial decisions.

Mitigation: Treat reports as decision support and have qualified tax or compliance professionals review material actions and end-of-year outputs.

## Reference(s):

- [Rhetra TaxGuard ClawHub listing](https://clawhub.ai/aaronahadi23/skills/rhetra-taxguard)
- [aaronahadi23 ClawHub publisher profile](https://clawhub.ai/user/aaronahadi23)
- [Rhetra trading signup](https://rhetra.io/trading)
- [Rhetra website](https://rhetra.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and plain-text trade check output with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guardian Mode may block selected risks before trade execution; daily reports summarize accumulated trade checks.]

## Skill Version(s):

1.0.0 (source: server evidence and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
