## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns probabilistic regime transition forecast with timing estimate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the paid x402 endpoint to retrieve a probabilistic market regime transition forecast and estimated timing, which can inform regime-aware strategy allocation or hedging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests incur USDC charges and the example requires an EVM private key.

Mitigation: Protect EVM_PRIVATE_KEY in a secret store and review the endpoint and payment cap before sending a request.

Risk: A probabilistic forecast and estimated timing may not match subsequent market behavior.

Mitigation: Treat the response as an uncertain input to analysis rather than a guaranteed outcome.

## Reference(s):

- [Regime Transition Probability API](https://apexrunner.ai/signals/regime-transition-probability)
- [Related signal: Regime Transition](https://apexrunner.ai/signals/regime-transition)
- [Related signal: Regime Confluence](https://apexrunner.ai/signals/regime-confluence)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON response containing regime, transition probability, likely next regime, and estimated timing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forecast values are returned by a paid x402 request.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
