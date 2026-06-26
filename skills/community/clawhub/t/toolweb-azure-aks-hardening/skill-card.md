## Description: <br>
Generates CIS v1.8.0 compliant Azure Kubernetes Service (AKS) configurations for security hardening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
DevSecOps engineers, cloud architects, and security teams use this skill to request AKS hardening configurations aligned with CIS v1.8.0 controls and review the generated settings, warnings, and recommendations before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated AKS hardening settings may be incomplete or unsuitable for a specific cluster, workload, or regulatory environment. <br>
Mitigation: Review the returned configuration against the target AKS environment, CIS benchmark requirements, and organizational policy before deployment. <br>
Risk: Requests can include session identifiers, user identifiers, and timestamps that may be sensitive in some environments. <br>
Mitigation: Avoid sending secrets or unnecessary personal data in request fields and follow the API provider's data-handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-azure-aks-hardening) <br>
- [ToolWeb](https://toolweb.in) <br>
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/) <br>
- [AKS hardening API route](https://api.mkkpro.com/hardening/azure-aks) <br>
- [AKS hardening API docs](https://api.mkkpro.com:8149/docs) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, guidance, text] <br>
**Output Format:** [JSON responses with hardened AKS settings, compliance score, warnings, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The POST /api/aks/generate endpoint requires hardeningOptions and sessionId; userId and timestamp are optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
