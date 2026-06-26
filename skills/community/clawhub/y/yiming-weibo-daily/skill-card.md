## Description: <br>
张一鸣微博金句飞书私聊技能。安装后每小时推送一条张一鸣微博精选，附主题标签和今日练习。适用于安装、配置、试发和排查。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rocke1001feller](https://clawhub.ai/user/rocke1001feller) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to install and configure hourly Feishu private messages that send selected Zhang Yiming Weibo quotes with topic tags and a daily practice prompt. It also supports previewing, test-sending, and troubleshooting delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Feishu app credentials and a target open_id to send live private messages. <br>
Mitigation: Confirm the credential source, recipient open_id, and test message before sending; use a dedicated least-privilege Feishu app secret. <br>
Risk: The skill can enable recurring hourly delivery without enough explicit user control. <br>
Mitigation: Require explicit user approval for the hourly schedule and confirm how to disable the scheduled job before enabling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rocke1001feller/yiming-weibo-daily) <br>
- [Project homepage](https://github.com/Rocke1001feller/yiming-weibo-daily) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials and a target open_id for live sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and publish metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
