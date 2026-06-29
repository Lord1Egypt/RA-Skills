## Description: <br>
X Creat Agent standardizes OpenClaw agent creation by collecting agent details, running a creation script, generating workspace files, registering the agent, and optionally pairing a Feishu bot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snlcc](https://clawhub.ai/user/snlcc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create standardized OpenClaw agents, generate required workspace files, register agents in openclaw.json, and optionally configure Feishu bot pairing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu AppID and AppSecret can be written to openclaw.json as local credentials. <br>
Mitigation: Use a private terminal, avoid sharing command history or logs, and treat openclaw.json as sensitive. <br>
Risk: The creation script modifies local OpenClaw configuration and creates agent workspace files. <br>
Mitigation: Review the displayed path summary before confirming creation and run the script only in the intended OpenClaw home directory. <br>


## Reference(s): <br>
- [X Creat Agent on ClawHub](https://clawhub.ai/snlcc/x-creat-agent) <br>
- [Feishu agent creation](https://open.feishu.cn/page/launcher?from=backend_oneclick) <br>
- [Feishu bot creation](https://open.feishu.cn/page/openclaw?form=multiAgent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates OpenClaw workspace files and may update openclaw.json with Feishu credentials when supplied.] <br>

## Skill Version(s): <br>
1.2.14 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
