## Description: <br>
Generate and apply security hardening configurations for Google Kubernetes Engine AutoPilot clusters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
DevOps engineers, security teams, and infrastructure automation platforms use this skill to request repeatable hardening configurations for GKE Autopilot clusters, including network policies, RBAC controls, pod security standards, audit logging, and encryption at rest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests include session identifiers and may include user IDs or operational context. <br>
Mitigation: Use pseudonymous session IDs and avoid sending real user IDs or sensitive operational data unless the provider is approved for the environment. <br>
Risk: Generated Kubernetes manifests can affect cluster access, networking, logging, and encryption posture. <br>
Mitigation: Review generated manifests and hardening recommendations before applying them to any GKE Autopilot cluster. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-gke-autopilot-hardening) <br>
- [GKE Hardening API Docs](https://api.mkkpro.com:8145/docs) <br>
- [GKE Hardening API Route](https://api.mkkpro.com/hardening/gke-autopilot) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance, api calls] <br>
**Output Format:** [JSON responses and Markdown-facing API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated manifests and hardening recommendations should be reviewed before applying them to a GKE cluster.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
