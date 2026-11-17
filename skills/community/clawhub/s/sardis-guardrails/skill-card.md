## Description:

Real-time security monitoring and circuit breaker controls for Sardis agent wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efedurmaz16](https://clawhub.ai/user/efedurmaz16)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect Sardis wallet guardrail status, monitor rate limits and behavioral alerts, and issue emergency circuit breaker or kill switch commands during security incidents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate or deactivate wallet-wide emergency controls.

Mitigation: Require explicit human approval before kill switch activation or deactivation, and limit the Sardis API key to the intended wallets and permissions.

Risk: The release references an npm SDK dependency even though the artifact primarily documents curl and jq workflows.

Mitigation: Remove the SDK dependency if it is not required, or pin and review it before installation.

## Reference(s):

- [Sardis Website](https://sardis.sh)
- [Sardis Guardrails Documentation](https://sardis.sh/docs/guardrails)
- [Sardis API Reference](https://api.sardis.sh/v2/docs)
- [ClawHub Skill Page](https://clawhub.ai/efedurmaz16/skills/sardis-guardrails)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API calls, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SARDIS_API_KEY and uses curl and jq for command examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
