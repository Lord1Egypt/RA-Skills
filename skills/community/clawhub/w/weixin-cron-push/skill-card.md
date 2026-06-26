## Description: <br>
Helps agents create OpenClaw cron tasks that send scheduled WeChat reminders, daily updates, and recurring notifications to a specific user through the openclaw-weixin channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gausshj](https://clawhub.ai/user/gausshj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure one-time, cron-based, or interval-based WeChat pushes through an existing openclaw-weixin setup. It is intended for reminders, weather updates, news summaries, and similar scheduled notifications routed by sessionKey. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session keys, user identifiers, and WeChat account JSON contents can route messages to specific users and should be treated as sensitive. <br>
Mitigation: Avoid exposing these values in logs, screenshots, shared prompts, or published examples; use placeholders in documentation and review generated commands before execution. <br>
Risk: A wrong sessionKey or account selection can create a task that sends messages to the wrong recipient or fails silently. <br>
Mitigation: Confirm the intended recipient and account before creating a cron task, and test routing with a low-impact message when configuring a new user. <br>
Risk: Recurring cron jobs can continue sending WeChat messages after they are no longer needed. <br>
Mitigation: Use delete-after-run for one-time reminders and periodically review or delete active cron jobs that are obsolete. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gausshj/weixin-cron-push) <br>
- [WeChat plugin API reference](references/weixin-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenClaw cron arguments, sessionKey routing guidance, and WeChat channel setup notes.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
