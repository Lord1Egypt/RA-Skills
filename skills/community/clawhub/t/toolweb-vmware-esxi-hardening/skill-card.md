## Description:

Professional VMware ESXi 8.0 security configuration generator that produces hardened configuration files based on industry best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Infrastructure security teams, VMware administrators, compliance teams, and managed service providers use this skill to generate ESXi 8.0 hardening configurations for selected firewall, authentication, logging, and service controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote API requests may share sensitive identifiers through sessionId, userId, hostnames, credentials, or related request data.

Mitigation: Do not send internal conversation IDs, credentials, hostnames, or sensitive identifiers to the API.

Risk: Generated ESXi hardening configurations can affect host access, services, logging, firewall behavior, and authentication posture if applied directly.

Mitigation: Review and test generated configurations in a non-production environment with rollback access before applying them to real hosts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-vmware-esxi-hardening)
- [API Documentation](https://api.mkkpro.com:8146/docs)
- [Service Route](https://api.mkkpro.com/hardening/vmware-esxi)
- [OpenAPI Specification](artifact/openapi.json)

## Skill Output:

**Output Type(s):** [configuration, json, guidance]

**Output Format:** [JSON response containing generated hardening profiles, base64-encoded configuration files, and a summary of applied policies.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requests require hardeningOptions, sessionId, and timestamp, with optional userId.]

## Skill Version(s):

1.0.0 (source: server release evidence and openapi.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
