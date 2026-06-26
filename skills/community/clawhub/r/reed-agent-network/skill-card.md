## Description: <br>
Build and operate a cross-gateway AgentNetwork using Discord as the message bus and GitHub as shared state storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reed1898](https://clawhub.ai/user/reed1898) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to coordinate agents across gateways, register and heartbeat agents, manage offline or remove actions, and synchronize a shared roster through Discord and GitHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent shared constitution or registry changes may steer future agent behavior. <br>
Mitigation: Use a controlled GitHub repository, review AGENT_CONSTITUTION.md before use, and require human approval before accepting constitution or registry changes as instructions. <br>
Risk: Discord and GitHub access may broadcast network messages or mutate shared state outside the intended trust boundary. <br>
Mitigation: Limit Discord and GitHub permissions, configure channels and repositories you control, and install only when intentionally joining this Reed AgentNetwork. <br>


## Reference(s): <br>
- [Git shared-state configuration](references/git-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown instructions with shell commands and JSON protocol messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update shared registry, constitution, and local memory index files when commands are run.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
