## Description: <br>
Automates recurring Windows desktop WeChat group engagement workflows, including morning questions, afternoon follow-ups, and evening case posts for manually whitelisted groups with content pools, posting history, and OpenClaw cron scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinhuadeng](https://clawhub.ai/user/jinhuadeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External community operators and developers use this skill to schedule and run recurring engagement posts in manually whitelisted WeChat groups, including morning questions, afternoon follow-ups, and evening case posts. It supports dry runs, content pools, posting history, and OpenClaw cron scheduling for repeatable group operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real scheduled messages to WeChat groups through an external sender. <br>
Mitigation: Review the external wechat-desktop-sender script, confirm the logged-in WeChat account and group whitelist, and run dry runs before enabling real sends. <br>
Risk: Unattended cron jobs can post to configured groups on a recurring schedule. <br>
Mitigation: Enable cron only when unattended scheduled posts are acceptable for the whitelisted groups. <br>
Risk: Group names, message content, and posting history may contain sensitive operational information. <br>
Mitigation: Avoid storing sensitive group names or message content in content pools or the history file. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/jinhuadeng/wechat-group-operator) <br>
- [Actions](references/actions.md) <br>
- [Config](references/config.md) <br>
- [Cron setup](references/cron-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples; the runtime script emits JSON results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run previews and records post history.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
