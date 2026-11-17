## Description:

A paid x402 endpoint that returns whether the current trend has sufficient momentum to trade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and crypto traders can use the endpoint as a momentum confirmation signal before trend-following trades or to filter possible false breakouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each x402 request incurs a USDC charge, and the example signs payment using an EVM private key.

Mitigation: Keep EVM_PRIVATE_KEY in a protected secret store, set a per-request spending cap appropriate to your budget, and review the endpoint and current price before enabling calls.

## Reference(s):

- [Trend Confirmed endpoint](https://apexrunner.ai/signals/trend-confirmed)
- [ClawHub skill release](https://clawhub.ai/kynto2001-ctrl/skills/trend-confirmed)
- [Related regime signal](https://apexrunner.ai/signals/regime)
- [Related APEX composite signal](https://apexrunner.ai/signals/apex-composite)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON signal response with confirmation, direction, and strength fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid x402 request; release summary lists $0.007 USDC per call on Base.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
