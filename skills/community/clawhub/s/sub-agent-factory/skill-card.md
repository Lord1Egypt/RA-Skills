## Description: <br>
Sub Agent Factory rapidly spawns and configures specialized sub-agents with templates for research, coding, and analysis plus workspace setup and instruction delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[balkanblbn](https://clawhub.ai/user/balkanblbn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to create role-specific sub-agent workspaces for coding, research, and analysis tasks. It provides setup guidance and a helper script that provisions inbox, outbox, workspace, and SKILL.md files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script can write files outside the intended agents folder when given a crafted agent name. <br>
Mitigation: Use simple agent names containing only letters, numbers, hyphens, or underscores, and avoid slashes or '..'. <br>
Risk: Generated role text and inbox contents become trusted instructions for the provisioned agent. <br>
Mitigation: Review role descriptions and inbox contents before using the generated agent. <br>
Risk: Running the helper script creates local directories and a SKILL.md file. <br>
Mitigation: Check the target path before provisioning and review the generated SKILL.md before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/balkanblbn/sub-agent-factory) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown instructions with shell command usage and generated SKILL.md files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script creates an agent directory with inbox, outbox, workspace, and SKILL.md files.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
