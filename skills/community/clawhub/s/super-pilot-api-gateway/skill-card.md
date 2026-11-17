## Description:

Exposes local APIs to the Pilot Protocol network for remote agent access without public internet exposure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[molexazwo](https://clawhub.ai/user/molexazwo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to expose local API services to authorized Pilot Protocol agents and integrate private endpoints into Pilot-based agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gateway examples may expose local services to remote access without sufficient access-control guidance.

Mitigation: Restrict who can reach the gateway and add authentication, authorization, request validation, logging, and least-privilege service boundaries before using it with real local APIs.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl on PATH and a running Pilot Protocol daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
