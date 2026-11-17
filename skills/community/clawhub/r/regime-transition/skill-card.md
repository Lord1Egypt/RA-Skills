## Description:

A paid x402 endpoint that returns a market signal about the likelihood of an imminent regime transition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automated trading agents use the paid signal to inform strategy changes or exposure decisions during changing market conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each request authorizes a USDC payment using an EVM wallet private key.

Mitigation: Use a dedicated wallet funded for expected calls, protect the private key in a secret store, cap each signed payment, and confirm the current price before use.

Risk: A regime signal is probabilistic and may not predict future market conditions.

Mitigation: Treat the response as one input to a decision and apply independent trading risk controls.

## Reference(s):

- [Regime Transition endpoint](https://apexrunner.ai/signals/regime-transition)
- [ClawHub release page](https://clawhub.ai/kynto2001-ctrl/skills/regime-transition)
- [Related regime signals](https://apexrunner.ai/signals/regime)
- [Regime Confluence signal](https://apexrunner.ai/signals/regime-confluence)
- [Regime Transition Probability signal](https://apexrunner.ai/signals/regime-transition-probability)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON signal response with transition_likely, probability, and target_regime fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid per call; the artifact describes a $0.007 USDC early-adopter price and a $0.01 standard price.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
