## Description: <br>
Configure OpenClaw Feishu plugin without editing config files. Send simple commands via Feishu private chat to toggle streaming, set group reply behavior, run diagnostics, or restart the service. No CLI knowledge needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guanqi0914](https://clawhub.ai/user/guanqi0914) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw administrators and Feishu bot operators use this skill to inspect and change Feishu plugin settings from private chat, including streaming behavior, group reply behavior, diagnostics, and service restart. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trusted Feishu users can administer OpenClaw Feishu configuration from chat. <br>
Mitigation: Restrict who can message or invoke the bot before enabling this skill. <br>
Risk: State-changing commands can modify Feishu settings or restart the OpenClaw service without visible confirmation controls. <br>
Mitigation: Add confirmation for restart and other state-changing commands in production deployments. <br>
Risk: The skill uses Feishu credentials and caches a tenant token locally. <br>
Mitigation: Review local credential storage and the /tmp token handling before deployment. <br>
Risk: The security guidance calls out a generic shell execution helper as a risk. <br>
Mitigation: Remove it or restrict it with a tight allowlist before enabling the release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guanqi0914/wcs-helper-feishu-skill) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Feishu interactive card JSON with markdown text elements, plus command-line configuration actions executed by the skill] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw and a configured Feishu bot; several commands change local OpenClaw Feishu settings or request a service restart.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
