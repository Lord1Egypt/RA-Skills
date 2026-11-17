## Description:

Professional OKE security configuration generator based on CIS Benchmark standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, cloud security architects, and Kubernetes administrators use this skill to generate Oracle Kubernetes Engine hardening configurations, reports, and recommendations based on selected security controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends OKE hardening selections, sessionId, timestamp, and optional userId to an external provider API.

Mitigation: Confirm the data sharing is acceptable before use, and avoid sending sensitive identifiers unless they are required for the workflow.

Risk: Generated Kubernetes security configuration is advisory and may not match every cluster's operating requirements.

Mitigation: Review the generated manifests, policies, RBAC roles, audit settings, compliance score, and recommendations before applying them to a real OKE cluster.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-oracle-oke-hardening)
- [Kong route](https://api.mkkpro.com/hardening/oracle-oke)
- [API docs](https://api.mkkpro.com:8148/docs)
- [ToolWeb](https://toolweb.in)
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/)

## Skill Output:

**Output Type(s):** [Configuration, Code, Guidance]

**Output Format:** [JSON containing generated Kubernetes manifests, network policies, RBAC roles, audit policies, hardening reports, compliance scores, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts may be encoded strings returned by the provider API.]

## Skill Version(s):

1.0.0 (source: release evidence and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
