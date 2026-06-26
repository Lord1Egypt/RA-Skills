## Description: <br>
Migrates local OpenClaw sub-agents to a VPS by guiding file sync, Discord bot configuration, bindings updates, gateway restarts, and local account disablement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sparkingskin-tech](https://clawhub.ai/user/sparkingskin-tech) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill when moving OpenClaw agents such as creative, dev, qa, strategist, or pojun from a local machine to a VPS while preserving Discord routing and avoiding duplicate local and remote responders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The migration handles live credentials, including SSH access and Discord bot tokens. <br>
Mitigation: Prefer SSH keys with verified host fingerprints, avoid putting passwords or tokens directly in commands, validate all substituted values, and rotate the Discord token after migration. <br>
Risk: Remote and local OpenClaw configuration changes can interrupt routing or create duplicate responders. <br>
Mitigation: Back up local and VPS configurations first, review bindings before restart, confirm the VPS agent is healthy, and disable the local account only after the cutover is verified. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses placeholders for VPS IP, Discord ID, agent ID, token, agent name, and password that users must replace before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
