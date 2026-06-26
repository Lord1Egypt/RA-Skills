## Description: <br>
创建每分钟发送当前时间的QQ定时提醒任务，用于用户要求每分钟报时、定期收到时间提醒或测试定时任务功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eric331](https://clawhub.ai/user/eric331) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to create or cancel a QQ bot cron reminder that sends the current time to a selected QQ openid every minute. It is also suitable for validating basic scheduled-message behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reminder may run more frequently than the user expects because the artifact mentions hourly phrasing while the cron expression runs every minute. <br>
Mitigation: Confirm the intended cadence and timezone with the user before creating the cron task. <br>
Risk: A reminder can continue sending QQ bot messages until it is removed. <br>
Mitigation: Return and retain the cron task ID, and use it with the documented removal command when the user asks to cancel. <br>
Risk: Messages may be delivered to the wrong recipient if the openid is incorrect. <br>
Mitigation: Confirm the recipient openid before running the add command. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a QQ recipient openid, Asia/Shanghai timezone selection, and retention of the returned cron task ID for later cancellation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
