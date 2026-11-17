## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns momentum + whale sentiment + regime confluence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External agents use this paid endpoint to retrieve combined momentum, whale sentiment, and market regime signals in one request before making multi-factor crypto trading decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner marks the release suspicious because the per-call payment ceiling is above the advertised discounted price; repeated calls may cost more in total than that advertised price.

Mitigation: Review the payment terms, including the per-call ceiling, before installing, and monitor repeated calls and cumulative charges.

## Reference(s):

- [Trading Intelligence Bundle endpoint](https://apexrunner.ai/signals/trading-intelligence-bundle)
- [ClawHub release](https://clawhub.ai/kynto2001-ctrl/skills/trading-intelligence-bundle)
- [Market Pulse Bundle](https://apexrunner.ai/signals/market-pulse-bundle)
- [Risk Assessment Bundle](https://apexrunner.ai/signals/risk-assessment-bundle)
- [APEX Composite](https://apexrunner.ai/signals/apex-composite)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [Structured JSON market signals, including momentum status, whale sentiment, regime confluence, and a timestamp.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned by a paid x402 request; the agent needs an EVM wallet private key and USDC on Base.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
