## Description: <br>
Professional Ubuntu 22.04 LTS security configuration generator for STIG-compliant hardening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers, system administrators, and DevOps teams use this skill to generate Ubuntu 22.04 LTS hardening configurations for kernel, SSH, firewall, audit, account, file permission, and network controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hardening choices and tracking identifiers are sent to the provider API. <br>
Mitigation: Send only necessary identifiers and avoid personally identifying user IDs unless needed. <br>
Risk: Generated hardening configurations may disrupt access or services if applied without review. <br>
Mitigation: Review generated configurations, test outside production first, and keep rollback or console access available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-ubuntu-hardening-v2) <br>
- [Ubuntu Hardening API Docs](https://api.mkkpro.com:8129/docs) <br>
- [Ubuntu Hardening API Route](https://api.mkkpro.com/hardening/ubuntu-v2) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration, Shell commands, Guidance] <br>
**Output Format:** [JSON containing generated hardening settings, file metadata, command entries, and a download URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires hardeningOptions, sessionId, and timestamp; userId is optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
