## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns aggregated signal quality score across all active APEX modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents can pay per call to retrieve a single aggregated APEX signal-quality score for confidence calibration. Use the score as one input when assessing signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The paid request uses an EVM wallet key and spends USDC automatically.

Mitigation: Keep EVM_PRIVATE_KEY in a secret store, limit the wallet balance to intended spending, and retain a per-call payment cap.

Risk: An aggregated signal-quality score may be mistaken for a trading recommendation or guarantee.

Mitigation: Treat the score as one input to confidence calibration and assess trading decisions and risk independently.

## Reference(s):

- [Signal Intelligence endpoint](https://apexrunner.ai/signals/signal-intelligence)
- [APEX Composite signal](https://apexrunner.ai/signals/apex-composite)
- [Combined Alpha signal](https://apexrunner.ai/signals/combined-alpha)
- [APEX Alpha Score signal](https://apexrunner.ai/signals/apex-alpha-score)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Analysis]

**Output Format:** [JSON response with quality_score, signals_active, and confidence fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One aggregated signal-quality result per request.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
