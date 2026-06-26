## Description: <br>
Generates hardened Cisco ASA firewall configurations based on security best practices and specified hardening options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network administrators, security engineers, managed service providers, security consultants, and DevSecOps teams use this skill to draft repeatable Cisco ASA hardening configurations from selected hardening options and session metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ASA commands could be incomplete, incorrect, or unsuitable for a specific production firewall environment. <br>
Mitigation: Use the output as a draft and have a qualified network or security engineer review and test commands before applying them. <br>
Risk: Requests to the external API may expose identifiers or sensitive internal network context if users include them. <br>
Mitigation: Avoid sending real user identifiers, customer names, secrets, or sensitive internal network details unless the API provider is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-cisco-asa-hardening) <br>
- [API documentation](https://api.mkkpro.com:8142/docs) <br>
- [Kong route](https://api.mkkpro.com/hardening/cisco-asa) <br>
- [Publisher profile](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>
- [ToolWeb](https://toolweb.in) <br>
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Configuration, Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON response containing generated ASA settings, CLI command groups, applied option counts, deployment estimate, and timestamps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires hardeningOptions, sessionId, and timestamp; userId is optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
