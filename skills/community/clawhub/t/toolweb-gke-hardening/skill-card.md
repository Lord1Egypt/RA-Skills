## Description:

Generates CIS Benchmark-aligned security hardening configurations for Google Kubernetes Engine clusters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, DevOps engineers, and security teams use this skill to generate GKE hardening configuration files and inspect available hardening options aligned with CIS Benchmark practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected hardening options, sessionId, timestamp, and optional userId may be sent to a third-party API service.

Mitigation: Use pseudonymous session identifiers, omit userId when possible, and avoid sending secrets, cluster credentials, or sensitive tenant details in option values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-gke-hardening)
- [API Docs](https://api.mkkpro.com:8147/docs)
- [Kong Route](https://api.mkkpro.com/hardening/gke)

## Skill Output:

**Output Type(s):** [API Calls, Configuration, Code, Guidance]

**Output Format:** [JSON responses containing generated configuration file names and YAML content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires hardening options, sessionId, and timestamp; optional userId may be included.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
