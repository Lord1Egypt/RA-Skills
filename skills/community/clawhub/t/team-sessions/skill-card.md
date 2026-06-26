## Description: <br>
主控发号施令、成员各司其职的团队沟通流程规范。零横向沟通，workspace 隔离，sessions_spawn 标准流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhao-zwl](https://clawhub.ai/user/zhao-zwl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to coordinate multi-agent team sessions with a main controller, isolated member workspaces, and standardized task handoff through sessions_spawn and sessions_send. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad sub-agent delegation can allow unintended agent IDs to be spawned if allowAgents is configured as a wildcard. <br>
Mitigation: Use explicit agent IDs instead of allowAgents wildcard wherever possible, and review the configured member list before enabling the skill. <br>
Risk: Changing OpenClaw configuration and restarting the gateway can disrupt routing or delegation behavior. <br>
Mitigation: Back up openclaw.json before editing, apply the smallest required configuration change, and keep a rollback path ready before restarting the gateway. <br>


## Reference(s): <br>
- [Team Sessions ClawHub Listing](https://clawhub.ai/zhao-zwl/team-sessions) <br>
- [README](README.md) <br>
- [Usage Examples](examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include OpenClaw configuration changes, workspace setup steps, and task delegation templates.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
