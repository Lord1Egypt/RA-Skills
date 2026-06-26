## Description: <br>
Use when the task involves QJZD Nav CLI, including managing links, categories, tags, backups, settings, or authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nqdy666](https://clawhub.ai/user/nqdy666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this routing skill to choose the right QJZD Nav CLI domain skill and run top-level commands for authentication, content management, backups, settings, and shell completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to authenticate with QJZD Nav and use stored keyring credentials. <br>
Mitigation: Install and use only a trusted qjzd-nav binary, and select the intended profile before authentication or credential repair. <br>
Risk: Backup, restore, settings, and force operations can change or overwrite QJZD Nav data. <br>
Mitigation: Review generated commands before execution and reserve force or restore operations for confirmed targets. <br>


## Reference(s): <br>
- [QJZD Nav CLI ClawHub Page](https://clawhub.ai/nqdy666/qjzd-nav-cli) <br>
- [qjzd-nav-cli-auth](../qjzd-nav-cli-auth) <br>
- [qjzd-nav-cli-content](../qjzd-nav-cli-content) <br>
- [qjzd-nav-cli-operations](../qjzd-nav-cli-operations) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May point the agent to QJZD Nav domain skills and CLI help commands.] <br>

## Skill Version(s): <br>
1.3.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
