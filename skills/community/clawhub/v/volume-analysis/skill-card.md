## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns volume profile analysis detecting accumulation or distribution patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents use the paid endpoint to request volume profile signals that can help assess breakouts, accumulation, distribution, and momentum setups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid calls spend USDC from a wallet on Base.

Mitigation: Check the current price and set an explicit payment cap before authorizing calls.

Risk: The example reads an EVM private key from EVM_PRIVATE_KEY to authorize payment.

Mitigation: Use a dedicated wallet with limited funds and keep the key in a secure secret store.

Risk: Volume signals may be incomplete or misleading when used to make trading decisions.

Mitigation: Treat the response as one analytical input and apply independent validation and trading controls.

## Reference(s):

- [Volume Analysis endpoint](https://apexrunner.ai/signals/volume-analysis)
- [ClawHub release page](https://clawhub.ai/kynto2001-ctrl/skills/volume-analysis)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, JSON]

**Output Format:** [JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Example fields: signal, volume_ratio, and above_average.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
