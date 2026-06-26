## Description: <br>
Tool Master helps an agent find command-line tools by searching a keyword-to-tool mapping table. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamwangli](https://clawhub.ai/user/iamwangli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to choose practical shell, development, data, system, network, and OpenClaw commands from a keyword-indexed catalog before executing a task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives broad command-selection guidance, including destructive, networked, Git, process, permission, service, backup, messaging, and OpenClaw administrative actions. <br>
Mitigation: Require explicit user confirmation before commands that delete or edit files, change permissions, kill processes, contact the network, change Git remotes or push, read OpenClaw sessions or config, change OpenClaw models/settings/skills, restore backups, restart services, or send messages. <br>
Risk: A suggested command may be incorrect for the current environment or broader than the user's intended task. <br>
Mitigation: Review command scope, arguments, current working directory, and expected side effects before execution; prefer read-only inspection commands when validating a tool choice. <br>


## Reference(s): <br>
- [Tool Master ClawHub page](https://clawhub.ai/iamwangli/tool-master) <br>
- [Publisher profile: iamwangli](https://clawhub.ai/user/iamwangli) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [tool_keyword_map.md](artifact/tool_keyword_map.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code] <br>
**Output Format:** [Markdown with inline shell commands and short explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest command examples from the keyword mapping table; commands still require normal agent and user safety review before execution.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
