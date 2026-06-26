## Description: <br>
Team Projects helps OpenClaw users coordinate multi-agent work with project boards, work breakdown structures, @-mention routing, task dispatch, and a Control UI projects tab with Team Chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to plan, assign, dispatch, and track work across multiple OpenClaw agents. It is intended for coordinated projects where a lead agent manages phases, dependencies, task status, and inter-agent communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad agent allowlists and broad session visibility can expose more agents or sessions than a project requires. <br>
Mitigation: Replace wildcard allowlists with explicit project-team agents and avoid broad session visibility unless the deployment needs it. <br>
Risk: Source patches and local execution paths change OpenClaw UI and project-management behavior. <br>
Mitigation: Review the source patches before installing and rebuild only from reviewed files. <br>
Risk: Dashboard refresh through a silent sessions.send command can be under-scoped for read-only project status updates. <br>
Mitigation: Use a dedicated read-only project API for dashboard refresh behavior. <br>
Risk: The optional localhost HTTP API can mutate project data and is not suitable to enable without additional controls. <br>
Mitigation: Do not enable the optional localhost HTTP API unless authentication, restricted CORS, and clear mutation controls are added. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/maverick-software/team-projects) <br>
- [Team Projects Walkthrough](artifact/references/walkthrough.md) <br>
- [Example OpenClaw Configuration](artifact/references/example-config.json) <br>
- [Gateway Plugin Build Registration](artifact/gateway-plugin/BUILD_REGISTRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell command blocks, JavaScript and TypeScript files, and prompt templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional Control UI plugin files and local JSON project-state workflows.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
