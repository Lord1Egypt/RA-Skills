## Description: <br>
拉取并展示「新闻联播」热点数据，按 source_name 分组列出标题，并可在用户确认后提供每日定时推送的 cron 创建命令。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xltang](https://clawhub.ai/user/xltang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query 新闻联播 hotspot headlines, view them by source, and check hotspot service status. With explicit approval, it can also provide an OpenClaw cron command for daily scheduled updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requests to hotspot.api4claw.com when users ask for hotspot data or service status. <br>
Mitigation: Confirm that the disclosed external service is acceptable before installing or running the skill. <br>
Risk: Optional scheduling can create a recurring OpenClaw cron job if the user approves it. <br>
Mitigation: Review the schedule, recipient, channel, and message before executing any cron registration command. <br>
Risk: Network failures or malformed API responses can make hotspot results unavailable or incomplete. <br>
Mitigation: Return an explicit failure or format-mismatch message and avoid fabricating hotspot content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xltang/xwlb) <br>
- [Hotspot API service](https://hotspot.api4claw.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with grouped headline lists, status text, and optional bash cron command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches current JSON data from the disclosed hotspot API when requested and does not persist identifiers by default.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
