## Description: <br>
Interact with Tractus-X EDC (Eclipse Data Connector) control plane API v3 for managing assets, contract negotiations, policies, and data transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shibazishiye](https://clawhub.ai/user/shibazishiye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work with Tractus-X EDC control plane v3 APIs for assets, policies, contracts, negotiations, transfers, endpoint data references, business partner groups, and health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can create, update, delete, negotiate, or transfer EDC resources when run against a live control plane. <br>
Mitigation: Verify EDC_CONTROL_PLANE_URL and require explicit approval before executing mutating, negotiation, or transfer commands. <br>
Risk: A broad EDC API key can over-authorize agent-assisted administration. <br>
Mitigation: Use a least-privilege EDC_API_KEY scoped to the intended control-plane operations. <br>


## Reference(s): <br>
- [Tractus-X EDC Documentation](https://eclipse-tractusx.github.io/tractusx-edc/) <br>
- [Tractus-X EDC Control Plane API Specification](https://eclipse-tractusx.github.io/api-hub/tractusx-edc/0.12.0/control-plane/control-plane.yaml) <br>
- [ClawHub Skill Page](https://clawhub.ai/shibazishiye/tractusx-edc) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EDC_CONTROL_PLANE_URL and may use EDC_API_KEY depending on connector configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
