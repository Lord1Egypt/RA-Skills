## Description: <br>
Generates hardened security configurations for Check Point systems based on specified hardening options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, security architects, compliance teams, and DevSecOps engineers use this skill to request JSON hardening profiles for Check Point appliances and gateways from selected encryption, access control, logging, and compliance options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends hardening request details and identifiers to an external provider. <br>
Mitigation: Use it only after approving the ToolWeb/api.mkkpro data flow, and avoid sending credentials, internal network details, or identifiable session values unless approved. <br>
Risk: Generated hardening output may be incomplete or unsuitable for a specific Check Point deployment. <br>
Mitigation: Have qualified security personnel review the generated configuration before applying it to production systems. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-checkpoint-hardening) <br>
- [ToolWeb](https://toolweb.in) <br>
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/) <br>
- [Check Point Hardening API route](https://api.mkkpro.com/hardening/checkpoint) <br>
- [API documentation](https://api.mkkpro.com:8143/docs) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Configuration, JSON, Guidance] <br>
**Output Format:** [JSON hardening profile and status response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a generated configuration identifier, hardening settings by category, applied rule count, and estimated deployment time.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
