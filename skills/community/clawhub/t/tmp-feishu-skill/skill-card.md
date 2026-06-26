## Description: <br>
Guides users through creating a Feishu bot and connecting it to OpenClaw as a dedicated Agent in a Windows environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[song123-wq](https://clawhub.ai/user/song123-wq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create Feishu bots, bind them to separate Agents, configure local Windows workspaces, and validate message routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu App Secret or other credentials could be exposed if copied into chat, logs, screenshots, or memory files. <br>
Mitigation: Store secrets only in the intended protected configuration or secret store, avoid pasting them into shared surfaces, and rotate them if exposure is suspected. <br>
Risk: Windows paths and OpenClaw commands may not match a different local machine or OpenClaw installation. <br>
Mitigation: Confirm local paths, OpenClaw version, Gateway status, and Feishu event permissions before relying on the bot connection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/song123-wq/tmp-feishu-skill) <br>
- [Feishu Open Platform OpenClaw app creation](https://open.feishu.cn/page/openclaw?form=multiAgent) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with PowerShell command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Windows-specific OpenClaw paths and placeholders for Feishu App ID, App Secret, bot name, and Agent ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
