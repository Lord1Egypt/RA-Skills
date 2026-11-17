## Description:

Generate and apply security hardening configurations for Google Kubernetes Engine AutoPilot clusters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, and security teams use this skill to request GKE Autopilot hardening guidance and generated Kubernetes configuration for network policies, RBAC controls, pod security standards, audit logging, and encryption at rest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send selected hardening options and request metadata to a third-party API.

Mitigation: Use pseudonymous session IDs and omit userId and timestamp unless they are required for the workflow.

Risk: Generated Kubernetes manifests may not match a specific cluster's policies, workload needs, or compliance baseline.

Mitigation: Review and test generated manifests before applying them to a GKE Autopilot cluster.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-gke-autopilot-hardening)
- [API Documentation](https://api.mkkpro.com:8145/docs)
- [API Route](https://api.mkkpro.com/hardening/gke-autopilot)
- [ToolWeb](https://toolweb.in)
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JSON responses containing generated Kubernetes hardening manifests, descriptions, status, and warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The API request includes hardening options, a session ID, and optional user ID and timestamp.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
