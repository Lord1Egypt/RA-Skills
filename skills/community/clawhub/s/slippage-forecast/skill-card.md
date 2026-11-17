## Description:

A paid x402 endpoint that returns expected slippage estimates for a given order size and market condition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Trading agents and developers use this endpoint to request expected slippage estimates by order size and market condition, helping assess execution costs or compare venues before placing orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A paid request uses an EVM wallet private key and can authorize a USDC charge.

Mitigation: Keep the private key in a secret store and set the x402 maximum-payment policy to the amount intended for each call; check the endpoint price before use.

## Reference(s):

- [Slippage Forecast endpoint](https://apexrunner.ai/signals/slippage-forecast)
- [Optimal Order Routing signal](https://apexrunner.ai/signals/optimal-order-routing)
- [Execution Window Optimizer signal](https://apexrunner.ai/signals/execution-window-optimizer)
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/slippage-forecast)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON slippage forecast with asset, venue, order-size range, average slippage, confidence, and timestamp fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forecast values are returned per asset, venue, and order-size range.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
