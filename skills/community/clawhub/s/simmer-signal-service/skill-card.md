## Description:

Professional Polymarket trading signals powered by Simmer and Binance, producing BUY/SELL/HOLD recommendations with confidence scores for BTC, ETH, and SOL fast markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickqi688](https://clawhub.ai/user/nickqi688)

### License/Terms of Use:


## Use Case:

External users can run the skill to request crypto prediction-market signals for BTC, ETH, and SOL fast markets. The skill checks billing, fetches market data, and returns a signal, confidence score, reasoning, and balance information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Billing disclosures and safeguards are inconsistent across the evidence.

Mitigation: Review the skill before installing, confirm the actual per-call price, and use a spend cap before enabling recurring use.

Risk: Recurring cron examples can generate repeated paid calls.

Mitigation: Do not enable recurring schedules unless pricing, limits, and account balance behavior have been verified.

Risk: The skill requires SkillPay and Simmer API keys.

Mitigation: Provide credentials only if the publisher and connected services are trusted, and scope or rotate keys where possible.

Risk: Security evidence says billing errors should fail closed and demo payment behavior should be removed from production.

Mitigation: Prefer a version that fails closed on billing failures and avoids demo fallback charging behavior in production paths.

Risk: Dependencies are not pinned to exact versions.

Mitigation: Pin and review dependencies before deployment in managed or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickqi688/skills/simmer-signal-service)
- [Publisher profile](https://clawhub.ai/user/nickqi688)
- [SkillPay](https://skillpay.me)
- [Simmer](https://simmer.markets)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON responses and Markdown documentation with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime responses can include charged amount, remaining balance, asset, signal, confidence score, reasoning, timestamp, and data-source availability.]

## Skill Version(s):

1.0.1 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
