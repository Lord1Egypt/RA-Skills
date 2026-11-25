## Description:

Provides paid, live crypto market signals for potential short-squeeze setups in BTC, ETH, and SOL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the paid endpoint to check live BTC, ETH, and SOL market conditions for potential short-squeeze setups and receive an entry zone, target, and invalidation level when its signal criteria are met.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Squeeze risk is described as an uncalibrated heuristic, and live market signals may not predict price movements reliably.

Mitigation: Treat the returned setup as decision support; check current market conditions and apply independent risk limits before acting.

Risk: The security scan did not inspect the four external links listed by the skill.

Mitigation: Review those external pages before relying on their content.

## Reference(s):

- [Short Squeeze Fuel signal endpoint](https://apexrunner.ai/signals/short-squeeze-fuel)
- [Capitulation Alert](https://apexrunner.ai/signals/capitulation-alert)
- [Crowded Trade Detector](https://apexrunner.ai/signals/crowded-trade-detector)
- [Liquidation Pressure](https://apexrunner.ai/signals/liquidation-pressure)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON response payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One signal payload per call; may include alert status, entry zone, target, invalidation, and a no-setup reason.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
