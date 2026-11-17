## Description:

Returns a paid market-regime classification (TRENDING, RANGING, CHOPPY, or CRISIS) from the APEX Runner endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Trading agents use the classification as market context before choosing a strategy or routing decisions through regime-aware logic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid requests use an EVM wallet private key and spend USDC on Base.

Mitigation: Use a dedicated wallet with limited funds and set a strict per-request payment cap.

Risk: A regime classification may be an incomplete basis for a trading decision.

Mitigation: Check the signal against independent market information before acting.

## Reference(s):

- [Regime endpoint](https://apexrunner.ai/signals/regime)
- [Regime Micro](https://apexrunner.ai/signals/regime-micro)
- [Regime Confluence](https://apexrunner.ai/signals/regime-confluence)
- [Regime Transition](https://apexrunner.ai/signals/regime-transition)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a regime label, confidence, asset symbol, and timestamp.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
