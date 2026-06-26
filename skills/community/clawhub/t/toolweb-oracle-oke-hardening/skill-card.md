## Description: <br>
Professional OKE security configuration generator based on CIS Benchmark standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
DevOps engineers, cloud security architects, and Kubernetes administrators use this skill to generate Oracle Kubernetes Engine hardening configuration artifacts and recommendations aligned with CIS Benchmark practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests are handled by an external ToolWeb/api.mkkpro.com service, so sensitive cluster details could be exposed if included in prompts or API payloads. <br>
Mitigation: Avoid sending kubeconfigs, secrets, production identifiers, or detailed private cluster topology unless the provider's data handling practices have been approved. <br>
Risk: Generated hardening artifacts may not fully match a specific production OKE environment or organizational compliance policy. <br>
Mitigation: Review generated manifests, network policies, RBAC roles, audit policies, and recommendations before applying them to a cluster. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-oracle-oke-hardening) <br>
- [Oracle OKE Hardening API Route](https://api.mkkpro.com/hardening/oracle-oke) <br>
- [Oracle OKE Hardening API Docs](https://api.mkkpro.com:8148/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration, Guidance] <br>
**Output Format:** [JSON API response with generated Kubernetes manifests, network policies, RBAC roles, audit policies, hardening reports, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts may be base64-encoded.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
