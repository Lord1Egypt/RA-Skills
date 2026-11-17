## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns current market regime label at minimal cost for fast agent loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents use this paid endpoint to retrieve a compact market-regime label for frequent checks and as a pre-filter before deeper signal analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each request authorizes a USDC payment from the configured wallet.

Mitigation: Set a payment cap and check the amount before signing requests; the example uses an x402 maximum-amount policy.

Risk: The EVM_PRIVATE_KEY can authorize access to the wallet if exposed.

Mitigation: Keep the key in a protected secret store or environment and avoid printing or sharing it.

Risk: A compact regime label may be incomplete for making a trading decision.

Mitigation: Check other relevant signals and analysis instead of relying on this response as the sole trading input.

## Reference(s):

- [Regime Micro endpoint](https://apexrunner.ai/signals/regime-micro)
- [Regime signal](https://apexrunner.ai/signals/regime)
- [Regime Confluence signal](https://apexrunner.ai/signals/regime-confluence)
- [Trend Confirmed signal](https://apexrunner.ai/signals/trend-confirmed)
- [ClawHub release page](https://clawhub.ai/kynto2001-ctrl/skills/regime-micro)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [Compact JSON market-regime response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response fields: b, e, s, a, and t.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
