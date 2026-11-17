## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns 4 signals in one call — liquidation pressure + liquidation magnet + portfolio heat + whale sentiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and crypto market participants can retrieve a paid bundle of four market risk signals for dashboards, periodic monitoring, or additional context before position changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The x402 client uses EVM_PRIVATE_KEY to sign USDC payments for endpoint calls.

Mitigation: Keep the key in a secret store, use a wallet funded only for intended calls, and retain a strict maximum-payment policy.

Risk: Market signals may be used to inform position changes, and the response states that it is valid for 300 seconds.

Mitigation: Treat the signals as time-sensitive supporting information and independently verify current market conditions before acting.

## Reference(s):

- [APEX Runner Risk Assessment Bundle endpoint](https://apexrunner.ai/signals/risk-assessment-bundle)
- [ClawHub release page](https://clawhub.ai/kynto2001-ctrl/skills/risk-assessment-bundle)
- [APEX Runner Trading Intelligence Bundle](https://apexrunner.ai/signals/trading-intelligence-bundle)
- [APEX Runner Portfolio Heat](https://apexrunner.ai/signals/portfolio-heat)
- [APEX Runner Agent Stress Index](https://apexrunner.ai/signals/agent-stress-index)

## Skill Output:

**Output Type(s):** [API calls, JSON data]

**Output Format:** [JSON response from the paid endpoint]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Four market signals per call; the response states a 300-second validity period.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
