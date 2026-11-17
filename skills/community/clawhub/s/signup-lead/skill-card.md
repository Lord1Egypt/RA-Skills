## Description:

Create a signup lead in AgenticCreed by submitting contact and personal details through the AgenticCreed signup-leads HTTP endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waqas-orcalo](https://clawhub.ai/user/waqas-orcalo)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to create AgenticCreed signup leads from supplied contact and personal details. It is intended for workflows where the subject has consented to submitting those details to AgenticCreed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal and contact details may be submitted to AgenticCreed without appropriate authorization or consent.

Mitigation: Use the skill only after confirming the subject has consented to sharing the requested lead details with AgenticCreed.

Risk: The AgenticCreed API key could be configured in an environment that is not approved to submit signup leads.

Mitigation: Configure AGENTICCREED_API_KEY only in authorized environments and restrict access to agents that are allowed to create signup leads.

## Reference(s):

- [Signup Lead on ClawHub](https://clawhub.ai/waqas-orcalo/skills/signup-lead)
- [AgenticCreed signup-leads endpoint](https://gateway.agenticcreed.ai/signup-leads)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTICCREED_API_KEY and submits the configured lead fields to AgenticCreed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
