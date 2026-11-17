## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns upcoming token unlock events that may create sell pressure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use this signal in crypto research and trading workflows to review upcoming token unlocks as a potential source of sell pressure and as an input to risk filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example signs paid Base USDC requests using EVM_PRIVATE_KEY.

Mitigation: Keep the key in a secrets manager, use a wallet with a limited USDC balance, and retain the per-call max_amount cap.

Risk: A clean scan does not guarantee zero risk.

Mitigation: Review whether the skill's purpose suits your needs before installing, as recommended by the security guidance.

## Reference(s):

- [Token Unlock endpoint](https://apexrunner.ai/signals/token-unlock)
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/token-unlock)
- [Narrative Intelligence signal](https://apexrunner.ai/signals/narrative-intelligence)
- [Regime signal](https://apexrunner.ai/signals/regime)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON response containing upcoming token unlock records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid x402 request; requires an EVM wallet with USDC on Base and an EVM_PRIVATE_KEY.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
