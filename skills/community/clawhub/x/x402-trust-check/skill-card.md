## Description:

Check the trust rating of any x402 service before paying it, and of any skill before installing it. Free JSON, daily, sybil-resistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aladaf](https://clawhub.ai/user/aladaf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to review adoption and liveness ratings for x402 payment recipients or skills before paying or installing them. It provides a risk-informed signal, not a guarantee of service quality or safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checking a service or skill shares its hostname or name with agenteconomy.report.

Mitigation: Avoid submitting confidential identifiers.

Risk: Optional paid checks can trigger wallet payments.

Mitigation: Keep automatic payments within the approved budget; use the free rating for routine checks.

Risk: Adoption and liveness ratings may be mistaken for a guarantee of quality or safety.

Mitigation: Treat ratings as one signal, and review the service or skill independently when the decision requires more assurance.

## Reference(s):

- [Agent Economy Report](https://agenteconomy.report/s/)
- [Rating methodology and corrections policy](https://agenteconomy.report/s/policy)
- [ClawHub skill release](https://clawhub.ai/aladaf/skills/x402-trust-check)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text guidance]

**Output Format:** [JSON rating data with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interprets reported adoption and liveness signals; ratings do not guarantee quality or safety.]

## Skill Version(s):

1.5.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
