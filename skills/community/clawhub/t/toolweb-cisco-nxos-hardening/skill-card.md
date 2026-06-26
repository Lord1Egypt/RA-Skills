## Description: <br>
Generates security hardening configurations for Cisco NX-OS network devices based on specified options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network engineers, security architects, and DevOps teams use this skill to generate reviewable Cisco Nexus and NX-OS hardening configuration templates for selected security categories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated NX-OS commands may not match a specific network environment or change policy. <br>
Mitigation: Review all generated commands through normal network change control before applying them. <br>
Risk: Requests could expose sensitive internal topology, credentials, or identifiable user data to the hosted API. <br>
Mitigation: Do not include secrets or sensitive topology details, and use a pseudonymous or null userId when possible. <br>
Risk: A hosted provider endpoint can change or become unavailable outside the agent's control. <br>
Mitigation: Verify the provider endpoint and service behavior before relying on generated output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-cisco-nxos-hardening) <br>
- [ToolWeb](https://toolweb.in) <br>
- [ToolWeb portal](https://portal.toolweb.in) <br>
- [ToolWeb hub](https://hub.toolweb.in) <br>
- [OpenClaw page](https://toolweb.in/openclaw/) <br>
- [RapidAPI publisher profile](https://rapidapi.com/user/mkrishna477) <br>
- [API route](https://api.mkkpro.com/hardening/cisco-nxos) <br>
- [API docs](https://api.mkkpro.com:8137/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSON response containing Cisco NX-OS configuration commands organized by hardening category] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated commands are templates for review and change control, not direct device changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
