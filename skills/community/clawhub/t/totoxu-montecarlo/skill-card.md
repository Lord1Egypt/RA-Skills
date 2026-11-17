## Description:

Monte Carlo Crypto Trading Core. Simulates thousands of future price paths (Geometric Brownian Motion) to evaluate win probabilities, risk of ruin, and stop-loss impact for trading strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[totoxu](https://clawhub.ai/user/totoxu)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to run Monte Carlo simulations for crypto trading positions and estimate win probability, stop-loss probability, take-profit probability, and price percentiles. The results can support risk assessment, but they should not be treated as guaranteed trading outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically contacts an external paid billing service using user IDs during normal simulation execution.

Mitigation: Require explicit user approval before any paid charge and document the billing flow before installation.

Risk: The security summary identifies a bundled API key and the release changelog says billing keys were hardcoded as defaults.

Mitigation: Require the publisher to remove embedded keys and use deployment-provided secrets only.

Risk: The security guidance identifies an environment variable mismatch for billing configuration.

Mitigation: Align the documented and runtime environment variables before deployment.

Risk: The security guidance says user data sent to SkillPay is not fully documented.

Mitigation: Document exactly what user data is sent to the billing service and obtain user consent for that transfer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/totoxu/skills/totoxu-montecarlo)
- [SkillPay billing API endpoint](https://skillpay.me/api/v1/billing)

## Skill Output:

**Output Type(s):** [JSON, guidance, shell commands]

**Output Format:** [JSON simulation results with risk metrics, optionally summarized by the agent as user-facing guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Simulation limits are 20,000 paths and 365 days; normal execution requires a billed user ID unless billing is explicitly skipped for testing.]

## Skill Version(s):

1.3.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
