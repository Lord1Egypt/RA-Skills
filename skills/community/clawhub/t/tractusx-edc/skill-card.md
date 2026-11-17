## Description:

Interact with Tractus-X EDC (Eclipse Data Connector) control plane API v3 for managing assets, contract negotiations, policies, and data transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shibazishiye](https://clawhub.ai/user/shibazishiye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration engineers use this skill to prepare and run Tractus-X EDC control-plane API v3 commands for assets, policies, contract negotiation, transfers, EDR access, business partner groups, and health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands may mutate or delete EDC control-plane resources, initiate transfers, or expose EDR data addresses.

Mitigation: Review curl payloads before execution, use least-privilege EDC credentials, and run against the intended control-plane URL.

Risk: EDC_API_KEY may grant access to connector management operations.

Mitigation: Store the API key in an environment variable, limit credential scope where possible, and avoid pasting secrets into shared logs or transcripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shibazishiye/skills/tractusx-edc)
- [Tractus-X EDC Documentation](https://eclipse-tractusx.github.io/tractusx-edc/)
- [Tractus-X EDC Control Plane API Specification](https://eclipse-tractusx.github.io/api-hub/tractusx-edc/0.12.0/control-plane/control-plane.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash curl commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EDC_CONTROL_PLANE_URL and may require EDC_API_KEY depending on connector configuration.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
