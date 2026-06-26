## Description: <br>
Generates CIS Benchmark-aligned security hardening configurations for Google Kubernetes Engine clusters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
DevOps engineers and security teams use this skill to request CIS Benchmark-aligned GKE hardening options and generate YAML configuration files for review before cluster deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests are sent to an external provider API with selected hardening options, session ID, timestamp, and optionally user ID. <br>
Mitigation: Do not include secrets or sensitive cluster details in option values, and use non-sensitive identifiers where possible. <br>
Risk: Generated Kubernetes configuration may not match every cluster policy or current CIS interpretation. <br>
Mitigation: Review generated YAML and test it in a non-production environment before applying it to a cluster. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-gke-hardening) <br>
- [GKE Hardening API Docs](https://api.mkkpro.com:8147/docs) <br>
- [GKE Hardening API Route](https://api.mkkpro.com/hardening/gke) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [JSON responses with generated YAML configuration file contents] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires hardeningOptions, sessionId, and timestamp; userId is optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
